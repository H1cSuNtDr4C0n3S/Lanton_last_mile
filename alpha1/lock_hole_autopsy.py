# lock_hole_autopsy.py — §105b: il MECCANISMO DEI BUCHI della scalinata.
#
# Avviso §105 (a verbale): la scala si rifornisce da sola — le pose-record vecchie
# formano una scalinata nera che ricade nelle palle dei record successivi; il
# rigetto-shallow e' il default. I 2 episodi-lock §101 sono i BUCHI: record in cui
# il read-set del transiente del germe ha mancato TUTTE le nere (residuo-corto
# interamente bianco) e la corsa reale ha cavalcato W0 per 269/384 passi.
#
# Domanda: che cosa ha svuotato il read-set? Tre ipotesi misurabili:
#   H1 (drift laterale): la discesa ha driftato in x, la scalinata e' rimasta da
#      un lato e il transiente legge dall'altro;
#   H2 (consumo recente): le nere della zona erano appena state CONSUMATE
#      (lette->flip bianco) da un passaggio precedente (es. il tentativo fallito
#      del record precedente);
#   H3 (transiente anomalo): la parola-porta ha un transiente che legge quasi
#      solo colonne mai visitate (read-set "storto" rispetto alla scalinata).
#
# Misure per ciascun episodio (+ controllo = record shallow immediatamente
# precedente dello stesso seme):
#   - read-set del transiente (prime-letture < onset_germe, non-footprint,
#     y_rel>=1): quante celle, bbox, colori reali a t (attesi: tutti bianchi
#     nell'episodio, >=1 nero nel controllo);
#   - scalinata: le ultime 30 pose-record prima di t: posizione relativa, colore
#     a t (nera/consumata), distanza minima dal read-set;
#   - storia delle celle del read-set: mai-visitate / visitate-e-bianche a t
#     (consumate: quando? da chi — tentativo precedente?);
#   - drift x della discesa negli ultimi 10 record.
# Uscita: alpha1/lock_hole_autopsy_summary.json
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import build_seed
from record_divergence_lens import run_real, germ_turns_from_real

HERE = os.path.dirname(os.path.abspath(__file__))
HUNT = os.path.join(HERE, "record_divergence_hunt_summary.json")
OUT = os.path.join(HERE, "lock_hole_autopsy_summary.json")
K = 101
DX = (0, 1, 0, -1)
DY = (-1, 0, 1, 0)


def transient_readset(seed, t, onset_germe):
    """Prime-letture del germe (costruito dalla griglia reale, lente §101)
    entro il transiente: ritorna [(cella_rel, i_lettura)], footprint escluso,
    y_rel >= 1."""
    turns, grid, traj, pose = run_real(seed, t)
    px, py = pose[0], pose[1]
    # ricostruisco germe e leggo
    gturns, reads = germ_turns_from_real(seed, t, onset_germe)
    fp = set(traj[t - K:t])
    seen = set()
    out = []
    for i, c in enumerate(reads):
        if c in seen:
            continue
        seen.add(c)
        rel = (c[0] - px, c[1] - py)
        if c not in fp and rel[1] >= 1:
            out.append((rel, i))
    return out, (px, py), grid, traj


def analyze(rng_state, t, onset_germe, label):
    seed, _, _ = build_seed(rng_state, 5, 25)
    rs, (px, py), grid, traj = transient_readset(seed, t, onset_germe)
    # colori reali a t delle celle del read-set + storia
    # run fino a t per griglia; per "quando consumata" servono i tempi: rifaccio
    # una corsa con log di ultima-scrittura
    black = set(c for c in seed)
    lastw = {}
    x = y = 0
    h = 0
    poses = []
    y_min = 0
    rec_poses = []
    for tt in range(t):
        c = (x, y)
        if y < y_min:
            rec_poses.append((tt, c))
            y_min = y
        col = 1 if c in black else 0
        if col == 0:
            h = (h + 1) & 3
            black.add(c)
        else:
            h = (h + 3) & 3
            black.discard(c)
        lastw[c] = tt
        x += DX[h]
        y += DY[h]
    n_black = 0
    visited_white = 0
    never = 0
    consumed_recent = []
    for (rel, i) in rs:
        ca = (px + rel[0], py + rel[1])
        if ca in black:
            n_black += 1
        elif ca in lastw:
            visited_white += 1
            consumed_recent.append(t - lastw[ca])
        else:
            never += 1
    # scalinata: ultime 30 pose-record
    stair = []
    for (tt, c) in rec_poses[-30:]:
        rel = (c[0] - px, c[1] - py)
        stair.append({"rel": list(rel), "nera": c in black,
                      "age": t - tt})
    stair_black_near = [s for s in stair if s["nera"]
                        and max(abs(s["rel"][0]), abs(s["rel"][1])) <= 10]
    # distanza minima scalinata-nera -> read-set
    dmin = None
    for s in stair:
        if not s["nera"]:
            continue
        for (rel, i) in rs:
            d = max(abs(s["rel"][0] - rel[0]), abs(s["rel"][1] - rel[1]))
            dmin = d if dmin is None else min(dmin, d)
    # drift x della discesa (ultimi 10 record)
    if len(rec_poses) >= 11:
        xa = rec_poses[-11][1][0]
        xb = rec_poses[-1][1][0]
        drift_x = xb - xa
    else:
        drift_x = None
    rs_bbox = [min(r[0] for r, _ in rs), max(r[0] for r, _ in rs),
               min(r[1] for r, _ in rs), max(r[1] for r, _ in rs)] if rs else None
    info = {"label": label, "rngstate": rng_state, "t": t,
            "onset_germe": onset_germe,
            "readset_n": len(rs), "readset_bbox_xxyy": rs_bbox,
            "readset_neri": n_black, "readset_bianchi_visitati": visited_white,
            "readset_mai_visitati": never,
            "eta_consumo_bianchi (min/med)": (
                [min(consumed_recent),
                 sorted(consumed_recent)[len(consumed_recent) // 2]]
                if consumed_recent else None),
            "scalinata_nere_entro_cheb10": len(stair_black_near),
            "scalinata_nere_ultime30": sum(1 for s in stair if s["nera"]),
            "dmin_scalinata_nera_vs_readset": dmin,
            "drift_x_ultimi_10_record": drift_x}
    print(json.dumps(info, indent=1), flush=True)
    return info


def main():
    hunt = json.load(open(HUNT))
    eps = [hunt["F2"][0], hunt["F2"][1]]      # episodio A; episodio B (1o record)
    out = []
    for e in eps:
        rng_state = int(e["rngstate"])
        t = int(e["t"])
        og = int(e["onset_germe"])
        out.append(analyze(rng_state, t, og, f"LOCK t={t}"))
        # controllo: record profondo precedente dello stesso seme
        seed, _, _ = build_seed(rng_state, 5, 25)
        turns, grid, traj, pose = run_real(seed, t)
        y_min = 0
        prev_rec = None
        x = y = 0
        # ricalcolo pose-record dai traj (posizioni al tempo tt)
        ymin = 0
        recs = []
        for tt, c in enumerate(traj[:t]):
            if c[1] < ymin:
                recs.append((tt, c))
                ymin = c[1]
        prev = [r for r in recs if r[0] < t - 104 and r[0] >= K]
        assert prev
        tprev = prev[-1][0]
        # onset del germe del controllo: riuso eval_word
        from record_weapon_hunt import eval_word
        turns_full, _, _, _ = run_real(seed, tprev + 1)
        w = tuple(1 if b else 0 for b in turns_full[tprev - K:tprev])
        r = eval_word(w)
        assert r is not None
        out.append(analyze(rng_state, tprev, r[1], f"CONTROLLO t={tprev}"))
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT}", flush=True)


if __name__ == "__main__":
    main()
