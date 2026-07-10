# fascia_door_probe.py — §102: la fascia word-mediated e' UNA PORTA (fase W0 = 0),
# e gli onset reali si concentrano su DUE porte.
#
# Tre misure (piu' gate ed esche):
#   1. FASCIA (14 parole uniche: testimoni §100 + lock F2 §101): per ogni parola,
#      onset_germe, burden, drift del germe e FASE W0 della coda del germe all'onset
#      (fase = rotazione k di data/w0.txt che combacia con gturns[onset:onset+104];
#      univoca: le 104 rotazioni di W0 sono tutte distinte, verificato).
#   2. TRONCAMENTO: eval_word(word[-K':]) per K' crescente — la realizzabilita'
#      arriva subito (K'=20) ma l'onset CAMBIA: il germe veloce dipende dall'intera
#      finestra 101 (footprint all'indietro cambia i colori, come §87e).
#   3. ONSET REALI delle 24 orbite canoniche: fase W0 di turns[t_on:t_on+104]
#      (gate: onset == header; coda periodica per==per2 assert).
#
# Esche: bit corrotto nella coda => fase None (beccata); controllo positivo fase 13.
# Uscita: alpha1/fascia_door_probe_summary.json
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA
from record_weapon_hunt import eval_word
from record_divergence_census import germ_long_run
from record_word_census import run_collect_records

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "fascia_door_probe_summary.json")

W0 = open(os.path.join(HERE, "..", "data", "w0.txt")).read().strip()
W0b = "".join("1" if c == "R" else "0" for c in W0)
assert len(W0b) == 104


def phase_of(per):
    """Fase = k tale che per == rotazione-k di W0 (None se non-W0)."""
    return next((k for k in range(104) if W0b[k:] + W0b[:k] == per), None)


def bits(w):
    return tuple(1 if c == "R" else 0 for c in w)


def main():
    t0 = time.time()
    # ---- gate/esche dell'estrattore di fase ----
    rots = {W0b[k:] + W0b[:k] for k in range(104)}
    assert len(rots) == 104, "rotazioni degeneri: fase non univoca"
    per13 = W0b[13:] + W0b[:13]
    assert phase_of(per13) == 13
    bad = per13[:50] + ("0" if per13[50] == "1" else "1") + per13[51:]
    assert phase_of(bad) is None, "esca non beccata"

    # ---- 1+2: fascia ----
    m2 = json.load(open(os.path.join(HERE, "record_minep_hunt_summary2.json")))
    h = json.load(open(os.path.join(HERE, "record_divergence_hunt_summary.json")))
    words = sorted(set(t["word"] for t in m2["TESTIMONI_minep_gt5"])
                   | set(t["word"] for t in h["F2"]))
    fascia = []
    for w in words:
        r = eval_word(bits(w))
        assert r is not None
        og = r[1]
        gturns, fr, tdag, drift, fp, xs, ys = germ_long_run(bits(w), og)
        per = "".join(str(b) for b in gturns[og:og + 104])
        ph = phase_of(per)
        assert ph is not None, "coda del germe non-W0?!"
        # troncamento: primo K' realizzabile e onset a quel K'
        kmin = None
        o_k = None
        for K2 in range(20, len(w) + 1):
            rt = eval_word(bits(w[-K2:]))
            if rt is not None:
                kmin, o_k = K2, rt[1]
                break
        fascia.append({"word": w, "onset_germe": og, "burden": r[0],
                       "fase_W0": ph, "drift": list(drift),
                       "Kmin_realizzabile": kmin, "onset_a_Kmin": o_k})
        print(f"fascia: onset={og:4d} burden={r[0]:4d} fase={ph:3d} "
              f"drift={drift} K'min={kmin} onset@K'={o_k}", flush=True)

    # ---- 3: onset reali ----
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    reali = []
    for od in dumps:
        seed, _, _ = build_seed(od.rngstate, 5, 25)
        turns, t_on, records = run_collect_records(seed)
        assert t_on == od.onset_header, f"orb {od.index}: onset != header"
        per = "".join(str(b) for b in turns[t_on:t_on + 104])
        per2 = "".join(str(b) for b in turns[t_on + 104:t_on + 208])
        assert per == per2, f"orb {od.index}: coda non periodica"
        ph = phase_of(per)
        assert ph is not None
        reali.append({"orbit": od.index, "onset": t_on, "fase_W0": ph})
        print(f"reale: orb {od.index:2d} fase={ph}", flush=True)

    fasi_fascia = sorted(f["fase_W0"] for f in fascia)
    fasi_reali = sorted(r["fase_W0"] for r in reali)

    def clusters(fasi):
        # estensione all'indietro: ext = (104 - fase) % 104
        return {"esatta_0": sum(1 for p in fasi if p == 0),
                "ext_1_7 (97..103)": sum(1 for p in fasi if 97 <= p <= 103),
                "porta_24_25": sum(1 for p in fasi if p in (24, 25)),
                "altre": sum(1 for p in fasi
                             if p != 0 and not 97 <= p <= 103
                             and p not in (24, 25))}

    out = {"fascia": fascia, "onset_reali": reali,
           "fasi_fascia": fasi_fascia, "fasi_reali": fasi_reali,
           "cluster_fascia": clusters(fasi_fascia),
           "cluster_reali": clusters(fasi_reali),
           "esche": "bit corrotto => None; fase 13 OK; 104 rotazioni distinte",
           "elapsed_s": round(time.time() - t0, 1)}
    print(f"\nFASCIA cluster: {out['cluster_fascia']}", flush=True)
    print(f"REALI  cluster: {out['cluster_reali']}", flush=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
