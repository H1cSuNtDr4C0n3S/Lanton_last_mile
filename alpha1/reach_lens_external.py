# -*- coding: utf-8 -*-
"""
reach_lens_external.py — §107c, LENTE ESTERNA INDIPENDENTE per lo strumento "reach".

Checker brute-force scritto DA ZERO (nessuna logica condivisa con
alpha1/danger_reach_depth.py, MAI aperto): per i 2 lock reali
(F2[0]=LOCKA, F2[1]=LOCKB di record_divergence_hunt_summary.json) enumera per
livelli (BFS sui prefissi, chiusura per troncamento verso w) tutti i passati
validi di profondita' <= D della parola w (101 bit che terminano al record
y-min stretto) e misura, per ogni cella di R_T (frame ancora),
first_hit(cella) = profondita' minima alla quale la cella viene letta dal
passo piu' profondo appena aggiunto, su TUTTI i passati validi.

Passato valido di profondita' d = pre in {0,1}^d tale che:
  (1) pre+w REALIZZABILE (prima lettura di una cella libera; ogni rilettura
      forzata al colore alternato rispetto alla lettura precedente);
  (2) RECORD-COMPATIBILE: ogni cella letta da pre+w ha y >= 1 nel frame
      ancora (record y-min stretto; il record stesso, letto a t, non fa
      parte di w).

Moduli ground-truth usati SOLO per i DATI (episodi, parola, onset_germe, R_T):
build_seed, run_collect_records, eval_word, transient_readset_from_germ.
Walk / validazione / frame / enumerazione: riscritti qui.

CONVENZIONI DICHIARATE (con l'evidenza usata per risolverle):
 1. bit 1 = R = lettura BIANCA, bit 0 = L = lettura NERA (§95; conferma
    indipendente: record_word_census.run_collect_records fa
    color==0 -> turns.append(1)).
 2. Heading 0=su,1=destra,2=giu,3=sinistra; DX=(0,1,0,-1), DY=(-1,0,1,0)
    (coordinate schermo: "su" = y-1; fonte onset_cone_lock.py; coerente con
    l'assert h==0 ai record y-min di run_collect_records: la formica che
    scende in y viaggia con heading 0).
 3. Ordine del passo: lettura -> svolta -> flip -> mossa (CLAUDE.md §2).
 4. FRAME ANCORA: trasla la posa finale del cammino in origine e ruota di
    k=(-h_finale)%4 rotazioni ORARIE (x,y)->(-y,x); questa rotazione manda
    delta(h) in delta(h+1) (check: delta(0)=(0,-1) -> (1,0)=delta(1)).
    Direzione verificata (trappola kk) su DUE binari: (i) caso-giocattolo
    word="R" (gate GV0: la cella letta finisce a (0,1), dietro la formica);
    (ii) gate GV1 su entrambe le parole reali: cammino in avanti + rotazione
    == cammino all'indietro dalla posa ancora, lettura per lettura.
    NB: il cammino all'indietro parte da (0,0,0) perche' ai record y-min
    l'heading ASSOLUTO e' 0 (assert di run_collect_records); il cammino in
    avanti invece parte con heading 0 all'inizio di w, quindi il suo frame
    e' ruotato di k_rot != 0 in generale: GV1 esercita davvero la rotazione.
 5. CAVEAT §107b.6 (dichiarato): onset_germe e' misurato DAL RECORD (il
    germe parte dall'origine ancora = posa del record); sull'asse temporale
    della parola l'onset cade a og+101.
 6. Profondita': il passo adiacente a w ha profondita' 1; pre[0] e' il piu'
    profondo. first_hit e' registrato al livello BFS del passo appena
    aggiunto (chiusura per troncamento: se un passato valido di prof. d
    legge la cella a prof. j<d, il troncamento agli ultimi j bit e' un
    passato valido che la legge a prof. j => il minimo per livelli e' esatto).

Sanity che DEVONO passare (e possono fallire, trappola bb):
  (a) nodes_per_depth["0"] = 1 (contenuto reale: w stessa realizzabile e
      record-compatibile per la MIA verifica, non solo per eval_word);
  (b) |R_T| = 14 (LOCKA) e 9 (LOCKB);
  (c) onset_germe = 55 (LOCKA) e 65 (LOCKB);
  (d) LOCKA: first_hit[(-1, 5)] = 1.

Esecuzione:  C:\\Python\\Python310\\python.exe alpha1\\reach_lens_external.py
(cwd C:\\Lanton_last_mile). Uscita: alpha1/reach_lens_external.json.
"""
import sys, os, json, time

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# --- ground truth: SOLO DATI --------------------------------------------------
from delta4_long_orbits import build_seed
from record_word_census import run_collect_records
from record_weapon_hunt import eval_word
from speed_limit_theorem import transient_readset_from_germ

SUMMARY = os.path.join(HERE, "record_divergence_hunt_summary.json")
CHECK_A = os.path.join(HERE, "locka_d16_check.json")   # dati §107b, cross-check post-hoc
OUT = os.path.join(HERE, "reach_lens_external.json")

# --- convenzioni locali (riscritte, vedi header) --------------------------------
DX = (0, 1, 0, -1)
DY = (-1, 0, 1, 0)


def forward_walk(word):
    """Cammino in avanti da (0,0,0): prima lettura libera (colore dichiarato dal
    bit), rilettura vincolata al colore corrente (alternanza via flip).
    Ritorna (reads=[(cella,colore),...], end_pose) o (None, None)."""
    grid = {}
    x = y = 0
    h = 0
    reads = []
    for bit in word:
        c = (x, y)
        col = 0 if bit else 1            # 1=R legge BIANCO(0), 0=L legge NERO(1)
        if c in grid and grid[c] != col:
            return None, None            # rilettura contraddittoria
        reads.append((c, col))
        grid[c] = 1 - col                # flip dopo la lettura
        h = (h + 1) & 3 if bit else (h + 3) & 3
        x += DX[h]
        y += DY[h]
    return reads, (x, y, h)


def rot_cw(p):
    """Rotazione oraria di 90 gradi (coordinate schermo): delta(h) -> delta(h+1)."""
    return (-p[1], p[0])


def to_anchor(cells, end_pose):
    """Frame ancora: trasla end_pose in origine, poi k=(-h)%4 rotazioni orarie.
    Ritorna (celle trasformate, k)."""
    x0, y0, h0 = end_pose
    k = (-h0) % 4
    out = []
    for (cx, cy) in cells:
        p = (cx - x0, cy - y0)
        for _ in range(k):
            p = rot_cw(p)
        out.append(p)
    return out, k


def back_step(pose, bit):
    """Passo ALL'INDIETRO. pose = (x,y,h) della formica DOPO il passo che
    ricostruiamo (posizione della lettura successiva, heading d'arrivo).
    Quel passo ha mosso in direzione h, quindi ha letto (x,y)-delta(h);
    la svolta era R (h-1 -> h) se bit=1, L (h+1 -> h) se bit=0.
    Ritorna (cella_letta, colore_letto, pose_prima)."""
    x, y, h = pose
    cx, cy = x - DX[h], y - DY[h]
    if bit:
        return (cx, cy), 0, (cx, cy, (h - 1) & 3)
    return (cx, cy), 1, (cx, cy, (h + 1) & 3)


def backward_reads_w(word):
    """Cammino all'indietro dell'intera parola dalla posa ancora (0,0,0) (=il
    record: y-min stretto => heading assoluto 0). Le celle escono direttamente
    in frame ancora. Ritorna (reads in ordine temporale, pose_pre_w)."""
    pose = (0, 0, 0)
    rev = []
    for bit in reversed(word):
        cell, col, pose = back_step(pose, bit)
        rev.append((cell, col))
    return rev[::-1], pose


def gate_gv0():
    """GV0 (trappola kk): caso-giocattolo word='R'. In avanti: legge (0,0)
    bianca, end_pose (1,0,1), k=3; l'ancora della cella letta deve essere
    (0,1) (dietro la formica che guarda 'su'). All'indietro da (0,0,0):
    stessa cella (0,1), stesso colore 0."""
    reads_f, endp = forward_walk((1,))
    assert reads_f is not None
    anc, k = to_anchor([c for c, _ in reads_f], endp)
    assert anc == [(0, 1)], f"GV0 avanti+rotazione: {anc}"
    assert k == 3, f"GV0 k: {k}"
    reads_b, pose_pre = backward_reads_w((1,))
    assert reads_b == [((0, 1), 0)], f"GV0 indietro: {reads_b}"
    assert pose_pre == (0, 1, 3), f"GV0 pose_pre: {pose_pre}"


def bfs_reach(word, targets, depth_max):
    """BFS per livelli sui prefissi validi di word. Ritorna
    (nodes_per_depth, first_hit, foot_w, pose_pre_w, k_rot, extinct_at)."""
    # gate GV1: frame/chiralita' (kk) — avanti+rotazione == indietro
    reads_f, endp = forward_walk(word)
    assert reads_f is not None, "w irrealizzabile per la MIA verifica di alternanza"
    anc_cells, k_rot = to_anchor([c for c, _ in reads_f], endp)
    reads_b, pose_pre_w = backward_reads_w(word)
    assert anc_cells == [c for c, _ in reads_b], "GV1: celle avanti/indietro divergono"
    assert [c for _, c in reads_f] == [c for _, c in reads_b], "GV1: colori divergono"
    endp_anc, _ = to_anchor([endp[:2]], endp)
    assert endp_anc[0] == (0, 0), "GV1: la posa finale non va in origine"

    # record-compat di w (y>=1) + footprint + colore della PRIMA lettura
    foot = {c for c, _ in reads_b}
    bad = [c for c in foot if c[1] < 1]
    assert not bad, f"cella di w a y<1 nel frame ancora?! {bad}"
    first_color = {}
    for c, col in reads_b:
        if c not in first_color:
            first_color[c] = col

    tset = set(targets)
    first_hit = {c: None for c in targets}
    nodes = [(pose_pre_w, {})]           # (pose_between, overlay prima-lettura)
    npd = {0: 1}
    extinct_at = None
    for d in range(1, depth_max + 1):
        nxt = []
        for pose, ov in nodes:
            for bit in (0, 1):
                cell, col, pb = back_step(pose, bit)
                if cell[1] < 1:
                    continue             # record-compat: y>=1 nel frame ancora
                prev = ov.get(cell, first_color.get(cell))
                if prev is not None and col != 1 - prev:
                    continue             # alternanza violata verso la lettura successiva
                ov2 = dict(ov)
                ov2[cell] = col          # la nuova lettura e' ora la piu' antica
                nxt.append((pb, ov2))
                if cell in tset and first_hit[cell] is None:
                    first_hit[cell] = d
        nodes = nxt
        npd[d] = len(nodes)
        if not nodes:
            extinct_at = d
            for dd in range(d + 1, depth_max + 1):
                npd[dd] = 0
            break
    return npd, first_hit, foot, pose_pre_w, k_rot, extinct_at


def run_episode(name, entry, depth, expect_og, expect_nrt):
    t0 = time.time()
    print(f"\n=== {name}: rngstate={entry['rngstate']} t={entry['t']} "
          f"depth={depth} ===")
    seed, _, _ = build_seed(int(entry["rngstate"]), 5, 25)
    turns, t_on, records = run_collect_records(seed)
    # gate dati (ground truth vs summary)
    assert t_on == entry["t_on"], f"onset {t_on} != {entry['t_on']}"
    rec = [r for r in records if r[0] == entry["t"]]
    assert len(rec) == 1, f"record a t={entry['t']} non trovato"
    _, rx, ry = rec[0]
    assert [rx, ry] == list(entry["pose"]), f"posa {(rx, ry)} != {entry['pose']}"
    t = int(entry["t"])
    w = tuple(turns[t - 101:t])
    ws = "".join("R" if b else "L" for b in w)
    assert ws == entry["word"], "parola ricostruita != campo 'word' del summary"

    ev = eval_word(w)                     # ground truth (og)
    assert ev is not None, "eval_word boccia w?!"
    og = ev[1]
    assert og == expect_og == entry["onset_germe"], \
        f"onset_germe {og} != atteso {expect_og} / summary {entry['onset_germe']}"
    rt = [tuple(c) for (c, _tf) in transient_readset_from_germ(w, og)]
    assert len(rt) == expect_nrt, f"|R_T| = {len(rt)} != atteso {expect_nrt}"
    assert all(cy >= 1 for (_, cy) in rt), "cella di R_T a y<1?!"

    npd, first_hit, foot, pose_pre_w, k_rot, extinct = bfs_reach(w, rt, depth)
    assert not (set(rt) & foot), "R_T interseca il footprint di w?!"
    assert npd[0] == 1                    # sanity (a): prefisso vuoto valido

    el = time.time() - t0
    rt_sorted = sorted(rt)
    print(f"  onset_germe = {og} (misurato DAL RECORD; asse parola = og+101)")
    print(f"  |R_T| = {len(rt)} | k_rot(parola->ancora) = {k_rot} | "
          f"pose_pre_w = {pose_pre_w}")
    print(f"  nodes_per_depth: {[npd[d] for d in range(depth + 1)]}")
    if extinct is not None:
        print(f"  !! albero ESTINTO a profondita' {extinct} (cap non raggiunto)")
    for c in rt_sorted:
        fh = first_hit[c]
        print(f"    first_hit{str(c):>10} = {fh if fh is not None else '-- (mai <= ' + str(depth) + ')'}")
    n_unr = sum(1 for c in rt if first_hit[c] is None)
    print(f"  celle mai raggiunte a prof. <= {depth}: {n_unr}/{len(rt)}")
    print(f"  tempo: {el:.2f} s")

    return {
        "depth": depth,
        "nodes_per_depth": {str(d): npd[d] for d in range(depth + 1)},
        "first_hit_anchor": {str(c): first_hit[c] for c in rt_sorted},
        "unreached_at_depth": [str(c) for c in rt_sorted if first_hit[c] is None],
    }, el, k_rot, extinct


def crosscheck_locka(res_a):
    """Cross-check post-hoc DICHIARATO con i dati §107b (locka_d16_check.json):
    (i) nodi per profondita' bit-identici; (ii) insieme celle identico;
    (iii) coerenza cell_bits: cella decisa in >=1 passato al cap (nero+bianco>0)
    => first_hit non nullo. NB (iii) e' solo unidirezionale: un first_hit basso
    con cella indecisa in tutti i passati al cap NON e' contraddittorio (il nodo
    che la legge puo' morire prima del cap — trappola rr)."""
    if not os.path.exists(CHECK_A):
        print("\n[cross-check] locka_d16_check.json assente: salto (dichiarato).")
        return "assente"
    ck = json.load(open(CHECK_A))
    ok = True
    mine = res_a["nodes_per_depth"]
    theirs = ck.get("nodi_per_depth", {})
    if mine != {k: v for k, v in theirs.items()}:
        ok = False
        print(f"\n[cross-check] MISMATCH nodi_per_depth:\n  mio:    {mine}\n  §107b: {theirs}")
    cells_mine = set(res_a["first_hit_anchor"])
    cells_theirs = set(ck.get("cell_bits", {}))
    if cells_mine != cells_theirs:
        ok = False
        print(f"\n[cross-check] MISMATCH celle R_T: solo-mie {cells_mine - cells_theirs}, "
              f"solo-§107b {cells_theirs - cells_mine}")
    for c, bits in ck.get("cell_bits", {}).items():
        decided = bits[0] + bits[1] > 0
        if decided and res_a["first_hit_anchor"].get(c) is None:
            ok = False
            print(f"[cross-check] INCOERENZA: {c} decisa al cap §107b ma first_hit nullo")
    print(f"\n[cross-check locka_d16_check.json] {'VERDE (bit-identico)' if ok else 'ROSSO'}")
    return "verde" if ok else "rosso"


def main():
    t_all = time.time()
    gate_gv0()
    print("GV0 (rotazione ancora, caso-giocattolo 'R'): verde")

    F2 = json.load(open(SUMMARY))["F2"]
    locka, lockb = F2[0], F2[1]

    out = {}
    res_a, el_a, k_a, ext_a = run_episode("LOCKA", locka, 16, expect_og=55, expect_nrt=14)
    # sanity (d): (-1,5) letta al primo passo all'indietro da ogni passato
    fh = res_a["first_hit_anchor"].get("(-1, 5)")
    assert fh == 1, f"sanity (d) FALLITA: first_hit[(-1,5)] = {fh} != 1"
    print("  sanity (d) LOCKA first_hit[(-1, 5)] = 1: verde")
    out["LOCKA"] = res_a

    res_b, el_b, k_b, ext_b = run_episode("LOCKB", lockb, 14, expect_og=65, expect_nrt=9)
    out["LOCKB"] = res_b

    cc = crosscheck_locka(res_a)

    out["_meta"] = {
        "strumento": "reach_lens_external.py — lente esterna indipendente §107c",
        "caveat_onset_germe": "misurato DAL RECORD (germe dall'origine ancora); "
                              "asse della parola = og+101 (§107b.6)",
        "frame": "ancora = trasla posa finale in origine + k=(-h)%4 rotazioni "
                 "orarie (x,y)->(-y,x); GV0/GV1 verdi; heading assoluto al "
                 "record = 0 (assert run_collect_records)",
        "k_rot_parola": {"LOCKA": k_a, "LOCKB": k_b},
        "estinzione": {"LOCKA": ext_a, "LOCKB": ext_b},
        "cap_dichiarato": {"LOCKA": 16, "LOCKB": 14},
        "crosscheck_locka_d16": cc,
        "tempo_s": {"LOCKA": round(el_a, 2), "LOCKB": round(el_b, 2),
                    "totale": round(time.time() - t_all, 2)},
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(f"\nScritto {OUT} | tempo totale {time.time() - t_all:.2f} s")


if __name__ == "__main__":
    main()
