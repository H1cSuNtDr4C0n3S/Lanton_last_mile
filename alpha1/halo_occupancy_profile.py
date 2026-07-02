# halo_occupancy_profile.py — §86a: anatomia dell'occupazione dell'halo ai deep-black.
# §85 ha ridotto l'evitamento totale di (LRRRR)^3 all'invariante ambientale "nessun deep-black
# presenta le 9 celle-halo tutte bianche" (0 / 2.323.679 deep_1). Qui si misura PERCHE':
#   1. distribuzione del numero k_r di neri nell'halo ai deep_1 (minimo empirico: se >=2
#      l'enunciato vero e' piu' forte del necessario);
#   2. tassi per-cella (frame heading-su): esiste una cella dominante? in particolare (0,1)
#      e' la cella di ARRIVO (bianca <=> svolta precedente L) — se la svolta precedente fosse
#      sempre R ai deep-event l'invariante sarebbe banale;
#   3. bilancio scrittura->rilettura: k_w dallo snapshot 5x5 preso all'ultima scrittura del
#      nero profondo, Delta = k_r - k_w; classificazione dei neri-halo alla rilettura in
#      SOPRAVVISSUTI intatti (ultimo tocco <= t_w), CHURNED (toccati nell'intervallo, neri ora),
#      SEED (mai visitati). Dicotomia chiave: se s>=1 sempre, l'ambiente alla scrittura basta;
#      se esistono eventi s=0, il rifornimento e' dinamico (frontiera B-T) e serve un argomento
#      d'intervallo;
#   4. recenza: eta' minima dei neri-halo (quanto e' vicina nel tempo l'attivita' che nutre
#      l'halo) — legame Lemma del morso / frontiera B-T;
#   5. omogeneita' (trappola q): k_r medio per bucket d'eta' del nero profondo.
#
# Tripwire (auto-verifica del TEOREMA HALO §85c su dati reali): per OGNI lettura nera con
# futuro pieno di 15 passi, (parola == (LRRRR)^3) <=> (k_r == 0). Una sola violazione = ROSSO
# (bug di rotazione o teorema male applicato). Gate esatti per orbita contro §85a
# (lrrrr_depth_summary.json): nblack e tot deep_1 devono coincidere al numero.
#
# Popolazioni k_r gratuite (servono al tripwire): tutte le letture nere, fresche (seme),
# in-finestra r=1. Dettagli di occupazione solo sui deep_1 (73% degli eventi).
#
# TEOREMA DELLA SCIA (candidato §86, verificato qui per-evento): a ogni deep_1 almeno una
# delle tre celle di scia {(0,1),(-1,1),(-1,0)} (frame heading-su) e' nera con eta' <=3.
# Dimostrazione (induzione all'indietro): pos(t-1)=(0,1); se svolta(t-1)=R, (0,1) e' nera (eta' 1).
# Altrimenti (0,1) bianca <=> letta nera a t-1 (L), heading pre-svolta = destra => pos(t-2)=(-1,1);
# se svolta(t-2)=R, (-1,1) nera (eta' 2); altrimenti pos(t-3)=(-1,0); se svolta(t-3)=R, nera
# (eta' 3); altrimenti heading pre-svolta = sinistra => pos(t-4) = CENTRO: il centro resta a
# distanza Chebyshev <=1 per tutti i passi t-4..t, quindi non esce mai dalla finestra viva r=1
# ed e' visitato => la lettura NON e' deep_1 (ne' fresca). Contraddizione. QED.
# Corollari: (1) deep_1 => halo non tutto bianco => (Teorema Halo §85c) NESSUN deep_1 inizia
# (LRRRR)^3 — l'evitamento §84/§85a e' un TEOREMA, valido per ogni orbita incluse le eterne
# (la trappola (i) cade per questo enunciato); (2) via entailment §85.3, lo 0% di motivi potati
# vuoti ai deep (§81) e' teorema; (3) per t>=4, halo tutto bianco => svolte(t-4..t-1)=R,L,L,L
# e il centro e' stato dipinto di nero dalla formica stessa ESATTAMENTE 4 passi prima (loop di
# ritorno): ogni cavalcata e' in-finestra, mai fresca, mai deep.
# Tripwire per-evento: T2 (scia) su ogni deep_1; T3 (RLLL + revisita-4) su ogni lettura nera
# con halo bianco e t>=4; T4 (cavalcate solo in-finestra a t>=4).
#
# Self-test PRIMA di ogni run (convenzione §5): testimone ai 4 heading, necessita' 9/9 ai
# 4 heading, <=> randomizzato (20k ambienti) contro simulazione diretta, estrazione snapshot.
import sys, os, json, time, argparse, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps, build_seed, ALPHA

DX = (0, 1, 0, -1); DY = (-1, 0, 1, 0)
WORD = bytes([1, 0, 0, 0, 0] * 3)   # (LRRRR)^3, L=1 (nero), 15 svolte
WL = len(WORD)
HALO = ((-2, 0), (-2, 1), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (0, -1), (0, 1), (0, 2))
ARRIVO = HALO.index((0, 1))          # cella di arrivo (dietro la formica)

def rot1(p):
    x, y = p
    return (-y, x)                   # quarto di giro orario in coordinate schermo (x dx, y giu')

ROT_HALO = []
for h in range(4):
    cs = list(HALO)
    for _ in range(h):
        cs = [rot1(c) for c in cs]
    ROT_HALO.append(tuple(cs))

SNAP_OFF = tuple((dx, dy) for dx in range(-2, 3) for dy in range(-2, 3) if (dx, dy) != (0, 0))
SNAP_BIT = {c: i for i, c in enumerate(SNAP_OFF)}
A_EDGES = (104, 1040, 10400, 104000)             # bucket eta' del nero profondo (stile §82)
AGE_EDGES = (3, 10, 31, 104, 1040)               # bucket eta' minima dei neri-halo

def bucket(v, edges):
    for i, e in enumerate(edges):
        if v <= e: return i
    return len(edges)

def sim_word(black, x, y, h, n):
    w = bytearray()
    for _ in range(n):
        c = (x, y); isb = c in black
        w.append(1 if isb else 0)
        if isb: black.discard(c); h = (h + 3) & 3
        else: black.add(c); h = (h + 1) & 3
        x += DX[h]; y += DY[h]
    return bytes(w)

def selftest():
    rnd = random.Random(86)
    # ST-A testimone ai 4 heading, posizioni casuali: nero isolato => (LRRRR)^3, halo ruotato bianco
    for h in range(4):
        for _ in range(50):
            px, py = rnd.randint(-50, 50), rnd.randint(-50, 50)
            assert sim_word({(px, py)}, px, py, h, WL) == WORD
            assert all((px + dx, py + dy) not in {(px, py)} for dx, dy in ROT_HALO[h])
    # ST-B necessita' 9/9 ai 4 heading: ogni singolo nero nell'halo ruotato rompe la parola
    for h in range(4):
        for dx, dy in ROT_HALO[h]:
            assert sim_word({(0, 0), (dx, dy)}, 0, 0, h, WL) != WORD, (h, dx, dy)
    # ST-C <=> randomizzato: ambiente casuale (r<=4), formica su nero, heading casuale
    ok_match = ok_nomatch = 0
    for _ in range(20000):
        h = rnd.randrange(4)
        px, py = rnd.randint(-30, 30), rnd.randint(-30, 30)
        black = {(px + rnd.randint(-4, 4), py + rnd.randint(-4, 4)) for _ in range(rnd.randint(0, 14))}
        black.add((px, py))
        halo_white = all((px + dx, py + dy) not in black for dx, dy in ROT_HALO[h])
        m = sim_word(set(black), px, py, h, WL) == WORD
        assert m == halo_white, (h, px, py, sorted(black))
        ok_match += m; ok_nomatch += (not m)
    assert ok_match >= 100 and ok_nomatch >= 100    # entrambi i rami esercitati
    # ST-D snapshot: estrazione k_w == conteggio diretto sui 9 offset ruotati
    for _ in range(1000):
        h = rnd.randrange(4)
        black = {(rnd.randint(-2, 2), rnd.randint(-2, 2)) for _ in range(rnd.randint(0, 12))}
        bits = 0
        for c in SNAP_OFF:
            if c in black: bits |= 1 << SNAP_BIT[c]
        kw = sum(1 for c in ROT_HALO[h] if (bits >> SNAP_BIT[c]) & 1)
        assert kw == sum(1 for c in ROT_HALO[h] if c in black)
    print("SELFTEST §86: testimone 4h OK, necessita' 4hx9 OK, <=> 20k OK "
          f"(match {ok_match}, no-match {ok_nomatch}), snapshot 1000 OK", flush=True)

def analyze(rng, onset):
    black, side, dens = build_seed(rng, 5, 25)
    known = set(); last = {}; wsnap = {}
    x = y = h = 0
    turns = bytearray()
    pending = []
    posbuf = [(0, 0)] * 4                            # posizioni t-4..t-1 (ring, idx t&3)
    nblack = 0; chain_missing_snap = 0
    t2_viol = 0; t3_viol = 0; t4_viol = 0; ride_early = 0
    trail_case = [0, 0, 0]                           # j=1,2,3 (ultima R nella scia)
    agemin_exact = [0, 0, 0, 0]                      # agemin 1,2,3, altro(=violazione)
    # istogrammi k_r per popolazione
    hk = {"all": [0]*10, "fresh": [0]*10, "inw": [0]*10, "deep1": [0]*10}
    mat = {"all": 0, "fresh": 0, "inw": 0, "deep1": 0}
    tot = {"all": 0, "fresh": 0, "inw": 0, "deep1": 0}
    iff_viol = 0
    # dettagli deep_1
    hkw = [0]*10; hdelta = [0]*21                    # k_w, Delta+10
    cell_r = [0]*9; cell_w = [0]*9; cell_dep = [0]*9 # per-cella: nero a rilettura / a scrittura / depositato
    prevL = 0; prevR = 0
    hk_prevL = [0]*10
    surv_hist = [0]*10                               # s = sopravvissuti intatti (incl. seed)
    s0_events = 0                                    # eventi con s==0 (tutto churned)
    seed_events = 0                                  # eventi con almeno un nero-halo mai visitato
    agemin_hist = [0]*(len(AGE_EDGES)+2)             # +1 overflow, +1 "solo-seed"
    a_kr_sum = [0]*(len(A_EDGES)+1); a_n = [0]*(len(A_EDGES)+1)
    kmin = 99; kmin_detail = None
    k1_cells = [0]*9                                 # eventi k_r==1: quale cella porta il nero

    for t in range(onset):
        c = (x, y); isb = c in black
        turns.append(1 if isb else 0)
        if isb:
            nblack += 1
            visited = c in last
            deep1 = visited and c not in known
            halo = ROT_HALO[h]
            habs = tuple((x + dx, y + dy) for dx, dy in halo)
            mr = 0; kr = 0
            for i in range(9):
                if habs[i] in black:
                    mr |= 1 << i; kr += 1
            if kr == 0 and t >= 4:
                # T3: halo bianco => prefisso R,L,L,L e pos(t-4) == centro
                if not (turns[t-4] == 0 and turns[t-3] == 1 and turns[t-2] == 1
                        and turns[t-1] == 1 and posbuf[t & 3] == c):
                    t3_viol += 1
                # T4: cavalcate solo in-finestra (visitate, non deep)
                if (not visited) or deep1:
                    t4_viol += 1
            elif kr == 0:
                ride_early += 1
            det = None
            if deep1:
                sn = wsnap.get(c)
                if sn is None:
                    chain_missing_snap += 1
                    tw, bits = -1, 0
                else:
                    tw, bits = sn
                mw = 0
                mu = 0; ms = 0                        # intatti dal write / mai visitati
                for i in range(9):
                    if (bits >> SNAP_BIT[halo[i]]) & 1: mw |= 1 << i
                    if mr >> i & 1:
                        lu = last.get(habs[i])
                        if lu is None: ms |= 1 << i; mu |= 1 << i
                        elif lu <= tw: mu |= 1 << i
                pv = turns[t-1] if t > 0 else 2
                # T2: teorema della scia
                if turns[t-1] == 0: j = 1
                elif turns[t-2] == 0: j = 2
                elif turns[t-3] == 0: j = 3
                else: j = 0
                if j == 0 or not (mr >> (ARRIVO, HALO.index((-1, 1)), HALO.index((-1, 0)))[j-1] & 1):
                    t2_viol += 1
                else:
                    trail_case[j-1] += 1
                agemin = None
                ages = [t - last[u] for i, u in enumerate(habs) if (mr >> i & 1) and u in last]
                if ages: agemin = min(ages)
                agemin_exact[agemin - 1 if agemin in (1, 2, 3) else 3] += 1
                det = (kr, mw, mr, mu, ms, pv, t - tw if tw >= 0 else -1, agemin)
            pending.append((t, visited, deep1, kr, det))
        if isb: black.discard(c); wsnap.pop(c, None); h = (h + 3) & 3
        else:
            bits = 0
            for dx, dy in SNAP_OFF:
                if (x + dx, y + dy) in black: bits |= 1 << SNAP_BIT[(dx, dy)]
            wsnap[c] = (t, bits)
            black.add(c); h = (h + 1) & 3
        last[c] = t
        known.add(c)
        posbuf[t & 3] = c
        x += DX[h]; y += DY[h]
        # forget raggio 1: anello a distanza Chebyshev 2
        for cx, cy in ((x-2,y-2),(x-2,y-1),(x-2,y),(x-2,y+1),(x-2,y+2),
                       (x+2,y-2),(x+2,y-1),(x+2,y),(x+2,y+1),(x+2,y+2),
                       (x-1,y-2),(x,y-2),(x+1,y-2),(x-1,y+2),(x,y+2),(x+1,y+2)):
            known.discard((cx, cy))
        while pending and t - pending[0][0] >= WL:
            te, visited, deep1, kr, det = pending.pop(0)
            m = bytes(turns[te:te+WL]) == WORD
            if m != (kr == 0): iff_viol += 1
            tot["all"] += 1; mat["all"] += m; hk["all"][kr] += 1
            if not visited:
                tot["fresh"] += 1; mat["fresh"] += m; hk["fresh"][kr] += 1
            elif not deep1:
                tot["inw"] += 1; mat["inw"] += m; hk["inw"][kr] += 1
            if deep1:
                tot["deep1"] += 1; mat["deep1"] += m; hk["deep1"][kr] += 1
                kr_, mw, mr, mu, ms, pv, A, agemin = det
                kw = bin(mw).count("1")
                hkw[kw] += 1; hdelta[kr_ - kw + 10] += 1
                s = bin(mu).count("1")
                surv_hist[s] += 1
                if s == 0: s0_events += 1
                if ms: seed_events += 1
                for i in range(9):
                    if mr >> i & 1:
                        cell_r[i] += 1
                        if not (mu >> i & 1): cell_dep[i] += 1
                    if mw >> i & 1: cell_w[i] += 1
                if pv == 1:
                    prevL += 1; hk_prevL[kr_] += 1
                elif pv == 0: prevR += 1
                if agemin is None: agemin_hist[-1] += 1
                else: agemin_hist[bucket(agemin, AGE_EDGES)] += 1
                if A >= 0:
                    ab = bucket(A, A_EDGES); a_kr_sum[ab] += kr_; a_n[ab] += 1
                if kr_ < kmin:
                    kmin = kr_; kmin_detail = {"t": te, "k": kr_, "mask_r": mr, "prev": pv, "A": A}
                if kr_ == 1:
                    for i in range(9):
                        if mr >> i & 1: k1_cells[i] += 1
    return {"rng": rng, "onset": onset, "nblack": nblack, "ntrunc": len(pending),
            "iff_viol": iff_viol, "missing_snap": chain_missing_snap,
            "tot": tot, "mat": mat, "hk": hk,
            "t2_viol": t2_viol, "t3_viol": t3_viol, "t4_viol": t4_viol,
            "ride_early": ride_early, "trail_case": trail_case, "agemin_exact": agemin_exact,
            "deep1": {"hkw": hkw, "hdelta": hdelta, "cell_r": cell_r, "cell_w": cell_w,
                      "cell_dep": cell_dep, "prevL": prevL, "prevR": prevR,
                      "hk_prevL": hk_prevL, "surv_hist": surv_hist, "s0": s0_events,
                      "seed_events": seed_events, "agemin_hist": agemin_hist,
                      "a_kr_sum": a_kr_sum, "a_n": a_n, "kmin": kmin,
                      "kmin_detail": kmin_detail, "k1_cells": k1_cells}}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--orbits", default="")
    ap.add_argument("--out", default=str(ALPHA / "halo_occupancy_summary.json"))
    ap.add_argument("--ref", default=str(ALPHA / "lrrrr_depth_summary.json"))
    a = ap.parse_args()
    selftest()
    t0 = time.time()
    dumps = parse_dumps(ALPHA / "dumps_all.txt")
    idxs = list(range(len(dumps))) if not a.orbits else [int(s) for s in a.orbits.split(",")]
    ref = json.load(open(a.ref))["res"] if os.path.exists(a.ref) else None
    res = []
    gate_red = 0
    for j, i in enumerate(idxs):
        r = analyze(dumps[i].rngstate, dumps[i].onset_dump)
        res.append(r)
        g = ""
        if ref is not None:
            rr = ref[i]
            ok = (r["nblack"] == rr["nblack"] and r["tot"]["deep1"] == rr["tot"]["1"]
                  and r["tot"]["all"] == rr["tot_all"] and r["mat"]["all"] == rr["mat_all"])
            g = "gate §85a OK" if ok else "gate §85a ROSSO"
            gate_red += (not ok)
        tw = "tripwire<=> OK" if r["iff_viol"] == 0 else f"tripwire<=> ROSSO({r['iff_viol']})"
        tvi = r["t2_viol"] + r["t3_viol"] + r["t4_viol"]
        tw += " T2/T3/T4 OK" if tvi == 0 else f" T2={r['t2_viol']} T3={r['t3_viol']} T4={r['t4_viol']} ROSSO"
        ms = "" if r["missing_snap"] == 0 else f" SNAP-MANCANTI {r['missing_snap']}"
        print(f"[{time.time()-t0:7.1f}s] orbita {i} ({j+1}/{len(idxs)}) "
              f"deep1={r['tot']['deep1']} kmin={r['deep1']['kmin']} {g} {tw}{ms}", flush=True)
    iv = sum(r["iff_viol"] for r in res); msn = sum(r["missing_snap"] for r in res)
    print(f"\nTRIPWIRE <=> halo (teorema §85c su dati reali): "
          f"{'OK (0 violazioni)' if iv == 0 else f'ROSSO: {iv}'}")
    print(f"SNAPSHOT mancanti ai deep_1: {'OK (0)' if msn == 0 else f'ROSSO: {msn}'}")
    if ref is not None:
        print(f"GATE §85a per orbita (nblack, deep_1, tot_all, mat_all): "
              f"{'VERDI ' + str(len(idxs)) + '/' + str(len(idxs)) if gate_red == 0 else f'ROSSI: {gate_red}'}")
    t2 = sum(r["t2_viol"] for r in res); t3 = sum(r["t3_viol"] for r in res)
    t4 = sum(r["t4_viol"] for r in res); re_ = sum(r["ride_early"] for r in res)
    print(f"TEOREMA DELLA SCIA (T2, per-evento sui deep_1): "
          f"{'OK (0 violazioni)' if t2 == 0 else f'ROSSO: {t2}'}")
    print(f"COROLLARIO RLLL+revisita-4 (T3, su ogni halo-bianco t>=4): "
          f"{'OK (0 violazioni)' if t3 == 0 else f'ROSSO: {t3}'}"
          + (f"  [cavalcate a t<4: {re_}]" if re_ else ""))
    print(f"CAVALCATE solo in-finestra (T4): {'OK (0 violazioni)' if t4 == 0 else f'ROSSO: {t4}'}")
    if iv or msn or gate_red or t2 or t3 or t4: sys.exit(1)

    def H(key, sub=None):
        out = [0]*32
        for r in res:
            src = r["deep1"][key] if sub is None else r[key][sub]
            for i, v in enumerate(src): out[i] += v
        return out
    D1 = sum(r["tot"]["deep1"] for r in res)
    print(f"\n=== §86a OCCUPAZIONE HALO ai deep_1 (pooled, {D1} eventi, {len(idxs)} orbite) ===")
    hk1 = H("hk", "deep1")
    print("k_r (neri nell'halo alla rilettura):")
    for k in range(10):
        if hk1[k]: print(f"  k={k}: {hk1[k]:>8}  ({100*hk1[k]/D1:7.4f}%)")
    kmin_all = min(r["deep1"]["kmin"] for r in res)
    kmin_perorb = [r["deep1"]["kmin"] for r in res]
    print(f"minimo empirico k_r: pooled {kmin_all}; per orbita {kmin_perorb}")
    hkw = H("hkw")
    kwm = sum(k*v for k, v in enumerate(hkw))/D1
    krm = sum(k*v for k, v in enumerate(hk1))/D1
    print(f"\nk_w (alla scrittura) medio {kwm:.3f} vs k_r (alla rilettura) medio {krm:.3f}")
    hd = H("hdelta")
    print("Delta = k_r - k_w:", {d-10: v for d, v in enumerate(hd) if v})
    cr = H("cell_r"); cw = H("cell_w"); cd = H("cell_dep")
    print("\nper-cella (frame heading-su) — nero a rilettura / a scrittura / depositato nell'intervallo:")
    for i, c in enumerate(HALO):
        tag = " <- ARRIVO" if i == ARRIVO else ""
        print(f"  {str(c):>8}: {100*cr[i]/D1:6.2f}% / {100*cw[i]/D1:6.2f}% / {100*cd[i]/D1:6.2f}%{tag}")
    pL = sum(r["deep1"]["prevL"] for r in res); pR = sum(r["deep1"]["prevR"] for r in res)
    print(f"\nsvolta precedente: L={pL} ({100*pL/D1:.2f}%)  R={pR} ({100*pR/D1:.2f}%)")
    hkL = H("hk_prevL")
    if pL:
        print("k_r | prev=L (cella d'arrivo bianca):",
              {k: v for k, v in enumerate(hkL) if v}, f" min={min(k for k,v in enumerate(hkL) if v)}")
    sh = H("surv_hist")
    s0 = sum(r["deep1"]["s0"] for r in res); se = sum(r["deep1"]["seed_events"] for r in res)
    print(f"\ns (neri-halo INTATTI dalla scrittura, incl. seed): {dict((k,v) for k,v in enumerate(sh) if v)}")
    print(f"eventi s=0 (halo interamente rifornito nell'intervallo): {s0} ({100*s0/D1:.3f}%)")
    print(f"eventi con nero-halo di seme mai visitato: {se} ({100*se/D1:.4f}%)")
    ame = [sum(r["agemin_exact"][i] for r in res) for i in range(4)]
    print(f"eta' minima dei neri-halo (teorema: <=3 sempre): 1:{ame[0]} 2:{ame[1]} 3:{ame[2]} altro:{ame[3]}")
    tc = [sum(r["trail_case"][i] for r in res) for i in range(3)]
    print(f"caso di scia j (ultima R in t-1/t-2/t-3): j=1 {tc[0]} ({100*tc[0]/D1:.2f}%), "
          f"j=2 {tc[1]} ({100*tc[1]/D1:.2f}%), j=3 {tc[2]} ({100*tc[2]/D1:.2f}%)")
    aks = H("a_kr_sum"); an = H("a_n")
    albl = [f"<={e}" for e in A_EDGES] + [f">{A_EDGES[-1]}"]
    print("k_r medio per bucket eta' del nero profondo (trappola q):",
          {albl[i]: round(aks[i]/an[i], 3) for i in range(len(albl)) if an[i]})
    k1 = H("k1_cells")
    if hk1[1]:
        print("eventi k_r=1 — cella del nero solitario:",
              {str(HALO[i]): v for i, v in enumerate(k1) if v})
    base = {p: (sum(r["mat"][p] for r in res), sum(r["tot"][p] for r in res)) for p in ("all","fresh","inw")}
    print("\ncontesto (riproduzione §85a): match/tot —",
          {p: f"{m}/{t}" for p, (m, t) in base.items()}, f" deep1: {sum(r['mat']['deep1'] for r in res)}/{D1}")
    json.dump({"orbits": idxs, "res": res}, open(a.out, "w"), indent=1)
    print(f"scritto {a.out}  (elapsed {time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
