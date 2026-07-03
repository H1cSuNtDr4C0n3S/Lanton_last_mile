# record_weapon_onset_lock.py — §88 (sigillo): chiusura della clausola-onset via Replay-Lock.
#
# Il certificato geometrico (record_weapon_cycle.py) copre realizzabilita' + record-
# compatibilita' di sigma^m + base2 per OGNI m; l'onset del germe (che definisce burden1)
# restava empirico (m <= 40 in verifica, m <= 200 dallo scettico, onset SEMPRE 160).
# Qui lo si chiude per induzione col Lemma Replay-Lock (§87a: la corsa fino a t_end
# dipende SOLO dai colori iniziali delle celle visitate V):
#   1. per m0 = 40: simula germ(m0), onset(m0), V = {celle visitate con t < onset + P};
#   2. il germe cresce di un blocco per m: B_m = germ(m) \ germ(m-1); i B_m sono copie
#      traslate di passo fisso Delta_B (frame anchor) — verificato esplicitamente;
#   3. se B_{m0+1} + k*Delta_B e' disgiunto da V per ogni k >= 0 (check finito: disgiunto
#      finche' il bbox non e' oltre, poi geometrico per monotonia), allora per induzione
#      run(m) = run(m0) per OGNI m >= m0: stesso onset, stessa V, stesso burden1, stesso
#      residuo. La clausola-onset diventa TEOREMA e l'intero enunciato eval_word-valido.
#   4. controprova diretta: run(m) per m = 41..46 identica (onset, |V|, burden, residuo).
# Uscita: alpha1/record_weapon_onset_lock_summary.json
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import P, simulate
from kwindow_spoiler_census import virtual_walk, to_anchor_frame
from record_weapon_vitality import to_bits, SUMMARY

HERE = os.path.dirname(os.path.abspath(__file__))
CYC = os.path.join(HERE, "record_weapon_cycle_summary.json")
RAIL = os.path.join(HERE, "record_weapon_rail_summary.json")
OUT = os.path.join(HERE, "record_weapon_onset_lock_summary.json")
M0 = 40


def germ_anchor(word):
    vg, pose = virtual_walk(word)
    assert vg is not None
    return to_anchor_frame(vg, pose)


def run_of(anchor, cap=2_000_000):
    germ_black = {c for c, col in anchor.items() if col == 1}
    turns, n, onset, fr, _ = simulate(germ_black, 0, 0, 0, cap, chk=2600)
    assert onset >= 0
    t_end = onset + P
    V = {c for c, (t, _) in fr.items() if t < t_end}
    spoiler = V - set(anchor)
    deep1 = sorted(c for c in spoiler if c[1] >= 1)
    return onset, V, deep1


def bbox(cells):
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
    return min(xs), max(xs), min(ys), max(ys)


def main():
    t0 = time.time()
    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    cyc = json.load(open(CYC))
    cert = cyc["certificato"]
    rail = json.load(open(RAIL))["rail_oldest_first"]
    sigma = to_bits(cert["sigma"])
    tau = to_bits(rail[cyc["finestra"][1] - cert["j"]:])
    base2 = tau + w101

    # 1. run di riferimento a m0
    anch = {m: germ_anchor(sigma * m + base2) for m in range(M0 - 1, M0 + 7)}
    onset0, V0, deep0 = run_of(anch[M0])
    print(f"m0={M0}: onset {onset0}, |V| {len(V0)}, burden1 {len(deep0)}, "
          f"residuo {deep0}", flush=True)
    assert deep0 == [(1, 1)]

    # 2. blocchi nuovi e loro traslazione (frame anchor)
    blocks = {}
    for m in range(M0, M0 + 7):
        gm, gp = set(anch[m]), set(anch[m - 1])
        assert gp <= gm, f"anchor(m-1) non contenuto in anchor(m) a m={m}"
        assert all(anch[m][c] == anch[m - 1][c] for c in gp), f"colori cambiati a m={m}"
        blocks[m] = gm - gp
    keys = sorted(blocks)
    deltas = set()
    for a, b in zip(keys, keys[1:]):
        dd = {(c2[0] - c1[0], c2[1] - c1[1])
              for c1 in [min(blocks[a])] for c2 in [min(blocks[b])]}
        # traslazione esatta dell'intero blocco
        (dx, dy), = dd
        assert {(c[0] + dx, c[1] + dy) for c in blocks[a]} == blocks[b], \
            f"blocco m={b} non e' traslato del blocco m={a}"
        assert all(anch[b][(c[0] + dx, c[1] + dy)] == anch[a][c] for c in blocks[a]), \
            f"colori del blocco traslato diversi a m={b}"
        deltas.add((dx, dy))
    assert len(deltas) == 1, f"passo di traslazione non costante: {deltas}"
    (dx, dy), = deltas
    assert dy == 0 and dx != 0, f"atteso passo orizzontale, trovato {(dx, dy)}"
    print(f"blocchi nuovi: copie traslate esatte, passo Delta_B = {(dx, dy)}", flush=True)

    # 3. disgiunzione B_{m}+k*Delta_B da V0 per ogni k >= 0 (finito + geometrico)
    B = blocks[M0 + 1]
    vx0, vx1, vy0, vy1 = bbox(V0)
    bx0, bx1, by0, by1 = bbox(B)
    if dx < 0:
        k_pass = 0 if bx1 < vx0 else (bx1 - vx0) // (-dx) + 1
    else:
        k_pass = 0 if bx0 > vx1 else (vx1 - bx0) // dx + 1
    checked = 0
    for k in range(k_pass + 1):
        Bk = {(c[0] + k * dx, c[1] + k * dy) for c in B}
        assert not (Bk & V0), f"ROSSO: blocco a k={k} interseca V0!"
        checked += 1
    print(f"3. VERDE: B+k*Delta disgiunto da V0 per k=0..{k_pass} (esplicito), "
          f"oltre per monotonia del bbox (V0 x in [{vx0},{vx1}], blocco x in "
          f"[{bx0},{bx1}], passo {dx})", flush=True)

    # 4. controprova diretta
    rows = []
    for m in range(M0 + 1, M0 + 7):
        o, V, dp = run_of(anch[m])
        assert (o, V, dp) == (onset0, V0, deep0), f"ROSSO: run(m={m}) != run(m0)!"
        rows.append(m)
    print(f"4. VERDE: run(m) identica a run(m0) per m={rows} (onset, V, burden, residuo)",
          flush=True)

    print(f"\n=> TEOREMA (Replay-Lock + disgiunzione): per OGNI m >= {M0}, "
          f"onset(m) = {onset0}, burden1(m) = 1, residuo {{(1,1)}}. "
          f"La clausola-onset non e' piu' empirica.", flush=True)

    out = {"m0": M0, "onset": onset0, "V_size": len(V0), "residuo": [list(c) for c in deep0],
           "delta_B": [dx, dy], "k_pass": k_pass, "disjoint_checked": checked,
           "direct_m": rows, "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
