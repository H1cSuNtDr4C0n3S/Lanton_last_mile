# -*- coding: utf-8 -*-
"""Figura §88: struttura delle parole best-per-K della caccia all'arma.

Tre pannelli:
  A) raster delle parole allineate al suffisso (le parole crescono per prepend:
     i suffissi condivisi appaiono come bande verticali; righe rosse = rotture
     di catena, dove best(K+1) NON estende best(K));
  B) dot-plot di auto-similarita' della parola K=120 (run diagonali >= LMIN
     = motivi ripetuti interni);
  C) dot-plot della parola K=120 contro W0 ciclica (frammenti di highway).

Con baseline nulla (shuffle a conteggi L/R fissati) per LRS interna e LCS vs W0,
metodo §84: nessun claim di struttura senza confronto col caso.
"""
import json
import random
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

SUMMARY = HERE / "record_weapon_summary.json"
W0_TXT = ROOT / "data" / "w0.txt"
OUT_PNG = HERE / "record_weapon_words.png"

LMIN = 6          # lunghezza minima dei run nei dot-plot
N_SHUFFLE = 500   # baseline nulla
RNG_SEED = 88     # riproducibilita'


def load_words():
    d = json.loads(SUMMARY.read_text())
    bpk = {int(k): v for k, v in d["best_per_K"].items()}
    return d, dict(sorted(bpk.items()))


def word_to_bits(w):
    return np.frombuffer(w.encode(), dtype=np.uint8) == ord("R")


def runfilter_dotplot(a, b, lmin):
    """Matrice di match a[i]==b[j], tenendo solo i punti su run diagonali >= lmin."""
    n, m = len(a), len(b)
    M = (a[:, None] == b[None, :])
    keep = np.zeros_like(M)
    for d in range(-(n - 1), m):
        diag = np.diagonal(M, offset=d)
        L = len(diag)
        run = 0
        starts = []
        for i in range(L + 1):
            if i < L and diag[i]:
                run += 1
            else:
                if run >= lmin:
                    starts.append((i - run, run))
                run = 0
        for s, r in starts:
            for i in range(s, s + r):
                ii = i if d >= 0 else i - d
                jj = i + d if d >= 0 else i
                keep[ii, jj] = True
    return keep


def lcs_len(a, b):
    """Lunghezza della piu' lunga sottostringa comune (DP rolling)."""
    n, m = len(a), len(b)
    prev = [0] * (m + 1)
    best = 0
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        ai = a[i - 1]
        for j in range(1, m + 1):
            if ai == b[j - 1]:
                v = prev[j - 1] + 1
                cur[j] = v
                if v > best:
                    best = v
        prev = cur
    return best


def lrs_len(a):
    """Piu' lunga sottostringa ripetuta (occorrenze a inizio diverso, overlap ok)."""
    n = len(a)
    prev = [0] * (n + 1)
    best = 0
    for i in range(1, n + 1):
        cur = [0] * (n + 1)
        ai = a[i - 1]
        for j in range(i + 1, n + 1):
            if ai == a[j - 1]:
                v = prev[j - 1] + 1
                cur[j] = v
                if v > best:
                    best = v
        prev = cur
    return best


def find_lcs(a, b):
    """(lunghezza, i, j) della LCS tra stringhe a e b."""
    n, m = len(a), len(b)
    prev = [0] * (m + 1)
    best, bi, bj = 0, -1, -1
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best, bi, bj = cur[j], i - best, j - best
        prev = cur
    # bi/bj ricalcolati sotto per chiarezza
    prev = [0] * (m + 1)
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] == best and bi < 0:
                    bi, bj = i - best, j - best
        prev = cur
    return best, bi, bj


def main():
    d, bpk = load_words()
    ks = list(bpk)
    W = max(len(bpk[k]["word"]) for k in ks)
    w0 = W0_TXT.read_text().strip()
    assert len(w0) == 104, f"W0 attesa 104, trovata {len(w0)}"

    # ---- pannello A: raster suffisso-allineato ----
    raster = np.full((len(ks), W), np.nan)
    burden = np.zeros((len(ks), 1))
    for r, k in enumerate(ks):
        w = bpk[k]["word"]
        raster[r, W - len(w):] = word_to_bits(w).astype(float)
        burden[r, 0] = bpk[k]["burden1"]
    # rotture di catena: best(K+1) non termina con best(K)
    breaks = [r for r, k in enumerate(ks[:-1])
              if not bpk[ks[r + 1]]["word"].endswith(bpk[k]["word"])]

    # ---- dot-plot: parola K=120 ----
    kbig = ks[-1]
    wbig = bpk[kbig]["word"]
    abig = word_to_bits(wbig)
    selfdot = runfilter_dotplot(abig, abig, LMIN)
    np.fill_diagonal(selfdot, False)  # la diagonale principale e' banale
    w0d = w0 + w0  # ciclica
    crossdot = runfilter_dotplot(abig, word_to_bits(w0d), LMIN)

    # ---- statistiche + baseline nulla ----
    lrs_real = lrs_len(wbig)
    lcs_real, ci, cj = find_lcs(wbig, w0d)
    lcs_frag = wbig[ci:ci + lcs_real] if ci >= 0 else ""

    rng = random.Random(RNG_SEED)
    chars = list(wbig)
    lrs_null, lcs_null = [], []
    for _ in range(N_SHUFFLE):
        rng.shuffle(chars)
        s = "".join(chars)
        lrs_null.append(lrs_len(s))
        lcs_null.append(lcs_len(s, w0d))
    lrs_null = np.array(lrs_null)
    lcs_null = np.array(lcs_null)

    def pval(null, real):
        return float((null >= real).mean())

    print(f"parola K={kbig} (len {len(wbig)}): {wbig}")
    print(f"LRS interna: {lrs_real}  | nulla: media {lrs_null.mean():.1f}, "
          f"max {lrs_null.max()}, P(null>=reale)={pval(lrs_null, lrs_real):.3f}")
    print(f"LCS vs W0 ciclica: {lcs_real} ('{lcs_frag}') a pos parola {ci}, "
          f"pos W0 {cj % 104} | nulla: media {lcs_null.mean():.1f}, "
          f"max {lcs_null.max()}, P(null>=reale)={pval(lcs_null, lcs_real):.3f}")

    # occorrenze del motivo LRS
    lrs_frag = ""
    if lrs_real > 0:
        for i in range(len(wbig) - lrs_real + 1):
            f = wbig[i:i + lrs_real]
            if wbig.count(f) >= 2:
                lrs_frag = f
                occ = [j for j in range(len(wbig) - lrs_real + 1)
                       if wbig[j:j + lrs_real] == f]
                print(f"motivo LRS: '{f}' occorrenze a {occ}")
                break

    # ---- figura ----
    fig = plt.figure(figsize=(17, 11))
    gs = fig.add_gridspec(2, 3, width_ratios=[0.06, 1.35, 1.0],
                          height_ratios=[1, 1], wspace=0.12, hspace=0.25)

    cmap = ListedColormap(["#2166ac", "#e08214"])  # L blu, R arancio
    cmap.set_bad("white")

    axb = fig.add_subplot(gs[:, 0])
    axb.imshow(burden, aspect="auto", cmap="viridis_r",
               extent=(0, 1, ks[-1] + 0.5, ks[0] - 0.5))
    axb.set_xticks([])
    axb.set_ylabel("K (lunghezza parola)")
    axb.set_title("burden1", fontsize=9)
    for r, k in enumerate(ks):
        if r == 0 or bpk[k]["burden1"] != bpk[ks[r - 1]]["burden1"]:
            axb.text(0.5, k, str(bpk[k]["burden1"]), ha="center", va="center",
                     fontsize=7, color="white")

    axA = fig.add_subplot(gs[:, 1], sharey=axb)
    axA.imshow(raster, aspect="auto", cmap=cmap, interpolation="nearest",
               extent=(-W, 0, ks[-1] + 0.5, ks[0] - 0.5))
    for r in breaks:
        axA.axhline(ks[r] + 0.5, color="red", lw=1.2)
    axA.set_xlabel("posizione dalla fine della parola (0 = ultima lettera)")
    axA.set_title(f"parole best per K, allineate al suffisso  "
                  f"(blu=L, arancio=R; righe rosse = rottura di catena)")
    plt.setp(axA.get_yticklabels(), visible=False)

    axB = fig.add_subplot(gs[0, 2])
    axB.imshow(selfdot, aspect="equal", cmap="Greys", interpolation="nearest")
    axB.set_title(f"auto-similarita' parola K={kbig} (run ≥ {LMIN})\n"
                  f"LRS={lrs_real} (nulla max {lrs_null.max()}, "
                  f"p={pval(lrs_null, lrs_real):.2f})", fontsize=10)
    axB.set_xlabel("j")
    axB.set_ylabel("i")

    axC = fig.add_subplot(gs[1, 2])
    axC.imshow(crossdot, aspect="auto", cmap="Greys", interpolation="nearest")
    axC.axvline(104 - 0.5, color="red", lw=0.8, ls="--")
    axC.set_title(f"parola K={kbig} vs W0 ciclica (run ≥ {LMIN})\n"
                  f"LCS={lcs_real} (nulla max {lcs_null.max()}, "
                  f"p={pval(lcs_null, lcs_real):.2f})", fontsize=10)
    axC.set_xlabel("posizione in W0+W0 (tratteggio = cucitura ciclica)")
    axC.set_ylabel("posizione nella parola")

    fig.suptitle("§88 caccia all'arma (beam 4000, kmax 120, viable-k 8): "
                 "struttura delle parole minime record-compatibili", fontsize=13)
    fig.savefig(OUT_PNG, dpi=140, bbox_inches="tight")
    print(f"scritto {OUT_PNG}")


if __name__ == "__main__":
    sys.exit(main())
