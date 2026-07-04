# u2_far_clean_oracle_v2.py — §96: ORACOLO v2 con vincoli di raggiungibilita'.
#
# §95d lasciava 15 firme-exit astratte. Qui si aggiungono due vincoli
# DEDUTTIVI, validi a ogni nodo di pulizia m* di un albero radicato a w101:
#
# C1 (il muro delle nove): w101 visita 9 delle 10 celle di palla-2
#    ({|x|<=2, y in {1,2}} \ {(1,1)}; misurato da exact_state(w101), gate V1).
#    Ogni suffisso contiene w101 => quelle 9 celle sono VISITATE a ogni nodo
#    => a ogni nodo con pend2=0 hanno req=1 (visitata /\ pend2=0 => req!=0).
#    Nel tratto pulito le celle req=1 sono MORTE (R irrealizzabile, L pota)
#    => l'unica cella di palla percorribile dal tratto pulito e' (1,1), e al
#    piu' UNA volta (se libera; se visitata dall'estensione, req=1 e morta
#    anche lei — si biforca sull'oracolo {FREE, 1}).
# C3 (catena del genitore): il passo di pulizia arriva da
#    c_par = c* + D[(h*+1)&3]; c_par e' la cella letta dal passo del genitore
#    => VISITATA a m*; se c_par e' in palla, req(c_par)=1 (pend2(m*)=0).
#    Morde solo quando c_par == (1,1): elimina il ramo (1,1)=FREE.
# C4 (riga zero): c_par e' una cella LETTA (dal passo del genitore) => y>=1
#    (valid() esige y>=1 su ogni cella visitata). Se c_par ha y<1 la firma e'
#    IRREALIZZABILE: nessun genitore possibile.
#
# LEMMA DELLA CATENA DI CHIUSURA (riscritto dal pannello §96 — la prima
# versione "ingresso fresco dal bordo" era un BUCO): al nodo di pulizia m*
# di firma (c*, h*), i passi immediatamente precedenti IN palla sono R su
# p_k = c* + D[h_par] + ... + D[h_par+k-1], con p_k fuori da {c*, p1..p_{k-1}}
# per k <= 3 (distinttezza geometrica) e pend2(n_k) ⊇ {c*, p1, ..., p_{k-1}}:
# sotto w101 le nove sono visitate, quindi ogni R in palla della catena e'
# R-SU-PENDING e i pending si ACCUMULANO andando all'indietro. Il run di R in
# palla e' <= 3: il 4o passo all'indietro NON puo' essere R (p4 = c*
# renderebbe req(c*)=1 al genitore => pulizia irrealizzabile) ed e'
# forzatamente L SU c* STESSA (l'apertura del pending di c*, realizzabile su
# req=1), con p5 = c* + D[h*-1] vicino di c*: la catena PUO' proseguire in
# palla indefinitamente con aperture L — nessun enunciato di ingresso dal
# bordo o di freschezza (in palla le nove non sono mai fresche; l'unica
# potenzialmente fresca e' (1,1)). Conferma di terra (lente indipendente
# §96): run-R = 3 e pattern RRRRL attorno a TUTTI gli 8 nodi puliti reali.
#
# NOTA (1,1) (pannello, B4): l'oracolo esplora il SOLO ramo FREE per le celle
# non note (risoluzione FREE-dominante): il ramo req=1 muore subito ed e'
# sottoinsieme stretto degli exit — sovra-approssimazione sound per i
# verdetti "confinata".
#
# GATE:
#   W1: footprint di palla di w101 = le 9 celle attese, (1,1) esclusa;
#   O0: la firma reale ((-1,2), h=3) e' confinata GIA' per C1 (cn=(0,2),
#       req=1 universale) — il fatto §95 "req((0,2))=1 concreto" e' promosso
#       a vincolo deduttivo;
#   E1 (esca): senza C1/C3 l'oracolo v2 deve riprodurre ESATTAMENTE le 15
#       firme-exit di §95d (il codice sa tornare all'oracolo v1);
#   E2 (esca): con C1 su SOLE 8 celle (togliendo (0,2)) le firme confinate
#       devono cambiare (il vincolo lavora davvero).
#
# Uscita: alpha1/u2_far_clean_oracle_v2_summary.json
import sys, os, json, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY
from record_weapon_vitality import to_bits, SUMMARY
from u2_pocket_certificate import exact_state
from u2_far_ledger import cheb

HERE = os.path.dirname(os.path.abspath(__file__))
V1_SUM = os.path.join(HERE, "u2_far_clean_oracle_summary.json")
OUT_JSON = os.path.join(HERE, "u2_far_clean_oracle_v2_summary.json")

BALL_R = 2
POSE = [(x, y) for x in range(-2, 3) for y in (1, 2)]


def in_ball(c):
    return cheb(c) <= BALL_R


def stretch_exits(c0, h0, known1, free_ok):
    """Enumera il tratto pulito astratto da (c0,h0): known1 = celle in palla
    con req=1 (morte per il tratto); free_ok = celle in palla percorribili se
    non ancora toccate (risolte FREE). Foglia-EXIT alla prima posa fuori.
    Ritorna (exits, prof_max_exit)."""
    exits = []
    stack = [(c0, h0, frozenset(known1), 0)]
    while stack:
        c, h, k1, dep = stack.pop()
        cn = (c[0] - DX[h], c[1] - DY[h])
        if cn[1] < 1:
            continue
        if not in_ball(cn):
            exits.append((cn, dep + 1))
            continue
        if cn in k1 or cn not in free_ok:
            continue                       # req=1 (morta) o non percorribile
        # read 0 su FREE: lettera R, heading indietro h-1
        stack.append((cn, (h - 1) & 3, k1 | {cn}, dep + 1))
    return exits


def oracle_v2(c0, h0, nine, use_c1=True, use_c3=True):
    """Firma (c0,h0): rami dell'oracolo v2. Biforca su (1,1) in {FREE, 1}
    (salvo C3 che la forza a visitata=req1). Ritorna lista exits totale."""
    # celle in palla NOTE req=1 al nodo di pulizia: c0 (appena chiusa) + C1
    # (le nove di w101) + C3 (c_par se in palla: cella letta dal genitore =>
    # visitata => req=1 a pend2=0). Per le celle NON note la risoluzione FREE
    # domina il ramo visitata-req1 (piu' mosse => sovrainsieme di exit):
    # free_ok = palla \ note, un solo ramo, sovra-approssimazione sana.
    known_base = {c0}
    if use_c1:
        known_base |= set(nine)
    h_par = (h0 + 1) & 3
    c_par = (c0[0] + DX[h_par], c0[1] + DY[h_par])
    if use_c3 and c_par[1] < 1:
        return [], c_par                   # C4: nessun genitore possibile
    if use_c3 and in_ball(c_par):
        known_base = known_base | {c_par}
    free_ok = set(POSE) - known_base
    exits = stretch_exits(c0, h0, known_base, free_ok)
    return exits, c_par


def run_all(nine, use_c1, use_c3):
    rows = []
    for c0 in POSE:
        for h0 in range(4):
            ex, c_par = oracle_v2(c0, h0, nine, use_c1, use_c3)
            rows.append({"posa": list(c0), "h": h0,
                         "c_par": list(c_par),
                         "exits": [{"cella": list(c), "prof": d}
                                   for c, d in ex]})
    return rows


def main():
    ap = argparse.ArgumentParser()
    args = ap.parse_args()
    t0 = time.time()

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    cw, hw, reqw = exact_state(w101)

    # GATE W1: footprint di palla di w101
    ball_vis = sorted(c for c in reqw if in_ball(c))
    nine_exp = sorted(c for c in POSE if c != (1, 1))
    assert ball_vis == nine_exp, f"footprint palla w101 cambiato: {ball_vis}"
    print(f"GATE W1 verde: w101 visita esattamente le 9 celle di palla "
          f"(manca solo (1,1))", flush=True)

    # oracolo v2 pieno (tre esiti distinti: residua / confinata /
    # C4-irrealizzabile — pannello §96, nota C)
    rows = run_all(nine_exp, True, True)
    ex_v2 = [(tuple(r["posa"]), r["h"]) for r in rows if r["exits"]]
    c4_irr = [(tuple(r["posa"]), r["h"]) for r in rows
              if not r["exits"] and r["c_par"][1] < 1]
    conf_v2 = [(tuple(r["posa"]), r["h"]) for r in rows if not r["exits"]]

    # GATE O0: firma reale confinata per C1
    assert ((-1, 2), 3) in conf_v2, "firma reale NON confinata?!"
    print(f"GATE O0 verde: ((-1,2), h=3) confinata deduttivamente da C1 "
          f"(cn=(0,2) e' una delle nove)", flush=True)

    # GATE E1 (esca): senza C1/C3 == le 15 di §95d
    rows_v1 = run_all(nine_exp, False, False)
    ex_v1 = {(tuple(r["posa"]), r["h"]) for r in rows_v1 if r["exits"]}
    v1_ref = json.load(open(V1_SUM))
    ex_ref = {(tuple(r["posa"]), r["h"]) for r in v1_ref["rows"]
              if r["foglie_exit"] > 0}
    assert ex_v1 == ex_ref, f"esca E1: v2-senza-vincoli != §95d: " \
        f"{sorted(ex_v1 ^ ex_ref)}"
    print(f"GATE E1 verde (esca): senza C1/C3 l'oracolo riproduce le "
          f"{len(ex_ref)} firme-exit di §95d", flush=True)

    # GATE E2 (esca): C1 monco (senza (0,2)) cambia le confinate
    eight = [c for c in nine_exp if c != (0, 2)]
    rows_e2 = run_all(eight, True, True)
    ex_e2 = {(tuple(r["posa"]), r["h"]) for r in rows_e2 if r["exits"]}
    assert ex_e2 != set(ex_v2), "esca E2: togliere (0,2) non cambia nulla?!"
    print(f"GATE E2 verde (esca): C1 monco produce {len(ex_e2)} exit "
          f"(vs {len(ex_v2)} piene) — il vincolo lavora", flush=True)

    print(f"\n---- ORACOLO v2: {len(conf_v2)}/40 non-exit "
          f"({len(conf_v2) - len(c4_irr)} confinate + {len(c4_irr)} "
          f"C4-irrealizzabili), {len(ex_v2)} firme-exit residue ----")
    for (p, h) in ex_v2:
        r = next(x for x in rows if tuple(x["posa"]) == p and x["h"] == h)
        via = "diretta" if all(e["prof"] == 1 for e in r["exits"]) \
            else "via (1,1)"
        print(f"  posa={p} h={h}: {len(r['exits'])} exit ({via}), "
              f"c_par={tuple(r['c_par'])}", flush=True)

    killed = sorted(set(ex_ref) - set(ex_v2))
    print(f"\nuccise da C1/C3: {len(killed)}/{len(ex_ref)}: {killed}")

    out = {"gates": {"W1": "verde", "O0": "verde", "E1": "verde",
                     "E2": "verde"},
           "nove": [list(c) for c in nine_exp],
           "rows": rows,
           "confinate": len(conf_v2) - len(c4_irr),
           "c4_irrealizzabili": [{"posa": list(p), "h": h}
                                 for p, h in sorted(c4_irr)],
           "firme_exit": [
               {"posa": list(p), "h": h} for p, h in sorted(ex_v2)],
           "uccise_da_vincoli": [{"posa": list(p), "h": h}
                                 for p, h in killed],
           "elapsed_s": round(time.time() - t0, 2)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT_JSON} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
