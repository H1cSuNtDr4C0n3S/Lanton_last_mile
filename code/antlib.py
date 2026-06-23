import ctypes, numpy as np, os

LIB = ctypes.CDLL("/home/claude/ant/libant.so")
LIB.simulate.restype = ctypes.c_long
LIB.simulate.argtypes = [
    ctypes.c_int,
    np.ctypeslib.ndpointer(np.int32), np.ctypeslib.ndpointer(np.int32), ctypes.c_long,
    ctypes.c_int, ctypes.c_int, ctypes.c_int,
    ctypes.c_long,
    np.ctypeslib.ndpointer(np.uint8),
    np.ctypeslib.ndpointer(np.uint8),
    ctypes.c_long,
    ctypes.c_void_p, ctypes.c_void_p,
]

P = 104  # highway period

def simulate(cells, ax, ay, ah, max_steps, H, snap_step=-1):
    """cells: (n,2) int array of black cells. Returns dict."""
    cells = np.asarray(cells, dtype=np.int32).reshape(-1, 2)
    xs = np.ascontiguousarray(cells[:, 0]); ys = np.ascontiguousarray(cells[:, 1])
    turns = np.zeros(max_steps, dtype=np.uint8)
    grid = np.zeros((2*H)*(2*H), dtype=np.uint8)
    if snap_step >= 0:
        sg = np.zeros((2*H)*(2*H), dtype=np.uint8)
        ss = np.zeros(3, dtype=np.int32)
        sgp, ssp = sg.ctypes.data_as(ctypes.c_void_p), ss.ctypes.data_as(ctypes.c_void_p)
    else:
        sg = ss = None; sgp = ssp = None
    n = LIB.simulate(H, xs, ys, len(cells), ax, ay, ah, max_steps,
                     turns, grid, snap_step, sgp, ssp)
    out = {"turns": turns[:n], "n": int(n), "hit_boundary": n < max_steps}
    if snap_step >= 0 and n > snap_step:
        out["snap_grid"] = sg.reshape(2*H, 2*H)
        out["snap_state"] = (int(ss[0]), int(ss[1]), int(ss[2]))
        out["H"] = H
    return out

def detect_onset(turns, min_periods=5):
    """Smallest t such that turns[t:] is exactly P-periodic with >= min_periods tail,
       with nonzero net drift. Returns (onset, word) or (None, None)."""
    n = len(turns)
    if n < (min_periods + 1) * P: return None, None
    d = turns[:-P] != turns[P:]
    idx = np.flatnonzero(d)
    onset = 0 if len(idx) == 0 else int(idx[-1]) + 1
    if n - onset < min_periods * P: return None, None
    word = turns[onset:onset + P].copy()
    # drift check: net displacement over one period must be nonzero, heading net 0 mod 4
    h, x, y = 0, 0, 0
    dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0]
    rot = 0
    for s in word:
        if s == 1: h = (h + 1) & 3; rot += 1
        else:      h = (h + 3) & 3; rot -= 1
        x += dx[h]; y += dy[h]
    if rot % 4 != 0: return None, None
    if x == 0 and y == 0: return None, None
    return onset, word

def cyc_hamming(w1, w2):
    """min Hamming distance between w1 and all cyclic shifts of w2 (len P)."""
    best = P + 1
    for s in range(P):
        d = int(np.sum(w1 != np.roll(w2, s)))
        if d < best: best = d
    return best

def classify_word(word, W0):
    """Returns ('W', d) or ('Wbar', d) or ('other', d)."""
    d0 = cyc_hamming(word, W0)
    d1 = cyc_hamming(word, 1 - W0)
    if d0 == 0: return "W", 0
    if d1 == 0: return "Wbar", 0
    return ("W~" if d0 < d1 else "Wbar~", min(d0, d1))

# C4 normalization: rotate frame so heading -> 0 (up), ant at origin.
# Rotation by 90deg CW k times maps heading h -> h+k. We need h+k=0 mod 4 -> k=(-h)%4.
def rot_cw(pts, k):
    """rotate points 90deg clockwise k times: (x,y) -> (-y, x)"""
    pts = np.asarray(pts, dtype=np.int64).reshape(-1, 2)
    for _ in range(k % 4):
        pts = np.stack([-pts[:, 1], pts[:, 0]], axis=1)
    return pts

def normalize_C4(cells, ax, ay, ah):
    """translate ant to origin, rotate so heading=0. Returns cells (n,2)."""
    c = np.asarray(cells, dtype=np.int64).reshape(-1, 2) - np.array([ax, ay])
    k = (-ah) % 4
    return rot_cw(c, k)

def reflect_x(cells, ah):
    """reflect across vertical axis through origin: x -> -x. heading: 0->0,1->3,2->2,3->1"""
    c = np.asarray(cells, dtype=np.int64).reshape(-1, 2).copy()
    c[:, 0] = -c[:, 0]
    return c, (4 - ah) % 4 if ah % 2 == 1 else ah

def canon_C4(cells):
    """canonical form under C4 + translation: lexicographic min over 4 rotations,
       each translated to min corner. Returns bytes key."""
    best = None
    for k in range(4):
        p = rot_cw(cells, k)
        p = p - p.min(axis=0)
        key = p[np.lexsort((p[:, 1], p[:, 0]))].tobytes() + bytes([p.shape[0] % 251])
        if best is None or key < best: best = key
    return best
