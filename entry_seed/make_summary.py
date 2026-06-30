import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clib

# Campioni trovati dal brute (entry_seed/brute.c), box [-3,3] salvo b=1 verificato anche su [-12,12].
CHAMP = {
 "1": {"fastest": [[0,-2]], "nearest": [[1,3]]},
 "2": {"fastest": [[-1,3],[1,3]], "nearest": [[0,-1],[1,-1]]},
 "3": {"fastest": [[1,-3],[-2,-1],[-1,-1]], "nearest": [[-2,-3],[0,-1],[1,-1]]},
 "4": {"fastest": [[-2,-1],[-1,0],[-1,3],[2,3]], "nearest": [[-3,-2],[-1,-1],[1,0],[3,0]]},
 "5": {"fastest": [[1,-3],[-1,-1],[-2,0],[-3,1],[-1,1]], "nearest": [[-3,-2],[-1,-1],[-2,0],[1,0],[3,0]]},
}


def certify(cells):
    r = clib.simulate(np.array(cells), 0, 0, 0, 200000, 1500)
    onset, word = clib.detect_onset(r["turns"])
    if onset is None:
        return {"onset": None}
    cls, d = clib.classify_word(word)
    lx, ly = clib.lock_position(r["turns"], onset)
    return {"onset": int(onset), "class": cls, "ham": int(d),
            "lock": [int(lx), int(ly)], "lockdist": int(abs(lx) + abs(ly))}


germs = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "germs_22.json")))
gmin = min(g["support"] for g in germs.values())
gmin_phases = [k for k, g in germs.items() if g["support"] == gmin]

out = {
 "convention": "libant.c / CLAUDE.md §2; W0 period 104; reference empty->9977, (7,-7)->106258",
 "method": "forward brute force, seeds = b black cells in box, ant at (0,0,0); reset-touched",
 "phi_ent": [0,16,21,24,25,26,30,31,72,83,90,91,92,93,94,97,98,99,100,101,102,103],
 "germ_min_support": gmin, "germ_min_phases": [int(p) for p in gmin_phases], "germ_onset": 0,
 "empty_grid_onset": 9977,
 "Q1_fastest_entry": {}, "Q2_nearest_lock": {},
}
for b, c in CHAMP.items():
    f = certify(c["fastest"]); n = certify(c["nearest"])
    out["Q1_fastest_entry"][b] = {"seed": c["fastest"], **f}
    out["Q2_nearest_lock"][b] = {"seed": c["nearest"], **n}

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed_frontier.json")
json.dump(out, open(p, "w"), indent=1)
print("Q1 frontiera supporto -> onset (ri-certificato):")
print("  b=0 (vuota): 9977")
for b in ["1","2","3","4","5"]:
    e = out["Q1_fastest_entry"][b]; print("  b=%s: onset=%s class=%s lockdist=%s seed=%s" % (b, e["onset"], e["class"], e["lockdist"], e["seed"]))
print("  germe (%d celle, fasi %s): onset 0" % (gmin, gmin_phases))
print("Q2 aggancio piu' vicino:")
for b in ["1","2","3","4","5"]:
    e = out["Q2_nearest_lock"][b]; print("  b=%s: lockdist=%s onset=%s seed=%s" % (b, e["lockdist"], e["onset"], e["seed"]))
print("salvato", p)
