# u2_far_clean_stretch.py — §95 (U2-LONTANO 3): il TRATTO PULITO.
#
# CONTESTO (§94c): il pavimento del ledger e' falsificato (pend2=0 raggiungibile,
# posa (-1,2) in palla); sopravvive il LEDGER SPORCO v2 (posa di nascita fuori
# palla-2 => pend2 >= 1), che basta al Muro ma era solo "mai visto violato"
# (~1,45G nodi, survivorship di politica — trappola hh). Il programma §95.2
# ("chiusura per vitalita'": pend2=0 => albero dei prepend finito) e' FALSO
# cosi' com'era: i nodi puliti di nere400[0]/[2] hanno sottoalbero INTERO vivo
# oltre depth 400 (misurato qui, gate G2). L'oggetto giusto e' un altro:
#
# CONVENZIONE BIT (fissata dal pannello §95): to_bits mappa 'R'->1, 'L'->0;
# bit 1 = R = lettura BIANCA (read=0, svolta forward h+1), bit 0 = L = lettura
# NERA (read=1). Nel codice: read = 0 if bit == 1 else 1.
#
# LEMMA DEL PASSO DI PULIZIA (deduttivo, dal ledger §93):
#   il pending di una cella cambia SOLO alla cella cn del passo corrente;
#   pend2 (= #pending con cheb<=2) decrementa <=> il passo e' R (read=0) su
#   cn pending con cheb(cn)<=2; il decremento e' esattamente 1 e la posa
#   dopo il passo E' cn, dentro la palla-2. QED.
#
# TEOREMA DEL TRATTO PULITO (riduzione, deduttivo dato il lemma; enunciato
# riparato dal pannello §95: m* <= n):
#   sia n un nodo con pend2(n)=0 in un albero dei prepend con radice sporca
#   (pend2(root)>=1). Allora esiste m* <= n, ultimo nodo della catena root->n
#   in cui pend2 transisce 1->0 (eventualmente m* = n), con posa(m*) in
#   palla-2, e pend2 == 0 su TUTTO il tratto [m*, n]: n appartiene al
#   SOTTOALBERO PULITO di m* (prepend con pend2=0 a ogni nodo intermedio).
#   RADICAMENTO A w101 (pannello §95, attacco 5): pend2(w101) = 6 >= 1 (GATE
#   G1b) => la riduzione vale per OGNI passato completo che presenta w101 a un
#   record, a qualunque profondita' avvenga la nascita (dentro o sopra
#   qualsiasi coprente): ogni nascita pulita ha un m* strettamente sopra il
#   nodo-w101.
#   COROLLARIO: Ledger Sporco v2 ("nascita con posa fuori palla => pend2>=1")
#   <=> nessun sottoalbero pulito sopra un nodo di pulizia raggiungibile
#   contiene una posa fuori palla-2. I 1.376 clean-far astratti (§93f) sono
#   raggiungibili SOLO attraverso un tratto pulito.
#
# DICOTOMIA DEL TRATTO PULITO (deduttiva; sostituisce l'enunciato ingenuo
# "sottoalbero pulito sempre finito", smontato dal pannello §95 — fuori palla
# il tratto potrebbe vagare a pend2=0): dentro un tratto pulito nessuna cella
# della palla e' pending, quindi sulle celle di palla sono possibili solo
# R-su-fresca (req diventa 1) — L su fresca/req=1 aprirebbe/riaprirebbe un
# pending in palla (esce dal tratto), L su pending e' irrealizzabile (§93), R
# su req=1 e' irrealizzabile. Le celle di palla visitabili sono le 10
# {|x|<=2, y in {1,2}} (valid() esige y>=1; (0,0) e' la posa finale, mai
# letta), ognuna al piu' UNA volta nel tratto. QUINDI per ogni nodo di pulizia
# m*: O il sottoalbero pulito resta confinato in palla (profondita' <= 10,
# l'enumerazione esaurisce SEMPRE), O il primo nodo con posa fuori palla e'
# GIA' un testimone clean-far (pend2=0, posa fuori, profondita' <= 11 da m*) =
# falsificazione di v2. L'enumeratore tronca i rami alla prima posa fuori
# palla (foglia-testimone): esaurisce sempre, e ogni non-confinamento produce
# un TESTIMONE esplicito, mai un rosso generico.
#
# QUANTIFICATORI (onesta', trappole hh/gg): i certificati di confinamento sono
# per-nodo-di-pulizia RAGGIUNTO (controesempi §94 + cacce G3 multi-politica):
# v2 resta congettura empirica sui nodi non raggiunti. La promozione deduttiva
# candidata (pannello §95): enumerazione a oracolo pigro sugli stati astratti
# di pulizia (posa in 10 celle, heading 4, req lazy su {cheb<=3, y>=1},
# profondita' <= 11) — vedi u2_far_clean_oracle.py (§95d).
#
# GATE (fermarsi al primo rosso; ognuno puo' fallire):
#   G0 lemma del passo di pulizia DI TERRA: scan di ogni passo dei 10
#      controesempi §94 + estensioni casuali; ogni decremento di pend2 deve
#      essere (-1, read=0, rb=0, cheb(cn)<=2, posa==cn). ESCA: il claim
#      rafforzato a palla-1 (cheb<=1) DEVE trovare violazioni (il checker sa
#      fallire).
#   G1 root sporchi: le fuggenti nominali (8 §92 + 34 censimento §94) dedup
#      per parola; pend2(root) >= 1 su tutte; conteggio duplicati coerente con
#      §94a (34 = 6 vecchie nere400 + 28 nuove => 36 distinte).
#   G2 tratti puliti esaustivi sui controesempi: per ogni controesempio §94,
#      TUTTI i nodi puliti del cammino; per ciascuno (a) sottoalbero INTERO
#      sondato (vivo/finito — risposta alla domanda §95.2 originale),
#      (b) sottoalbero PULITO enumerato esaustivamente: DEVE esaurirsi e non
#      contenere pose fuori palla (se ne contiene una: v2 FALSIFICATA, il gate
#      la salva come testimone).
#   G3 caccia multi-politica a NUOVI nodi di pulizia (antidoto trappola hh:
#      >= 3 famiglie di politiche indipendenti) sulle 36 fuggenti distinte:
#      (P1) milestone-greedy stile §93 (chiudi i pend2 uno alla volta),
#      (P2) DFS greedy mirata stile lente §94 (ordina per pend2, poi random),
#      (P3) passeggiate profonde randomizzate con steering occasionale.
#      Ogni volta che pend2 tocca 0: lemma in-run (posa in palla), dedupe per
#      stato, poi sottoalbero PULITO esaustivo => in palla. In piu' caccia
#      DIRETTA al falsificatore (goal pend2==0 & cheb(posa)>2).
#   G4 soglie asseribili (trappola cc): >= MIN_CLEAN nodi di pulizia distinti,
#      da >= 2 politiche e >= 3 fuggenti diverse; altrimenti ROSSO (si alza il
#      budget, non la soglia).
#
# Uscita: alpha1/u2_far_clean_stretch_summary.json (+ .log append-only)
import sys, os, json, time, random, argparse, multiprocessing as mp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_weapon_vitality import to_bits, to_str, SUMMARY
from u2_cover_rail_map import valid
from u2_pocket_certificate import exact_state, exact_step, FREE
from u2_far_ledger import cheb, pend_set
from u2_far_born_near import wall_exhaustive
from onset_cone_lock import DX, DY

HERE = os.path.dirname(os.path.abspath(__file__))
WIT = os.path.join(HERE, "u2_cover_witnesses.json")
CEN = os.path.join(HERE, "u2_far_born_near_census_summary.json")
CEX = os.path.join(HERE, "u2_far_pend2_counterexamples.json")
OUT_JSON = os.path.join(HERE, "u2_far_clean_stretch_summary.json")
LOG = os.path.join(HERE, "u2_far_clean_stretch.log")

BALL_R = 2


def _below_normal():
    try:
        import ctypes
        h = ctypes.windll.kernel32.GetCurrentProcess()
        ctypes.windll.kernel32.SetPriorityClass(h, 0x4000)
    except Exception:
        pass


def pend2_of(req):
    return sorted(c for c in pend_set(req) if cheb(c) <= BALL_R)


def state_sig(c, h, req):
    """Firma esatta dello stato del camminatore (per dedupe dei nodi)."""
    return (c, h, tuple(sorted(req.items())))


# ---------------- camminatore con ledger pend2 e undo ----------------

class Walker:
    __slots__ = ("c", "h", "req", "pend", "p2", "bits", "trail")

    def __init__(self, word):
        c, h, req = exact_state(word)
        self.c = c; self.h = h
        self.req = dict(req)
        self.pend = pend_set(req)
        self.p2 = sum(1 for x in self.pend if cheb(x) <= BALL_R)
        self.bits = []
        self.trail = []

    def next_cell(self):
        return (self.c[0] - DX[self.h], self.c[1] - DY[self.h])

    def legal_bits(self):
        cn = self.next_cell()
        if cn[1] < 1:
            return []
        r = self.req.get(cn, FREE)
        if r == FREE:
            return [0, 1]
        return [1 if r == 0 else 0]

    def apply(self, bit):
        cn = self.next_cell()
        read = 0 if bit == 1 else 1
        old = self.req.get(cn, FREE)
        pd = 0; dp2 = 0
        if read == 1 and cn not in self.pend:
            pd = 1
            if cheb(cn) <= BALL_R:
                dp2 = 1
        elif read == 0 and cn in self.pend:
            pd = -1
            if cheb(cn) <= BALL_R:
                dp2 = -1
        self.trail.append((self.c, self.h, cn, old, pd, dp2))
        self.req[cn] = 1 - read
        if pd == 1:
            self.pend.add(cn)
        elif pd == -1:
            self.pend.discard(cn)
        self.p2 += dp2
        self.h = (self.h - 1) & 3 if bit == 1 else (self.h + 1) & 3
        self.c = cn
        self.bits.append(bit)

    def undo(self):
        cp, hp, cu, old, pd, dp2 = self.trail.pop()
        if old == FREE:
            del self.req[cu]
        else:
            self.req[cu] = old
        if pd == 1:
            self.pend.discard(cu)
        elif pd == -1:
            self.pend.add(cu)
        self.p2 -= dp2
        self.c, self.h = cp, hp
        self.bits.pop()


# ---------------- sottoalbero pulito (esaustivo) ----------------

def clean_subtree(word, node_cap=1_000_000, depth_cap=64):
    """Enumera ESAUSTIVAMENTE il sottoalbero dei prepend sopra 'word' potato ai
    nodi con pend2==0, troncando ogni ramo alla PRIMA posa fuori palla
    (foglia-testimone, Dicotomia del Tratto Pulito: profondita' confinata
    <= 10, quindi l'enumerazione esaurisce sempre; i cap sono sole cinture di
    sicurezza e NON dovrebbero mai scattare). Richiede pend2(word)==0.
    Ritorna dict con esaurito, nodi, D, r_max, pose_fuori (foglie-testimoni
    con cheb>BALL_R: ognuna e' un CONTROESEMPIO a v2), primo testimone (bits)."""
    w = Walker(word)
    assert w.p2 == 0, "clean_subtree su nodo sporco"
    nodes = 0; D = 0; rmax = cheb(w.c)
    pose_fuori = []
    witness = None

    def alts():
        out = []
        for bit in w.legal_bits():
            read = 0 if bit == 1 else 1
            cn = w.next_cell()
            if read == 1 and cn not in w.pend and cheb(cn) <= BALL_R:
                continue                     # aprirebbe pend2: fuori dal tratto
            out.append(bit)
        return out

    frames = [alts()]
    while frames:
        if nodes >= node_cap or len(w.bits) >= depth_cap:
            return {"esaurito": False, "nodi": nodes, "D": D, "r_max": rmax,
                    "pose_fuori": [list(p) for p in pose_fuori],
                    "witness": witness}
        a = frames[-1]
        if not a:
            frames.pop()
            if w.bits:
                w.undo()
            continue
        bit = a.pop()
        nodes += 1
        w.apply(bit)
        assert w.p2 == 0, "tratto pulito con pend2>0?!"
        D = max(D, len(w.bits))
        rmax = max(rmax, cheb(w.c))
        if cheb(w.c) > BALL_R:
            # Dicotomia: foglia-testimone — registra e NON ricorrere oltre
            pose_fuori.append(w.c)
            if witness is None:
                witness = to_str(tuple(reversed(w.bits)))
            frames.append([])
            continue
        frames.append(alts())
    return {"esaurito": True, "nodi": nodes, "D": D, "r_max": rmax,
            "pose_fuori": [list(p) for p in pose_fuori], "witness": witness}


# ---------------- scan di un cammino: nodi puliti + lemma ----------------

def scan_path(word_full, word_root, ball_r=BALL_R):
    """Percorre il cammino dal suffisso word_root alla parola intera word_full
    (prepend bit per bit). Ritorna (violazioni_lemma, nodi_puliti, transizioni)
    dove nodi_puliti = lista (j, posa, heading) con pend2==0 al suffisso
    word_full[j:], transizioni = i nodi di pulizia (pend2: 1->0)."""
    nroot = len(word_root)
    assert tuple(word_full[len(word_full) - nroot:]) == tuple(word_root)
    c, h, req = exact_state(word_root)
    pend = pend_set(req)
    p2 = sum(1 for x in pend if cheb(x) <= ball_r)
    viol = []
    clean_nodes = [] if p2 else [(len(word_full) - nroot, c, h)]
    trans = []
    for j in range(len(word_full) - nroot - 1, -1, -1):
        bit = word_full[j]
        cn = (c[0] - DX[h], c[1] - DY[h])
        rb = req.get(cn, FREE)
        read = 0 if bit == 1 else 1
        p2_prev = p2
        if read == 1 and cn not in pend:
            pend.add(cn)
            if cheb(cn) <= ball_r:
                p2 += 1
        elif read == 0 and cn in pend:
            pend.discard(cn)
            if cheb(cn) <= ball_r:
                p2 -= 1
        cn2, hn, _ = exact_step(c, h, req, bit)
        assert cn2 == cn, "cammino non valido"
        c, h = cn2, hn
        if p2 < p2_prev:
            ok = (p2_prev - p2 == 1 and read == 0 and rb == 0
                  and cheb(cn) <= ball_r and c == cn)
            if not ok:
                viol.append((j, c, read, rb))
        if p2 == 0:
            clean_nodes.append((j, c, h))
            if p2_prev > 0:
                trans.append((j, c))
    return viol, clean_nodes, trans


# ---------------- gate G0 ----------------

def gate_G0(counterexamples, w101, fuggenti, rng, n_ext=300):
    """Lemma del passo di pulizia di terra + esca palla-1."""
    total_dec = 0
    paths = []
    for w in counterexamples:
        W = to_bits(w["word"])
        assert valid(W)[1] is None, w["tag"]
        paths.append((w["tag"], W))
    # estensioni casuali sopra fuggenti a caso
    made = 0
    while made < n_ext:
        name, e2 = fuggenti[rng.randrange(len(fuggenti))]
        wk = Walker(e2 + w101)
        for _ in range(rng.randrange(20, 400)):
            lb = wk.legal_bits()
            if not lb:
                break
            wk.apply(lb[rng.randrange(len(lb))])
        if wk.bits:
            paths.append((f"ext:{name}", tuple(reversed(wk.bits)) + e2 + w101))
            made += 1
    viol_tot = 0
    viol_ball1 = 0
    clean_fuori = 0
    for tag, W in paths:
        viol, clean_nodes, trans = scan_path(W, w101)
        viol_tot += len(viol)
        total_dec += len(trans)
        # falsificazione gratis (pannello §95): ogni nodo pulito incontrato
        # nei cammini casuali deve avere posa in palla (lemma + tratto)
        clean_fuori += sum(1 for (_, p, _) in clean_nodes if cheb(p) > BALL_R)
        # esca: claim rafforzato a palla-1 — i decrementi di pend2 con cella
        # chiusa a cheb==2 lo violano
        c, h, req = exact_state(w101)
        pend = pend_set(req)
        p2 = sum(1 for x in pend if cheb(x) <= BALL_R)
        for j in range(len(W) - len(w101) - 1, -1, -1):
            bit = W[j]
            cn = (c[0] - DX[h], c[1] - DY[h])
            read = 0 if bit == 1 else 1
            p2p = p2
            if read == 1 and cn not in pend:
                pend.add(cn)
                if cheb(cn) <= BALL_R:
                    p2 += 1
            elif read == 0 and cn in pend:
                pend.discard(cn)
                if cheb(cn) <= BALL_R:
                    p2 -= 1
            cn2, hn, _ = exact_step(c, h, req, bit)
            c, h = cn2, hn
            if p2 < p2p and cheb(cn) > 1:
                viol_ball1 += 1
    assert viol_tot == 0, f"LEMMA VIOLATO {viol_tot} volte"
    assert clean_fuori == 0, \
        f"nodo pulito con posa FUORI palla nei cammini: v2 FALSIFICATA " \
        f"({clean_fuori} occorrenze)"
    assert total_dec > 0, "gate vacuo: nessun decremento di pend2 osservato"
    assert viol_ball1 > 0, ("esca fallita: il claim palla-1 non trova "
                            "violazioni (checker che non sa fallire)")
    return {"cammini": len(paths), "decrementi": total_dec,
            "viol_lemma": viol_tot, "clean_fuori": clean_fuori,
            "esca_palla1_viol": viol_ball1}


# ---------------- gate G1 ----------------

def gate_G1(w101):
    wit = json.load(open(WIT))
    cen = json.load(open(CEN))
    nominali = []
    for k, w in enumerate(wit["jackpot"]):
        nominali.append((f"jackpot[{k}]", to_bits(w["word"])))
    for k, w in enumerate(wit["nere400"]):
        nominali.append((f"nere400[{k}]", to_bits(w["word"])))
    for k, w in enumerate(cen["fuggenti_dettaglio"]):
        nominali.append((f"census[{k}]", to_bits(w["word_ext"])))
    seen = {}
    fuggenti = []
    dups = 0
    minp2 = 10 ** 9
    rows = []
    for name, e2 in nominali:
        w2 = e2 + w101
        key = tuple(w2)
        if key in seen:
            dups += 1
            continue
        seen[key] = name
        assert valid(w2)[1] is None, name
        c, h, req = exact_state(w2)
        p2 = pend2_of(req)
        minp2 = min(minp2, len(p2))
        rows.append({"nome": name, "posa": list(c), "pend2_n": len(p2)})
        fuggenti.append((name, e2))
    assert minp2 >= 1, "root PULITO trovato: la riduzione perde la gamba G1!"
    # G1b (pannello §95, radicamento a w101): pend2 del nodo-w101 stesso
    cw, hw, reqw = exact_state(w101)
    p2_w101 = pend2_of(reqw)
    assert len(p2_w101) == 6 and p2_w101 == \
        [(-2, 1), (-1, 1), (0, 1), (0, 2), (1, 2), (2, 1)], \
        f"pend2(w101) cambiato: {p2_w101}"
    return {"nominali": len(nominali), "distinte": len(fuggenti),
            "duplicati": dups, "min_pend2_root": minp2,
            "pend2_w101": [list(c) for c in p2_w101], "rows": rows}, fuggenti


# ---------------- gate G2 ----------------

def gate_G2(counterexamples, w101, probe_cap=200_000, probe_depth=400):
    rows = []
    n_clean_nodes = 0
    v2_witness = None
    for w in counterexamples:
        W = to_bits(w["word"])
        viol, clean_nodes, trans = scan_path(W, w101)
        assert not viol
        for (j, posa, h) in clean_nodes:
            n_clean_nodes += 1
            if cheb(posa) > BALL_R:
                # falsificazione di v2 GIA' nel cammino: testimone, non rosso
                v2_witness = {"tag": w["tag"], "j": j,
                              "posa_fuori_nel_cammino": list(posa)}
                print(f"!!! G2: nodo pulito con posa FUORI palla nel cammino "
                      f"{w['tag']} j={j} posa={posa} — v2 FALSIFICATA",
                      flush=True)
            Wj = W[j:]
            # (a) sonda del sottoalbero INTERO (domanda §95.2 originale)
            exh_full, D_full, r_full, nn_full, mp_full = wall_exhaustive(
                Wj, node_cap=probe_cap, depth_cap=probe_depth)
            # (b) sottoalbero PULITO esaustivo (Dicotomia: prima i testimoni,
            # POI l'assert di esaurimento — mai mascherare una falsificazione)
            cs = clean_subtree(Wj)
            if cs["pose_fuori"]:
                v2_witness = {"tag": w["tag"], "j": j, "ext": cs["witness"],
                              "pose": cs["pose_fuori"][:5]}
                print(f"!!! G2: tratto pulito ESCE dalla palla su {w['tag']} "
                      f"j={j}: {cs['pose_fuori'][:3]} — v2 FALSIFICATA",
                      flush=True)
            assert cs["esaurito"], \
                f"sottoalbero pulito NON esaurito su {w['tag']} j={j} " \
                f"(cap di sicurezza: impossibile per Dicotomia senza testimone)"
            rows.append({
                "tag": w["tag"], "j": j, "posa": list(posa),
                "full_esaurito": exh_full, "full_D": D_full,
                "full_r": r_full, "full_nodi": nn_full,
                "clean_nodi": cs["nodi"], "clean_D": cs["D"],
                "clean_r_max": cs["r_max"],
                "clean_pose_fuori": len(cs["pose_fuori"])})
            print(f"  G2 {w['tag']:20s} j={j:4d} posa={posa} | intero: "
                  f"{'ESAURITO' if exh_full else 'VIVO    '} D={D_full:3d} "
                  f"r={r_full:2d} nodi={nn_full:7d} | PULITO: nodi={cs['nodi']} "
                  f"D={cs['D']} r_max={cs['r_max']} "
                  f"pose_fuori={len(cs['pose_fuori'])}", flush=True)
    assert n_clean_nodes > 0, "gate vacuo: nessun nodo pulito nei controesempi"
    return {"rows": rows, "nodi_puliti": n_clean_nodes,
            "v2_witness": v2_witness}


# ---------------- gate G3: cacce multi-politica ----------------

def hunt_job(job):
    """Worker G3. Ritorna nodi di pulizia trovati (parole complete) + esiti
    della caccia diretta al falsificatore. La parola base w2_str e' la radice
    della caccia (fuggente per P1-P3; testimone troncato per P4)."""
    (name, w2_str, policy, seed, restarts, step_budget) = job
    _below_normal()
    rng = random.Random(seed)
    w2 = to_bits(w2_str)
    found = []          # (bits_ext_str, posa, heading)
    far_hits = []       # falsificatore diretto: pend2==0 & cheb>2
    stats = {"passi": 0, "tocchi_pend2_0": 0}

    for rs in range(restarts):
        wk = Walker(w2)
        p_L = rng.choice((0.25, 0.4, 0.55))
        p_steer = rng.choice((0.4, 0.7, 0.9))
        budget = step_budget
        if policy == "P1":            # milestone-greedy: chiudi pend2 uno a uno
            while wk.p2 and budget > 0:
                n_now = wk.p2
                # DFS mirata con backtracking limitato al milestone;
                # cap per-milestone: fallire presto e riparare, non bruciare
                # tutto il budget su un solo milestone
                depth0 = len(wk.bits)
                frames = [order_steer(wk, rng, p_steer)]
                got = False
                ms_budget = min(budget, 40_000)
                while frames and ms_budget > 0:
                    a = frames[-1]
                    if not a:
                        frames.pop()
                        if len(wk.bits) > depth0:
                            wk.undo()
                        continue
                    wk.apply(a.pop())
                    budget -= 1
                    ms_budget -= 1
                    stats["passi"] += 1
                    if wk.p2 < n_now:
                        got = True
                        break
                    frames.append(order_steer(wk, rng, p_steer))
                if not got:
                    break
            if wk.p2 == 0:
                stats["tocchi_pend2_0"] += 1
                found.append((to_str(tuple(reversed(wk.bits))),
                              wk.c, wk.h))
                # da qui: caccia diretta al falsificatore nel sottoalbero
                far = probe_far(wk, rng, min(budget, 30_000), stats)
                far_hits.extend(far)
        elif policy in ("P2", "P4"):  # DFS greedy: priorita' pend2 basso
                                      # (P4 = stessa DFS ma da testimone troncato)
            frames = [order_greedy(wk, rng)]
            while frames and budget > 0:
                a = frames[-1]
                if not a:
                    frames.pop()
                    if wk.bits:
                        wk.undo()
                    continue
                wk.apply(a.pop())
                budget -= 1
                stats["passi"] += 1
                if wk.p2 == 0:
                    stats["tocchi_pend2_0"] += 1
                    found.append((to_str(tuple(reversed(wk.bits))),
                                  wk.c, wk.h))
                    if cheb(wk.c) > BALL_R:
                        far_hits.append((to_str(tuple(reversed(wk.bits))),
                                         wk.c))
                frames.append(order_greedy(wk, rng))
        else:                         # P3: passeggiata profonda randomizzata
            for _ in range(budget):
                lb = wk.legal_bits()
                if not lb:
                    if wk.bits:
                        wk.undo()
                        continue
                    break
                if len(lb) == 2:
                    # steering occasionale verso il pending in palla piu' vicino
                    if wk.p2 and rng.random() < p_steer:
                        bit = steer_bit(wk)
                    else:
                        bit = 1 if rng.random() < p_L else 0
                else:
                    bit = lb[0]
                wk.apply(bit)
                stats["passi"] += 1
                if wk.p2 == 0:
                    stats["tocchi_pend2_0"] += 1
                    found.append((to_str(tuple(reversed(wk.bits))),
                                  wk.c, wk.h))
                    if cheb(wk.c) > BALL_R:
                        far_hits.append((to_str(tuple(reversed(wk.bits))),
                                         wk.c))
                    break
    return {"nome": name, "policy": policy, "base": w2_str, "found": found,
            "far_hits": far_hits, **stats}


def steer_bit(wk):
    cn = wk.next_cell()
    tgt = min((p for p in wk.pend if cheb(p) <= BALL_R),
              key=lambda p: abs(p[0] - cn[0]) + abs(p[1] - cn[1]))
    best = None
    for b in (0, 1):
        hn = (wk.h - 1) & 3 if b == 1 else (wk.h + 1) & 3
        cnn = (cn[0] - DX[hn], cn[1] - DY[hn])
        d = abs(cnn[0] - tgt[0]) + abs(cnn[1] - tgt[1])
        if best is None or d < best[0]:
            best = (d, b)
    return best[1]


def order_steer(wk, rng, p_steer):
    lb = wk.legal_bits()
    if len(lb) < 2:
        return lb
    if wk.p2 and rng.random() < p_steer:
        b = steer_bit(wk)
        return [1 - b, b]                 # migliore per ultimo (pop dal fondo)
    f = rng.randrange(2)
    return [1 - f, f]


def order_greedy(wk, rng):
    """Priorita' (stile lente §94): chiudi pend2 appena puoi; MAI aprire in
    palla se c'e' alternativa; steering verso il pending in palla piu' vicino."""
    lb = wk.legal_bits()
    if len(lb) < 2:
        return lb
    cn = wk.next_cell()
    if cheb(cn) <= BALL_R:
        return [1, 0]          # R provato per primo (chiude o evita apertura)
    if wk.p2:
        b = steer_bit(wk)
        return [1 - b, b]
    f = rng.randrange(2)
    return [1 - f, f]


def probe_far(wk, rng, budget, stats):
    """Dal nodo pulito corrente: caccia il falsificatore (pend2==0 & cheb>2)
    nel sottoalbero INTERO (pend2 puo' oscillare). DFS randomizzata."""
    hits = []
    depth0 = len(wk.bits)
    frames = [order_greedy(wk, rng)]
    while frames and budget > 0:
        a = frames[-1]
        if not a:
            frames.pop()
            if len(wk.bits) > depth0:
                wk.undo()
            continue
        wk.apply(a.pop())
        budget -= 1
        stats["passi"] += 1
        if wk.p2 == 0 and cheb(wk.c) > BALL_R:
            hits.append((to_str(tuple(reversed(wk.bits))), wk.c))
            break
        frames.append(order_greedy(wk, rng))
    while len(wk.bits) > depth0:
        wk.undo()
    return hits


def gate_G3(fuggenti, w101, counterexamples, args, log):
    # firme dei nodi puliti GIA' noti (G2): per contare i NUOVI
    known_sigs = set()
    for w in counterexamples:
        W = to_bits(w["word"])
        _, clean_nodes, _ = scan_path(W, w101)
        for (j, _, _) in clean_nodes:
            c2, h2, req2 = exact_state(W[j:])
            known_sigs.add(state_sig(c2, h2, req2))

    jobs = []
    jid = 0
    for name, e2 in fuggenti:
        w2 = e2 + w101
        for policy in ("P1", "P2", "P3"):
            for j in range(args.jobs_per_cell):
                rs = args.restarts_p1 if policy == "P1" else args.restarts
                bd = args.budget_p1 if policy == "P1" else args.step_budget
                jobs.append((name, to_str(w2), policy,
                             args.seed * 7919 + jid, rs, bd))
                jid += 1
    # P4: mutazione dei testimoni — tronca kb bit antichi e ri-esplora
    for w in counterexamples:
        W = to_bits(w["word"])
        for kb in (10, 20, 40, 80, 160, 320):
            if kb >= len(W) - len(w101):
                continue
            jobs.append((f"P4:{w['tag']}:kb{kb}", to_str(W[kb:]), "P4",
                         args.seed * 7919 + jid, 1, args.step_budget))
            jid += 1
    print(f"G3: {len(fuggenti)} fuggenti x P1-P3 x {args.jobs_per_cell} job "
          f"+ P4 mutazioni = {len(jobs)} job ({args.restarts} restart x "
          f"{args.step_budget} passi)", flush=True)

    clean_states = {}    # sig -> record
    far_witnesses = []
    passi_tot = 0
    per_policy = {"P1": 0, "P2": 0, "P3": 0, "P4": 0}
    with mp.Pool(args.workers, initializer=_below_normal) as pool:
        for r in pool.imap_unordered(hunt_job, jobs, chunksize=1):
            passi_tot += r["passi"]
            base = to_bits(r["base"])
            for (ext_str, posa, h) in r["found"]:
                # verifica di terra del nodo di pulizia + lemma in-run
                Wfull = to_bits(ext_str) + base
                assert valid(Wfull)[1] is None
                c2, h2, req2 = exact_state(Wfull)
                p2 = pend2_of(req2)
                assert p2 == [], f"falso nodo pulito {r['nome']}"
                assert c2 == (tuple(posa) if isinstance(posa, list)
                              else posa), "posa incoerente"
                assert cheb(c2) <= BALL_R, \
                    f"LEMMA VIOLATO IN CACCIA: nodo pulito con posa {c2}"
                sig = state_sig(c2, h2, req2)
                if sig not in clean_states:
                    clean_states[sig] = {
                        "nome": r["nome"], "policy": r["policy"],
                        "posa": list(c2), "heading": h2,
                        "nuovo": sig not in known_sigs,
                        "prof_ext": len(to_bits(ext_str)),
                        "word_full": to_str(Wfull)}
                    per_policy[r["policy"]] += 1
            for (ext_str, posa) in r["far_hits"]:
                # verifica di terra PRIMA di dichiarare la falsificazione
                Wfull = to_bits(ext_str) + base
                assert valid(Wfull)[1] is None, "far-hit non valido?!"
                c2, h2, req2 = exact_state(Wfull)
                assert pend2_of(req2) == [] and cheb(c2) > BALL_R, \
                    f"far-hit smentito di terra: posa={c2}"
                far_witnesses.append({"nome": r["nome"],
                                      "policy": r["policy"],
                                      "ext": ext_str, "posa": list(c2)})
    log.write(f"G3 raw: {len(clean_states)} stati puliti distinti, "
              f"{len(far_witnesses)} far-hit, {passi_tot} passi\n")

    # certificazione: sottoalbero pulito esaustivo per ogni stato trovato
    cert_rows = []
    v2_wit = None
    for sig, rec in clean_states.items():
        cs = clean_subtree(to_bits(rec["word_full"]))
        if cs["pose_fuori"]:
            v2_wit = {**rec, "clean_ext": cs["witness"],
                      "pose": [list(p) for p in cs["pose_fuori"][:5]]}
            print(f"!!! G3: tratto pulito ESCE dalla palla su {rec['nome']} "
                  f"— v2 FALSIFICATA", flush=True)
        assert cs["esaurito"], \
            f"sottoalbero pulito NON esaurito {rec['nome']} " \
            f"(cap di sicurezza: impossibile per Dicotomia senza testimone)"
        cert_rows.append({"nome": rec["nome"], "policy": rec["policy"],
                          "posa": rec["posa"], "heading": rec["heading"],
                          "nuovo": rec["nuovo"],
                          "prof_ext": rec["prof_ext"],
                          "clean_nodi": cs["nodi"], "clean_D": cs["D"],
                          "clean_r_max": cs["r_max"],
                          "pose_fuori": len(cs["pose_fuori"])})
    return {"stati_puliti_distinti": len(clean_states),
            "nuovi": sum(1 for r in cert_rows if r["nuovo"]),
            "per_policy": per_policy,
            "fuggenti_con_pulito": len({r["nome"] for r in cert_rows}),
            "passi_totali": passi_tot,
            "far_witnesses": far_witnesses,
            "v2_witness": v2_wit,
            "cert_rows": cert_rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--jobs-per-cell", type=int, default=2)
    ap.add_argument("--restarts", type=int, default=6)
    ap.add_argument("--restarts-p1", type=int, default=24,
                    help="restart per la P1 (milestone-greedy fallisce presto)")
    ap.add_argument("--budget-p1", type=int, default=50_000)
    ap.add_argument("--step-budget", type=int, default=200_000)
    ap.add_argument("--seed", type=int, default=95)
    ap.add_argument("--min-clean", type=int, default=10)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        args.jobs_per_cell = 1
        args.restarts = 2
        args.step_budget = 30_000
    t0 = time.time()
    rng = random.Random(args.seed)
    log = open(LOG, "a")
    log.write(f"\n==== run {time.strftime('%Y-%m-%d %H:%M:%S')} "
              f"args={vars(args)}\n")

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    cex = json.load(open(CEX))["witnesses"]

    gates = {}
    print("---- GATE G1 (root sporchi) ----", flush=True)
    gates["G1"], fuggenti = gate_G1(w101)
    print(f"G1 verde: {gates['G1']['distinte']} fuggenti distinte "
          f"({gates['G1']['duplicati']} dup), min pend2 root = "
          f"{gates['G1']['min_pend2_root']}; G1b: pend2(w101) = 6 "
          f"(radicamento a w101)", flush=True)
    log.write(f"G1 {json.dumps({k: v for k, v in gates['G1'].items() if k != 'rows'})}\n")

    print("---- GATE G0 (lemma del passo di pulizia) ----", flush=True)
    gates["G0"] = gate_G0(cex, w101, fuggenti, rng)
    print(f"G0 verde: {gates['G0']['cammini']} cammini, "
          f"{gates['G0']['decrementi']} decrementi, 0 violazioni; esca "
          f"palla-1: {gates['G0']['esca_palla1_viol']} violazioni trovate "
          f"(il checker sa fallire)", flush=True)
    log.write(f"G0 {json.dumps(gates['G0'])}\n")

    print("---- GATE G2 (tratti puliti sui controesempi) ----", flush=True)
    gates["G2"] = gate_G2(cex, w101)
    if gates["G2"]["v2_witness"]:
        print(f"!!! G2: TESTIMONE clean-far — v2 FALSIFICATA: "
              f"{gates['G2']['v2_witness']}", flush=True)
    else:
        print(f"G2 verde: {gates['G2']['nodi_puliti']} nodi puliti, tutti con "
              f"tratto in palla", flush=True)
    log.write(f"G2 {json.dumps(gates['G2'])}\n")

    print("---- GATE G3 (cacce multi-politica) ----", flush=True)
    gates["G3"] = gate_G3(fuggenti, w101, cex, args, log)
    g3 = gates["G3"]
    if g3["v2_witness"] or g3["far_witnesses"]:
        print(f"!!! G3: v2 FALSIFICATA — testimoni: "
              f"{g3['v2_witness'] or g3['far_witnesses'][:3]}", flush=True)
    print(f"G3: {g3['stati_puliti_distinti']} stati di pulizia distinti "
          f"({g3['nuovi']} NUOVI; per policy {g3['per_policy']}), "
          f"{g3['fuggenti_con_pulito']} basi coperte, {g3['passi_totali']} "
          f"passi; far diretti: {len(g3['far_witnesses'])}", flush=True)

    print("---- GATE G4 (soglie) ----", flush=True)
    ok_pol = sum(1 for v in g3["per_policy"].values() if v > 0)
    assert g3["stati_puliti_distinti"] >= args.min_clean, \
        f"G4 ROSSO: {g3['stati_puliti_distinti']} < {args.min_clean} stati"
    assert g3["nuovi"] >= 2, f"G4 ROSSO: solo {g3['nuovi']} stati NUOVI"
    assert ok_pol >= 2, f"G4 ROSSO: solo {ok_pol} politiche produttive"
    print(f"G4 verde: {g3['stati_puliti_distinti']} >= {args.min_clean} stati "
          f"({g3['nuovi']} nuovi), {ok_pol} politiche produttive", flush=True)

    verdict = ("V2-FALSIFICATA" if (gates["G2"]["v2_witness"]
               or g3["v2_witness"] or g3["far_witnesses"])
               else "TRATTO-PULITO-IN-PALLA (sui nodi di pulizia raggiunti: "
                    "controesempi §94 + cacce G3 — v2 resta congettura "
                    "empirica, trappola hh)")
    out = {"args": vars(args), "gates": {
               "G0": gates["G0"],
               "G1": {k: v for k, v in gates["G1"].items() if k != "rows"},
               "G2": gates["G2"], "G3": g3},
           "verdetto": verdict,
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    log.write(f"done in {out['elapsed_s']}s verdetto={verdict}\n")
    log.close()
    print(f"\nVERDETTO: {verdict}. scritto {OUT_JSON} in "
          f"{out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
