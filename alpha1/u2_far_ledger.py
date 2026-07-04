# u2_far_ledger.py — §93 (U2-LONTANO): il LEDGER DEI PENDING, macchinario + gate.
#
# OGGETTO (dal pannello §92, ledger corretto): il pending e' uno STATO della cella,
# non un evento. Nel camminatore all'indietro (frame anchor, exact_step §92):
#   pending(c)  <=>  la prima-lettura-corrente-nella-parola di c e' NERA
#               <=>  req(c) == 0 (la prossima visita piu' antica deve leggere BIANCO).
# OGNI L apre il pending di una cella NON-pending (fresca o rivisitata req=1);
# L su cella gia' pending e' IRREALIZZABILE (pending => req=0 => lettura bianca
# forzata — pannello §93, lente ledger): ogni L e' un'apertura netta. Ogni R su
# cella pending lo chiude; fresh-R e' neutra. Bilancio = #pending a fine corsa.
#
# SEMANTICA (il ponte con le orbite REALI, GATE L1): per una parola-passato COMPLETA
# (dalla nascita), pending(c) <=> la prima lettura della VITA di c e' nera <=> c e'
# una cella NERA del SEME. Quindi in ogni regione senza seme i pending a fine
# ricostruzione DEVONO essere zero: e' il vincolo che U2-LONTANO usa nella palla-R.
#
# GATE (fermarsi al primo rosso; ognuno puo' fallire):
#   L0 identita' incrementale: req/pending mantenuti prepend-per-prepend ==
#      ricomputati da zero via anchor_trace, su estensioni casuali di w101;
#   L1 verita' di terra forward (3 sotto-gate):
#      a. griglia vuota (onset 9977): la parola di vita ha ZERO pending;
#      b. seme {(7,-7)} (onset 106258): pending == {(7,-7)} esatto;
#      c. 10 blob casuali: pending == {celle nere del seme visitate}, con
#         uguaglianza dei conteggi (il bilancio §92e: #prime-letture-vita-nere
#         == |seme_nero visitato|);
#   L2 controesempio del pannello §92: sul testimone infinite-rail
#      (fuga+coprente+w101), la corsa forzata fresco=>R e' deterministica,
#      sopravvive 2918 passi, fa 1326 L-su-rivisitata e porta i pending
#      da 60 a 286 (numeri ESATTI dall'addendum §92e — devono riprodursi);
#   L3 lemma dei bianchi che curvano (all-R): su 4000 parole valide casuali la
#      corsa all-R muore entro il 5° prepend, e le morti al 4° cadono TUTTE
#      sulla cella di coda (enunciato deduttivo nel docstring di allr_run).
#
# Uscita: alpha1/u2_far_ledger_summary.json
import sys, os, json, time, random, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY, rotk, simulate, onset_verified
from record_weapon_vitality import to_bits, to_str, SUMMARY
from u2_cover_rail_map import valid
from u2_pocket_certificate import (anchor_trace, exact_state, exact_step,
                                   random_valid_ext, FREE, TGT)

HERE = os.path.dirname(os.path.abspath(__file__))
RAIL_SUM = os.path.join(HERE, "u2_infinite_rail_summary.json")
OUT_JSON = os.path.join(HERE, "u2_far_ledger_summary.json")


def cheb(c):
    return max(abs(c[0]), abs(c[1]))


def pend_set(req):
    """I pending sono GIA' dentro req: pending(c) <=> req(c)==0 (prossima lettura
    piu' antica = bianca <=> prima-lettura-corrente = nera)."""
    return {c for c, r in req.items() if r == 0}


def first_reads_abs(word):
    """Prime letture in frame ASSOLUTO di nascita (0,0,h=0), parola antico->recente.
    Ritorna dict cella->colore_iniziale (None se irrealizzabile). Stessa passeggiata
    di virtual_walk ma con tracking esplicito delle prime letture."""
    fr = {}
    grid = {}
    x = y = 0; h = 0
    for b in word:
        c = (x, y)
        need = 0 if b else 1
        if c in grid:
            if grid[c] != need:
                return None
        else:
            fr[c] = need
        if b:
            h = (h + 1) & 3; grid[c] = 1
        else:
            h = (h + 3) & 3; grid[c] = 0
        x += DX[h]; y += DY[h]
    return fr


def forced_run(word, step_cap=100_000, ball_radii=()):
    """La CORSA INVERSA FORZATA (fresco=>R) sopra 'word' (valida, frame anchor).
    Deterministica al 100%: su cella fresca il bit e' R (lettura bianca); su cella
    rivisitata la lettura e' forzata dall'alternanza (= req). Muore SOLO per y<1
    (la cella del prepend e' bit-indipendente; su rivisitata la lettura forzata e'
    per definizione realizzabile). Ritorna dict con: passi, causa, L_su_rivisitata,
    pend0/pend_fine (totali), y_max, cheb_max, e per ogni R in ball_radii lo
    snapshot alla PRIMA uscita dalla palla (passo, pending in-palla aperti,
    celle pending in-palla)."""
    c, h, req = exact_state(word)
    pend = pend_set(req)
    pend0 = len(pend)
    balls = {R: None for R in ball_radii}
    out = {"pend0": pend0, "L_riv": 0, "y_max": c[1], "cheb_max": cheb(c)}
    steps = 0
    while steps < step_cap:
        cn = (c[0] - DX[h], c[1] - DY[h])
        if cn[1] < 1:
            out["causa"] = "y<1"
            break
        r = req.get(cn, FREE)
        if r == FREE:
            read = 0                      # fresco => R (lettura bianca)
        else:
            read = r                      # rivisitata: lettura forzata
            if read == 1:
                out["L_riv"] += 1
        bit = 1 if read == 0 else 0
        req[cn] = 1 - read
        if read == 1:
            pend.add(cn)                  # ogni L apre/riapre
        else:
            pend.discard(cn)              # R chiude (se pending), fresh-R neutra
        h = (h - 1) & 3 if bit == 1 else (h + 1) & 3
        c = cn
        steps += 1
        out["y_max"] = max(out["y_max"], c[1])
        out["cheb_max"] = max(out["cheb_max"], cheb(c))
        for R in ball_radii:
            if balls[R] is None and cheb(c) > R:
                inb = sorted(p for p in pend if cheb(p) <= R)
                balls[R] = {"passo": steps, "pend_in_palla": len(inb),
                            "celle": inb}
    else:
        out["causa"] = "step_cap"
    out["passi"] = steps
    out["pend_fine"] = len(pend)
    out["balls"] = balls
    return out


def allr_run(word):
    """Corsa all-R (solo prepend R) su parola valida NON VUOTA.
    LEMMA DEI BIANCHI CHE CURVANO (deduttivo):
    4 prepend R consecutivi sommano D[h]+D[h-1]+D[h-2]+D[h-3] = 0, quindi il 4°
    prepend cade sulla cella di CODA c0; le celle c1,c2,c3 sono distinte da c0
    (somme parziali di versori non nulle). Se la prima lettura di c0 nella parola
    era BIANCA (R), req(c0)=1 e il 4° R (lettura bianca) e' irrealizzabile: morte
    al 4° SULLA CODA. Se era NERA, il 4° R chiude il pending di c0 e il 5° prepend
    cade su c1 = c0 - D[h0], gia' letta BIANCA al 1° prepend: req(c1)=1, il 5° R
    e' irrealizzabile: morte al 5°. Ai passi 1..3 la corsa puo' morire prima
    (y<1 O req=nero su cella di parola rivisitata): morte ancora piu' precoce.
    In ogni caso OGNI parola valida uccide all-R entro il 5° prepend. QED.
    Ritorna (passo di morte 1..5, causa, cella di morte, cella=coda?)."""
    c0, h, req = exact_state(word)
    c = c0
    for k in range(1, 7):
        cn = (c[0] - DX[h], c[1] - DY[h])
        if cn[1] < 1:
            return k, "y<1", cn, cn == c0
        r = req.get(cn, FREE)
        if r == 1:
            return k, "irrealizzabile", cn, cn == c0
        req[cn] = 1
        h = (h - 1) & 3
        c = cn
    return None, "sopravvissuta", None, False


# ---------------- gate ----------------

def gateL0(w101, rng, trials=800):
    """Identita' incrementale: prepend-per-prepend vs anchor_trace da zero."""
    tested = 0
    for _ in range(trials):
        ext = random_valid_ext(w101, rng, rng.randrange(0, 40))
        w = ext + w101
        if valid(w)[1] is not None:
            continue
        # incrementale: parti da w101 e prependi ext (dal recente all'antico)
        c, h, req = exact_state(w101)
        pend = pend_set(req)
        for i in range(len(ext) - 1, -1, -1):
            bit = ext[i]
            cn = (c[0] - DX[h], c[1] - DY[h])
            read = 0 if bit == 1 else 1
            cn2, hn, _ = exact_step(c, h, req, bit)
            assert cn2 == cn
            if read == 1:
                pend.add(cn)
            else:
                pend.discard(cn)
            c, h = cn2, hn
        # da zero
        tr = anchor_trace(w)
        fr = tr[2]
        req_scratch = {cc: 1 - g for cc, g in fr.items()}
        assert req == req_scratch, "req incrementale != da zero"
        assert pend == {cc for cc, g in fr.items() if g == 1}, "pending != fr nere"
        assert pend == pend_set(req), "pending != {req==0}"
        tested += 1
    return tested


def gateL1(rng):
    """Verita' di terra forward: pending della parola di vita == seme nero visitato."""
    res = {}
    # a. griglia vuota
    turns, n, onset, first_read, _ = simulate(set(), 0, 0, 0, 12500,
                                              stop_at_onset=False)
    assert onset_verified(turns, n) == 9977, "onset griglia vuota != 9977"
    fr = first_reads_abs(tuple(turns))
    assert fr is not None, "parola di vita irrealizzabile?!"
    pend = {c for c, g in fr.items() if g == 1}
    assert pend == set(), f"griglia vuota: pending {len(pend)} != 0"
    # cross-check indipendente col first_read del simulatore
    assert {c for c, (t, g) in first_read.items() if g == 1} == set()
    res["a_vuota"] = {"passi": n, "onset": 9977, "pending": 0}
    print("GATE L1a verde: griglia vuota, parola di vita 12500 passi, "
          "onset 9977, pending = 0", flush=True)
    # b. seme {(7,-7)}
    seed = {(7, -7)}
    turns, n, onset, first_read, _ = simulate(seed, 0, 0, 0, 110_000,
                                              stop_at_onset=False)
    assert onset_verified(turns, n) == 106258, "onset (7,-7) != 106258"
    fr = first_reads_abs(tuple(turns))
    pend = {c for c, g in fr.items() if g == 1}
    assert pend == seed, f"(7,-7): pending {pend} != seme"
    res["b_7m7"] = {"passi": n, "onset": 106258, "pending": sorted(pend)}
    print("GATE L1b verde: seme {(7,-7)}, onset 106258, pending = {(7,-7)} esatto",
          flush=True)
    # c. blob casuali: pending == nere-del-seme visitate (bilancio §92e)
    rows = []
    for k in range(10):
        side = rng.randrange(5, 12)
        dens = 0.3 + rng.random() * 0.2
        seed = set()
        half = side // 2
        for a in range(-half, half + 1):
            for b in range(-half, half + 1):
                if rng.random() < dens:
                    seed.add((a, b))
        turns, n, _, first_read, _ = simulate(seed, 0, 0, 0, 50_000,
                                              stop_at_onset=False)
        fr = first_reads_abs(tuple(turns))
        assert fr is not None
        pend = {c for c, g in fr.items() if g == 1}
        visited_black = {c for c in seed if c in fr}
        assert pend == visited_black, f"blob {k}: pending != seme nero visitato"
        # cross-check col simulatore
        assert pend == {c for c, (t, g) in first_read.items() if g == 1}
        rows.append({"side": side, "seme": len(seed),
                     "visitate": len(visited_black), "pending": len(pend)})
    res["c_blobs"] = rows
    print(f"GATE L1c verde: 10 blob, pending == seme nero visitato "
          f"(uguaglianza esatta 10/10)", flush=True)
    return res


def gateL2(w101):
    """Riproduzione ESATTA del controesempio del pannello §92e: corsa fresco=>R
    sul testimone infinite-rail: 2918 passi, 1326 L-su-rivisitata, pending 60->286."""
    rail = json.load(open(RAIL_SUM))
    f_word = to_bits(rail["escape"]["word"])
    e2 = to_bits(rail["witness"]["word_ext"])
    W = f_word + e2 + w101
    assert valid(W)[1] is None, "testimone infinite-rail non valido?!"
    r = forced_run(W)
    assert r["pend0"] == 60, f"pend0 {r['pend0']} != 60 (addendum §92e)"
    assert r["passi"] == 2918, f"passi {r['passi']} != 2918 (addendum §92e)"
    assert r["L_riv"] == 1326, f"L_riv {r['L_riv']} != 1326 (addendum §92e)"
    assert r["pend_fine"] == 286, f"pend_fine {r['pend_fine']} != 286 (§92e)"
    assert r["causa"] == "y<1"
    print(f"GATE L2 verde: corsa fresco=>R sul testimone rail: 2918 passi, "
          f"1326 L-su-rivisitata, pending 60->286, morte y<1 — bit-identica "
          f"all'addendum §92e", flush=True)
    return {"passi": r["passi"], "L_riv": r["L_riv"],
            "pend0": r["pend0"], "pend_fine": r["pend_fine"],
            "y_max": r["y_max"]}


def gateL3(w101, rng, trials=4000):
    """Lemma all-R su parole valide casuali: morte <= 5, morti al 4° tutte in coda."""
    deaths = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    tested = 0
    while tested < trials:
        ext = random_valid_ext(w101, rng, rng.randrange(0, 60))
        w = ext + w101
        if valid(w)[1] is not None:
            continue
        k, causa, cell, on_tail = allr_run(w)
        assert k is not None and k <= 5, f"all-R sopravvive oltre il 5°! ({k})"
        if k == 4:
            assert on_tail, "morte al 4° NON sulla cella di coda"
            assert causa == "irrealizzabile"
            # dicotomia del lemma (pannello §93): morte al 4° <=> prima lettura
            # della coda BIANCA (word[0] == R)
            assert w[0] == 1, "morte al 4° con coda letta nera?!"
        if k == 5:
            assert causa == "irrealizzabile"
            assert w[0] == 0, "morte al 5° con coda letta bianca?!"
        deaths[k] += 1
        tested += 1
    assert deaths[4] + deaths[5] > 0, "gate vacuo: nessuna morte 4°/5°"
    print(f"GATE L3 verde: all-R muore entro il 5° su {tested} parole "
          f"(distr. {deaths}); morti al 4° tutte sulla coda", flush=True)
    return deaths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=93)
    args = ap.parse_args()
    t0 = time.time()
    rng = random.Random(args.seed)

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])

    gates = {}
    gates["L0_parole"] = gateL0(w101, rng)
    print(f"GATE L0 verde: identita' incrementale req/pending su "
          f"{gates['L0_parole']} estensioni", flush=True)
    gates["L1"] = gateL1(rng)
    gates["L2"] = gateL2(w101)
    gates["L3_allR"] = gateL3(w101, rng)

    # profilo base: i pending che coprente+w101 lasciano (la parte w101-specifica)
    tr = anchor_trace(w101)
    pend_w101 = sorted(c for c, g in tr[2].items() if g == 1)
    print(f"\nPending di w101 da sola: {len(pend_w101)} celle "
          f"(cheb max {max(cheb(c) for c in pend_w101)})", flush=True)

    out = {"args": vars(args), "gates": gates,
           "pend_w101": {"n": len(pend_w101), "celle": pend_w101},
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nTUTTI I GATE VERDI. scritto {OUT_JSON} in {out['elapsed_s']} s",
          flush=True)


if __name__ == "__main__":
    main()
