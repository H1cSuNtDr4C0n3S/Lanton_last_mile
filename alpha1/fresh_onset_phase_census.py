# fresh_onset_phase_census.py — §103.1: le DUE PORTE reggono senza selezione?
#
# PREREGISTRAZIONE (fissata prima della run): §102 misura porta-0 20/24 +
# porta-24/25 4/24 + ZERO fuori-cluster sugli onset delle 24 orbite canoniche
# (selezionate per onset alto, trappola h). Qui: fase W0 dell'onset di semi
# FRESCHI catena-3 (riuso dichiarato della catena §101; disgiunzione da catene
# 1-2 gia' verificata li').
#   FALSIFICATORE F: onset con fase FUORI dai cluster {0} U {97..103} U {24,25}.
#     Aspettativa: APERTA (i cluster §102 sono su n=24: possono essere quantili
#     — trappola qq — o struttura; questo censimento decide).
#   POTENZA: >= 1000 onset censiti; sotto, dichiarare sottopotenza.
#   Osservabili secondarie: quote porta-0 vs porta-24/25; distribuzione ext 1..7
#     (il modello a moneta 2^-k e' testabile con n grande).
# Gate: le 24 canoniche riprodotte bit-identiche a §102 (fase per orbita).
# Uscita: alpha1/fresh_onset_phase_census_summary.json
import sys, os, json, time, argparse
import multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, xs, ALPHA
from record_word_census import run_collect_records

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "fascia_door_probe_summary.json")
OUT = os.path.join(HERE, "fresh_onset_phase_census_summary.json")
BASE = 0x9E3779B97F4A7C15
GOLD = 0xBF58476D1CE4E5B9

W0 = open(os.path.join(HERE, "..", "data", "w0.txt")).read().strip()
W0b = "".join("1" if c == "R" else "0" for c in W0)
ROTS = {W0b[k:] + W0b[:k]: k for k in range(104)}
assert len(ROTS) == 104


def fresh_states(n, base=None):
    s = xs(xs(BASE if base is None else base))
    out = []
    for _ in range(n):
        out.append(s)
        s = xs(xs(s ^ GOLD))
    return out


def phase_of_seed(rngstate):
    seed, _, _ = build_seed(rngstate, 5, 25)
    if not seed or min(cy for (_, cy) in seed) > 0:
        return {"rngstate": rngstate, "skip": True}
    turns, t_on, _ = run_collect_records(seed)
    if t_on < 0:
        return {"rngstate": rngstate, "no_onset": True}
    per = "".join(str(b) for b in turns[t_on:t_on + 104])
    per2 = "".join(str(b) for b in turns[t_on + 104:t_on + 208])
    assert per == per2, f"coda non periodica rng {rngstate}"
    ph = ROTS.get(per)
    assert ph is not None, f"coda non-W0 rng {rngstate}"
    return {"rngstate": rngstate, "onset": t_on, "fase": ph}


def _worker(s):
    try:
        return phase_of_seed(s)
    except AssertionError as e:
        return {"rngstate": s, "assert_error": str(e)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-seeds", type=int, default=2500)
    ap.add_argument("--workers", type=int, default=14)
    args = ap.parse_args()
    t0 = time.time()

    # gate: 24 canoniche == §102
    ref = json.load(open(REF))
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    for od, rr in zip(dumps, ref["onset_reali"]):
        got = phase_of_seed(od.rngstate)
        assert got["fase"] == rr["fase_W0"] and got["onset"] == rr["onset"], \
            f"orb {od.index}: fase/onset != §102"
    print("GATE: 24/24 canoniche bit-identiche a §102", flush=True)

    base3 = xs(BASE ^ 0x94D049BB133111EB)
    states = fresh_states(args.n_seeds, base=base3)
    with mp.Pool(args.workers) as pool:
        results = pool.map(_worker, states, chunksize=8)

    errors = [r for r in results if r.get("assert_error")]
    assert not errors, f"assert nei worker: {errors[:3]}"
    ok = [r for r in results if "fase" in r]
    skip = sum(1 for r in results if r.get("skip"))
    noon = sum(1 for r in results if r.get("no_onset"))
    fasi = [r["fase"] for r in ok]
    hist = {}
    for p in fasi:
        hist[p] = hist.get(p, 0) + 1

    in0 = sum(1 for p in fasi if p == 0)
    ext = sum(1 for p in fasi if 97 <= p <= 103)
    p24 = sum(1 for p in fasi if p in (24, 25))
    fuori = [r for r in ok if r["fase"] != 0 and not 97 <= r["fase"] <= 103
             and r["fase"] not in (24, 25)]
    ext_hist = {str(104 - p): sum(1 for q in fasi if q == p)
                for p in range(97, 104)}

    potenza = len(ok) >= 1000
    if not potenza:
        verdetto = f"SOTTOPOTENZIATO ({len(ok)} onset < 1000)"
    elif fuori:
        verdetto = (f"F REALIZZATO: {len(fuori)} onset fuori-cluster "
                    f"(fasi {sorted(set(r['fase'] for r in fuori))[:20]}) — "
                    f"i cluster §102 erano quantili")
    else:
        verdetto = ("F VUOTO CON POTENZA: due porte confermate senza selezione "
                    "(resta empirico, trappola i)")

    out = {"preregistrazione": {
               "falsificatore": "onset fresco con fase fuori {0}U{97..103}U{24,25}",
               "potenza": ">=1000 onset", "aspettativa": "APERTA (dichiarata)"},
           "n_seeds": args.n_seeds, "onset_censiti": len(ok),
           "skip": skip, "no_onset": noon,
           "porta_0_esatta": in0, "ext_97_103": ext, "porta_24_25": p24,
           "fuori_cluster": [{"rngstate": r["rngstate"], "onset": r["onset"],
                              "fase": r["fase"]} for r in fuori],
           "hist_fasi": {str(k): hist[k] for k in sorted(hist)},
           "ext_hist_1_7": ext_hist,
           "VERDETTO_PREREGISTRATO": verdetto,
           "elapsed_s": round(time.time() - t0, 1)}
    print(f"semi {args.n_seeds}: onset {len(ok)} (skip {skip}, no-onset {noon})",
          flush=True)
    print(f"porta-0 esatta {in0} ({in0/len(ok):.3f}), ext 97-103 {ext} "
          f"({ext/len(ok):.3f}), porta-24/25 {p24} ({p24/len(ok):.3f}), "
          f"FUORI {len(fuori)} ({len(fuori)/len(ok):.4f})", flush=True)
    print(f"ext hist (1..7): {ext_hist}", flush=True)
    for r in fuori[:15]:
        print(f"  !!! FUORI: rng {r['rngstate']} onset {r['onset']} fase {r['fase']}",
              flush=True)
    print(f"VERDETTO: {verdetto}", flush=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
