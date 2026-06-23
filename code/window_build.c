// window_build.c — port C del BFS build() di window_automaton.py (semantica IDENTICA).
// Motivo del port: a r=4 il BFS Python supera i 27M stati e ~6 GB RSS (macchina da 16 GB);
// vedi CLAUDE.md §5.3. La semantica replicata alla lettera:
//   - stato = finestra (2r+1)x(2r+1), celle {0=ignota,1=bianca,2=nera}, frame canonico heading=su;
//   - lettura centro -> flip del centro PRIMA della trasformazione -> permutazione mapR/mapL;
//   - celle uscite dalla finestra = ignote (leak);
//   - centro ignoto: due archi nell'ordine (assumiW, assumiB); centro noto: un arco forzato;
//   - ordine BFS = ordine di scoperta (coda FIFO == ordine del pool).
//
// Uso: window_build <radius> <outdir> [cap_stati]
// Output binari (per analyze_radius.py):
//   <outdir>/r<R>_edges.bin  — 6 B/arco: u32 dst (little-endian), u8 ty (0=forzato,1=assumiW,2=assumiB), u8 tn (1=R,0=L)
//   <outdir>/r<R>_outdeg.bin — 1 B/stato (1 o 2), in ordine BFS: ricostruisce src = repeat(arange(N), outdeg)
//   <outdir>/r<R>_pool.bin   — stati impacchettati 2 bit/cella, KB=ceil(NC/4) B/stato (per certificati futuri)
//   <outdir>/r<R>_stats.txt  — conteggi per il cross-check
// Compilare: gcc -O3 -o window_build window_build.c

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

static int R, NC, KB, C0;
static int *mapR_, *mapL_;

static uint8_t *pool;       // KB byte per stato, in ordine BFS
static uint64_t pool_cap;   // capienza in stati
static uint64_t nstates;

static uint32_t *table;     // open addressing lineare, 0xFFFFFFFF = vuoto
static uint64_t tcap, tmask, tcount;

static uint64_t fnv1a(const uint8_t *k) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < KB; i++) { h ^= k[i]; h *= 1099511628211ULL; }
    return h;
}

static void table_grow(void) {
    uint64_t nc = tcap << 1, nm = nc - 1;
    uint32_t *nt = (uint32_t*)malloc(nc * 4);
    if (!nt) { fprintf(stderr, "OOM tabella (%llu slot)\n", (unsigned long long)nc); exit(2); }
    memset(nt, 0xFF, nc * 4);
    for (uint64_t i = 0; i < tcap; i++) {
        uint32_t v = table[i];
        if (v == 0xFFFFFFFFu) continue;
        uint64_t h = fnv1a(pool + (uint64_t)v * KB) & nm;
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
        if (memcmp(pool + (uint64_t)v * KB, key, KB) == 0) { *isnew = 0; return v; }
        h = (h + 1) & tmask;
    }
    if (nstates >= 0xFFFFFFFEull) { fprintf(stderr, "overflow u32 sugli stati\n"); exit(2); }
    if (nstates >= pool_cap) {
        pool_cap <<= 1;
        uint8_t *np_ = (uint8_t*)realloc(pool, pool_cap * (uint64_t)KB);
        if (!np_) { fprintf(stderr, "OOM pool (%llu stati)\n", (unsigned long long)pool_cap); exit(2); }
        pool = np_;
    }
    memcpy(pool + nstates * (uint64_t)KB, key, KB);
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

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "uso: window_build <radius> <outdir> [cap_stati]\n"); return 1; }
    R = atoi(argv[1]);
    const char *outdir = argv[2];
    uint64_t cap = (argc > 3) ? strtoull(argv[3], NULL, 10) : 0;
    int S = 2 * R + 1;
    NC = S * S;
    KB = (NC + 3) / 4;
    C0 = R * S + R;

    // mappe di trasformazione: per ogni cella nuova i=(xp,yp) -> cella vecchia o -1
    // (identiche a build() in window_automaton.py: R: (ox,oy)=(yp+1,-xp); L: (ox,oy)=(-yp-1,xp))
    mapR_ = (int*)malloc(NC * sizeof(int));
    mapL_ = (int*)malloc(NC * sizeof(int));
    for (int xp = -R; xp <= R; xp++) for (int yp = -R; yp <= R; yp++) {
        int i = (xp + R) * S + (yp + R);
        int ox = yp + 1, oy = -xp;
        mapR_[i] = (ox >= -R && ox <= R && oy >= -R && oy <= R) ? (ox + R) * S + (oy + R) : -1;
        ox = -yp - 1; oy = xp;
        mapL_[i] = (ox >= -R && ox <= R && oy >= -R && oy <= R) ? (ox + R) * S + (oy + R) : -1;
    }

    pool_cap = 1ull << 20;
    pool = (uint8_t*)calloc(pool_cap, KB);
    tcap = 1ull << 21; tmask = tcap - 1; tcount = 0;
    table = (uint32_t*)malloc(tcap * 4);
    memset(table, 0xFF, tcap * 4);

    char path[1024];
    snprintf(path, sizeof path, "%s/r%d_edges.bin", outdir, R);
    FILE *fedg = fopen(path, "wb");
    snprintf(path, sizeof path, "%s/r%d_outdeg.bin", outdir, R);
    FILE *fdeg = fopen(path, "wb");
    if (!fedg || !fdeg) { fprintf(stderr, "impossibile aprire output in %s\n", outdir); return 1; }
    setvbuf(fedg, NULL, _IOFBF, 1 << 23);
    setvbuf(fdeg, NULL, _IOFBF, 1 << 22);

    uint8_t *buf  = (uint8_t*)malloc(NC);   // stato corrente decompresso
    uint8_t *tmp  = (uint8_t*)malloc(NC);   // dopo flip del centro
    uint8_t *nbuf = (uint8_t*)malloc(NC);   // stato successivo decompresso
    uint8_t *key  = (uint8_t*)malloc(KB);   // stato successivo impacchettato

    int isnew;
    memset(key, 0, KB);
    intern(key, &isnew);                     // stato iniziale: tutto ignoto

    uint64_t nedges = 0, cnt_ty[3] = {0, 0, 0};
    time_t t0 = time(NULL);

    for (uint64_t si = 0; si < nstates; si++) {
        const uint8_t *ps = pool + si * (uint64_t)KB;
        for (int i = 0; i < NC; i++) buf[i] = (uint8_t)get_cell(ps, i);
        int c0 = buf[C0];
        // opzioni: centro ignoto -> (W=1,ty=1),(B=2,ty=2); centro noto -> (c0,ty=0)
        int cols[2], tys[2], nopt;
        if (c0 == 0) { cols[0] = 1; tys[0] = 1; cols[1] = 2; tys[1] = 2; nopt = 2; }
        else         { cols[0] = c0; tys[0] = 0; nopt = 1; }
        uint8_t od = (uint8_t)nopt;
        fwrite(&od, 1, 1, fdeg);
        for (int o = 0; o < nopt; o++) {
            int col = cols[o];
            memcpy(tmp, buf, NC);
            tmp[C0] = (col == 1) ? 2 : 1;            // flip del centro DOPO la lettura
            const int *m = (col == 1) ? mapR_ : mapL_;
            for (int i = 0; i < NC; i++) { int j = m[i]; nbuf[i] = (j >= 0) ? tmp[j] : 0; }
            memset(key, 0, KB);
            for (int i = 0; i < NC; i++) if (nbuf[i]) set_cell(key, i, nbuf[i]);
            uint32_t d = intern(key, &isnew);
            uint8_t rec[6];
            memcpy(rec, &d, 4);
            rec[4] = (uint8_t)tys[o];
            rec[5] = (uint8_t)(col == 1);            // tn: 1 se lettura bianca (svolta R)
            fwrite(rec, 6, 1, fedg);
            nedges++; cnt_ty[tys[o]]++;
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

    fclose(fedg); fclose(fdeg);
    snprintf(path, sizeof path, "%s/r%d_pool.bin", outdir, R);
    FILE *fpool = fopen(path, "wb");
    fwrite(pool, KB, nstates, fpool);
    fclose(fpool);

    snprintf(path, sizeof path, "%s/r%d_stats.txt", outdir, R);
    FILE *fst = fopen(path, "w");
    fprintf(fst, "radius %d\nstates %llu\nedges %llu\nforced %llu\nassumeW %llu\nassumeB %llu\nseconds %lld\n",
            R, (unsigned long long)nstates, (unsigned long long)nedges,
            (unsigned long long)cnt_ty[0], (unsigned long long)cnt_ty[1], (unsigned long long)cnt_ty[2],
            (long long)(time(NULL) - t0));
    fclose(fst);
    printf("FATTO r=%d: stati %llu, archi %llu (forzati %llu, assumiW %llu, assumiB %llu) [%llds]\n",
           R, (unsigned long long)nstates, (unsigned long long)nedges,
           (unsigned long long)cnt_ty[0], (unsigned long long)cnt_ty[1], (unsigned long long)cnt_ty[2],
           (long long)(time(NULL) - t0));
    return 0;
}
