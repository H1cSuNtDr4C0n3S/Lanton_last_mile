import sys
from collections import Counter
sys.setrecursionlimit(10000)

# Dinamica (CLAUDE.md §2): lettura -> svolta (bianco=R orario, nero=L) -> flip -> mossa 1.
# heading 0=su(0,1) 1=destra(1,0) 2=giu(0,-1) 3=sinistra(-1,0)
DIRS = {0:(0,1),1:(1,0),2:(0,-1),3:(-1,0)}

def run(initial_black, nsteps, ant=(0,0), heading=0, record=True):
    black = set(initial_black)
    vcount = {}      # cell -> numero visite gia' fatte
    last   = {}      # cell -> ultimo tempo di visita
    x,y = ant
    log = [] if record else None
    rcount_blocks = []  # per validazione W0
    pos_log = []
    for t in range(nsteps):
        c = (x,y)
        color = 1 if c in black else 0
        fresh = c not in vcount
        vc = vcount.get(c,0)
        if record:
            age = -1 if fresh else (t - last[c])
            log.append((t, color, fresh, vc, age))
        # svolta
        heading = (heading+1)%4 if color==0 else (heading-1)%4
        # flip
        if color==0: black.add(c)
        else: black.discard(c)
        vcount[c]=vc+1; last[c]=t
        dx,dy = DIRS[heading]; x+=dx; y+=dy
        if not record: pos_log.append((x,y,color))
    return log, vcount, (x,y,heading), pos_log

# ---------- VALIDAZIONE W0 su griglia vuota ----------
_,_,_,pos = run(set(), 12000, record=False)
# coda: ultimi 20 periodi
tail = pos[-2080:]
# net displacement su 104 passi nella coda
p0 = pos[-2080]; p1 = pos[-2080+104]
drift = (p1[0]-p0[0], p1[1]-p0[1])
# R (=letture bianche) per blocco 104 nella coda
whites = sum(1 for (_,_,col) in tail[:104] if col==0)
# periodicita': la sequenza di colori si ripete con periodo 104?
cols = [col for (_,_,col) in tail]
per104 = all(cols[i]==cols[i+104] for i in range(len(cols)-104))
print("=== VALIDAZIONE W0 (griglia vuota, coda di 12000 passi) ===")
print(f"  periodicita' 104 nella coda : {per104}")
print(f"  letture bianche (R) / 104   : {whites}   (atteso 58)")
print(f"  drift su 104 passi          : {drift}   (atteso (+/-2,+/-2))")
print()

# ---------- LEDGER su difetto (7,-7), transiente caotico ----------
NST = 106000
log, vcount, end, _ = run({(7,-7)}, NST, record=True)
print(f"=== LEDGER DI CONSUMO  —  difetto (7,-7), {NST} passi (pre-onset) ===")

# sanity alternanza: per ogni cella le letture devono alternare W,B,W,B...
# ricostruisco la sequenza di colori per cella dal log
seqs = {}
for (t,color,fresh,vc,age) in log:
    pass
# piu' efficiente: rifaccio una passata tracciando per-cella la lista colori
# (uso il fatto che vc indica l'indice di visita; verifico color vs parita')
# Per cella che parte BIANCA: visita dispari(1,3,..) legge bianco, pari legge nero.
# (7,-7) parte NERA: invertito. Conto le violazioni dell'alternanza attesa.
viol = 0
defect = (7,-7)
# devo sapere la cella di ogni log: non l'ho salvata. Rifaccio run salvando cella.
def run_cells(initial_black, nsteps, ant=(0,0), heading=0):
    black=set(initial_black); vcount={}; last={}; x,y=ant; out=[]
    for t in range(nsteps):
        c=(x,y); color=1 if c in black else 0; fresh=c not in vcount; vc=vcount.get(c,0)
        out.append((t,c,color,fresh,vc, -1 if fresh else t-last[c]))
        heading=(heading+1)%4 if color==0 else (heading-1)%4
        if color==0: black.add(c)
        else: black.discard(c)
        vcount[c]=vc+1; last[c]=t; dx,dy=DIRS[heading]; x+=dx;y+=dy
    return out,vcount
log2, vcount = run_cells({(7,-7)}, NST)

for (t,c,color,fresh,vc,age) in log2:
    starts_black = (c==defect)
    # parita' attesa del colore alla visita (vc+1)-esima
    # cella bianca all'origine: visita k -> bianco se k dispari
    k = vc+1
    exp_white = (k%2==1)
    if starts_black: exp_white = not exp_white
    got_white = (color==0)
    if got_white!=exp_white: viol+=1
print(f"  violazioni alternanza        : {viol} / {NST}   (atteso 0)")

# metriche
morsi = 0          # fresh & white
black_reads = 0
deep104 = 0; deep1040 = 0     # black revisit con age>soglia
morso_fed = 0; recycle_fed = 0
deep_morso_fed = 0; deep_recycle_fed = 0
ages = []
for (t,c,color,fresh,vc,age) in log2:
    if fresh and color==0: morsi+=1
    if color==1 and not fresh:
        black_reads+=1
        ages.append(age)
        if age>104: deep104+=1
        if age>1040: deep1040+=1
        # sorgente: vc==1 -> il nero viene dal morso una-tantum; vc>=3 -> riciclo interno
        if vc==1:
            morso_fed+=1
            if age>1040: deep_morso_fed+=1
        else:
            recycle_fed+=1
            if age>1040: deep_recycle_fed+=1

distinct = len(vcount)
maxv = max(vcount.values())
vc_hist = Counter(vcount.values())
ages.sort()
def pct(a,p): 
    return a[int(len(a)*p)] if a else 0
print(f"  celle distinte visitate      : {distinct}")
print(f"  passi/cella distinta         : {NST/distinct:.3f}")
print(f"  max visite su una cella      : {maxv}")
print(f"  celle visitate >=4 volte     : {sum(n for v,n in vc_hist.items() if v>=4)}  ({100*sum(n for v,n in vc_hist.items() if v>=4)/distinct:.2f}%)")
print(f"  celle visitate >=6 volte     : {sum(n for v,n in vc_hist.items() if v>=6)}")
print()
print(f"  morsi (fresh-white)          : {morsi}")
print(f"  black-reads totali           : {black_reads}")
print(f"  black-reads age>104 (deep)   : {deep104}   ({100*deep104/black_reads:.1f}% dei black-read)")
print(f"  black-reads age>1040 (deep+) : {deep1040}   ({100*deep1040/black_reads:.1f}%)")
print(f"  eta' rivisita-nera  mediana  : {pct(ages,0.5)}   p90={pct(ages,0.9)}   p99={pct(ages,0.99)}   max={ages[-1] if ages else 0}")
print()
print("  --- SORGENTE DEL NERO CONSUMATO (il cuore del lemma di consumo) ---")
print(f"  black-read morso-fed (vc=1)  : {morso_fed}   ({100*morso_fed/black_reads:.1f}%)")
print(f"  black-read recycle-fed(vc>=3): {recycle_fed}   ({100*recycle_fed/black_reads:.1f}%)")
if deep1040:
    print(f"  tra i DEEP (age>1040): morso-fed {deep_morso_fed} ({100*deep_morso_fed/deep1040:.1f}%) | recycle-fed {deep_recycle_fed} ({100*deep_recycle_fed/deep1040:.1f}%)")

# curva cumulativa inflow vs consumo nel tempo (per figura)
import numpy as np
NB = 200
edges = np.linspace(0, NST, NB+1)
cum_morsi = np.zeros(NB); cum_deep = np.zeros(NB)
mi=0; di=0
# ricostruisco cumulativi binnati
ev_morsi = []; ev_deep = []
for (t,c,color,fresh,vc,age) in log2:
    if fresh and color==0: ev_morsi.append(t)
    if color==1 and not fresh and age>104: ev_deep.append(t)
ev_morsi=np.array(ev_morsi); ev_deep=np.array(ev_deep)
cm = np.searchsorted(ev_morsi, edges[1:])
cd = np.searchsorted(ev_deep, edges[1:])
np.save('/home/claude/cm.npy', cm); np.save('/home/claude/cd.npy', cd); np.save('/home/claude/edges.npy', edges)
print()
print("  ratio (deep consumo cumulativo)/(morsi cumulativi) a fine transiente:")
print(f"    deep104_cum/morsi = {len(ev_deep)/morsi:.3f}")
