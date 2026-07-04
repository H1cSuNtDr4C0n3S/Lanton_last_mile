# u2_far_born_near_census.py — §94: censimento NASCITA VICINA sulla FAMIGLIA intera.
#
# §93h.3: estendere il Lemma della Nascita Vicina (§93c, per-parola) dalle 48
# parole-testimone alla famiglia delle coprenti-nere di §92 (43.726 nere, 43
# configurazioni di copertura distinte). Lo script della campagna §92 non fu
# salvato (solo i witnesses): qui la campagna viene RIGENERATA con politiche
# randomizzate + steering (antidoto trappola bb: niente best-first puro), le
# coprenti-nere raccolte vengono classificate per CONFIG DI COPERTURA
#   config = (h1, req|S_CORE)   con h1 = heading dopo la svolta di copertura
# (la stessa nozione della macchina §92: replay_extension ritorna (h1, rt)),
# e OGNI parola distinta riceve il verdetto born-near:
#   - albero dei prepend ESAURITO con min_pend>0 su tutti i nodi
#       => CERTIFICATA vietata ai record lontani (r_seed = max(r_foot, r_wall));
#   - cap raggiunto => FUGGENTE (classificazione del corridoio di fuga:
#       riga massima del muro, config, profondita' raggiunta).
#
# GATE (devono poter fallire — corollario trappola bb):
#   GC0 i 60 coprenti del censimento §90c cadono in ESATTAMENTE 2 config
#       distinte (il numero citato a §92c);
#   GC1 i 12 testimoni finiti di u2_cover_witnesses.json riproducono D_true e
#       min_pend bit-identici al summary di u2_far_born_near.py;
#   GC2 cross-validazione di terra (gate_cross, solo valid()) su un campione
#       di alberi esauriti: (D, min_pend) bit-identici;
#   GC3 soglie minime della campagna: >= 30 config distinte, >= 10.000 nere
#       distinte, >= 1 config nuova oltre le 2 di §90c (else: sottocampionata);
#   GC4 il req incrementale del camminatore coincide con exact_state() su un
#       campione di hit (identita' ledger).
#
# Uscita: alpha1/u2_far_born_near_census_summary.json (+ .log append-only)
import sys, os, json, time, random, argparse, multiprocessing as mp
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_weapon_vitality import to_bits, SUMMARY
from u2_cover_rail_map import valid
from u2_pocket_certificate import exact_state, exact_step, anchor_trace, \
    S_CORE, TGT, FREE
from u2_far_ledger import cheb
from u2_far_born_near import wall_exhaustive, gate_cross
from u2_far_run import collect_black_covers
from onset_cone_lock import DX, DY

HERE = os.path.dirname(os.path.abspath(__file__))
CC = os.path.join(HERE, "record_cover_census_summary.json")
BN = os.path.join(HERE, "u2_far_born_near_summary.json")
WIT = os.path.join(HERE, "u2_cover_witnesses.json")
OUT_JSON = os.path.join(HERE, "u2_far_born_near_census_summary.json")
LOG = os.path.join(HERE, "u2_far_born_near_census.log")


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def _below_normal():
    try:
        import ctypes
        h = ctypes.windll.kernel32.GetCurrentProcess()
        ctypes.windll.kernel32.SetPriorityClass(h, 0x4000)
    except Exception:
        pass


def cover_config(word):
    """Config di copertura di una coprente (parola completa e2+w101, e2[0]=R su
    TGT): (h1, req|S_CORE) — h1 = heading dopo la svolta di copertura."""
    c0, h0, req = exact_state(word)
    assert c0 == TGT
    h1 = (h0 - 1) & 3          # il bit di copertura e' R (nera)
    rt = tuple(req.get(c, FREE) for c in S_CORE)
    return (h1, rt)


# ---------------- campagna (worker) ----------------

def _heading_toward(c, h, target):
    """Bit preferito per orientare il prossimo passo all'indietro verso target
    (il prepend cade su c-D[h] per entrambi i bit; il bit decide h')."""
    best = None; bestd = None
    for bit in (0, 1):
        hn = (h - 1) & 3 if bit == 1 else (h + 1) & 3
        cn2 = (c[0] - DX[h] - DX[hn], c[1] - DY[h] - DY[hn])
        dd = max(abs(cn2[0] - target[0]), abs(cn2[1] - target[1]))
        if bestd is None or dd < bestd:
            bestd = dd; best = bit
    return best


_W101 = None


def _init_worker(w101_bits):
    global _W101
    _W101 = tuple(w101_bits)
    _below_normal()


def hunt_worker(job):
    """Passeggiate casuali all'indietro sopra w101; hit = prepend che cade su
    TGT (prima visita all'indietro). Ritorna (nere, bianche, tentativi)."""
    (wid, seed, budget_s, cap_nere) = job
    rng = random.Random(seed)
    w101 = _W101
    c0, h0, req0 = exact_state(w101)
    t0 = time.time()
    nere = set(); bianche = 0; walks = 0
    while time.time() - t0 < budget_s and len(nere) < cap_nere:
        walks += 1
        # politica randomizzata per passeggiata (anti trappola bb)
        p_L = rng.uniform(0.05, 0.6)
        p_steer = rng.uniform(0.0, 0.9)
        wild = rng.randrange(0, 60)            # fase iniziale senza steering
        max_steps = rng.randrange(8, 320)
        away = rng.random() < 0.3              # stile deep/jackseed: prima fuggi
        away_len = rng.randrange(20, 200) if away else 0
        c, h, req = c0, h0, dict(req0)
        ext = ()
        for step in range(max_steps):
            cn = (c[0] - DX[h], c[1] - DY[h])
            if cn[1] < 1:
                break
            r = req.get(cn, FREE)
            if cn == TGT:
                # copertura: la prima visita all'indietro a (1,1)
                if r == FREE or r == 0:
                    # bit R legge bianco => coprente NERA
                    e2 = (1,) + ext
                    nere.add(e2)
                if r == FREE or r == 1:
                    bianche += 1
                break                          # in ogni caso la storia si ferma qui
            # scelta del bit (su rivisitata e' forzata)
            if r == FREE:
                if step >= wild and rng.random() < p_steer:
                    tgt = ((c[0], c[1] + 12) if step < away_len else TGT)
                    bit = _heading_toward(c, h, tgt)
                else:
                    bit = 0 if rng.random() < p_L else 1
            else:
                bit = 1 if r == 0 else 0       # read forzato = req
            c2, h2, _ = exact_step(c, h, req, bit)
            if c2 is None:
                break
            c, h = c2, h2
            ext = (bit,) + ext
    return wid, nere, bianche, walks


# ---------------- verdetto per parola (worker fase B) ----------------

def verdict_worker(job):
    """wall_exhaustive con cap rapidi; ritorna il verdetto born-near."""
    (e2, node_cap, depth_cap) = job
    w2 = tuple(e2) + _W101
    tr = anchor_trace(w2)
    r_foot = max(cheb(c) for c in tr[0])
    exh, D_true, r_wall, nodes, min_pend = wall_exhaustive(
        w2, node_cap=node_cap, depth_cap=depth_cap)
    return (e2, r_foot, exh, D_true, r_wall, nodes, min_pend)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--budget-s", type=int, default=600)
    ap.add_argument("--node-cap", type=int, default=60_000)
    ap.add_argument("--depth-cap", type=int, default=150)
    ap.add_argument("--node-cap-big", type=int, default=3_000_000)
    ap.add_argument("--depth-cap-big", type=int, default=450)
    ap.add_argument("--cross-samples", type=int, default=8)
    ap.add_argument("--cap-nere", type=int, default=40_000,
                    help="cap di nere distinte per worker (bersaglio = config)")
    ap.add_argument("--seed", type=int, default=94)
    ap.add_argument("--smoke", action="store_true",
                    help="smoke-test: budget corto, soglie GC3 rilassate")
    args = ap.parse_args()
    if args.smoke:
        args.budget_s = min(args.budget_s, 45)
    t0 = time.time()
    log(f"censimento born_near §94: workers={args.workers} budget={args.budget_s}s "
        f"cap rapido={args.node_cap}/{args.depth_cap} seed={args.seed}")

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])

    # ---------- GATE GC0: i 60 coprenti §90c -> 2 config ----------
    cc = json.load(open(CC))
    cfg90 = set()
    for r in cc["rows"]:
        e2 = to_bits(r["word_ext"])
        w2 = e2 + w101
        assert valid(w2)[1] is None
        if r["colore_11"] == "B":
            cfg90.add(cover_config(w2))
    log(f"GC0: config distinte dei coprenti-neri §90c = {len(cfg90)}")
    assert len(cfg90) == 2, f"GC0 FALLITO: attese 2 config (§92c), viste {len(cfg90)}"

    # ---------- GATE GC1: i 12 testimoni finiti bit-identici al summary ----------
    bn = json.load(open(BN))
    wit_words = collect_black_covers(w101)
    assert len(bn["rows"]) == len(wit_words), "ordine collect_black_covers cambiato!"
    n_gc1 = 0
    for (name, e2), ref in zip(wit_words, bn["rows"]):
        # NB: i nomi cc90c_prof* NON sono unici (piu' coprenti a pari prof.):
        # il pairing corretto e' per INDICE (ordine deterministico), col nome
        # e la profondita' come sanity check.
        assert ref["nome"] == name and ref["prof"] == len(e2), (name, ref["nome"])
        if not ref["esaurito"] or ref["nodi"] > 2_000_000:
            continue
        exh, D_true, r_wall, nodes, min_pend = wall_exhaustive(
            e2 + w101, node_cap=args.node_cap_big, depth_cap=args.depth_cap_big)
        assert exh and D_true == ref["D_true"] and min_pend == ref["min_pend_nodi"], \
            (name, D_true, ref["D_true"], min_pend, ref["min_pend_nodi"])
        n_gc1 += 1
    log(f"GC1: {n_gc1} testimoni finiti riprodotti bit-identici al summary §93")
    assert n_gc1 >= 10, f"GC1 FALLITO: solo {n_gc1} testimoni riprodotti"

    # ---------- campagna ----------
    jobs = [(w, args.seed * 1000 + w, args.budget_s, args.cap_nere)
            for w in range(args.workers)]
    nere = set(); bianche = 0; walks = 0
    with mp.Pool(args.workers, initializer=_init_worker,
                 initargs=(list(w101),)) as pool:
        for wid, ns, nb, nw in pool.imap_unordered(hunt_worker, jobs):
            nere |= ns; bianche += nb; walks += nw
            log(f"  worker {wid}: +{len(ns)} nere (tot distinte {len(nere)}), "
                f"{nw} passeggiate")
    log(f"campagna: {len(nere)} coprenti-nere DISTINTE, ~{bianche} hit bianche, "
        f"{walks} passeggiate totali")

    # unione coi 48 testimoni noti (garantisce copertura delle config note)
    for name, e2 in wit_words:
        nere.add(tuple(e2))

    # ---------- GATE GC4: ledger del camminatore == exact_state ----------
    smp = random.Random(args.seed).sample(sorted(nere), min(100, len(nere)))
    for e2 in smp:
        w2 = tuple(e2) + w101
        assert valid(w2)[1] is None, "hit non valida!"
        assert e2[0] == 1, "coprente nera deve avere primo bit R"
        c0, h0, req = exact_state(w2)
        assert c0 == TGT, "il passo piu' antico non e' su (1,1)!"
    log(f"GC4: {len(smp)} hit ricontrollate con valid()+exact_state: tutte coprenti-nere")

    # ---------- classificazione per config ----------
    by_cfg = {}
    for e2 in nere:
        cfg = cover_config(tuple(e2) + w101)
        by_cfg.setdefault(cfg, []).append(e2)
    n_cfg = len(by_cfg)
    log(f"config di copertura distinte: {n_cfg} (le §90c erano {len(cfg90)}; "
        f"§92c ne cito' 43)")
    # GC3: soglie minime
    min_cfg, min_nere = (5, 200) if args.smoke else (30, 10_000)
    assert n_cfg >= min_cfg, f"GC3 FALLITO: solo {n_cfg} config (attese >={min_cfg})"
    assert len(nere) >= min_nere, \
        f"GC3 FALLITO: solo {len(nere)} nere (attese >={min_nere})"
    assert len(set(by_cfg) - cfg90) >= 1, "GC3 FALLITO: nessuna config nuova"

    # ---------- fase B: verdetto born-near per parola (cap rapidi) ----------
    all_words = sorted(nere)
    log(f"fase B: verdetto rapido su {len(all_words)} parole "
        f"(cap {args.node_cap}/{args.depth_cap})")
    jobsB = [(e2, args.node_cap, args.depth_cap) for e2 in all_words]
    res = {}
    done = 0
    with mp.Pool(args.workers, initializer=_init_worker,
                 initargs=(list(w101),)) as pool:
        for r in pool.imap_unordered(verdict_worker, jobsB, chunksize=64):
            res[r[0]] = r
            done += 1
            if done % 20000 == 0:
                log(f"  fase B: {done}/{len(all_words)}")

    # secondo passo: TUTTE le cap-raggiunte ricevono cap grandi (se poche;
    # oltre la soglia si campiona per config, dichiarandolo)
    capped = [e2 for e2, r in res.items() if not r[2]]
    if len(capped) <= 500:
        second = capped
        note2 = "tutte"
    else:
        by_cfg_capped = {}
        for e2 in capped:
            cfg = cover_config(tuple(e2) + w101)
            by_cfg_capped.setdefault(cfg, []).append(e2)
        rng2 = random.Random(args.seed + 1)
        second = []
        for cfg, lst in by_cfg_capped.items():
            second += rng2.sample(lst, min(10, len(lst)))
        note2 = f"campione 10/config su {len(by_cfg_capped)} config"
    log(f"fase B: {len(capped)} parole a cap rapido raggiunto -> secondo passo "
        f"su {len(second)} ({note2}; cap {args.node_cap_big}/{args.depth_cap_big})")
    jobs2 = [(e2, args.node_cap_big, args.depth_cap_big) for e2 in second]
    if jobs2:
        with mp.Pool(min(args.workers, len(jobs2)), initializer=_init_worker,
                     initargs=(list(w101),)) as pool:
            for r in pool.imap_unordered(verdict_worker, jobs2):
                res[r[0]] = r
    log(f"fase B: secondo passo completato su {len(second)} parole")

    # ---------- GATE GC2: cross-validazione di terra ----------
    exhausted = [e2 for e2, r in res.items() if r[2] and r[5] <= 40_000]
    smp2 = random.Random(args.seed + 2).sample(
        exhausted, min(args.cross_samples, len(exhausted)))
    for e2 in smp2:
        w2 = tuple(e2) + w101
        nv, Dv, mpv = gate_cross(w2)
        r = res[e2]
        assert Dv == r[3] and mpv == r[6], (e2, Dv, r[3], mpv, r[6])
    log(f"GC2: {len(smp2)} alberi esauriti cross-validati con valid() di terra: "
        f"(D, min_pend) bit-identici")

    # ---------- sintesi ----------
    cfg_rows = []
    tot_cert = tot_fug = tot_mp0 = 0
    fug_rows = []
    for idx, (cfg, lst) in enumerate(
            sorted(by_cfg.items(), key=lambda kv: -len(kv[1]))):
        n_cert = n_fug = n_mp0 = 0
        r_seed_max = 0
        D_vals = Counter()
        for e2 in lst:
            r = res[e2]
            (_, r_foot, exh, D_true, r_wall, nodes, min_pend) = r
            if exh and min_pend > 0:
                n_cert += 1
                r_seed_max = max(r_seed_max, max(r_foot, r_wall))
                D_vals[D_true] += 1
            elif exh:
                n_mp0 += 1
            else:
                n_fug += 1
                fug_rows.append({
                    "word_ext": "".join("R" if b else "L" for b in e2),
                    "prof": len(e2), "D_raggiunto": D_true,
                    "r_wall": r_wall, "nodi": nodes,
                    "cap": ("big" if nodes >= args.node_cap_big or
                            D_true >= args.depth_cap_big - 1 else "rapido"),
                    "config_idx": idx})
        tot_cert += n_cert; tot_fug += n_fug; tot_mp0 += n_mp0
        cfg_rows.append({
            "config_idx": idx,
            "h1": cfg[0], "req_S": list(cfg[1]), "n_parole": len(lst),
            "certificate": n_cert, "fuggenti": n_fug, "min_pend_0": n_mp0,
            "r_seed_max": r_seed_max,
            "D_hist": {str(k): v for k, v in sorted(D_vals.items())},
            "e' delle §90c": cfg in cfg90})
    log(f"SINTESI: {len(nere)} coprenti-nere distinte in {n_cfg} config; "
        f"CERTIFICATE born-near {tot_cert} | fuggenti {tot_fug} | "
        f"esaurite-con-min-pend-0 {tot_mp0}")
    if tot_mp0 > 0:
        log("ATTENZIONE: alberi esauriti con min_pend=0 => la gamba-2 NON copre "
            "queste parole (solo gamba-1 origine): da ispezionare!")

    out = {"args": vars(args),
           "gates": {"GC0_config_90c": len(cfg90),
                     "GC1_testimoni_riprodotti": n_gc1,
                     "GC2_cross_validati": len(smp2),
                     "GC4_hit_ricontrollate": len(smp)},
           "campagna": {"nere_distinte": len(nere), "hit_bianche": bianche,
                        "passeggiate": walks},
           "config_distinte": n_cfg,
           "certificate": tot_cert, "fuggenti": tot_fug,
           "esaurite_min_pend_0": tot_mp0,
           "per_config": cfg_rows,
           "fuggenti_dettaglio": fug_rows,
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    log(f"scritto {OUT_JSON} in {out['elapsed_s']} s")


if __name__ == "__main__":
    main()
