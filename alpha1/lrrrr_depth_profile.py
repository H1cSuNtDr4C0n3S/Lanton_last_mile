# lrrrr_depth_profile.py — §85a: a quale raggio di finestra inizia l'evitamento di (LRRRR)^3?
# §84 ha stabilito: 0 match su tutti gli eventi deep-r4 (~1,5M), ma ~0,18% delle letture nere
# generiche matcha. Qui ogni lettura nera pre-onset viene classificata per profondita' di
# conoscenza: deep_r = cella gia' visitata ma NON in known_r (finestra viva di raggio r), per
# r=1,2,3,4 simultanei (catena deep_4 ⊆ deep_3 ⊆ deep_2 ⊆ deep_1, verificata come tripwire).
# Il piu' piccolo r con zero match tra i deep_r e' il raggio dove il teorema puo' vivere e dove
# tentare il certificato automa (§85b): il certificato a raggio r copre TUTTE le letture nere
# fuori-finestra-r, quindi r minore = teorema piu' forte.
#
# Gate: il conteggio dei match totali per orbita deve essere coerente con la baseline §84
# (ordine 0,18% delle letture nere) e i deep_4 devono dare 0 match (riproduzione §84).
import sys, os, json, time, argparse, statistics as st
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA

DX = (0, 1, 0, -1); DY = (-1, 0, 1, 0)
RS = (1, 2, 3, 4)
WORD = bytes([1, 0, 0, 0, 0] * 3)   # (LRRRR)^3, L=1 (nero), 15 svolte
WL = len(WORD)

def forget_r(known, x, y, r):
    r1 = r + 1
    for cx, cy in ([(x - r1, y + d) for d in range(-r1, r1 + 1)] +
                   [(x + r1, y + d) for d in range(-r1, r1 + 1)] +
                   [(x + d, y - r1) for d in range(-r1, r1 + 1)] +
                   [(x + d, y + r1) for d in range(-r1, r1 + 1)]):
        if (cx, cy) in known and max(abs(cx - x), abs(cy - y)) > r:
            known.discard((cx, cy))

def analyze(arg):
    rng, onset = arg
    black, side, dens = build_seed(rng, 5, 25)
    known = {r: set() for r in RS}
    last = {}
    x = y = h = 0
    turns = bytearray()
    pending = []                      # (t, flag_visited, deep_r bools)
    nblack = 0
    tot = {r: 0 for r in RS}; mat = {r: 0 for r in RS}
    tot_inw = 0; mat_inw = 0          # letture nere in-finestra a TUTTI i raggi (visitate)
    tot_fresh = 0; mat_fresh = 0      # letture nere mai visitate (seme)
    tot_all = 0; mat_all = 0
    chain_viol = 0

    for t in range(onset):
        c = (x, y); isb = c in black
        turns.append(1 if isb else 0)
        if isb:
            visited = c in last
            deep = tuple((visited and c not in known[r]) for r in RS)
            # tripwire catena: deep_4 => deep_3 => deep_2 => deep_1
            for a in range(len(RS) - 1):
                if deep[a + 1] and not deep[a]:
                    chain_viol += 1
            pending.append((t, visited, deep))
        if isb: black.discard(c); h = (h + 3) & 3
        else: black.add(c); h = (h + 1) & 3
        last[c] = t
        for r in RS: known[r].add(c)
        x += DX[h]; y += DY[h]
        for r in RS: forget_r(known[r], x, y, r)
        while pending and t - pending[0][0] >= WL:
            te, visited, deep = pending.pop(0)
            m = bytes(turns[te:te + WL]) == WORD
            tot_all += 1; mat_all += m
            if not visited:
                tot_fresh += 1; mat_fresh += m
            elif not any(deep):
                tot_inw += 1; mat_inw += m
            for i, r in enumerate(RS):
                if deep[i]:
                    tot[r] += 1; mat[r] += m
        nblack += isb
    # coda troncata: scartata (finestra parola incompleta), conteggiata
    ntrunc = len(pending)
    return {"rng": rng, "onset": onset, "nblack": nblack, "ntrunc": ntrunc,
            "chain_viol": chain_viol,
            "tot_all": tot_all, "mat_all": mat_all,
            "tot_fresh": tot_fresh, "mat_fresh": mat_fresh,
            "tot_inw": tot_inw, "mat_inw": mat_inw,
            "tot": tot, "mat": mat}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--orbits", default="")
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--out", default=str(ALPHA / "lrrrr_depth_summary.json"))
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

    cv = sum(r["chain_viol"] for r in res)
    print(f"TRIPWIRE catena deep_4⊆deep_3⊆deep_2⊆deep_1: {'OK (0 violazioni)' if cv == 0 else f'ROSSO: {cv} violazioni'}")
    if cv: sys.exit(1)

    def pooled(tk, mk):
        T = sum(r[tk] if isinstance(r[tk], int) else 0 for r in res)
        M = sum(r[mk] if isinstance(r[mk], int) else 0 for r in res)
        return T, M
    print(f"\nmatch (LRRRR)^3 per popolazione (pooled 24 orbite):")
    T, M = pooled("tot_all", "mat_all")
    print(f"  {'tutte le letture nere':>28}: {M:>6} / {T:>9}  ({100*M/max(T,1):.4f}%)")
    T, M = pooled("tot_fresh", "mat_fresh")
    print(f"  {'mai visitate (seme)':>28}: {M:>6} / {T:>9}  ({100*M/max(T,1):.4f}%)")
    T, M = pooled("tot_inw", "mat_inw")
    print(f"  {'in-finestra a ogni r':>28}: {M:>6} / {T:>9}  ({100*M/max(T,1):.4f}%)")
    prof = {}
    for r in RS:
        T = sum(x["tot"][r] for x in res); M = sum(x["mat"][r] for x in res)
        prof[r] = {"tot": T, "mat": M}
        print(f"  {'deep_r='+str(r):>28}: {M:>6} / {T:>9}  ({100*M/max(T,1):.4f}%)")
    print(f"\n(gate §84: deep_4 deve avere 0 match — {'OK' if prof[4]['mat'] == 0 else 'ROSSO'})")
    rstar = None
    for r in RS:
        if prof[r]["mat"] == 0:
            rstar = r; break
    print(f"raggio minimo con evitamento empirico esatto: r* = {rstar}")
    print(f"=> tentare il certificato automa (§85b) a raggio r*, poi eventualmente scendere.")
    json.dump({"orbits": idxs, "profile": {str(r): prof[r] for r in RS},
               "rstar": rstar,
               "res": res}, open(a.out, "w"), indent=1)
    print(f"scritto {a.out}  (elapsed {time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
