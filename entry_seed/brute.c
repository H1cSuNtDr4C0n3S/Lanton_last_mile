/* entry_seed/brute.c  (sessione §76)
   Ricerca forward a forza bruta dei semi minimi che entrano in autostrada.
   Semi: b celle nere nel box [-R,R]^2, formica a (0,0,0). Per ogni seme: onset (ingresso),
   classe (match esatto a W0/Wbar), distanza Manhattan |lock-start|. Reset SOLO celle toccate
   (evita la trappola di banda di memoria, CLAUDE.md §1-g e §4).
   Trappola §76: l'onset va rilevato sui turni raccolti ANCHE se poi la formica esce dal box
   (la highway drifta all'infinito e la spinge fuori): bocciare al bordo scarta un ingresso valido.
   Build: gcc -O3 -o entry_seed/brute entry_seed/brute.c
   Uso:   ./entry_seed/brute R b MAXSTEPS minp [path_w0]    (da root repo; default data/w0.txt)
   Riferimenti: vuota->9977, (7,-7)->106258 (motore C). */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

/* Brute force: semi con b celle nere in box [-R,R]^2, formica a (0,0,0).
   Trova onset (ingresso autostrada) e distanza lock-start. Reset solo celle toccate. */

#define H 700
#define W (2*H)
#define P 104
static uint8_t grid[(size_t)W*W];
static int dxh[4] = {0,1,0,-1};
static int dyh[4] = {0,-1+1,0,0}; /* placeholder, set in main */

static int DX[4] = {0,1,0,-1};
static int DY[4] = {-1,0,1,0};

static uint8_t W0[P];

static long *touched;
static uint8_t *turns;
static long MAXSTEPS;

/* cyclic hamming of word (len P) vs W0 (and vs 1-W0). returns 0 if exact match to either. */
static int classify(const uint8_t* word, int* is_wbar){
    int best0=P+1, best1=P+1;
    for(int s=0;s<P;s++){
        int d0=0,d1=0;
        for(int i=0;i<P;i++){
            int wi=word[(i+s)%P];
            if(wi!=W0[i]) d0++;
            if(wi!=(1-W0[i])) d1++;
        }
        if(d0<best0)best0=d0;
        if(d1<best1)best1=d1;
    }
    *is_wbar = (best1<best0);
    return best0<best1?best0:best1;
}

/* run one seed. returns onset>=0 if highway entry (exact W/Wbar) with >=minp tail, else -1.
   sets *lockdist (manhattan |lock-start|) and *iswbar when onset>=0. */
static long run_seed(const int* px, const int* py, int b, int minp, long* lockdist, int* iswbar){
    long nt=0;
    for(int i=0;i<b;i++){
        long x=px[i]+H, y=py[i]+H;
        long idx=y*W+x;
        if(!grid[idx]){ grid[idx]=1; touched[nt++]=idx; }
    }
    long x=0+H, y=0+H; int h=0;
    long n=MAXSTEPS; int hitb=0;
    for(long t=0;t<MAXSTEPS;t++){
        long idx=y*W+x;
        uint8_t c=grid[idx];
        if(c==0){ h=(h+1)&3; grid[idx]=1; turns[t]=1; touched[nt++]=idx; }
        else    { h=(h+3)&3; grid[idx]=0; turns[t]=0; }
        x+=DX[h]; y+=DY[h];
        if(x<1||x>=W-1||y<1||y>=W-1){ n=t+1; hitb=1; break; }
    }
    long onset=-1;
    {   /* rileva onset sui turni raccolti (anche se poi tocca il bordo) */
        long ons=0;
        for(long t=0;t+P<n;t++) if(turns[t]!=turns[t+P]) ons=t+1;
        if(n-ons >= (long)minp*P){
            /* drift check + word class */
            uint8_t word[P];
            for(int i=0;i<P;i++) word[i]=turns[ons+i];
            int hh=0; long ddx=0,ddy=0,rot=0;
            for(int i=0;i<P;i++){ if(word[i]==1){hh=(hh+1)&3;rot++;} else {hh=(hh+3)&3;rot--;} ddx+=DX[hh]; ddy+=DY[hh]; }
            if(rot%4==0 && !(ddx==0&&ddy==0)){
                int wbar; int d=classify(word,&wbar);
                if(d==0){
                    onset=ons; *iswbar=wbar;
                    /* lock position: replay turns[0..ons) */
                    int h2=0; long x2=0,y2=0;
                    for(long t=0;t<ons;t++){ if(turns[t]==1)h2=(h2+1)&3; else h2=(h2+3)&3; x2+=DX[h2]; y2+=DY[h2]; }
                    *lockdist = labs(x2)+labs(y2);
                }
            }
        }
    }
    for(long i=0;i<nt;i++) grid[touched[i]]=0;
    return onset;
}

/* combination generator over npos positions, choose b. */
static int POSX[4096], POSY[4096], NPOS;
static int combo[16];

static long best_onset, best_onset_dist; static int best_onset_seed[16], best_onset_b;
static long best_dist, best_dist_onset; static int best_dist_seed[16], best_dist_b;
static long n_entered, n_total;

static void test_combo(int b, int minp){
    int px[16],py[16];
    for(int i=0;i<b;i++){ px[i]=POSX[combo[i]]; py[i]=POSY[combo[i]]; }
    long ld; int wbar;
    long ons=run_seed(px,py,b,minp,&ld,&wbar);
    n_total++;
    if(ons>=0){
        n_entered++;
        if(ons<best_onset || (ons==best_onset && ld<best_onset_dist)){
            best_onset=ons; best_onset_dist=ld; best_onset_b=b;
            for(int i=0;i<b;i++){best_onset_seed[i*2]=px[i];best_onset_seed[i*2+1]=py[i];}
        }
        if(ld<best_dist || (ld==best_dist && ons<best_dist_onset)){
            best_dist=ld; best_dist_onset=ons; best_dist_b=b;
            for(int i=0;i<b;i++){best_dist_seed[i*2]=px[i];best_dist_seed[i*2+1]=py[i];}
        }
    }
}

static void rec(int start, int depth, int b, int minp){
    if(depth==b){ test_combo(b,minp); return; }
    for(int i=start;i<=NPOS-(b-depth);i++){ combo[depth]=i; rec(i+1,depth+1,b,minp); }
}

int main(int argc, char** argv){
    /* args: R b MAXSTEPS minp */
    int R=atoi(argv[1]); int b=atoi(argv[2]); MAXSTEPS=atol(argv[3]); int minp=atoi(argv[4]);
    /* load W0 */
    const char* w0path = (argc>5)?argv[5]:"data/w0.txt";
    FILE* f=fopen(w0path,"r");
    if(!f){fprintf(stderr,"non trovo %s (lancia da root repo)\n",w0path);return 1;}
    char buf[256]; fgets(buf,256,f); fclose(f);
    for(int i=0;i<P;i++) W0[i] = (buf[i]=='R')?1:0;
    touched=malloc(sizeof(long)*(MAXSTEPS+64));
    turns=malloc(MAXSTEPS+8);
    memset(grid,0,(size_t)W*W);
    NPOS=0;
    for(int yy=-R;yy<=R;yy++) for(int xx=-R;xx<=R;xx++){ POSX[NPOS]=xx; POSY[NPOS]=yy; NPOS++; }
    best_onset=1L<<60; best_dist=1L<<60;
    rec(0,0,b,minp);
    printf("R=%d b=%d MAXSTEPS=%ld : seeds=%ld entered=%ld (%.2f%%)\n",
           R,b,MAXSTEPS,n_total,n_entered, n_total?100.0*n_entered/n_total:0.0);
    if(best_onset<(1L<<60)){
        printf("  FASTEST ENTRY: onset=%ld lockdist=%ld  seed=", best_onset, best_onset_dist);
        for(int i=0;i<best_onset_b;i++) printf("(%d,%d)", best_onset_seed[i*2],best_onset_seed[i*2+1]);
        printf("\n");
    }
    if(best_dist<(1L<<60)){
        printf("  NEAREST LOCK: lockdist=%ld onset=%ld  seed=", best_dist, best_dist_onset);
        for(int i=0;i<best_dist_b;i++) printf("(%d,%d)", best_dist_seed[i*2],best_dist_seed[i*2+1]);
        printf("\n");
    }
    return 0;
}
