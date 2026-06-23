// product_build.c — port C del BFS di product_automaton.py (semantica IDENTICA).
// Automa-prodotto A(r; m, D): finestra (2r+1)^2 con celle {0=U,1=W,2=B,3=B*} + memoria M
// di al piu' m celle uscite dalla finestra, box ||.||inf <= D, eviction "nearest"
// (chiave (dist, x, y)), ordine canonico di M per (x, y). Vedi product_automaton.py per
// la semantica e la soundness; questo file DEVE riprodurre byte-per-byte i binari del
// prototipo Python su istanze piccole (validazione obbligatoria prima di r>=3).
//
// Uso: product_build <radius> <m> <D> <outdir> [cap_stati] [modo]
//   modo: 0=full (default), 1=black-only (ricorda solo nere), 2=ibrida (nere prioritarie)
// Output (prefisso p{r}m{m}d{D} + suffisso '' / 'b' / 'h'):
//   <outdir>/<pfx>_edges.bin  — 6 B/arco: u32 dst, u8 ty (0=forzato,1=assumiW,2=paga), u8 tn (1=R)
//   <outdir>/<pfx>_tyx.bin    — 1 B/arco: tipo esteso (0,1,2 come ty; 3=B* forzata pagante)
//   <outdir>/<pfx>_outdeg.bin — 1 B/stato (1 o 2) in ordine BFS
//   <outdir>/<pfx>_stats.txt  — conteggi per il cross-check
// Compilare: gcc -O3 -o product_build product_build.c

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#define UC 0
#define WC 1
#define BC 2
#define BS 3

static int R, MM, DD, NC, S, KB, KEYB, C0, MODE;
static int *mapR_, *mapL_;
static int *fwdRx, *fwdRy, *fwdLx, *fwdLy;   // nuova posizione della cella vecchia j

static uint8_t *pool;
static uint64_t pool_cap, nstates;
static uint32_t *table;
static uint64_t tcap, tmask, tcount;

static void die(const char *m) { fprintf(stderr, "ERRORE: %s\n", m); exit(2); }

static uint64_t fnv1a(const uint8_t *k) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < KEYB; i++) { h ^= k[i]; h *= 1099511628211ULL; }
    return h;
}

static void table_grow(void) {
    uint64_t nc = tcap << 1, nm = nc - 1;
    uint32_t *nt = (uint32_t*)malloc(nc * 4);
    if (!nt) die("OOM tabella");
    memset(nt, 0xFF, nc * 4);
    for (uint64_t i = 0; i < tcap; i++) {
        uint32_t v = table[i];
        if (v == 0xFFFFFFFFu) continue;
        uint64_t h = fnv1a(pool + (uint64_t)v * KEYB) & nm;
        while (nt[h] != 0xFFFFFFFFu) h = (h + 1) & nm;
        nt[h] = v;
    }
    free(table); table = nt; tcap = nc; tmask = nm;
}

static uint32_t intern(const uint8_t *key, int *isnew) {
    if (tcount * 10 >= tcap * 7) table_grow();
    uint64_t h = fnv1a(key) & tmask;
    while (table[h] != 0xFFFFFFFFu) {
        uint32_t v = table[h];
        if (memcmp(pool + (uint64_t)v * KEYB, key, KEYB) == 0) { *isnew = 0; return v; }
        h = (h + 1) & tmask;
    }
    if (nstates >= 0xFFFFFFFEull) die("overflow u32 sugli stati");
    if (nstates >= pool_cap) {
        pool_cap <<= 1;
        uint8_t *np_ = (uint8_t*)realloc(pool, pool_cap * (uint64_t)KEYB);
        if (!np_) die("OOM pool");
        pool = np_;
    }
    memcpy(pool + nstates * (uint64_t)KEYB, key, KEYB);
    uint32_t idx = (uint32_t)nstates++;
    table[h] = idx; tcount++;
    *isnew = 1;
    return idx;
}

static inline int get_cell(const uint8_t *p, int i) { return (p[i >> 2] >> ((i & 3) << 1)) & 3; }
static inline void set_cell(uint8_t *p, int i, int v) {
    int b = i >> 2, s = (i & 3) << 1;
    p[b] = (uint8_t)((p[b] & ~(3 << s)) | (v << s));
}

typedef struct { int x, y, black; } MemCell;

// un passo del prodotto: stato (win,M) decompresso, colore letto col (WC/BC).
// scrive il nuovo stato impacchettato in key. Ritorna 0, o muore su incoerenze.
static void step_product(const uint8_t *win, const MemCell *M, int nM, int col, uint8_t *key) {
    static uint8_t tmp[1024], nw[1024];
    static MemCell cand[4096];
    int ncand = 0;
    memcpy(tmp, win, NC);
    tmp[C0] = (col == WC) ? BC : WC;             // flip del centro (B* perde la stella)
    int right = (col == WC);
    const int *mp = right ? mapR_ : mapL_;
    const int *fx = right ? fwdRx : fwdLx;
    const int *fy = right ? fwdRy : fwdLy;
    for (int i = 0; i < NC; i++) { int j = mp[i]; nw[i] = (j >= 0) ? tmp[j] : UC; }
    // celle note che escono dalla finestra (black-only: le bianche si dimenticano subito)
    for (int j = 0; j < NC; j++) {
        if (tmp[j] == UC || (MODE == 1 && tmp[j] == WC)) continue;
        int nx = fx[j], ny = fy[j];
        if (nx < -R || nx > R || ny < -R || ny > R) {
            cand[ncand].x = nx; cand[ncand].y = ny;
            cand[ncand].black = (tmp[j] != WC); ncand++;
        }
    }
    // memoria esistente: trasforma; chi rientra viene ripristinato
    for (int k = 0; k < nM; k++) {
        int ox = M[k].x, oy = M[k].y, nx, ny;
        if (right) { nx = -oy; ny = ox - 1; } else { nx = oy; ny = -ox - 1; }
        if (nx >= -R && nx <= R && ny >= -R && ny <= R) {
            int i = (nx + R) * S + (ny + R);
            if (nw[i] != UC) die("rientro su cella gia' nota");
            nw[i] = M[k].black ? BS : WC;
        } else {
            cand[ncand].x = nx; cand[ncand].y = ny; cand[ncand].black = M[k].black; ncand++;
        }
    }
    // box D
    int nk = 0;
    for (int k = 0; k < ncand; k++)
        if (cand[k].x >= -DD && cand[k].x <= DD && cand[k].y >= -DD && cand[k].y <= DD)
            cand[nk++] = cand[k];
    ncand = nk;
    // eviction: ordina per chiave di politica e tieni i primi m (insertion sort: ncand piccolo)
    // chiave full/black-only: (dist, x, y); ibrida (MODE 2): (1-black, dist, x, y)
    if (ncand > MM) {
        for (int a = 1; a < ncand; a++) {
            MemCell t = cand[a];
            int da = t.x < 0 ? -t.x : t.x, db = t.y < 0 ? -t.y : t.y;
            int dt = da > db ? da : db;
            int pt = (MODE == 2) ? 1 - t.black : 0;
            int b = a - 1;
            while (b >= 0) {
                int ea = cand[b].x < 0 ? -cand[b].x : cand[b].x;
                int eb = cand[b].y < 0 ? -cand[b].y : cand[b].y;
                int de = ea > eb ? ea : eb;
                int pe = (MODE == 2) ? 1 - cand[b].black : 0;
                if (pe < pt || (pe == pt && (de < dt || (de == dt && (cand[b].x < t.x ||
                    (cand[b].x == t.x && cand[b].y <= t.y)))))) break;
                cand[b + 1] = cand[b]; b--;
            }
            cand[b + 1] = t;
        }
        ncand = MM;
    }
    // ordine canonico (x, y) e impacchettamento
    for (int a = 1; a < ncand; a++) {
        MemCell t = cand[a];
        int b = a - 1;
        while (b >= 0 && (cand[b].x > t.x || (cand[b].x == t.x && cand[b].y > t.y))) {
            cand[b + 1] = cand[b]; b--;
        }
        cand[b + 1] = t;
    }
    memset(key, 0, KEYB);
    for (int i = 0; i < NC; i++) if (nw[i]) set_cell(key, i, nw[i]);
    for (int k = 0; k < MM; k++) {
        uint16_t v = 0xFFFF;
        if (k < ncand)
            v = (uint16_t)(((cand[k].x + DD) << 6) | ((cand[k].y + DD) << 1) | cand[k].black);
        key[KB + 2 * k] = (uint8_t)(v & 0xFF);
        key[KB + 2 * k + 1] = (uint8_t)(v >> 8);
    }
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "uso: product_build <radius> <m> <D> <outdir> [cap]\n"); return 1; }
    R = atoi(argv[1]); MM = atoi(argv[2]); DD = atoi(argv[3]);
    const char *outdir = argv[4];
    uint64_t cap = (argc > 5) ? strtoull(argv[5], NULL, 10) : 0;
    MODE = (argc > 6) ? atoi(argv[6]) : 0;
    if (MODE < 0 || MODE > 2) die("modo sconosciuto (0=full, 1=black-only, 2=ibrida)");
    if (DD > 31) die("D > 31 non supportato dal packing (6 bit per coordinata)");
    S = 2 * R + 1; NC = S * S; KB = (NC + 3) / 4; KEYB = KB + 2 * MM; C0 = R * S + R;

    mapR_ = malloc(NC * 4); mapL_ = malloc(NC * 4);
    fwdRx = malloc(NC * 4); fwdRy = malloc(NC * 4);
    fwdLx = malloc(NC * 4); fwdLy = malloc(NC * 4);
    for (int xp = -R; xp <= R; xp++) for (int yp = -R; yp <= R; yp++) {
        int i = (xp + R) * S + (yp + R);
        int ox = yp + 1, oy = -xp;
        mapR_[i] = (ox >= -R && ox <= R && oy >= -R && oy <= R) ? (ox + R) * S + (oy + R) : -1;
        ox = -yp - 1; oy = xp;
        mapL_[i] = (ox >= -R && ox <= R && oy >= -R && oy <= R) ? (ox + R) * S + (oy + R) : -1;
    }
    for (int ox = -R; ox <= R; ox++) for (int oy = -R; oy <= R; oy++) {
        int j = (ox + R) * S + (oy + R);
        fwdRx[j] = -oy; fwdRy[j] = ox - 1;       // svolta R: (ox,oy) -> (-oy, ox-1)
        fwdLx[j] = oy;  fwdLy[j] = -ox - 1;      // svolta L: (ox,oy) -> (oy, -ox-1)
    }

    pool_cap = 1ull << 20;
    pool = calloc(pool_cap, KEYB);
    tcap = 1ull << 21; tmask = tcap - 1; tcount = 0;
    table = malloc(tcap * 4);
    memset(table, 0xFF, tcap * 4);

    char pfx[64], path[1024];
    const char *sfx = (MODE == 1) ? "b" : (MODE == 2) ? "h" : "";
    snprintf(pfx, sizeof pfx, "p%dm%dd%d%s", R, MM, DD, sfx);
    snprintf(path, sizeof path, "%s/%s_edges.bin", outdir, pfx);
    FILE *fedg = fopen(path, "wb");
    snprintf(path, sizeof path, "%s/%s_outdeg.bin", outdir, pfx);
    FILE *fdeg = fopen(path, "wb");
    snprintf(path, sizeof path, "%s/%s_tyx.bin", outdir, pfx);
    FILE *ftyx = fopen(path, "wb");
    if (!fedg || !fdeg || !ftyx) die("impossibile aprire gli output");
    setvbuf(fedg, NULL, _IOFBF, 1 << 23);
    setvbuf(fdeg, NULL, _IOFBF, 1 << 22);
    setvbuf(ftyx, NULL, _IOFBF, 1 << 22);

    uint8_t *win = malloc(NC);
    MemCell *M = malloc((MM + 1) * sizeof(MemCell));
    uint8_t *key = malloc(KEYB);

    int isnew;
    memset(key, 0, KB);
    for (int k = 0; k < MM; k++) { key[KB + 2 * k] = 0xFF; key[KB + 2 * k + 1] = 0xFF; }
    intern(key, &isnew);

    uint64_t nedges = 0, cnt[4] = {0, 0, 0, 0};
    time_t t0 = time(NULL);

    for (uint64_t si = 0; si < nstates; si++) {
        const uint8_t *ps = pool + si * (uint64_t)KEYB;
        for (int i = 0; i < NC; i++) win[i] = (uint8_t)get_cell(ps, i);
        int nM = 0;
        for (int k = 0; k < MM; k++) {
            uint16_t v = (uint16_t)(ps[KB + 2 * k] | (ps[KB + 2 * k + 1] << 8));
            if (v == 0xFFFF) break;
            M[nM].x = (int)(v >> 6) - DD;
            M[nM].y = (int)((v >> 1) & 0x1F) - DD;
            M[nM].black = v & 1;
            nM++;
        }
        int c0 = win[C0];
        // opzioni: (colore, ty, tyx)
        int cols[2], tys[2], tyxs[2], nopt;
        if (c0 == UC)      { cols[0]=WC; tys[0]=1; tyxs[0]=1; cols[1]=BC; tys[1]=2; tyxs[1]=2; nopt=2; }
        else if (c0 == WC) { cols[0]=WC; tys[0]=0; tyxs[0]=0; nopt=1; }
        else if (c0 == BC) { cols[0]=BC; tys[0]=0; tyxs[0]=0; nopt=1; }
        else               { cols[0]=BC; tys[0]=2; tyxs[0]=3; nopt=1; }   // B*: forzata, paga
        uint8_t od = (uint8_t)nopt;
        fwrite(&od, 1, 1, fdeg);
        for (int o = 0; o < nopt; o++) {
            step_product(win, M, nM, cols[o], key);
            uint32_t d = intern(key, &isnew);
            uint8_t rec[6];
            memcpy(rec, &d, 4);
            rec[4] = (uint8_t)tys[o];
            rec[5] = (uint8_t)(cols[o] == WC);
            fwrite(rec, 6, 1, fedg);
            uint8_t tx = (uint8_t)tyxs[o];
            fwrite(&tx, 1, 1, ftyx);
            nedges++; cnt[tyxs[o]]++;
        }
        if ((si & 0xFFFFF) == 0 && si) {
            printf("  ... processati %llu / scoperti %llu stati, %llu archi, %llds\n",
                   (unsigned long long)si, (unsigned long long)nstates,
                   (unsigned long long)nedges, (long long)(time(NULL) - t0));
            fflush(stdout);
        }
        if (cap && nstates > cap) {
            fprintf(stderr, "ABORT: superato il cap di %llu stati (scoperti %llu)\n",
                    (unsigned long long)cap, (unsigned long long)nstates);
            return 3;
        }
    }

    fclose(fedg); fclose(fdeg); fclose(ftyx);
    snprintf(path, sizeof path, "%s/%s_stats.txt", outdir, pfx);
    FILE *fst = fopen(path, "w");
    fprintf(fst, "radius %d\nmem %d\nbox %d\nmode %d\nstates %llu\nedges %llu\nforced %llu\nassumeW %llu\nassumeB %llu\nBstar %llu\nseconds %lld\n",
            R, MM, DD, MODE, (unsigned long long)nstates, (unsigned long long)nedges,
            (unsigned long long)cnt[0], (unsigned long long)cnt[1], (unsigned long long)cnt[2],
            (unsigned long long)cnt[3], (long long)(time(NULL) - t0));
    fclose(fst);
    printf("FATTO %s: stati %llu, archi %llu (forzati %llu, assumiW %llu, assumiB %llu, B* %llu) [%llds]\n",
           pfx, (unsigned long long)nstates, (unsigned long long)nedges,
           (unsigned long long)cnt[0], (unsigned long long)cnt[1], (unsigned long long)cnt[2],
           (unsigned long long)cnt[3], (long long)(time(NULL) - t0));
    return 0;
}
