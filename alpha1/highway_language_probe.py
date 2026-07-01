# highway_language_probe.py — §83: il vocabolario universale (nucleo-24, §81-§82) e' il
# linguaggio quasi-periodico "di transito"? Confronto con il linguaggio locale della highway pura.
#
# Bersaglio equo: la highway in territorio vergine non rivisita territorio dimenticato, quindi
# (quasi certamente) non ha eventi deep-black. L'analogo corretto e' L_hw = insieme dei motivi
# potati (p104, r=3, C4-normalizzati, centro escluso — pipeline IDENTICA a §81/§82) estratti a
# OGNI lettura nera post-onset sul regime di highway pura. Per periodicita' (W0, periodo 104)
# L_hw deve SATURARE a un insieme finito, e deve coincidere tra orbite (stessa highway a meno
# di simmetria, quozientata dalla normalizzazione C4).
#
# Domande:
#   A. |L_hw|? satura? identico tra orbite? (check interni)
#   B. L_hw ⊆ nucleo-24? quanti dei 1.572 motivi sono linguaggio-highway?
#   C. (il numero chiave) quanta MASSA del traffico deep-black pre-onset cade su L_hw?
#      Confronto con la massa del nucleo (35,63%): se mass(L_hw) ~ mass(core∩L_hw) ~ 35% il
#      nucleo E' il linguaggio di transito; se molto minore, il nucleo e' piu' del transito.
#
# Validazione (fermarsi al primo rosso):
#   GATE 1: nev pre-onset per orbita == §80 esatti (stessa definizione evento).
#   GATE 2: nucleo-24 ricostruito == 1572 motivi, massa mediana identica a §81 (determinismo).
#   GATE 3: L_hw satura (taglia a 10 periodi == taglia a 20 periodi, per orbita).
# NOTA tcap: gli eventi pre-onset risolvono la finestra futura troncata a onset (tcap=onset),
# identico a §81/§82, anche se la simulazione ora prosegue oltre — necessario per il GATE 2.
import sys, os, json, time, argparse, hashlib, statistics as st
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, forget_outside_ring, ALPHA

DX = (0, 1, 0, -1); DY = (-1, 0, 1, 0)
H = 104
SETTLE = 2 * 104        # periodi di assestamento post-onset prima della raccolta
KPER = 20               # periodi raccolti per L_hw
KCHK = 10               # checkpoint saturazione

def rotk(cells, k):
    for _ in range(k % 4):
        cells = [(-y, x) for (x, y) in cells]
    return cells

def motif_dig(rel):
    rr = sorted([(dx, dy) for (dx, dy) in rel if max(abs(dx), abs(dy)) <= 3])
    return hashlib.blake2b(repr(rr).encode(), digest_size=8).digest()

def analyze(arg):
    rng, onset = arg
    black, side, dens = build_seed(rng, 5, 25)
    known = set(); last = {}
    x = y = h = 0
    traj = []
    pend_pre = []; pend_hw = []
    cnt = {}                     # pre-onset: dig -> conteggio eventi deep-black
    nev = 0
    lhw = set()                  # linguaggio highway
    lhw_chk = None               # taglia al checkpoint (GATE 3)
    t_collect0 = onset + SETTLE
    t_collect1 = t_collect0 + KPER * H
    t_chk = t_collect0 + KCHK * H
    t_end = t_collect1 + H       # margine per risolvere le finestre future

    def extract(te, ax, ay, hh, rel_abs, tcap):
        hi = min(te + H, tcap)
        vis = set(traj[te + 1: hi + 1])
        k = (-hh) % 4
        rel = rotk([(cx - ax, cy - ay) for (cx, cy) in rel_abs if (cx, cy) in vis], k)
        return motif_dig(rel)

    for t in range(t_end):
        c = (x, y); isb = c in black
        traj.append(c)
        if isb:
            rel_abs = None
            if t < onset and c not in known and last.get(c) is not None:
                rel_abs = [(cx, cy) for cx in range(x - 3, x + 4) for cy in range(y - 3, y + 4)
                           if (cx, cy) in black and not (cx == x and cy == y)]
                pend_pre.append((t, x, y, h, rel_abs))
            elif t_collect0 <= t < t_collect1:
                rel_abs = [(cx, cy) for cx in range(x - 3, x + 4) for cy in range(y - 3, y + 4)
                           if (cx, cy) in black and not (cx == x and cy == y)]
                pend_hw.append((t, x, y, h, rel_abs))
        if isb: black.discard(c); h = (h + 3) & 3
        else: black.add(c); h = (h + 1) & 3
        last[c] = t; known.add(c)
        x += DX[h]; y += DY[h]
        forget_outside_ring(known, x, y)
        while pend_pre and t - pend_pre[0][0] >= H:
            te, ax, ay, hh, ra = pend_pre.pop(0)
            dig = extract(te, ax, ay, hh, ra, onset)   # tcap=onset, identico a §81/§82
            nev += 1; cnt[dig] = cnt.get(dig, 0) + 1
        while pend_hw and t - pend_hw[0][0] >= H:
            te, ax, ay, hh, ra = pend_hw.pop(0)
            if te >= t_chk and lhw_chk is None:
                lhw_chk = len(lhw)                     # taglia a KCHK periodi
            lhw.add(extract(te, ax, ay, hh, ra, t_end))
    for te, ax, ay, hh, ra in pend_pre:
        dig = extract(te, ax, ay, hh, ra, onset)
        nev += 1; cnt[dig] = cnt.get(dig, 0) + 1
    for te, ax, ay, hh, ra in pend_hw:
        if te >= t_chk and lhw_chk is None:
            lhw_chk = len(lhw)
        lhw.add(extract(te, ax, ay, hh, ra, t_end))
    if lhw_chk is None: lhw_chk = len(lhw)
    return {"rng": rng, "onset": onset, "nev": nev, "cnt": cnt,
            "lhw": list(lhw), "lhw_chk": lhw_chk}

def med3(v): return st.median(v), min(v), max(v)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--orbits", default="")
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--out", default=str(ALPHA / "highway_language_summary.json"))
    a = ap.parse_args()
    t0 = time.time()
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    idxs = list(range(len(dumps))) if not a.orbits else [int(s) for s in a.orbits.split(",")]
    args = [(dumps[i].rngstate, dumps[i].onset_dump) for i in idxs]
    nw = a.workers or min(16, os.cpu_count() or 1, len(args))
    if nw > 1:
        with Pool(nw) as pool: res = pool.map(analyze, args)
    else:
        res = []
        for j, xx in enumerate(args):
            res.append(analyze(xx))
            print(f"[{time.time()-t0:7.1f}s] orbita {idxs[j]} fatta ({j+1}/{len(args)})", flush=True)

    n_orb = len(res)
    ref80 = json.load(open(ALPHA / "deep_motif_saturation_summary.json"))["res"]
    g1 = all(r["nev"] == ref80[i]["nev"] for i, r in zip(idxs, res))
    print(f"GATE 1 (nev pre-onset vs §80): {'OK' if g1 else 'ROSSO: FERMARSI'}")

    dfreq = {}
    for r in res:
        for dig in r["cnt"]: dfreq[dig] = dfreq.get(dig, 0) + 1
    core = {d for d, f in dfreq.items() if f == n_orb}
    mass_core = [sum(c for d, c in r["cnt"].items() if d in core) / max(r["nev"], 1) for r in res]
    g2 = True
    ref81p = ALPHA / "deep_motif_pruned_summary.json"
    if n_orb == 24 and ref81p.exists():
        m81 = json.load(open(ref81p))["event_mass"]["p104"]
        g2 = (len(core) == m81["core_all"] and abs(st.median(mass_core) - m81["mass_all_med"]) < 1e-12)
    print(f"GATE 2 (nucleo/massa vs §81): {'OK' if g2 else 'ROSSO: FERMARSI'} "
          f"({len(core)} motivi, massa med {st.median(mass_core)*100:.2f}%)")

    g3 = all(len(r["lhw"]) == r["lhw_chk"] for r in res)
    print(f"GATE 3 (L_hw satura a {KCHK} periodi): {'OK' if g3 else 'ROSSO: FERMARSI'}")
    if not (g1 and g2 and g3): sys.exit(1)

    sets = [set(r["lhw"]) for r in res]
    lhw_union = set().union(*sets)
    lhw_inter = set(sets[0]).intersection(*sets[1:]) if n_orb > 1 else sets[0]
    szs = [len(s) for s in sets]
    print(f"\nA. |L_hw| per orbita: med {st.median(szs):.0f} [min {min(szs)}, max {max(szs)}]; "
          f"unione {len(lhw_union)}, intersezione {len(lhw_inter)} "
          f"({'IDENTICO tra orbite' if len(lhw_union)==len(lhw_inter) else 'varia tra orbite'})")

    inter_core = core & lhw_union
    print(f"\nB. sovrapposizione: |L_hw ∩ nucleo-24| = {len(inter_core)} "
          f"({100*len(inter_core)/max(len(lhw_union),1):.1f}% di L_hw; "
          f"{100*len(inter_core)/max(len(core),1):.1f}% del nucleo)")

    m_lhw = [sum(c for d, c in r["cnt"].items() if d in lhw_union) / max(r["nev"], 1) for r in res]
    m_both = [sum(c for d, c in r["cnt"].items() if d in inter_core) / max(r["nev"], 1) for r in res]
    m, lo, hi = med3(m_lhw)
    print(f"\nC. massa del traffico deep-black pre-onset:")
    print(f"   su L_hw:          {m*100:6.2f}% [{lo*100:.2f}, {hi*100:.2f}]")
    m, lo, hi = med3(m_both)
    print(f"   su L_hw ∩ nucleo: {m*100:6.2f}% [{lo*100:.2f}, {hi*100:.2f}]")
    m, lo, hi = med3(mass_core)
    print(f"   su nucleo (rif.): {m*100:6.2f}% [{lo*100:.2f}, {hi*100:.2f}]")

    # top core motifs in L_hw?
    mot_path = ALPHA / "core24_motifs.json"
    topin = None
    if mot_path.exists():
        mot = json.load(open(mot_path))
        topin = [bytes.fromhex(x["dig"]) in lhw_union for x in mot[:20]]
        print(f"\nD. top-20 motivi del nucleo presenti in L_hw: {sum(topin)}/20 "
              f"(pattern: {''.join('X' if b else '.' for b in topin)})")

    json.dump({"orbits": idxs, "gates": [g1, g2, g3],
               "lhw_sizes": szs, "lhw_union": len(lhw_union), "lhw_inter": len(lhw_inter),
               "overlap_core": len(inter_core),
               "mass_lhw": m_lhw, "mass_lhw_core": m_both, "mass_core": mass_core,
               "top20_in_lhw": topin},
              open(a.out, "w"), indent=1)
    print(f"\nscritto {a.out}  (elapsed {time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
