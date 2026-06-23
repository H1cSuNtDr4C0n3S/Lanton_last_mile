# check_witnesses.py — per ogni testimone delta del prodotto (build/<pfx>_delta_cycle.txt)
# riporta: media p/q, rot/drift, B-T?, alternanza (first_conflict), realizzabilita' (gamma_enum).
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from window_automaton import drift_and_rot, max_power_realizable, realizable
from altmin_driver import first_conflict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMMA = os.path.join(ROOT, "code", "gamma_enum.exe")

for pfx in sys.argv[1:]:
    fn = os.path.join(ROOT, "build", f"{pfx}_delta_cycle.txt")
    if not os.path.exists(fn):
        print(f"{pfx}: nessun delta_cycle"); continue
    d = dict(l.split(maxsplit=1) for l in open(fn) if l.strip())
    p, q, w = int(d["p"]), int(d["q"]), d["word"].strip()
    rot, dr = drift_and_rot(w)
    bt = "B-T" if (rot % 4 != 0 or dr == (0, 0)) else "NO-B-T"
    conf = first_conflict(w)
    alt = "alternanza-OK" if conf is None else f"FANTASMA(d={conf['distanza']},step={conf['step']})"
    rz = realizable(w)
    tmp = os.path.join(ROOT, "build", f"tmp_{pfx}.txt")
    open(tmp, "w").write(w)
    g = subprocess.run([GAMMA, "check", tmp], capture_output=True, text=True)
    gline = [l for l in g.stdout.splitlines() if "ACCEPT" in l or "REJECT" in l]
    print(f"{pfx}: {p}/{q}={p/q:.5f} rot={rot:+d} drift={dr} {bt} | {alt} | "
          f"realizz={rz} pow={max_power_realizable(w)} | gamma: {gline[0] if gline else g.stdout.strip()[:60]}")
