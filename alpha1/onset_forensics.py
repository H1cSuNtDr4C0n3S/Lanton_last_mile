# onset_forensics.py — §87c: autopsia degli onset reali (24 orbite) + scarico del
# KILL-GATE §79.1 (deep-black-anchored decisive-depth).
#
# Due domande:
#   1. FORENSE D'INGRESSO. Come entra DAVVERO un'orbita caotica? All'anchor t_on (onset del
#      motore, convenzione alpha1_engine.c) si misura il GERME REALE: le prime-letture dei
#      20 periodi successivi, coi colori al tempo t_on:
#        - massa nera ambientale (neri pre-esistenti consumati dalla highway neonata),
#        - profondita' d'interfaccia (ultimo periodo che legge un nero ambientale),
#        - frazione di territorio MAI visitato per periodo (la highway punta nel fresco?),
#        - geometria: f = Cheb(posa)/R_visitato (nasce al bordo?), allineamento drift-radiale.
#   2. KILL-GATE §79.1. Per il Lemma del Replay-Lock (§87a) il verdetto "onset entro l'orizzonte"
#      da un anchor qualunque e' funzione ESATTA dell'insieme delle prime-letture dall'anchor
#      all'orizzonte (footprint decisivo — sufficiente e word-minimale; il verdetto potrebbe
#      avere un determinante piu' piccolo, ma §59/§78-80 hanno gia' escluso i piccoli).
#      Qui si MISURA il footprint decisivo da anchor a t_on-Delta per Delta = 2, 10, 100, 1000
#      periodi: se il raggio decisivo cresce senza stabilizzare con Delta, il verdetto deep->W0
#      NON e' un programma a footprint limitato: il kill-gate chiude come atteso (§79.6.1).
#
# GATE (esatti, per orbita): onset ricalcolato == onset dell'header di dumps_all.txt, 24/24.
# TRIPWIRE (per anchor): la sotto-corsa dallo snapshot deve riprodurre ESATTAMENTE le svolte
# della corsa principale (qualunque divergenza = bug di snapshot/replay = ROSSO).
#
# Convenzioni: alpha1_engine.c via onset_cone_lock (§87a); semi da parse_dumps/build_seed.
# Uscita: alpha1/onset_forensics_summary.json
import sys, os, json, time, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA
from onset_cone_lock import DX, DY, P, onset_verified, cheb

DELTAS = (2 * P, 10 * P, 100 * P, 1000 * P)
KCERT = 20                      # periodi post-onset del germe reale
HORIZ_TAIL = 2 * P              # orizzonte del verdetto: t_on + 2 periodi

def run_to_onset(seed, chk=20000, max_steps=1_500_000):
    grid = {}; x = y = 0; h = 0
    turns = bytearray()
    t = 0
    while t < max_steps:
        c = (x, y)
        color = grid[c] if c in grid else (1 if c in seed else 0)
        if color == 0:
            h = (h + 1) & 3; grid[c] = 1; turns.append(1)
        else:
            h = (h + 3) & 3; grid[c] = 0; turns.append(0)
        x += DX[h]; y += DY[h]
        t += 1
        if t >= 2600 and (t % chk) == 0:
            o = onset_verified(turns, t)
            if o >= 0:
                return turns, t, o
    return turns, t, onset_verified(turns, t)

def replay_with_snapshots(seed, turns_ref, t_on, anchors):
    """Replay deterministico; cattura (grid copia, posa, visitati copia a t_on) agli anchor.
    Tripwire: le svolte replay devono coincidere con turns_ref."""
    grid = {}; x = y = 0; h = 0
    snaps = {}
    vis_at_on = None
    t_max = max(anchors) if anchors else 0
    t_max = max(t_max, t_on)
    for t in range(t_max + 1):
        if t in anchors or t == t_on:
            snaps[t] = (dict(grid), (x, y, h))
            if t == t_on:
                vis_at_on = set(grid)
        c = (x, y)
        color = grid[c] if c in grid else (1 if c in seed else 0)
        b = 1 if color == 0 else 0
        assert b == turns_ref[t], f"replay diverge a t={t}"
        if color == 0:
            h = (h + 1) & 3; grid[c] = 1
        else:
            h = (h + 3) & 3; grid[c] = 0
        x += DX[h]; y += DY[h]
    return snaps, vis_at_on

def subrun_footprint(seed, snap, n_steps, turns_ref, t0):
    """Sotto-corsa dallo snapshot: footprint prime-letture (col colore all'anchor).
    Tripwire: svolte == turns_ref[t0:t0+n_steps]."""
    grid0, (x, y, h) = snap
    grid = dict(grid0)
    seen = {}
    for i in range(n_steps):
        c = (x, y)
        color = grid[c] if c in grid else (1 if c in seed else 0)
        if c not in seen:
            seen[c] = color
        b = 1 if color == 0 else 0
        assert b == turns_ref[t0 + i], f"sotto-corsa diverge a offset {i}"
        if color == 0:
            h = (h + 1) & 3; grid[c] = 1
        else:
            h = (h + 3) & 3; grid[c] = 0
        x += DX[h]; y += DY[h]
    return seen

def main():
    t_start = time.time()
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    out = {"convention": "alpha1_engine.c; anchor = onset dell'header; "
                         "footprint decisivo = prime-letture anchor->t_on+2P (Replay-Lock §87a)",
           "deltas_periods": [d // P for d in DELTAS], "orbits": []}
    gate_all = True
    for od in dumps:
        t0 = time.time()
        seed, side, dens = build_seed(od.rngstate, 5, 25)
        turns, n, onset = run_to_onset(seed)
        gate = (onset == od.onset_header)
        gate_all = gate_all and gate
        assert gate, f"orbita {od.index}: onset {onset} != header {od.onset_header}"
        anchors = {onset - d for d in DELTAS if onset - d >= 0}
        snaps, vis_on = replay_with_snapshots(seed, turns, onset, anchors)

        # --- kill-gate: footprint decisivo per Delta ---
        dec = []
        for d in sorted(DELTAS):
            a = onset - d
            if a < 0:
                continue
            hor = d + HORIZ_TAIL
            seen = subrun_footprint(seed, snaps[a], hor, turns, a)
            ax, ay, ah = snaps[a][1]
            rad = max(max(abs(cx - ax), abs(cy - ay)) for (cx, cy) in seen)
            nb = sum(1 for v in seen.values() if v == 1)
            dec.append({"delta_periods": d // P, "footprint": len(seen),
                        "radius": rad, "blacks": nb})

        # --- forense d'ingresso: germe reale a t_on ---
        grid_on, pose_on = snaps[onset]
        gx, gy, gh = pose_on
        grid = dict(grid_on)
        x, y, h = gx, gy, gh
        seen = set()
        per_env_black = [0] * KCERT
        per_fresh = [0] * KCERT
        per_new = [0] * KCERT
        env_black_cells = []
        for i in range(KCERT * P):
            c = (x, y)
            color = grid[c] if c in grid else (1 if c in seed else 0)
            if c not in seen:
                seen.add(c)
                p = i // P
                per_new[p] += 1
                if color == 1:
                    per_env_black[p] += 1
                    env_black_cells.append(c)
                if c not in vis_on and c not in seed:
                    per_fresh[p] += 1
            b = 1 if color == 0 else 0
            assert b == turns[onset + i] if onset + i < len(turns) else True
            if color == 0:
                h = (h + 1) & 3; grid[c] = 1
            else:
                h = (h + 3) & 3; grid[c] = 0
            x += DX[h]; y += DY[h]
        iface_depth = max((p for p in range(KCERT) if per_env_black[p] > 0), default=-1)
        germ_mass = sum(per_env_black)
        germ_rad = max((max(abs(cx - gx), abs(cy - gy)) for (cx, cy) in env_black_cells),
                       default=0)

        # geometria: dove nasce?
        r_vis = max(cheb(c) for c in vis_on)
        r_ant = max(abs(gx), abs(gy))
        # drift reale del primo periodo post-onset
        hh = gh; dx = dy = 0
        for s in range(onset, onset + P):
            hh = (hh + 1) & 3 if turns[s] else (hh + 3) & 3
            dx += DX[hh]; dy += DY[hh]
        outward = (dx * gx + dy * gy)          # >0 = verso l'esterno
        last8 = "".join("R" if turns[onset - 8 + i] else "L" for i in range(8))

        row = {
            "orbit": od.index, "onset": onset, "gate_onset": gate,
            "decisive": dec,
            "germ_env_blacks_20p": germ_mass, "iface_depth_periods": iface_depth + 1,
            "germ_black_radius": germ_rad,
            "per_period_env_black": per_env_black,
            "fresh_frac_p1": round(per_fresh[0] / per_new[0], 3),
            "fresh_frac_p2_20": round(sum(per_fresh[1:]) / max(1, sum(per_new[1:])), 3),
            "r_ant": r_ant, "r_vis": r_vis, "f_border": round(r_ant / r_vis, 3),
            "drift": [dx, dy], "outward": int(outward), "last8_pre_onset": last8,
            "elapsed_s": round(time.time() - t0, 1),
        }
        out["orbits"].append(row)
        print(f"[orb {od.index:2d}] onset {onset} gate {'OK' if gate else 'ROSSO'} | "
              f"germe {germ_mass}N r{germ_rad} iface {row['iface_depth_periods']}p | "
              f"fresh p1 {row['fresh_frac_p1']} p2+ {row['fresh_frac_p2_20']} | "
              f"f_bordo {row['f_border']} out {'SI' if outward > 0 else 'no'} | "
              f"R_dec {[d['radius'] for d in dec]} | {row['elapsed_s']}s", flush=True)

    print(f"GATE onset 24/24: {'OK' if gate_all else 'ROSSO'}")
    assert gate_all

    # pooled
    rows = out["orbits"]
    def med(k): return st.median(r[k] for r in rows)
    pool = {
        "germ_mass_min": min(r["germ_env_blacks_20p"] for r in rows),
        "germ_mass_med": med("germ_env_blacks_20p"),
        "germ_mass_max": max(r["germ_env_blacks_20p"] for r in rows),
        "iface_med": med("iface_depth_periods"),
        "iface_max": max(r["iface_depth_periods"] for r in rows),
        "germ_radius_med": med("germ_black_radius"),
        "germ_radius_max": max(r["germ_black_radius"] for r in rows),
        "f_border_min": min(r["f_border"] for r in rows),
        "f_border_med": med("f_border"),
        "fresh_p2_20_min": min(r["fresh_frac_p2_20"] for r in rows),
        "outward_count": sum(1 for r in rows if r["outward"] > 0),
        "decisive_radius_by_delta": {},
    }
    for j, dp in enumerate(sorted(d // P for d in DELTAS)):
        vals = [r["decisive"][j]["radius"] for r in rows]
        pool["decisive_radius_by_delta"][str(dp)] = {
            "min": min(vals), "med": st.median(vals), "max": max(vals)}
    out["pooled"] = pool
    out["elapsed_s"] = round(time.time() - t_start, 1)
    print("POOLED:", json.dumps(pool, indent=1))
    path = str(ALPHA / "onset_forensics_summary.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {path} in {out['elapsed_s']} s")

if __name__ == "__main__":
    main()
