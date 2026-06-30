"""
entry_seed/reverse.py  (sessione §76)

Mappa DIRETTA e INVERSA della formica di Langton su griglia sparsa (set di celle nere).
Convenzioni IDENTICHE a code/libant.c e CLAUDE.md §2:
  bianco(0) -> svolta R (h+1), flip a nero,  mossa di 1
  nero(1)   -> svolta L (h-1), flip a bianco, mossa di 1
  heading: 0=su(-y), 1=destra(+x), 2=giu(+y), 3=sinistra(-x); turns[t]: 1=R, 0=L

MAPPA INVERSA (deterministica: UNA sola preimmagine; nessun albero).
  Stato corrente (x,y,h): la formica e' appena entrata in (x,y) muovendosi in direzione h
  da p_prev = (x,y)-dir(h). Il COLORE ATTUALE di p_prev decide il tipo di svolta forward:
    p_prev nero   => era bianco prima del flip => svolta R fu fatta => h_prev=h-1; p_prev torna BIANCO
    p_prev bianco => era nero  prima del flip => svolta L fu fatta => h_prev=h+1; p_prev torna NERO

Self-test (python entry_seed/reverse.py):
  1) forward Python == motore C (code/libant.c) per 12000 passi da griglia vuota;
  2) round-trip: dallo stato a t=12000 inverto 12000 passi e recupero griglia vuota + (0,0,0).
"""
import os
import numpy as np

DX = (0, 1, 0, -1)
DY = (-1, 0, 1, 0)


def fwd_step(black, x, y, h):
    if (x, y) in black:
        h = (h + 3) & 3; black.discard((x, y)); turn = 0
    else:
        h = (h + 1) & 3; black.add((x, y)); turn = 1
    x += DX[h]; y += DY[h]
    return x, y, h, turn


def inv_step(black, x, y, h):
    xp = x - DX[h]; yp = y - DY[h]
    if (xp, yp) in black:           # svolta R era stata fatta: ripristina bianco
        h_prev = (h - 1) & 3; black.discard((xp, yp)); turn = 1
    else:                            # svolta L era stata fatta: ripristina nero
        h_prev = (h + 1) & 3; black.add((xp, yp)); turn = 0
    return xp, yp, h_prev, turn


def run_fwd(black0, x0, y0, h0, steps):
    black = set(black0); x, y, h = x0, y0, h0
    turns = np.empty(steps, dtype=np.uint8)
    for t in range(steps):
        x, y, h, turns[t] = fwd_step(black, x, y, h)
    return black, (x, y, h), turns


def run_inv(black0, x0, y0, h0, steps):
    black = set(black0); x, y, h = x0, y0, h0
    turns = np.empty(steps, dtype=np.uint8)
    for t in range(steps):
        x, y, h, turns[t] = inv_step(black, x, y, h)
    return black, (x, y, h), turns


def _selftest():
    import ctypes, subprocess, tempfile
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = os.path.join(repo, "code", "libant.c")
    so = os.path.join(tempfile.gettempdir(), "libant_s76.so")
    subprocess.run(["gcc", "-O3", "-shared", "-fPIC", "-o", so, src], check=True)
    LIB = ctypes.CDLL(so); LIB.simulate.restype = ctypes.c_long
    LIB.simulate.argtypes = [ctypes.c_int,
        np.ctypeslib.ndpointer(np.int32), np.ctypeslib.ndpointer(np.int32), ctypes.c_long,
        ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_long,
        np.ctypeslib.ndpointer(np.uint8), np.ctypeslib.ndpointer(np.uint8),
        ctypes.c_long, ctypes.c_void_p, ctypes.c_void_p]
    T, H = 12000, 600
    turns = np.zeros(T, dtype=np.uint8); grid = np.zeros((2 * H) * (2 * H), dtype=np.uint8)
    nC = LIB.simulate(H, np.zeros(0, np.int32), np.zeros(0, np.int32), 0, 0, 0, 0, T,
                      turns, grid, -1, None, None)
    blackF, stateF, turnsF = run_fwd(set(), 0, 0, 0, T)
    agree = np.array_equal(turnsF, turns[:nC])
    xF, yF, hF = stateF
    blackB, stateB, turnsB = run_inv(blackF, xF, yF, hF, T)
    print("ENGINE AGREEMENT (Python fwd vs C, %d passi): %s" % (T, agree))
    print("ROUND-TRIP: griglia vuota=%s stato(0,0,0)=%s (stato=%s)"
          % (len(blackB) == 0, stateB == (0, 0, 0), stateB))
    print("ROUND-TRIP: turni invertiti == forward[::-1]: %s" % np.array_equal(turnsB[::-1], turnsF))
    print("Supporto a t=%d: %d celle nere" % (T, len(blackF)))
    assert agree and len(blackB) == 0 and stateB == (0, 0, 0)
    print("SELF-TEST OK")


if __name__ == "__main__":
    _selftest()
