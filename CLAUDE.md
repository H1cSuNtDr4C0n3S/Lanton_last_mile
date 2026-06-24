# CLAUDE.md — Progetto Langton Last Mile (C:\langton_last_mile)

Programma di dimostrazione della congettura dell'autostrada della formica di Langton.
Collaborazione con Michael Spina. **Lingua di lavoro: italiano.**

## 0. Prima di tutto
1. Leggi `CHAT_HANDOVER.md` (stato del programma, risultati, roadmap) — è la fonte di verità.
2. Se esiste `C:\Langton_research\claude.md` (l'altro progetto), leggilo e **fondi le sue
   convenzioni di parallelizzazione con la §4 qui sotto: in caso di conflitto vince quello**.
3. Non eseguire MAI run lunghe prima di aver passato i self-test (§5).

## 1. Metodologia (non negoziabile)
- Stile Faraday–Maxwell: falsificazionismo, onestà sopra validazione. Ogni ipotesi va
  attaccata, non difesa. Un risultato senza tentativo di falsificazione non è un risultato.
- Ogni numero importante va validato con almeno un check indipendente (identità interne,
  casi noti, conteggi incrociati). I valori certificati sono nei summary JSON e negli addenda.
- Verbali: si continua la numerazione dei paragrafi degli addenda (prossimo: **§72**).
  Ogni sessione produce un ADDENDUM nello stesso stile (riepilogo in una frase, risultati,
  trappole nuove, domande aperte, inventario file).
- Trappole note: lista cumulativa negli addenda (`docs/`). Le più letali:
  (a) **survivorship da bordo griglia** (run a onset precoce escono percorrendo la highway
      ⇒ campione distorto; antidoto: onset detection incrementale con stop anticipato);
  (b) DFS con stack condiviso: il ramo a svolta forzata DEVE fare pop come il ramo libero
      (sintomo: rapporti interi esatti tra conteggi indipendenti);
  (c) l'automa a finestra è una SOVRA-approssimazione: si trasferiscono alle orbite solo
      enunciati "ogni cammino infinito fa X", MAI "esiste un cammino che fa Y";
  (d) parole cicliche: confronti solo a meno di rotazione (funzione `canon`);
  (e) min cycle mean assumiB sul grafo pieno è banalmente 0: ha senso solo senza archi-rotore;
  (f) processi lunghi: chunking con budget temporale interno e checkpoint su disco;
  (g) **reset-hash per-seme = collo di banda di memoria** (ALPHA1 §57.7-a): in una ricerca
      parallela su molti semi, azzerare l'INTERA tabella hash a ogni seme satura la banda di
      memoria (non i thread) e fa crollare il throughput ~8×. Resettare SOLO le celle toccate
      (lista `touched`, reset O(celle) non O(tabella)). Vale per ogni sweep multi-seme;
  (h) **survivorship temporale** (ALPHA1 §57.7-b): selezionare orbite per onset alto = selezionare
      per starvation (densità bassa/stalli lunghi quasi per definizione). I tassi/pavimenti si
      leggono SOLO within-orbit, mai confrontando semi di T diverso. È la (a) nel tempo;
  (i) **controfattuale eterno** (ALPHA1 §57.6): ogni orbita simulata converge ⇒ NESSUNA soglia
      misurata sul finito prova un enunciato su orbite eterne (α1, pavimenti del tasso, ...).
      La simulazione può falsificare un meccanismo locale, non decidere α1.

## 2. Convenzioni della dinamica (INVARIATE da HANDOVER §2)
- Bianco → svolta R (orario), nero → L; la cella si inverte dopo la lettura; poi mossa di 1.
- Heading: 0=su, 1=destra, 2=giù, 3=sinistra. Lettura→svolta→flip→mossa.
- W0 = parola della highway, periodo 104 (58 R, P(R)=0.558, rot=12), drift diagonale (±2,±2).
  File: `data/W0.npy` (0/1), `data/w0.txt` (L/R). Onset griglia vuota: N0=9977.
- morso = lettura **fresca-bianca** (`fresh & color==0`); definizione canonica in `morso_census.py`.
- Parola realizzabile = compatibile con QUALCHE configurazione finita: fresche libere,
  rivisite forzate dall'alternanza. R(n) censiti fino a 40 (`data/gamma_enum.pkl`).

## 3. Mappa del progetto
- `CHAT_HANDOVER.md` — stato completo del programma e roadmap.
- `docs/` — catena degli addenda: HANDOVER, HANDOVER2, ANATOMY, ALPHA (§1–28),
  GAMMA (§29–35), MORSO (§36–44), RADIUS (§45–55), PRODOTTO (§56), ALPHA1_FABRY (§57),
  DELTA4-BETA (§58), DEBT-LOCK (§59), DEBT-LOCK 2D (§60), LOCK-CHECKLIST (§61),
  CHECKLIST-MIXING (§62), CHECKLIST-VECTOR (§63), CHECKLIST-VECTOR-MODEL (§64),
  CHECKLIST-NONLOCAL (§65), DOOR-DEFECT-PROFILE (§66), POTENTIAL-SEGMENT-SCANNER (§67),
  ENDPOINT-MONOTONE-NOGO (§68), COMPATIBILITY-POTENTIAL (§69),
  **COMPAT-EVENT/CO-RAGGIUNGIBILITA' (§70-§71)**.
  La numerazione § è globale e continua.
- `alpha1/` — **sonde α1/β via distribuzione dei valori (§57), non-localita' r=4 (§58),
  hazard debito->lock (§59), modello 2D deep/bite (§60), lock->checklist T3' (§61),
  hazard/mixing checklist (§62), vettore/geometria checklist (§63), modello/compressione
  vettoriale checklist (§64), ridirezione non-locale/globale con correzione Pauli (§65),
  profilo 22-porte lock-condizionato (§66), scanner dei potenziali segmentali (§67),
  audit/no-go endpoint-monotono (§68), `Φ_compat` endpoint (§69), `Φ_compat` event-wise
  + schema T3'/co-raggiungibilita' (§70), e scanner di coppie co-raggiungibili T3' (§71).**
  `alpha1_engine.c` (+ .exe): simulatore C self-contained, modi `search`/`reseed`/`dump`,
  **early-stop all'onset + reset-solo-celle-toccate** (31.7k semi/s su 14 shard), semi
  riproducibili dal solo stato RNG a 64 bit. Validato: vuota→9977, (7,−7)→106258, highway 22/104.
  `alpha1_within.py` (test within-orbit: max-stall, pavimento a finestra), `status.ps1` (monitor),
  `ALPHA1_RUN.md` (run), `onsets_shard*.txt` (88.521 hit≥100k), `dumps_all.txt` (24 orbite lunghe).
  `delta4_long_orbits.py` rigenera le 24 orbite da `rngstate` e misura `r=4` deep-black,
  minimi mobili e lock W0-like; risultato §58: il debito profondo tiene mentre il morso fresco
  affonda.
  `debt_lock_hazard.py` usa predictor causale `[t-L,t)` e lock futuro `[t,t+H)`; risultato §59:
  il ponte diretto deep-black -> lock e' anti-correlato, mentre fresh-bite predice positivamente.
  `debt_lock_2d.py` mostra che l'effetto fresh-bite resta positivo a deep quasi fissato, mentre
  deep resta negativo/debole a bite quasi fissato.
  `lock_checklist_probe.py` ricostruisce E(k) da `W0` e valuta T3' sui gate-lock: risultato §61,
  891/891 morti esatte alla prima lettura esogena cattiva e 24/24 onset veri OK.
  `checklist_mixing.py` deduplica i gate-attempt e misura hazard/mixing: risultato §62,
  810 tentativi porta unici, hazard OK 0.0296, riuso cella critica 1/762 consecutivo e
  1/12.945 intra-orbita.
  `checklist_vector_geometry.py` salva origine/heading porta e vettore esogeno: risultato §63,
  57.177 letture esogene, 5.806 mismatch, prima cattiva=morte in 786/786 fallimenti,
  origine porta consecutiva riusata 0/786.
  `checklist_vector_model.py` analizza i CSV di §63 senza nuova simulazione: risultato §64,
  full-vector diagonale (786/786 KO, 24/24 OK), due periodi coprono 774/786 KO, fascia 45-77
  domina le prime morti, 98-99 resta necessario, compressione greedy 37 offset / 66 componenti
  phase-conditioned sul campione lungo.
  `docs/CHECKLIST_NONLOCAL_STRATEGY_ADDENDUM.md` registra §65: T3' e' verdetto esatto ma
  il troncamento corto fallisce; 12 KO oltre due periodi arrivano a offset 1591 e L∞ 36.
  Correzione Pauli: §65 e' diagnosi strategica/campionaria, non teorema dinamico.
  `door_defect_profile.py` registra §66: su 810 tentativi la fase reale e' best unica 810/810,
  fasi compatibili alternative muoiono entro 5 letture. Upgrade strategico: identificare la
  porta e' locale, decidere se la porta vera entra e' globale.
  `potential_segment_scanner.py` registra §67: Pauli ha selezionato `Φ_depth` e `Φ_mass(λ)`;
  la run completa fa 24/24 orbite, 21.327 ancore, 21.183 segmenti. Gate `L=1600`: violazioni
  **400/762** per `Φ_depth`, **373/762** per `Φ_mass_104`, **380/762** per `Φ_mass_208`.
  Grid `L=1600`: `best22_depth` **3591/6275**, `best22_mass_104` **3150/6275**,
  `best22_mass_208` **3145/6275**. Conclusione: non riprovare potenziali endpoint-monotoni
  finiti cambiando solo pesi.
  `endpoint_monotone_audit.py` registra §68: no-go empirico/testimoniale, non teorema dinamico.
  Gate `L=1600`: `Φ_depth` **400/762** non-decrementi e **350/762** peggioramenti stretti;
  `Φ_mass_104` **373/762** e **371/762**; `Φ_mass_208` **380/762** e **378/762**.
  Grid `L=1600`: `best22_mass_104` **3150/6275** non-decrementi e **3149/6275** peggioramenti
  stretti. Addendum strategico §68: massa/area/mismatch non sono coordinate orientate; i flip
  locali depositano e ripuliscono, quindi i conteggi oscillano. §69 = `Φ_compat^L` + schema
  T3'/co-raggiungibilita', non nuovo `λ`.
  `compat_endpoint_audit.py` registra §69: endpoint `Φ_compat^L` coincide con `best22_depth` e
  quindi non e' nuovo. Gate `L=1600`: `h_best` non migliora in **400/762** e peggiora strettamente
  in **350/762**; grid: **3591/6275** e **2736/6275**.
  `compat_event_audit.py` registra §70: su **600** eventi deep-black (24 orbite, 25/orbita,
  `L=1600`, `--min-event-t 1040`), `h_best` non migliora in **357/600** e peggiora in
  **259/600**; la monotonia immediata ingenua di `Φ_compat` e' falsificata.
  `t3_coreachability_pair_scanner.py` registra §71: witness dinamico co-raggiungibile a
  `R=8` (orbita 5, fase 98, offset 494, rel `(15,13)`, `L∞=15`). Lettura conservativa:
  e' non-vacuita' dinamica dello schema, non sostegno diretto a un potenziale uniforme.
  A `R=16`, zero collisioni sulla griglia stride 520 e' soprattutto sparsita' combinatoria.
- `code/window_automaton.py` — automa a finestra raggio r (lo strumento principale ora).
- `code/product_automaton.py` (+ `product_build.c`/.exe) — automa-prodotto A(r;m,D): finestra ×
  memoria di celle uscite (alternanza dentro gli stati). Builder C, 3 politiche; `--selftest`
  OBBLIGATORIO. Per istanze non minuscole usare SOLO il builder C (`--use-c`); MAI il BFS Python
  oltre poche migliaia di stati (esplode + swap). Diagnosi e ostacoli aperti: PRODOTTO §56.4–56.6.
- `code/ghost_block_analysis.py`, `code/check_witnesses.py` — copertura catalogo (m,D,politica) e
  check alternanza/realizzabilità/gamma dei testimoni del prodotto.
- `code/gamma_enum.c` — enumeratore/checker code periodiche eterne (`gcc -O3 -o gamma_enum gamma_enum.c`).
  Modi: `sweep pmin pmax`, `part p K idx`, `check file.txt`.
- `code/morso_census.py`, `code/morso_automaton.py` — censimento morsi e prototipo automa.
- `code/libant.c`, `code/antlib.py` — simulatore C della vecchia pipeline (compilare:
  `gcc -O3 -shared -fPIC -o libant.so libant.c`).
- `data/` — parole di test, pkl certificati; `results/` — summary e cicli raggio 1–3 già
  calcolati (valori di riferimento per i cross-check).

## 4. Parallelizzazione (Ryzen 7 5800X, 8C/16T) — default se claude.md esterno non dice altro
- CPU-bound puro (C, sweep gamma_enum / alpha1 search): 14 processi shard con `start /low` o
  priorità BelowNormal (lasciare 2 thread liberi); shard disgiunti (per prefissi di scelte libere,
  o per offset RNG con semi riproducibili). I conteggi dei shard DEVONO sommare ai totali noti.
- **Collo di bottiglia = memoria, non thread** (lezione ALPHA1 §57.1): se ogni iterazione tocca/
  azzera una struttura grossa, 14 processi saturano la banda. Resettare solo lo stato sporcato
  (es. celle toccate) prima di scalare i thread. Misurato: 1.8k→31.7k semi/s solo con questo fix.
- Python memory-bound (BFS automa, dict grossi): 6–8 processi max (la RAM e la cache L3
  contano più dei thread); preferire un singolo processo ottimizzato + numpy vettoriale
  quando possibile. Niente hyperthreading per BFS con dict > 1 GB.
- Run > 10 min: SEMPRE log append-only con timestamp + (per i BFS) checkpoint su disco, così la
  run è riprendibile e monitorabile. Per le search a semi riproducibili basta loggare il rngstate.
- Ogni port C/numba di codice Python validato va rivalidato con i self-test PRIMA dell'uso.

## 5. Self-test (PRIMA di tutto, fermarsi al primo rosso)
1. `python code\window_automaton.py --selftest` (r=1: 15 stati, h=0.8114, 1 rotore; r=2: 403, 3 rotori).
2. `python code\product_automaton.py --selftest` (4/4 verde: m=0≡base; orbita reale costo invariante;
   frame canonico≡assoluto; 252/252 fantasmi bloccati; non richiede `build/r*_delta_cycle.txt`).
3. `alpha1\alpha1_engine.exe`: vuota→onset 9977; (7,−7)→106258; highway densità morso 22/104.
4. Cross-check r=3/r=4 coi `results/radius*_summary.json` prima di ogni nuova analisi a finestra.

## 6. Obiettivo strategico (perché questo task)
Teorema della Finestra (MORSO §40–40.1): ogni orbita eterna legge infinitamente spesso celle
nere fuori dalla finestra di memoria (2r+1)×(2r+1), con tasso ≥ δ_r (δ₁=3/5, δ₂=1/7), salvo
cavalcate finite (≤4 periodi) di rotori espliciti tutti uccisi da B–T/γ. La domanda a cui
r=4,5 rispondono: la stretta sui rotori resta monotona e B–T/γ-uccidibile a ogni raggio?
**AGGIORNAMENTO ALPHA1 §57:** la formulazione di α1 come *pavimento del tasso di morso fresco*
("modo DC del morso", #24) è stata **misurata ed erode** (densità→0, stalli ~lineari in T fino a
3·10⁵, anche nel caos puro). NON è l'invariante giusto. L'handle sano è il tasso di **non-località
δ_r** (lettura nera fuori-finestra), che NON è legato alla densità globale di morso ed è già un
teorema per r≤4. **AGGIORNAMENTO §58:** sulle 24 orbite lunghe il tasso nero fuori-finestra r=4
ha mediana 0.2334/passo e tail/core mediano 1.06; i minimi mobili sono ancora 9x/16x/27.4x
`delta4_auto` per L=313/1040/10400, mentre il morso fresco ha finestre a zero. **AGGIORNAMENTO
§59:** il ponte diretto debito profondo -> lock e' falso nel predittore locale: hazard `D>=40`
cala coi quantili deep-black e cresce coi quantili fresh-bite. **AGGIORNAMENTO §60:** la griglia
2D conferma che bite e' l'innesco: effetto `D>=40` mediano +0.1373 entro strisce deep, mentre
deep resta -0.0350 entro strisce bite. **AGGIORNAMENTO §61:** il ponte locale lock -> checklist
e' confermato: 891/891 gate-lock pre-onset muoiono esattamente alla prima lettura esogena cattiva
e 24/24 onset veri passano il controllo positivo. **AGGIORNAMENTO §62:** la checklist viene
quasi ricampionata localmente: 810 tentativi porta unici, 24 OK, 786 KO, riuso della cella
critica 1/762 consecutivo e tipo di errore quasi senza memoria. Prossimo fronte: vettore
checklist completo + geometria della porta. **AGGIORNAMENTO §63:** il vettore e la geometria
sono salvati: 57.177 letture esogene, mismatch mediano 6 nei fallimenti, stessa origine porta
consecutiva 0/786, L1 origine mediana 43. **AGGIORNAMENTO §64:** il modello vettoriale mantiene
la diagonale col full-vector, comprime a 37 offset / 66 componenti sul campione lungo, ma due
periodi mancano 12 KO. **AGGIORNAMENTO §65:** la lacuna non si chiude comprimendo ancora:
il troncamento corto fallisce e le celle decisive possono essere lontane. Correzione Pauli:
questo non e' ancora un teorema di non-localita' dinamica. **AGGIORNAMENTO §66:** il
`door-defect profile` sui lock e' fatto: fase reale best unica 810/810, off-phase compatibili
muoiono entro 5 letture, coda 268...1591 ritrovata. Quindi il profilo lock-condizionato non e'
l'invariante globale; §66 nomina l'asimmetria corretta: identificare la porta e' locale, decidere
il successo della porta vera e' globale. **AGGIORNAMENTO §67:** lo scanner segmentale ha falsificato
i candidati naturali `Φ_depth`/`Φ_mass`: su segmenti deep/no-entry, `Φ(next) >= Φ(prev)` avviene
in circa meta' dei casi sia su gate sia su grid. Quindi deep-black non e' decremento endpoint-monotono
di un potenziale finito basato su prima morte o massa pesata dei mismatch. **AGGIORNAMENTO §68:**
Pauli restringe il linguaggio: no-go empirico/testimoniale sui proxy scalari finiti testati, non
teorema dinamico. L'audit da CSV conferma peggioramenti stretti, non solo pareggi: gate `L=1600`
`Φ_mass_104` peggiora strettamente in **371/762** segmenti; grid `best22_mass_104` in **3149/6275**.
Addendum §68: non scrivere che la reversibilita' conserva massa; scrivere che massa/area/mismatch
sono conteggi non orientati, perche' i flip locali depositano e ripuliscono. Prossimo fronte (§69):
`Φ_compat^L`, dove `h_g^L` e' il primo offset cattivo della porta `g`, `h_best^L=max_g h_g^L`,
e `Φ_compat^L=0` se `h_best^L=L+1`, altrimenti `exp(-h_best^L/104)`. Se `Φ_compat` diventa somma di mismatch, ricade in
`best22_mass`; se resta solo endpoint `h_best`, e' gia' ferita da `Φ_best22_depth`. Questo ha
impostato §69: separare endpoint da forma event-wise/amortizzata e co-raggiungibilita' con due storie finite della formica,
localmente indistinguibili alla porta, discordi nella cella lontana. Caveat scala: `R(n)` arriva
a 40, celle decisive osservate a offset 1591. **AGGIORNAMENTO §69:** la versione endpoint e'
chiusa: `compat_endpoint_audit.py` mostra che `h_best` non migliora in **400/762** gate e
**3591/6275** grid, con peggioramenti stretti **350/762** e **2736/6275**.
**AGGIORNAMENTO §70:** il pre/post evento deep-black falsifica anche la monotonia immediata
ingenua: su **600** eventi, `h_best` non migliora in **357/600** e peggiora in **259/600**.
**AGGIORNAMENTO §71:** `alpha1/t3_coreachability_pair_scanner.py` trova un witness dinamico
co-raggiungibile a `R=8` (stesso patch locale, fase 98, discriminante rel `(15,13)` a offset
494). Questo chiude solo la lettura "esistenza/non-vacuita'"; non muove α1 e non supporta da
solo un potenziale. `R=16` zero-collisioni e' baseline di sparsita', non confine strutturale.
Prossimo fronte (§72): replay mirato del witness, equivalenza quoziente/approssimata e
closure/SAT locale per raggi maggiori.
Roadmap completa:
CHAT_HANDOVER §C.
