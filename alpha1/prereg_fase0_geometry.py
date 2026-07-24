# prereg_fase0_geometry.py — FASE 0 della PREREG RIENTRO-SCIA (pre-§109, v2).
#
# Mandato (docs/PREREG_RIENTRO_SCIA.md, Fase 0 ridotta da ERRATA-1.2):
# geometria LOCALE delle 8 firme-exit residue di §96a — SOLO c_par, primo
# passo e cella d'uscita. NIENTE lati/heading di rientro (RC1 da sola non li
# determina). NESSUN valore geometrico scritto a mano nei documenti: questo
# tool e' l'unica sorgente; i valori vivono nel JSON di output.
#
# Doppia implementazione (obbligo di Fase 0) — CLASSIFICAZIONE CORRETTA
# dall'ERRATA del titolare (post-a36e67c, verdetto 2026-07-25):
#   A: formule del macchinario esistente (DX/DY di onset_cone_lock, come
#      u2_far_clean_oracle_v2.py): h_par=(h*+1)&3, c_par=c*+D[h_par],
#      primo passo cn=c*-D[h*] (§97a: cella letta = posa - D[h]).
#   B: calibrazione INDIPENDENTE della SOLA tabella D (dai soli anchor
#      pubblicati a verbale, mai da DX/DY) ma CINEMATICA CONDIVISA con A
#      (le formule h_par=(h*+1)&3, c_par=c*+D[h_par], cn=c*-D[h*] sono le
#      stesse): B NON e' un'implementazione indipendente in senso pieno.
#      Heading 0=su,1=destra,2=giu,3=sinistra (CLAUDE.md §2) con segni
#      degli assi liberi (4 combinazioni), pinnati da tre anchor:
#        A1 (§96c):  c_par((-1,2), h=3) = (-1,1), h_par=0;
#        A2 (§96a C4): c_par((2,1), h=3) = (2,0);
#        A3 (§96 GATE O0): primo passo di ((-1,2), h=3) legge cn=(0,2).
#      La calibrazione DEVE essere unica (assert), altrimenti Fase 0 rossa.
#
# GATE:
#   G0     : firme_exit del summary §96 == lista a verbale §96a (8 firme);
#   G-ANCH : A e B riproducono i tre anchor;
#   G-AB   : A == B su tutte le 8 firme (c_par, h_par, cn);
#   G-SUM  : cross-check col summary §96 — REGRESSIONE DI COERENZA A
#            GENEALOGIA COMUNE (il summary e' prodotto con gli stessi
#            DX/DY e le stesse formule), NON verifica indipendente
#            (ERRATA classificatoria del titolare). Contenuto: c_par per
#            riga; exit-diretta: 1 exit a prof 1, cella == cn;
#            y(exit)>=1, cheb>2;
#   E1 esca: B con D[1]/D[3] scambiate => G-AB DEVE fallire (beccata);
#   E2 esca: heading corrotto su una firma del summary => G-SUM DEVE fallire.
#
# Uscita: alpha1/prereg_fase0_geometry_summary.json
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY
from u2_far_ledger import cheb

HERE = os.path.dirname(os.path.abspath(__file__))
V2_SUM = os.path.join(HERE, "u2_far_clean_oracle_v2_summary.json")
OUT_JSON = os.path.join(HERE, "prereg_fase0_geometry_summary.json")

# ERRATA del titolare: i gate usano assert => fail-open sotto `python -O`.
# Guardia esplicita (il risultato a36e67c e' stato riprodotto dal titolare
# senza ottimizzazione); da Fase 0b in poi: controlli espliciti, non assert.
if sys.flags.optimize:
    raise SystemExit("ERRORE: eseguire SENZA -O (gli assert dei gate "
                     "sarebbero fail-open)")

BALL_R = 2

# Lista a verbale §96a — usata SOLO come cross-check contro il summary,
# mai come sorgente di geometria.
FIRME_96A = [((-2, 1), 1), ((-2, 2), 0), ((-2, 2), 1), ((-1, 2), 0),
             ((0, 2), 0), ((1, 2), 0), ((2, 2), 0), ((2, 2), 3)]

# Anchor pubblicati (vedi header): (firma) -> fatti attesi.
ANCHOR_CPAR = {((-1, 2), 3): (-1, 1),   # §96c (h_par=0 anch'esso a verbale)
               ((2, 1), 3): (2, 0)}     # §96a C4
ANCHOR_CN = {((-1, 2), 3): (0, 2)}      # §96 GATE O0


def impl_A(c0, h0):
    h_par = (h0 + 1) & 3
    c_par = (c0[0] + DX[h_par], c0[1] + DY[h_par])
    cn = (c0[0] - DX[h0], c0[1] - DY[h0])
    return c_par, h_par, cn


def make_B(swap_horiz=False):
    """Calibra la tabella D di B dai soli anchor. swap_horiz=True e' l'esca
    E1 (scambia D[1] e D[3] DOPO la calibrazione)."""
    cands = []
    for sx in (1, -1):
        for sy in (1, -1):
            D = {0: (0, sy), 1: (sx, 0), 2: (0, -sy), 3: (-sx, 0)}
            ok = True
            for (c0, h0), cp_exp in ANCHOR_CPAR.items():
                hp = (h0 + 1) & 3
                cp = (c0[0] + D[hp][0], c0[1] + D[hp][1])
                if cp != cp_exp or ((c0, h0) == ((-1, 2), 3) and hp != 0):
                    ok = False
            for (c0, h0), cn_exp in ANCHOR_CN.items():
                cn = (c0[0] - D[h0][0], c0[1] - D[h0][1])
                if cn != cn_exp:
                    ok = False
            if ok:
                cands.append(D)
    assert len(cands) == 1, \
        f"calibrazione B non unica: {len(cands)} tabelle compatibili"
    D = dict(cands[0])
    if swap_horiz:
        D[1], D[3] = D[3], D[1]
    return D


def impl_B(c0, h0, D):
    h_par = (h0 + 1) & 3
    c_par = (c0[0] + D[h_par][0], c0[1] + D[h_par][1])
    cn = (c0[0] - D[h0][0], c0[1] - D[h0][1])
    return c_par, h_par, cn


def check_sum(firme, rows_by_key, computed):
    """G-SUM: cross-check contro le righe del summary §96. Ritorna lista di
    mismatch (vuota = verde)."""
    bad = []
    for (c0, h0) in firme:
        r = rows_by_key[(c0, h0)]
        c_par, h_par, cn = computed[(c0, h0)]
        if tuple(r["c_par"]) != c_par:
            bad.append((c0, h0, "c_par", r["c_par"], c_par))
        ex = r["exits"]
        if len(ex) != 1 or ex[0]["prof"] != 1:
            bad.append((c0, h0, "exit-diretta", ex, None))
            continue
        if tuple(ex[0]["cella"]) != cn:
            bad.append((c0, h0, "exit-cella", ex[0]["cella"], cn))
        if cn[1] < 1 or cheb(cn) <= BALL_R:
            bad.append((c0, h0, "exit-fuori-palla-y>=1", cn, None))
    return bad


def main():
    t0 = time.time()
    v2 = json.load(open(V2_SUM))

    # G0: le firme del summary == lista a verbale §96a
    firme_sum = sorted((tuple(f["posa"]), f["h"]) for f in v2["firme_exit"])
    assert firme_sum == sorted(FIRME_96A), \
        f"G0: firme summary != §96a: {firme_sum}"
    print(f"GATE G0 verde: 8 firme del summary §96 == lista a verbale §96a",
          flush=True)

    rows_by_key = {(tuple(r["posa"]), r["h"]): r for r in v2["rows"]}

    # G-ANCH: A e B sui tre anchor
    D_B = make_B()
    for (c0, h0), cp_exp in ANCHOR_CPAR.items():
        assert impl_A(c0, h0)[0] == cp_exp, f"G-ANCH A c_par {c0},{h0}"
        assert impl_B(c0, h0, D_B)[0] == cp_exp, f"G-ANCH B c_par {c0},{h0}"
    for (c0, h0), cn_exp in ANCHOR_CN.items():
        assert impl_A(c0, h0)[2] == cn_exp, f"G-ANCH A cn {c0},{h0}"
        assert impl_B(c0, h0, D_B)[2] == cn_exp, f"G-ANCH B cn {c0},{h0}"
    print("GATE G-ANCH verde: A e B riproducono i 3 anchor a verbale "
          "(§96c, §96a-C4, §96-O0)", flush=True)

    # calcolo sulle 8 + G-AB
    comp_A = {(c0, h0): impl_A(c0, h0) for (c0, h0) in FIRME_96A}
    comp_B = {(c0, h0): impl_B(c0, h0, D_B) for (c0, h0) in FIRME_96A}
    mism = [k for k in FIRME_96A if comp_A[k] != comp_B[k]]
    assert not mism, f"G-AB: A != B su {mism}"
    print("GATE G-AB verde: A == B su tutte le 8 firme (c_par, h_par, cn)",
          flush=True)

    # G-SUM
    bad = check_sum(FIRME_96A, rows_by_key, comp_A)
    assert not bad, f"G-SUM: mismatch col summary §96: {bad}"
    print("GATE G-SUM verde: c_par e cella d'uscita coincidono col summary "
          "§96; 8/8 exit-diretta (1 exit, prof 1, fuori palla, y>=1)",
          flush=True)

    # E1 (esca): B con D orizzontali scambiate deve produrre mismatch
    D_bad = make_B(swap_horiz=True)
    comp_B_bad = {(c0, h0): impl_B(c0, h0, D_bad) for (c0, h0) in FIRME_96A}
    mism_e1 = [k for k in FIRME_96A if comp_A[k] != comp_B_bad[k]]
    assert mism_e1, "ESCA E1 NON beccata: D corrotta ma A==B?!"
    print(f"GATE E1 verde (esca): D[1]/D[3] scambiate => mismatch su "
          f"{len(mism_e1)}/8 firme (beccata)", flush=True)

    # E2 (esca): heading corrotto su una firma => G-SUM deve fallire
    (c0x, h0x) = FIRME_96A[0]
    comp_bad = dict(comp_A)
    comp_bad[(c0x, h0x)] = impl_A(c0x, (h0x + 1) & 3)
    bad_e2 = check_sum(FIRME_96A, rows_by_key, comp_bad)
    assert bad_e2, "ESCA E2 NON beccata: heading corrotto ma G-SUM verde?!"
    print(f"GATE E2 verde (esca): heading corrotto su {c0x} h={h0x} => "
          f"{len(bad_e2)} mismatch (beccata)", flush=True)

    # tabella e output
    print("\n---- FASE 0: geometria locale delle 8 firme (output del tool, "
          "unica sorgente) ----")
    out_rows = []
    for (c0, h0) in FIRME_96A:
        c_par, h_par, cn = comp_A[(c0, h0)]
        row = {"c_star": list(c0), "h_star": h0,
               "c_par": list(c_par), "h_par": h_par,
               "c_par_in_palla": cheb(c_par) <= BALL_R,
               "c_par_y_ge_1": c_par[1] >= 1,
               "primo_passo_cella": list(cn),
               "exit_cell": list(cn), "prof": 1, "exit_diretta": True}
        out_rows.append(row)
        print(f"  firma c*={c0} h*={h0}: c_par={c_par} (h_par={h_par}, "
              f"in_palla={row['c_par_in_palla']}), "
              f"primo passo/exit={cn}", flush=True)

    out = {"prereg": "docs/PREREG_RIENTRO_SCIA.md v2 (ERRATA-1)",
           "fase": "0 (geometria locale; ridotta da ERRATA-1.2)",
           "classificazione_errata_titolare": {
               "B": "calibrazione indipendente della sola tabella D; "
                    "cinematica condivisa con A (h_par, c_par, cn)",
               "G-SUM": "regressione di coerenza a genealogia comune "
                        "(summary prodotto con gli stessi DX/DY), non "
                        "verifica indipendente",
               "assert": "fail-open sotto python -O; guardia esplicita "
                         "aggiunta; da Fase 0b: controlli espliciti"},
           "sys_flags_optimize": sys.flags.optimize,
           "gates": {"G0": "verde", "G-ANCH": "verde", "G-AB": "verde",
                     "G-SUM": "verde", "E1-esca": "beccata",
                     "E2-esca": "beccata"},
           "anchor": {"c_par((-1,2),3)": [-1, 1], "c_par((2,1),3)": [2, 0],
                      "cn((-1,2),3)": [0, 2]},
           "firme": out_rows,
           "elapsed_s": round(time.time() - t0, 2)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nscritto {OUT_JSON} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
