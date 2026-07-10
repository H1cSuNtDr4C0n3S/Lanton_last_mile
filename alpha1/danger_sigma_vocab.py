# danger_sigma_vocab.py — §107c P2: sigma_D sul vocabolario intero.
#
# OGGETTO: sigma_D(w) = quota-shield dei passati validi di profondita' D
# (funzionale word-decidibile, §107b) calcolato su TUTTE le parole del
# censimento F0 (danger_geometry_census.json per_word, 1459+2), non solo
# sulla classe pericolosa <=50. Domanda (roadmap §C punto 2): che quota del
# vocabolario reale dei record e' deduttivamente sicura (sigma=1, rigetto
# garantito a profondita' dichiarata)?
#
# DISCIPLINA:
#   - sigma=1 e' un fatto ESATTO per-parola (enumerazione esaustiva al cap):
#     nessuna soglia (qq). La quota complessiva e' descrittiva.
#   - parole TRONCATE (budget nodi/tempo) = NON-DEFINITE (trappola mm),
#     flag esplicito, mai contate come misurate.
#   - run sharded (§4): questo script e' UN worker; lanciare N processi con
#     --shard 0..N-1 --nshards N. Log append-only con timestamp, output
#     JSONL per shard (riprendibile: le parole gia' scritte vengono saltate).
#   - convenzione (caveat §107b.6): onset_germe misurato DAL RECORD,
#     asse assoluto = og+101.
#
# Uscita: alpha1/sigma_vocab_shard{i}.jsonl (+ .log)
import sys, os, json, time, argparse

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from danger_backward_autopsy import Machine, dfs_census

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.join(HERE, "danger_geometry_census.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard", type=int, required=True)
    ap.add_argument("--nshards", type=int, required=True)
    ap.add_argument("--depth", type=int, default=22)
    ap.add_argument("--budget-per-word", type=int, default=120)
    ap.add_argument("--node-budget", type=int, default=60_000_000)
    args = ap.parse_args()
    out_path = os.path.join(HERE, f"sigma_vocab_shard{args.shard}.jsonl")
    log_path = os.path.join(HERE, f"sigma_vocab_shard{args.shard}.log")

    def log(msg):
        line = f"[{time.strftime('%H:%M:%S')}] {msg}"
        print(line, flush=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    census = json.load(open(CENSUS))["per_word"]
    words = sorted(census.keys())
    mine = [ws for idx, ws in enumerate(words)
            if idx % args.nshards == args.shard]
    done = set()
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                try:
                    done.add(json.loads(line)["word"])
                except Exception:
                    pass
    log(f"shard {args.shard}/{args.nshards}: {len(mine)} parole, "
        f"{len(done)} gia' fatte, depth={args.depth}, "
        f"budget {args.budget_per_word}s/parola")
    t0 = time.time()
    n_ok = n_trunc = n_err = 0
    for k, ws in enumerate(mine):
        if ws in done:
            continue
        rec = {"word": ws, "n_rt": census[ws]["n"],
               "onset_germe": census[ws]["onset_germe"],
               "depth": args.depth}
        try:
            w = tuple(1 if ch == "R" else 0 for ch in ws)
            m = Machine(w)
            stats, cap, nodes, truncated, touch, cell_bits = dfs_census(
                m, args.depth, node_budget=args.node_budget,
                budget_s=args.budget_per_word)
            n_cap = sum(cap.values())
            rec.update({
                "cap": n_cap, "nodi": nodes,
                "shield": cap["shield"], "white_all": cap["white_all"],
                "open": cap["open"],
                "sigma": round(cap["shield"] / max(1, n_cap), 6),
                "sigma_uno_esatto": (not truncated and n_cap > 0 and
                                     cap["shield"] == n_cap),
                "celle_irraggiungibili": sum(
                    1 for b in cell_bits.values() if b[0] + b[1] == 0),
                "non_definito": bool(truncated)})
            if truncated:
                n_trunc += 1
            else:
                n_ok += 1
        except Exception as ex:
            rec.update({"errore": repr(ex), "non_definito": True})
            n_err += 1
        with open(out_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        if (k + 1) % 10 == 0 or k + 1 == len(mine):
            log(f"{k + 1}/{len(mine)} (ok {n_ok}, non-def {n_trunc}, "
                f"err {n_err}, {time.time() - t0:.0f} s)")
    log(f"FINITO: ok {n_ok}, non-definite {n_trunc}, errori {n_err} in "
        f"{time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
