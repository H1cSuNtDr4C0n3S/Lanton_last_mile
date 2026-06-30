import sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import clib as A
from reverse import run_fwd, DX, DY

W0 = A.W0

# ---- Frontiera Q1: supporto -> min onset (verificati) ----
frontier = [(0, 9977), (1, 310), (2, 162), (3, 142), (4, 71), (5, 62), (13, 0)]

# ---- Semi campioni (verificati con antlib) ----
germ0 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"germs_22.json")))["0"]
champions = {
    "Germe fase 0\n13 celle · onset 0": (germ0["germ"], germ0["ax"], germ0["ay"], germ0["ah"]),
    "1 cella · onset 310\n(ingresso più rapido a b=1)": ([[0, -2]], 0, 0, 0),
    "2 celle · onset 276 · dist 0\n(aggancio sul punto di partenza)": ([[0, -1], [1, -1]], 0, 0, 0),
    "4 celle · onset 71\n(ingresso più rapido trovato)": ([[-2, -1], [-1, 0], [-1, 3], [2, 3]], 0, 0, 0),
}


def lock_pos(cells, ax, ay, ah):
    r = A.simulate(np.array(cells).reshape(-1, 2), ax, ay, ah, 200000, 1500)
    onset, word = A.detect_onset(r["turns"])
    if onset is None:
        return None, None
    h, x, y = ah, ax, ay
    for t in range(onset):
        if r["turns"][t] == 1: h = (h + 1) & 3
        else: h = (h + 3) & 3
        x += DX[h]; y += DY[h]
    return onset, (x, y)


fig = plt.figure(figsize=(15, 9))
gs = fig.add_gridspec(2, 4, height_ratios=[1.25, 1.0], hspace=0.32, wspace=0.3)

# --- Pannello frontiera ---
axf = fig.add_subplot(gs[0, :2])
xs = [b for b, _ in frontier]; ys = [max(o, 0.5) for _, o in frontier]
axf.plot(xs, ys, "o-", color="#1f3a93", lw=2, ms=7, zorder=3)
axf.set_yscale("log")
for b, o in frontier:
    axf.annotate(str(o), (b, max(o, 0.5)), textcoords="offset points", xytext=(6, 6),
                 fontsize=9, color="#222")
axf.axhspan(0.5, 0.7, color="#2ecc71", alpha=0.15)
axf.text(9.5, 1.0, "germe: onset 0", color="#1a7a3a", fontsize=9)
axf.set_xlabel("supporto del seme (celle nere)")
axf.set_ylabel("onset minimo  (passi all'ingresso)")
axf.set_title("Q1 — frontiera di Pareto: supporto vs ingresso più rapido", fontsize=12, weight="bold")
axf.grid(True, which="both", alpha=0.25)
axf.set_xticks(range(0, 14))

# --- Pannello testo sintesi ---
axt = fig.add_subplot(gs[0, 2:]); axt.axis("off")
txt = (
    "REVERSIBILITÀ  (verificata: round-trip 12 000 passi → griglia vuota)\n"
    "  · una sola orbita all'indietro; nessun albero di preimmagini.\n\n"
    "Q1 — seme minimo, ingresso più rapido\n"
    "  · NON c'è dilemma severo: anche 1 cella entra in 310 passi\n"
    "    (vs 9977 della griglia vuota).\n"
    "  · la frontiera crolla subito e si appiattisce verso il germe.\n"
    "  · germe minimo globale = 13 celle, onset 0 (fasi 0 e 103).\n\n"
    "Q2 — seme minimo, aggancio più vicino al punto di partenza\n"
    "  · 1 cella: distanza minima = 3.\n"
    "  · 2 celle: distanza = 0 (aggancio ESATTO sul punto di partenza),\n"
    "    onset 276 — seme {(0,−1),(1,−1)}.\n\n"
    "LIMITE  (onesto)\n"
    "  · tutto vive nel bacino: per reversibilità l'orbita eterna\n"
    "    non-highway (se esiste) sta in un'altra classe e nessuno\n"
    "    di questi semi la tocca. Raffina la bocca, non chiude α1."
)
axt.text(0.0, 0.98, txt, va="top", ha="left", fontsize=10.2, family="monospace",
         transform=axt.transAxes)

# --- Pannelli griglia campioni ---
def draw_seed(ax, cells, ax0, ay0, title):
    cells = np.array(cells).reshape(-1, 2)
    onset, lock = lock_pos(cells, ax0, ay0, 0)
    allx = list(cells[:, 0]) + [ax0] + ([lock[0]] if lock else [])
    ally = list(cells[:, 1]) + [ay0] + ([lock[1]] if lock else [])
    pad = 1.5
    xlo, xhi = min(allx) - pad, max(allx) + pad
    ylo, yhi = min(ally) - pad, max(ally) + pad
    for (cx, cy) in cells:
        ax.add_patch(Rectangle((cx - 0.5, cy - 0.5), 1, 1, color="#111", zorder=2))
    # ant start (origin) marker
    ax.plot(ax0, ay0, marker="^", color="#e74c3c", ms=13, zorder=4,
            markeredgecolor="white", markeredgewidth=0.8)
    # lock point
    if lock:
        ax.plot(lock[0], lock[1], marker="*", color="#27ae60", ms=16, zorder=4,
                markeredgecolor="white", markeredgewidth=0.8)
    ax.set_xlim(xlo, xhi); ax.set_ylim(yhi, ylo)  # invert y (y down)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title, fontsize=9.5)
    for s in ax.spines.values():
        s.set_edgecolor("#bbb")

for i, (title, (cells, ax0, ay0, ah)) in enumerate(champions.items()):
    ax = fig.add_subplot(gs[1, i])
    draw_seed(ax, cells, ax0, ay0, title)

# legenda comune
from matplotlib.lines import Line2D
leg = [Line2D([0], [0], marker="^", color="w", markerfacecolor="#e74c3c", ms=11, label="partenza formica (origine)"),
       Line2D([0], [0], marker="*", color="w", markerfacecolor="#27ae60", ms=13, label="punto di aggancio (lock)"),
       Line2D([0], [0], marker="s", color="w", markerfacecolor="#111", ms=10, label="cella nera del seme")]
fig.legend(handles=leg, loc="lower center", ncol=3, fontsize=10, frameon=False, bbox_to_anchor=(0.5, -0.01))

fig.suptitle("Formica di Langton — semi minimi d'ingresso in autostrada", fontsize=14, weight="bold")
fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontiera_semi.png"), dpi=130, bbox_inches="tight")
print("OK figura salvata")
print("Frontiera:", frontier)
