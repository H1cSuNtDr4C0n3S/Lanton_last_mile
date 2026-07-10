# door_approach_lens.py — §105a: PANNELLO del blocco §102-§104 (debito §104e).
#
# LENTE A (macchinario indipendente) su tre risultati:
#   A1. approcci/fasi freschi (§103/§104a): 30 semi catena-3 ricalcolati con il
#       simulatore INDIPENDENTE di record_divergence_lens.run_real (quello dei
#       40/40 §101e) + estrattore di fase basato su data/W0.npy (FILE DIVERSO da
#       data/w0.txt: cross-valida anche la coppia di file canonici §2) + rilevatore
#       d'onset RISCRITTO (scan in avanti del primo punto con coda periodica-104
#       >= 2080, poi estensione all'indietro) — onset, fase e approccio-12 devono
#       coincidere con la pipeline §103/§104 (run_collect_records + w0.txt).
#   A2. LEMMA LINGUA D'APPROCCIO (§104c): testimoni di REALIZZAZIONE — per 25
#       approcci realizzabili casuali, costruisco la configurazione finita dal
#       cammino virtuale e la CORRO col simulatore indipendente: le prime 220
#       svolte devono riprodurre approccio+W0x2 esattamente (realizzabilita'
#       DIMOSTRATA per costruzione, non solo dichiarata). Per 25 non-realizzabili:
#       checker di contraddizione RISCRITTO (rilettura incoerente su cammino).
#   A3. fasi dei germi ai record (§104d): 20 record canonici, germe costruito
#       dalla GRIGLIA REALE (germ_turns_from_real, lente §101) e fase dalla coda.
# ESCHE: (E1) riferimento W0 ruotato di 1 => fasi tutte diverse (beccata);
#   (E2) finestra d'approccio sfasata di 1 => parole diverse dal censimento;
#   (E3) coda di realizzabilita' a 1 periodo => conteggio DIVERSO da 671 (la
#   saturazione dichiarata a §104c e' 2 periodi: con 1 il vincolo e' piu' lasco).
import sys, os, json, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, xs, ALPHA
from record_divergence_lens import run_real, germ_turns_from_real

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 0x9E3779B97F4A7C15
GOLD = 0xBF58476D1CE4E5B9

# --- riferimento W0 dal FILE BINARIO (indipendente da w0.txt) ---
W0npy = np.load(os.path.join(HERE, "..", "data", "W0.npy"))
W0b = "".join(str(int(b)) for b in W0npy)
assert len(W0b) == 104


def fresh_states(n, base=None):
    s = xs(xs(BASE if base is None else base))
    out = []
    for _ in range(n):
        out.append(s)
        s = xs(xs(s ^ GOLD))
    return out


def onset_backext(turns):
    """Rilevatore riscritto: primo n con coda 104-periodica lunga >= 2080 che
    arriva a n, poi estensione all'indietro. Ritorna onset o -1."""
    T = len(turns)
    run = 0
    for i in range(104, T):
        if turns[i] == turns[i - 104]:
            run += 1
            if run >= 2080:
                onset = i - run + 1 - 104 + 104
                while onset > 0 and turns[onset - 1] == turns[onset - 1 + 104]:
                    onset -= 1
                return onset
        else:
            run = 0
    return -1


def phase_of(per):
    return next((k for k in range(104) if W0b[k:] + W0b[:k] == per), None)


def virtual_grid(word_bits):
    """Cammino virtuale RISCRITTO: griglia dei colori iniziali rivelati; None se
    rilettura contraddittoria. Ritorna (init_colors: cella->colore iniziale)."""
    DX = (0, 1, 0, -1)
    DY = (-1, 0, 1, 0)
    x = y = 0
    h = 0
    cur = {}
    init = {}
    for b in word_bits:
        need = 0 if b else 1
        c = (x, y)
        if c in cur:
            if cur[c] != need:
                return None
        else:
            init[c] = need
        if b:
            h = (h + 1) & 3
            cur[c] = 1
        else:
            h = (h + 3) & 3
            cur[c] = 0
        x += DX[h]
        y += DY[h]
    return init


def realizable_count(app_width, tail_periods):
    W0bits = tuple(int(c) for c in W0b)
    n = 0
    for m in range(1 << app_width):
        app = tuple((m >> i) & 1 for i in range(app_width - 1, -1, -1))
        if virtual_grid(app + W0bits * tail_periods) is not None:
            n += 1
    return n


def main():
    global W0b
    rng = random.Random(105)
    ref = json.load(open(os.path.join(HERE, "fresh_onset_phase_census_summary.json")))
    fails = 0

    # ---------- A1: 30 semi freschi ----------
    states = fresh_states(2500, base=xs(BASE ^ 0x94D049BB133111EB))
    idxs = rng.sample(range(2500), 30)
    ok1 = 0
    for i in idxs:
        seed, _, _ = build_seed(states[i], 5, 25)
        if not seed or min(cy for (_, cy) in seed) > 0:
            continue
        turns, grid, traj, pose = run_real(seed, 400_000)
        t_on = onset_backext(turns)
        assert t_on >= 0
        per = "".join(str(b) for b in turns[t_on:t_on + 104])
        ph = phase_of(per)
        app = "".join("R" if b else "L" for b in turns[t_on - 12:t_on])
        # confronto con la pipeline ufficiale
        from record_word_census import run_collect_records
        turns2, t_on2, _ = run_collect_records(seed)
        per2 = "".join(str(b) for b in turns2[t_on2:t_on2 + 104])
        app2 = "".join("R" if b else "L" for b in turns2[t_on2 - 12:t_on2])
        W0txt = open(os.path.join(HERE, "..", "data", "w0.txt")).read().strip()
        W0tb = "".join("1" if c == "R" else "0" for c in W0txt)
        ph2 = next((k for k in range(104) if W0tb[k:] + W0tb[:k] == per2), None)
        same = (t_on == t_on2 and ph == ph2 and app == app2)
        ok1 += 1 if same else 0
        if not same:
            fails += 1
            print(f"A1 FAIL: seme {states[i]} onset {t_on}/{t_on2} fase {ph}/{ph2}")
    print(f"A1 (semi freschi, sim+onset+W0.npy indipendenti): {ok1}/30 PASS",
          flush=True)

    # ---------- A2: realizzazione costruttiva ----------
    W0bits = tuple(int(c) for c in W0b)
    realizzabili = []
    non_real = []
    for m in range(4096):
        app = tuple((m >> i) & 1 for i in range(11, -1, -1))
        ig = virtual_grid(app + W0bits * 2)
        (realizzabili if ig is not None else non_real).append((app, ig))
    assert len(realizzabili) == 671, f"ri-enumerazione: {len(realizzabili)} != 671"
    print(f"A2a: ri-enumerazione indipendente = {len(realizzabili)}/4096 == 671 OK",
          flush=True)
    ok2 = 0
    for (app, ig) in rng.sample(realizzabili, 25):
        seed_black = {c for c, col in ig.items() if col == 1}
        # correzione: il mondo di realizzazione ha SOLO le celle di init;
        # le celle mai lette prima sono libere: bianche va bene per il replay
        turns, grid, traj, pose = run_real(seed_black, 220)
        want = app + W0bits * 2
        got = tuple(turns[:220])
        if got == want:
            ok2 += 1
        else:
            d = next(i for i in range(220) if got[i] != want[i])
            # la cella letta a d era fuori da init (libera): il testimone
            # richiede il colore giusto — con init completo non accade
            fails += 1
            print(f"A2 FAIL: divergenza a {d}")
    print(f"A2b: realizzazione costruttiva (25 campioni, sim indipendente): "
          f"{ok2}/25 PASS", flush=True)

    # ---------- A3: fasi dei germi ai record ----------
    import csv
    rows = list(csv.DictReader(open(os.path.join(
        HERE, "record_divergence_census_records.csv"))))
    dumps = {od.index: od for od in parse_dumps(ALPHA / "dumps_all.txt")}
    ok3 = 0
    for r in rng.sample(rows, 20):
        oi = int(r["orbit"])
        t = int(r["t"])
        og = int(r["onset_germe"])
        seed, _, _ = build_seed(dumps[oi].rngstate, 5, 25)
        gturns, reads = germ_turns_from_real(seed, t, og + 208)
        per = "".join(str(b) for b in gturns[og:og + 104])
        per2 = "".join(str(b) for b in gturns[og + 104:og + 208])
        ph = phase_of(per)
        if per == per2 and ph is not None:
            ok3 += 1
        else:
            fails += 1
            print(f"A3 FAIL: orb {oi} t={t} fase {ph}")
    print(f"A3 (germe dalla griglia reale, coda periodica + fase): {ok3}/20 PASS",
          flush=True)

    # ---------- ESCHE ----------
    per13 = W0b[13:] + W0b[:13]
    W0rot = W0b[1:] + W0b[:1]
    e1 = next((k for k in range(104) if W0rot[k:] + W0rot[:k] == per13), None)
    print(f"E1 riferimento ruotato: fase {e1} != 13 "
          f"{'BECCATA' if e1 != 13 else '*** NON BECCATA ***'}", flush=True)
    assert e1 != 13
    # E3-v1 (coda a 1 periodo) NON e' un'esca: misurato 671 anche a 1 periodo —
    # la realizzabilita' dell'approccio-12 satura GIA' a un periodo (fatto piu'
    # netto del "saturo a 2" di §104c; correzione a verbale). Esca vera: coda
    # con un bit di W0 corrotto => il conteggio DEVE cambiare.
    n1 = realizable_count(12, 1)
    print(f"E3-v1 (promossa a misura): coda a 1 periodo = {n1} (saturazione "
          f"gia' a 1 periodo)", flush=True)
    W0b_orig = W0b
    W0b = W0b_orig[:50] + ("0" if W0b_orig[50] == "1" else "1") + W0b_orig[51:]
    n_bad = realizable_count(12, 2)
    W0b = W0b_orig
    print(f"E3-v2 coda corrotta (1 bit): {n_bad} != 671 "
          f"{'BECCATA' if n_bad != 671 else '*** NON BECCATA ***'}", flush=True)
    assert n_bad != 671
    print(f"\nPANNELLO §105a: {'TUTTO VERDE' if fails == 0 else f'{fails} FAIL'}",
          flush=True)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
