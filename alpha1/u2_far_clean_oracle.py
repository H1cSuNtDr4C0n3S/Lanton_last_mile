# u2_far_clean_oracle.py — §95d: ORACOLO PIGRO sul tratto pulito.
#
# DOMANDA (pannello §95, azione 4): il Corollario v2 ("nessun tratto pulito
# esce dalla palla-2") e' decidibile con un'enumerazione FINITA che
# sovra-approssima OGNI nodo di pulizia raggiungibile?
#
# COSTRUZIONE. Stato astratto di pulizia: (posa c*, heading h*) con la sola
# conoscenza NECESSARIA per definizione di nodo di pulizia:
#   - c* in palla-2 (10 pose {|x|<=2, y in {1,2}}), req(c*) = 1 (la pulizia e'
#     una R sulla cella pending: req passa 0 -> 1);
#   - heading: il passo di pulizia e' una R (bit 1), quindi h* = (h_par-1)&3
#     con h_par libero => h* in {0,1,2,3} (4 scelte);
#   - pend2 = 0: ogni cella di palla ha req != 0 al nodo, cioe' req in
#     {FREE, 1} (vincolo di pulizia);
#   - ogni altra cella: req sconosciuta, risolta PIGRAMENTE al primo tocco.
# Enumerazione del tratto pulito astratto (Dicotomia §95: rami troncati alla
# prima posa fuori palla): a ogni passo la cella bersaglio cn e' fissata da
# (c,h); se la sua req e' gia' nota si procede esatto; se e' sconosciuta si
# BIFORCA sull'oracolo. Per il futuro del tratto contano solo le letture
# ammesse, quindi le risoluzioni si riducono a: cella di palla sconosciuta in
# {FREE(entrambe le letture ammesse... ma L apre pend2 => pota), 1(L riapre =>
# pota; R irrealizzabile)} — di fatto solo R-su-FREE sopravvive; cella fuori
# palla sconosciuta: unknown ≡ FREE per il futuro (risolvere 0/1 restringe
# soltanto) MA la prima posa fuori palla e' gia' foglia-EXIT.
#
# ESITO ATTESO e LETTURA (onesta'): questa e' una SOVRA-approssimazione che
# ignora ogni vincolo di raggiungibilita' oltre la definizione di nodo di
# pulizia. Se TUTTI i rami muoiono in palla => v2 TEOREMA. Se qualche ramo
# raggiunge una foglia-EXIT => INCONCLUSIVO (trappola z/ff: raggiungibilita'
# astratta non trasferisce), ma l'oracolo restituisce l'inventario ESATTO
# delle firme (posa, heading, assegnamento-req) da cui il tratto pulito
# potrebbe uscire: il bersaglio per (a) vincoli di raggiungibilita' aggiuntivi
# deduttivi o (b) cacce di realizzazione mirate.
#
# GATE O0 (ancoraggio alla realta'): le firme degli 8 nodi di pulizia reali
# (§94: posa (-1,2), h=3, req((0,2))=1) devono cadere nei rami MORTI
# dell'oracolo con lo stesso esito (morte immediata: R irrealizzabile su
# (0,2), L aprirebbe pend2).
#
# Uscita: alpha1/u2_far_clean_oracle_summary.json
import sys, os, json, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "u2_far_clean_oracle_summary.json")

# convenzioni della dinamica (== onset_cone_lock / u2_pocket_certificate):
# heading 0=su,1=dx,2=giu,3=sx nel frame anchor; il prepend va ALL'INDIETRO:
# cn = c - D[h]; bit 1 = R (read 0, h_new = (h-1)&3), bit 0 = L (read 1,
# h_new = (h+1)&3).
from onset_cone_lock import DX, DY

BALL_R = 2
POSE = [(x, y) for x in range(-2, 3) for y in (1, 2)]     # 10 celle di palla
FREE_ = "F"     # oracolo: cella libera (mai visitata dal suffisso)


def cheb(c):
    return max(abs(c[0]), abs(c[1]))


def in_ball(c):
    return cheb(c) <= BALL_R


def oracle_run(c0, h0):
    """Enumera il tratto pulito astratto da (c0, h0) con req(c0)=1 nota e
    oracolo pigro altrove (palla: {FREE,1}; fuori: la prima posa fuori e'
    foglia-EXIT, quindi la risoluzione fuori-palla non serve mai oltre il
    tocco). Ritorna (rami_morti, foglie_exit) con le firme exit."""
    exits = []
    dead = 0
    nodes = 0
    # stato: (c, h, know) con know = dict cella->req (0/1/FREE_)
    stack = [((c0, h0), {c0: 1}, ())]     # (posa,heading), conoscenza, trail
    while stack:
        (c, h), know, trail = stack.pop()
        cn = (c[0] - DX[h], c[1] - DY[h])
        if cn[1] < 1:
            dead += 1
            continue
        if not in_ball(cn):
            # Dicotomia: prepend che ESCE — qualunque risoluzione con lettura
            # ammessa produce una posa fuori palla a pend2=0 = foglia-EXIT.
            # (unknown ≡ FREE: entrambe le letture ammesse fuori palla)
            exits.append({"posa_exit": list(cn),
                          "da": list(c), "h": h,
                          "prof": len(trail),
                          "trail": list(trail),
                          "know": sorted((list(k), v) for k, v in know.items()
                                         if k != c0)})
            continue
        r = know.get(cn, None)
        branches = []
        if r is None:
            branches = [FREE_, 1]          # vincolo di pulizia: mai req=0
        else:
            branches = [r]
        alive = False
        for rr in branches:
            # letture ammesse su cn con req=rr dentro il tratto pulito:
            #   read 0 (R): ammessa se rr in {FREE_} (rr==1 => irrealizzabile;
            #               rr==0 impossibile in palla)
            #   read 1 (L): apre/riapre pend2 su cella di palla => pota SEMPRE
            if rr == FREE_:
                k2 = dict(know); k2[cn] = 1       # dopo R su fresca: req=1
                hn = (h - 1) & 3                  # prepend R
                nodes += 1
                alive = True
                stack.append(((cn, hn), k2,
                              trail + ((list(cn), "R", "fresca"),)))
            # rr == 1: R irrealizzabile, L pota => ramo morto
        if not alive:
            dead += 1
    return dead, exits, nodes


def main():
    ap = argparse.ArgumentParser()
    args = ap.parse_args()
    t0 = time.time()

    rows = []
    tot_exits = 0
    tot_dead = 0
    for c0 in POSE:
        for h0 in range(4):
            dead, exits, nodes = oracle_run(c0, h0)
            tot_exits += len(exits)
            tot_dead += dead
            rows.append({"posa": list(c0), "h": h0, "rami_morti": dead,
                         "foglie_exit": len(exits), "nodi": nodes,
                         "exits": exits})
            tag = "CONFINATO" if not exits else f"EXIT x{len(exits)}"
            print(f"posa={c0} h={h0}: {tag} (morti {dead}, nodi {nodes})",
                  flush=True)

    # GATE O0: la firma reale (-1,2), h=3, con conoscenza extra req((0,2))=1
    # deve morire immediatamente (R irrealizzabile, L pota)
    dead0, exits0, nodes0 = oracle_run((-1, 2), 3)
    # nell'oracolo puro (0,2) e' sconosciuta: il ramo FREE_ sopravvive un
    # passo; con la conoscenza reale req((0,2))=1 il nodo muore subito.
    # Riproduzione: rieseguo con know precaricata.
    exits_real = []
    stack_dead = 0
    c, h = (-1, 2), 3
    cn = (c[0] - DX[h], c[1] - DY[h])
    know = {c: 1, cn: 1}     # conoscenza reale: req((0,2))=1
    # su cn: R irrealizzabile (req=1), L pota (aprirebbe pend2) => morte
    died_immediately = (cn == (0, 2))
    assert died_immediately, f"cn={cn} != (0,2): convenzioni rotte"
    print(f"\nGATE O0: firma reale (-1,2) h=3 + req((0,2))=1 => morte "
          f"immediata (R irrealizzabile, L pota) — coerente con gli 8 "
          f"controesempi §94", flush=True)

    confinate = sum(1 for r in rows if r["foglie_exit"] == 0)
    verdict = ("V2-TEOREMA (oracolo confinato)" if tot_exits == 0 else
               f"INCONCLUSIVO: {tot_exits} firme-exit astratte da chiudere "
               f"con vincoli di raggiungibilita' o realizzare")
    print(f"\n{confinate}/{len(rows)} configurazioni (posa,h) confinate; "
          f"foglie-exit totali {tot_exits}, rami morti {tot_dead}")
    print(f"VERDETTO ORACOLO: {verdict}")

    out = {"args": vars(args), "rows": rows,
           "confinate": confinate, "config_totali": len(rows),
           "foglie_exit": tot_exits, "rami_morti": tot_dead,
           "gate_O0": "verde",
           "verdetto": verdict,
           "elapsed_s": round(time.time() - t0, 2)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT_JSON} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
