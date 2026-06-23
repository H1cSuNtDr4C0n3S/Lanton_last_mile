# altmin_driver.py — calcolo di delta4_alt per taglio iterativo dei cicli-fantasma.
# Loop: estrai il ciclo minimo corrente (min_assumeB extract, con cutsfile) -> check di
# alternanza della parola ciclica (max_power_realizable, cap 50) -> se fantasma: classifica
# il PRIMO conflitto (cella, offset nel periodo, distanza temporale, stesso periodo o no),
# taglia i suoi archi assumiB e ripeti. Si fermano due soglie:
#   delta4_alt    = primo ciclo alternanza-consistente (>= 50 potenze)
#   delta4_alt_BT = primo ciclo alternanza-consistente E non B-T-uccidibile
# ONESTA': il valore ottenuto e' il minimo del grafo TAGLIATO, quindi un upper bound di
# delta4_alt "vero" relativo al catalogo: ogni arco tagliato e' certificato da un fantasma
# esplicito, ma un ciclo consistente piu' economico potrebbe passare per un arco tagliato.
# Il catalogo dei fantasmi e' la base del Lemma A; la certificazione esaustiva e' teoria futura.
# Riprendibile: i tagli sono append-only in build/r4c_cuts.txt; log in results/delta4_alt.log.

import json, os, subprocess, sys, time

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build")
sys.path.insert(0, os.path.join(ROOT, "code"))
from window_automaton import canon, drift_and_rot  # noqa: E402

EXE = os.path.join(ROOT, "code", "min_assumeB.exe")
CUTS = os.path.join(BUILD, "r4c_cuts.txt")
CATALOG = os.path.join(ROOT, "results", "delta4_alt_catalog.jsonl")
DX = [0, 1, 0, -1]; DY = [1, 0, -1, 0]
POWER_CAP = 50
MAXROUNDS = 60
MU_CAP = 0.25
MAX_ITERS = 60


def first_conflict(word, kmax=POWER_CAP):
    """simula word^k; al primo conflitto di alternanza ritorna i dettagli; None se ok."""
    lastt = {}
    x = y = h = 0
    L = len(word)
    for t in range(L * kmax):
        c = word[t % L]
        tt = 1 if c == "R" else 0
        prev = lastt.get((x, y))
        if prev is not None and tt != 1 - prev[0]:
            return {"step": t, "periodo": t // L, "offset": t % L, "cella": [x, y],
                    "lettura_prec": prev[1], "distanza": t - prev[1],
                    "stesso_periodo": prev[1] // L == t // L}
        lastt[(x, y)] = (tt, t)
        h = (h + 1) & 3 if tt else (h - 1) & 3
        x += DX[h]; y += DY[h]
    return None


def parse_cycle():
    lines = open(os.path.join(BUILD, "r4c_delta_cycle.txt")).read().split()
    p, q, word, types = int(lines[1]), int(lines[3]), lines[5], lines[7]
    annot = [l.split() for l in open(os.path.join(BUILD, "r4c_delta_cycle_annot.txt"))
             if not l.startswith("#")]
    dstnode = [int(a[3]) for a in annot]
    bedges = [(dstnode[(k - 1) % q], dstnode[k]) for k in range(q) if types[k] == "B"]
    return p, q, word, types, bedges


def main():
    open(CUTS, "a").close()
    mu = (float(sys.argv[1]) if len(sys.argv) > 1 else 2 / 313) * (1 + 1e-6)
    max_iters = int(sys.argv[2]) if len(sys.argv) > 2 else MAX_ITERS
    found_alt = None
    t0 = time.time()
    seen = set()
    for it in range(1, max_iters + 1):
        rc = subprocess.call([EXE, BUILD, "r4c", "extract", f"{mu:.12f}",
                              str(MAXROUNDS), CUTS],
                             stdout=open(os.path.join(ROOT, "results", "delta4_alt_extract.log"), "w"),
                             stderr=subprocess.STDOUT)
        if rc == 5:  # fixpoint: nessun ciclo < mu nel grafo tagliato
            print(f"[{it}] mu={mu:.8f}: fixpoint, alzo mu  ({time.time()-t0:.0f}s)", flush=True)
            mu *= 1.3
            if mu > MU_CAP:
                print("mu oltre il cap: il grafo tagliato non ha piu' cicli economici", flush=True)
                break
            continue
        if rc != 0:
            print(f"[{it}] extract rc={rc}: ERRORE", flush=True)
            break
        p, q, word, types, bedges = parse_cycle()
        mean = p / q
        cw = canon(word)
        rot, dr = drift_and_rot(word)
        bt = "B-T" if (rot % 4 != 0 or dr == (0, 0)) else "NO-B-T"
        conf = first_conflict(word)
        rec = {"iter": it, "p": p, "q": q, "mean": mean, "rot": rot, "drift": list(dr),
               "bt": bt, "conflitto": conf, "word": word, "types": types,
               "b_edges": bedges, "dup": cw in seen}
        seen.add(cw)
        with open(CATALOG, "a") as f:
            f.write(json.dumps(rec) + "\n")
        if conf is None:
            tag = "CONSISTENTE"
            if found_alt is None:
                found_alt = (p, q, word)
                print(f"[{it}] *** delta4_alt = {p}/{q} = {mean:.6f} ({bt}) ***", flush=True)
            if bt == "NO-B-T":
                print(f"[{it}] *** sopravvissuto pieno (consistente, no B-T): {p}/{q} — STOP ***",
                      flush=True)
                break
            # consistente ma B-T: catalogato, tagliato, si continua (bersaglio Lemma A)
        else:
            tag = (f"fantasma (conflitto periodo {conf['periodo']}, offset {conf['offset']}, "
                   f"cella {conf['cella']}, distanza {conf['distanza']}, "
                   f"{'stesso periodo' if conf['stesso_periodo'] else 'cross-periodo'})")
        print(f"[{it}] ciclo {p}/{q} = {mean:.6f} rot={rot:+d} drift={tuple(dr)} {bt}: {tag}"
              f"  ({time.time()-t0:.0f}s)", flush=True)
        with open(CUTS, "a") as f:
            for s, d in bedges:
                f.write(f"{s} {d}\n")
        mu = max(mu, mean * (1 + 1e-6))
    print(f"\nfine: delta4_alt {'= %d/%d' % found_alt[:2] if found_alt else 'NON trovato'} "
          f"dopo {it} iterazioni, {time.time()-t0:.0f}s; catalogo: {CATALOG}", flush=True)


if __name__ == "__main__":
    main()
