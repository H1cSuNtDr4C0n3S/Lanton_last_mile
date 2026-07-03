# record_weapon_vitality.py — §88: VITALITA' del minimo vivo della caccia §87e/§88.
#
# Contesto (trappola (w), CONE-LOCK §87e-2): un teorema-parola ai record e' VACUO se la
# parola non ha estensioni all'indietro record-compatibili di profondita' arbitraria.
# La run v3 (beam 4000, kmax 120, viable-k 8, per-class 200) ha trovato burden1=1 a
# K=101..120 (residuo {(1,1)}); questo script certifica quanto e' VIVA la parola K=101.
#
# Test (gate incorporati, fermarsi al primo rosso):
#   GATE  riproduzione in-process dei numeri della run (w101, w120, catena 102..120)
#         + controllo negativo: la parola vacua K=60 di §87e-2 deve estinguersi subito.
#   A     D(w101) >= target: DFS early-exit con memo dei fallimenti (default target 104
#         = un periodo pieno di prepend). Riporta la catena testimone e il profilo burden.
#   B     censimento ESAUSTIVO del muro dei prepend sopra w101 (livelli 1..enum-depth) +
#         caccia al CICLO DI PREPEND con certificato geometrico finito:
#         se il blocco beta ha cammino virtuale con heading di ritorno h=0 e drift Delta!=0,
#         i blocchi successivi sono copie TRASLATE; i conflitti tra blocchi dipendono solo
#         dal gap g e sono nulli per g > g_max = floor(diam_inf(tutto)/|Delta|_inf)+1;
#         quindi la validita' (realizzabilita' + record-compatibilita') di beta^m + w101
#         per OGNI m segue dal check finito m <= M_cert = g_max+2, piu' la condizione di
#         record-compatibilita' eterna Delta_anchor.y <= 0 (i blocchi vecchi salgono).
#         NB: l'onset del germe (usato solo per LEGGERE burden1) non e' coperto
#         dall'induzione geometrica: viene verificato empiricamente per ogni m <= M_cert
#         e dichiarato tale nell'addendum (il censimento §87b non ha mai visto buchi).
#   C     corridoio a fardello <=1: DFS esaustiva da w101 con pota burden1 > 1
#         (la linea del beam 101->120 continua? muore? tocca burden1=0?).
#
# Uscita: alpha1/record_weapon_vitality_summary.json (+ stampe log-friendly).
import sys, os, json, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from onset_cone_lock import DX, DY, P, rotk
from kwindow_spoiler_census import virtual_walk, to_anchor_frame
from record_weapon_hunt import eval_word

HERE = os.path.dirname(os.path.abspath(__file__))
SUMMARY = os.path.join(HERE, "record_weapon_summary.json")
OUT = os.path.join(HERE, "record_weapon_vitality_summary.json")

# §87e-2 (CONE_LOCK_ADDENDUM AGGIORNAMENTO 2): campione a fardello 2, K=60, onset 156,
# residuo {(-2,1),(1,1)} — dichiarato VACUO (estinzione all'indietro entro prof. 3).
CONTROL_K60 = "LRLLRLRRLLLLRRLLLLRRLRRLRRLRRRRLLLLRLLRLRRLRLRLLRLLRLLRLRLRL"

def to_bits(s):
    return tuple(1 if ch == "R" else 0 for ch in s.strip().upper())

def to_str(w):
    return "".join("R" if b else "L" for b in w)


class Evaluator:
    """eval_word con cache (le parole si ripetono tra DFS/enumerazione/certificati)."""
    def __init__(self):
        self.cache = {}
        self.calls = 0

    def __call__(self, w):
        r = self.cache.get(w, "MISS")
        if r != "MISS":
            return r
        self.calls += 1
        r = eval_word(w)
        self.cache[w] = r
        return r


def chain_dfs(ev, base, target, node_budget, t0, budget_s):
    """Esiste una catena di prepend validi di profondita' >= target sopra base?
    DFS early-exit; memo dei sottoalberi falliti: fail[w] = profondita' residua
    dimostrata impossibile (sound: il sottoalbero di w non dipende dal cammino)."""
    fail = {}
    nodes = [0]

    def rec(w, remaining):
        if remaining == 0:
            return ()
        if fail.get(w, 0) >= remaining:
            return None
        if nodes[0] >= node_budget or time.time() - t0 > budget_s:
            return None                      # budget: NON marca fail (risposta = unknown)
        kids = []
        for bit in (0, 1):
            w2 = (bit,) + w
            nodes[0] += 1
            r = ev(w2)
            if r is not None:
                kids.append((r[0], bit, w2))
        kids.sort()                          # prima i fardelli bassi (euristica, non pota)
        for _, bit, w2 in kids:
            tail = rec(w2, remaining - 1)
            if tail is not None:
                return tail + (bit,)         # testimone: dal piu' vecchio al piu' recente
        fail[w] = max(fail.get(w, 0), remaining)
        return None

    wit = rec(base, target)
    return wit, nodes[0]


def enumerate_wall(ev, base, depth_max, level_cap, t0, budget_s):
    """Enumerazione esaustiva per livelli dei prefissi di prepend validi sopra base.
    Ritorna (levels: prof->lista di prefissi (tuple, dal piu' vecchio), counts, truncated)."""
    levels = {0: [()]}
    counts = {}
    truncated = None
    for d in range(1, depth_max + 1):
        cur = []
        for pref in levels[d - 1]:
            for bit in (0, 1):
                p2 = (bit,) + pref
                if ev(p2 + base) is not None:
                    cur.append(p2)
        counts[d] = len(cur)
        levels[d] = cur
        if not cur:
            break
        if len(cur) > level_cap or time.time() - t0 > budget_s:
            truncated = d
            break
    return levels, counts, truncated


def walk_block(beta):
    """Cammino virtuale del solo blocco beta da (0,0,0). Ritorna (grid, pose) o (None,None)."""
    return virtual_walk(beta)


def bbox_diam(cells):
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
    return max(max(xs) - min(xs), max(ys) - min(ys))


def chain_valid(ev, ext, base):
    """La catena lettera-per-lettera ext+base e' valida a OGNI passo? ext e' il prefisso
    finale (dal piu' vecchio al piu' recente = ordine naturale della parola)."""
    for j in range(len(ext) - 1, -1, -1):
        if ev(ext[j:] + base) is None:
            return False
    return True


def certify_cycle(ev, sigma, base):
    """Tenta il certificato geometrico D=infinito per il blocco sigma sopra base.
    Ritorna dict con esito e dettagli (vedi header). Sound per realizzabilita' +
    record-compatibilita'; l'onset resta empirico (dichiarato nel campo 'onset_empirico')."""
    out = {"sigma": to_str(sigma), "p": len(sigma)}
    g, pose = walk_block(sigma)
    if g is None:
        out["esito"] = "blocco irrealizzabile da solo"
        return out
    x, y, h = pose
    q = {0: 1, 2: 2, 1: 4, 3: 4}[h]          # ordine dell'heading: beta = sigma^q torna a h=0
    beta = sigma * q
    gb, pb = walk_block(beta)
    if gb is None:
        out["esito"] = f"beta=sigma^{q} irrealizzabile"
        return out
    dx, dy, hb = pb
    out["q"] = q
    out["delta_walk"] = [dx, dy]
    assert hb == 0, "heading di beta deve essere 0 per costruzione"
    if (dx, dy) == (0, 0):
        out["esito"] = "drift nullo (ciclo fisso impossibile da certificare cosi')"
        return out
    # pre-filtro: >= 3 periodi pieni (metodo §84) in catena lettera-per-lettera
    if not chain_valid(ev, beta * 3, base):
        out["esito"] = "muore entro 3 periodi"
        return out
    # M_cert dal raggio di interazione
    gw, pose_full = virtual_walk(beta + base)
    diam_all = bbox_diam(list(gw))
    dinf = max(abs(dx), abs(dy))
    g_max = diam_all // dinf + 1
    m_cert = g_max + 2
    out["diam_all"] = diam_all
    out["g_max"] = g_max
    out["m_cert"] = m_cert
    if m_cert * len(beta) > 4000:
        out["esito"] = f"M_cert={m_cert} fuori budget (catena {m_cert*len(beta)} lettere)"
        return out
    # condizione di record-compatibilita' eterna: Delta in frame anchor deve salire
    k = (-pose_full[2]) % 4
    da = rotk((dx, dy), k)
    out["delta_anchor"] = list(da)
    if da[1] > 0:
        out["esito"] = "delta_anchor.y > 0: i blocchi vecchi scendono, record-compat muore"
        return out
    if not chain_valid(ev, beta * m_cert, base):
        out["esito"] = f"muore entro M_cert={m_cert} periodi"
        return out
    # profilo burden lungo i periodi certificati
    prof = []
    for m in range(1, m_cert + 1):
        r = ev(beta * m + base)
        prof.append(None if r is None else r[0])
    out["burden_per_periodo"] = prof
    out["onset_empirico"] = f"onset verificato per ogni passo fino a m={m_cert}"
    out["esito"] = "CERTIFICATO: D = infinito (realizzabilita'+record-compat per ogni m)"
    out["certificato"] = True
    return out


def corridor_dfs(ev, base, cap, extra_max, node_budget, t0, budget_s):
    """DFS esaustiva con pota burden1 > cap: mappa il corridoio a fardello basso.
    Ritorna (deepest, deaths_by_depth, alive_at_max, weapon, nodes, exhausted)."""
    deaths = {}
    deepest = 0
    alive_at_max = 0
    weapon = None
    nodes = 0
    stack = [((), 0)]
    exhausted = True
    while stack:
        if nodes >= node_budget or time.time() - t0 > budget_s:
            exhausted = False
            break
        pref, d = stack.pop()
        if d >= extra_max:
            alive_at_max += 1
            continue
        any_kid = False
        for bit in (0, 1):
            p2 = (bit,) + pref
            nodes += 1
            r = ev(p2 + base)
            if r is None or r[0] > cap:
                continue
            any_kid = True
            if r[0] == 0:
                r2 = eval_word(p2 + base)     # ri-verifica indipendente (no cache)
                assert r2 is not None and r2[0] == 0
                weapon = {"K": len(p2 + base), "word": to_str(p2 + base), "onset": r[1]}
            deepest = max(deepest, d + 1)
            stack.append((p2, d + 1))
        if not any_kid:
            deaths[d] = deaths.get(d, 0) + 1
    return deepest, deaths, alive_at_max, weapon, nodes, exhausted


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=104, help="profondita' bersaglio D(w101)")
    ap.add_argument("--enum-depth", type=int, default=14)
    ap.add_argument("--enum-level-cap", type=int, default=60000)
    ap.add_argument("--corridor-extra", type=int, default=60)
    ap.add_argument("--max-cert", type=int, default=40,
                    help="max tentativi di certificato di ciclo (ordinati per p e burden)")
    ap.add_argument("--nodes", type=int, default=1_500_000)
    ap.add_argument("--budget-s", type=int, default=1500)
    args = ap.parse_args()
    t0 = time.time()
    ev = Evaluator()

    d = json.load(open(SUMMARY))
    bpk = {int(k): v for k, v in d["best_per_K"].items()}
    w101 = to_bits(bpk[101]["word"])
    w120 = to_bits(bpk[120]["word"])

    # ---------------- GATE ----------------
    r101 = ev(w101)
    assert r101 is not None and r101[0] == 1 and r101[3] == [(1, 1)] \
        and r101[1] == bpk[101]["onset"], f"GATE w101 fallito: {r101}"
    r120 = ev(w120)
    assert r120 is not None and r120[0] == 1 and r120[3] == [(1, 1)], f"GATE w120: {r120}"
    for k in range(102, 121):
        wk = to_bits(bpk[k]["word"])
        assert wk[-101:] == w101, f"GATE catena: best K={k} non estende w101"
        rk = ev(wk)
        assert rk is not None and rk[0] == bpk[k]["burden1"] and rk[1] == bpk[k]["onset"], \
            f"GATE riproduzione K={k}: {rk} vs {bpk[k]}"
    ctrl = to_bits(CONTROL_K60)
    rc = ev(ctrl)
    assert rc is not None and rc[0] == 2 and rc[1] == 156 \
        and rc[3] == [(-2, 1), (1, 1)], f"GATE controllo K=60: {rc}"
    # controllo negativo: D(ctrl) deve essere piccolo (§87e-2: estinzione entro prof. 3)
    d_ctrl = 0
    for depth in range(1, 9):
        wit, _ = chain_dfs(ev, ctrl, depth, 200_000, t0, args.budget_s)
        if wit is None:
            break
        d_ctrl = depth
    assert d_ctrl <= 3, f"controllo negativo NON vacuo? D={d_ctrl}"
    print(f"GATE verdi: w101/w120/catena 102..120 riprodotti; controllo K=60 "
          f"burden=2 onset=156 D={d_ctrl} (<=3, vacuo confermato)", flush=True)

    # ---------------- Test A: D(w101) >= target ----------------
    tA = time.time()
    wit, nodesA = chain_dfs(ev, w101, args.target, args.nodes, t0, args.budget_s)
    resA = {"target": args.target, "nodes": nodesA, "elapsed_s": round(time.time() - tA, 1)}
    if wit is not None:
        ext = tuple(wit)                       # dal piu' vecchio al piu' recente
        assert chain_valid(ev, ext, w101), "testimone non ricontrollato!"
        prof = [ev(ext[j:] + w101)[0] for j in range(len(ext) - 1, -1, -1)]
        resA.update({"raggiunto": True, "testimone": to_str(ext),
                     "burden_lungo_catena_min": min(prof), "burden_lungo_catena_max": max(prof)})
        print(f"TEST A: D(w101) >= {args.target} — testimone di {len(ext)} prepend "
              f"(burden lungo la catena in [{min(prof)},{max(prof)}]), "
              f"{nodesA} nodi, {resA['elapsed_s']}s", flush=True)
    else:
        resA["raggiunto"] = False
        print(f"TEST A: target {args.target} NON raggiunto entro i budget "
              f"({nodesA} nodi) — vedi muro in Test B", flush=True)

    # ---------------- Test B: muro esaustivo + cicli certificati ----------------
    tB = time.time()
    levels, counts, trunc = enumerate_wall(ev, w101, args.enum_depth,
                                           args.enum_level_cap, t0, args.budget_s)
    print(f"TEST B: muro dei prepend sopra w101 (esaustivo fino a prof. "
          f"{max(counts) if counts else 0}{' TRONCATO' if trunc else ''}): "
          f"{[counts[d] for d in sorted(counts)]}", flush=True)
    certs = []
    tried = 0
    found = None
    for p in sorted(levels):
        if p == 0 or found:
            continue
        # candidati sigma = prefissi sopravvissuti a prof. p, ordinati per burden
        cands = sorted(levels[p], key=lambda s: ev(s + w101)[0])
        for s in cands:
            if tried >= args.max_cert or found:
                break
            tried += 1
            c = certify_cycle(ev, s, w101)
            certs.append(c)
            if c.get("certificato"):
                found = c
                print(f"  CICLO CERTIFICATO: sigma={c['sigma']} (p={c['p']}, q={c['q']}, "
                      f"delta_anchor={c['delta_anchor']}, M_cert={c['m_cert']}, "
                      f"burden/periodo={c['burden_per_periodo']})", flush=True)
        if found:
            break
    n_die3 = sum(1 for c in certs if c.get("esito", "").startswith("muore entro 3"))
    print(f"TEST B: {tried} candidati-ciclo provati, {n_die3} morti entro 3 periodi, "
          f"certificati: {1 if found else 0} ({round(time.time()-tB,1)}s)", flush=True)
    resB = {"counts_per_depth": counts, "truncated_at": trunc,
            "cert_tried": tried, "certs": certs[:60], "certificato": found}

    # ---------------- Test C: corridoio a fardello <=1 ----------------
    tC = time.time()
    deepest, deaths, alive, weap, nodesC, exh = corridor_dfs(
        ev, w101, 1, args.corridor_extra, args.nodes, t0, args.budget_s + 600)
    resC = {"cap": 1, "extra_max": args.corridor_extra, "deepest": deepest,
            "alive_at_max": alive, "deaths_by_depth": deaths, "weapon": weap,
            "nodes": nodesC, "esaustivo": exh, "elapsed_s": round(time.time() - tC, 1)}
    print(f"TEST C: corridoio burden1<=1 sopra w101: prof. max {deepest}"
          f"{' (VIVO al cap ' + str(args.corridor_extra) + ', rami ' + str(alive) + ')' if alive else ' (MORTO)'}"
          f", morti per prof. {dict(sorted(deaths.items()))}, arma: {weap}, "
          f"{nodesC} nodi{'' if exh else ' (NON esaustivo)'}, {resC['elapsed_s']}s", flush=True)

    out = {"args": vars(args), "gates": {"w101": True, "w120": True, "chain_102_120": True,
                                         "control_K60_burden": 2, "control_K60_D": d_ctrl},
           "test_A_depth": resA, "test_B_wall_cycles": resB, "test_C_corridor": resC,
           "eval_calls": ev.calls, "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"scritto {OUT} in {out['elapsed_s']} s ({ev.calls} eval)", flush=True)


if __name__ == "__main__":
    main()
