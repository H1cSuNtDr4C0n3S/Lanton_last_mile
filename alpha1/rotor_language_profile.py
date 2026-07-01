# rotor_language_profile.py — §84: il vocabolario universale (nucleo-24) vive sulle cavalcate
# di rotore? Dopo la disgiunzione dalla highway (§83), i rotori espliciti B-T del censimento
# finestra (radius1..4_cycles.txt) sono l'ultima famiglia quasi-periodica nota.
#
# Metodo: per ogni evento deep-black pre-onset (stessa definizione/pipeline §80-§83), la parola
# di svolta futura turns[te : te+3p] viene confrontata con ogni parola PRIMITIVA del censimento
# (match = 3 PERIODI PIENI uguali a una ROTAZIONE della parola ripetuta — trappola d; 2 periodi
# sono statisticamente banali per p piccole), con priorita' alla p minima; controllo:
# periodicita' generica q in 2..15 su 3 periodi. BASELINE NULLA empirica: stesso classificatore
# su ancore pseudo-casuali (LCG deterministico) dello stesso flusso di svolte -> l'eccesso
# sopra il caso e' misurato, non presunto. Poi incrocio con la membership al nucleo-24
# (streaming binario anti-OOM come §82).
#
# Domande:
#   A. incidenza: quanti eventi deep-black siedono su una cavalcata di rotore? (attesa: pochi —
#      le cavalcate sono finite, <=4 periodi, per il Teorema della Finestra §40)
#   B. il nucleo e' concentrato sulle cavalcate? core-mass per classe vs 35,63% globale.
#      Se piatta anche qui, l'omogeneita' (trappola q) si estende ai rotori e il nucleo resta
#      senza antenati periodici noti.
#
# Gate (fermarsi al primo rosso): (1) nev == §80 esatti 24/24; (2) nucleo ricostruito == 1572
# motivi e massa mediana == §81 a precisione macchina.
import sys, os, json, time, argparse, hashlib, statistics as st
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, forget_outside_ring, ALPHA

DX = (0, 1, 0, -1); DY = (-1, 0, 1, 0)
H = 104
ROOT = ALPHA.parent
QMAX = 15

def primitive(w):
    n = len(w)
    for d in range(1, n):
        if n % d == 0 and w == w[:d] * (n // d):
            return w[:d]
    return w

def load_census():
    words = []
    for f in ("radius1_cycles.txt", "radius2_cycles.txt",
              "radius3_cycles.txt", "radius4_cycles.txt"):
        p = ROOT / f
        if p.exists():
            for line in p.read_text().split():
                w = primitive(line.strip())
                if w and w not in words: words.append(w)
    words.sort(key=len)
    return words

CENSUS = load_census()

NPER = 3   # periodi pieni richiesti per un match

def compile_word(w):
    b = bytes(1 if ch == 'L' else 0 for ch in w)
    return {bytes(b[k:] + b[:k]) * NPER for k in range(len(b))}

CENSUS_SETS = [(len(w), compile_word(w)) for w in CENSUS]
# classi: 0 = none; 1..len(CENSUS) = parola censimento (per p crescente);
#         CLS_GEN = periodico generico q<=QMAX non-censimento; CLS_TRUNC = finestra troncata.
CLS_GEN = len(CENSUS) + 1
CLS_TRUNC = len(CENSUS) + 2
NCLS = len(CENSUS) + 3

def classify(turns, te, onset):
    matched_trunc = True   # diventa False se almeno una finestra intera ci sta
    for ci, (p, ss) in enumerate(CENSUS_SETS):
        if te + NPER * p <= onset:
            matched_trunc = False
            if bytes(turns[te:te + NPER * p]) in ss:
                return 1 + ci
    if matched_trunc:
        return CLS_TRUNC
    for q in range(2, QMAX + 1):
        if te + NPER * q > onset: break
        if all(turns[te + i] == turns[te + i + q] for i in range((NPER - 1) * q)):
            return CLS_GEN
    return 0

def rotk(cells, k):
    for _ in range(k % 4):
        cells = [(-y, x) for (x, y) in cells]
    return cells

def motif_dig(rel):
    rr = sorted([(dx, dy) for (dx, dy) in rel if max(abs(dx), abs(dy)) <= 3])
    return hashlib.blake2b(repr(rr).encode(), digest_size=8).digest()

def analyze(arg):
    rng, onset, evpath = arg
    black, side, dens = build_seed(rng, 5, 25)
    known = set(); last = {}
    x = y = h = 0
    traj = []; turns = bytearray(); pending = []
    cnt = {}; nev = 0
    tot = [0] * NCLS
    evf = open(evpath, "wb")

    def resolve(ev):
        nonlocal nev
        te, ax, ay, hh, rel_abs = ev
        hi = min(te + H, onset)
        vis = set(traj[te + 1: hi + 1])
        k = (-hh) % 4
        rel = rotk([(cx - ax, cy - ay) for (cx, cy) in rel_abs if (cx, cy) in vis], k)
        dig = motif_dig(rel)
        cls = classify(turns, te, onset)
        nev += 1
        cnt[dig] = cnt.get(dig, 0) + 1
        tot[cls] += 1
        evf.write(dig + bytes((cls,)))

    for t in range(onset):
        c = (x, y); isb = c in black
        traj.append(c)
        turns.append(1 if isb else 0)
        if isb and c not in known:
            prev = last.get(c)
            if prev is not None:
                pending.append((t, x, y, h,
                                [(cx, cy) for cx in range(x - 3, x + 4)
                                 for cy in range(y - 3, y + 4)
                                 if (cx, cy) in black and not (cx == x and cy == y)]))
        if isb: black.discard(c); h = (h + 3) & 3
        else: black.add(c); h = (h + 1) & 3
        last[c] = t; known.add(c)
        x += DX[h]; y += DY[h]
        forget_outside_ring(known, x, y)
        # la classificazione richiede turns fino a te+2*p_max: risolviamo con ritardo MAXDELAY
        while pending and t - pending[0][0] >= MAXDELAY:
            resolve(pending.pop(0))
    for ev in pending:
        resolve(ev)
    evf.close()
    # baseline nulla: ancore pseudo-casuali del flusso reale CONDIZIONATE a lettura nera (turn L)
    null_tot = [0] * NCLS
    span = onset - MAXDELAY
    state = rng | 1
    filled = 0
    while filled < nev:
        state = (state * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        pos = (state >> 16) % span
        if turns[pos] != 1:      # baseline condizionata a lettura nera (come gli eventi)
            continue
        null_tot[classify(turns, pos, onset)] += 1
        filled += 1
    return {"rng": rng, "onset": onset, "nev": nev, "cnt": cnt, "tot": tot,
            "null_tot": null_tot, "evpath": evpath}

MAXDELAY = max(H, NPER * max(len(w) for w in CENSUS))

def med3(v): return st.median(v), min(v), max(v)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--orbits", default="")
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--out", default=str(ALPHA / "rotor_language_summary.json"))
    a = ap.parse_args()
    t0 = time.time()
    print("censimento parole primitive:", ", ".join(f"{w}(p{len(w)})" for w in CENSUS))
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    idxs = list(range(len(dumps))) if not a.orbits else [int(s) for s in a.orbits.split(",")]
    args = [(dumps[i].rngstate, dumps[i].onset_dump, f"/tmp/rlp_{i}.bin") for i in idxs]
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
    print(f"GATE 1 (nev vs §80): {'OK' if g1 else 'ROSSO: FERMARSI'}")
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
    if not (g1 and g2): sys.exit(1)

    # streaming: per orbita, conteggi sul nucleo per classe
    for r in res:
        cg = [0] * NCLS
        with open(r["evpath"], "rb") as f:
            while True:
                chunk = f.read(9 * 65536)
                if not chunk: break
                for o in range(0, len(chunk), 9):
                    if chunk[o:o+8] in core: cg[chunk[o+8]] += 1
        r["coregrid"] = cg

    labels = ["nessuna"] + [f"{w} (p{len(w)})" for w in CENSUS] + [f"periodica generica q<={QMAX}", "troncata"]
    print(f"\nincidenza (vs baseline nulla) e massa-nucleo per classe (mediana orbite [min,max]):")
    prof = []
    for cl in range(NCLS):
        sh, nl, cm = [], [], []
        for r in res:
            tb = r["tot"][cl]
            sh.append(tb / r["nev"]); nl.append(r["null_tot"][cl] / r["nev"])
            if tb: cm.append(r["coregrid"][cl] / tb)
        shm = st.median(sh); nlm = st.median(nl)
        exc = shm / nlm if nlm > 0 else float("inf")
        row = {"classe": labels[cl], "share_med": shm, "null_med": nlm}
        if cm:
            m, lo, hi = med3(cm)
            row.update({"core_mass_med": m, "core_mass_min": lo, "core_mass_max": hi})
            print(f"  {labels[cl]:>32}: quota {shm*100:8.4f}% (nulla {nlm*100:7.4f}%, x{exc:5.1f})  "
                  f"massa-nucleo {m*100:6.2f}% [{lo*100:.2f}, {hi*100:.2f}]")
        else:
            print(f"  {labels[cl]:>32}: quota {shm*100:8.4f}% (nulla {nlm*100:7.4f}%)  (nessun evento)")
        prof.append(row)
    m, lo, hi = med3(mass_core)
    print(f"  {'TUTTE (rif. §81)':>32}: quota 100.0000%  massa-nucleo {m*100:6.2f}% [{lo*100:.2f}, {hi*100:.2f}]")

    # quota della massa del nucleo che cade su cavalcate (classi censimento + generica)
    ride_cls = list(range(1, len(CENSUS) + 1)) + [CLS_GEN]
    ride_core_share = []
    for r in res:
        core_tot = sum(r["coregrid"])
        if core_tot:
            ride_core_share.append(sum(r["coregrid"][cl] for cl in ride_cls) / core_tot)
    m, lo, hi = med3(ride_core_share)
    print(f"\nquota degli eventi-nucleo che siede su una cavalcata (censimento o q<={QMAX}): "
          f"{m*100:.3f}% [{lo*100:.3f}, {hi*100:.3f}]")

    json.dump({"orbits": idxs, "census": CENSUS, "gates": [g1, g2],
               "profile": prof, "ride_core_share": ride_core_share,
               "mass_core": mass_core,
               "res": [{"rng": r["rng"], "onset": r["onset"], "nev": r["nev"], "tot": r["tot"]}
                       for r in res]},
              open(a.out, "w"), indent=1)
    print(f"scritto {a.out}  (elapsed {time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
