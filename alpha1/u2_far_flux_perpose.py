# u2_far_flux_perpose.py — §94: chiusura induttiva PER-POSA del parity-flux.
#
# u2_far_flux_closure ha mostrato che phi_colonna0 = p(0,1)+p(0,2)+[posa=(0,2)]
# e' vero sui campioni ma NON e' induttivo nel dominio lineare globale: i passi
# killer (es. posa (0,2) -> (0,3) con p(0,3) pendente) richiedono fatti
# CONDIZIONALI ALLA POSA ("posa=(0,2) => p(0,3)=0"). Qui si sale al dominio
# standard: UNA relazione affine GF(2) PER CLASSE DI POSA (33 pose di W + OUT).
#
#   I_c = spazio affine generato dai campioni con posa c  (base di differenze
#         + rappresentante);  invarianti di classe = nullspace + costanti.
#   CHIUSURA: per ogni tipo-di-passo t: c -> cn (delta_t noto, vincoli su
#   req(cn) noti), l'immagine di I_c ristretta ai vincoli deve stare in I_cn:
#     per ogni psi in I_cn:  psi . (v ^ delta_t) = k_psi  per ogni v in I_c
#     con req(cn) = r  <=>  il vincolo (psi, k_psi ^ psi.delta_t) e' IMPLICATO
#     da I_c + {req(cn)=r}. Implicazione = risolubilita' del sistema aumentato
#     con la negazione (feasibility GF(2)).
#   Houdini: si eliminano gli psi non implicati e si itera al punto fisso
#   (il punto fisso e' il massimo invariante induttivo dentro lo spazio
#   campionato).
#
# VERDETTO: phi_colonna0 e' TEOREMA se, al punto fisso, per ogni classe c la
# restrizione di phi_colonna0 a c (p(0,1)+p(0,2) = 1 ^ [c=(0,2)]) e' implicata
# da I_c, e v0 (posa (1,1)) soddisfa I_{(1,1)}.
#
# GATE:
#   PP0 controllo positivo: par(x+y)+par(h) implicato in ogni classe;
#   PP1 esca: delta corrotto sui passi OUT->OUT uccide il controllo positivo;
#   PP2 v0 delle 42 fuggenti note soddisfa I_{(1,1)} (per parola: le costanti
#       di classe possono differire per parola -> si verifica il phi bersaglio);
#   PP3 la chiusura DEVE potare qualcosa (se nessuno psi muore, il test non
#       distingue: sospetto di vacuita').
#
# Uscita: alpha1/u2_far_flux_perpose_summary.json (+ .log)
import sys, os, json, time, random, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_weapon_vitality import to_bits, SUMMARY
from u2_cover_rail_map import valid
from u2_pocket_certificate import exact_state, exact_step, FREE
from onset_cone_lock import DX, DY
from u2_far_parity_flux import (W_CELLS, W_IDX, NW, BALL2, F_P, F_V, F_POSE,
                                F_OUT, F_HEAD, F_PAR, F_BIAS, NFEAT,
                                feat_vector, dot, Basis, nullspace, pend2_of)
from u2_far_flux_closure import step_types, parity_bits, pose_bit, feasible

HERE = os.path.dirname(os.path.abspath(__file__))
WIT = os.path.join(HERE, "u2_cover_witnesses.json")
CEN = os.path.join(HERE, "u2_far_born_near_census_summary.json")
OUT_JSON = os.path.join(HERE, "u2_far_flux_perpose_summary.json")
LOG = os.path.join(HERE, "u2_far_flux_perpose.log")

OUTCLS = "OUT"


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def pose_class(c):
    return c if c in W_IDX else OUTCLS


def sample_classes(words, rng, n_walks, max_steps):
    """Camminate; per classe di posa: (rappresentante v_ref, base differenze)."""
    cls = {}                              # classe -> [v_ref, Basis]

    def add(v, c):
        k = pose_class(c)
        if k not in cls:
            cls[k] = [v, Basis()]
        else:
            cls[k][1].add(v ^ cls[k][0])

    n_samples = 0
    for name, word in words:
        c0, h0, req0 = exact_state(word)
        add(feat_vector(c0, h0, req0), c0)
        for wk in range(n_walks):
            p_L = rng.uniform(0.05, 0.55)
            p_steer = rng.uniform(0.2, 0.95)
            c, h, req = c0, h0, dict(req0)
            for step in range(max_steps):
                cn = (c[0] - DX[h], c[1] - DY[h])
                if cn[1] < 1:
                    break
                r = req.get(cn, FREE)
                if r == FREE:
                    if rng.random() < p_steer:
                        targ = None; td = None
                        for cb in BALL2:
                            if req.get(cb, FREE) == 0:
                                dd = max(abs(c[0] - cb[0]), abs(c[1] - cb[1]))
                                if td is None or dd < td:
                                    td = dd; targ = cb
                        if targ is not None:
                            best = None; bd = None
                            for b in (0, 1):
                                hn = (h - 1) & 3 if b == 1 else (h + 1) & 3
                                cn2 = (cn[0] - DX[hn], cn[1] - DY[hn])
                                dd = max(abs(cn2[0] - targ[0]),
                                         abs(cn2[1] - targ[1]))
                                if bd is None or dd < bd:
                                    bd = dd; best = b
                            bit = best
                        else:
                            bit = 0 if rng.random() < p_L else 1
                    else:
                        bit = 0 if rng.random() < p_L else 1
                else:
                    bit = 1 if r == 0 else 0
                c2, h2, _ = exact_step(c, h, req, bit)
                if c2 is None:
                    break
                c, h = c2, h2
                add(feat_vector(c, h, req), c)
                n_samples += 1
    return cls, n_samples


def class_invariants(cls):
    """classe -> lista (psi, costante)."""
    out = {}
    for k, (vref, basis) in cls.items():
        null = nullspace(basis.rows, NFEAT)
        out[k] = [(psi, dot(psi, vref)) for psi in null]
    return out


def implied(inv_c, extra_fix, psi, k_target):
    """(psi, k_target) e' implicato da I_c + vincoli fissi? Vero sse il sistema
    I_c + fix + (psi = 1-k_target) e' INFEASIBILE."""
    eqs = [(phi, cc) for phi, cc in inv_c]
    eqs += [(1 << idx, val) for idx, val in extra_fix]
    eqs.append((1 << F_BIAS, 1))
    eqs.append((psi, 1 - k_target))
    return not feasible(eqs)


def closure(inv, steps, tag=""):
    """Houdini per-classe. inv: classe -> [(psi, k)]. Ritorna punto fisso."""
    inv = {k: list(v) for k, v in inv.items()}
    rounds = 0
    killed_log = []
    while True:
        rounds += 1
        kills = []                          # (classe, indice, killer)
        for name, delta, fix in steps:
            # classe sorgente e destinazione dal tipo di passo
            src = None; dst = None
            for idx, val in fix:
                if val == 1 and F_POSE <= idx < F_OUT:
                    src = W_CELLS[idx - F_POSE]
                if val == 1 and idx == F_OUT:
                    src = OUTCLS
            # destinazione: dal delta sui bit di posa
            dst_bits = [i for i in range(F_POSE, F_OUT + 1)
                        if (delta >> i) & 1]
            dst = src
            for i in dst_bits:
                cand = OUTCLS if i == F_OUT else W_CELLS[i - F_POSE]
                if cand != src:
                    dst = cand
            if src not in inv or dst not in inv:
                continue                    # classe mai campionata: nessun
                                            # vincolo da/verso di essa (sound?
                                            # NO: va dichiarato — vedi main)
            fix_req = [(i, v) for i, v in fix
                       if not (F_POSE <= i <= F_OUT) and not
                       (F_HEAD <= i < F_HEAD + 4) and not
                       (F_PAR <= i < F_PAR + 3)]
            # heading/parita' della sorgente sono vincoli legittimi: tienili
            fix_all = [(i, v) for i, v in fix
                       if not (F_POSE <= i <= F_OUT)]
            for j, (psi, k) in enumerate(inv[dst]):
                if implied(inv[src], fix_all, psi, k ^ dot(psi, delta)):
                    continue
                kills.append((dst, j, name))
        if not kills:
            break
        seen = set()
        for dst, j, name in sorted(kills, key=lambda t: -t[1]):
            if (dst, j) in seen:
                continue
            seen.add((dst, j))
            killed_log.append((dst, readable_short(inv[dst][j][0]), name))
            del inv[dst][j]
        log(f"  {tag}round {rounds}: uccisi {len(seen)} "
            f"(vivi {sum(len(v) for v in inv.values())})")
    return inv, rounds, killed_log


def readable_short(phi):
    supp = []
    for i in range(NFEAT):
        if (phi >> i) & 1:
            supp.append(
                f"p{W_CELLS[i-F_P]}" if i < F_V else
                f"v{W_CELLS[i-F_V]}" if i < F_POSE else
                f"pose{W_CELLS[i-F_POSE]}" if i < F_OUT else
                "OUT" if i == F_OUT else
                f"h{i-F_HEAD}" if i < F_PAR else
                ["x%2", "y%2", "(x+y)%2"][i - F_PAR] if i < F_BIAS else "1")
    return "+".join(supp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--walks", type=int, default=3000)
    ap.add_argument("--max-steps", type=int, default=8000)
    ap.add_argument("--seed", type=int, default=942)
    args = ap.parse_args()
    t0 = time.time()

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    wit = json.load(open(WIT))
    words = []
    for grp in ("jackpot", "nere400"):
        for k, w in enumerate(wit[grp]):
            e2 = to_bits(w["word"])
            words.append((f"{grp}[{k}]", tuple(e2) + tuple(w101)))
    log(f"per-pose §94: {len(words)} fuggenti, walks={args.walks} "
        f"max_steps={args.max_steps}")

    rng = random.Random(args.seed)
    cls, n_samples = sample_classes(words, rng, args.walks, args.max_steps)
    log(f"campioni: {n_samples}; classi di posa campionate: {len(cls)}/"
        f"{NW + 1}")
    non_campionate = [str(c) for c in W_CELLS if c not in cls]
    if OUTCLS not in cls:
        non_campionate.append(OUTCLS)
    log(f"classi MAI campionate: {non_campionate if non_campionate else 'nessuna'}")

    inv0 = class_invariants(cls)
    tot0 = sum(len(v) for v in inv0.values())
    log(f"invarianti di classe iniziali: {tot0}")

    steps = step_types()
    # SOUNDNESS delle classi mai campionate: se una classe non campionata e'
    # DESTINAZIONE raggiungibile di un passo da una classe campionata, la
    # chiusura non e' un certificato. Le si tratta come TOP (nessun vincolo)
    # e si segnala ogni arco src(campionata)->dst(mai campionata) FEASIBLE.
    archi_top = []
    for name, delta, fix in steps:
        src = None
        for idx, val in fix:
            if val == 1 and F_POSE <= idx < F_OUT:
                src = W_CELLS[idx - F_POSE]
            if val == 1 and idx == F_OUT:
                src = OUTCLS
        dst_bits = [i for i in range(F_POSE, F_OUT + 1) if (delta >> i) & 1]
        dst = src
        for i in dst_bits:
            cand = OUTCLS if i == F_OUT else W_CELLS[i - F_POSE]
            if cand != src:
                dst = cand
        if src in cls and dst not in cls:
            fix_all = [(i, v) for i, v in fix if not (F_POSE <= i <= F_OUT)]
            eqs = [(phi, cc) for phi, cc in inv0[src]]
            eqs += [(1 << idx, val) for idx, val in fix_all]
            eqs.append((1 << F_BIAS, 1))
            if feasible(eqs):
                archi_top.append((name, str(dst)))
    log(f"archi feasible verso classi mai campionate: {len(archi_top)} "
        f"{'(VIETANO il certificato pieno su quelle classi!)' if archi_top else ''}")

    inv_fix, rounds, killed_log = closure(inv0, steps)
    tot_fix = sum(len(v) for v in inv_fix.values())
    log(f"punto fisso in {rounds} round: {tot_fix}/{tot0} invarianti")
    assert tot_fix < tot0 or not killed_log, "?"
    if tot_fix == tot0:
        log("PP3: ATTENZIONE, nessuno psi ucciso: chiusura sospetta di vacuita'")

    # verdetto phi_colonna0: per ogni classe campionata, la restrizione
    # p(0,1)+p(0,2) = 1 ^ [classe=(0,2)] deve essere implicata da I_c (senza
    # vincoli extra)
    phi_p = (1 << (F_P + W_IDX[(0, 1)])) | (1 << (F_P + W_IDX[(0, 2)]))
    verdict = {}
    for k in cls:
        k_target = 0 if k == (0, 2) else 1
        verdict[str(k)] = implied(inv_fix[k], [], phi_p, k_target)
    n_ok = sum(1 for v in verdict.values() if v)
    log(f"phi_colonna0 implicato al punto fisso in {n_ok}/{len(verdict)} classi")
    all_ok = n_ok == len(verdict) and not archi_top
    log(f"VERDETTO phi_colonna0 induttivo per-posa: {all_ok}")

    # PP0: controllo positivo
    phi_univ = (1 << (F_PAR + 2)) | (1 << (F_HEAD + 1)) | (1 << (F_HEAD + 3))
    pp0 = all(implied(inv_fix[k], [],
                      phi_univ, dot(phi_univ, cls[k][0])) for k in cls)
    log(f"PP0 (universale implicato in ogni classe): {pp0}")
    assert pp0, "PP0 FALLITO"

    # PP1: esca — delta corrotto (parita' omessa nei passi OUT->OUT)
    steps_esca = []
    for name, delta, fix in steps:
        if name.startswith("OUT"):
            delta ^= 1 << (F_PAR + 2)
        steps_esca.append((name, delta, fix))
    inv_e, _, _ = closure(inv0, steps_esca, tag="esca ")
    pp1 = not all(implied(inv_e.get(k, []), [], phi_univ,
                          dot(phi_univ, cls[k][0])) for k in cls)
    log(f"PP1 (esca uccide l'universale da qualche classe): {pp1}")
    assert pp1, "PP1 FALLITO: la chiusura non becca il delta corrotto"

    # PP2: v0 delle 42 fuggenti note nella classe (1,1)
    cen = json.load(open(CEN))
    fugg = list(words)
    for k, f in enumerate(cen["fuggenti_dettaglio"]):
        fugg.append((f"cens[{k}]", tuple(to_bits(f["word_ext"])) + tuple(w101)))
    n_pp2 = 0
    for name, w2 in fugg:
        c0, h0, req0 = exact_state(w2)
        v0 = feat_vector(c0, h0, req0)
        if dot(phi_p, v0) == 1:             # posa (1,1) != (0,2)
            n_pp2 += 1
        else:
            log(f"  PP2: {name} costante iniziale 0!")
    log(f"PP2: costante iniziale colonna-0 = 1 su {n_pp2}/{len(fugg)}")

    out = {"args": vars(args),
           "campioni": n_samples,
           "classi": len(cls),
           "classi_mai_campionate": non_campionate,
           "archi_verso_top": archi_top,
           "invarianti_iniziali": tot0,
           "invarianti_punto_fisso": tot_fix,
           "round": rounds,
           "phi_colonna0_per_classe": verdict,
           "phi_colonna0_induttivo": all_ok,
           "pp0": pp0, "pp1": pp1,
           "pp2": [n_pp2, len(fugg)],
           "uccisi_esempi": [{"classe": str(c), "psi": p, "killer": kk}
                             for c, p, kk in killed_log[:40]],
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    log(f"scritto {OUT_JSON} in {out['elapsed_s']} s")
    if all_ok:
        log("*** phi_colonna0 E' INDUTTIVO nel dominio per-posa (sul campione "
            "di 8 fuggenti): candidato TEOREMA DEL LEDGER SPORCO >=1 — "
            "resta la promozione word-independent (costanti per parola). ***")


if __name__ == "__main__":
    main()
