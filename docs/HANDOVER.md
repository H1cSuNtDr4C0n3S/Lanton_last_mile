# HANDOVER — Formica di Langton: dalla congettura dell'autostrada alle bocche d'ingresso
**Data: 10 giugno 2026 — Michael Spina + Claude. Stato: sessione conclusa dopo enumerazione e certificazione delle bocche.**

## 1. Obiettivo del programma
Trasformare la congettura dell'autostrada (ogni configurazione iniziale finita porta la formica nella highway di periodo P=104) da domanda globale a domanda locale e finita. Strategia maturata nella sessione: **non dimostrare che esistono pochi canali; dimostrare che la highway ha poche bocche d'ingresso e che ogni transiente finito raggiunge il bacino backward di una di esse.**

## 2. Convenzioni e protocollo (tutto il resto è condizionale a questi parametri)
- Regola: bianco→R+flip, nero→L+flip. heading 0=su,1=dx,2=giù,3=sx. turns: 1=R, 0=L.
- W0 = parola periodica di 104 svolte estratta dall'onset della griglia vuota (onset canonico = 9977). Fase k ≡ parola = roll(W0, −k).
- Onset N0 = minimo t tale che turns[t:] è esattamente 104-periodica (coda ≥ 5P, drift ≠ 0, rotazione netta ≡ 0 mod 4). Minimalità ⇒ turns[N0−1] viola la periodicità.
- Snapshot pre-onset a Δ = 208 passi prima di N0. Crop a raggio 30/45/60 attorno alla formica.
- **Criterio committed (scoperta definizionale chiave): "forza una highway" è VACUO** (la griglia vuota stessa la forza). Definizione corretta: patch committed ⟺ il replay isolato ha onset N0' ≤ Δ + 2P = 416.
- Nucleo 1-minimale: greedy iterata a punto fisso (passate ripetute finché nessuna rimozione preserva il commitment). La greedy single-pass NON è 1-minimale (lasciava ~50% di celle rimovibili e ~35% mai visitate).
- t* = ultimo first-hit delle celle del nucleo 1-minimale (commitment horizon). L_I = N0' − t* (lunghezza inerziale).
- Canale (stretto) = identità esatta della coda turns[t* : N0'+P]. Bocca = fase d'ingresso, parola turns[N0 : N0+P].
- Famiglia di seed usata OVUNQUE: box 7–15, densità 0.25–0.55, formica al centro heading 0. n=2000 run (seed rng 2026).

## 3. Catena dei risultati (con falsificazioni)
1. **Seme morfologico universale: falsificato** (classi canoniche C4+traslazione esplodono ~1/run, anche a punto fisso 30/30 distinte).
2. **Geometria statica fine: falsificata.** Pixel-model con GroupKFold per run: l'AUC 0.866 iniziale era confound di dimensione (solo conteggio celle: AUC 0.837). Size-matched (1 cella spostata di 1 passo, non-forcing): AUC 0.500, p=1.0. Spostare una cella di un passo distrugge il commitment senza firma lineare.
3. **Chiralità: il bacino committed è C4, non D4, in forma forte.** Nuclei riflessi: 2/30 restano committed (mediana onset 2712 vs ≤416). W̄ non può apparire: la riflessione coniuga LR→RL; sotto regola fissa esiste UNA sola classe chirale di parola. La riflessione espelle dal bacino committed.
4. **Lemma di località (dimostrabile + verificato):** cella mai visitata ⇒ traiettorie identiche ⇒ essenziale ⇒ visitata. Empirico: 0 essenziali mai visitate, 0 essenziali post-onset. **Nuclei 1-minimali: 100% delle celle visitate prima dell'onset, 30/30 run** ⇒ il nucleo è una sezione finita del cono causale, non un seme geometrico (test non tautologico: nuclei da crop spaziale).
5. **Struttura OR/hitting set:** il sottoinsieme delle celle individualmente essenziali è committed da solo solo in 18/30 run ⇒ esistono gruppi ridondanti disgiuntivi; il nucleo è un hitting set causale, non l'insieme delle essenziali.
6. **Commitment ≠ onset simbolico:** t*/N0' ≈ 0.45; l'ultimo ~50% del replay corre "in silenzio" senza nuovi switch essenziali.
7. **Cylinder set naive (parole pre-onset allineate a N0): falsificato** (27–28 cluster/30, dist ≈ null). Coerenza 6-gram = grammatica generica del replay sparso, non firma di commitment (controllo pre-t* vs mid-transiente).
8. **Canali esatti (la scoperta centrale):** parole post-t* identiche LETTERALMENTE per 200–330 simboli tra nuclei canonicamente distinti, con L_I costante per classe (165/165 classi multi-run a n=2000). Per determinismo: identità parola sull'intervallo spazzato ⟺ identità dello stato relativo sul cono ⇒ canale = stato-imbuto. Verificato: stati-imbuto identici tra membri (top 3 canali), compatti (regione spazzata 52–108 celle, 10–18 nere), e la maggioranza dello stato totale a t* è FUORI dal cono (es. 49/67 celle nere irrilevanti).
9. **Scaling C(n), n=2000:** legge di potenza C(n) = 2.68·n^0.70 (R²=0.9999); modello saturante e log nettamente battuti (AIC). Good–Turing P(nuovo) = 0.20. **Alfabeto di canali APERTO**, Zipf pendenza −0.98 (top 5 = 28% delle run, top 50 = 62%). I canali sono la chiusura backward delle bocche: la legge di potenza è la firma dell'enumerazione di preimmagini, non un fallimento del Lemma 1.
10. **Bocche: l'oggetto finito.** Suffissi distinti allineati all'onset: m=0 → **12**; 13→61, 26→157, 104→448, 208→794 (albero: bocca stretta, ramificazione backward).
11. **Teorema di collasso (argomento esatto):** la parola di svolte è C4-invariante ⇒ stati C4-correlati = stessa fase ⇒ le 12 bocche sono GIÀ il quoziente C4; fasi distinte ⇒ parole distinte ⇒ stati geometricamente distinti. Bocca ≅ fase. "3 ingressi × 4 rotazioni" impossibile.
12. **Φ = {0, 21, 24, 25, 31, 92, 98, 99, 100, 101, 102, 103} ⊂ Z₁₀₄. Due archi:** A = {92, 98–103, 0}: 98.45% delle run; B = {21,24,25,31}: 1.55%. Dominanza Zipf: fase 0 (= fase della griglia vuota!) 66.7%, poi 99 (19.2%), 102 (8.1%), 103 (4.0%). Non-monotonia interna (99 ≫ 98,100,101) + minimalità dell'onset ⇒ sotto-bocche genuine, non jitter.
13. **Certificati delle 12 bocche:** |R| = 39–50 celle (1 periodo), |B| = 13–18, periodicità esatta dal passo 0, drift (±2,±2). K=1 periodo di regione basta per 10/12; **fasi 98 e 99 richiedono K=2** (la highway lì rivisita il proprio corpo più indietro — anomalia nell'arco dominante). Struttura Lean: verifica finita di 104 passi + induzione per shift (stato del cono a t+104 = stato a t traslato del drift ⇒ periodicità eterna).
14. **Densità (intuizione 1/4 di Michael: falsificata come costante, sostituita dal gradiente):** bocche ρ_B = 0.317–0.385 (media 0.347), non speciali rispetto alle 104 fasi (percentile 39%). Invariante vero: **gradiente di densificazione backward** ρ(m): 0.144 (m=208) → 0.224 (104) → 0.285 (52) → 0.314 (26) → 0.329 (0), con **collasso di varianza** σ: 0.044 → 0.008. Il 18/72 = 0.25 del canale #1 era il punto della curva a profondità L_I = 131.

## 4. Formulazione corrente del Lemma 1
*Esiste un insieme finito di bocche d'ingresso alla highway (empiricamente 12 fasi su 104, in due archi, sotto la misura di seed usata). Ogni configurazione committed raggiunge una bocca tramite una preimmagine causale finita (stato-imbuto, certificabile); i canali osservati sono rami backward scale-free delle bocche. L'avvicinamento è un gradiente di densificazione del cono con collasso di varianza. La parte infinita della congettura si sposta nel problema backward/ricorrenza: ogni transiente finito raggiunge il bacino backward di una bocca.*

## 5. Domande aperte (in ordine di priorità)
1. **Stress-test di Φ:** famiglie di seed diverse (densità, box grandi, formica fuori centro, heading vari), Δ diverso, commit cap diverso, transienti lunghi. Le 12 restano 12? I due archi restano due? La dominanza della fase 0 è universale o è la misura?
2. **Perché QUELLE fasi?** Identificare l'evento geometrico del ciclo 104 che rende una fase "attaccabile" (le fasi 0 e 99 corrispondono a quali momenti della costruzione del mattone?). Perché 98/99 richiedono K=2?
3. **Formalizzazione Lean dei 12 certificati** (verifica finita + induzione per shift). Primo deliverable pubblicabile.
4. **Il problema backward:** caratterizzare il bacino backward delle bocche; il gradiente di densificazione come funzione di Lyapunov candidata? (ρ del cono cresce monotonicamente in media con collasso di varianza — può diventare un argomento di convergenza?)
5. Mappatura branch-point della struttura OR (celle diverse che proteggono lo stesso ingresso di canale).
6. I singleton di C(n): frammenti di canali lunghi (chiavi sovra-specificate) o canali genuini rari? L'analisi per bocche è key-length-free ed è l'invariante pulito.

## 6. Inventario file (in questo tar, dir ant_pkg/)
- `libant.c` — simulatore C (compilare: `gcc -O3 -march=native -shared -fPIC libant.c -o libant.so`). Snapshot a passo arbitrario. Validato: onset griglia vuota = 9977.
- `antlib.py` — wrapper ctypes, detect_onset, classify_word, normalize_C4, canon_C4, reflect_x. W0 in `W0.npy`.
- `pipeline.py` — generazione run + greedy single-pass (criterio committed). Output `runs.pkl` (30 run pilota).
- `tests.py` — Test 1 speculare, Test 2 clustering parole, Test 3 pixel model (con i confound POI corretti: vedi §3.2, size-matched fatto a parte).
- `causal.py` — first-hit, essenzialità, tabella `causal_table.csv`, figura `causal_cone.png`.
- `runway.py` — test pista inerziale; output `fixpoint.pkl` (nuclei 1-minimali, 30 run).
- `scaling.py` — pipeline completa a n=2000; output `scaling.pkl` (core, ah, onset, tstar, LI, tail, turns per run).
- `mouths.py` — fasi, certificati delle 12 bocche, densità su tutte le 104 fasi, gradiente backward ρ(m), ρ dei top 50 canali.
- Tempi: n=2000 run complete ≈ 134 s. Tutto il resto è secondi.

## 7. Trappole note (non ricaderci)
- Criterio di forcing senza vincolo temporale = vacuo.
- Greedy single-pass ≠ 1-minimale: iterare a punto fisso.
- Negativi della greedy hanno più celle dei positivi: confound di dimensione nei classificatori (usare size-matched + GroupKFold per run + null di permutazione).
- snap_grid del wrapper è GIÀ 2D (indicizzare g[y+H, x+H]).
- Hamming con shift su finestre a Δ fisso da N0 guarda nel punto sbagliato: ancorare a t*.
- La coerenza k-gram nei replay sparsi è grammatica generica: controllare sempre vs pre-t* e mid-transiente.
- Il quoziente C4 sulle bocche è già consumato dalla parola: non cercare collassi geometrici ulteriori.
