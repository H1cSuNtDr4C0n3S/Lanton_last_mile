# u2_pocket_certificate.py — §92: la macchina esatta-in-striscia per U2-NERO,
# i suoi gate, e la FALSIFICAZIONE del bound "coprente-nera => D <= 4".
#
# STORIA (onesta). Il progetto §91b prevedeva un certificato finito alla-HALO:
# analisi esatta-in-striscia sulla tasca (15 celle), partenza = coperture-nere
# ammissibili, uscita = sopravvivenza. La macchina e' stata costruita e validata
# (gate 0-4 verdi, replay bit-identico dei 60 muri §90c). Esito:
#   1. il certificato NON chiude sulla striscia CORE: 18.402/47.312 coperture
#      astratte FUGGONO (verso riga 3 e fianchi); l'astrazione OUT e' troppo
#      generosa (round-trip rientro-flip-uscita scramblano le parita' del bordo);
#   2. l'attacco empirico (campagna 12 worker) ha FALSIFICATO il bound del
#      censimento §90c: la scala reale dei muri e' D = 0 / 4 / 8 / 12 / 48 / 56
#      (testimoni in u2_cover_witnesses.json). Il campione best-first di §90c
#      (30 nere, D<=4) era survivorship della porta piu' vicina;
#   3. una configurazione-FUGA e' REALIZZATA da coprenti reali (2 testimoni,
#      D=48 e 56): il muro esce dalla tasca, serpeggia nel footprint di w101
#      fino alla riga 6 (su 7) e muore sul muro dei record a (-5,1). Il campo
#      di w101 instrada il fuggitivo: mai raggiunto il territorio vergine
#      (dove D=infinito sarebbe automatico, come la rotaia sigma di §88).
#
# COSA RESTA VERO E CERTIFICATO (fatti meccanici di questo script):
#   T1. h1=2 => D=0: il primo prepend sopra la copertura cade su (1,0), y=0
#       (geometria pura, nessuna ipotesi di campo).
#   T2. ZERO CICLI in-tasca: nessuna copertura astratta (=> nessuna reale)
#       sopravvive DENTRO la striscia CORE; sopravvivere = uscirne.
#   T3. Ogni muro reale le cui CELLE restano tutte in S_CORE ha D <= 33 (max tra
#       le 28.910 coperture astratte morenti). Poggia sul LEMMA DI SOVRA-
#       APPROSSIMAZIONE (deduttivo, pannello §92): ogni transizione reale
#       soddisfa le condizioni di in_succ/out_succ — la regola della cella-
#       giovane e' NECESSARIA (la cella del passo piu' recente e' un passo del
#       cammino: fuori S e a y>=1) — e req|S e' congelato durante il
#       vagabondaggio fuori striscia (le visite esterne non toccano celle di S).
#       Su una copertura confinata il verdetto astratto E' il muro reale
#       (verificato: testimoni D=4/8/12 hanno verdetto astratto identico).
#       NB: confinamento = celle del muro in S_CORE, NON riga_max <= 2
#       ((3,2) e (-5,2) hanno y=2 ma stanno fuori da S_CORE).
#   T4. Corridoio h1=0: req(2,1)=B alla copertura e' FORZATO (il bit L del passo
#       di corridoio manderebbe la cella-giovane a (2,0), y=0).
#
# LA MACCHINA (frame anchor, record in origine heading su; parole = ext+w101).
#   Camminatore all'indietro: stato = (cella del passo piu' antico, heading
#   pre-svolta, requisiti sulle celle della striscia S). Fatti meccanici (GATE 0):
#     - prepend del bit b: nuova cella c' = c - D[h] (INDIPENDENTE da b);
#     - heading pre-svolta del nuovo passo: R -> h-1, L -> h+1 (mod 4);
#     - il bit dichiara il colore LETTO (R=bianco, L=nero); su cella vincolata
#       la lettura e' forzata dall'alternanza: req(c) = flip(prima-lettura
#       corrente); dopo la visita req(c) = flip(colore letto);
#     - validita' = realizzabilita' (req) + record-compat (ogni cella y>=1).
#   FASE 1 (pre-copertura): fixpoint dalla coda di w101, esatto in S, OUT fuori
#     (rientro su qualunque cella di S, vincolo cella-giovane fuori-S e y>=1).
#     Sovra-approssima OGNI estensione valida (GATE 4). Prima visita a (1,1) =
#     copertura: bit R -> NERA, bit L -> BIANCA.
#   FASE 2 (muro post-copertura): esatta-in-S; y<1 = morte; uscita da S = FUGA
#     (sopravvivenza concessa); ciclo = sopravvivenza. Verdetto per copertura.
#
# GATE (fermarsi al primo rosso):
#   0 formula del passo all'indietro vs tail_cell/valid su parole casuali;
#   1 lemma del suffisso (ogni suffisso di parola valida e' valido);
#   2 replay esatto dei 60 coprenti §90c: muro bit-identico a valid() e al JSON;
#   3 membership: i 60 stati di copertura reali nel raggiungibile di fase 1;
#   4 ammissione: estensioni casuali LUNGHE (<=320 passi, steering sul bordo)
#     -> traccia astratta ammessa; ASSERISCE soglie minime (>=500 rientri
#     OUT->IN, >=50 coperture) — riparato dal pannello §92: la v1 (<=39 passi)
#     non toccava mai la striscia ed era vacua;
#   5 testimoni: le coprenti di u2_cover_witnesses.json riprodotte (replay,
#     membership, D del muro, confinamento esplicito; jackpot = config-FUGA
#     realizzata; confinati => verdetto astratto == D reale).
#
# NOTA MEMORIA (trappola g): fase 1 CORE = ~1.2M stati (ok). La striscia WIDE
# supera i 30M stati in Python (>10 GB, OOM su 16 GB): NON eseguirla in Python;
# se serve, motore C con tabella hash a dimensione fissa. Default: solo CORE.
#
# Uscita: alpha1/u2_pocket_certificate_summary.json
import sys, os, json, time, heapq, random, argparse
from collections import deque, Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY, rotk
from kwindow_spoiler_census import virtual_walk
from record_weapon_vitality import to_bits, to_str, SUMMARY
from u2_cover_rail_map import valid, tail_cell

HERE = os.path.dirname(os.path.abspath(__file__))
CC = os.path.join(HERE, "record_cover_census_summary.json")
RAIL = os.path.join(HERE, "u2_cover_rail_map_summary.json")
WIT = os.path.join(HERE, "u2_cover_witnesses.json")
OUT_JSON = os.path.join(HERE, "u2_pocket_certificate_summary.json")
TGT = (1, 1)
FREE = 2                              # req: 0 = prossima-lettura-bianca, 1 = -nera, 2 = libera

# Striscia CORE: unione misurata §91b (15 celle, coordinate ASSOLUTE anchor) + (1,1).
S_CORE = [(-5, 1), (-4, 1), (-4, 2), (-3, 1), (-3, 2), (-2, 1), (-2, 2), (-1, 1),
          (-1, 2), (0, 1), (0, 2), (1, 1), (1, 2), (2, 1), (2, 2), (3, 1)]
# Striscia WIDE: definita per riferimento; in Python ESPLODE (vedi nota memoria).
S_WIDE = [(x, 1) for x in range(-7, 6)] + [(x, 2) for x in range(-7, 6)] + \
         [(x, 3) for x in range(-6, 5)]


# ---------------- ingredienti esatti (frame anchor) ----------------

def anchor_trace(word):
    """(posizioni dei passi, heading pre-svolta dei passi, prime letture per cella,
    rotazione k) in frame anchor; None se irrealizzabile."""
    g, pose = virtual_walk(word)
    if g is None:
        return None
    pos = []; hpre = []; fr = {}
    x = y = 0; h = 0
    for b in word:
        c = (x, y)
        pos.append(c); hpre.append(h)
        if c not in fr:
            fr[c] = 0 if b == 1 else 1          # R legge bianco(0), L nero(1)
        if b:
            h = (h + 1) & 3
        else:
            h = (h + 3) & 3
        x += DX[h]; y += DY[h]
    k = (-h) % 4
    A = lambda c: rotk((c[0] - x, c[1] - y), k)
    return ([A(c) for c in pos], [(hh + k) % 4 for hh in hpre],
            {A(c): g0 for c, g0 in fr.items()}, k)


def exact_state(word):
    """Stato esatto del camminatore all'indietro sopra 'word' (valida):
    (cella coda, heading pre-svolta coda, req: cella -> colore da leggere)."""
    tr = anchor_trace(word)
    assert tr is not None
    pos, hpre, fr, _ = tr
    req = {c: 1 - g for c, g in fr.items()}
    return pos[0], hpre[0], req


def exact_step(c, h, req, bit):
    """Un prepend esatto (nessuna striscia). Ritorna (c', h', None) se valido
    (req aggiornato IN PLACE), oppure (None, causa, None)."""
    cn = (c[0] - DX[h], c[1] - DY[h])
    if cn[1] < 1:
        return None, "y<1", None
    read = 0 if bit == 1 else 1
    r = req.get(cn, FREE)
    if r != FREE and r != read:
        return None, "irrealizzabile", None
    req[cn] = 1 - read
    hn = (h - 1) & 3 if bit == 1 else (h + 1) & 3
    return cn, hn, None


def exact_wall(word, depth_cap=30):
    """Muro esaustivo per livelli (solo per muri PICCOLI: censimento §90c).
    Ritorna (counts per livello, morti per causa)."""
    c0, h0, req0 = exact_state(word)
    level = [(c0, h0, req0)]
    counts = []; deaths = {"irrealizzabile": 0, "y<1": 0}
    dep = 0
    while level and dep < depth_cap:
        dep += 1
        nxt = []
        for (c, h, req) in level:
            for bit in (0, 1):
                r2 = dict(req)
                cn, hn, _ = exact_step(c, h, r2, bit)
                if cn is None:
                    deaths[hn] += 1
                    continue
                nxt.append((cn, hn, r2))
        counts.append(len(nxt))
        level = nxt
    return counts, deaths


def wall_depth(word, node_cap=500_000, depth_cap=400, strip=None):
    """DFS a budget, MEMORY-SAFE (niente liste di livelli): ritorna
    (D = prof. massima, riga massima, esaurito?, confinato-in-strip?).
    NB (pannello §92): il confinamento va letto sulle CELLE del muro, non sulla
    riga massima — (3,2) e (-5,2) hanno y=2 ma stanno fuori da S_CORE."""
    c0, h0, req0 = exact_state(word)
    maxdep = 0; maxy = 1; nodes = 0; exhausted = False
    confined = True
    stack = [(c0, h0, req0, 0)]
    while stack:
        if nodes >= node_cap:
            exhausted = True
            break
        c, h, req, dep = stack.pop()
        if dep >= depth_cap:
            exhausted = True
            continue
        for bit in (0, 1):
            nodes += 1
            r2 = dict(req)
            cn, hn, _ = exact_step(c, h, r2, bit)
            if cn is None:
                continue
            maxdep = max(maxdep, dep + 1)
            maxy = max(maxy, cn[1])
            if strip is not None and cn not in strip:
                confined = False
            stack.append((cn, hn, r2, dep + 1))
    return maxdep, maxy, exhausted, confined


def step_ok(c, h, req, bit):
    """Validita' di un prepend SENZA mutare req (peek O(1))."""
    cn = (c[0] - DX[h], c[1] - DY[h])
    if cn[1] < 1:
        return False
    r = req.get(cn, FREE)
    return r == FREE or r == (0 if bit == 1 else 1)


# ---------------- la macchina astratta (esatta-in-S, OUT fuori) ----------------

class Machine:
    def __init__(self, strip):
        self.S = list(strip)
        self.idx = {c: i for i, c in enumerate(self.S)}
        assert TGT in self.idx
        self.ti = self.idx[TGT]

    def w101_start(self, w101):
        """Stato iniziale di fase 1: coda di w101 + req di w101 ristretti a S."""
        c0, h0, req = exact_state(w101)
        rt = tuple(req.get(c, FREE) for c in self.S)
        assert rt[self.ti] == FREE, "(1,1) deve essere fuori dal footprint di w101"
        if c0 in self.idx:
            return ("I", self.idx[c0], h0, rt)
        return ("O", rt)

    def project(self, c, h, req):
        rt = tuple(req.get(cc, FREE) for cc in self.S)
        if c in self.idx:
            return ("I", self.idx[c], h, rt)
        return ("O", rt)

    def in_succ(self, ci, h, rt, phase1):
        """Successori di uno stato IN. Ritorna (stati, coperture, fughe)."""
        c = self.S[ci]
        cn = (c[0] - DX[h], c[1] - DY[h])
        succ = []; covers = []; escapes = []
        if cn == TGT and phase1:
            assert rt[self.ti] == FREE
            for bit in (0, 1):
                read = 0 if bit == 1 else 1
                r2 = list(rt); r2[self.ti] = 1 - read
                covers.append((bit, (h - 1) & 3 if bit == 1 else (h + 1) & 3,
                               tuple(r2)))
            return succ, covers, escapes
        if cn in self.idx:
            j = self.idx[cn]
            for bit in (0, 1):
                read = 0 if bit == 1 else 1
                if rt[j] != FREE and rt[j] != read:
                    continue
                r2 = list(rt); r2[j] = 1 - read
                hn = (h - 1) & 3 if bit == 1 else (h + 1) & 3
                succ.append(("I", j, hn, tuple(r2)))
            return succ, covers, escapes
        if cn[1] < 1:
            return succ, covers, escapes           # morte (nessun successore)
        if phase1:
            succ.append(("O", rt))                 # esce dalla striscia
        else:
            escapes.append(cn)                     # FUGA in fase 2
        return succ, covers, escapes

    def out_succ(self, rt):
        """Rientri da OUT: qualunque cella di S, qualunque heading pre-svolta,
        bit vincolato da req; regola della cella-giovane (fuori S, y>=1)."""
        succ = []
        for j, ce in enumerate(self.S):
            for he in range(4):
                for bit in (0, 1):
                    hp = (he + 1) & 3 if bit == 1 else (he - 1) & 3
                    yc = (ce[0] + DX[hp], ce[1] + DY[hp])
                    if yc in self.idx or yc[1] < 1:
                        continue
                    read = 0 if bit == 1 else 1
                    if rt[j] != FREE and rt[j] != read:
                        continue
                    if ce == TGT:
                        raise AssertionError(
                            "ingresso da OUT su (1,1): striscia troppo piccola")
                    r2 = list(rt); r2[j] = 1 - read
                    succ.append(("I", j, he, tuple(r2)))
        return succ

    def phase1(self, start, state_cap=6_000_000):
        """Fixpoint di raggiungibilita' pre-copertura (BFS). Il cap protegge la
        memoria (trappola g): con tuple Python ~1M stati ~ 1 GB."""
        seen = {start}
        q = deque([start])
        cov_n = set(); cov_b = set()
        while q:
            st = q.popleft()
            if st[0] == "I":
                succ, covers, _ = self.in_succ(st[1], st[2], st[3], True)
                for bit, h1, rt2 in covers:
                    (cov_n if bit == 1 else cov_b).add((h1, rt2))
            else:
                succ = self.out_succ(st[1])
            for s2 in succ:
                if s2 not in seen:
                    if len(seen) >= state_cap:
                        raise RuntimeError("fase 1: cap stati superato — "
                                           "striscia troppo grande per Python")
                    seen.add(s2)
                    q.append(s2)
        return seen, cov_n, cov_b

    def phase2_profile(self, covers):
        """Verdetto esatto-in-S per ogni copertura: ('D', depth) | ('F', cella)
        | ('C',) [ciclo]. Memo globale condiviso."""
        memo = {}
        GRAY = ("G",)

        def rec(ci, h, rt):
            key = (ci, h, rt)
            v = memo.get(key)
            if v is GRAY:
                return ("C",)
            if v is not None:
                return v
            memo[key] = GRAY
            succ, _, esc = self.in_succ(ci, h, rt, False)
            if esc:
                memo[key] = ("F", esc[0])
                return memo[key]
            best = 0
            for (_, j2, h2, rt2) in succ:
                r = rec(j2, h2, rt2)
                if r[0] != "D":
                    memo[key] = r
                    return r
                best = max(best, 1 + r[1])
            memo[key] = ("D", best)
            return memo[key]

        out = {}
        for (h1, rt) in covers:
            out[(h1, rt)] = rec(self.ti, h1, rt)
        return out, memo


# ---------------- gate ----------------

def random_valid_ext(w101, rng, max_len):
    ext = ()
    for _ in range(max_len):
        bit = rng.randrange(2)
        if valid((bit,) + ext + w101)[1] is None:
            ext = (bit,) + ext
        elif valid((1 - bit,) + ext + w101)[1] is None:
            ext = (1 - bit,) + ext
        else:
            break
    return ext


def gate0(w101, rng, trials=1500):
    """Formula del passo all'indietro vs tail_cell/valid (verita' di terra)."""
    tested = 0
    for _ in range(trials):
        w = random_valid_ext(w101, rng, rng.randrange(0, 12)) + w101
        if valid(w)[1] is not None:
            continue
        tr = anchor_trace(w)
        pos, hpre = tr[0], tr[1]
        for bit in (0, 1):
            w2 = (bit,) + w
            pred = (pos[0][0] - DX[hpre[0]], pos[0][1] - DY[hpre[0]])
            assert tail_cell(w2) == pred
            ok_true = valid(w2)[1] is None
            c, h, req = exact_state(w)
            cn, hn, _ = exact_step(c, h, req, bit)
            assert ok_true == (cn is not None)
            if ok_true:
                tr2 = anchor_trace(w2)
                assert tr2[0][0] == cn and tr2[1][0] == hn
                assert tr2[0][1:] == pos and tr2[1][1:] == hpre
        tested += 1
    return tested


def gate1(w101, rng, trials=400):
    """Lemma del suffisso: ogni suffisso di una parola valida e' valido."""
    checked = 0
    for _ in range(trials):
        w = random_valid_ext(w101, rng, rng.randrange(0, 25)) + w101
        if valid(w)[1] is not None:
            continue
        for cut in range(1, len(w)):
            assert valid(w[cut:])[1] is None, ("suffisso non valido!", cut)
            checked += 1
    return checked


def replay_extension(w101, e2, machine, seen):
    """Replay esatto dell'estensione e2 (ordine parola). Verifica che ogni stato
    proiettato sia in 'seen'. Ritorna (h1, req_su_S alla copertura, colore)."""
    c, h, req = exact_state(w101)
    assert machine.project(c, h, req) in seen
    for i in range(len(e2) - 1, -1, -1):
        bit = e2[i]
        cn, hn, _ = exact_step(c, h, req, bit)
        assert cn is not None, f"replay: bit {i} invalido"
        if cn == TGT:
            assert i == 0, "visita a (1,1) prima della copertura"
            read = 0 if bit == 1 else 1
            rt = tuple((1 - read) if cc == TGT else req.get(cc, FREE)
                       for cc in machine.S)
            h1 = (h - 1) & 3 if bit == 1 else (h + 1) & 3
            return h1, rt, ("B" if read == 0 else "W")
        c, h = cn, hn
        assert machine.project(c, h, req) in seen, f"stato fuori raggiungibile ({i})"
    raise AssertionError("estensione senza copertura")


def gate4(w101, machine, seen, cov_n, cov_b, rng, trials=2500, max_len=320,
          min_reentries=500, min_covers=50):
    """Estensioni valide casuali LUNGHE con steering verso la tasca: ogni prefisso
    proiettato deve essere ammesso/visto; ogni copertura nei cover-set.
    RIPARATO dal pannello §92 (BUCO G4): la versione originale usava camminate
    <=39 passi che non toccavano MAI la striscia (0 rientri: gate vacuo). Ora il
    gate ASSERISCE soglie minime di copertura del test (rientri OUT->IN e
    coperture raggiunte): un gate deve poter fallire."""
    admitted = 0; covers_hit = 0; reentries = 0; exits = 0
    for _ in range(trials):
        c, h, req = exact_state(w101)
        inside = c in machine.idx
        for _ in range(max_len):
            bits = [b for b in (0, 1) if step_ok(c, h, req, b)]
            if not bits:
                break
            if len(bits) == 2 and rng.random() < 0.7:
                # steering: preferisci il bit che tiene la cella dopo-la-prossima
                # vicina alla tasca (la prossima cella e' bit-indipendente)
                def score(b):
                    hn = (h - 1) & 3 if b == 1 else (h + 1) & 3
                    cn = (c[0] - DX[h], c[1] - DY[h])
                    cnn = (cn[0] - DX[hn], cn[1] - DY[hn])
                    return abs(cnn[0]) + abs(cnn[1] - 1)
                bits.sort(key=score)
                bit = bits[0]
            else:
                bit = rng.choice(bits)
            cn, hn, _ = exact_step(c, h, req, bit)
            if cn == TGT:
                read = 0 if bit == 1 else 1
                rt = tuple((1 - read) if cc == TGT else req.get(cc, FREE)
                           for cc in machine.S)
                h1 = (h - 1) & 3 if bit == 1 else (h + 1) & 3
                assert (h1, rt) in (cov_n if bit == 1 else cov_b), \
                    "copertura casuale fuori dai cover-set!"
                covers_hit += 1
                break
            c, h = cn, hn
            now_inside = c in machine.idx
            if now_inside and not inside:
                reentries += 1
            if inside and not now_inside:
                exits += 1
            inside = now_inside
            assert machine.project(c, h, req) in seen, "stato fuori raggiungibile!"
            admitted += 1
    assert reentries >= min_reentries, f"gate 4 sotto-copertura: {reentries} rientri"
    assert covers_hit >= min_covers, f"gate 4 sotto-copertura: {covers_hit} coperture"
    return admitted, covers_hit, reentries, exits


# ---------------- main ----------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=92)
    ap.add_argument("--skip-slow-gates", action="store_true",
                    help="salta gate 0/1/4 (solo per iterazioni rapide)")
    args = ap.parse_args()
    t0 = time.time()
    rng = random.Random(args.seed)

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    cc = json.load(open(CC))
    rail = json.load(open(RAIL))

    gates = {}
    if not args.skip_slow_gates:
        gates["g0_parole"] = gate0(w101, rng)
        print(f"GATE 0 verde: formula del passo all'indietro su "
              f"{gates['g0_parole']} parole (2 bit ciascuna)", flush=True)
        gates["g1_suffissi"] = gate1(w101, rng)
        print(f"GATE 1 verde: lemma del suffisso su {gates['g1_suffissi']} suffissi",
              flush=True)

    # ---------- GATE 2: replay esatto dei 60 coprenti §90c ----------
    for r_cc, r_rail in zip(cc["rows"], rail["rows"]):
        assert r_cc["depth"] == r_rail["depth"] and r_cc["colore_11"] == r_rail["colore_11"]
        w2 = to_bits(r_cc["word_ext"]) + w101
        counts, deaths = exact_wall(w2)
        assert counts == r_rail["wall"] and deaths == r_rail["deaths"], r_cc["depth"]
    gates["g2_muri"] = 60
    print("GATE 2 verde: 60/60 muri §90c bit-identici (esatto == valid() == JSON)",
          flush=True)

    # ---------- FASE 1 (CORE) ----------
    M = Machine(S_CORE)
    t1 = time.time()
    seen, cov_n, cov_b = M.phase1(M.w101_start(w101))
    h1_n = sorted(set(h for h, _ in cov_n))
    print(f"\nFASE 1 (CORE, {len(S_CORE)} celle): {len(seen)} stati "
          f"({round(time.time()-t1,1)}s); coperture NERE {len(cov_n)} (h1 {h1_n}), "
          f"BIANCHE {len(cov_b)}", flush=True)

    # ---------- FASE 2: profilo dei verdetti ----------
    verd_n, memo = M.phase2_profile(cov_n)
    dieD = Counter(); fuga = Counter(); h1_die = Counter(); h1_fuga = Counter()
    cicli = 0
    for (h1, rt), r in verd_n.items():
        if r[0] == "D":
            dieD[r[1]] += 1; h1_die[h1] += 1
        elif r[0] == "F":
            fuga[r[1]] += 1; h1_fuga[h1] += 1
        else:
            cicli += 1
    assert cicli == 0, "ciclo in-tasca trovato: T2 cade!"
    max_die = max(dieD) if dieD else None
    print(f"FASE 2 NERA: morenti {sum(dieD.values())} (D max {max_die}, "
          f"distr. {dict(sorted(dieD.items()))}), FUGGENTI {sum(fuga.values())} "
          f"(h1 {dict(h1_fuga)}), cicli 0", flush=True)
    print(f"  celle di fuga: {dict(sorted(fuga.items(), key=lambda kv: -kv[1]))}",
          flush=True)
    verd_b, _ = M.phase2_profile(cov_b)
    dieD_b = Counter(v[1] for v in verd_b.values() if v[0] == "D")
    fuga_b = sum(1 for v in verd_b.values() if v[0] == "F")
    print(f"FASE 2 BIANCA (bonus): morenti {sum(dieD_b.values())} "
          f"(D max {max(dieD_b) if dieD_b else None}), fuggenti {fuga_b}", flush=True)

    # ---------- GATE 3: membership dei 60 stati di copertura reali ----------
    for r_cc in cc["rows"]:
        h1, rt, col = replay_extension(w101, to_bits(r_cc["word_ext"]), M, seen)
        assert col == r_cc["colore_11"]
        assert (h1, rt) in (cov_n if col == "B" else cov_b)
    gates["g3_membership"] = 60
    print("GATE 3 verde: 60/60 coperture reali nel raggiungibile di fase 1",
          flush=True)

    if not args.skip_slow_gates:
        adm, chit, reen, exi = gate4(w101, M, seen, cov_n, cov_b, rng)
        gates["g4_ammessi"] = adm
        gates["g4_rientri"] = reen
        gates["g4_coperture"] = chit
        print(f"GATE 4 verde: {adm} stati casuali ammessi, {reen} rientri OUT->IN, "
              f"{exi} uscite, {chit} coperture nei cover-set (soglie: >=500 rientri, "
              f">=50 coperture)", flush=True)

    # ---------- GATE 5: testimoni della falsificazione ----------
    wit = json.load(open(WIT))
    wrows = []
    core_set = set(S_CORE)
    for grp in ("jackpot", "D12", "D8", "D4"):
        for w in wit[grp]:
            e2 = to_bits(w["word"])
            h1, rt, col = replay_extension(w101, e2, M, seen)
            assert col == "B"
            assert (h1, rt) in cov_n, "testimone fuori dal cover-set!"
            D, maxy, exh, conf = wall_depth(e2 + w101, strip=core_set)
            assert not exh, "budget muro esaurito sul testimone"
            assert D == w["D"], (w["D"], D)
            av = verd_n[(h1, rt)]
            if grp == "jackpot":
                assert av[0] == "F", "il jackpot deve essere config-FUGA"
                assert not conf and maxy == 6
            else:
                # confinamento esplicito (celle del muro tutte in S_CORE), non riga_max
                assert conf and av == ("D", D), \
                    "testimone confinato deve avere verdetto astratto esatto"
            wrows.append({"grp": grp, "prof": len(e2), "h1": h1, "D": D,
                          "riga_max": maxy, "confinato_core": conf,
                          "verdetto_astratto": list(av)})
            print(f"GATE 5: testimone {grp} prof.{len(e2)} h1={h1} D={D} "
                  f"riga_max={maxy} confinato={conf} astratto={av}", flush=True)
    gates["g5_testimoni"] = len(wrows)

    # ---------- verdetto ----------
    print("\n================ VERDETTO §92 ================", flush=True)
    print("U2-NERO nella forma §90c/§91b ('coprente-nera => D <= 4') e' FALSO:", flush=True)
    print(f"  scala reale dei muri D = {wit['counts_D']} (testimoni verificati)", flush=True)
    print("Fatti certificati: T1 h1=2 => D=0 (geometria); T2 zero cicli in-tasca;", flush=True)
    print(f"  T3 muro confinato in CORE => D <= {max_die}; T4 req(2,1)=B forzato a h1=0.", flush=True)
    print("Il certificato a striscia NON chiude: le config-FUGA sono realizzabili;", flush=True)
    print("  34 coprenti-nere hanno muri D>=400 fino alla riga 33 (vergine), e", flush=True)
    print("  u2_infinite_rail.py certifica un testimone con D = INFINITO.", flush=True)
    print("=> sup D = infinito: la vitalita' D e' l'invariante SBAGLIATO. La rotaia", flush=True)
    print("  paga ~1 nero FRESCO (= cella di seme) a coppia: lontano dal seme una", flush=True)
    print("  prima-visita-della-vita legge bianco (R forzato) e il muro e' una corsa", flush=True)
    print("  inversa quasi-deterministica con debiti di rivisita (L-su-fresco).", flush=True)
    print("  Oggetto per §93: bilancio dei neri freschi / corsa inversa forzata.", flush=True)

    out = {"args": vars(args), "gates": gates,
           "fase1": {"stati": len(seen), "cov_nere": len(cov_n),
                     "cov_bianche": len(cov_b), "h1_nere": h1_n},
           "fase2_nera": {"morenti": sum(dieD.values()),
                          "D_distr": {str(k): v for k, v in sorted(dieD.items())},
                          "D_max_confinato": max_die,
                          "fuggenti": sum(fuga.values()),
                          "celle_fuga": {str(k): v for k, v in fuga.items()},
                          "cicli": cicli},
           "fase2_bianca": {"morenti": sum(dieD_b.values()),
                            "D_max_confinato": max(dieD_b) if dieD_b else None,
                            "fuggenti": fuga_b},
           "testimoni": wrows,
           "scala_D_reale": wit["counts_D"],
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nscritto {OUT_JSON} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
