# record_ancient_block_tree.py — §89d: il Blocco Antico sull'ALBERO INTERO dei passati.
#
# §89c ha dimostrato il Blocco Antico lungo la famiglia certificata. Qui la domanda
# giusta e' piu' forte: il passato REALE di un'orbita che presenta w101 a un record e'
# una QUALUNQUE estensione all'indietro realizzabile e record-compatibile (footprint in
# {y>=1}) — l'onset del germe NON e' richiesto a un passato (albero piu' grande del muro
# §88 Test B, che filtrava anche per onset). Se NESSUNA estensione valida visita (1,1)
# fino a profondita' D, allora a OGNI record y-min con suffisso w101, di QUALSIASI
# orbita, la cella (1,1) non e' stata visitata negli ultimi 101+D passi: eta' > 101+D.
# (La posizione aggiunta dal prepend a profondita' j e' la posa dell'orbita a t-101-j;
# le posizioni t-101..t-1 sono fissate da w101, che gia' evita (1,1).)
#
# Dicotomia per il §90 (discesa ben fondata): a ogni record o il passato evita (1,1)
# per sempre (=> il nero viene dal seme iniziale, e i record B-T escono da ogni seme
# finito), o il passato visita (1,1) a qualche profondita' j (=> il colore di (1,1) e'
# word-determinato dalla parola estesa: il verdetto passa alla parola piu' lunga).
# Questo script misura il primo corno: conta, per profondita', le estensioni valide e
# quante visitano (1,1). Zero visite fino a D = teorema a profondita' finita.
#
# Costo: solo virtual_walk + check footprint (niente simulazioni di germe).
# Uscita: alpha1/record_ancient_block_tree_summary.json
import sys, os, json, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kwindow_spoiler_census import virtual_walk, to_anchor_frame
from record_weapon_vitality import to_bits, SUMMARY

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "record_ancient_block_tree_summary.json")
TARGET_CELL = (1, 1)


def valid_and_hits(word):
    """(valida, visita_target): realizzabile + footprint in {y>=1}; target nel footprint?"""
    vg, pose = virtual_walk(word)
    if vg is None:
        return False, False
    anchor = to_anchor_frame(vg, pose)
    if any(cy < 1 for (_, cy) in anchor):
        return False, False
    return True, TARGET_CELL in anchor


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--depth", type=int, default=40)
    ap.add_argument("--nodes", type=int, default=3_000_000)
    ap.add_argument("--budget-s", type=int, default=900)
    args = ap.parse_args()
    t0 = time.time()

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    ok, hit = valid_and_hits(w101)
    assert ok and not hit, "gate w101 fallito"

    level = [()]
    counts = {}
    hits = {}
    hit_words = []
    nodes = 0
    truncated = None
    for dep in range(1, args.depth + 1):
        nxt = []
        nhit = 0
        for pref in level:
            for bit in (0, 1):
                p2 = (bit,) + pref
                nodes += 1
                ok, hit = valid_and_hits(p2 + w101)
                if not ok:
                    continue
                if hit:
                    nhit += 1
                    if len(hit_words) < 10:
                        hit_words.append("".join("R" if b else "L" for b in p2))
                    continue          # ramo passato al secondo corno della dicotomia
                nxt.append(p2)
        counts[dep] = len(nxt) + nhit
        hits[dep] = nhit
        level = nxt
        el = time.time() - t0
        print(f"prof. {dep:3d}: valide {counts[dep]:8d} (visitano (1,1): {nhit}) "
              f"[{nodes} nodi, {el:.0f}s]", flush=True)
        if not level:
            break
        if nodes >= args.nodes or el > args.budget_s:
            truncated = dep
            print(f"TRONCATO a prof. {dep} (budget)", flush=True)
            break

    tot_hits = sum(hits.values())
    dmax = max(counts) if counts else 0
    if tot_hits == 0 and truncated is None and dmax == args.depth:
        print(f"\nTEOREMA (prof. finita {args.depth}): NESSUN passato record-compatibile "
              f"di w101 visita (1,1) entro {args.depth} prepend => a ogni record y-min "
              f"con suffisso w101, eta'((1,1)) > {101 + args.depth}.", flush=True)
    elif tot_hits > 0:
        print(f"\nDICOTOMIA ATTIVA: {tot_hits} estensioni visitano (1,1) "
              f"(prime: {hit_words}) — quei rami passano al verdetto della parola "
              f"estesa (secondo corno).", flush=True)

    out = {"depth": args.depth, "counts": counts, "hits": hits,
           "hit_words_oldest_first": hit_words, "truncated_at": truncated,
           "nodes": nodes, "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
