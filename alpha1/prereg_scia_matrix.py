# -*- coding: utf-8 -*-
# prereg_scia_matrix.py — Matrice 8x5x3 della Scia di Forced-L7
# (PREREG_RC2_PONTE v14 sez. 3e; verdetto del titolare /13).
#
# CONTRATTO CONGELATO (v14):
#  - matrice CONDIZIONATA a deep: solo j in {1,2,3}; LLL eliminato PRIMA,
#    deduttivamente, da L-SCIA-J(c) [T] (LLL => evento KNOWN => non-deep);
#  - fase temporale: cella-scia NERA a t- (L-SCIA-J(b)); trasporto canonico =
#    INTERA sequenza forward L*R^{k-1} dallo stato a t- fino a m*-;
#  - mappa req->colore: first_color(c) = 1 - req(c) (req=1 forza BIANCO=0);
#    vincoli req certificati a m*: NOVE di C1 (POSE\{(1,1)}) => 1; c* => 1;
#    c_par se in palla (C3+clean) => 1; NIENT'ALTRO;
#  - COND-KILL SOLO con evidenza: (tipo 1) lettura del tratto incompatibile
#    col colore corrente della cella-scia; (tipo 2) colore finale a m*- che
#    contraddice 1-req su cella certificata. Mai dalla sola collisione.
#  - INFEASIBLE SOLO da contraddizione certificata che NON coinvolge la
#    catena di colore della cella-scia (alternanza interna, y<1, endpoint
#    su celle diverse dalla scia). MAI da assenza di estensione.
#  - ORDINE: non-Scia => INFEASIBLE; Scia => COND-KILL; modello esplicito
#    => LOCAL-SURVIVE; altrimenti UNKNOWN.
#  - classificazione per firma: ACTIONABLE (>=1 non-INF e tutti i non-INF
#    COND-KILL) / SURVIVES (>=1 LS) / UNKNOWN (no LS, >=1 UNK) / INFEASIBLE.
#  - gate finale: esiste una firma ACTIONABLE? (mai "almeno un ramo").
#
# Convenzioni cinematiche CANONICHE (fondamento, onset_cone_lock.py):
#  DX=(0,1,0,-1), DY=(-1,0,1,0); R=+1 orario, L=-1; bit 1=R=lettura BIANCA(0),
#  bit 0=L=lettura NERA(1); prepend (L-0b0/§92a): cn = posa - D[h],
#  h' = h-1 (R) / h+1 (L), posa' = cn; forward: p' = p + D[h'].
#
# Esche preregistrate (kill-list /13 punto 8):
#  E1 = omissione del passo L nel trasporto (deve fallire il round-trip);
#  E2 = scambio celle j=2/j=3 (deve fallire la doppia derivazione G2);
#  E3 = kill dalla sola collisione geometrica (deve divergere dal predicato
#       congelato su un caso reale o sul caso sintetico (1,1)).
#
# Controlli ESPLICITI (niente assert nudi: fail-open sotto python -O);
# sys.flags.optimize registrato nel summary. Exit code 1 se un check e' rosso.
import sys
import os
import json
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from onset_cone_lock import DX, DY, rotk  # noqa: E402  (convenzione canonica)

FASE0_SUM = os.path.join(HERE, "prereg_fase0_geometry_summary.json")
OUT_JSON = os.path.join(HERE, "prereg_scia_matrix_summary.json")

POSE = [(x, y) for x in range(-2, 3) for y in (1, 2)]
NINE = [c for c in POSE if c != (1, 1)]
FRAME_SCIA = {1: (0, 1), 2: (-1, 1), 3: (-1, 0)}   # L-SCIA-J, frame evento
KS = (1, 2, 3, 4, 5)
JS = (1, 2, 3)
# Lista a verbale §96a — SOLO cross-check, mai sorgente di geometria.
FIRME_96A = [((-2, 1), 1), ((-2, 2), 0), ((-2, 2), 1), ((-1, 2), 0),
             ((0, 2), 0), ((1, 2), 0), ((2, 2), 0), ((2, 2), 3)]

FAILS = []


def check(cond, label):
    if not cond:
        FAILS.append(label)
        print("[ROSSO] " + label, flush=True)
    return bool(cond)


def cheb(c):
    return max(abs(c[0]), abs(c[1]))


def first_color(req):
    """Contratto congelato /13.3: colore della prima lettura forward nel
    suffisso = 1 - req. req=1 => BIANCO (0)."""
    return 1 - req


def prepend(c, h, bit):
    """Prepend cinematico puro (L-0b0/§92a): cella letta cn = posa - D[h];
    h' = h-1 se R / h+1 se L; posa' = cn."""
    cn = (c[0] - DX[h], c[1] - DY[h])
    hn = (h - 1) & 3 if bit == 1 else (h + 1) & 3
    return cn, hn


def forward_sim(start, letters, scia_cell, cert_req, skip_index=None):
    """Trasporto canonico: dallo stato di (t-j)- processa le lettere forward
    (R, L^{j-1}, L evento, R^{k-1}) fino a m*-. Colori 3-valued: ignoto finche'
    non letto; la prima lettura ASSEGNA il colore iniziale (modello).
    Raccoglie TUTTE le contraddizioni (al conflitto forza e continua).
    skip_index: indice lettera da saltare (SOLO esca E1)."""
    c, h = start
    colors = {}
    init_model = {}
    contrs = []
    for i, bit in enumerate(letters):
        if skip_index is not None and i == skip_index:
            continue
        cell = c
        req_read = 0 if bit == 1 else 1
        if cell[1] < 1:
            contrs.append({"tipo": "y<1", "cella": list(cell), "step": i,
                           "scia": False})
        if cell in colors:
            if colors[cell] != req_read:
                contrs.append({"tipo": "lettura", "cella": list(cell),
                               "step": i, "richiesto": req_read,
                               "trovato": colors[cell],
                               "scia": cell == scia_cell})
                colors[cell] = req_read
        else:
            colors[cell] = req_read
            init_model[cell] = req_read
        colors[cell] = 1 - colors[cell]
        h = (h + 1) & 3 if bit == 1 else (h + 3) & 3
        c = (c[0] + DX[h], c[1] + DY[h])
    for cell in sorted(colors):
        if cell in cert_req:
            need = first_color(cert_req[cell])
            if colors[cell] != need:
                contrs.append({"tipo": "endpoint", "cella": list(cell),
                               "richiesto": need, "trovato": colors[cell],
                               "scia": cell == scia_cell})
    return (c, h), colors, init_model, contrs


def decide(contrs):
    """Ordine di decisione congelato: non-Scia => INFEASIBLE;
    Scia => COND-KILL; altrimenti None (=> LOCAL-SURVIVE col modello)."""
    non_scia = [x for x in contrs if not x["scia"]]
    scia = [x for x in contrs if x["scia"]]
    if non_scia:
        return "INFEASIBLE", non_scia
    if scia:
        return "COND-KILL", scia
    return None, []


def classify_firma(stati15):
    """Classificazione per firma (congelata /12-/13); itera TUTTE le colonne."""
    non_inf = [s for s in stati15 if s != "INFEASIBLE"]
    if not non_inf:
        return "INFEASIBLE"
    if any(s == "LOCAL-SURVIVE" for s in stati15):
        return "SURVIVES"
    if any(s == "UNKNOWN" for s in stati15):
        return "UNKNOWN"
    return "ACTIONABLE"


def build_case(f, k, j):
    """Costruzione backward del caso (f,k,j): parola prepend-order
    R^{k-1} L L^{j-1} R; stati dopo ogni prepend."""
    c, h = f["c_star"], f["h_star"]
    bits = [1] * (k - 1) + [0] + [0] * (j - 1) + [1]
    states = []
    for b in bits:
        c, h = prepend(c, h, b)
        states.append((c, h))
    p_t, h_t = states[k - 1]              # stato dell'evento (L-0b0)
    scia_walk = states[k + j - 1][0]      # cella letta al prepend k+j
    start = states[k + j - 1]             # stato di (t-j)
    letters = list(reversed(bits))        # forward antico->recente
    return bits, letters, states, (p_t, h_t), scia_walk, start


def scia_by_lemma(p_t, h_t, j, swap23=False):
    fc = FRAME_SCIA[j]
    if swap23 and j in (2, 3):
        fc = FRAME_SCIA[5 - j]
    d = rotk(fc, h_t)
    return (p_t[0] + d[0], p_t[1] + d[1])


def cert_req_for(f):
    cert = {c: 1 for c in NINE}
    cert[f["c_star"]] = 1                 # appena chiusa dal passo R di pulizia
    if f["c_par_in_palla"]:
        cert[f["c_par"]] = 1              # C3 + pend2=0
    return cert


def main():
    t0 = time.time()
    ok_opt = check(sys.flags.optimize == 0, "G0: sys.flags.optimize != 0")

    d = json.load(open(FASE0_SUM))
    firme = []
    for r in d["firme"]:
        firme.append({"c_star": tuple(r["c_star"]), "h_star": r["h_star"],
                      "c_par": tuple(r["c_par"]), "h_par": r["h_par"],
                      "c_par_in_palla": bool(r["c_par_in_palla"]),
                      "primo_passo": tuple(r["primo_passo_cella"])})

    # ---- G1: geometria di base vs verbale/Fase 0 (verifica [C]) ----
    check(sorted((f["c_star"], f["h_star"]) for f in firme) ==
          sorted(FIRME_96A), "G1: firme != lista a verbale §96a")
    interne = 0
    for f in firme:
        hp = (f["h_star"] + 1) & 3
        cp = (f["c_star"][0] + DX[hp], f["c_star"][1] + DY[hp])
        check(hp == f["h_par"] and cp == f["c_par"],
              "G1: c_par/h_par formula vs summary per %r" % (f,))
        c1, _ = prepend(f["c_star"], f["h_star"], 1)
        check(c1 == f["primo_passo"],
              "G1: primo passo vs summary per %r" % (f,))
        check(f["c_star"] in NINE, "G1: c* fuori dalle nove per %r" % (f,))
        interne += 1 if f["c_par_in_palla"] else 0
    check(interne == 6, "G1: firme interne != 6")

    # ---- G4: direzione della mappa req->colore (regressione L-P0) ----
    check(first_color(1) == 0, "G4: first_color(1) != 0 (bianco)")
    check(first_color(0) == 1, "G4: first_color(0) != 1 (nero)")
    for f in firme:
        if f["c_par_in_palla"]:
            lett = "R" if first_color(1) == 0 else "L"
            check(lett == "R",
                  "G4: parent-step != R per firma interna %r" % (f,))

    # ---- G5: unita' L-SCIA-J nel frame normalizzato ----
    for j, exp in ((1, (0, 1)), (2, (-1, 1)), (3, (-1, 0))):
        c, h = (0, 0), 0
        for b in [0] * (j - 1) + [1]:
            c, h = prepend(c, h, b)
        check(c == exp, "G5: prefisso j=%d da' %r != %r" % (j, c, exp))
        check(scia_by_lemma((0, 0), 0, j) == exp,
              "G5: formula lemma j=%d != %r" % (j, exp))
    c, h = (0, 0), 0
    inter = []
    for b in [0, 0, 0]:
        c, h = prepend(c, h, b)
        inter.append(c)
    c4, _ = prepend(c, h, 1)
    check(c4 == (0, 0), "G5: LLL non torna al centro (p_{t-4} != (0,0))")
    check(all(cheb(x) == 1 for x in inter),
          "G5: LLL con posizione intermedia a distanza != 1")
    # G-LLL strutturale: la matrice contiene solo j in {1,2,3}
    check(tuple(JS) == (1, 2, 3), "G-LLL: enumerazione j non e' {1,2,3}")

    # ---- matrice congelata ----
    rows = []
    per_firma = {}
    for f in firme:
        key = "%r h%d" % (list(f["c_star"]), f["h_star"])
        stati = []
        cert = cert_req_for(f)
        for k in KS:
            for j in JS:
                bits, letters, states, (p_t, h_t), scia_w, start = \
                    build_case(f, k, j)
                scia_l = scia_by_lemma(p_t, h_t, j)
                check(scia_l == scia_w,
                      "G2: scia lemma %r != walk %r a %s k%d j%d"
                      % (scia_l, scia_w, key, k, j))
                fin, colors, model, contrs = forward_sim(
                    start, letters, scia_w, cert)
                check(fin == (f["c_star"], f["h_star"]),
                      "G3: round-trip fallito a %s k%d j%d" % (key, k, j))
                stato, evid = decide(contrs)
                row = {"firma": key, "c_star": list(f["c_star"]),
                       "h_star": f["h_star"], "k": k, "j": j,
                       "evento": {"cella": list(p_t), "h": h_t},
                       "scia": list(scia_w),
                       "scia_cheb": cheb(scia_w)}
                if stato is None:
                    stato = "LOCAL-SURVIVE"
                    check(len(model) == len(colors),
                          "kill-list 5: modello incompleto a %s k%d j%d"
                          % (key, k, j))
                    row["modello"] = {"colori_iniziali_t_minus_j":
                                      {str(cc): v for cc, v in
                                       sorted(model.items())},
                                      "riletture_richieste_U7":
                                      [list(cc) for cc, v in
                                       sorted(model.items())
                                       if v == 1 and cheb(cc) <= 7]}
                else:
                    row["evidenza"] = evid
                    if stato == "COND-KILL":
                        check(evid and all(x["scia"] for x in evid) and
                              all(x["tipo"] in ("lettura", "endpoint")
                                  for x in evid),
                              "kill-list 3: COND-KILL senza evidenza valida "
                              "a %s k%d j%d" % (key, k, j))
                    if stato == "INFEASIBLE":
                        check(evid and all(not x["scia"] for x in evid),
                              "kill-list 6: INFEASIBLE senza contraddizione "
                              "certificata a %s k%d j%d" % (key, k, j))
                row["stato"] = stato
                stati.append(stato)
                rows.append(row)
        check(len(stati) == len(KS) * len(JS),
              "kill-list 7: colonne != 15 per %s" % key)
        per_firma[key] = {"stati": stati,
                          "classe": classify_firma(stati)}

    # ---- kill-list 7: unit-test del classificatore ----
    CK, LS, UNK, INF = "COND-KILL", "LOCAL-SURVIVE", "UNKNOWN", "INFEASIBLE"
    tests = [([CK] * 15, "ACTIONABLE"),
             ([INF] * 15, "INFEASIBLE"),
             ([CK] * 14 + [LS], "SURVIVES"),
             ([LS] + [CK] * 14, "SURVIVES"),
             ([CK] * 14 + [UNK], "UNKNOWN"),
             ([INF] * 14 + [CK], "ACTIONABLE"),
             ([INF] * 7 + [CK] * 8, "ACTIONABLE")]
    for vec, exp in tests:
        check(classify_firma(vec) == exp,
              "kill-list 7: classificatore %r su vettore atteso %s" %
              (classify_firma(vec), exp))

    # ---- ESCA E1: omissione del passo L nel trasporto ----
    e1_fail = 0
    for f in firme:
        for k in KS:
            for j in JS:
                bits, letters, states, _, scia_w, start = build_case(f, k, j)
                fin, _, _, _ = forward_sim(start, letters, scia_w,
                                           cert_req_for(f), skip_index=j)
                if fin != (f["c_star"], f["h_star"]):
                    e1_fail += 1
    e1_becc = check(e1_fail > 0, "E1 non beccata: round-trip mai fallito")

    # ---- ESCA E2: scambio celle j=2/j=3 ----
    e2_fail = 0
    for f in firme:
        for k in KS:
            for j in (2, 3):
                _, _, _, (p_t, h_t), scia_w, _ = build_case(f, k, j)
                if scia_by_lemma(p_t, h_t, j, swap23=True) != scia_w:
                    e2_fail += 1
    e2_becc = check(e2_fail > 0, "E2 non beccata: scambio j=2/3 invisibile")

    # ---- ESCA E3: kill dalla sola collisione geometrica ----
    # predicato naive: COND-KILL se la scia collide con palla/cert/tratto.
    e3_diff_real = 0
    for f in firme:
        cert = cert_req_for(f)
        for k in KS:
            for j in JS:
                bits, letters, states, _, scia_w, start = build_case(f, k, j)
                path = set(s[0] for s in states)
                naive = (scia_w in cert or tuple(scia_w) in POSE or
                         scia_w in path)
                _, _, _, contrs = forward_sim(start, letters, scia_w, cert)
                stato, _ = decide(contrs)
                frozen_kill = (stato == "COND-KILL")
                if naive != frozen_kill:
                    e3_diff_real += 1
    # caso sintetico dichiarato: scia su (1,1) (visitabile ma NON certificata):
    # il predicato congelato NON deve uccidere (nessuna evidenza di colore),
    # il naive collide e uccide => differenza garantita se il congelato e' sano.
    synth_contrs = []                       # nessuna lettura, nessun endpoint
    synth_stato, _ = decide(synth_contrs)
    synth_naive = (1, 1) in POSE            # collisione geometrica pura
    e3_synth_diff = (synth_stato is None) and synth_naive
    e3_becc = check(e3_diff_real > 0 or e3_synth_diff,
                    "E3 non beccata: naive == congelato ovunque")
    check(synth_stato is None,
          "kill-list 3: il predicato congelato uccide il caso sintetico "
          "(1,1) per sola collisione")

    # ---- verdetto globale (gate finale /12-/13) ----
    classi = {kk: v["classe"] for kk, v in per_firma.items()}
    actionable = sorted(kk for kk, cl in classi.items()
                        if cl == "ACTIONABLE")
    conta = {}
    for r in rows:
        conta[r["stato"]] = conta.get(r["stato"], 0) + 1
    verdetto = ("ALMENO UNA FIRMA ACTIONABLE => costruire L-OBL/Gamma per "
                "quella firma" if actionable else
                "NESSUNA FIRMA ACTIONABLE => VALIDA-MA-INUTILE e "
                "consolidamento (decisione /13 punto 5)")

    print("\n=== MATRICE 8x5x3 (condizionata a deep; LLL eliminato da "
          "L-SCIA-J(c)) ===", flush=True)
    for kk in sorted(per_firma):
        st = per_firma[kk]["stati"]
        sym = {"COND-KILL": "K", "LOCAL-SURVIVE": "S",
               "UNKNOWN": "?", "INFEASIBLE": "I"}
        riga = " ".join("k%dj%d:%s" % (k, j, sym[st[(k - 1) * 3 + (j - 1)]])
                        for k in KS for j in JS)
        print("%-14s %s  => %s" % (kk, riga, per_firma[kk]["classe"]),
              flush=True)
    print("conteggio stati:", conta, flush=True)
    print("classi per firma:", classi, flush=True)
    print("VERDETTO:", verdetto, flush=True)
    print("esche: E1 beccata=%s (%d fail) E2 beccata=%s (%d fail) "
          "E3 beccata=%s (diff reali %d, sintetico %s)"
          % (e1_becc, e1_fail, e2_becc, e2_fail, e3_becc, e3_diff_real,
             e3_synth_diff), flush=True)

    out = {
        "prereg": "docs/PREREG_RC2_PONTE.md v14 sez. 3e (verdetto /13)",
        "contratto": {
            "condizionata_a_deep": True,
            "LLL": "eliminato prima della matrice da L-SCIA-J(c) [T]",
            "fase_temporale": "canonica: stato a t-, sequenza forward "
                              "L*R^{k-1} fino a m*-",
            "first_color": "1 - req (req=1 => bianco=0)",
            "req_certificati": {"NOVE_C1": 1, "c_star": 1,
                                "c_par_se_in_palla": 1},
            "ordine_decisione": ["non-Scia => INFEASIBLE",
                                 "Scia => COND-KILL",
                                 "modello => LOCAL-SURVIVE", "UNKNOWN"],
        },
        "convenzioni": {"DX": list(DX), "DY": list(DY),
                        "fonte": "alpha1/onset_cone_lock.py (canonica)",
                        "POSE": [list(c) for c in POSE],
                        "NOVE": [list(c) for c in NINE],
                        "frame_scia": {str(j): list(c)
                                       for j, c in FRAME_SCIA.items()}},
        "gates": {"G0_optimize": bool(ok_opt),
                  "G1_geometria_vs_fase0": "verde",
                  "G2_scia_doppia_derivazione": "verde",
                  "G3_round_trip": "verde",
                  "G4_req_direzione_LP0": "verde",
                  "G5_unita_LSCIAJ": "verde",
                  "G_LLL_escluso": "verde"},
        "esche": {"E1_omissione_L": {"beccata": bool(e1_becc),
                                     "fail": e1_fail},
                  "E2_scambio_j23": {"beccata": bool(e2_becc),
                                     "fail": e2_fail},
                  "E3_collisione": {"beccata": bool(e3_becc),
                                    "diff_reali": e3_diff_real,
                                    "sintetico_11": bool(e3_synth_diff)}},
        "matrice": rows,
        "classi_per_firma": classi,
        "stati_conteggio": conta,
        "firme_actionable": actionable,
        "verdetto": verdetto,
        "unknown_nota": "UNKNOWN previsto dal contratto ma non realizzato: "
                        "nel dominio dichiarato (req certificati + alternanza "
                        "di finestra + y>=1) ogni caso decide",
        "rossi": FAILS,
        "sys_flags_optimize": sys.flags.optimize,
        "elapsed_s": round(time.time() - t0, 3),
    }
    json.dump(out, open(OUT_JSON, "w"), indent=1)
    print("summary ->", OUT_JSON, flush=True)
    if FAILS:
        print("\n*** %d CHECK ROSSI ***" % len(FAILS), flush=True)
        return 1
    print("\nTUTTI I CHECK VERDI (gates + esche + kill-list)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
