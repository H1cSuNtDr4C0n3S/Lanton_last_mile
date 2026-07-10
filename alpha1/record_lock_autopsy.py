# record_lock_autopsy.py — §101c: AUTOPSIA dei lock F2 (+ campione F1) con lente
# indipendente (stesso macchinario di record_divergence_lens.py: footprint dalla
# griglia reale, non da virtual_walk).
#
# Per ogni testimone F2 (record di classe R con ride >= P): riverifica d, classe,
# ride; poi geometria: parola, fase W0 del tratto, righe scese durante il ride,
# record consecutivi dentro lo stesso ride (EPISODI, lezione §100), cella di
# divergenza (y_rel, cheb, colore, eta'). Per il campione F1: riverifica d e
# min_cheb (il minimo va ricontato dal residuo con macchinario proprio: qui
# ci si limita a d/classe e alla colpevole di divergenza).
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import build_seed
from record_divergence_lens import run_real, germ_turns_from_real

HERE = os.path.dirname(os.path.abspath(__file__))
HUNT = os.path.join(HERE, "record_divergence_hunt_summary.json")
P = 104


def verify(tst, tag):
    rng = int(tst["rngstate"])
    t = int(tst["t"])
    og = int(tst["onset_germe"])
    d_ref = tst["d"]
    seed, _, _ = build_seed(rng, 5, 25)
    t_dag = max(2600, og + 2080)
    # corsa reale lunga abbastanza
    L_req = t + min(t_dag, 10**9)
    turns, grid, traj, pose = run_real(seed, t + t_dag)
    L = t_dag
    gturns, reads = germ_turns_from_real(seed, t, L)
    d = next((i for i in range(min(L, len(turns) - t))
              if gturns[i] != turns[t + i]), None)
    classe = "E" if d is None else ("T" if d < og else "R")
    ride = (d - og) if (d is not None and d >= og) else (0 if d is not None else None)
    ok = (d == d_ref and classe == tst["classe"] and ride == tst["ride"])
    px, py = traj[t]
    div = reads[d] if d is not None else None
    extra = ""
    if classe == "R":
        # righe nuove (y-min) scese durante il ride [t, t+d): record consecutivi
        y_min_pre = py
        new_rows = 0
        t_rows = []
        yy = py
        for i in range(d):
            cx, cy = traj[t + i + 1] if t + i + 1 < len(traj) else traj[-1]
            if cy < yy:
                yy = cy
                new_rows += 1
                t_rows.append(t + i + 1)
        extra = (f" ride={ride} ({ride/P:.1f} periodi), righe nuove nel ride: "
                 f"{new_rows} (t: {t_rows[:8]}...)")
    print(f"{tag} rng {rng} t={t}: d={d} (ref {d_ref}) classe={classe} "
          f"(ref {tst['classe']}) {'PASS' if ok else '*** FAIL ***'}"
          f" div_rel=({div[0]-px},{div[1]-py})" + extra, flush=True)
    return ok


def main():
    hunt = json.load(open(HUNT))
    fails = 0
    print("=== F2 (lock ai record) ===", flush=True)
    for tst in hunt["F2"]:
        if not verify(tst, "F2"):
            fails += 1
    print("\n=== F1 (min_cheb > 8), campione 8 ===", flush=True)
    F1 = sorted(hunt["F1"], key=lambda v: -v["min_cheb"])[:8]
    for tst in F1:
        if not verify(tst, "F1"):
            fails += 1
    # parole dei F2: confronto con la fascia §100 (parole dei testimoni/violatori)
    print("\n=== parole F2 (prefisso 40) ===", flush=True)
    for tst in hunt["F2"]:
        print(f"  onset_germe={tst['onset_germe']} word[:40]={tst['word'][:40]}",
              flush=True)
    print(f"\nAUTOPSIA: {'TUTTO PASS' if fails == 0 else f'{fails} FAIL'}", flush=True)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
