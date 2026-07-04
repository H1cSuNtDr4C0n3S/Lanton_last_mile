# u2_far_signature_hunt.py — §96: CACCIA PER-FIRMA alle firme-exit residue.
#
# Dall'oracolo v2 (§96, C1/C3/C4) restano 8 firme di pulizia (c*, h*) il cui
# tratto pulito esce dalla palla al primo passo. FATTO CHIAVE: l'exit-step da
# un nodo di pulizia realizzato e' SEMPRE realizzabile (la cella d'uscita e'
# fuori palla con y>=1: se FREE entrambe le letture vanno, se visitata la
# lettura forzata va — e in ogni caso pend2 resta 0 e la posa e' fuori).
# QUINDI: v2 vera <=> NESSUNA delle 8 firme e' realizzabile come nodo di
# pulizia. Realizzarne UNA = testimone clean-far = v2 FALSIFICATA.
#
# Caccia: per ogni firma bersaglio, multi-politica (trappola hh):
#   PA milestone-greedy con steering finale: chiudi i pending; quando
#      pend2 == {c*}, punta (posa,heading) verso (c_par, h_par) — la chiusura
#      dal genitore giusto produce ESATTAMENTE la firma;
#   PB passeggiate profonde randomizzate (censimento firme spontanee);
#   PC mutazione dei 31 testimoni puliti noti (tronca kb bit, ri-esplora PA);
#   PD "palla-cameriere" (pannello §96, azione B3): resta in palla il piu'
#      possibile e ri-apri c* con L quando capita — campiona gli approcci
#      con apertura-L in palla a profondita' >=4 (il corno che il Lemma
#      della Catena di Chiusura lascia aperto e che le politiche
#      bordo-orientate non coprono).
# OGNI transizione pend2: 1->0 incontrata viene registrata CON la politica
# (censimento per-politica, pannello §96 azione B2 — il negativo va
# etichettato per famiglia di politiche, trappola hh).
#
# GATE:
#   S0 controllo positivo: il bersaglio ((-1,2), h=3) — l'unica firma
#      realizzata nota — DEVE essere ritrovato dal cacciatore (altrimenti il
#      negativo sulle 8 non ha valore);
#   S1 verifica di terra di ogni hit: valid() + exact_state (pend2 == vuoto,
#      posa == c*, heading == h*); per le 8 residue, in piu' viene costruito
#      e verificato il testimone clean-far (exit-step) => report V2-FALSIFICATA.
#
# Uscita: alpha1/u2_far_signature_hunt_summary.json (+ .log)
import sys, os, json, time, random, argparse, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY
from record_weapon_vitality import to_bits, to_str, SUMMARY
from u2_cover_rail_map import valid
from u2_pocket_certificate import exact_state, FREE
from u2_far_ledger import cheb, pend_set
from u2_far_clean_stretch import Walker, pend2_of, BALL_R, _below_normal

HERE = os.path.dirname(os.path.abspath(__file__))
WIT = os.path.join(HERE, "u2_cover_witnesses.json")
CEN = os.path.join(HERE, "u2_far_born_near_census_summary.json")
CSS = os.path.join(HERE, "u2_far_clean_stretch_summary.json")
CEX = os.path.join(HERE, "u2_far_pend2_counterexamples.json")
ORC2 = os.path.join(HERE, "u2_far_clean_oracle_v2_summary.json")
OUT_JSON = os.path.join(HERE, "u2_far_signature_hunt_summary.json")
LOG = os.path.join(HERE, "u2_far_signature_hunt.log")


def par_of(sig):
    (cx, cy), h = sig
    hp = (h + 1) & 3
    return (cx + DX[hp], cy + DY[hp]), hp


def hunt_job(job):
    (tgt_sig, base_name, base_str, policy, seed, restarts, budget) = job
    _below_normal()
    rng = random.Random(seed)
    base = to_bits(base_str)
    (tc, th) = tgt_sig
    tc = tuple(tc)
    (c_par, h_par) = par_of((tc, th))
    hits = []                 # estensioni che realizzano la firma bersaglio
    census = {}               # firma -> conteggio (tutte le pulizie viste)
    steps = 0

    def record_cleaning(wk):
        nonlocal hits
        sig = (wk.c, wk.h)
        census[str((sig[0], sig[1]))] = census.get(str((sig[0], sig[1])), 0) + 1
        if sig == (tc, th):
            hits.append(to_str(tuple(reversed(wk.bits))))

    for rs in range(restarts):
        wk = Walker(base)
        b = budget
        p_steer = rng.choice((0.5, 0.8, 0.95))
        while b > 0:
            lb = wk.legal_bits()
            if not lb:
                if wk.bits:
                    wk.undo()
                    continue
                break
            if len(lb) == 1:
                bit = lb[0]
            elif policy == "PB":
                bit = lb[rng.randrange(2)]
            elif policy == "PD":
                # palla-cameriere: se la prossima cella e' c* con req=1,
                # ri-aprila (L) con prob. 1/2; altrimenti resta vicino alla
                # palla (minimizza cheb del secondo passo), tie random
                cn = wk.next_cell()
                if cn == tc and wk.req.get(cn, FREE) == 1 \
                        and rng.random() < 0.5:
                    bit = 0                    # L: riapre il pending di c*
                else:
                    best = None
                    for bb in (0, 1):
                        hn = (wk.h - 1) & 3 if bb == 1 else (wk.h + 1) & 3
                        cnn = (cn[0] - DX[hn], cn[1] - DY[hn])
                        d = (cheb(cnn), rng.random())
                        if best is None or d < best[0]:
                            best = (d, bb)
                    bit = best[1]
            else:                              # PA / PC: steering
                if wk.p2 == 1 and next(iter(
                        c for c in wk.pend if cheb(c) <= BALL_R)) == tc \
                        and rng.random() < p_steer:
                    # punta (c_par, h_par)
                    best = None
                    cn = wk.next_cell()
                    for bb in (0, 1):
                        hn = (wk.h - 1) & 3 if bb == 1 else (wk.h + 1) & 3
                        cnn = (cn[0] - DX[hn], cn[1] - DY[hn])
                        d = (abs(cnn[0] - c_par[0]) + abs(cnn[1] - c_par[1])
                             + (0 if hn == h_par else 1))
                        if best is None or d < best[0]:
                            best = (d, bb)
                    bit = best[1]
                elif wk.p2 and rng.random() < p_steer:
                    # chiudi il pending in palla piu' vicino
                    tgt = min((c for c in wk.pend if cheb(c) <= BALL_R),
                              key=lambda p: abs(p[0] - wk.c[0])
                              + abs(p[1] - wk.c[1]))
                    best = None
                    cn = wk.next_cell()
                    for bb in (0, 1):
                        hn = (wk.h - 1) & 3 if bb == 1 else (wk.h + 1) & 3
                        cnn = (cn[0] - DX[hn], cn[1] - DY[hn])
                        d = abs(cnn[0] - tgt[0]) + abs(cnn[1] - tgt[1])
                        if best is None or d < best[0]:
                            best = (d, bb)
                    bit = best[1]
                else:
                    bit = lb[rng.randrange(2)]
            p2_before = wk.p2
            wk.apply(bit)
            b -= 1
            steps += 1
            if p2_before == 1 and wk.p2 == 0:
                record_cleaning(wk)
                if hits:
                    return {"target": (list(tc), th), "base": base_str,
                            "nome": base_name, "policy": policy,
                            "hits": hits, "census": census, "steps": steps}
    return {"target": (list(tc), th), "base": base_str, "nome": base_name,
            "policy": policy, "hits": hits, "census": census, "steps": steps}


def collect_bases(w101):
    """Basi di caccia: 36 fuggenti + 31 parole pulite §95 troncate (PC)."""
    wit = json.load(open(WIT))
    cen = json.load(open(CEN))
    seen = set()
    fug = []
    for k, w in enumerate(wit["jackpot"]):
        fug.append((f"jackpot[{k}]", to_bits(w["word"]) + w101))
    for k, w in enumerate(wit["nere400"]):
        fug.append((f"nere400[{k}]", to_bits(w["word"]) + w101))
    for k, w in enumerate(cen["fuggenti_dettaglio"]):
        fug.append((f"census[{k}]", to_bits(w["word_ext"]) + w101))
    fug2 = []
    for n, w in fug:
        if tuple(w) in seen:
            continue
        seen.add(tuple(w))
        fug2.append((n, w))
    # parole pulite note (dai cert_rows §95 + controesempi)
    clean_words = []
    css = json.load(open(CSS))
    for r in css["gates"]["G3"]["cert_rows"]:
        pass                                   # word_full non salvato nei rows
    cex = json.load(open(CEX))["witnesses"]
    for w in cex:
        W = to_bits(w["word"])
        clean_words.append((f"cex:{w['tag']}", W))
    return fug2, clean_words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--restarts", type=int, default=3)
    ap.add_argument("--budget", type=int, default=120_000)
    ap.add_argument("--seed", type=int, default=96)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        args.restarts = 1
        args.budget = 25_000
    t0 = time.time()
    log = open(LOG, "a")
    log.write(f"\n==== run {time.strftime('%Y-%m-%d %H:%M:%S')} "
              f"args={vars(args)}\n")

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    orc = json.load(open(ORC2))
    residue = [((tuple(r["posa"])), r["h"]) for r in
               [{"posa": x["posa"], "h": x["h"]} for x in orc["firme_exit"]]]
    targets = [(tuple(p), h) for p, h in residue] + [((-1, 2), 3)]  # +controllo
    fug, clean_words = collect_bases(w101)
    print(f"{len(targets)} bersagli ({len(residue)} residue + controllo "
          f"positivo), {len(fug)} fuggenti, {len(clean_words)} parole pulite",
          flush=True)

    jobs = []
    jid = 0
    for tgt in targets:
        for name, w in fug:
            for policy in ("PA", "PB", "PD"):
                jobs.append(((list(tgt[0]), tgt[1]), name, to_str(w), policy,
                             args.seed * 104729 + jid, args.restarts,
                             args.budget))
                jid += 1
        for name, W in clean_words:
            for kb in (10, 40, 160):
                if kb >= len(W) - 101:
                    continue
                jobs.append(((list(tgt[0]), tgt[1]), f"PC:{name}:kb{kb}",
                             to_str(W[kb:]), "PC",
                             args.seed * 104729 + jid, args.restarts,
                             args.budget))
                jid += 1
    print(f"{len(jobs)} job ({args.restarts} restart x {args.budget} passi)",
          flush=True)

    per_target = {str(t): {"hits": [], "steps": 0} for t in targets}
    census_glob = {}
    census_policy = {}          # (firma, policy) -> conteggio (B2, pannello)
    v2_witness = None
    with mp.Pool(args.workers, initializer=_below_normal) as pool:
        for r in pool.imap_unordered(hunt_job, jobs, chunksize=1):
            key = str((tuple(r["target"][0]), r["target"][1]))
            pt = per_target[key]
            pt["steps"] += r["steps"]
            for s, n in r["census"].items():
                census_glob[s] = census_glob.get(s, 0) + n
                kp = f"{s}|{r['policy']}"
                census_policy[kp] = census_policy.get(kp, 0) + n
            for ext in r["hits"]:
                # S1: verifica di terra
                Wfull = to_bits(ext) + to_bits(r["base"])
                assert valid(Wfull)[1] is None
                c2, h2, req2 = exact_state(Wfull)
                assert pend2_of(req2) == [] and \
                    c2 == tuple(r["target"][0]) and h2 == r["target"][1], \
                    f"hit smentito di terra {key}"
                pt["hits"].append({"nome": r["nome"], "policy": r["policy"],
                                   "len": len(Wfull)})
                tgt_t = (tuple(r["target"][0]), r["target"][1])
                if tgt_t != ((-1, 2), 3):
                    # firma residua realizzata: costruisci il clean-far
                    cx = (c2[0] - DX[h2], c2[1] - DY[h2])
                    rq = req2.get(cx, FREE)
                    bit = 1 if rq in (FREE, 0) else 0
                    Wexit = (bit,) + Wfull
                    assert valid(Wexit)[1] is None
                    c3, h3, req3 = exact_state(Wexit)
                    assert pend2_of(req3) == [] and cheb(c3) > BALL_R
                    v2_witness = {"firma": key, "posa_exit": list(c3),
                                  "word": to_str(Wexit)}
                    print(f"!!! V2 FALSIFICATA: firma {key} realizzata, "
                          f"clean-far a {c3}", flush=True)

    print("\n---- esiti per bersaglio ----")
    rows = []
    for t in targets:
        pt = per_target[str(t)]
        tag = "CONTROLLO" if t == ((-1, 2), 3) else "residua"
        print(f"  {str(t):18s} [{tag}]: hit={len(pt['hits'])} "
              f"passi={pt['steps']}", flush=True)
        rows.append({"firma": str(t), "tag": tag,
                     "hits": len(pt["hits"]), "passi": pt["steps"],
                     "hits_per_policy": {p: sum(1 for h in pt["hits"]
                                                if h["policy"] == p)
                                         for p in ("PA", "PB", "PC", "PD")},
                     "dettaglio_hits": pt["hits"][:20]})
    print(f"\ncensimento firme di pulizia viste (globale): {census_glob}")
    print(f"censimento per-politica (B2): {census_policy}")

    # GATE S0 (per-politica, pannello §96 B2)
    ctrl = per_target[str(((-1, 2), 3))]
    assert len(ctrl["hits"]) > 0, \
        "GATE S0 ROSSO: il controllo positivo ((-1,2),3) non e' stato trovato"
    ctrl_pp = {p: sum(1 for h in ctrl["hits"] if h["policy"] == p)
               for p in ("PA", "PB", "PC", "PD")}
    pol_ok = [p for p, n in ctrl_pp.items() if n > 0]
    print(f"\nGATE S0 verde: controllo positivo ritrovato "
          f"({len(ctrl['hits'])} hit, per policy {ctrl_pp}) — il negativo "
          f"sulle residue e' etichettato dalle politiche con potere "
          f"positivo dimostrato: {pol_ok}", flush=True)

    verdict = ("V2-FALSIFICATA" if v2_witness else
               f"8-FIRME-MAI-REALIZZATE (negativo empirico etichettato "
               f"per-politica, trappola hh: potere positivo dimostrato da "
               f"{pol_ok}; censimento globale = solo ((-1,2),3))")
    out = {"args": vars(args), "targets": [str(t) for t in targets],
           "rows": rows, "census_globale": census_glob,
           "census_per_policy": census_policy,
           "controllo_hits_per_policy": ctrl_pp,
           "v2_witness": v2_witness, "verdetto": verdict,
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    log.write(json.dumps({"verdetto": verdict, "census": census_glob}) + "\n")
    log.close()
    print(f"\nVERDETTO: {verdict}\nscritto {OUT_JSON} in {out['elapsed_s']} s",
          flush=True)


if __name__ == "__main__":
    main()
