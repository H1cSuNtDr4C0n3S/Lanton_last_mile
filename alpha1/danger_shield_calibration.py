# danger_shield_calibration.py — §107d F3: calibrazione sigma_D vs scudo di
# griglia (preregistrata a §107c.5).
#
# DOMANDA: la misura uniforme sui passati enumerati (sigma_D, P2 §107c)
# predice la ricchezza-scudo REALE di griglia alle presentazioni canoniche?
# Se non correla, il verdetto "lock non estremi" §107b perde la base di
# misura (angolo cieco del round-1 §107c, forma di griglia del round-2).
#
# OSSERVABILE DI GRIGLIA (per presentazione = record canonico): colori reali
# delle celle di R_T(w) al tempo del record (frame ancora = assoluto
# traslato, heading 0 assertato da run_collect_records):
#   nb = #nere in R_T; OR = (nb >= 1).
# UNITA' PRIMARIA: parola unica (i record consecutivi condividono scudo e
# colpevoli — lezione episodi §100); per-record riportato come dato.
#
# GATES (bidirezionali, deduttivi dalla dicotomia §101 + corollario OR §107a):
#   GF0: 1639 record canonici, istogramma |R_T| bit-identico a
#        danger_class_sizes.json (stessa selezione di F0 §107b).
#   GF1: replay interno con verifica bit-per-bit dei turns (il mio replay
#        rilegge la griglia e DEVE riprodurre ogni svolta di
#        run_collect_records — validazione per-passo del mio stato griglia).
#   GF2 (controllo positivo KILL): i 2 lock reali (fuori canonico) devono
#        avere nb == 0 (OR=0) al loro record — il lock e' successo.
#   GF3 (deduttivo): OR == 1 su TUTTI i 1639 canonici (T ⟺ OR=1: se un
#        canonico avesse OR=0 il ride sarebbe garantito ⇒ non-T ⇒
#        contraddizione con §101). Un fallimento = bug o falsificazione.
# Nessuna soglia enunciata (qq): bande dichiarate, distribuzioni = dato,
# aspettativa preregistrata = sigma correla ordinalmente con lo scudo.
#
# Convenzione (caveat §107b.6): onset_germe dal record, asse assoluto og+101.
# Uscita: alpha1/danger_shield_calibration.json
import sys, os, json, time

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA
from record_word_census import run_collect_records
from record_weapon_hunt import eval_word
from speed_limit_theorem import transient_readset_from_germ

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "danger_shield_calibration.json")
HUNT = os.path.join(HERE, "record_divergence_hunt_summary.json")
DANGER_HIST = os.path.join(HERE, "danger_class_sizes.json")
PERWORD = os.path.join(HERE, "sigma_vocab_perword.jsonl")
K = 101


def word_str(w):
    return "".join("R" if b else "L" for b in w)


def rt_cache_get(w, cache):
    ws = word_str(w)
    if ws not in cache:
        r = eval_word(w)
        assert r is not None
        og = r[1]
        cache[ws] = [c for (c, tf) in transient_readset_from_germ(w, og)]
    return ws, cache[ws]


def replay_measure(seed, turns, targets):
    """Replay forward con verifica bit-per-bit (GF1). targets: t -> celle
    assolute; ritorna t -> #nere al tempo t (stato griglia PRIMA del passo t)."""
    grid = {}
    x = y = 0
    h = 0
    res = {}
    T = max(targets) + 1 if targets else 0
    for t in range(T):
        if t in targets:
            nb = 0
            for c in targets[t]:
                col = grid[c] if c in grid else (1 if c in seed else 0)
                nb += col
            res[t] = nb
        c = (x, y)
        color = grid[c] if c in grid else (1 if c in seed else 0)
        b = 1 if color == 0 else 0
        assert b == turns[t], f"GF1 FALLITO: replay diverge a t={t}"
        if color == 0:
            h = (h + 1) & 3
            grid[c] = 1
        else:
            h = (h + 3) & 3
            grid[c] = 0
        x += (0, 1, 0, -1)[h]
        y += (-1, 0, 1, 0)[h]
    return res


def main():
    t0 = time.time()
    sigma = {}
    with open(PERWORD, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            sigma[r["word"]] = r
    rt_cache = {}
    per_record = []
    hist = {}
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    for od in dumps:
        seed, _, _ = build_seed(od.rngstate, 5, 25)
        y_seed_min = min(cy for (_, cy) in seed)
        turns, t_on, records = run_collect_records(seed)
        assert t_on == od.onset_header
        recs = [(t, x, y) for (t, x, y) in records
                if t < t_on and y < y_seed_min and t >= K]
        targets = {}
        meta = {}
        for (t, rx, ry) in recs:
            w = tuple(turns[t - K:t])
            ws, rt = rt_cache_get(w, rt_cache)
            targets[t] = [(rx + cx, ry + cy) for (cx, cy) in rt]
            meta[t] = (ws, len(rt))
        nb_at = replay_measure(seed, turns, targets)
        for t in sorted(targets):
            ws, n_rt = meta[t]
            hist[n_rt] = hist.get(n_rt, 0) + 1
            per_record.append({"orb": od.index, "t": t, "word": ws,
                               "n_rt": n_rt, "nb": nb_at[t]})
        print(f"[orb {od.index:2d}] record {len(recs)}, parole cumul. "
              f"{len(rt_cache)}", flush=True)

    # GF0
    ref = {int(k): v for k, v in json.load(
        open(DANGER_HIST))["per_record_sizes_hist"].items()}
    assert ref == hist, "GF0 FALLITO: istogramma |R_T| diverso da §107a"
    assert len(per_record) == sum(hist.values())
    print(f"GF0 OK: {len(per_record)} record, istogramma == §107a", flush=True)

    # GF3 deduttivo: OR=1 su tutti i canonici
    or0 = [r for r in per_record if r["nb"] == 0]
    print(f"GF3 (T ⟺ OR=1): violazioni {len(or0)}/{len(per_record)}",
          flush=True)
    assert not or0, f"GF3 FALLITO: {or0[:3]}"

    # GF2: i 2 lock (controllo positivo KILL)
    hunt = json.load(open(HUNT))
    gf2 = []
    for i, e in enumerate([hunt["F2"][0], hunt["F2"][1]]):
        rngs, t = int(e["rngstate"]), int(e["t"])
        seed, _, _ = build_seed(rngs, 5, 25)
        turns, t_on, records = run_collect_records(seed)
        rec = next((r for r in records if r[0] == t), None)
        assert rec is not None, f"lock t={t} non e' un record"
        _, rx, ry = rec
        w = tuple(turns[t - K:t])
        ws, rt = rt_cache_get(w, rt_cache)
        nb = replay_measure(seed, turns,
                            {t: [(rx + cx, ry + cy) for (cx, cy) in rt]})[t]
        gf2.append({"label": f"LOCK{'AB'[i]}", "n_rt": len(rt), "nb": nb})
        print(f"GF2 LOCK{'AB'[i]}: nb={nb}/{len(rt)} "
              f"{'OK (OR=0)' if nb == 0 else 'FALLITO'}", flush=True)
        assert nb == 0, "GF2 FALLITO: lock con scudo?!"

    # ---- calibrazione per-parola ----
    words = {}
    for r in per_record:
        d = words.setdefault(r["word"], {"n_rt": r["n_rt"], "pres": 0,
                                         "nb_sum": 0, "nb_min": 10 ** 9})
        d["pres"] += 1
        d["nb_sum"] += r["nb"]
        d["nb_min"] = min(d["nb_min"], r["nb"])
    for ws, d in words.items():
        s = sigma.get(ws)
        assert s is not None, f"parola fuori P2: {ws[:16]}"
        d["sigma"] = s["sigma"]
        d["ricchezza"] = d["nb_sum"] / d["pres"] / d["n_rt"]
    bands = [("sigma=1", lambda s: s == 1.0),
             ("[0.9,1)", lambda s: 0.9 <= s < 1.0),
             ("[0.5,0.9)", lambda s: 0.5 <= s < 0.9),
             ("[0.1,0.5)", lambda s: 0.1 <= s < 0.5),
             ("[0.01,0.1)", lambda s: 0.01 <= s < 0.1),
             ("<0.01", lambda s: s < 0.01)]
    out_bands = []
    print("\nbanda sigma | parole | pres | ricchezza med (nb/n_rt) | "
          "nb_min med", flush=True)
    for lab, pred in bands:
        sel = [d for d in words.values() if pred(d["sigma"])]
        if not sel:
            continue
        ric = sorted(d["ricchezza"] for d in sel)
        nbm = sorted(d["nb_min"] for d in sel)
        row = {"banda": lab, "parole": len(sel),
               "presentazioni": sum(d["pres"] for d in sel),
               "ricchezza_med": round(ric[len(ric) // 2], 4),
               "nb_min_med": nbm[len(nbm) // 2]}
        out_bands.append(row)
        print(f"{lab:>11} | {len(sel):5d} | {row['presentazioni']:5d} | "
              f"{row['ricchezza_med']:.4f} | {row['nb_min_med']}", flush=True)

    out = {"gates": {"GF0": True, "GF1": "bit-per-bit nel replay",
                     "GF2": gf2, "GF3_violazioni": 0},
           "n_record": len(per_record), "n_parole": len(words),
           "bande": out_bands,
           "per_word": {ws: {"n_rt": d["n_rt"], "sigma": d["sigma"],
                             "pres": d["pres"],
                             "ricchezza": round(d["ricchezza"], 4),
                             "nb_min": d["nb_min"]}
                        for ws, d in words.items()},
           "convenzione": "nb = #nere in R_T al tempo del record (prima del "
                          "passo t); unita' primaria = parola unica; og dal "
                          "record (asse assoluto og+101)",
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
