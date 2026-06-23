// min_assumeB.c — min tasso assumiB per passo (min cycle mean con pesi 0/1) sul grafo
// dell'automa a finestra SENZA archi-rotore. Sostituisce la bisezione Bellman-Ford O(V*E)
// di window_automaton.py --karp, infattibile a r=4 (27M stati).
//
// Fatto strutturale sfruttato: il sottografo noB-senza-rotori e' un DAG (tutti i cicli noB
// vivono nei rotori — Teorema della Finestra). Quindi un "round" = una passata di
// rilassamento esatto in ordine topologico sugli archi noB + un rilassamento degli archi
// assumiB. Fixpoint => nessun ciclo di media < mu (certificato di lower bound).
//
// Semantica identica al --karp Python: si rimuovono TUTTI gli archi (s,d), di qualunque
// tipo, la cui coppia coincide con un arco-rotore; peso = 1 se assumiB, 0 altrimenti.
//
// Modi:
//   min_assumeB <outdir> <prefix es. r4> bisect [maxrounds]
//       bisezione float (30 passi) per LOCALIZZARE il minimo; al termine estrae un ciclo
//       esplicito con media < hi via predecessori e ne stampa la media esatta p/q e la
//       parola di svolte. (La bisezione e' euristica: il rigore arriva dal modo verify.)
//   min_assumeB <outdir> <radius> verify <p> <q>
//       check ESATTO in aritmetica intera (pesi q*w - p, int64): se raggiunge il fixpoint,
//       NESSUN ciclo ha media < p/q => insieme a un ciclo esplicito di media p/q si ha
//       delta_r = p/q esatto.
//
// Richiede: r<R>_outdeg.bin, r<R>_edges.bin (da window_build) e r<R>_rotor_edges.txt
// (da gen_rotor_edges.py) in <outdir>.
// Compilare: gcc -O3 -o min_assumeB min_assumeB.c

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

static int64_t N, E;
static uint32_t *eptr;   // N+1: archi dello stato v in [eptr[v], eptr[v+1])
static uint32_t *dst;
static uint8_t *ty, *tn, *keep;
static uint32_t *topo;   // ordine topologico del sottografo noB-kept
static int64_t ntopo;

static void die(const char *msg) { fprintf(stderr, "ERRORE: %s\n", msg); exit(2); }

static void load(const char *outdir, const char *pfx) {
    char path[1024];
    snprintf(path, sizeof path, "%s/%s_outdeg.bin", outdir, pfx);
    FILE *f = fopen(path, "rb");
    if (!f) die("outdeg.bin mancante");
    fseek(f, 0, SEEK_END); N = ftell(f); fseek(f, 0, SEEK_SET);
    uint8_t *deg = (uint8_t*)malloc(N);
    if (fread(deg, 1, N, f) != (size_t)N) die("lettura outdeg");
    fclose(f);

    eptr = (uint32_t*)malloc((N + 1) * 4);
    eptr[0] = 0;
    for (int64_t i = 0; i < N; i++) eptr[i + 1] = eptr[i] + deg[i];
    free(deg);
    E = eptr[N];

    snprintf(path, sizeof path, "%s/%s_edges.bin", outdir, pfx);
    f = fopen(path, "rb");
    if (!f) die("edges.bin mancante");
    fseek(f, 0, SEEK_END);
    if (ftell(f) != E * 6) die("dimensione edges.bin incoerente con outdeg");
    fseek(f, 0, SEEK_SET);
    dst = (uint32_t*)malloc(E * 4);
    ty = (uint8_t*)malloc(E); tn = (uint8_t*)malloc(E); keep = (uint8_t*)malloc(E);
    uint8_t *rawbuf = (uint8_t*)malloc(6 << 20);
    int64_t i = 0;
    size_t got;
    while ((got = fread(rawbuf, 6, 1 << 20, f)) > 0) {
        for (size_t k = 0; k < got; k++, i++) {
            memcpy(&dst[i], rawbuf + 6 * k, 4);
            ty[i] = rawbuf[6 * k + 4];
            tn[i] = rawbuf[6 * k + 5];
        }
    }
    fclose(f); free(rawbuf);
    if (i != E) die("conteggio archi incoerente");
    memset(keep, 1, E);

    snprintf(path, sizeof path, "%s/%s_rotor_edges.txt", outdir, pfx);
    f = fopen(path, "r");
    if (!f) die("rotor_edges.txt mancante (eseguire gen_rotor_edges.py)");
    long long s, d;
    int64_t nrot = 0, nmark = 0;
    while (fscanf(f, "%lld %lld", &s, &d) == 2) {
        nrot++;
        for (uint32_t e2 = eptr[s]; e2 < eptr[s + 1]; e2++)
            if (dst[e2] == (uint32_t)d) { keep[e2] = 0; nmark++; }
    }
    fclose(f);
    printf("N=%lld E=%lld | coppie-rotore %lld -> archi rimossi %lld\n",
           (long long)N, (long long)E, (long long)nrot, (long long)nmark);

    // ordine topologico (Kahn) del sottografo noB-kept; se non copre tutti i nodi
    // raggiungibili da cicli noB residui, il fatto strutturale e' FALSO -> abort.
    uint32_t *indeg = (uint32_t*)calloc(N, 4);
    for (int64_t v = 0; v < N; v++)
        for (uint32_t e2 = eptr[v]; e2 < eptr[v + 1]; e2++)
            if (keep[e2] && ty[e2] != 2) indeg[dst[e2]]++;
    topo = (uint32_t*)malloc(N * 4);
    int64_t head = 0;
    ntopo = 0;
    for (int64_t v = 0; v < N; v++) if (indeg[v] == 0) topo[ntopo++] = (uint32_t)v;
    while (head < ntopo) {
        uint32_t v = topo[head++];
        for (uint32_t e2 = eptr[v]; e2 < eptr[v + 1]; e2++)
            if (keep[e2] && ty[e2] != 2 && --indeg[dst[e2]] == 0) topo[ntopo++] = dst[e2];
    }
    free(indeg);
    if (ntopo != N) {
        fprintf(stderr, "ATTENZIONE: il sottografo noB-senza-rotori NON e' un DAG "
                "(%lld/%lld nodi in ordine topologico) — fatto strutturale FALSIFICATO\n",
                (long long)ntopo, (long long)N);
        exit(4);
    }
    printf("noB-senza-rotori: DAG confermato (%lld nodi in ordine topologico)\n", (long long)ntopo);
}

// un round float: passata DAG (noB) in ordine topologico + rilassamento archi assumiB.
// ritorna 1 se qualche dist e' diminuita. pred*: per l'estrazione del ciclo.
static uint32_t g_lastupd;

static int round_float(double *dist, double mu, uint32_t *pred, uint32_t *prede) {
    int changed = 0;
    for (int64_t k = 0; k < N; k++) {
        uint32_t v = topo[k];
        double dv = dist[v];
        for (uint32_t e2 = eptr[v]; e2 < eptr[v + 1]; e2++) {
            if (!keep[e2] || ty[e2] == 2) continue;
            double nd = dv - mu;
            uint32_t d = dst[e2];
            if (nd < dist[d] - 1e-12) {
                dist[d] = nd;
                if (pred) { pred[d] = v; prede[d] = e2; }
                changed = 1; g_lastupd = d;
            }
        }
    }
    for (int64_t v = 0; v < N; v++) {
        double dv = dist[v];
        for (uint32_t e2 = eptr[v]; e2 < eptr[v + 1]; e2++) {
            if (!keep[e2] || ty[e2] != 2) continue;
            double nd = dv + 1.0 - mu;
            uint32_t d = dst[e2];
            if (nd < dist[d] - 1e-12) {
                dist[d] = nd;
                if (pred) { pred[d] = (uint32_t)v; prede[d] = e2; }
                changed = 1; g_lastupd = d;
            }
        }
    }
    return changed;
}

// 1 se esiste (probabilmente) un ciclo con media < mu: cambia ancora dopo maxrounds
static int has_negcycle_float(double mu, int maxrounds, uint32_t *last_changed) {
    double *dist = (double*)calloc(N, 8);
    int ch = 0, r;
    for (r = 0; r < maxrounds; r++) {
        ch = round_float(dist, mu, NULL, NULL);
        if (!ch) break;
    }
    free(dist);
    if (ch) printf("    mu=%.10f: ancora attivo dopo %d round (ciclo negativo)\n", mu, r);
    else    printf("    mu=%.10f: fixpoint dopo %d round (nessun ciclo < mu)\n", mu, r + 1);
    fflush(stdout);
    (void)last_changed;
    return ch;
}

static void extract_cycle(double mu, int maxrounds, const char *outdir, const char *pfx) {
    double *dist = (double*)calloc(N, 8);
    uint32_t *pred = (uint32_t*)malloc(N * 4), *prede = (uint32_t*)malloc(N * 4);
    memset(pred, 0xFF, N * 4);
    int ch = 0;
    for (int r = 0; r < maxrounds; r++) { ch = round_float(dist, mu, pred, prede); if (!ch) break; }
    if (!ch) { printf("estrazione: fixpoint a mu=%.10f, niente ciclo\n", mu); exit(5); }
    // parti dall'ULTIMO nodo aggiornato (sta su un ciclo o a valle di uno) e cammina
    // all'indietro marcando: il primo nodo rivisitato appartiene al ciclo dei predecessori
    uint8_t *mark = (uint8_t*)calloc(N, 1);
    uint32_t u = g_lastupd;
    while (!mark[u]) {
        mark[u] = 1;
        if (pred[u] == 0xFFFFFFFFu) die("catena predecessori interrotta (riprovare con piu' round)");
        u = pred[u];
    }
    // u e' nel ciclo: raccogli (parola + annotazioni per l'autopsia)
    long long p = 0, q = 0;
    char *word = (char*)malloc(1 << 22);
    char *tych = (char*)malloc(1 << 22);
    uint32_t *cnode = (uint32_t*)malloc((size_t)4 << 22);
    uint32_t w = u;
    int64_t wi = 0;
    do {
        uint32_t e2 = prede[w];
        word[wi] = tn[e2] ? 'R' : 'L';
        tych[wi] = (ty[e2] == 0) ? 'F' : (ty[e2] == 1 ? 'W' : 'B');
        cnode[wi] = w;                       // nodo di ARRIVO dell'arco e2
        wi++;
        p += (ty[e2] == 2);
        q++;
        w = pred[w];
    } while (w != u && wi < (1 << 22) - 1);
    word[wi] = 0; tych[wi] = 0;
    // la camminata sui predecessori va all'INDIETRO: inverti parola, tipi e nodi
    for (int64_t a2 = 0, b2 = wi - 1; a2 < b2; a2++, b2--) {
        char t = word[a2]; word[a2] = word[b2]; word[b2] = t;
        t = tych[a2]; tych[a2] = tych[b2]; tych[b2] = t;
        uint32_t tu = cnode[a2]; cnode[a2] = cnode[b2]; cnode[b2] = tu;
    }
    printf("CICLO ESPLICITO: lunghezza q=%lld, assumiB p=%lld, media p/q=%lld/%lld = %.10f\n",
           q, p, p, q, (double)p / (double)q);
    char path[1024];
    snprintf(path, sizeof path, "%s/%s_delta_cycle.txt", outdir, pfx);
    FILE *f = fopen(path, "w");
    fprintf(f, "p %lld\nq %lld\nword %s\ntypes %s\n", p, q, word, tych);
    fclose(f);
    snprintf(path, sizeof path, "%s/%s_delta_cycle_annot.txt", outdir, pfx);
    f = fopen(path, "w");
    fprintf(f, "# step turn type dst_node_id (id nel grafo ridotto; lo stato di partenza dello\n");
    fprintf(f, "# step k e' dst dello step k-1, ciclicamente)\n");
    for (int64_t k = 0; k < wi; k++)
        fprintf(f, "%lld %c %c %u\n", (long long)k, word[k], tych[k], cnode[k]);
    fclose(f);
    printf("parola del ciclo + annotazioni scritte in %s\n", path);
    free(dist); free(pred); free(prede); free(mark); free(word); free(tych); free(cnode);
}

// verifica esatta: pesi interi q*w - p; fixpoint => nessun ciclo con media < p/q
static int verify_exact(long long p, long long q, int maxrounds) {
    int64_t *dist = (int64_t*)calloc(N, 8);
    long long wB = q - p, w0 = -p;
    for (int r = 0; r < maxrounds; r++) {
        int changed = 0;
        for (int64_t k = 0; k < N; k++) {
            uint32_t v = topo[k];
            int64_t dv = dist[v];
            for (uint32_t e2 = eptr[v]; e2 < eptr[v + 1]; e2++) {
                if (!keep[e2] || ty[e2] == 2) continue;
                int64_t nd = dv + w0;
                if (nd < dist[dst[e2]]) { dist[dst[e2]] = nd; changed = 1; }
            }
        }
        for (int64_t v = 0; v < N; v++) {
            int64_t dv = dist[v];
            for (uint32_t e2 = eptr[v]; e2 < eptr[v + 1]; e2++) {
                if (!keep[e2] || ty[e2] != 2) continue;
                int64_t nd = dv + wB;
                if (nd < dist[dst[e2]]) { dist[dst[e2]] = nd; changed = 1; }
            }
        }
        if (!changed) {
            printf("VERIFY: fixpoint INTERO dopo %d round => nessun ciclo con media < %lld/%lld "
                   "(lower bound certificato)\n", r + 1, p, q);
            free(dist);
            return 1;
        }
    }
    printf("VERIFY: ancora attivo dopo %d round => ESISTE un ciclo con media < %lld/%lld\n",
           maxrounds, p, q);
    free(dist);
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "uso: min_assumeB <outdir> <prefix es. r4> bisect [maxrounds] | verify <p> <q> [maxrounds]\n"); return 1; }
    const char *outdir = argv[1];
    const char *pfx = argv[2];
    load(outdir, pfx);
    time_t t0 = time(NULL);
    if (strcmp(argv[3], "bisect") == 0) {
        int maxrounds = (argc > 4) ? atoi(argv[4]) : 5000;
        double lo = 0.0, hi = 1.0;
        for (int i = 0; i < 30; i++) {
            double mid = 0.5 * (lo + hi);
            if (has_negcycle_float(mid, maxrounds, NULL)) hi = mid; else lo = mid;
            printf("  bisez %2d: [%.10f, %.10f]  (%llds)\n", i + 1, lo, hi, (long long)(time(NULL) - t0));
            fflush(stdout);
        }
        printf("min tasso assumiB (float): in (%.10f, %.10f]\n", lo, hi);
        extract_cycle(hi, maxrounds, outdir, pfx);
    } else if (strcmp(argv[3], "extract") == 0) {
        // extract <mu> [maxrounds] [cutsfile]: il cutsfile (coppie "src dst") rimuove i SOLI
        // archi assumiB con quella coppia — e' il taglio dei cicli-fantasma di delta_alt.
        if (argc < 5) die("extract richiede mu");
        double mu = atof(argv[4]);
        int maxrounds = (argc > 5) ? atoi(argv[5]) : 200;
        if (argc > 6) {
            FILE *fc = fopen(argv[6], "r");
            if (!fc) die("cutsfile illeggibile");
            long long s, d;
            int64_t ncut = 0;
            while (fscanf(fc, "%lld %lld", &s, &d) == 2)
                for (uint32_t e2 = eptr[s]; e2 < eptr[s + 1]; e2++)
                    if (dst[e2] == (uint32_t)d && ty[e2] == 2 && keep[e2]) { keep[e2] = 0; ncut++; }
            fclose(fc);
            printf("tagli fantasma: %lld archi assumiB rimossi\n", (long long)ncut);
        }
        extract_cycle(mu, maxrounds, outdir, pfx);
    } else if (strcmp(argv[3], "verify") == 0) {
        if (argc < 6) die("verify richiede p e q");
        long long p = atoll(argv[4]), q = atoll(argv[5]);
        int maxrounds = (argc > 6) ? atoi(argv[6]) : 100000;
        if (!verify_exact(p, q, maxrounds)) return 6;
    } else die("modo sconosciuto");
    printf("[%llds totali]\n", (long long)(time(NULL) - t0));
    return 0;
}

