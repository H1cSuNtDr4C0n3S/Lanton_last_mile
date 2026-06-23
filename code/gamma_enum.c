// gamma_enum.c — Enumerazione esaustiva delle code periodiche eterne ammissibili (fronte gamma)
// Michael Spina + Claude, 11 giugno 2026.
//
// Oggetto: parole w di periodo p tali che w^inf possa essere il suffisso eterno del
// linguaggio di svolte di un'orbita da configurazione finita.
// Condizioni (necessarie, tutte finite):
//   (1) rot(w) == 0 mod 4 e drift != 0      [altrimenti cammino limitato => B-T]
//   (2) alternanza delle svolte su ogni cella, per sempre   [cond. (i) di L_inf]
//   (3) zero prime-visite L nel regime stazionario          [cond. (ii): finitezza]
// Finestra di verifica: M = 2p+10 periodi; testa libera J0 = p+4 periodi
// (stabilizzazione del pattern di freschezza entro diam/|d|+2 <= p+2; ogni classe
// di vincolo con lookback <= p+1 ha un rappresentante interamente stazionario
// entro 2p+3 <= M; eternita' per induzione di shift, stile T1).
//
// Convenzioni HANDOVER.md par.2: bianco->R(+1), nero->L(-1); h 0=su,1=dx,2=giu,3=sx;
// turns 1=R, 0=L. Mossa DOPO la svolta.
//
// Modi:
//   ./gamma_enum sweep PMIN PMAX     enumerazione esaustiva, p pari in [PMIN,PMAX]
//   ./gamma_enum check FILE          verifica una singola parola (stringa di R/L)
//
// gcc -O3 -march=native -o gamma_enum gamma_enum.c

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXP 48
#define DS (2*MAXP+8)          // griglia DFS, coord in [-MAXP-4, MAXP+4)
#define BS 5504                // griglia full-check (raggio max ~ (2p+10)*p/2 + p < 2700)
#define MAXW 256               // buffer parola (check mode: W0 ha p=104)

static const int DX[4]={0,1,0,-1}, DY[4]={1,0,-1,0};

static int P;                          // periodo corrente
static uint8_t w[MAXW];
static int8_t  lastt[DS*DS];           // ultima svolta per cella (DFS): -1 mai, 0 L, 1 R
static int32_t *stampA;                // full-check: stamp per cella
static int8_t  *blastA;                // full-check: ultima svolta per cella
static int32_t curstamp = 0;

static long long n_leaves, n_rot0, n_driftnz, n_fail_alt, n_fail_fresh, n_pass;
static int force_k = 0, force_idx = 0;   // modo chunk: prime force_k scelte libere forzate

// full_check: simula w^inf per M periodi.
// ritorna 1 = ammissibile (candidato coda eterna), 0 = rigettata.
// fail_code (se non NULL): 1 = alternanza, 2 = fresca-L stazionaria.
static int full_check(int p, int *fail_code, int verbose){
    int M  = 2*p + 10;
    int J0 = p + 4;
    curstamp++;
    if(curstamp == 0){ memset(stampA, 0, (size_t)BS*BS*sizeof(int32_t)); curstamp = 1; }
    int x = BS/2, y = BS/2, h = 0;
    for(int j = 1; j <= M; j++){
        for(int i = 0; i < p; i++){
            if(x < 2 || x >= BS-2 || y < 2 || y >= BS-2){
                fprintf(stderr, "FATAL: overflow griglia full_check (p=%d)\n", p);
                exit(1);
            }
            int idx = x*BS + y;
            int b = w[i];
            if(stampA[idx] == curstamp){
                if(blastA[idx] == (int8_t)b){       // alternanza violata
                    if(fail_code) *fail_code = 1;
                    if(verbose) printf("  FAIL alternanza: periodo %d, offset %d\n", j, i);
                    n_fail_alt++;
                    return 0;
                }
                blastA[idx] = (int8_t)b;
            } else {                                 // prima visita
                stampA[idx] = curstamp;
                blastA[idx] = (int8_t)b;
                if(j > J0 && b == 0){                // fresca-L in regime stazionario
                    if(fail_code) *fail_code = 2;
                    if(verbose) printf("  FAIL fresca-L stazionaria: periodo %d, offset %d\n", j, i);
                    n_fail_fresh++;
                    return 0;
                }
            }
            h = b ? ((h+1)&3) : ((h+3)&3);
            x += DX[h]; y += DY[h];
        }
    }
    n_pass++;
    return 1;
}

static void dfs(int depth, int x, int y, int h, int rot, int nfree){
    if(depth == P){
        n_leaves++;
        if((rot & 3) != 0) return;       // rot != 0 mod 4 => limitato => B-T
        n_rot0++;
        if(x == 0 && y == 0) return;     // drift nullo => limitato => B-T
        n_driftnz++;
        if(full_check(P, NULL, 0)){
            printf("SURVIVOR p=%d w=", P);
            for(int i = 0; i < P; i++) putchar(w[i] ? 'R' : 'L');
            putchar('\n');
            fflush(stdout);
        }
        return;
    }
    int idx = (x + MAXP + 4)*DS + (y + MAXP + 4);
    int8_t lt = lastt[idx];
    if(lt == -1){                        // cella fresca
        int blo = 0, bhi = 1;
        if(nfree < force_k){             // scelta forzata dal chunk (MSB first)
            int b = (force_idx >> (force_k - 1 - nfree)) & 1;
            blo = bhi = b;
        }
        for(int b = bhi; b >= blo; b--){
            w[depth] = (uint8_t)b;
            lastt[idx] = (int8_t)b;
            int nh = b ? ((h+1)&3) : ((h+3)&3);
            dfs(depth+1, x + DX[nh], y + DY[nh], nh, rot + (b ? 1 : -1), nfree+1);
        }
        lastt[idx] = -1;
    } else {                             // rivisita: svolta forzata
        int b = 1 - lt;
        w[depth] = (uint8_t)b;
        lastt[idx] = (int8_t)b;
        int nh = b ? ((h+1)&3) : ((h+3)&3);
        dfs(depth+1, x + DX[nh], y + DY[nh], nh, rot + (b ? 1 : -1), nfree+1);
        lastt[idx] = lt;
    }
}

int main(int argc, char **argv){
    stampA = calloc((size_t)BS*BS, sizeof(int32_t));
    blastA = malloc((size_t)BS*BS);
    if(!stampA || !blastA){ fprintf(stderr, "alloc fail\n"); return 1; }

    if(argc >= 2 && strcmp(argv[1], "check") == 0){
        FILE *f = fopen(argv[2], "r");
        if(!f){ perror("open"); return 1; }
        int p = 0; int ch;
        while((ch = fgetc(f)) != EOF && p < MAXW){
            if(ch == 'R') w[p++] = 1;
            else if(ch == 'L') w[p++] = 0;
        }
        fclose(f);
        // rot e drift su un periodo
        int x = 0, y = 0, h = 0, rot = 0;
        for(int i = 0; i < p; i++){
            int b = w[i];
            rot += b ? 1 : -1;
            h = b ? ((h+1)&3) : ((h+3)&3);
            x += DX[h]; y += DY[h];
        }
        printf("p=%d  rot=%d (mod4=%d)  drift=(%d,%d)\n", p, rot, ((rot%4)+4)%4, x, y);
        if((rot & 3) != 0){ printf("REJECT: rot != 0 mod 4 (cammino limitato, B-T)\n"); return 0; }
        if(x == 0 && y == 0){ printf("REJECT: drift nullo (cammino limitato, B-T)\n"); return 0; }
        int fc = 0;
        if(full_check(p, &fc, 1)) printf("PASS: coda eterna ammissibile\n");
        else                      printf("REJECT (fail_code=%d: 1=alternanza, 2=fresca-L)\n", fc);
        return 0;
    }

    int pmin = 2, pmax = 24;
    if(argc >= 5 && strcmp(argv[1], "part") == 0){
        P = atoi(argv[2]); force_k = atoi(argv[3]); force_idx = atoi(argv[4]);
        n_leaves = n_rot0 = n_driftnz = n_fail_alt = n_fail_fresh = n_pass = 0;
        memset(lastt, -1, sizeof(lastt));
        clock_t t0 = clock();
        dfs(0, 0, 0, 0, 0, 0);
        double secs = (double)(clock() - t0)/CLOCKS_PER_SEC;
        printf("%d %lld %lld %lld %lld %lld %lld %.2f\n",
               P, n_leaves, n_rot0, n_driftnz, n_fail_alt, n_fail_fresh, n_pass, secs);
        return 0;
    }
    if(argc >= 4 && strcmp(argv[1], "sweep") == 0){ pmin = atoi(argv[2]); pmax = atoi(argv[3]); }
    printf("# p leaves rot0 driftnz fail_alt fail_fresh pass secs\n");
    fflush(stdout);
    for(P = pmin; P <= pmax; P += 2){
        if(P & 1) continue;
        n_leaves = n_rot0 = n_driftnz = n_fail_alt = n_fail_fresh = n_pass = 0;
        memset(lastt, -1, sizeof(lastt));
        clock_t t0 = clock();
        dfs(0, 0, 0, 0, 0, 0);
        double secs = (double)(clock() - t0)/CLOCKS_PER_SEC;
        printf("%d %lld %lld %lld %lld %lld %lld %.2f\n",
               P, n_leaves, n_rot0, n_driftnz, n_fail_alt, n_fail_fresh, n_pass, secs);
        fflush(stdout);
    }
    return 0;
}
