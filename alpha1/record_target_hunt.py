# record_target_hunt.py — §90b: caccia CONCRETA a un passato di w101 che visiti (1,1).
#
# L'automa a scatola (§90a) dichiara (1,1) raggiungibile nell'ASTRATTO, ma la
# raggiungibilita' in una sovra-approssimazione non dimostra nulla (trappola c al
# contrario). Qui si tenta di REALIZZARE il corno (b) della dicotomia: best-first
# sull'albero reale dei passati (realizzabile + record-compatibile, onset non richiesto),
# priorita' = distanza Chebyshev della coda da (1,1), poi profondita'. Se un passato
# visita (1,1): la vietanza eterna e' FALSA e il verdetto passa alla parola estesa.
# Se la caccia fallisce entro il budget: riporta l'approccio minimo per profondita'
# (il "muro geometrico" attorno a (1,1)).
# Uscita: alpha1/record_target_hunt_summary.json
import sys, os, json, time, heapq, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY, rotk
from kwindow_spoiler_census import virtual_walk, to_anchor_frame
from record_weapon_vitality import to_bits, SUMMARY

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "record_target_hunt_summary.json")
TGT = (1, 1)


def tail_state(word):
    """(valida, posa_coda_anchor, visita_tgt) del cammino di word (ext+w101)."""
    vg, pose = virtual_walk(word)
    if vg is None:
        return False, None, False
    anchor = to_anchor_frame(vg, pose)
    if any(cy < 1 for (_, cy) in anchor):
        return False, None, False
    # posa della coda = prima posizione del cammino, in anchor
    xx = yy = 0
    hh = 0
    for b in word:
        if b:
            hh = (hh + 1) & 3
        else:
            hh = (hh + 3) & 3
        xx += DX[hh]
        yy += DY[hh]
    k = (-hh) % 4
    tail = rotk((0 - xx, 0 - yy), k)
    return True, tail, TGT in anchor


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nodes", type=int, default=1_500_000)
    ap.add_argument("--max-depth", type=int, default=140)
    ap.add_argument("--budget-s", type=int, default=900)
    args = ap.parse_args()
    t0 = time.time()

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])

    def cheb(c):
        return max(abs(c[0] - TGT[0]), abs(c[1] - TGT[1]))

    ok, tail0, hit0 = tail_state(w101)
    assert ok and not hit0
    heap = [(cheb(tail0), 0, ())]        # (priorita', prof., ext)
    seen = 0
    best_by_depth = {}
    found = None
    tie = 0
    while heap and seen < args.nodes and time.time() - t0 < args.budget_s:
        pri, dep, ext = heapq.heappop(heap)
        if dep >= args.max_depth:
            continue
        for bit in (0, 1):
            e2 = (bit,) + ext
            seen += 1
            ok, tail, hit = tail_state(e2 + w101)
            if not ok:
                continue
            if hit:
                found = "".join("R" if b else "L" for b in e2)
                heap.clear()
                break
            c = cheb(tail)
            if c < best_by_depth.get(dep + 1, 99):
                best_by_depth[dep + 1] = c
            tie += 1
            heapq.heappush(heap, (c, dep + 1, e2))
    el = round(time.time() - t0, 1)

    approach = min(best_by_depth.values()) if best_by_depth else None
    if found:
        print(f"CORNO (b) ATTIVATO: passato che visita (1,1) trovato "
              f"(prof. {len(found)}): {found}", flush=True)
    else:
        print(f"nessuna visita a (1,1) in {seen} nodi (prof. max esplorata "
              f"{max(best_by_depth) if best_by_depth else 0}); approccio minimo della "
              f"coda a (1,1): cheb {approach}", flush=True)
        prof_min = sorted((v, k) for k, v in best_by_depth.items())[:8]
        print(f"migliori avvicinamenti (cheb, prof.): {prof_min}", flush=True)

    out = {"nodes": seen, "found": found,
           "best_cheb_overall": approach,
           "best_cheb_by_depth": {str(k): v for k, v in sorted(best_by_depth.items())},
           "elapsed_s": el}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {el} s", flush=True)


if __name__ == "__main__":
    main()
