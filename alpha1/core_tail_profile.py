# core_tail_profile.py — §82: dove vive la coda lunga? Profilo nucleo/coda del motivo potato
# (p104, r=3, identico a §81) incrociato con ETA' dell'evento (t - ultima visita) e ALIMENTAZIONE
# (vc==1 morso-fed / vc>=2 recycle-fed, definizione §79 riusata verbatim da consumption_ledger_probe).
#
# Domande (roadmap §81.5.1-2):
#   A. La coda lunga delle eta' (age >> periodo, la leva di §79) vive FUORI dal vocabolario
#      universale (nucleo-24)? Se si', isola la parte genuinamente aperiodica.
#   B. Il nucleo coincide con la meccanica del riciclo (recycle-fed) o e' trasversale?
#
# Validazione (doppio gate, fermarsi al primo rosso):
#   1. nev per orbita == deep_motif_saturation_summary.json (§80) esatti;
#   2. nucleo-24 ricostruito: |core| == 1572 e massa per orbita IDENTICA a
#      deep_motif_pruned_summary.json (§81) (pipeline deterministica => uguaglianza esatta).
#
# Bonus per §83: dump dei motivi del nucleo-24 in chiaro (celle relative canoniche) in
# alpha1/core24_motifs.json (materia prima per l'interpretabilita').
import sys, os, json, time, argparse, hashlib, statistics as st
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, forget_outside_ring, ALPHA

DX = (0, 1, 0, -1); DY = (-1, 0, 1, 0)
H = 104
AGE_EDGES = (104, 1040, 10400, 104000)   # bucket: <=104, <=1040, <=10400, <=104000, oltre
NB = len(AGE_EDGES) + 1
VC_CLS = 3                                # vc==1, vc==2, vc>=3 (morso-fed = vc==1, recycle = resto)

def rotk(cells, k):
    for _ in range(k % 4):
        cells = [(-y, x) for (x, y) in cells]
    return cells

def enc(rr):
    return bytes((dx + 3) * 7 + (dy + 3) for (dx, dy) in rr)

def dec(b):
    return [(v // 7 - 3, v % 7 - 3) for v in b]

def abucket(age):
    for i, e in enumerate(AGE_EDGES):
        if age <= e: return i
    return NB - 1

def analyze(arg):
    rng, onset, evpath = arg
    black, side, dens = build_seed(rng, 5, 25)
    known = set(); last = {}; vcount = {}
    x = y = h = 0
    traj = []; pending = []
    cnt = {}                    # dig -> conteggio totale eventi
    repr_new = {}               # dig -> encoding compatto del motivo
    tot = [0] * (NB * VC_CLS)   # totali per cella della griglia bucket x classe
    nev = 0
    evf = open(evpath, "wb")    # stream eventi: 8B dig + 1B cella (bucket*VC_CLS+classe)

    def resolve(ev, tcap):
        nonlocal nev
        te, ax, ay, hh, rel_abs, age, vc = ev
        hi = min(te + H, tcap)
        vis = set(traj[te + 1: hi + 1])
        k = (-hh) % 4
        rel = rotk([(cx - ax, cy - ay) for (cx, cy) in rel_abs if (cx, cy) in vis], k)
        rr = tuple(sorted([(dx, dy) for (dx, dy) in rel if max(abs(dx), abs(dy)) <= 3]))
        dig = hashlib.blake2b(repr(list(rr)).encode(), digest_size=8).digest()
        nev += 1
        cnt[dig] = cnt.get(dig, 0) + 1
        if dig not in repr_new: repr_new[dig] = enc(rr)
        cls = 0 if vc == 1 else (1 if vc == 2 else 2)
        cell = abucket(age) * VC_CLS + cls
        tot[cell] += 1
        evf.write(dig + bytes((cell,)))

    for t in range(onset):
        c = (x, y); isb = c in black
        traj.append(c)
        if isb and c not in known:
            prev = last.get(c)
            if prev is not None:
                pending.append((t, x, y, h, [(cx, cy) for cx in range(x - 3, x + 4)
                                             for cy in range(y - 3, y + 4)
                                             if (cx, cy) in black and not (cx == x and cy == y)],
                                t - prev, vcount.get(c, 0)))
        if isb: black.discard(c); h = (h + 3) & 3
        else: black.add(c); h = (h + 1) & 3
        last[c] = t; vcount[c] = vcount.get(c, 0) + 1; known.add(c)
        x += DX[h]; y += DY[h]
        forget_outside_ring(known, x, y)
        while pending and t - pending[0][0] >= H:
            resolve(pending.pop(0), onset)
    for ev in pending:
        resolve(ev, onset)
    evf.close()
    return {"rng": rng, "onset": onset, "nev": nev, "cnt": cnt,
            "repr": repr_new, "tot": tot, "evpath": evpath}

def med3(vals):
    return st.median(vals), min(vals), max(vals)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--orbits", default="")
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--out", default=str(ALPHA / "core_tail_profile_summary.json"))
    ap.add_argument("--motifs-out", default=str(ALPHA / "core24_motifs.json"))
    a = ap.parse_args()
    t0 = time.time()
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    idxs = list(range(len(dumps))) if not a.orbits else [int(s) for s in a.orbits.split(",")]
    args = [(dumps[i].rngstate, dumps[i].onset_dump, f"/tmp/cte_{i}.bin") for i in idxs]
    nw = a.workers or min(16, os.cpu_count() or 1, len(args))
    if nw > 1:
        with Pool(nw) as pool: res = pool.map(analyze, args)
    else:
        res = []
        for j, xx in enumerate(args):
            res.append(analyze(xx))
            print(f"[{time.time()-t0:7.1f}s] orbita {idxs[j]} fatta ({j+1}/{len(args)})", flush=True)

    # --- GATE 1: nev esatti vs §80 ---
    ref80 = json.load(open(ALPHA / "deep_motif_saturation_summary.json"))["res"]
    g1 = all(r["nev"] == ref80[i]["nev"] for i, r in zip(idxs, res))
    print(f"GATE 1 (nev vs §80): {'OK' if g1 else 'ROSSO: FERMARSI'}")

    # --- nucleo-24 e GATE 2: massa identica a §81 ---
    n_orb = len(res)
    dfreq = {}
    for r in res:
        for dig in r["cnt"]: dfreq[dig] = dfreq.get(dig, 0) + 1
    core = {d for d, f in dfreq.items() if f == n_orb}
    mass = [sum(c for d, c in r["cnt"].items() if d in core) / max(r["nev"], 1) for r in res]
    print(f"nucleo-{n_orb}: {len(core)} motivi; massa med {st.median(mass)*100:.2f}% "
          f"[min {min(mass)*100:.2f}, max {max(mass)*100:.2f}]")
    g2 = True
    ref81p = ALPHA / "deep_motif_pruned_summary.json"
    if n_orb == 24 and ref81p.exists():
        m81 = json.load(open(ref81p))["event_mass"]["p104"]
        g2 = (len(core) == m81["core_all"] and abs(st.median(mass) - m81["mass_all_med"]) < 1e-12)
        print(f"GATE 2 (nucleo/massa vs §81): {'OK' if g2 else 'ROSSO: FERMARSI'}")
    if not (g1 and g2):
        sys.exit(1)

    # streaming: per orbita, conteggi sul nucleo per cella (bucket x classe)
    for r in res:
        cg = [0] * (NB * VC_CLS)
        with open(r["evpath"], "rb") as f:
            while True:
                chunk = f.read(9 * 65536)
                if not chunk: break
                for o in range(0, len(chunk), 9):
                    if chunk[o:o+8] in core: cg[chunk[o+8]] += 1
        r["coregrid"] = cg

    # --- Domanda A: massa sul nucleo per bucket di eta' ---
    labels = ["<=104", "105-1040", "1041-10400", "10401-104000", ">104000"]
    print(f"\nA. massa nucleo per bucket ETA' (mediana orbite [min,max]; quota eventi del bucket):")
    qmassA = []
    for b in range(NB):
        cm, sh = [], []
        for r in res:
            tb = sum(r["tot"][b * VC_CLS: (b + 1) * VC_CLS])
            cb = sum(r["coregrid"][b * VC_CLS: (b + 1) * VC_CLS])
            if tb: cm.append(cb / tb); sh.append(tb / r["nev"])
        if cm:
            m, lo, hi = med3(cm)
            qmassA.append({"bucket": labels[b], "share_med": st.median(sh),
                           "core_mass_med": m, "core_mass_min": lo, "core_mass_max": hi})
            print(f"  {labels[b]:>13}: quota {st.median(sh)*100:5.2f}%  massa-nucleo "
                  f"{m*100:6.2f}% [{lo*100:.2f}, {hi*100:.2f}]")

    # --- Domanda B: massa sul nucleo per classe di alimentazione ---
    clabels = ["vc==1 (morso-fed)", "vc==2", "vc>=3 (recycle)"]
    print(f"\nB. massa nucleo per ALIMENTAZIONE (definizione §79):")
    qmassB = []
    for cl in range(VC_CLS):
        cm, sh = [], []
        for r in res:
            tb = sum(r["tot"][b * VC_CLS + cl] for b in range(NB))
            cb = sum(r["coregrid"][b * VC_CLS + cl] for b in range(NB))
            if tb: cm.append(cb / tb); sh.append(tb / r["nev"])
        if cm:
            m, lo, hi = med3(cm)
            qmassB.append({"classe": clabels[cl], "share_med": st.median(sh),
                           "core_mass_med": m, "core_mass_min": lo, "core_mass_max": hi})
            print(f"  {clabels[cl]:>18}: quota {st.median(sh)*100:5.2f}%  massa-nucleo "
                  f"{m*100:6.2f}% [{lo*100:.2f}, {hi*100:.2f}]")

    # --- interazione: bucket estremi x classe (mediane orbite) ---
    print(f"\nC. interazione eta' x alimentazione (massa-nucleo, mediana orbite):")
    inter = []
    for b in range(NB):
        row = []
        for cl in range(VC_CLS):
            cm = []
            for r in res:
                tb = r["tot"][b * VC_CLS + cl]
                if tb:
                    cm.append(r["coregrid"][b * VC_CLS + cl] / tb)
            row.append(st.median(cm) if cm else None)
        inter.append(row)
        cells = " ".join(f"{v*100:6.2f}%" if v is not None else "   --  " for v in row)
        print(f"  {labels[b]:>13}: {cells}")

    # --- dump motivi del nucleo (per §83) ---
    if n_orb == 24:
        allrepr = {}
        for r in res: allrepr.update(r["repr"])
        totcnt = {}
        for r in res:
            for d, c in r["cnt"].items():
                if d in core: totcnt[d] = totcnt.get(d, 0) + c
        motifs = sorted(({"dig": d.hex(), "cells": dec(allrepr[d]), "n_ev": totcnt[d]}
                         for d in core), key=lambda m: -m["n_ev"])
        json.dump(motifs, open(a.motifs_out, "w"))
        print(f"\nscritto {a.motifs_out} ({len(motifs)} motivi, ordinati per massa)")

    json.dump({"orbits": idxs, "gate1_nev": g1, "gate2_core": g2,
               "core_size": len(core), "mass_med": st.median(mass),
               "age_profile": qmassA, "feed_profile": qmassB,
               "interaction_med": inter,
               "res": [{"rng": r["rng"], "onset": r["onset"], "nev": r["nev"], "tot": r["tot"]}
                       for r in res]},
              open(a.out, "w"), indent=1)
    print(f"scritto {a.out}  (elapsed {time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
