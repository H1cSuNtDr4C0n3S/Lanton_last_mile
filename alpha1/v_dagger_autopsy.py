# v_dagger_autopsy.py — §100b: AUTOPSIA dei 2 violatori dell'orizzonte (§99c).
#
# I due record freschi con residuo V(onset+P) tutto bianco ma onset lontano
# (t_on - t = 2372 e 14757 >> onset_germe + P = 159) provano che il rigioco del
# germe e' stato deviato da una cella letta DOPO l'orizzonte corto: una cella di
# V† \ V (lezione §91: la rilevazione legge fino a T=2600). Qui si trova LA cella:
#   1. ri-verifica della violazione (residuo corto tutto bianco, t_on - t);
#   2. corsa del germe per 2600 passi (senza stop all'onset) vs svolte reali da t:
#      d = primo indice di divergenza. TRIPWIRE: d >= onset_germe + P (la deviazione
#      DEVE essere oltre l'orizzonte corto, altrimenti §99c era mal diagnosticato);
#   3. la cella di divergenza: posizione relativa (frame anchor: heading 0 al
#      record, pura traslazione), prima-lettura del germe == d, fuori dal footprint,
#      colore germe (bianco) vs colore reale (nero atteso);
#   4. anagrafe della cella alla §98: seme-o-dipinta, eta', ep (epoche), y_rel,
#      cheb, e (se riga sotto il seme) lag dall'apertura della riga.
# Esito atteso: il meccanismo G>=1 "guarisce" alla V† — la colpevole esiste, vive
# solo oltre l'orizzonte corto. Se la cella fosse BIANCA o dentro V, sarebbe un
# ROSSO diagnostico da verbale.
#
# Uscita: alpha1/v_dagger_autopsy_summary.json
import sys, os, json, time, bisect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import build_seed
from onset_cone_lock import DX, DY, P, simulate
from kwindow_spoiler_census import virtual_walk, to_anchor_frame
from record_weapon_hunt import eval_word
from record_word_census import run_collect_records
from record_supply_census import replay_supply

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "v_dagger_autopsy_summary.json")
K = 101
T_DAGGER = 2600

VIOLATORS = [
    {"rngstate": 7589057972138690721, "t": 13356, "t_on_meno_t_atteso": 2372},
    {"rngstate": 17133539851518799906, "t": 12164, "t_on_meno_t_atteso": 14757},
]


def walk_to(turns_seq, d):
    """Posizione della formica al passo d (cella letta al passo d), da (0,0,0)."""
    x = y = 0
    h = 0
    for i in range(d):
        if turns_seq[i]:
            h = (h + 1) & 3
        else:
            h = (h + 3) & 3
        x += DX[h]
        y += DY[h]
    return x, y


def main():
    t_start = time.time()
    results = []
    for v in VIOLATORS:
        rng, t = v["rngstate"], v["t"]
        seed, _, _ = build_seed(rng, 5, 25)
        y_seed_min = min(cy for (_, cy) in seed)
        turns, t_on, records = run_collect_records(seed)
        assert t_on - t == v["t_on_meno_t_atteso"], \
            f"t_on-t {t_on - t} != atteso {v['t_on_meno_t_atteso']}"
        rec = next((r for r in records if r[0] == t), None)
        assert rec is not None, "record non trovato"
        _, rx, ry = rec
        rec_times = [tt for (tt, _, _) in records]
        t_rec_of_row = {ryy: tt for (tt, _, ryy) in records}

        word = tuple(turns[t - K:t])
        r = eval_word(word)
        assert r is not None
        burden, onset_germe, _, residuo = r
        horizon_corto = onset_germe + P

        # 1. ri-verifica: residuo corto tutto bianco al tempo t
        res_abs = [(rx + cx, ry + cy) for (cx, cy) in residuo]
        colors, _ = replay_supply(seed, turns, {t: set(res_abs)})
        whites = [c for c in res_abs if colors[t][c][0] == 0]
        assert len(whites) == len(res_abs) == burden, \
            f"violazione non riprodotta: {len(whites)}/{len(res_abs)} bianche"

        # 2. germe per 2600 passi vs svolte reali da t
        vg, pose = virtual_walk(word)
        anchor = to_anchor_frame(vg, pose)
        germ_black = {c for c, col in anchor.items() if col == 1}
        gturns, n, _, fr, _ = simulate(germ_black, 0, 0, 0, T_DAGGER,
                                       stop_at_onset=False, chk=T_DAGGER + 1)
        L = min(T_DAGGER, len(turns) - t)
        d = next((i for i in range(L) if gturns[i] != turns[t + i]), None)
        assert d is not None, "germe e reale identici fino a 2600?!"
        assert d >= horizon_corto, \
            f"divergenza a {d} < orizzonte corto {horizon_corto}: diagnosi §99c errata!"

        # 3. la cella di divergenza
        cx, cy = walk_to(gturns, d)
        cell_rel = (cx, cy)
        cell_abs = (rx + cx, ry + cy)
        assert cell_rel not in anchor, "divergenza su cella di footprint?!"
        assert cell_rel in fr and fr[cell_rel][0] == d, \
            f"prima lettura del germe {fr.get(cell_rel)} != d={d}"
        germ_reads_white = gturns[d] == 1     # bit 1 = R = lettura bianca
        real_reads_white = turns[t + d] == 1

        # 4. anagrafe reale della cella al tempo t
        colors2, _ = replay_supply(seed, turns, {t: {cell_abs}})
        col, paint_t = colors2[t][cell_abs]
        info = {
            "rngstate": rng, "t": t, "t_on": t_on, "burden": burden,
            "onset_germe": onset_germe, "orizzonte_corto": horizon_corto,
            "residuo_corto_bianco": f"{len(whites)}/{burden}",
            "d_divergenza": d, "cella_rel": list(cell_rel),
            "cella_abs": list(cell_abs), "y_rel": cy,
            "cheb": max(abs(cx), abs(cy)),
            "germe_legge": "bianco" if germ_reads_white else "nero",
            "reale_legge": "bianco" if real_reads_white else "nero",
            "colore_reale_a_t": "nero" if col == 1 else "bianco",
            "origine": None, "eta": None, "ep": None,
        }
        if col == 1:
            if paint_t is None:
                info["origine"] = "SEME"
                assert cell_abs in seed
            else:
                info["origine"] = "dipinta"
                info["eta"] = t - paint_t
                lo = bisect.bisect_right(rec_times, paint_t)
                hi = bisect.bisect_right(rec_times, t)
                info["ep"] = hi - lo
                if cell_abs[1] < y_seed_min and cell_abs[1] < 0:
                    t_row = t_rec_of_row[cell_abs[1]]
                    info["lag_apertura_riga"] = paint_t - t_row
        results.append(info)
        print(f"VIOLATORE rng {rng} t={t}: residuo corto {info['residuo_corto_bianco']} "
              f"bianco RIPRODOTTO; divergenza a d={d} (orizzonte corto "
              f"{horizon_corto}, V-dagger {T_DAGGER}) su cella rel {cell_rel} "
              f"(y_rel {cy}, cheb {info['cheb']}): germe legge "
              f"{info['germe_legge']}, reale legge {info['reale_legge']}; "
              f"colore reale a t: {info['colore_reale_a_t']}, origine "
              f"{info['origine']}, eta' {info['eta']}, ep {info['ep']}", flush=True)

    out = {"violators": results, "T_dagger": T_DAGGER,
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
