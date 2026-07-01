# deep_motif_pruned.py — §81: chiusura del caveat §80.3. Il motivo co-moving agli eventi
# deep-black viene POTATO alla parte causalmente attiva: le sole celle nere (entro raggio r)
# che la formica VISITA/LEGGE nei successivi H passi (H=104, 208). Se l'alfabeto potato
# satura, il caveat entropia-del-detrito era fondato; se non satura, §80 e' confermato
# anche sulla parte attiva e la trappola (o) si estende al motivo potato.
#
# Dinamica + definizione evento deep-black IDENTICHE a deep_motif_saturation.py (§80):
# lettura nera di cella fuori dalla finestra viva (non in `known`) gia' visitata in passato.
# La modalita' FULL (nessuna potatura) e' calcolata nella stessa passata e DEVE riprodurre
# esattamente nev e distinct di alpha1/deep_motif_saturation_summary.json (validazione).
#
# Guardie di onesta':
# - distribuzione taglie del motivo potato (una "saturazione" con motivi quasi vuoti e' vacua);
# - asserzioni per-evento |pruned| <= |full| e pruned104 ⊆ pruned208 ⊆ full (per costruzione,
#   verificate comunque come tripwire di implementazione);
# - traiettoria ricostruita lunga esattamente onset passi.
import sys, os, json, time, argparse, hashlib, statistics as st
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, forget_outside_ring, ALPHA

DX = (0, 1, 0, -1); DY = (-1, 0, 1, 0)
RS = (3, 4, 5)
HS = (104, 208)            # orizzonti di potatura (1 e 2 periodi W0)
HMAX = max(HS)

def rotk(cells, k):
    for _ in range(k % 4):
        cells = [(-y, x) for (x, y) in cells]
    return cells

def hash_rel(rel, r):
    rr = sorted([(dx, dy) for (dx, dy) in rel if max(abs(dx), abs(dy)) <= r])
    return hashlib.blake2b(repr(rr).encode(), digest_size=8).digest(), len(rr)

def analyze(arg):
    rng, onset = arg
    black, side, dens = build_seed(rng, 5, 25)
    known = set(); last = {}; x = y = h = 0
    traj = []                                  # traj[t] = posizione della formica al passo t
    pending = []                               # eventi in attesa della finestra futura
    modes = ("full",) + tuple(f"p{H}" for H in HS)
    seen = {m: {r: set() for r in RS} for m in modes}
    df = {m: {r: 0 for r in RS} for m in modes}
    dl = {m: {r: 0 for r in RS} for m in modes}
    sizes104 = []                              # taglia motivo potato H=104, r=3
    empties104 = 0
    cnt3 = {"p104": {}, "p208": {}}            # molteplicita' motivo -> n. eventi (r=3)
    bkt = {}                                   # p104 r=3: dig -> conteggi per quintile temporale
    agg = {}                                   # p104 r=3: dig -> [n, somma eta']
    nev_q = [0] * 5                            # eventi per quintile
    fc = int(onset * 0.2); lc = int(onset * 0.8)
    nev = 0; viol = 0

    def resolve(ev, tcap):
        nonlocal viol, empties104
        te, ax, ay, hh, rel_abs, age = ev
        k = (-hh) % 4
        rel_full = rotk([(cx - ax, cy - ay) for (cx, cy) in rel_abs], k)
        pruned = {}
        for H in HS:
            hi = min(te + H, tcap)
            vis = set(traj[te + 1: hi + 1])
            rel_p = rotk([(cx - ax, cy - ay) for (cx, cy) in rel_abs if (cx, cy) in vis], k)
            pruned[H] = rel_p
        # tripwire: inclusioni per costruzione
        s104 = set(pruned[104]); s208 = set(pruned[208]); sfull = set(rel_full)
        if not (s104 <= s208 <= sfull):
            viol += 1
        qi = min(4, te * 5 // max(onset, 1))
        nev_q[qi] += 1
        for m, rel in (("full", rel_full),) + tuple((f"p{H}", pruned[H]) for H in HS):
            for r in RS:
                dig, _n = hash_rel(rel, r)
                s = seen[m][r]; b = len(s); s.add(dig); nw = len(s) - b
                if te < fc: df[m][r] += nw
                elif te >= lc: dl[m][r] += nw
                if r == 3 and m in cnt3:
                    cnt3[m][dig] = cnt3[m].get(dig, 0) + 1
                    if m == "p104":
                        bb = bkt.get(dig)
                        if bb is None: bb = bkt[dig] = [0] * 5
                        bb[qi] += 1
                        aa = agg.get(dig)
                        if aa is None: aa = agg[dig] = [0, 0]
                        aa[0] += 1; aa[1] += age
        _dig, n104 = hash_rel(pruned[104], 3)
        sizes104.append(n104)
        if n104 == 0: empties104 += 1

    for t in range(onset):
        c = (x, y); isb = c in black
        traj.append(c)
        if isb and c not in known:
            prev = last.get(c)
            if prev is not None:
                nev += 1
                rel_abs = [(cx, cy) for cx in range(x - 5, x + 6) for cy in range(y - 5, y + 6)
                           if (cx, cy) in black and not (cx == x and cy == y)]
                pending.append((t, x, y, h, rel_abs, t - prev))
        if isb: black.discard(c); h = (h + 3) & 3
        else: black.add(c); h = (h + 1) & 3
        last[c] = t; known.add(c); x += DX[h]; y += DY[h]
        forget_outside_ring(known, x, y)
        while pending and t - pending[0][0] >= HMAX:
            resolve(pending.pop(0), onset)
    for ev in pending:                          # coda: finestre troncate a onset (documentato)
        resolve(ev, onset)
    assert len(traj) == onset, "traiettoria != onset"

    sizes104.sort()
    q = lambda v, p: v[min(int(len(v) * p), len(v) - 1)] if v else 0
    return {"rng": rng, "onset": onset, "side": side, "nev": nev, "viol": viol,
            "distinct": {m: {r: len(seen[m][r]) for r in RS} for m in modes},
            "df": df, "dl": dl, "fc": fc, "lc": onset - lc,
            "set3": {m: list(seen[m][3]) for m in modes},
            "cnt3": cnt3, "bkt": bkt, "agg": agg, "nev_q": nev_q,
            "sz_med": q(sizes104, 0.5), "sz_p90": q(sizes104, 0.9),
            "sz_max": sizes104[-1] if sizes104 else 0,
            "empty_frac": empties104 / max(nev, 1)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--orbits", default="", help="indici separati da virgola (default: tutte)")
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--out", default=str(ALPHA / "deep_motif_pruned_summary.json"))
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
        for j, x in enumerate(args):
            res.append(analyze(x))
            print(f"[{time.time()-t0:7.1f}s] orbita {idxs[j]} fatta ({j+1}/{len(args)})", flush=True)

    # --- VALIDAZIONE contro §80 (modalita' full) ---
    ref_path = ALPHA / "deep_motif_saturation_summary.json"
    ok_all = True
    if ref_path.exists():
        ref = json.load(open(ref_path))["res"]
        print("VALIDAZIONE full-mode vs §80:")
        for i, r in zip(idxs, res):
            rr = ref[i]
            ok = (r["nev"] == rr["nev"] and
                  all(r["distinct"]["full"][k] == rr["distinct"][str(k)] for k in RS))
            ok_all = ok_all and ok
            print(f"  orbita {i}: nev {r['nev']} vs {rr['nev']}, "
                  f"d3 {r['distinct']['full'][3]} vs {rr['distinct']['3']} -> {'OK' if ok else 'MISMATCH'}")
        print(f"  => {'TUTTO OK' if ok_all else 'ROSSO: FERMARSI'}")
    modes = ("full", "p104", "p208")
    print(f"\norbite {len(res)}, elapsed {time.time()-t0:.1f}s, violazioni-inclusione {sum(r['viol'] for r in res)}")
    hdr = f"{'idx':>3} {'onset':>7} {'nev':>6}"
    for m in modes: hdr += f" {m+'_d3':>9}"
    hdr += f" {'p104 new l/f':>12} {'szmed':>5} {'szp90':>5} {'szmax':>5} {'empty%':>6}"
    print(hdr)
    for i, r in zip(idxs, res):
        rf = r["df"]["p104"][3] / max(r["fc"], 1); rl = r["dl"]["p104"][3] / max(r["lc"], 1)
        ratio = rl / max(rf, 1e-12)
        line = f"{i:>3} {r['onset']:>7} {r['nev']:>6}"
        for m in modes: line += f" {r['distinct'][m][3]:>9}"
        line += f" {ratio:>12.3f} {r['sz_med']:>5} {r['sz_p90']:>5} {r['sz_max']:>5} {100*r['empty_frac']:>6.2f}"
        print(line)
    for m in modes:
        sets = [set(bytes(b, 'latin1') if isinstance(b, str) else b for b in r["set3"][m]) for r in res]
        union = set().union(*sets)
        inter = set(sets[0]).intersection(*sets[1:]) if len(sets) > 1 else sets[0]
        sumind = sum(len(s) for s in sets)
        print(f"\n{m} r=3 POOLED: somma {sumind}, UNIONE {len(union)}, INTERSEZIONE {len(inter)}, "
              f"union/sum = {len(union)/max(sumind,1):.3f}")
    dec = [(r["dl"]["p104"][3] / max(r["lc"], 1)) / max(r["df"]["p104"][3] / max(r["fc"], 1), 1e-12) for r in res]
    print(f"\nscoperta nuovi motivi POTATI (H=104, r=3) ultimo20%/primo20% (mediana): {st.median(dec):.3f}")
    print("  (->0 => alfabeto potato SATURA; ~1+ => cresce anche potato = caveat chiuso, §80 confermato)")

    # --- MASSA DI EVENTI sui nuclei condivisi (r=3) ---
    mass = {}
    for m in ("p104", "p208"):
        dfreq = {}
        for r in res:
            for dig in r["cnt3"][m]:
                dfreq[dig] = dfreq.get(dig, 0) + 1
        n_orb = len(res)
        core24 = {d for d, f in dfreq.items() if f == n_orb}
        core12 = {d for d, f in dfreq.items() if f >= (n_orb + 1) // 2}
        m24 = [sum(c for d, c in r["cnt3"][m].items() if d in core24) / max(r["nev"], 1) for r in res]
        m12 = [sum(c for d, c in r["cnt3"][m].items() if d in core12) / max(r["nev"], 1) for r in res]
        mass[m] = {"core_all": len(core24), "core_maj": len(core12),
                   "mass_all_med": st.median(m24), "mass_all_min": min(m24), "mass_all_max": max(m24),
                   "mass_maj_med": st.median(m12), "mass_maj_min": min(m12), "mass_maj_max": max(m12)}
        print(f"\n{m} r=3 MASSA EVENTI: nucleo-24 {len(core24)} motivi -> massa per orbita "
              f"med {st.median(m24)*100:.2f}% [min {min(m24)*100:.2f}, max {max(m24)*100:.2f}]")
        print(f"  nucleo-maggioranza (>= {(n_orb+1)//2} orbite) {len(core12)} motivi -> massa "
              f"med {st.median(m12)*100:.2f}% [min {min(m12)*100:.2f}, max {max(m12)*100:.2f}]")
        if m == "p104":
            # stazionarieta' within-orbit: massa sul nucleo-24 per quintile temporale
            qmass = [[] for _ in range(5)]
            for r in res:
                tot_q = r["nev_q"]
                core_q = [0] * 5
                for dig, bb in r["bkt"].items():
                    if dig in core24:
                        for qi in range(5): core_q[qi] += bb[qi]
                for qi in range(5):
                    if tot_q[qi]: qmass[qi].append(core_q[qi] / tot_q[qi])
            line = "  stazionarieta' within-orbit (massa nucleo-24 per quintile, mediana orbite): "
            line += " ".join(f"Q{qi+1} {st.median(v)*100:.2f}%" for qi, v in enumerate(qmass))
            print(line)
            mass[m]["qmass_med"] = [st.median(v) for v in qmass]
            # eta' media: eventi sul nucleo-24 vs fuori nucleo (per orbita, poi mediana)
            ac, at = [], []
            for r in res:
                nc = sc = nt_ = st_ = 0
                for dig, (n, sa) in r["agg"].items():
                    if dig in core24: nc += n; sc += sa
                    else: nt_ += n; st_ += sa
                if nc: ac.append(sc / nc)
                if nt_: at.append(st_ / nt_)
            print(f"  eta' media evento: nucleo-24 {st.median(ac):.0f} vs fuori-nucleo {st.median(at):.0f} (mediana orbite)")
            mass[m]["age_core_med"] = st.median(ac); mass[m]["age_tail_med"] = st.median(at)
    json.dump({"orbits": idxs,
               "res": [{k: v for k, v in r.items() if k not in ("set3", "cnt3", "bkt", "agg")} for r in res],
               "event_mass": mass,
               "validation_full_vs_80": ok_all},
              open(a.out, "w"), indent=1)
    print(f"scritto {a.out}")

if __name__ == "__main__":
    main()
