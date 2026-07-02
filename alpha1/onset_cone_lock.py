# onset_cone_lock.py — §87a: il LOCK ESATTO dell'ingresso (Cono Bianco) e il Lemma del Replay-Lock.
#
# Idea (estensione diretta di word_lock.py §86b dalla parola astratta alla CORSA reale):
#   LEMMA DEL REPLAY-LOCK. Sia data una corsa finita di T passi da posa (x,y,h) su ambiente E.
#   Sia V_T l'insieme delle celle LETTE (= visitate) durante la corsa, con i colori che avevano
#   in E al tempo 0 (ogni prima lettura legge il colore iniziale; le riletture leggono scrittura
#   propria). Allora per OGNI ambiente E' che coincide con E su V_T, la corsa da (x,y,h) su E'
#   produce la STESSA parola di svolte e la stessa traiettoria per T passi (sufficienza), e
#   cambiare il colore iniziale di UNA QUALSIASI cella di V_T cambia la svolta alla sua prima
#   lettura (necessita' per-cella). V_T con i suoi colori e' quindi il lock esatto della corsa.
#   Dimostrazione: induzione sui passi — al passo t la cella letta o e' alla prima lettura
#   (colore = iniziale, uguale per ipotesi) o e' una rilettura (colore = ultima scrittura della
#   formica, uguale per induzione). QED.
#
# Applicazione: §76 ha stabilito che la GRIGLIA VUOTA entra in autostrada a onset 9977 e che
# UNA cella nera in (0,-2) entra a 310. Il Replay-Lock trasforma questi fatti in LEMMI DEL CONO:
#   - CONO BIANCO: se in un istante qualunque di un'orbita qualunque tutte le celle di
#     V_T(posa) (traslato/ruotato sulla posa corrente) sono bianche, l'orbita replica la corsa
#     vuota => onset entro 9977 passi. Contrappositiva per Link 1: un'orbita eterna non-highway
#     deve avere, IN OGNI ISTANTE, almeno un nero dentro V_T(posa(t)).
#   - CONO A UN NERO: idem con 1 nero in (0,-2) relativo => onset entro 310 passi. Etc. (b=2,3).
#
# L'eternita' del cono: dopo l'onset la highway consuma territorio con AFFITTO PERIODICO —
# le celle nuove per periodo devono diventare un insieme fisso nel frame co-moving (drift
# (+-2,+-2)/104). Se l'affitto e' esattamente periodico (GATE qui), il lock eterno e'
# finitamente descritto: BLOB (fino all'onset+rodaggio) + STRISCIA periodica semi-infinita.
#
# Misure:
#   1. gate onset: vuota 9977, b1 310, b2 162, b3 142, (7,-7) 106258 (riferimenti §76/§79);
#   2. lock: |V| al onset (blob), raggio Chebyshev, per-periodo celle nuove (affitto), periodo
#      di stabilizzazione p0 dell'affitto (co-moving, gate esatto), drift;
#   3. scia: le 3 celle di scia dietro la posa iniziale appartengono al blob? (aggancio §86);
#   4. SELF-TEST §5: sufficienza (1000 ambienti junk fuori V_T => parola identica),
#      necessita' (200 flip dentro V_T => parola uguale fino alla prima lettura, diversa li');
#   5. tripwire: colori del lock == seme ristretto a V_T (nessun nero del seme fuori uso:
#      seme ⊆ V_T, altrimenti il "germe" dichiarato e' sovradimensionato).
#
# Convenzioni: identiche ad alpha1_engine.c / libant.c (bianco -> R=+1 orario, turns 1=R 0=L;
# DX/DY schermo, h=0 su; onset_verified: coda 104-periodica >=2080, estensione all'indietro,
# rot%4==0, drift != 0). Uscita: alpha1/onset_cone_lock_summary.json.
import sys, os, json, time, random

DX = (0, 1, 0, -1); DY = (-1, 0, 1, 0)
P = 104
LWIN = 2080          # >=20 periodi di coda (convenzione alpha1_engine.c)
KCERT = 20           # periodi post-onset tenuti nel lock

def rot1(p):
    x, y = p
    return (-y, x)   # quarto di giro orario (coordinate schermo)

def rotk(p, k):
    for _ in range(k % 4):
        p = rot1(p)
    return p

def onset_verified(turns, n):
    """Porta esatta di onset_verified() da alpha1_engine.c."""
    if n < 2600:
        return -1
    for i in range(n - LWIN, n - P):
        if turns[i] != turns[i + P]:
            return -1
    onset = n - LWIN
    while onset > 0 and turns[onset - 1] == turns[onset - 1 + P]:
        onset -= 1
    if n - onset < 520:
        return -1
    h = 0; x = 0; y = 0; rot = 0
    for s in range(onset, onset + P):
        if turns[s]:
            h = (h + 1) & 3; rot += 1
        else:
            h = (h + 3) & 3; rot -= 1
        x += DX[h]; y += DY[h]
    if rot % 4 != 0:
        return -1
    if x == 0 and y == 0:
        return -1
    return onset

def simulate(seed_black, x, y, h, max_steps, stop_at_onset=True, chk=20000,
             junk=None):
    """Corsa con tracking prima-lettura. junk: dict cella->colore per celle FUORI dal
    dominio del seme (usato dai self-test); il colore iniziale di una cella e':
    junk.get(c, 1 se c in seed_black else 0). Ritorna (turns bytearray, n, onset,
    first_read: dict cella->(indice_passo, colore_iniziale), traj_end=(x,y,h))."""
    grid = {}                      # celle toccate: colore corrente
    first_read = {}
    turns = bytearray()
    seed = seed_black
    jk = junk or {}
    t = 0
    while t < max_steps:
        c = (x, y)
        if c in grid:
            color = grid[c]
        else:
            color = jk.get(c, 1 if c in seed else 0)
            first_read[c] = (t, color)
        if color == 0:
            h = (h + 1) & 3
            grid[c] = 1
            turns.append(1)
        else:
            h = (h + 3) & 3
            grid[c] = 0
            turns.append(0)
        x += DX[h]; y += DY[h]
        t += 1
        if stop_at_onset and t >= 2600 and (t % chk) == 0:
            o = onset_verified(turns, t)
            if o >= 0:
                return turns, t, o, first_read, (x, y, h)
    o = onset_verified(turns, t) if t >= 2600 else -1
    return turns, t, o, first_read, (x, y, h)

def cheb(c):
    return max(abs(c[0]), abs(c[1]))

def lock_of(seed, name, ref_onset, extra_periods=KCERT):
    """Corsa fino a onset + coda; restituisce il lock (V con colori) e l'anatomia."""
    t0 = time.time()
    turns, n, onset, fr, _ = simulate(seed, 0, 0, 0, 4_000_000)
    assert onset >= 0, f"{name}: onset non trovato"
    gate = (onset == ref_onset)
    # estensione: garantiamo copertura fino a onset + extra_periods*P
    t_end = onset + extra_periods * P
    assert n >= t_end, f"{name}: corsa troppo corta ({n} < {t_end})"
    # anatomia del lock
    blob = [c for c, (t, _) in fr.items() if t < onset]
    per_period_new = []
    per_period_cells = []
    for p in range(extra_periods):
        cells = [c for c, (t, _) in fr.items() if onset + p * P <= t < onset + (p + 1) * P]
        per_period_new.append(len(cells))
        per_period_cells.append(cells)
    # drift per periodo dalla parola all'onset (heading REALE all'onset, non 0:
    # h(t) = h0 + #R - #L mod 4 — un heading sbagliato ruota il drift e rompe il
    # confronto co-moving dell'affitto)
    h = 0
    for s in range(onset):
        h = (h + 1) & 3 if turns[s] else (h + 3) & 3
    dx = 0; dy = 0
    for s in range(onset, onset + P):
        if turns[s]:
            h = (h + 1) & 3
        else:
            h = (h + 3) & 3
        dx += DX[h]; dy += DY[h]
    # stabilizzazione dell'affitto: primo periodo p0 tale che per ogni p>=p0 le celle nuove
    # del periodo p+1 == celle nuove del periodo p traslate del drift
    p0 = None
    for p in range(extra_periods - 1):
        ok = True
        for q in range(p, extra_periods - 1):
            a = {(cx + dx, cy + dy) for (cx, cy) in per_period_cells[q]}
            if a != set(per_period_cells[q + 1]):
                ok = False
                break
        if ok:
            p0 = p
            break
    # scia dietro la posa iniziale (heading 0 = su): celle {(0,1),(-1,1),(-1,0)}
    trail = [(0, 1), (-1, 1), (-1, 0)]
    trail_in_blob = [c in fr and fr[c][0] < onset for c in trail]
    # colori del lock
    n_black = sum(1 for c, (t, col) in fr.items() if col == 1 and t < t_end)
    n_white = sum(1 for c, (t, col) in fr.items() if col == 0 and t < t_end)
    seed_unread = [c for c in seed if c not in fr]
    res = {
        "name": name, "onset": onset, "ref_onset": ref_onset, "gate_onset": gate,
        "lock_cells_total": len([1 for c, (t, _) in fr.items() if t < t_end]),
        "lock_blacks": n_black, "lock_whites": n_white,
        "seed_unread": [list(c) for c in seed_unread],
        "blob_cells": len(blob), "blob_radius_cheb": max((cheb(c) for c in blob), default=0),
        "rent_per_period": per_period_new,
        "rent_p0": p0,
        "rent_stable_size": per_period_new[p0] if p0 is not None else None,
        "drift_per_period": [dx, dy],
        "trail_cells_in_blob": trail_in_blob,
        "elapsed_s": round(time.time() - t0, 2),
    }
    return res, turns, fr, onset, t_end

def selftest_replay(seed, turns_ref, fr, t_end, n_junk=1000, n_flip=200, rng_seed=87):
    """Sufficienza: junk arbitrario fuori V => parola identica per t_end passi.
    Necessita': flip di una cella di V => parola uguale fino alla sua prima lettura, poi diversa."""
    rng = random.Random(rng_seed)
    V = {c for c, (t, _) in fr.items() if t < t_end}
    Rv = max(cheb(c) for c in V) + 30
    ref_word = bytes(turns_ref[:t_end])
    # sufficienza
    for i in range(n_junk):
        junk = {}
        dens = rng.random() * 0.6 + 0.05
        for _ in range(rng.randrange(50, 400)):
            c = (rng.randrange(-Rv, Rv + 1), rng.randrange(-Rv, Rv + 1))
            if c not in V:
                junk[c] = 1 if rng.random() < dens else 0
        tt, n, _, _, _ = simulate(seed, 0, 0, 0, t_end, stop_at_onset=False, junk=junk)
        if bytes(tt[:t_end]) != ref_word:
            return False, f"sufficienza violata al junk {i}"
    # necessita'
    cells = sorted(V, key=lambda c: fr[c][0])
    picks = [cells[rng.randrange(len(cells))] for _ in range(n_flip)]
    for c in picks:
        t_first, col = fr[c]
        # flip: se la cella e' del seme la togliamo, altrimenti la aggiungiamo come junk nera
        if col == 1:
            seed2 = set(seed) - {c}
            junk = {}
        else:
            seed2 = set(seed)
            junk = {c: 1}
        tt, n, _, _, _ = simulate(seed2, 0, 0, 0, min(t_first + 1, t_end),
                                  stop_at_onset=False, junk=junk)
        if bytes(tt[:t_first]) != ref_word[:t_first]:
            return False, f"necessita': prefisso cambiato prima della prima lettura di {c}"
        if tt[t_first] == ref_word[t_first]:
            return False, f"necessita': svolta NON cambiata alla prima lettura di {c}"
    return True, "OK"

def main():
    out = {"convention": "alpha1_engine.c / libant.c; onset coda 104-periodica >=2080, "
                         "estensione indietro, rot%4==0, drift!=0",
           "lemma": "Replay-Lock: V_T coi colori iniziali e' il lock esatto (<=>) della corsa",
           "cases": [], "selftests": {}}
    t0 = time.time()

    cases = [
        ("vuota", set(), 9977),
        ("b1_(0,-2)", {(0, -2)}, 310),
        ("b2", {(-1, 3), (1, 3)}, 162),
        ("b3", {(1, -3), (-2, -1), (-1, -1)}, 142),
        ("(7,-7)", {(7, -7)}, 106258),
    ]
    locks = {}
    for name, seed, ref in cases:
        res, turns, fr, onset, t_end = lock_of(seed, name, ref)
        out["cases"].append(res)
        locks[name] = (seed, turns, fr, t_end)
        print(f"[{name}] onset {res['onset']} (rif {ref}) gate {'OK' if res['gate_onset'] else 'ROSSO'}"
              f" | lock {res['lock_cells_total']} celle ({res['lock_blacks']}N/{res['lock_whites']}B)"
              f" | blob {res['blob_cells']} r{res['blob_radius_cheb']}"
              f" | affitto p0={res['rent_p0']} taglia {res['rent_stable_size']}"
              f" | drift {res['drift_per_period']} | scia-in-blob {res['trail_cells_in_blob']}")
        sys.stdout.flush()

    gates = all(c["gate_onset"] for c in out["cases"])
    print(f"GATE ONSET (5 riferimenti §76/§79): {'OK' if gates else 'ROSSO: FERMARSI'}")
    assert gates

    # self-test Replay-Lock sul caso b1 (piccolo) e sul caso vuota (grande, meno junk)
    seed, turns, fr, t_end = locks["b1_(0,-2)"]
    ok1, msg1 = selftest_replay(seed, turns, fr, t_end, n_junk=1000, n_flip=200)
    print(f"SELF-TEST Replay-Lock b1 (1000 junk + 200 flip): {msg1}")
    assert ok1, msg1
    seed, turns, fr, t_end = locks["vuota"]
    ok2, msg2 = selftest_replay(seed, turns, fr, t_end, n_junk=100, n_flip=60)
    print(f"SELF-TEST Replay-Lock vuota (100 junk + 60 flip): {msg2}")
    assert ok2, msg2
    out["selftests"] = {"replay_b1": msg1, "replay_vuota": msg2}

    # tripwire: seme interamente letto (nessun nero dichiarato inutile)
    for c in out["cases"]:
        assert not c["seed_unread"], f"seme non letto in {c['name']}: {c['seed_unread']}"
    print("TRIPWIRE seme⊆V: OK (tutti i neri dichiarati sono letti)")

    out["elapsed_s"] = round(time.time() - t0, 1)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "onset_cone_lock_summary.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {path} in {out['elapsed_s']} s")

if __name__ == "__main__":
    main()
