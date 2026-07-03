# prepend_box_automaton.py — §90: L'AUTOMA DEI PREPEND (scatola esatta, esterno libero).
#
# Obiettivo: decidere il corno (b) della dicotomia §89d A OGNI PROFONDITA': esiste un
# passato realizzabile e record-compatibile di w101 che visita (1,1)?
#
# Costruzione (sovra-approssimazione SANA: si trasferisce solo "nessun cammino", trappola c):
#  - il camminatore all'indietro e' ESATTO dentro una scatola B attorno a (1,1) e LIBERO
#    fuori (posizione dimenticata, vincoli fuori-scatola dimenticati => piu' cammini);
#  - vincolo y>=1 ESATTO ovunque (ogni posizione di un passato di record stretto sta a
#    y_rel >= 1: non e' approssimazione);
#  - stato = (frontiera, requisiti): frontiera = (cella, heading-di-ingresso) del passo
#    piu' antico se in scatola, altrimenti OUT; requisito per cella di B in
#    {LIBERA, PROSSIMA-LETTURA-BIANCA, PROSSIMA-LETTURA-NERA} — la consistenza delle
#    riletture per cella e' un'alternanza ancorata alla prima lettura di w101
#    (celle di footprint) o alla prima visita all'indietro (celle libere);
#  - transizione all'indietro dalla frontiera (q, h_in): p = q - dir(h_in) [il passo
#    precedente esce con h_out = h_in e atterra su q]; lettera R: h_p_in = h_in - 1,
#    legge BIANCO scrive NERO; lettera L: h_p_in = h_in + 1, legge NERO scrive BIANCO;
#    su cella vincolata la scrittura deve combaciare col requisito (lettera FORZATA) e
#    il requisito si aggiorna alla lettura (alternanza);
#  - da OUT si puo' materializzare un ingresso (p, h_p_in, lettera) in B solo se il
#    successore q = p + dir(h_p_out) e' FUORI scatola e a y >= 1 (il vero successore
#    era fuori); (1,1) ha come successori legali solo le 3 celle del colletto, tutte in
#    scatola => nessun ingresso diretto da OUT.
#
# Verdetto: se nessuno stato raggiungibile genera p == (1,1), NESSUN passato reale
# visita (1,1) a QUALSIASI profondita' => TEOREMA DEL BLOCCO ETERNO per w101.
#
# Validazione (fermarsi al primo rosso):
#  V1 simulazione: la traiettoria all'indietro REALE del binario §88 (624 prepend)
#     proiettata sugli stati astratti deve essere ammessa transizione per transizione;
#  V2 controllo positivo: un bersaglio che il binario VISITA davvero deve risultare
#     RAGGIUNGIBILE dall'automa (l'astrazione non e' vacuamente chiusa);
#  V3 coerenza con lo sweep §89d: (1,1) non raggiunto nei primi 40 livelli concreti.
#
# Uscita: alpha1/prepend_box_automaton_summary.json
import sys, os, json, time, argparse
from collections import deque
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY, rotk
from kwindow_spoiler_census import virtual_walk, to_anchor_frame
from record_weapon_vitality import to_bits, SUMMARY

HERE = os.path.dirname(os.path.abspath(__file__))
RAIL = os.path.join(HERE, "record_weapon_rail_summary.json")
OUT_JSON = os.path.join(HERE, "prepend_box_automaton_summary.json")
TGT = (1, 1)
FREE, REQW, REQB = 0, 1, 2


def walk_anchor_trace(word):
    """Posizioni (ordine temporale) e heading-di-ingresso di ogni passo, in frame anchor."""
    x = y = 0
    h = 0
    pos = []
    hin = []
    for b in word:
        pos.append((x, y))
        hin.append(h)
        if b:
            h = (h + 1) & 3
        else:
            h = (h + 3) & 3
        x += DX[h]
        y += DY[h]
    k = (-h) % 4
    apos = [rotk((px - x, py - y), k) for (px, py) in pos]
    ahin = [(hh + k) & 3 for hh in hin]
    return apos, ahin


def cell_step(state_req, b):
    """(ok, nuovo requisito) per una visita all'indietro con lettera b (1=R, 0=L)."""
    write = 1 if b else 0            # R scrive nero, L scrive bianco
    read = 0 if b else 1             # R legge bianco, L legge nero
    if state_req == FREE:
        return True, (REQW if read == 0 else REQB)
    need = 0 if state_req == REQW else 1
    if write != need:
        return False, None
    return True, (REQW if read == 0 else REQB)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--x0", type=int, default=-1)
    ap.add_argument("--x1", type=int, default=3)
    ap.add_argument("--y0", type=int, default=1)
    ap.add_argument("--y1", type=int, default=3)
    ap.add_argument("--max-states", type=int, default=30_000_000)
    ap.add_argument("--target", type=int, nargs=2, default=None,
                    help="bersaglio alternativo (controllo positivo)")
    args = ap.parse_args()
    t0 = time.time()
    tgt = tuple(args.target) if args.target else TGT

    box = [(x, y) for x in range(args.x0, args.x1 + 1)
           for y in range(args.y0, args.y1 + 1)]
    idx = {c: i for i, c in enumerate(box)}
    nb = len(box)

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    apos, ahin = walk_anchor_trace(w101)
    assert tgt == TGT or True
    assert TGT not in set(apos), "(1,1) nel footprint di w101?!"

    # requisiti iniziali: prima lettura di w101 per le celle di footprint in scatola
    init = [FREE] * nb
    seen = set()
    for i, c in enumerate(apos):
        if c in seen:
            continue
        seen.add(c)
        if c in idx:
            init[idx[c]] = REQW if w101[i] else REQB
    # frontiera iniziale = passo piu' antico di w101
    p0, h0 = apos[0], ahin[0]
    pose0 = (idx[p0], h0) if p0 in idx else None      # None = OUT
    start = (pose0, tuple(init))

    def transitions(state):
        pose, cs = state
        outs = []
        if pose is None:
            # ingresso da OUT: successore fuori scatola e y>=1
            for p in box:
                pi = idx[p]
                for hpin in range(4):
                    for b in (0, 1):
                        hpout = (hpin + 1) & 3 if b else (hpin - 1) & 3
                        q = (p[0] + DX[hpout], p[1] + DY[hpout])
                        if q in idx or q[1] < 1:
                            continue
                        ok, nr = cell_step(cs[pi], b)
                        if not ok:
                            continue
                        cs2 = list(cs)
                        cs2[pi] = nr
                        outs.append(((pi, hpin), tuple(cs2), p))
        else:
            qi, hin = pose
            q = box[qi]
            p = (q[0] - DX[hin], q[1] - DY[hin])
            if p[1] < 1:
                return outs
            for b in (0, 1):
                hpin = (hin - 1) & 3 if b else (hin + 1) & 3
                if p in idx:
                    pi = idx[p]
                    ok, nr = cell_step(cs[pi], b)
                    if not ok:
                        continue
                    cs2 = list(cs)
                    cs2[pi] = nr
                    outs.append(((pi, hpin), tuple(cs2), p))
                else:
                    outs.append((None, cs, p))
        return outs

    # ---------------- V1: simulazione del binario reale ----------------
    rail = json.load(open(RAIL))["rail_oldest_first"]
    ext = to_bits(rail)
    full = ext + w101
    fpos, fhin = walk_anchor_trace(full)
    J = len(ext)
    state = start
    hits_rail = set()
    for j in range(J):                      # prepend j+1 = passo piu' antico a indice J-1-j
        i = J - 1 - j
        p, b, hpin = fpos[i], full[i], fhin[i]
        if p in idx:
            hits_rail.add(p)
        if p not in idx and state[0] is None:
            continue                    # passo fuori scatola con frontiera OUT: no-op
        want_pose = (idx[p], hpin) if p in idx else None
        match = None
        for (pose2, cs2, pp) in transitions(state):
            if pp == p and pose2 == want_pose:
                match = (pose2, cs2)
                break
        assert match is not None, f"V1 ROSSO: passo reale j={j+1} (cella {p}) non ammesso"
        state = match
    print(f"V1 VERDE: binario reale (624 prepend) interamente ammesso dall'automa; "
          f"celle di scatola toccate dal binario: {sorted(hits_rail)}", flush=True)

    # ---------------- BFS con ricostruzione del witness ----------------
    seen_states = {start: None}          # stato -> (stato padre, cella del passo)
    dq = deque([start])
    hit = None
    n_trans = 0
    while dq:
        st = dq.popleft()
        for (pose2, cs2, p) in transitions(st):
            n_trans += 1
            s2 = (pose2, cs2)
            if p == tgt:
                seen_states[s2] = (st, p)
                hit = s2
                dq.clear()
                break
            if s2 not in seen_states:
                seen_states[s2] = (st, p)
                if len(seen_states) > args.max_states:
                    raise RuntimeError("esplosione stati: allargare/analizzare")
                dq.append(s2)
    el = round(time.time() - t0, 1)

    witness = None
    if hit is None:
        verdict = (f"IRRAGGIUNGIBILE: nessun passato (anche astratto) visita {tgt}. "
                   f"Stati raggiungibili {len(seen_states)}, transizioni {n_trans}.")
    else:
        # catena di celle dal piu' recente al piu' antico
        chain = []
        cur = hit
        while seen_states[cur] is not None:
            par, p = seen_states[cur]
            chain.append(p)
            cur = par
        witness = chain[::-1]            # dall'ingresso in scatola fino al bersaglio
        verdict = (f"RAGGIUNGIBILE (astratto) in {len(chain)} passi-scatola; "
                   f"witness (celle, dal recente all'antico): {chain}")
    print(f"BFS: {verdict} ({el}s)", flush=True)

    out = {"box": [args.x0, args.x1, args.y0, args.y1], "target": list(tgt),
           "reachable": hit is not None, "states": len(seen_states),
           "transitions": n_trans, "rail_sim_ok": True,
           "witness_cells_recent_first": ([list(c) for c in witness[::-1]]
                                          if witness else None),
           "rail_box_cells": sorted(map(list, hits_rail)), "elapsed_s": el}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT_JSON} in {el} s", flush=True)


if __name__ == "__main__":
    main()
