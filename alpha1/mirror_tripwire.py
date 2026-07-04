# mirror_tripwire.py — §96: il TRIPWIRE SPECCHIO ("CP" della formica).
#
# SIMMETRIA ESATTA (proposta Michael §96, dall'analogia con la violazione di
# parita' debole): la dinamica della formica e' massimalmente chirale (R su
# bianco, L su nero) — lo specchio P da solo NON e' una simmetria, ma
# specchio + scambio R<->L ("CP") lo E': riflettendo il piano (x -> -x) e
# scambiando le svolte, un'orbita valida va in un'orbita valida con la stessa
# struttura (stessi onset, stessi conteggi, geometrie riflesse).
#
# Involuzione M:
#   celle:   (x, y) -> (-x, y)
#   heading: 0(su)<->0, 2(giu)<->2, 1(dx)<->3(sx)
#   bit:     R(1) <-> L(0)   [convenzione §95: bit 1 = R = lettura bianca]
#
# USO: self-test GRATUITO contro i bug di frame (§86.6, §89c: gia' costati
# cari). Ogni certificato/enumeratore del progetto, eseguito nell'universo
# riflesso, deve produrre output bit-identici dopo ri-riflessione.
# NB (onesta'): il tripwire NON riduce i problemi chirali (w101, il record,
# le firme dell'oracolo sono oggetti chirali: lo specchio li manda nella
# famiglia della formica speculare, non in se stessi) — verifica la
# COERENZA DI FRAME del codice, non dimezza il lavoro.
#
# GATE (fermarsi al primo rosso):
#   M0 dinamica forward: orbita di seme riflesso == riflessione dell'orbita,
#      con parola R<->L scambiata; onset griglia vuota = 9977 in entrambi gli
#      universi (griglia vuota e' P-simmetrica);
#   M1 esca: lo scambio bit SENZA riflessione delle celle DEVE divergere
#      (P da sola e' violata — il checker sa fallire);
#   M2 exact_state/pend2: per le 10 parole controesempio §94, lo stato del
#      camminatore all'indietro commuta con M — ATTENZIONE (lezione in-run,
#      precisazione CP): scambiare i BIT senza scambiare la REGOLA non e' la
#      simmetria. exact_state interpreta ogni parola con la regola standard
#      (bit R <=> read bianca): sulla parola riflessa produce il mondo a
#      COLORI INVERTITI (misurato: 256/256 req flippate sul controesempio 0,
#      posa/heading pero' coniugati — la geometria e' color-cieca). La
#      coniugazione giusta usa l'interprete a chiralita' SPECCHIO (read=bit):
#      allora posa, heading, req E pend2 commutano esattamente con M. Il
#      gate verifica: (i) interprete specchio == exact_state sul mondo
#      standard ri-riflesso; (ii) coniugazione esatta; (iii) ESCA: il
#      bit-swap nudo DEVE flippare tutte le req. LIMITE NOTO (pannello §96):
#      gli heading di posa dei 10 controesempi sono quasi tutti dispari
#      (3,3,...,1): M2 non esercita le voci PARI di m_head — una corruzione
#      0<->2 e' coperta SOLO da M0 (che la becca al primo seme). Per rendere
#      M2 autonomo servirebbe un controesempio a heading pari nel set;
#   M3 clean_subtree: enumeratore parametrizzato per chiralita' (in-script):
#      versione standard riproduce i numeri §95 (sottoalbero pulito VUOTO),
#      versione specchio sulla parola riflessa = immagine speculare esatta;
#   M4 oracolo: PRECISAZIONE in-run (seconda lezione CP della sessione) —
#      l'oracolo §95d e' intrinsecamente CHIRALE (il tratto confinato e' uno
#      spiral all-R, che curva da una parte sola): le 15 firme-exit NON sono
#      M-chiuse in se' (misurato: differenza simmetrica 12 firme — l'ipotesi
#      ingenua era FALSA). La coniugazione giusta: exit_set(oracolo specchio)
#      == M(exit_set(oracolo standard)), verificata con l'oracolo
#      parametrizzato per chiralita'.
#
# Uscita: alpha1/mirror_tripwire_summary.json
import sys, os, json, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY, simulate, onset_verified
from record_weapon_vitality import to_bits, to_str, SUMMARY
from u2_cover_rail_map import valid
from u2_pocket_certificate import exact_state, FREE
from u2_far_ledger import cheb, pend_set
from u2_far_clean_stretch import clean_subtree, pend2_of

HERE = os.path.dirname(os.path.abspath(__file__))
CEX = os.path.join(HERE, "u2_far_pend2_counterexamples.json")
ORC = os.path.join(HERE, "u2_far_clean_oracle_summary.json")
OUT_JSON = os.path.join(HERE, "mirror_tripwire_summary.json")


def m_cell(c):
    return (-c[0], c[1])


def m_head(h):
    return {0: 0, 1: 3, 2: 2, 3: 1}[h]


def m_bits(word):
    return tuple(1 - b for b in word)


def gate_M0(n_seeds=25, steps=6000, rng_seed=960):
    """Dinamica forward: M coniuga le orbite. + onset vuota nei due universi."""
    import random
    rng = random.Random(rng_seed)
    # onset griglia vuota: universo standard
    turns, n, onset, _, _ = simulate(set(), 0, 0, 0, 12500, stop_at_onset=False)
    assert onset_verified(turns, n) == 9977
    # universo riflesso = formica speculare: simulo a mano la dinamica M
    # (R su bianco diventa L su bianco) partendo da griglia vuota
    g = {}
    x = y = 0; h = 0
    turns_m = []
    for t in range(n):
        c = (x, y)
        col = g.get(c, 0)
        if col == 0:
            turns_m.append(0)              # bianco -> L nell'universo M
            g[c] = 1; h = (h + 3) & 3
        else:
            turns_m.append(1)
            g[c] = 0; h = (h + 1) & 3
        x += DX[h]; y += DY[h]
    assert tuple(turns_m) == m_bits(tuple(int(b) for b in turns)), \
        "parola dell'universo M != scambio R<->L"
    # coniugazione su semi casuali: orbita(M(seme)) == M(orbita(seme))
    for k in range(n_seeds):
        side = rng.randrange(3, 10)
        seed = {(rng.randrange(-side, side), rng.randrange(-side, side))
                for _ in range(rng.randrange(1, 2 * side))}
        nst = rng.randrange(100, steps)
        # universo standard su seme
        g1 = {c: 1 for c in seed}
        x = y = 0; h = 0
        w1 = []
        tr1 = []
        for t in range(nst):
            c = (x, y)
            col = g1.get(c, 0)
            if col == 0:
                w1.append(1); g1[c] = 1; h = (h + 1) & 3
            else:
                w1.append(0); g1[c] = 0; h = (h + 3) & 3
            x += DX[h]; y += DY[h]
            tr1.append(((x, y), h))
        # universo M su seme riflesso (dinamica standard! la formica M vista
        # nel mondo standard e' la stessa regola: qui coniughiamo davvero)
        g2 = {m_cell(c): 1 for c in seed}
        x = y = 0; h = 0
        w2 = []
        tr2 = []
        for t in range(nst):
            c = (x, y)
            col = g2.get(c, 0)
            if col == 0:
                w2.append(0); g2[c] = 1; h = (h + 3) & 3   # regola M: bianco->L
            else:
                w2.append(1); g2[c] = 0; h = (h + 1) & 3
            x += DX[h]; y += DY[h]
            tr2.append(((x, y), h))
        assert tuple(w2) == m_bits(tuple(w1)), f"seme {k}: parole non coniugate"
        for (c1, h1), (c2, h2) in zip(tr1, tr2):
            assert c2 == m_cell(c1) and h2 == m_head(h1), \
                f"seme {k}: traiettorie non speculari"
        assert {m_cell(c) for c, v in g1.items() if v == 1} == \
               {c for c, v in g2.items() if v == 1}, f"seme {k}: griglie"
    return {"onset_vuota_entrambi": 9977, "semi_coniugati": n_seeds}


def gate_M1(steps=300):
    """ESCA: P da sola (scambio bit SENZA riflettere il seme) deve divergere."""
    seed = {(2, 1), (3, -1), (0, 2)}       # seme chirale
    g1 = {c: 1 for c in seed}
    g2 = {c: 1 for c in seed}              # NON riflesso
    x1 = y1 = 0; h1 = 0
    x2 = y2 = 0; h2 = 0
    w1 = []; w2 = []
    for t in range(steps):
        c = (x1, y1); col = g1.get(c, 0)
        if col == 0:
            w1.append(1); g1[c] = 1; h1 = (h1 + 1) & 3
        else:
            w1.append(0); g1[c] = 0; h1 = (h1 + 3) & 3
        x1 += DX[h1]; y1 += DY[h1]
        c = (x2, y2); col = g2.get(c, 0)
        if col == 0:
            w2.append(0); g2[c] = 1; h2 = (h2 + 3) & 3
        else:
            w2.append(1); g2[c] = 0; h2 = (h2 + 1) & 3
        x2 += DX[h2]; y2 += DY[h2]
    assert tuple(w2) != m_bits(tuple(w1)), \
        "ESCA FALLITA: P da sola sembra una simmetria (impossibile)"
    return {"divergenza_P_sola": True, "passi": steps}


def back_state(word, chirality=+1):
    """Camminatore all'indietro parametrizzato per chiralita'.
    chirality=+1: regola standard (bit R=1 <=> read bianca: read = 1-bit);
    chirality=-1: regola SPECCHIO (bit R=1 <=> read nera: read = bit).
    Frame anchor come exact_state: posa finale (0,0), heading finale 0,
    ricostruzione req all'indietro. Ritorna (posa, heading, req)."""
    x, y = 0, 0
    h = 0
    req = {}
    for b in reversed(word):
        read = (1 - b) if chirality == +1 else b
        # cella letta = posa - D[h] (heading corrente = dopo la svolta);
        # req = 1 - read (alternanza: la visita piu' antica legge l'opposto);
        # l'overwrite verso l'antico lascia il valore della PRIMA lettura
        cx, cy = x - DX[h], y - DY[h]
        req[(cx, cy)] = 1 - read
        h = (h - 1) & 3 if b == 1 else (h + 1) & 3
        x, y = cx, cy
    return (x, y), h, req


def gate_M2(cex):
    """exact_state/pend2 commutano con M via interprete a chiralita' specchio."""
    rows = []
    esca_flip = 0
    for w in cex:
        W = to_bits(w["word"])
        Wm = m_bits(W)
        assert valid(Wm)[1] is None, f"{w['tag']}: parola riflessa NON valida"
        c1, h1, req1 = exact_state(W)
        # (i) l'interprete in-script a chiralita' standard == exact_state
        c1b, h1b, req1b = back_state(W, +1)
        assert (c1b, h1b) == (c1, h1) and req1b == req1, \
            f"{w['tag']}: back_state(+1) != exact_state"
        # (ii) coniugazione: interprete SPECCHIO sulla parola riflessa
        c2, h2, req2 = back_state(Wm, -1)
        assert c2 == m_cell(c1), f"{w['tag']}: posa {c2} != M{c1}"
        assert h2 == m_head(h1), f"{w['tag']}: heading"
        assert req2 == {m_cell(c): v for c, v in req1.items()}, \
            f"{w['tag']}: req non speculare (interprete specchio)"
        p1 = pend2_of(req1); p2 = pend2_of(req2)
        assert sorted(map(m_cell, p1)) == sorted(p2), f"{w['tag']}: pend2"
        # (iii) ESCA: bit-swap nudo (regola standard su parola riflessa) =
        # mondo a colori invertiti: TUTTE le req flippate
        _, _, req_naive = exact_state(Wm)
        flip = {m_cell(c): 1 - v for c, v in req1.items()}
        assert req_naive == flip, f"{w['tag']}: l'esca del bit-swap nudo " \
            f"non produce il flip totale atteso"
        esca_flip += 1
        rows.append({"tag": w["tag"], "posa_M": list(c2), "pend2_n": len(p2)})
    return {"parole": len(rows), "esca_bitswap_flip_totale": esca_flip,
            "rows": rows}


def clean_subtree_chiral(word, chirality):
    """Sottoalbero pulito minimale parametrizzato per chiralita' (in-script,
    indipendente da u2_far_clean_stretch.clean_subtree): enumerazione con
    foglia-testimone alla prima posa fuori palla. Ritorna (nodi, D, r_max,
    n_pose_fuori, esaurito)."""
    c0, h0, req0 = back_state(word, chirality)
    pend = {c for c, r in req0.items() if r == 0}
    assert not any(cheb(c) <= 2 for c in pend), "nodo sporco"
    nodes = 0; D = 0; rmax = cheb(c0); fuori = 0
    stack = [(c0, h0, dict(req0), 0)]
    while stack:
        c, h, req, dep = stack.pop()
        for b in (0, 1):
            read = (1 - b) if chirality == +1 else b
            hn = (h - 1) & 3 if b == 1 else (h + 1) & 3
            cn = (c[0] - DX[h], c[1] - DY[h])
            if cn[1] < 1:
                continue
            r = req.get(cn, FREE)
            if r != FREE and r != read:
                continue
            if read == 1 and r == FREE and cheb(cn) <= 2:
                continue                  # aprirebbe pend2
            if read == 1 and r == 1 and cheb(cn) <= 2:
                continue                  # riaprirebbe
            nodes += 1
            D = max(D, dep + 1)
            rmax = max(rmax, cheb(cn))
            if cheb(cn) > 2:
                fuori += 1
                continue                  # foglia-testimone
            r2 = dict(req); r2[cn] = 1 - read
            stack.append((cn, hn, r2, dep + 1))
    return nodes, D, rmax, fuori


def gate_M3(cex):
    """clean_subtree: standard riproduce §95 (vuoto), specchio = speculare."""
    checked = 0
    for w in cex:
        W = to_bits(w["word"])
        _, _, req1 = exact_state(W)
        if pend2_of(req1):
            continue                        # nodo finale sporco: salta
        # standard in-script == numeri §95 (sottoalbero pulito VUOTO)
        cs_std = clean_subtree_chiral(W, +1)
        cs_ref = clean_subtree(W)
        assert cs_std[0] == cs_ref["nodi"] == 0 and cs_std[3] == 0 == \
            len(cs_ref["pose_fuori"]), f"{w['tag']}: standard != §95"
        # specchio sulla parola riflessa: identico (qui: vuoto anche lui)
        cs_mir = clean_subtree_chiral(m_bits(W), -1)
        assert cs_mir == cs_std, f"{w['tag']}: specchio diverge {cs_mir}"
        checked += 1
    assert checked > 0
    return {"nodi_verificati": checked}


def oracle_chiral(c0, h0, chirality):
    """Mini-oracolo del tratto pulito parametrizzato per chiralita' (come
    §95d: conoscenza = req(c0)=1, palla mai req=0, unknown=FREE, foglia-EXIT
    alla prima posa fuori). Nel tratto confinato sopravvive solo read-0 su
    FREE: lettera R (bit1, h-1) per chirality=+1, lettera L (bit0, h+1) per
    chirality=-1. Ritorna insieme delle pose-exit raggiunte (vuoto=confinato)."""
    exits = set()
    stack = [(c0, h0, frozenset([c0]))]      # celle con req=1 nota
    while stack:
        c, h, known1 = stack.pop()
        cn = (c[0] - DX[h], c[1] - DY[h])
        if cn[1] < 1:
            continue
        if cheb(cn) > 2:
            exits.add(cn)
            continue
        if cn in known1:
            continue                          # read0 irrealizzabile; read1 pota
        hn = (h - 1) & 3 if chirality == +1 else (h + 1) & 3
        stack.append((cn, hn, known1 | {cn}))
    return exits


def gate_M4(orc_path):
    """Coniugazione dell'oracolo: exit(specchio) == M(exit(standard));
    + riproduzione delle 15 firme §95d con l'oracolo in-script; + ESCA:
    l'insieme exit NON e' M-chiuso in se' (l'oracolo e' chirale)."""
    d = json.load(open(orc_path))
    ex_ref = {(tuple(r["posa"]), r["h"]) for r in d["rows"]
              if r["foglie_exit"] > 0}
    # riproduzione in-script (chiralita' standard)
    ex_std = set()
    for x in range(-2, 3):
        for y in (1, 2):
            for h in range(4):
                if oracle_chiral((x, y), h, +1):
                    ex_std.add(((x, y), h))
    assert ex_std == ex_ref, \
        f"oracolo in-script != §95d: {sorted(ex_std ^ ex_ref)}"
    # coniugazione con l'oracolo specchio
    ex_mir = set()
    for x in range(-2, 3):
        for y in (1, 2):
            for h in range(4):
                if oracle_chiral((x, y), h, -1):
                    ex_mir.add(((x, y), h))
    ex_std_M = {(m_cell(p), m_head(h)) for p, h in ex_std}
    assert ex_mir == ex_std_M, \
        f"coniugazione oracolo VIOLATA: {sorted(ex_mir ^ ex_std_M)}"
    # ESCA: M-chiusura ingenua dell'insieme standard DEVE fallire
    naive_closed = (ex_std_M == ex_std)
    assert not naive_closed, ("esca fallita: l'insieme exit sembra M-chiuso "
                              "(l'oracolo sarebbe achirale?!)")
    return {"firme_exit": len(ex_std), "coniugazione": True,
            "esca_M_chiusura_ingenua_fallisce": True,
            "diff_simmetrica_ingenua": len(ex_std ^ ex_std_M)}


def main():
    ap = argparse.ArgumentParser()
    args = ap.parse_args()
    t0 = time.time()
    cex = json.load(open(CEX))["witnesses"]

    gates = {}
    gates["M0"] = gate_M0()
    print(f"GATE M0 verde: onset vuota 9977 in entrambi gli universi; "
          f"{gates['M0']['semi_coniugati']} semi coniugati esatti", flush=True)
    gates["M1"] = gate_M1()
    print("GATE M1 verde (esca): P da sola DIVERGE su seme chirale — "
          "la violazione di parita' c'e', il checker la vede", flush=True)
    gates["M2"] = gate_M2(cex)
    print(f"GATE M2 verde: exact_state/pend2 commutano con M su "
          f"{gates['M2']['parole']} parole", flush=True)
    gates["M3"] = gate_M3(cex)
    print(f"GATE M3 verde: clean_subtree bit-identico sotto M su "
          f"{gates['M3']['nodi_verificati']} nodi puliti", flush=True)
    gates["M4"] = gate_M4(ORC)
    print(f"GATE M4 verde: oracolo CONIUGATO (exit specchio == M(exit "
          f"standard), {gates['M4']['firme_exit']} firme riprodotte); esca: "
          f"l'insieme NON e' M-chiuso in se' (diff simmetrica "
          f"{gates['M4']['diff_simmetrica_ingenua']}) — l'oracolo e' chirale "
          f"come deve", flush=True)

    out = {"gates": gates, "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nTRIPWIRE SPECCHIO: TUTTI I GATE VERDI. scritto {OUT_JSON} "
          f"in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
