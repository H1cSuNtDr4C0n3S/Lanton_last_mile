"""
entry_seed/clib.py  (sessione §76)
Loader autosufficiente del simulatore C (code/libant.c) + onset detection / classificazione W0.
Costruisce libant.so in tmp al primo import; nessun percorso assoluto hard-coded.
Convenzioni invariate (CLAUDE.md §2). Riusa i casi di riferimento: vuota->9977, (7,-7)->106258.
"""
import os, ctypes, subprocess, tempfile
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = 104
W0 = np.load(os.path.join(REPO, "data", "W0.npy"))

_so = os.path.join(tempfile.gettempdir(), "libant_s76.so")
if not os.path.exists(_so) or os.path.getmtime(_so) < os.path.getmtime(os.path.join(REPO, "code", "libant.c")):
    subprocess.run(["gcc", "-O3", "-shared", "-fPIC", "-o", _so,
                    os.path.join(REPO, "code", "libant.c")], check=True)
_LIB = ctypes.CDLL(_so)
_LIB.simulate.restype = ctypes.c_long
_LIB.simulate.argtypes = [ctypes.c_int,
    np.ctypeslib.ndpointer(np.int32), np.ctypeslib.ndpointer(np.int32), ctypes.c_long,
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_long,
    np.ctypeslib.ndpointer(np.uint8), np.ctypeslib.ndpointer(np.uint8),
    ctypes.c_long, ctypes.c_void_p, ctypes.c_void_p]


def simulate(cells, ax, ay, ah, max_steps, H):
    cells = np.asarray(cells, dtype=np.int32).reshape(-1, 2)
    xs = np.ascontiguousarray(cells[:, 0]); ys = np.ascontiguousarray(cells[:, 1])
    turns = np.zeros(max_steps, dtype=np.uint8)
    grid = np.zeros((2 * H) * (2 * H), dtype=np.uint8)
    n = _LIB.simulate(H, xs, ys, len(cells), ax, ay, ah, max_steps, turns, grid, -1, None, None)
    return {"turns": turns[:n], "n": int(n), "hit_boundary": n < max_steps}


def detect_onset(turns, min_periods=5):
    n = len(turns)
    if n < (min_periods + 1) * P:
        return None, None
    d = turns[:-P] != turns[P:]
    idx = np.flatnonzero(d)
    onset = 0 if len(idx) == 0 else int(idx[-1]) + 1
    if n - onset < min_periods * P:
        return None, None
    word = turns[onset:onset + P].copy()
    h, x, y = 0, 0, 0
    dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0]; rot = 0
    for s in word:
        if s == 1: h = (h + 1) & 3; rot += 1
        else:      h = (h + 3) & 3; rot -= 1
        x += dx[h]; y += dy[h]
    if rot % 4 != 0 or (x == 0 and y == 0):
        return None, None
    return onset, word


def _cyc_hamming(w1, w2):
    return min(int(np.sum(w1 != np.roll(w2, s))) for s in range(P))


def classify_word(word, W=W0):
    d0 = _cyc_hamming(word, W); d1 = _cyc_hamming(word, 1 - W)
    if d0 == 0: return "W", 0
    if d1 == 0: return "Wbar", 0
    return ("W~" if d0 < d1 else "Wbar~", min(d0, d1))


def lock_position(turns, onset, ax=0, ay=0, ah=0):
    dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0]
    h, x, y = ah, ax, ay
    for t in range(onset):
        h = (h + 1) & 3 if turns[t] == 1 else (h + 3) & 3
        x += dx[h]; y += dy[h]
    return x, y
