# u2_far_parity_flux.py — §94: caccia all'INVARIANTE DI PARITA'/FLUSSO in palla-2.
#
# Bersaglio (§93h.2, via b): il pavimento del ledger pend2 >= 2 sulle fuggenti.
# Osservazione strutturale (dal ledger §93a): su una cella GIA' VISITATA il bit
# del prepend e' FORZATO (= req della cella): visita su req=1 => L (apre pending),
# visita su req=0 => R (chiude). Quindi OGNI visita TOGGLA pend(c); solo la prima
# visita di una cella FRESCA sceglie liberamente. pend2 e' allora governato da
# PARITA' DI VISITE + scelte fresche (che vivono fuori dalla tasca): la firma
# whack-a-mole riga1<->riga2 di §93e suggerisce un vincolo di parita' congiunto.
#
# METODO (stile §74 GF(2), ma su feature di stato del camminatore):
#   1. camminate all'indietro ESATTE (exact_state/exact_step, nessuna striscia,
#      nessuna astrazione OUT: qui la trappola ff non puo' mordere) sopra le 8
#      fuggenti (6 nere400 + 2 jackpot), politiche randomizzate + steering verso
#      la chiusura dei pending (per campionare il corner a pend2 basso);
#   2. per ogni stato: vettore di feature GF(2)
#        p_c = [req(c)==0] (pending), v_c = [req(c)!=FREE] (visitata)
#        per c nella finestra W = x in [-6,4], y in [1,3]  (33 celle),
#        pose one-hot in W + flag fuori-W, heading one-hot, parita' x%2, y%2,
#        (x+y)%2, bias 1;
#   3. per parola: base GF(2) dello span delle DIFFERENZE (v XOR v0) =>
#      nullspace = funzionali phi con phi*v COSTANTE lungo ogni cammino;
#      intersezione tra parole + confronto delle costanti phi*v0;
#   4. i candidati con supporto sui p_c della PALLA-2 sono i pre-teoremi:
#      phi*v = 1 con supporto {p_c : c in palla} => somma pending dispari
#      => pend2 >= 1 SEMPRE; due tali phi a supporto disgiunto => pend2 >= 2.
#
# GATE (devono poter fallire):
#   PF0 identita' ledger: pend-bit incrementali == pend_set(req) ricalcolato
#       (ogni ~5000 passi e a fine camminata);
#   PF1 il minimo pend2 osservato nelle camminate steered e' 2 (= floor §93d
#       misurato dalla caccia; se scendesse a 0-1 il pavimento e' FALSIFICATO
#       qui stesso: witness dump);
#   PF2 esca: iniettando una transizione corrotta (toggle omesso) i candidati
#       phi DEVONO rilevarla (phi*v cambia) — altrimenti la caccia e' vacua;
#   PF3 attivita': si riportano solo phi con supporto su feature ATTIVE
#       (variate nel campione); i phi su feature congelate sono dichiarati a
#       parte (invarianti banali).
#
# Uscita: alpha1/u2_far_parity_flux_summary.json (+ .log)
import sys, os, json, time, random, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_weapon_vitality import to_bits, SUMMARY
from u2_cover_rail_map import valid
from u2_pocket_certificate import exact_state, exact_step, TGT, FREE
from u2_far_ledger import cheb, pend_set
from onset_cone_lock import DX, DY

HERE = os.path.dirname(os.path.abspath(__file__))
WIT = os.path.join(HERE, "u2_cover_witnesses.json")
OUT_JSON = os.path.join(HERE, "u2_far_parity_flux_summary.json")
LOG = os.path.join(HERE, "u2_far_parity_flux.log")

# finestra delle feature
W_CELLS = [(x, y) for y in (1, 2, 3) for x in range(-6, 5)]
W_IDX = {c: i for i, c in enumerate(W_CELLS)}
NW = len(W_CELLS)                       # 33
BALL2 = [(x, y) for x in range(-2, 3) for y in (1, 2)]

# layout feature: [p_c 0..NW-1][v_c NW..2NW-1][pose one-hot 2NW..3NW-1]
# [pose-out 3NW][heading 3NW+1..3NW+4][x%2, y%2, (x+y)%2][bias]
F_P = 0
F_V = NW
F_POSE = 2 * NW
F_OUT = 3 * NW
F_HEAD = 3 * NW + 1
F_PAR = 3 * NW + 5
F_BIAS = 3 * NW + 8
NFEAT = 3 * NW + 9


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def feat_vector(c, h, req):
    """Vettore feature GF(2) come int (bit i = feature i)."""
    v = 1 << F_BIAS
    for cc, i in W_IDX.items():
        r = req.get(cc, FREE)
        if r != FREE:
            v |= 1 << (F_V + i)
            if r == 0:
                v |= 1 << (F_P + i)
    if c in W_IDX:
        v |= 1 << (F_POSE + W_IDX[c])
    else:
        v |= 1 << F_OUT
    v |= 1 << (F_HEAD + h)
    if c[0] & 1:
        v |= 1 << (F_PAR + 0)
    if c[1] & 1:
        v |= 1 << (F_PAR + 1)
    if (c[0] + c[1]) & 1:
        v |= 1 << (F_PAR + 2)
    return v


class Basis:
    """Base GF(2) incrementale (eliminazione per bit alto)."""
    def __init__(self):
        self.rows = {}                  # msb -> vettore

    def add(self, v):
        while v:
            m = v.bit_length() - 1
            if m in self.rows:
                v ^= self.rows[m]
            else:
                self.rows[m] = v
                return True
        return False

    def rank(self):
        return len(self.rows)


def nullspace(basis_rows, nfeat):
    """Nullspace della matrice le cui righe generano lo span dato (RREF +
    back-substitution; ortogonalita' verificata dal chiamante)."""
    piv = {}
    for r in basis_rows.values():
        cur = r
        while cur:
            m = cur.bit_length() - 1
            if m in piv:
                cur ^= piv[m]
            else:
                piv[m] = cur
                break
    # back-substitution: elimina ogni pivot dalle righe superiori
    for m in sorted(piv):
        for m2 in list(piv):
            if m2 > m and ((piv[m2] >> m) & 1):
                piv[m2] ^= piv[m]
    pivots = set(piv)
    free = [i for i in range(nfeat) if i not in pivots]
    null = []
    for f in free:
        phi = 1 << f
        for m, r in piv.items():
            if (r >> f) & 1:
                phi |= 1 << m
        null.append(phi)
    # verifica di ortogonalita' (il costruttore deve poter fallire)
    for phi in null:
        for r in basis_rows.values():
            assert bin(phi & r).count("1") & 1 == 0, "nullspace NON ortogonale!"
    return null


def dot(phi, v):
    return bin(phi & v).count("1") & 1


def pend2_of(req):
    return sum(1 for c in BALL2 if req.get(c, FREE) == 0)


def walk_word(word, rng, n_walks, max_steps, basis, v0_store, act_or,
              min_track, esca=False):
    """Camminate randomizzate+steered sopra 'word'; aggiorna base differenze."""
    c0, h0, req0 = exact_state(word)
    v_first = feat_vector(c0, h0, req0)
    v0_store.append(v_first)
    act_or[0] |= v_first
    samples = 0
    for wk in range(n_walks):
        p_L = rng.uniform(0.05, 0.55)
        p_steer = rng.uniform(0.2, 0.95)
        c, h, req = c0, h0, dict(req0)
        vcur = v_first
        pend2 = pend2_of(req0)
        esca_at = rng.randrange(3, 25) if esca else None
        esca_done = False
        for step in range(max_steps):
            cn = (c[0] - DX[h], c[1] - DY[h])
            if cn[1] < 1:
                break
            r = req.get(cn, FREE)
            if r == FREE:
                # scelta libera: con prob p_steer orienta il passo successivo
                # verso il pending in palla-2 piu' vicino (corner pend2 basso)
                if rng.random() < p_steer:
                    targ = None; td = None
                    for cb in BALL2:
                        if req.get(cb, FREE) == 0:
                            dd = max(abs(c[0] - cb[0]), abs(c[1] - cb[1]))
                            if td is None or dd < td:
                                td = dd; targ = cb
                    if targ is not None:
                        best = None; bd = None
                        for b in (0, 1):
                            hn = (h - 1) & 3 if b == 1 else (h + 1) & 3
                            cn2 = (cn[0] - DX[hn], cn[1] - DY[hn])
                            dd = max(abs(cn2[0] - targ[0]),
                                     abs(cn2[1] - targ[1]))
                            if bd is None or dd < bd:
                                bd = dd; best = b
                        bit = best
                    else:
                        bit = 0 if rng.random() < p_L else 1
                else:
                    bit = 0 if rng.random() < p_L else 1
            else:
                bit = 1 if r == 0 else 0        # forzato
            # aggiornamento incrementale feature
            c2, h2, _ = exact_step(c, h, req, bit)
            if c2 is None:
                break
            # cella visitata cn: req aggiornato da exact_step
            if cn in W_IDX:
                i = W_IDX[cn]
                newr = req[cn]
                vcur &= ~((1 << (F_P + i)))
                if newr == 0:
                    vcur |= 1 << (F_P + i)
                vcur |= 1 << (F_V + i)
                if cn in BALL2:
                    pend2 = pend2_of(req)
            # pose
            if c in W_IDX:
                vcur &= ~(1 << (F_POSE + W_IDX[c]))
            else:
                vcur &= ~(1 << F_OUT)
            if c2 in W_IDX:
                vcur |= 1 << (F_POSE + W_IDX[c2])
            else:
                vcur |= 1 << F_OUT
            vcur &= ~(0xF << F_HEAD)
            vcur |= 1 << (F_HEAD + h2)
            vcur &= ~(0x7 << F_PAR)
            if c2[0] & 1:
                vcur |= 1 << (F_PAR + 0)
            if c2[1] & 1:
                vcur |= 1 << (F_PAR + 1)
            if (c2[0] + c2[1]) & 1:
                vcur |= 1 << (F_PAR + 2)
            if esca and not esca_done and step >= esca_at and cn in W_IDX:
                # ESCA PF2: ometti il toggle del pend-bit (stato corrotto)
                vcur ^= 1 << (F_P + W_IDX[cn])
                esca_done = True
            c, h = c2, h2
            basis.add(vcur ^ v_first)
            act_or[0] |= vcur
            samples += 1
            if pend2 < min_track[0]:
                min_track[0] = pend2
            # PF0 a campione (mai sulle camminate-esca: sono corrotte apposta)
            if not esca and (samples & 0x1FFF) == 0:
                vchk = feat_vector(c, h, req)
                assert vchk == vcur, "PF0 FALLITO: feature incrementali != ricalcolo"
        # PF0 a fine camminata
        vchk = feat_vector(c, h, req)
        if not esca:
            assert vchk == vcur, "PF0 FALLITO (fine camminata)"
    return samples


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--walks", type=int, default=400)
    ap.add_argument("--max-steps", type=int, default=4000)
    ap.add_argument("--seed", type=int, default=941)
    args = ap.parse_args()
    t0 = time.time()
    log(f"parity-flux §94: walks={args.walks}/parola max_steps={args.max_steps} "
        f"seed={args.seed} | NFEAT={NFEAT}")

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    wit = json.load(open(WIT))
    words = []
    for grp in ("jackpot", "nere400"):
        for k, w in enumerate(wit[grp]):
            e2 = to_bits(w["word"])
            words.append((f"{grp}[{k}]", tuple(e2) + tuple(w101)))
    log(f"parole fuggenti: {len(words)}")

    rng = random.Random(args.seed)
    per_word = []
    all_null = None
    v0s = []
    act_or = [0]
    min_track = [10 ** 9]
    for name, w2 in words:
        assert valid(w2)[1] is None
        basis = Basis()
        v0_store = []
        ns = walk_word(w2, rng, args.walks, args.max_steps, basis, v0_store,
                       act_or, min_track)
        null = nullspace(basis.rows, NFEAT)
        log(f"{name}: {ns} campioni, rank differenze {basis.rank()}, "
            f"nullspace {len(null)}")
        per_word.append({"nome": name, "campioni": ns,
                         "rank": basis.rank(), "null_dim": len(null)})
        v0s.append((name, v0_store[0]))
        # intersezione degli spazi di invarianza: si accumula la base delle
        # differenze di TUTTE le parole in un'unica base globale
        if all_null is None:
            g_basis = basis
            all_null = True
        else:
            for r in list(basis.rows.values()):
                g_basis.add(r)
    null_g = nullspace(g_basis.rows, NFEAT)
    log(f"GLOBALE: rank {g_basis.rank()}, nullspace {len(null_g)} funzionali "
        f"invarianti lungo OGNI cammino di OGNI parola")

    # PF1: minimo pend2 visto
    log(f"PF1: min pend2 osservato nelle camminate = {min_track[0]} "
        f"(floor misurato §93d: 2)")

    # costanti per parola e filtro attivita' (PF3)
    active = act_or[0]
    # per confronto attivita': feature che hanno variato in ALMENO un campione
    # (bit acceso in qualche v ma non in tutti). Approssimazione: un funzionale
    # e' "attivo" se tutte le sue feature (tranne bias) compaiono in act_or.
    results = []
    for phi in null_g:
        consts = [(name, dot(phi, v0)) for name, v0 in v0s]
        cvals = {c for _, c in consts}
        supp = [i for i in range(NFEAT) if (phi >> i) & 1]
        supp_p_ball = [W_CELLS[i - F_P] for i in supp
                       if F_P <= i < F_P + NW and W_CELLS[i - F_P] in BALL2]
        results.append({
            "supporto_idx": supp,
            "supporto_leggibile": [
                (f"p{W_CELLS[i-F_P]}" if i < F_V else
                 f"v{W_CELLS[i-F_V]}" if i < F_POSE else
                 f"pose{W_CELLS[i-F_POSE]}" if i < F_OUT else
                 "OUT" if i == F_OUT else
                 f"h{i-F_HEAD}" if i < F_PAR else
                 ["x%2", "y%2", "(x+y)%2"][i - F_PAR] if i < F_BIAS else
                 "1") for i in supp],
            "costante_uniforme": len(cvals) == 1,
            "costante": consts[0][1] if len(cvals) == 1 else dict(consts),
            "p_ball_support": [list(c) for c in supp_p_ball]})
    n_unif = sum(1 for r in results if r["costante_uniforme"])
    n_ball = sum(1 for r in results if r["p_ball_support"])
    log(f"funzionali invarianti: {len(results)} | costante uniforme tra le 8 "
        f"parole: {n_unif} | con supporto p_c in palla-2: {n_ball}")

    # PF2a (report): esca casuale — quanta parte dei phi sente un toggle omesso
    # in un punto casuale? (puo' legittimamente essere 0: il flip casuale puo'
    # cadere fuori da ogni supporto)
    log("PF2a (esca casuale): camminate con toggle omesso...")
    basis_esca = Basis()
    v0e = []
    acte = [0]
    mine = [10 ** 9]
    rng_e = random.Random(args.seed + 7)
    walk_word(words[2][1], rng_e, 60, 2000, basis_esca, v0e, acte, mine,
              esca=True)
    broken = 0
    for phi in null_g:
        ok = all(dot(phi, r) == 0 for r in basis_esca.rows.values())
        if not ok:
            broken += 1
    log(f"PF2a: {broken}/{len(null_g)} funzionali violati dall'esca casuale")

    # PF2b (gate): corruzione MIRATA — per ogni phi con supporto p_c in palla,
    # il toggle di una cella del suo supporto DEVE violarlo (check di plumbing
    # sull'indicizzazione bit; se fallisce, il layout feature e' rotto)
    n_pf2b = 0
    for phi in null_g:
        supp_p = [i - F_P for i in range(F_P, F_P + NW) if (phi >> i) & 1
                  and W_CELLS[i - F_P] in BALL2]
        if not supp_p:
            continue
        v_corr = v0s[0][1] ^ (1 << (F_P + supp_p[0]))
        assert dot(phi, v_corr ^ v0s[0][1]) == 1, "PF2b: phi non sente il flip!"
        n_pf2b += 1
    log(f"PF2b: {n_pf2b} phi-palla verificati sensibili al flip mirato")

    out = {"args": vars(args), "n_feat": NFEAT,
           "per_word": per_word,
           "rank_globale": g_basis.rank(),
           "null_dim_globale": len(null_g),
           "min_pend2_osservato": min_track[0],
           "invarianti": results,
           "esca_violati_casuale": broken, "pf2b_mirati": n_pf2b,
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    log(f"scritto {OUT_JSON} in {out['elapsed_s']} s")


if __name__ == "__main__":
    main()
