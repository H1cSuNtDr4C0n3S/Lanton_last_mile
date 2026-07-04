# u2_far_ball2_machine.py — §93 (U2-LONTANO): la MACCHINA DEL LEDGER IN PALLA-2.
#
# IDEA. La palla-2 del record (10 celle: x in [-2,2], y in {1,2}) sta TUTTA
# dentro la striscia S_CORE della macchina §92 (16 celle). I pending della
# palla-2 sono leggibili direttamente dallo stato astratto: pending(c) <=>
# req(c)==0 (u2_far_ledger). Quindi la domanda di U2-LONTANO al raggio 2 —
# "esiste un'estensione all'indietro di una coprente-nera che chiude TUTTI i
# pending della palla-2 e finisce (nascita) fuori dalla palla?" — e' decidibile
# nella SOVRA-approssimazione: BFS post-copertura dall'insieme di TUTTE le
# 47.312 coperture-nere astratte (fase 1 §92), transizioni esatte-in-S + OUT
# astratto (rientro libero con cella-giovane, lemma di sovra-approssimazione
# DEDUTTIVO §92a: ogni transizione reale e' ammessa; req|S congelato fuori).
#
#   Se NESSUNO stato raggiungibile ha (zero pending in palla-2) E (posa fuori
#   dalla palla-2: OUT oppure cella di S con cheb > 2), allora NESSUNA
#   estensione reale di NESSUNA coprente-nera lo realizza (la macchina
#   sovra-approssima) => TEOREMA:
#
#   TEOREMA DEL LEDGER SPORCO (bersaglio): per ogni orbita, a ogni record y-min
#   stretto con suffisso coprente-nera+w101 e palla-2 del record priva di seme
#   e di origine, il passato completo NON esiste: il ledger della palla-2 non
#   si chiude mai. Con U1 (§91) e il corno 1 (seme in palla), il Muro dietro
#   l'Uno si chiude al raggio 2 (+ intorno finito), SENZA alcun bound su D.
#
#   Se invece stati puliti astratti ESISTONO: nessuna conclusione (trappola c:
#   la sovra-approssimazione trasferisce solo la morte) — si riporta il profilo
#   (quanti, da quali coperture, min pending) e la falsificazione resta aperta.
#
# GATE:
#   B0 fase 1 §92 riprodotta (stati, |cov_n|, |cov_b| identici al summary);
#   B1 membership: le 6 coprenti nere400 + 2 jackpot replayate nel raggiungibile
#      e i loro stati di copertura dentro cov_n (replay_extension §92);
#   B2 coerenza ledger: pend2(stato di copertura astratto) == pend2 calcolato
#      dalla parola reale ristretta alla palla-2, sugli 8 testimoni;
#   B3 la ricerca DEVE poter fallire: si verifica che stati con pend2 BASSO
#      (<= 2) siano raggiunti (il minimo della caccia reale), cosi' il "nessuno
#      stato pulito" non e' un artefatto di raggiungibilita' troppo povera.
#
# Uscita: alpha1/u2_far_ball2_machine_summary.json
import sys, os, json, time, argparse
from collections import deque, Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_weapon_vitality import to_bits, SUMMARY
from u2_cover_rail_map import valid
from u2_pocket_certificate import (Machine, S_CORE, TGT, FREE,
                                   exact_state, exact_step, replay_extension)
from u2_far_ledger import cheb
from onset_cone_lock import DX, DY

HERE = os.path.dirname(os.path.abspath(__file__))
WIT = os.path.join(HERE, "u2_cover_witnesses.json")
P92 = os.path.join(HERE, "u2_pocket_certificate_summary.json")
OUT_JSON = os.path.join(HERE, "u2_far_ball2_machine_summary.json")

BALL2 = [(x, y) for x in range(-2, 3) for y in (1, 2)]


class PostCoverMachine(Machine):
    """Transizioni post-copertura: (1,1) e' una cella ordinaria (il TGT
    special-case di fase 1 non si applica piu'); uscita dalla striscia = OUT."""

    def post_succ(self, ci, h, rt):
        c = self.S[ci]
        cn = (c[0] - DX[h], c[1] - DY[h])
        succ = []
        if cn in self.idx:
            j = self.idx[cn]
            for bit in (0, 1):
                read = 0 if bit == 1 else 1
                if rt[j] != FREE and rt[j] != read:
                    continue
                r2 = list(rt); r2[j] = 1 - read
                hn = (h - 1) & 3 if bit == 1 else (h + 1) & 3
                succ.append(("I", j, hn, tuple(r2)))
            return succ
        if cn[1] < 1:
            return succ                       # morte
        succ.append(("O", rt))                # esce dalla striscia
        return succ


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state-cap", type=int, default=12_000_000)
    args = ap.parse_args()
    t0 = time.time()

    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    M = PostCoverMachine(S_CORE)
    ball_idx = [M.idx[c] for c in BALL2]
    far_in = {i for i, c in enumerate(M.S) if cheb(c) > 2}

    # ---------- GATE B0: fase 1 riprodotta ----------
    seen1, cov_n, cov_b = M.phase1(M.w101_start(w101))
    p92 = json.load(open(P92))
    assert len(seen1) == p92["fase1"]["stati"], "fase 1 non riprodotta"
    assert len(cov_n) == p92["fase1"]["cov_nere"]
    assert len(cov_b) == p92["fase1"]["cov_bianche"]
    print(f"GATE B0 verde: fase 1 riprodotta ({len(seen1)} stati, "
          f"{len(cov_n)} coperture nere)", flush=True)

    # ---------- GATE B1/B2: testimoni reali dentro cov_n + ledger coerente ----
    wit = json.load(open(WIT))
    n_checked = 0
    for grp in ("jackpot", "nere400"):
        for w in wit[grp]:
            e2 = to_bits(w["word"])
            h1, rt, col = replay_extension(w101, e2, M, seen1)
            assert col == "B" and (h1, rt) in cov_n, "testimone fuori cov_n!"
            # ledger dalla parola reale, ristretto alla palla-2
            _, _, req_real = exact_state(e2 + w101)
            pend2_real = {c for c in BALL2 if req_real.get(c, FREE) == 0}
            pend2_abs = {M.S[j] for j in ball_idx if rt[j] == 0}
            assert pend2_real == pend2_abs, "ledger palla-2 incoerente!"
            n_checked += 1
    print(f"GATE B1/B2 verdi: {n_checked}/8 testimoni in cov_n, ledger "
          f"palla-2 astratto == reale", flush=True)

    # ---------- BFS post-copertura da TUTTE le coperture nere ----------
    def pend2(rt):
        return sum(1 for j in ball_idx if rt[j] == 0)

    def is_far_pose(st):
        return st[0] == "O" or st[1] in far_in

    seen = set()
    q = deque()
    for (h1, rt) in cov_n:
        st = ("I", M.ti, h1, rt)
        if st not in seen:
            seen.add(st); q.append(st)
    clean = []
    minp = Counter()
    min_seen = 99
    while q:
        st = q.popleft()
        if st[0] == "I":
            succ = M.post_succ(st[1], st[2], st[3])
        else:
            succ = M.out_succ(st[1])
        for s2 in succ:
            if s2 in seen:
                continue
            if len(seen) >= args.state_cap:
                raise RuntimeError("cap stati: macchina troppo grande")
            seen.add(s2); q.append(s2)
            rt2 = s2[3] if s2[0] == "I" else s2[1]
            p2 = pend2(rt2)
            if p2 < min_seen:
                min_seen = p2
                print(f"  nuovo minimo pend2 = {p2} "
                      f"({len(seen)} stati)", flush=True)
            minp[p2] += 1
            if p2 == 0 and is_far_pose(s2):
                clean.append(s2)
                if len(clean) <= 3:
                    print(f"  STATO PULITO trovato: {s2[:3]}...", flush=True)

    print(f"\nBFS post-copertura: {len(seen)} stati raggiungibili "
          f"({round(time.time()-t0,1)}s)", flush=True)
    print(f"distribuzione pend2 sugli stati NUOVI: "
          f"{dict(sorted(minp.items()))}", flush=True)

    # ---------- GATE B3: la macchina raggiunge pend2 bassi ----------
    assert min_seen <= 2, ("gate B3: la macchina non raggiunge nemmeno "
                           "pend2<=2 — raggiungibilita' sospetta")
    print(f"GATE B3 verde: pend2 minimo raggiunto = {min_seen} "
          f"(la ricerca puo' fallire, e infatti...)", flush=True)

    # ---------- verdetto ----------
    print("\n================ VERDETTO §93 (macchina palla-2) ================",
          flush=True)
    if not clean:
        # distinguo: esistono stati pend2==0 ma MAI con posa lontana?
        n_p0 = minp.get(0, 0)
        print(f"NESSUNO stato pulito (pend2=0 E posa fuori palla-2) "
              f"raggiungibile su {len(seen)} stati.", flush=True)
        print(f"  (stati con pend2=0 e posa DENTRO la palla: {n_p0})", flush=True)
        print("=> TEOREMA DEL LEDGER SPORCO (raggio 2), modulo i gate sopra:",
              flush=True)
        print("   nessuna estensione all'indietro di NESSUNA coprente-nera",
              flush=True)
        print("   chiude il ledger della palla-2 con nascita fuori dalla palla.",
              flush=True)
    else:
        print(f"{len(clean)} STATI PULITI astratti raggiungibili: "
              f"NESSUNA conclusione (trappola c) — profilo salvato.", flush=True)

    out = {"args": vars(args),
           "fase1": {"stati": len(seen1), "cov_nere": len(cov_n)},
           "post_bfs": {"stati": len(seen), "pend2_distr":
                        {str(k): v for k, v in sorted(minp.items())},
                        "pend2_min": min_seen,
                        "stati_puliti_lontani": len(clean),
                        "stati_pend0_vicini": minp.get(0, 0)},
           "teorema": (len(clean) == 0),
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nscritto {OUT_JSON} in {out['elapsed_s']} s", flush=True)


if __name__ == "__main__":
    main()
