# deep_motif_saturation.py — positive gate (§79.6): l'alfabeto dei motivi locali
# co-moving agli eventi deep-black (detrito delta4) satura o cresce col territorio?
# Riusa dinamica + definizione deep-black di delta4_long_orbits.py. Parallelo sulle 24 orbite.
import sys,os,json,time,hashlib,statistics as st
from multiprocessing import Pool
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from delta4_long_orbits import parse_dumps,build_seed,forget_outside_ring,ALPHA
DX=(0,1,0,-1);DY=(-1,0,1,0);RS=(3,4,5)
def rotk(c,k):
    for _ in range(k%4): c=[(-y,x) for (x,y) in c]
    return c
def patches(black,ax,ay,h):
    k=(-h)%4
    rel=[(cx-ax,cy-ay) for cx in range(ax-5,ax+6) for cy in range(ay-5,ay+6)
         if (cx,cy) in black and not(cx==ax and cy==ay)]
    rel=rotk(rel,k); out={}
    for r in RS:
        rr=sorted([(dx,dy) for (dx,dy) in rel if max(abs(dx),abs(dy))<=r])
        out[r]=hashlib.blake2b(repr(rr).encode(),digest_size=8).digest()
    return out
def analyze(arg):
    rng,onset=arg
    black,side,dens=build_seed(rng,5,25)
    known=set(); last={}; x=y=h=0
    seen={r:set() for r in RS}; df={r:0 for r in RS}; dl={r:0 for r in RS}
    fc=int(onset*0.2); lc=int(onset*0.8); nev=0; ages=[]
    sat={r:[] for r in RS}; chk=[int(onset*(i+1)/10) for i in range(10)]; ci=0
    for t in range(onset):
        c=(x,y); isb=c in black
        if isb and c not in known:
            prev=last.get(c)
            if prev is not None:
                nev+=1; ages.append(t-prev); ks=patches(black,x,y,h)
                for r in RS:
                    s=seen[r]; b=len(s); s.add(ks[r]); nw=len(s)-b
                    if t<fc: df[r]+=nw
                    elif t>=lc: dl[r]+=nw
        if isb: black.discard(c); h=(h+3)&3
        else: black.add(c); h=(h+1)&3
        last[c]=t; known.add(c); x+=DX[h]; y+=DY[h]; forget_outside_ring(known,x,y)
        while ci<10 and t+1>=chk[ci]:
            for r in RS: sat[r].append(len(seen[r]))
            ci+=1
    while ci<10:
        for r in RS: sat[r].append(len(seen[r]))
        ci+=1
    ages.sort()
    return {"rng":rng,"onset":onset,"side":side,"nev":nev,
            "distinct":{r:len(seen[r]) for r in RS},"df":df,"dl":dl,
            "fc":fc,"lc":onset-lc,"sat":sat,"set3":list(seen[3]),
            "med":ages[len(ages)//2] if ages else 0,
            "p90":ages[int(len(ages)*0.9)] if ages else 0,"mx":ages[-1] if ages else 0}
if __name__=="__main__":
    t0=time.time(); dumps=parse_dumps(ALPHA/"dumps_all.txt")
    args=[(d.rngstate,d.onset_dump) for d in dumps]
    with Pool(min(16,len(args))) as pool: res=pool.map(analyze,args)
    sets=[set(r["set3"]) for r in res]; union=set().union(*sets)
    inter=set(sets[0]).intersection(*sets[1:]) if len(sets)>1 else sets[0]
    sumind=sum(len(s) for s in sets)
    print(f"orbite {len(res)}, elapsed {time.time()-t0:.1f}s")
    print(f"{'idx':>3} {'onset':>7} {'nev':>6} {'d_r3':>6} {'d_r4':>7} {'d_r5':>7} {'new/ev_first':>12} {'new/ev_last':>11} {'agemed':>6} {'agemax':>6}")
    for i,r in enumerate(res):
        rf=r['df'][3]/max(r['fc'],1); rl=r['dl'][3]/max(r['lc'],1)
        print(f"{i:>3} {r['onset']:>7} {r['nev']:>6} {r['distinct'][3]:>6} {r['distinct'][4]:>7} {r['distinct'][5]:>7} {rf:>12.5f} {rl:>11.5f} {r['med']:>6} {r['mx']:>6}")
    print(f"\nr=3 POOLED: somma-per-orbita {sumind}, UNIONE {len(union)}, INTERSEZIONE {len(inter)}")
    print(f"  union/sum = {len(union)/max(sumind,1):.3f}  (~1 => alfabeti disgiunti/illimitati; <<1 => universale condiviso)")
    decay=[(r['dl'][3]/max(r['lc'],1))/max(r['df'][3]/max(r['fc'],1),1e-12) for r in res]
    print(f"  scoperta nuovi motivi r=3 ultimo20%/primo20% (mediana orbite): {st.median(decay):.3f}")
    print(f"  (->0 => alfabeto SATURA/finito; ~1+ => cresce col territorio = illimitato)")
    json.dump({"res":[{k:v for k,v in r.items() if k!='set3'} for r in res]},
              open(ALPHA/"deep_motif_saturation_summary.json","w"),indent=1)
    print("scritto deep_motif_saturation_summary.json")
