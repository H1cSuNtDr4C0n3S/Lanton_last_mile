# record_divergence_esche.py — §101 pannello, LENTE B: esche di falsificabilita'.
#
# Quattro mutazioni del checker di record_divergence_census.py, su orbita 0:
#   E1 footprint monco (tolgo una cella visitata dalla parola): il residuo eredita
#      una cella di footprint => T-DIV deve scattare (d per-celle != d per-svolte)
#      su almeno un record (la cella di footprint puo' essere nera senza divergenza).
#   E2 prime-letture sfasate (+1 sul tempo fr): T-DIV deve scattare.
#   E3 (POSITIVO, terra-check del Lemma 0): includo nel residuo anche y_rel <= 0:
#      le colpevoli aggiuntive devono essere ZERO (davanti e riga-0 bianche gratis).
#   E4 svolte reali sfasate (+1: confronto gturns[i] vs turns[t+1+i]): l'allineamento
#      parola/germe e' rotto => d per-svolte cambia => T-DIV deve scattare.
#      (NB: la prima versione dell'esca — colori a t-1 — NON PUO' scattare ed e'
#      stata promossa a verifica: l'unica cella scritta a t-1 e' la posa a t-1,
#      che e' footprint; i colori del residuo sono stabili sul passo. Misurato: 0.)
# CONTROLLO POSITIVO: baseline non corrotta = zero scatti (bit-identica al censimento).
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA
from record_divergence_census import germ_long_run
from record_weapon_hunt import eval_word
from record_word_census import run_collect_records
from record_supply_census import replay_supply

K = 101


def pipeline(esca=None):
    """Ritorna (n_record, n_scatti_TDIV, extra) per l'orbita 0 con l'esca data."""
    od = parse_dumps(ALPHA / "dumps_all.txt")[0]
    seed, _, _ = build_seed(od.rngstate, 5, 25)
    y_seed_min = min(cy for (_, cy) in seed)
    turns, t_on, records = run_collect_records(seed)
    n_real = len(turns)
    recs = [(t, x, y) for (t, x, y) in records
            if t < t_on and y < y_seed_min and t >= K]
    ev_cache = {}
    germ_cache = {}
    info = []
    queries = {}
    for (t, rx, ry) in recs:
        w = tuple(turns[t - K:t])
        if w not in germ_cache:
            r = eval_word(w)
            ev_cache[w] = r
            germ_cache[w] = germ_long_run(w, r[1])
        gturns, fr, t_dag, drift, footprint, xs, ys = germ_cache[w]
        fp = set(footprint)
        if esca == "E1":
            # footprint monco: tolgo le celle NERE del germe (per Finestra-K sono
            # nere anche in realta' e il transiente le rilegge presto): il residuo
            # corrotto le eredita come "colpevoli" a fr piccolo => d_celle < d_svolte
            vg, pose = __import__("kwindow_spoiler_census").virtual_walk(w)
            anchor = __import__("kwindow_spoiler_census").to_anchor_frame(vg, pose)
            fp -= {c for c, col in anchor.items() if col == 1}
        ymin_res = 1 if esca != "E3" else -10**9
        res = [c for c, (tf, _) in fr.items()
               if tf < t_dag and c not in fp and c[1] >= ymin_res]
        if esca == "E2":
            frx = {c: (tf + 1, col) for c, (tf, col) in fr.items()}
        else:
            frx = fr
        info.append((t, rx, ry, w, res, frx, gturns, t_dag))
        queries[t] = {(rx + cx, ry + cy) for (cx, cy) in res}
    colors, _ = replay_supply(seed, turns, queries)
    off = 1 if esca == "E4" else 0

    n_scatti = 0
    extra_guilty_low = 0
    for (t, rx, ry, w, res, frx, gturns, t_dag) in info:
        got = colors[t]
        guilty = [(c, frx[c][0]) for c in res
                  if got[(rx + c[0], ry + c[1])][0] == 1]
        if esca == "E3":
            extra_guilty_low += sum(1 for (c, _) in guilty if c[1] <= 0)
            continue
        d_cell = min((tf for (_, tf) in guilty), default=None)
        L = min(t_dag, n_real - t - off)
        d = next((i for i in range(L) if gturns[i] != turns[t + off + i]), None)
        if d is not None:
            if d_cell != d:
                n_scatti += 1
        else:
            if not (d_cell is None or d_cell >= L):
                n_scatti += 1
    return len(info), n_scatti, extra_guilty_low


def main():
    n, s, _ = pipeline(None)
    print(f"BASELINE: {n} record, scatti T-DIV = {s} (attesi 0)", flush=True)
    assert s == 0, "baseline sporca: controllo positivo fallito"
    n, s, _ = pipeline("E1")
    print(f"E1 footprint monco: scatti T-DIV = {s} (attesi >0) "
          f"{'BECCATA' if s > 0 else '*** NON BECCATA ***'}", flush=True)
    assert s > 0
    n, s, _ = pipeline("E2")
    print(f"E2 fr sfasate +1: scatti T-DIV = {s} (attesi >0) "
          f"{'BECCATA' if s > 0 else '*** NON BECCATA ***'}", flush=True)
    assert s > 0
    n, _, low = pipeline("E3")
    print(f"E3 terra-check Lemma 0: colpevoli a y_rel<=0 = {low} (attese 0) "
          f"{'VERDE' if low == 0 else '*** ROSSO ***'}", flush=True)
    assert low == 0
    n, s, _ = pipeline("E4")
    print(f"E4 svolte reali sfasate +1: scatti T-DIV = {s} (attesi >0) "
          f"{'BECCATA' if s > 0 else '*** NON BECCATA ***'}", flush=True)
    assert s > 0
    print("\nLENTE B: baseline pulita, 3/3 esche beccate, terra-check Lemma 0 verde",
          flush=True)


if __name__ == "__main__":
    main()
