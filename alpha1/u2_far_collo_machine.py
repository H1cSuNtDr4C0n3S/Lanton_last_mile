# u2_far_collo_machine.py — §97: la MACCHINA DEL COLLO (gambe a+b di §96g.1).
#
# BERSAGLIO (Teorema del Collo, forma sufficiente): nessun nodo di pulizia
# raggiungibile ha una delle 8 firme-exit residue dell'oracolo v2 (§96).
# Se vero: v2 = TEOREMA (§96b) e il Muro (corno 3b) si chiude senza pavimento.
# NON serve l'unicita' della firma reale ((-1,2),3): basta
# raggiungibili ∩ {8 residue} = ∅.
#
# MODELLO (esatto-in-zona / OUT-libero, zona = cheb <= R, y in [1, R]):
#   stato = (req delle celle di zona ∈ {FREE,0,1}^|zona|, loc ∈ {OUT} ∪
#            {(cella di zona, heading)}), int-packed.
#   - IN ZONA la dinamica del camminatore all'indietro e' ESATTA: cn =
#     posa - D[h] forzata, lettura forzata da req(cn) (branch se FREE),
#     ledger flippa req(cn), lettera fissa h' (R: h-1, L: h+1). Su una cella
#     visitata non-pending la lettura forzata e' L = riapertura: il
#     whack-a-mole e' nel modello per costruzione.
#   - FUORI si sovra-approssima: rientro da qualsiasi cella di zona leggibile
#     da una posa esterna con y>=1, heading libero; req fuori zona dimenticate.
#   L'astrazione ALLARGA le traiettorie reali => se nemmeno la macchina
#   raggiunge una firma, NESSUN passato reale la realizza (kill = teorema);
#   le firme raggiunte in piu' sono inconcludenti (trappole z/ff).
#
# ESITO RADIUS 2 (§97, prima corsa — INCONCLUDENTE e istruttivo): con la sola
# palla esatta la macchina raggiunge 24 firme (TUTTE le 8 residue) e le firme
# risultano INSENSIBILI ai flip dello stato iniziale (OSSERVAZIONE, pannello
# §97 B4: testata su tutti i flip singoli e sulle coppie — vedi campo
# washout_radius2 del summary; NON un "fatto di totalita'", e il meccanismo
# NON e' il solo rientro diretto: (−1,1),(0,1),(1,1) non hanno pose esterne
# adiacenti con y>=1 e sono riconfigurabili solo via cammino in-zona).
#
# VINCOLI DI SOUNDNESS (pannello §97, B1/B2 — bloccanti per il riuso):
#  - l'init loc=OUT e' sound SOLO se la posa di continuazione di w101
#    (cw=(4,1), cheb 4) e' FUORI zona: assert cheb(cw) > R (a R>=4 la
#    macchina cosi' com'e' sarebbe UNSOUND: servirebbe init loc=(cw,hw) e
#    build_init generalizzato alle celle non visitate da w101);
#  - i confronti differenziali K1/K2 sono DEFINITI solo tra esplorazioni
#    ESAUSTIVE: sotto cap, due BFS con frontiere diverse danno prefissi
#    diversi e il confronto e' spazzatura (trappola mm) — i flag esaurita
#    vengono propagati e i gate etichettati NON-DEFINITI se serve.
#
# RADIUS 3: w101 visita TUTTE le 11 celle dell'anello cheb=3 (GATE W1b) =>
# req note e tracciate esatte; le celle di palla non sono piu' raggiungibili
# dal rientro diretto (serve entrare dall'anello, read forzata, e camminare
# esatto). Qui il washout si spezza (K1 deve mordere) — se anche a radius 3
# le 8 residue sono irraggiungibili: TEOREMA (modulo pannello).
#
# GATE (trappola ii: testimone PRIMA di ogni assert):
#   W1b: w101 visita esattamente le 21 celle della zona-3 (9+1 FREE+11);
#   K0 controllo positivo: ((-1,2),3) raggiungibile (realizzata in natura:
#      se manca, macchina UNSOUND e ogni kill spazzatura);
#   R2 regressione: la macchina a radius 2 riproduce le 24 firme della prima
#      corsa + verifica del washout (firme indipendenti dallo stato iniziale);
#   K1 esca (radius 3): req9 iniziale corrotto => firme diverse (se il
#      washout persiste anche a radius 3, K1 ROSSO = inconcludente onesto);
#   K2 coniugazione specchio (trappola kk): macchina a chiralita' specchio
#      con zona/stato riflessi => firme M-coniugate esatte; esca: l'insieme
#      standard non e' M-chiuso in se'.
#
# Uscita: alpha1/u2_far_collo_machine_summary.json
import sys, os, json, time, argparse
from collections import deque
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY
from record_weapon_vitality import to_bits, SUMMARY
from u2_pocket_certificate import exact_state
from u2_far_ledger import cheb

HERE = os.path.dirname(os.path.abspath(__file__))
ORC2 = os.path.join(HERE, "u2_far_clean_oracle_v2_summary.json")
OUT_JSON = os.path.join(HERE, "u2_far_collo_machine_summary.json")

BALL_R = 2
FREE_ = 2


def zone_cells(R):
    return [(x, y) for y in range(1, R + 1) for x in range(-R, R + 1)
            if cheb((x, y)) <= R]


def in_ball(c):
    return cheb(c) <= BALL_R and c[1] >= 1


def m_cell(c):
    return (-c[0], c[1])


def m_head(h):
    return (-h) % 4


class Machine:
    """Macchina del collo su zona cheb<=R (esatta) / OUT (libero)."""

    def __init__(self, R, init_req, chirality=+1):
        self.R = R
        self.cells = zone_cells(R)
        self.idx = {c: i for i, c in enumerate(self.cells)}
        self.n = len(self.cells)
        self.chir = chirality
        self.ball_idx = [i for i, c in enumerate(self.cells) if in_ball(c)]
        # req iniziale: vettore {FREE,0,1}
        self.init = tuple(init_req[c] for c in self.cells)
        # rientri precomputati: (cella E, heading h) con P=E+D[h] fuori zona
        # e y(P)>=1
        self.entry_pts = []
        zs = set(self.cells)
        for E in self.cells:
            for h in range(4):
                P = (E[0] + DX[h], E[1] + DY[h])
                if P in zs or P[1] < 1:
                    continue
                self.entry_pts.append((E, h))

    def pend2(self, req):
        return sum(1 for i in self.ball_idx if req[i] == 0)

    def read_branches(self, req, E):
        r = req[self.idx[E]]
        return [0, 1] if r == FREE_ else [r]

    def apply_read(self, req, E, read):
        l = list(req)
        l[self.idx[E]] = 1 - read
        return tuple(l)

    def head_after(self, h, read):
        if self.chir == +1:
            bit_is_R = (read == 0)
        else:
            bit_is_R = (read == 1)
        return (h - 1) & 3 if bit_is_R else (h + 1) & 3

    def succ(self, req, loc):
        """Successori: lista (req', loc', cella_letta|None)."""
        out = []
        if loc == "OUT":
            for (E, h) in self.entry_pts:
                for read in self.read_branches(req, E):
                    out.append((self.apply_read(req, E, read),
                                (E, self.head_after(h, read)), E))
        else:
            posa, h = loc
            cn = (posa[0] - DX[h], posa[1] - DY[h])
            if cn[1] < 1:
                return out                      # morte
            if cn not in self.idx:
                out.append((req, "OUT", None))  # esce dalla zona
                return out
            for read in self.read_branches(req, cn):
                out.append((self.apply_read(req, cn, read),
                            (cn, self.head_after(h, read)), cn))
        return out

    def pack(self, req, loc):
        """Stato -> int (2 bit per cella + loc): anti-OOM (trappola g)."""
        v = 0
        for r in req:
            v = (v << 2) | r
        if loc == "OUT":
            v = (v << 8) | 0xFF
        else:
            (cell, h) = loc
            v = (v << 8) | (self.idx[cell] << 2) | h
        return v

    def unpack(self, v):
        lb = v & 0xFF
        v >>= 8
        req = []
        for _ in range(self.n):
            req.append(v & 3)
            v >>= 2
        req.reverse()
        loc = "OUT" if lb == 0xFF else (self.cells[lb >> 2], lb & 3)
        return tuple(req), loc

    def explore(self, state_cap=60_000_000, progress=None):
        """BFS esaustiva dallo stato iniziale (init, OUT). Ritorna
        (firme, whack_edges, n_stati, esaurita). Stati int-packed ovunque
        (set + coda): anti-OOM, trappola g."""
        k0 = self.pack(self.init, "OUT")
        seen = {k0}
        q = deque([k0])
        firme = set()
        whack = set()
        n = 0
        while q:
            if len(seen) >= state_cap:
                return firme, whack, len(seen), False
            req, loc = self.unpack(q.popleft())
            n += 1
            if progress and n % progress == 0:
                print(f"    ... {n} visitati, {len(seen)} stati, "
                      f"{len(firme)} firme", flush=True)
            p2 = self.pend2(req)
            for (req2, loc2, cn) in self.succ(req, loc):
                p2n = self.pend2(req2)
                if p2n == 0 and p2 == 1:
                    firme.add((cn, loc2[1]))
                if p2n < p2 and loc != "OUT" and cn is not None:
                    whack.add((cn, loc[0]))
                k = self.pack(req2, loc2)
                if k not in seen:
                    seen.add(k)
                    q.append(k)
        return firme, whack, len(seen), True


def build_init(reqw, R, free_cells):
    init = {}
    for c in zone_cells(R):
        if c in free_cells:
            init[c] = FREE_
        else:
            assert c in reqw, f"cella di zona {c} non visitata da w101"
            init[c] = reqw[c]
    return init


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--radius", type=int, default=3)
    ap.add_argument("--state-cap", type=int, default=60_000_000)
    args = ap.parse_args()
    t0 = time.time()

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    cw, hw, reqw = exact_state(w101)

    # GATE B1 (pannello §97): l'init loc=OUT esige la posa di continuazione
    # di w101 FUORI zona — a R>=4 (4,1) cade in zona e l'init va cambiato
    assert cheb(cw) > args.radius, \
        f"B1: posa w101 {cw} DENTRO la zona-{args.radius}: init loc=OUT " \
        f"UNSOUND — servono init loc=(cw,hw) e build_init generalizzato"
    print(f"GATE B1 verde: posa di continuazione w101 {cw} fuori "
          f"zona-{args.radius} (init loc=OUT sound)", flush=True)

    # GATE W1b: la zona-3 e' interamente visitata da w101 tranne (1,1)
    z3 = zone_cells(3)
    missing = [c for c in z3 if c not in reqw]
    assert missing == [(1, 1)], f"zona-3 non coperta come atteso: {missing}"
    print(f"GATE W1b verde: w101 visita 20/21 celle della zona-3 "
          f"(manca solo (1,1))", flush=True)

    orc = json.load(open(ORC2))
    residue = {(tuple(r["posa"]), r["h"]) for r in orc["firme_exit"]}

    # ---- GATE R2: regressione radius 2 + OSSERVAZIONE del washout ----
    init2 = build_init(reqw, 2, {(1, 1)})
    m2 = Machine(2, init2)
    firme2, whack2, ns2, ex2 = m2.explore()
    assert ex2
    print(f"\nR2: {ns2} stati, {len(firme2)} firme (attese 24, tutte le 8 "
          f"residue incluse)", flush=True)
    assert len(firme2) == 24 and residue <= firme2, "regressione R2 fallita"
    # washout (B4, pannello): TUTTI i flip singoli + tutte le coppie, corse
    # esaustive (secondi a r2); (1,1) e' FREE e non si flippa
    flippable = [c for c in zone_cells(2) if init2[c] != FREE_]
    wash_diff = []
    for i, ca in enumerate(flippable):
        for cb in [None] + flippable[i + 1:]:
            ib = dict(init2)
            ib[ca] = 1 - ib[ca]
            if cb is not None:
                ib[cb] = 1 - ib[cb]
            fb, _, _, exb = Machine(2, ib).explore()
            assert exb
            if fb != firme2:
                wash_diff.append((str(ca), str(cb),
                                  len(fb ^ firme2)))
    washout2 = (len(wash_diff) == 0)
    print(f"GATE R2 verde: radius 2 riprodotto; washout_radius2 "
          f"(osservazione, {len(flippable)} flip singoli + "
          f"{len(flippable)*(len(flippable)-1)//2} coppie, tutte esaustive) "
          f"= {washout2}"
          + ("" if washout2 else f" — {len(wash_diff)} config sensibili: "
             f"{wash_diff[:5]}"), flush=True)

    # ---- macchina radius 3 ----
    print(f"\n---- MACCHINA radius {args.radius} ----", flush=True)
    init3 = build_init(reqw, args.radius, {(1, 1)})
    m3 = Machine(args.radius, init3)
    firme3, whack3, ns3, ex3 = m3.explore(args.state_cap, progress=2_000_000)
    print(f"radius {args.radius}: {ns3} stati "
          f"({'ESAURITA' if ex3 else 'CAP RAGGIUNTO — INCONCLUDENTE'}), "
          f"{len(firme3)} firme di pulizia raggiungibili:", flush=True)
    for c, h in sorted(firme3):
        tag = " [RESIDUA!]" if (c, h) in residue else \
              (" [reale]" if (c, h) == ((-1, 2), 3) else "")
        print(f"  ({c}, h={h}){tag}", flush=True)

    inter = sorted((list(c), h) for c, h in (firme3 & residue))
    # TESTIMONE PRIMA DELL'ASSERT (trappola ii)
    if inter:
        print(f"\nFIRME RESIDUE RAGGIUNGIBILI a radius {args.radius}: {inter} "
              f"— INCONCLUDENTE (trappole z/ff: raggiungibilita' astratta "
              f"non trasferisce)", flush=True)
    elif ex3:
        print(f"\nTEOREMA DEL COLLO (forma sufficiente, radius "
              f"{args.radius}): nessuna delle 8 firme residue raggiungibile "
              f"nemmeno con OUT libero => v2 TEOREMA (modulo pannello §97)",
              flush=True)

    # GATE K0
    assert ((-1, 2), 3) in firme3, \
        "GATE K0 ROSSO: firma reale irraggiungibile — macchina UNSOUND"
    print(f"GATE K0 verde: firma reale raggiungibile", flush=True)

    # GATE K1 (esca): DEFINITO solo tra esplorazioni ESAUSTIVE (pannello B2,
    # trappola mm: due BFS cappate hanno frontiere diverse e il confronto
    # differenziale e' spazzatura)
    init3b = dict(init3); init3b[(0, 2)] = 1 - init3b[(0, 2)]
    firme3b, _, _, ex3b = Machine(args.radius, init3b).explore(args.state_cap)
    if ex3 and ex3b:
        k1_bites = (firme3b != firme3)
        k1_status = "verde" if k1_bites else "ROSSO"
        print(f"GATE K1 {k1_status}: req corrotto => firme "
              f"{'diverse' if k1_bites else 'IDENTICHE (washout)'} "
              f"({len(firme3b)} vs {len(firme3)})", flush=True)
    else:
        k1_bites = None
        k1_status = "NON-DEFINITO (cap)"
        print(f"GATE K1 NON-DEFINITO: confronto tra esplorazioni cappate "
              f"(esaurite: {ex3}/{ex3b}) — nessuna conclusione dal "
              f"differenziale (trappola mm); conteggi grezzi "
              f"{len(firme3b)} vs {len(firme3)}", flush=True)

    # GATE K2: coniugazione specchio — stessa regola di definitezza
    init3m = {c: init3[m_cell(c)] for c in zone_cells(args.radius)}
    m3m = Machine(args.radius, init3m, chirality=-1)
    firme3m, _, _, ex3m = m3m.explore(args.state_cap)
    if ex3 and ex3m:
        conj = {(m_cell(c), m_head(h)) for c, h in firme3}
        assert firme3m == conj, \
            f"GATE K2 ROSSO: coniugazione violata {sorted(firme3m ^ conj)}"
        assert firme3 != conj, "GATE K2 esca: firme M-chiuse in se'?!"
        k2_status = "verde"
        print(f"GATE K2 verde: coniugazione specchio esatta (esca: insieme "
              f"non M-chiuso, diff {len(firme3 ^ conj)})", flush=True)
    else:
        k2_status = "NON-DEFINITO (cap)"
        print(f"GATE K2 NON-DEFINITO: esplorazioni cappate (esaurite: "
              f"{ex3}/{ex3m}) — la coniugazione esatta e' verificabile solo "
              f"tra insiemi completi; conteggi grezzi {len(firme3m)} vs "
              f"{len(firme3)}", flush=True)

    verdict = ("INCONCLUDENTE-RESIDUE-RAGGIUNGIBILI: " + json.dumps(inter)
               if inter else
               ("TEOREMA-DEL-COLLO-SUFFICIENTE (radius 3, modulo pannello)"
                if ex3 and ex3b and ex3m and k1_bites else
                "INCONCLUDENTE (esplorazione non esaustiva)"))
    out = {"args": vars(args),
           "radius2": {"stati": ns2, "firme": len(firme2),
                       "washout_osservazione": washout2,
                       "washout_config_sensibili": wash_diff,
                       "whack_edges": sorted((list(a), list(b))
                                             for a, b in whack2)},
           "radius3": {"stati": ns3, "esaurita": ex3,
                       "firme_lower_bound": not ex3,
                       "firme": sorted((list(c), h) for c, h in firme3),
                       "residue_raggiungibili": inter,
                       "k1": k1_status, "k2": k2_status,
                       "whack_edges": sorted((list(a), list(b))
                                             for a, b in whack3)},
           "verdetto": verdict,
           "gates": {"B1": "verde", "W1b": "verde", "R2": "verde",
                     "K0": "verde", "K1": k1_status, "K2": k2_status},
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nVERDETTO: {verdict}\nscritto {OUT_JSON} in "
          f"{out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
