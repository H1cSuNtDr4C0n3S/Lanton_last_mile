# u2_infinite_rail.py — §92: TEOREMA del testimone D = infinito per U2-NERO.
#
# Le coprenti-nere fuggite (u2_cover_witnesses.json / campagna stress-2) hanno muri
# che sfondano il tetto del footprint (riga 7) ed entrano in territorio vergine.
# Qui una di esse viene promossa a TEOREMA: D(coprente-nera) = infinito, tramite il
#
#   LEMMA DEL RAGGIO MONOTONO. Sia W = f + coprente + w101 valida (realizzabile +
#   record-compatibile), con coda in posa (c0, h0=0 pre-svolta). Il raggio
#   r_m = (L,R)^m prepende passi alternati: le celle sono la scala
#   c0+(0,1), c0+(-0,1)+(-1,0), c0+(-1,2), ... — a coppie, y cresce di 1 e x cala
#   di 1: tutte DISTINTE tra loro, y strettamente crescente ogni 2 passi. Sia m0
#   tale che ogni cella del raggio oltre la coppia m0 abbia y > y_max(footprint(W)
#   U raggio fino a m0). Se r_m + W e' valida per ogni m <= m0+2 (check finito),
#   allora r_m + W e' valida per OGNI m: ogni passo successivo visita una cella
#   MAI vista (fuori dal footprint per y, distinta dalle celle del raggio per
#   monotonia) => prima lettura libera (il bit del raggio la dichiara) => la
#   realizzabilita' si conserva; y >= 1 sempre => record-compat si conserva. QED.
#
# NOTA (il senso per il Muro): il raggio legge un nero FRESCO ogni 2 passi (i bit
# L su celle mai viste). Per un'orbita REALE i freschi-neri sono celle di SEME:
# la rotaia infinita costa |seme| = infinito. Lontano dal seme le celle fresche
# sono bianche (R forzato): il testimone e' VACUO ai record lontani — la vitalita'
# D era l'invariante sbagliato (parente della trappola (w) e del pavimento del
# morso §57): l'oggetto giusto e' il BILANCIO DEI NERI FRESCHI (vedi addendum).
#
# Procedura:
#   1. prende i testimoni nere-D>=400 (stress-2), ne sceglie uno;
#   2. DFS con budget sopra la parola: trova un cammino di fuga f di prof. 80;
#   3. adjuster (<= 4 bit) per portare l'heading di coda a 0;
#   4. calcola m0 dal bbox, verifica valid() LETTERA PER LETTERA fino a m0+extra
#      (default extra-pairs = 40, ridondanza oltre il minimo m0+2 del lemma);
#   5. verifica meccanica della monotonia (celle raggio oltre m0: y > y_max, distinte);
#   6. scrive il certificato in alpha1/u2_infinite_rail_summary.json.
import sys, os, json, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY
from record_weapon_vitality import to_bits, to_str, SUMMARY
from u2_cover_rail_map import valid
from u2_pocket_certificate import exact_state, exact_step, anchor_trace, TGT

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "u2_infinite_rail_summary.json")


def dfs_escape_path(w2, y_goal, depth_cap=400, node_cap=1_000_000):
    """Primo cammino di prepend validi che porta la coda a (y >= y_goal, h == 0)
    (bit dal piu' recente al piu' antico). DFS con budget, euristica verso l'alto."""
    c0, h0, req0 = exact_state(w2)
    nodes = [0]
    sys.setrecursionlimit(depth_cap + 300)

    def rec(c, h, req, path):
        if c[1] >= y_goal and h == 0:
            return path
        if len(path) >= depth_cap or nodes[0] >= node_cap:
            return None
        # euristica: prova prima il bit che lascia l'heading vicino a 0 (= salire)
        order = sorted((0, 1), key=lambda b: ((h - 1) & 3 if b else (h + 1) & 3) % 4)
        for bit in order:
            nodes[0] += 1
            r2 = dict(req)
            cn, hn, _ = exact_step(c, h, r2, bit)
            if cn is None:
                continue
            got = rec(cn, hn, r2, path + [bit])
            if got is not None:
                return got
        return None

    return rec(c0, h0, req0, []), nodes[0]


def prepend_bits(bits_newest_first):
    """Converte una lista di bit in ordine di prepend nella tupla-parola (antico->recente)."""
    return tuple(reversed(bits_newest_first))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--witness", type=int, default=0, help="indice del testimone nere400")
    ap.add_argument("--escape-depth", type=int, default=80)
    ap.add_argument("--extra-pairs", type=int, default=40,
                    help="coppie di raggio verificate OLTRE m0 (ridondanza)")
    args = ap.parse_args()
    t0 = time.time()

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    wit = json.load(open(os.path.join(HERE, "u2_cover_witnesses.json")))
    assert "nere400" in wit, "servono i testimoni nere400 (campagna stress-2)"
    wrec = wit["nere400"][args.witness]
    e2 = to_bits(wrec["word"])
    assert e2[0] == 1, "il testimone deve essere una coprente NERA (primo bit R)"
    w2 = e2 + w101
    assert valid(w2)[1] is None

    # gate: e' davvero una coprente (unica visita a (1,1) = passo piu' antico)
    tr = anchor_trace(w2)
    assert tr[0][0] == TGT and TGT not in tr[0][1:], "non e' una coprente"
    print(f"testimone: coprente-nera prof.{len(e2)} (K totale {len(w2)})", flush=True)

    # 2. cammino di fuga con obiettivo di posa (y alto, h=0); se il raggio collide
    #    col footprint nei primi passi, alza la soglia e riprova
    foot_w2_pos = set(anchor_trace(w2)[0])
    y_top = max(cy for _, cy in foot_w2_pos)
    W = None
    for attempt in range(6):
        y_goal = y_top + 3 + 2 * attempt
        f_bits, nodes = dfs_escape_path(w2, y_goal)
        assert f_bits is not None, f"fuga non trovata (y_goal {y_goal})"
        f_word = prepend_bits(f_bits)
        Wc = f_word + w2
        assert valid(Wc)[1] is None
        for j in range(len(f_word) - 1, -1, -1):
            assert valid(f_word[j:] + w2)[1] is None
        c, h, req = exact_state(Wc)
        assert h == 0 and c[1] >= y_goal
        # le prime 60 celle del raggio devono essere FRESCHE (fuori dal req map)
        probe_ok = True
        cc, hh = c, 0
        for i in range(120):
            cn = (cc[0] - DX[hh], cc[1] - DY[hh])
            if cn in req:
                probe_ok = False
                break
            bit = 0 if i % 2 == 0 else 1
            hh = (hh - 1) & 3 if bit == 1 else (hh + 1) & 3
            cc = cn
        print(f"tentativo {attempt}: y_goal {y_goal}, fuga prof. {len(f_word)} "
              f"({nodes} nodi), coda {c} h=0, raggio-fresco={probe_ok}", flush=True)
        if probe_ok:
            W = Wc
            break
    assert W is not None, "nessuna fuga con raggio fresco entro 6 tentativi"
    A = ()
    WA = W

    # 4. raggio (L,R)^m: celle e m0
    foot = set(anchor_trace(WA)[0])
    y_max_foot = max(cy for _, cy in foot)
    ray_cells = []
    cc, hh = c, 0
    bits_seq = []
    for pair in range(2000):
        for bit in (0, 1):                      # L poi R
            cn = (cc[0] - DX[hh], cc[1] - DY[hh])
            ray_cells.append(cn)
            bits_seq.append(bit)
            hh = (hh - 1) & 3 if bit == 1 else (hh + 1) & 3
            cc = cn
    # m0: prima coppia dopo la quale ogni cella del raggio ha y > y_max di TUTTO
    # (footprint + raggio iniziale). y del raggio cresce: basta y > y_max_all.
    m0 = None
    for pair in range(1, 900):
        cells_up_to = ray_cells[:2 * pair]
        y_all = max(y_max_foot, max(cy for _, cy in cells_up_to))
        rest_ok = all(cy > y_all for _, cy in ray_cells[2 * pair: 2 * (pair + 300)])
        if rest_ok:
            m0 = pair
            break
    assert m0 is not None
    print(f"m0 = {m0} coppie (y_max footprint {y_max_foot})", flush=True)

    # verifica lettera-per-lettera fino a m0 + extra
    m_check = m0 + args.extra_pairs
    ray_word = prepend_bits(bits_seq[:2 * m_check])
    full = ray_word + WA
    for j in range(len(ray_word) - 1, -1, -1):
        assert valid(ray_word[j:] + WA)[1] is None, f"raggio invalido al passo {j}"
    print(f"raggio verificato lettera-per-lettera per {m_check} coppie "
          f"({2 * m_check} passi)", flush=True)

    # 5. monotonia meccanica: oltre m0 le celle sono distinte, y crescente a coppie,
    #    y > y_max(tutto fino a m0), e mai nel footprint
    seen_cells = set(ray_cells[:2 * m0]) | foot
    y_all = max(cy for _, cy in seen_cells)
    prev_y = None
    for i in range(2 * m0, 2 * (m0 + 500)):
        cell = ray_cells[i]
        assert cell not in seen_cells, "cella del raggio rivista!"
        seen_cells.add(cell)
        assert cell[1] > y_all, "cella del raggio non strettamente sopra il footprint"
        if i % 2 == 1:
            if prev_y is not None:
                assert cell[1] == prev_y + 1, "y non cresce di 1 a coppia"
            prev_y = cell[1]
    print("monotonia verificata su 500 coppie oltre m0", flush=True)

    # 6. bilancio dei neri freschi lungo fuga+raggio
    tr_full = anchor_trace(full)
    # freschi-neri = celle con prima lettura nera che NON sono nel footprint di w2
    foot_w2 = set(anchor_trace(w2)[0])
    fresh_blacks = sum(1 for cel, g in tr_full[2].items()
                      if g == 1 and cel not in foot_w2)
    print(f"neri FRESCHI (celle di seme) consumati da fuga+adjuster+raggio "
          f"({m_check} coppie): {fresh_blacks} (~1/coppia sul raggio)", flush=True)

    out = {"witness": {"word_ext": wrec["word"], "prof": len(e2)},
           "escape": {"prof": len(f_word), "word": to_str(f_word)},
           "adjuster": to_str(A),
           "ray": {"pattern": "LR", "m0": m0, "m_verificate": m_check,
                   "tail_pose": [list(c), 0]},
           "teorema": ("D = INFINITO per questa coprente-nera: valid(r_m + A + f + "
                       "coprente + w101) per ogni m (lemma del raggio monotono; "
                       "check finito fino a m0+%d)" % args.extra_pairs),
           "bilancio": {"neri_freschi_totali": fresh_blacks,
                        "nota": ("ogni coppia del raggio consuma 1 nero fresco = "
                                 "1 cella di seme: il testimone e' VACUO ai record "
                                 "lontani dal seme (bianco fresco => R forzato)")},
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nTEOREMA: D = infinito (testimone certificato, raggio monotono).")
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
