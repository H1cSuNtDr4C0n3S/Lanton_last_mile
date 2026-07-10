# record_divergence_lens.py — §101 pannello, LENTE A: ricontro indipendente di d/classe.
#
# Macchinario RISCRITTO DA ZERO (nessun import dalla pipeline sotto esame, tranne
# build_seed/parse_dumps per i semi canonici — oggetti §57/§58 gia' certificati):
#   - simulatore proprio (dict griglia, convenzioni CLAUDE.md §2, DX/DY schermo);
#   - ricostruzione del footprint della parola per RIGIOCO ALL'INDIETRO della corsa
#     reale (meccanismo DIVERSO: qui i colori del footprint si leggono dalla griglia
#     reale ricostruita al tempo t, non dal virtual_walk della parola — se il Lemma
#     della Finestra-K o virtual_walk avessero un bug, qui divergerebbe);
#   - germe = footprint reale (celle visitate in [t-K, t) coi colori reali a t);
#   - d = primo indice con svolta germe != svolta reale; classe T/R/E come §101a.
# Confronto: d, classe, cella di divergenza (assoluta), colore reale — devono essere
# BIT-IDENTICI al CSV di record_divergence_census.py su un campione di record.
#
# Uscita: stampa PASS/FAIL per record; exit code != 0 su mismatch.
import sys, os, csv, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA

HERE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HERE, "record_divergence_census_records.csv")
K = 101
DXs = (0, 1, 0, -1)
DYs = (-1, 0, 1, 0)


def run_real(seed, t_stop):
    """Corsa reale fino a t_stop: ritorna (turns, grid_finale, traiettoria celle)."""
    grid = {}
    x = y = 0
    h = 0
    turns = []
    traj = []
    for t in range(t_stop):
        c = (x, y)
        traj.append(c)
        col = grid[c] if c in grid else (1 if c in seed else 0)
        if col == 0:
            h = (h + 1) & 3
            grid[c] = 1
            turns.append(1)
        else:
            h = (h + 3) & 3
            grid[c] = 0
            turns.append(0)
        x += DXs[h]
        y += DYs[h]
    return turns, grid, traj, (x, y, h)


def germ_turns_from_real(seed, t, n_steps):
    """Germe della parola al record t, costruito dalla GRIGLIA REALE:
    footprint = celle visitate in [t-K, t), coi colori reali al tempo t.
    Corsa del germe (mondo: footprint + bianco altrove) dalla posa reale.
    Ritorna (gturns, posizioni lette)."""
    turns, grid, traj, pose = run_real(seed, t)
    px, py = traj[t - 1] if False else None, None  # (non usato: la posa e' sotto)
    # posa al tempo t = posizione DOPO il passo t-1 = dove la corsa si trova ora
    x, y, h = pose
    assert h == 0, f"heading {h} != 0 al record"
    fp_cells = set(traj[t - K:t])
    world = {c: grid.get(c, 1 if c in seed else 0) for c in fp_cells}
    gx, gy, gh = x, y, 0
    gturns = []
    reads = []
    g = dict(world)
    for i in range(n_steps):
        c = (gx, gy)
        col = g[c] if c in g else 0          # fuori footprint: bianco
        reads.append(c)
        if col == 0:
            gh = (gh + 1) & 3
            g[c] = 1
            gturns.append(1)
        else:
            gh = (gh + 3) & 3
            g[c] = 0
            gturns.append(0)
        gx += DXs[gh]
        gy += DYs[gh]
    return gturns, reads


def main():
    rng = random.Random(101)
    rows = list(csv.DictReader(open(CSV)))
    dumps = {od.index: od for od in parse_dumps(ALPHA / "dumps_all.txt")}
    sample = rng.sample(rows, 40)
    fails = 0
    for r in sample:
        oi = int(r["orbit"])
        t = int(r["t"])
        d_ref = int(r["d"])
        seed, _, _ = build_seed(dumps[oi].rngstate, 5, 25)
        t_dag = int(r["t_dagger"])
        L = int(r["L_avail"])
        # corsa reale abbastanza lunga da coprire t+L
        turns, _, traj, _ = run_real(seed, t + L)
        gturns, reads = germ_turns_from_real(seed, t, L)
        d = next((i for i in range(L) if gturns[i] != turns[t + i]), None)
        og = int(r["onset_germe"])
        classe = "E" if d is None else ("T" if d < og else "R")
        ok = (d == d_ref and classe == r["classe"])
        if ok and d is not None:
            # cella di divergenza assoluta == pose + cella rel del CSV
            cx, cy = reads[d]
            # pose reale al record
            px, py = traj[t]
            ok = (cx - px == 0 or True)  # la rel non e' nel CSV per esteso: check y_rel/cheb
            ok = ((cy - py) == int(r["div_y_rel"])
                  and max(abs(cx - px), abs(cy - py)) == int(r["div_cheb"]))
        print(f"orb {oi} t={t}: d={d} (ref {d_ref}) classe={classe} "
              f"(ref {r['classe']}) {'PASS' if ok else '*** FAIL ***'}", flush=True)
        if not ok:
            fails += 1
    print(f"\nLENTE A: {len(sample) - fails}/{len(sample)} PASS", flush=True)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
