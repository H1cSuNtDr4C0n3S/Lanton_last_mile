# record_trail_forensics.py — §89c: la scia al bordo del pigeonhole.
#
# Parte 1 (FORENSE, 3 eventi G=1 di §89b). Modello di autoconsistenza da validare:
# al record t con parola w (K=101) e colpevole unica c di eta' a = K+j, la parola ESTESA
# w' = svolte(t-a..t-1) deve:
#   (i)   essere realizzabile e con footprint in {y>=1} (automatico ai record stretti,
#         verificato: il passato reale E' l'estensione record-compatibile, §87e);
#   (ii)  visitare c ESATTAMENTE al passo 0 (eta' = ultima visita) con svolta R
#         (lettura bianca -> dipinge NERO) e mai piu';
#   (iii) quindi: colore di c nel germe di w' = NERO, word-determinato (Finestra-(K+j));
#   (iv)  le altre celle del residuo di w che cadono nel footprint di w' devono essere
#         BIANCHE nel germe di w' (autoconsistenza: la stessa scia che blocca c non deve
#         sporcare il resto del residuo); le celle fuori dal footprint restano assunzioni
#         sul passato piu' profondo (conteggiate).
#
# Parte 2 (COROLLARIO DEL BLOCCO ANTICO, famiglia certificata §88). Per ogni m,
# residuo(sigma^m tau w101) = {(1,1)} implica (1,1) FUORI dal footprint dell'estensione:
# se le ultime 405+8m svolte di un'orbita sono sigma^m tau w101, l'orbita NON ha visitato
# (1,1) in quell'intero arco => l'eta' della colpevole (1,1) supera 405+8m. Verifica
# diretta m=1..46 + induzione onset-lock ((1,1) in V0, blocchi nuovi disgiunti da V0
# per ogni m) => vale per OGNI m. Lungo la famiglia certificata la scia recente NON puo'
# salvare il pigeonhole: serve pre-semina di eta' illimitata al crescere del match.
#
# Uscita: alpha1/record_trail_forensics_summary.json
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA
from onset_cone_lock import DX, DY, P, simulate, rotk
from kwindow_spoiler_census import virtual_walk, to_anchor_frame
from record_weapon_hunt import eval_word
from record_word_census import run_collect_records
from record_weapon_vitality import to_bits, SUMMARY

HERE = os.path.dirname(os.path.abspath(__file__))
DYN = os.path.join(HERE, "record_guilty_dynamics_summary.json")
CYC = os.path.join(HERE, "record_weapon_cycle_summary.json")
RAIL = os.path.join(HERE, "record_weapon_rail_summary.json")
OUT = os.path.join(HERE, "record_trail_forensics_summary.json")
K = 101


def walk_positions(word):
    """Posizioni visitate dal cammino virtuale, nell'ordine (frame del cammino)."""
    pos = []
    x = y = 0
    h = 0
    for wbit in word:
        pos.append((x, y))
        if wbit:
            h = (h + 1) & 3
        else:
            h = (h + 3) & 3
        x += DX[h]
        y += DY[h]
    return pos, (x, y, h)


def main():
    t_start = time.time()
    dumps = {od.index: od for od in parse_dumps(ALPHA / "dumps_all.txt")}
    autopsy = json.load(open(DYN))["G1_autopsy"]
    assert len(autopsy) == 3

    # ---------------- Parte 1: forense dei 3 eventi ----------------
    part1 = []
    for ev in autopsy:
        od = dumps[ev["orbit"]]
        seed, _, _ = build_seed(od.rngstate, 5, 25)
        turns, t_on, records = run_collect_records(seed)
        assert t_on == od.onset_header
        t = ev["t"]
        a = ev["eta"]
        assert isinstance(a, int), "colpevole di seme: fuori dal modello di scia"
        j = a - K
        cell = tuple(ev["cella_rel"])

        w = tuple(turns[t - K:t])
        wex = tuple(turns[t - a:t])
        r = eval_word(w)
        assert r is not None and r[0] == ev["burden"]
        assert cell in {tuple(c) for c in r[3]}, "colpevole non nel residuo?!"

        # (i) realizzabilita' + record-compatibilita' dell'estensione
        vg, pose = virtual_walk(wex)
        assert vg is not None, "estensione irrealizzabile?!"
        anchor_ex = to_anchor_frame(vg, pose)
        assert all(cy >= 1 for (_, cy) in anchor_ex), "footprint esteso fuori {y>=1}?!"

        # (ii) visita di c solo al passo 0, svolta R — nel frame ANCHOR (rotazione
        # k=(-h0)%4 come to_anchor_frame: l'heading di fine cammino virtuale non e' 0
        # in generale, dipende dall'heading reale all'inizio dell'estensione)
        posl, endpose = walk_positions(wex)
        x0, y0, h0 = endpose
        kk = (-h0) % 4
        rel = [rotk((px - x0, py - y0), kk) for (px, py) in posl]
        visits = [i for i, p in enumerate(rel) if p == cell]
        assert visits == [0], f"visite della colpevole a passi {visits} != [0]"
        assert wex[0] == 1, "prima svolta dell'estensione non R?!"

        # (iii) colore word-determinato nero
        assert anchor_ex[cell] == 1, "germe esteso non nero sulla colpevole?!"
        fp_w = set(to_anchor_frame(*virtual_walk(w)))
        assert cell not in fp_w, "colpevole nel footprint del suffisso K?!"

        # (iv) autoconsistenza sulle altre celle del residuo
        others = [tuple(c) for c in r[3] if tuple(c) != cell]
        in_fp = [c for c in others if c in anchor_ex]
        bad = [c for c in in_fp if anchor_ex[c] != 0]
        assert not bad, f"scia sporca il residuo: {bad}"
        part1.append({"orbit": ev["orbit"], "t": t, "eta": a, "j": j,
                      "cella": list(cell), "burden": ev["burden"],
                      "residuo_altri": len(others),
                      "word_determinati_bianchi": len(in_fp),
                      "assunzioni_passato_profondo": len(others) - len(in_fp),
                      "footprint_esteso": len(anchor_ex)})
        print(f"FORENSE orb {ev['orbit']} t={t}: VERDE — colpevole {cell} dipinta al "
              f"passo 0 dell'estensione (j={j}), svolta R, mai rivisitata, germe esteso "
              f"nero su di lei e bianco su {len(in_fp)}/{len(others)} altre celle del "
              f"residuo ({len(others)-len(in_fp)} restano assunzioni profonde)", flush=True)

    # ---------------- Parte 2: Blocco Antico sulla famiglia certificata ----------------
    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    cyc = json.load(open(CYC))
    cert = cyc["certificato"]
    rail = json.load(open(RAIL))["rail_oldest_first"]
    sigma = to_bits(cert["sigma"])
    tau = to_bits(rail[cyc["finestra"][1] - cert["j"]:])
    base2 = tau + w101

    for m in range(0, 47):
        wfam = sigma * m + base2 if m > 0 else base2
        anch = to_anchor_frame(*virtual_walk(wfam))
        assert (1, 1) not in anch, f"(1,1) nel footprint a m={m}?!"
    # (1,1) in V0 (insieme visitato pre-onset a m=40): l'induzione onset-lock
    # (blocchi nuovi disgiunti da V0) estende l'esclusione a OGNI m.
    anch40 = to_anchor_frame(*virtual_walk(sigma * 40 + base2))
    germ_black = {c for c, col in anch40.items() if col == 1}
    _, _, onset, fr, _ = simulate(germ_black, 0, 0, 0, 2_000_000, chk=2600)
    V0 = {c for c, (tt, _) in fr.items() if tt < onset + P}
    assert (1, 1) in V0, "(1,1) non in V0?!"
    print(f"\nBLOCCO ANTICO: (1,1) fuori dal footprint per m=0..46 (diretto) e per OGNI "
          f"m (induzione onset-lock: blocchi disgiunti da V0, (1,1) in V0). "
          f"=> al record con suffisso sigma^m*tau*w101 l'eta' della colpevole (1,1) "
          f"supera {len(base2)}+8m: la scia recente NON puo' salvare il pigeonhole "
          f"lungo la famiglia certificata.", flush=True)

    out = {"part1_forensics": part1,
           "part2_blocco_antico": {"m_diretto": [0, 46], "suffix_len_base": len(base2),
                                   "eta_minima": f"{len(base2)}+8m",
                                   "v0_contains_11": True},
           "elapsed_s": round(time.time() - t_start, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
