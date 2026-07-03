# u2_cover_rail_map.py — §91b: la GEOMETRIA del muro dietro la copertura (per U2).
#
# U2 (aperta): ogni coprente muore all'indietro entro D limitato (misurato: bianche
# muro esatto [1x12,0], nere <= 4). Per trasformarla in lemma serve capire DOVE vive la
# continuazione forzata: se resta in una TASCA spazialmente limitata attorno a (1,1)
# fino alla morte, un'analisi esatta-in-tasca (esterno = sopravvivenza, alla HALO §85)
# puo' certificare U2 con un check finito.
#
# Per ogni coprente del censimento §90c: enumera ESAUSTIVAMENTE il muro dei prepend
# sopra la parola estesa e registra:
#   - profondita' di estinzione e conteggi per livello;
#   - CELLE toccate dalla continuazione (coordinate anchor, relative a (1,1));
#   - bbox della continuazione; causa di morte dei rami (irrealizzabile vs y<1);
#   - la continuazione rientra nel colletto/footprint di w101?
# Uscita: alpha1/u2_cover_rail_map_summary.json
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY, rotk
from kwindow_spoiler_census import virtual_walk, to_anchor_frame
from record_weapon_vitality import to_bits, SUMMARY

HERE = os.path.dirname(os.path.abspath(__file__))
CC = os.path.join(HERE, "record_cover_census_summary.json")
OUT = os.path.join(HERE, "u2_cover_rail_map_summary.json")
TGT = (1, 1)


def valid(word):
    vg, pose = virtual_walk(word)
    if vg is None:
        return None, "irrealizzabile"
    anchor = to_anchor_frame(vg, pose)
    if any(cy < 1 for (_, cy) in anchor):
        return None, "y<1"
    return anchor, None


def tail_cell(word):
    """Cella della coda (posizione piu' antica) in frame anchor."""
    x = y = 0
    h = 0
    for b in word:
        if b:
            h = (h + 1) & 3
        else:
            h = (h + 3) & 3
        x += DX[h]
        y += DY[h]
    k = (-h) % 4
    return rotk((0 - x, 0 - y), k)


def main():
    t0 = time.time()
    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    cc = json.load(open(CC))

    rows = []
    for r in cc["rows"]:
        w2 = to_bits(r["word_ext"]) + w101
        # muro esaustivo con celle e cause di morte
        level = [()]
        counts = []
        cells = set()
        deaths = {"irrealizzabile": 0, "y<1": 0}
        dep = 0
        while level and dep < 30:
            dep += 1
            nxt = []
            for pref in level:
                for bit in (0, 1):
                    p2 = (bit,) + pref
                    a, err = valid(p2 + w2)
                    if err:
                        deaths[err] += 1
                        continue
                    cells.add(tail_cell(p2 + w2))
                    nxt.append(p2)
            counts.append(len(nxt))
            level = nxt
        rel = [(c[0] - TGT[0], c[1] - TGT[1]) for c in cells]
        bbox = ([min(c[0] for c in rel), max(c[0] for c in rel),
                 min(c[1] for c in rel), max(c[1] for c in rel)] if rel else None)
        rows.append({"depth": r["depth"], "colore_11": r["colore_11"],
                     "wall": counts, "D": len([c for c in counts if c > 0]),
                     "deaths": deaths, "cells_rel_11": sorted(rel), "bbox_rel_11": bbox})
        print(f"prof.{r['depth']:3d} {r['colore_11']} muro {counts[:14]} "
              f"D={rows[-1]['D']} morti {deaths} bbox(rel (1,1)) {bbox}", flush=True)

    # sintesi: tasca comune?
    all_cells = set()
    for row in rows:
        all_cells |= {tuple(c) for c in row["cells_rel_11"]}
    Dmax = max(row["D"] for row in rows)
    print(f"\nSINTESI: D max {Dmax}; celle della continuazione (rel. a (1,1), "
          f"unione su {len(rows)} coprenti): {len(all_cells)} celle, "
          f"bbox x[{min(c[0] for c in all_cells)},{max(c[0] for c in all_cells)}] "
          f"y[{min(c[1] for c in all_cells)},{max(c[1] for c in all_cells)}]", flush=True)
    out = {"rows": rows, "D_max": Dmax,
           "union_cells_rel_11": sorted(map(list, all_cells)),
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
