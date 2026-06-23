/* alpha1_engine.c — Langton bite-stall engine (alpha1 last-mile probe).
   Convention identical to C:\Lanton_last_mile\code\libant.c (empty grid -> onset 9977).
   heading 0=up(-y),1=right(+x),2=down(+y),3=left(-x); white(0)->R, black(1)->L.
   morso = fresh-WHITE read (matches morso_census.py).
   search has EARLY-STOP at onset (cost ~ typical onset, not the cap).
   Modes:
     search <shardId> <nShards> <nSeeds> <maxSteps> <minSize> <maxSize>
         -> "onset size dens rngstate" for seeds that converge.
     reseed <maxSteps> <rngstate> <minSize> <maxSize>   (reproduce a search seed, full dump)
     dump   <maxSteps>   (explicit seed cells "x y" on stdin, full dump)
   Build: gcc -O3 -o alpha1_engine.exe alpha1_engine.c
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define HBITS 24
#define HSIZE (1u<<HBITS)
#define HMASK (HSIZE-1u)
static uint64_t *hkey; static uint8_t *hval, *hused;   /* bit0 color, bit1 visited */
static const int DX[4]={0,1,0,-1};
static const int DY[4]={-1,0,1,0};
static int8_t *turns; static uint8_t *fw;

static inline uint64_t mkkey(int32_t x,int32_t y){
    return (((uint64_t)(uint32_t)(x+(1<<30)))<<32)|(uint32_t)(y+(1<<30)); }
static inline uint8_t* slot(int32_t x,int32_t y){
    uint64_t key=mkkey(x,y); uint32_t h=(uint32_t)(key*2654435761u)&HMASK;
    while(hused[h]){ if(hkey[h]==key) return &hval[h]; h=(h+1)&HMASK; }
    hused[h]=1; hkey[h]=key; hval[h]=0; return &hval[h]; }
static inline uint64_t xs(uint64_t*s){ uint64_t x=*s; x^=x<<13; x^=x>>7; x^=x<<17; return *s=x; }

/* onset = minimal t with turns[t:n) exactly 104-periodic; verify rot%4==0 & nonzero drift */
static long onset_verified(long n){
    long P=104;
    if(n<2600) return -1;
    long LWIN=2080;                          /* require >=20 periods of tail */
    for(long i=n-LWIN;i<n-P;i++) if(turns[i]!=turns[i+P]) return -1;
    long onset=n-LWIN;
    while(onset>0 && turns[onset-1]==turns[onset-1+P]) onset--;
    if(n-onset<520) return -1;
    int h=0; int32_t x=0,y=0,rot=0;
    for(long s=onset;s<onset+P;s++){ if(turns[s]){h=(h+1)&3;rot++;} else {h=(h+3)&3;rot--;} x+=DX[h]; y+=DY[h]; }
    if(rot%4!=0) return -1;
    if(x==0&&y==0) return -1;
    return onset;
}

/* simulate; if stop_at_onset, check every CHK steps and return onset early. */
static long simulate(long MAX,int stop_at_onset,long*onset_out){
    int32_t x=0,y=0; int h=0; long n=0; const long CHK=20000;
    for(long t=0;t<MAX;t++){
        uint8_t*s=slot(x,y); uint8_t color=*s&1, vis=(*s>>1)&1;
        if(fw) fw[t]=(!vis&&color==0)?1:0;
        *s|=2;
        if(color==0){ h=(h+1)&3; *s=(*s&~1)|1; turns[t]=1; }
        else        { h=(h+3)&3; *s=(*s&~1)|0; turns[t]=0; }
        x+=DX[h]; y+=DY[h]; n=t+1;
        if(stop_at_onset && t>=2600 && (t%CHK)==0){
            long o=onset_verified(n); if(o>=0){ if(onset_out)*onset_out=o; return n; }
        }
    }
    if(onset_out)*onset_out=onset_verified(n);
    return n;
}

static void build_seed(uint64_t*st,int smin,int smax,int*side_out,double*dens_out){
    int side=smin+(int)(xs(st)%(smax-smin+1));
    double dens=0.25+(xs(st)%1000)/1000.0*0.35;
    int half=side/2;
    for(int a=-half;a<=half;a++)for(int b=-half;b<=half;b++)
        if((xs(st)%1000)/1000.0<dens) *slot(a,b)|=1;
    *side_out=side; *dens_out=dens;
}

int main(int argc,char**argv){
    hkey=malloc((size_t)HSIZE*8); hval=malloc(HSIZE); hused=malloc(HSIZE);
    if(!hkey||!hval||!hused){fprintf(stderr,"alloc fail\n");return 2;}

    if(argc>=8 && !strcmp(argv[1],"search")){
        int shard=atoi(argv[2]), nsh=atoi(argv[3]); long nseed=atol(argv[4]);
        long MAX=atol(argv[5]); int smin=atoi(argv[6]), smax=atoi(argv[7]);
        turns=malloc(MAX); fw=NULL;
        uint64_t st=0x9e3779b97f4a7c15ULL ^ ((uint64_t)(shard+1)*0xD1B54A32D192ED03ULL);
        long found=0;
        for(long k=0;k<nseed;k++){
            uint64_t seedstate=st; int side; double dens;
            memset(hused,0,HSIZE);
            build_seed(&st,smin,smax,&side,&dens);
            long o; simulate(MAX,1,&o);
            if(o>0){ printf("%ld %d %.3f %llu\n",o,side,dens,(unsigned long long)seedstate); found++; }
            if((k%2000)==0){ fflush(stdout);
                fprintf(stderr,"[shard %d] %ld/%ld seeds, %ld converged\n",shard,k,nseed,found); }
        }
        fprintf(stderr,"[shard %d] DONE %ld seeds, %ld converged\n",shard,nseed,found);
        return 0;
    }
    if(argc>=6 && !strcmp(argv[1],"reseed")){
        long MAX=atol(argv[2]); uint64_t st=strtoull(argv[3],0,10);
        int smin=atoi(argv[4]), smax=atoi(argv[5]);
        turns=malloc(MAX); fw=malloc(MAX); memset(hused,0,HSIZE);
        int side; double dens; build_seed(&st,smin,smax,&side,&dens);
        long o; long n=simulate(MAX,0,&o); if(o<0)o=n;
        long nb=0; for(long t=0;t<o;t++) if(fw[t])nb++;
        printf("%ld %ld\n",o,nb); for(long t=0;t<o;t++) if(fw[t]) printf("%ld\n",t);
        return 0;
    }
    if(argc>=3 && !strcmp(argv[1],"dump")){
        long MAX=atol(argv[2]); turns=malloc(MAX); fw=malloc(MAX); memset(hused,0,HSIZE);
        char line[128]; int x,y;
        while(fgets(line,sizeof line,stdin)) if(sscanf(line,"%d %d",&x,&y)==2) *slot(x,y)|=1;
        long o; long n=simulate(MAX,0,&o); if(o<0)o=n;
        long nb=0; for(long t=0;t<o;t++) if(fw[t])nb++;
        printf("%ld %ld\n",o,nb); for(long t=0;t<o;t++) if(fw[t]) printf("%ld\n",t);
        return 0;
    }
    fprintf(stderr,"usage: search|reseed|dump ...\n"); return 1;
}
