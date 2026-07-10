/* danger_reach.c — §107c: port C del reach_dfs di danger_reach_depth.py.
 *
 * Enumera ESAUSTIVAMENTE l'albero dei prepend validi (alternanza + record-
 * compat y>=1 nel frame ancora) a partire da uno o piu' PREFISSI (sharding
 * per prefissi di scelte libere, §4: i conteggi dei shard DEVONO sommare ai
 * totali Python) e registra per ogni cella la profondita' minima di lettura.
 *
 * Semantica identica a reach_dfs (validata: R0/R0b/R1/RG + lente esterna
 * bit-identica); gate R2 = bit-identico vs Python (driver).
 *
 * Job file (testo):
 *   depth_cap
 *   x0 y0 krot
 *   nfoot
 *   x y c        (nfoot righe: footprint req0, frame cammino)
 *   nprefix
 *   <stringa di bit '0'/'1' lunga L>   (nprefix righe; L uguale per tutte,
 *                                       L=0 => riga vuota non ammessa: usare
 *                                       nprefix=1 e stringa "-" per radice)
 * Output (testo):
 *   NODES d count      (d = L..depth_cap, somma sui prefissi del job)
 *   HIT x y d          (frame cammino, prof. minima su tutto il job,
 *                       inclusi i passi di applicazione del prefisso)
 *   DONE nodes_totali
 * Build: gcc -O2 -o danger_reach.exe danger_reach.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define GRID 512
#define OFF  256
#define IDX(x, y) ((((y) + OFF) << 9) | ((x) + OFF))

static const int DXa[4] = {0, 1, 0, -1};
static const int DYa[4] = {-1, 0, 1, 0};

static int8_t  req[GRID * GRID];       /* -1 libera, 0/1 colore prima lettura */
static int8_t  req_base[GRID * GRID];  /* footprint di w (req0) */
static int32_t hit[GRID * GRID];       /* prof. minima di lettura, INT32_MAX */
static uint64_t nodes_per_depth[512];
static uint64_t nodes_tot = 0;
static int depth_cap, x0g, y0g, krot;

static inline int anchor_y(int x, int y) {
    int ax = x - x0g, ay = y - y0g;
    switch (krot) {
        case 0: return ay;
        case 1: return ax;
        case 2: return -ay;
        default: return -ax;
    }
}

static void visit(int px, int py, int h, int d) {
    nodes_tot++;
    nodes_per_depth[d]++;
    if (d == depth_cap) return;
    int qx = px - DXa[h], qy = py - DYa[h];
    if (anchor_y(qx, qy) < 1) return;
    if (qx <= -OFF || qx >= OFF || qy <= -OFF || qy >= OFF) {
        fprintf(stderr, "FUORI GRIGLIA (%d,%d)\n", qx, qy); exit(3);
    }
    int idx = IDX(qx, qy);
    int8_t seen = req[idx];
    int dn = d + 1;
    for (int c = 0; c <= 1; c++) {
        if (seen >= 0 && c != 1 - seen) continue;
        if (dn < hit[idx]) hit[idx] = dn;
        int hp = (c == 0) ? ((h + 3) & 3) : ((h + 1) & 3);
        req[idx] = (int8_t)c;
        visit(qx, qy, hp, dn);
        req[idx] = seen;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: danger_reach job.txt out.txt\n"); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { fprintf(stderr, "no job file\n"); return 1; }
    int nfoot;
    if (fscanf(f, "%d %d %d %d %d", &depth_cap, &x0g, &y0g, &krot, &nfoot) != 5) return 2;
    memset(req_base, -1, sizeof(req_base));
    for (int i = 0; i < nfoot; i++) {
        int x, y, c;
        if (fscanf(f, "%d %d %d", &x, &y, &c) != 3) return 2;
        req_base[IDX(x, y)] = (int8_t)c;
    }
    int nprefix;
    if (fscanf(f, "%d", &nprefix) != 1) return 2;
    for (int i = 0; i < 512; i++) nodes_per_depth[i] = 0;
    for (long i = 0; i < (long)GRID * GRID; i++) hit[i] = INT32_MAX;

    char buf[512];
    int L_global = -1;
    for (int pi = 0; pi < nprefix; pi++) {
        if (fscanf(f, "%511s", buf) != 1) return 2;
        memcpy(req, req_base, sizeof(req));
        int px = 0, py = 0, h = 0, d = 0;
        if (strcmp(buf, "-") != 0) {
            int L = (int)strlen(buf);
            for (int j = 0; j < L; j++) {
                int c = buf[j] - '0';
                int qx = px - DXa[h], qy = py - DYa[h];
                if (anchor_y(qx, qy) < 1) { fprintf(stderr, "prefisso invalido y\n"); return 4; }
                int idx = IDX(qx, qy);
                int8_t seen = req[idx];
                if (seen >= 0 && c != 1 - seen) { fprintf(stderr, "prefisso invalido alt\n"); return 4; }
                d++;
                if (d < hit[idx]) hit[idx] = d;
                h = (c == 0) ? ((h + 3) & 3) : ((h + 1) & 3);
                req[idx] = (int8_t)c;
                px = qx; py = qy;
            }
            if (L_global < 0) L_global = L;
            else if (L != L_global) { fprintf(stderr, "prefissi di lunghezza diversa\n"); return 4; }
        } else L_global = 0;
        visit(px, py, h, d);
    }
    fclose(f);
    FILE *o = fopen(argv[2], "w");
    if (!o) return 1;
    for (int d = (L_global < 0 ? 0 : L_global); d <= depth_cap; d++)
        fprintf(o, "NODES %d %llu\n", d, (unsigned long long)nodes_per_depth[d]);
    for (int y = -OFF + 1; y < OFF; y++)
        for (int x = -OFF + 1; x < OFF; x++)
            if (hit[IDX(x, y)] != INT32_MAX)
                fprintf(o, "HIT %d %d %d\n", x, y, hit[IDX(x, y)]);
    fprintf(o, "DONE %llu\n", (unsigned long long)nodes_tot);
    fclose(o);
    return 0;
}
