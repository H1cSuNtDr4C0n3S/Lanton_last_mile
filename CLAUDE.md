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
- Verbali: si continua la numerazione dei paragrafi degli addenda (prossimo: **§86**).
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
  (j) **bordo-scarta nell'onset detection** (ENTRY-SEED §76.6): bocciare la rilevazione dell'onset
      quando la formica tocca il bordo della griglia scarta un ingresso GIA' avvenuto — la highway
      drifta all'infinito e spinge la formica fuori dal box ~22k passi dopo l'aggancio. Sintomo
      letale: 0% di ingressi per semi piccoli (falso). Antidoto: rilevare l'onset sui turni
      raccolti fino al bordo; il bordo limita la coda, non invalida l'aggancio.
  (k–m) vedi CHAT_HANDOVER §77/§78 (srotolare-germe, late-entry, spaziale-limitato != stato).
  (n) **deficit di consumo = pavimento-del-morso travestito** (CONSUMPTION-LEDGER §79): ogni
      lemma "consumo deep-black > rigenerazione da supporto finito" e' FALSO — le creazioni di
      nero (letture bianche, alimentate dalla frontiera B-T) sono >= distruzioni; il pool di nero
      CRESCE. Non riaprire bilancio/squilibrio di tasso del consumo (= pavimento-del-morso §57).
      La leva, se esiste, e' la coda lunga dei ritorni lontani (age >> periodo), non il bilancio.
  (o) **nessun classificatore finito-stato a raggio fisso sugli eventi deep-black** (DEEP-MOTIF
      §80, ESTESA §81): l'alfabeto dei motivi locali co-moving al detrito NON satura (r=3 ~99,4%
      unici; scoperta ultimo/primo 1,14; unione/somma tra orbite 0,979; intersezione 19/1,5M).
      §81: vale ANCHE potando il motivo alla parte causalmente attiva (celle visitate nei prossimi
      104/208 passi): scoperta 0,811, ~57% unici, unione cresce. Non riaprire checklist/
      footprint-finito/classe-co-moving SUL LATO-ALPHA, pieno o potato: finito-stato funziona
      solo sul lato-beta (porta, §78). Il lato-alpha e' irriducibilmente dinamico.
  (p) **il nucleo universale non e' un manico** (DEEP-MOTIF-PRUNED §81): esiste un vocabolario di
      1.572 motivi attivi condiviso da tutte le 24 orbite con massa eventi stazionaria ~35,6%
      (quintili piatti, ortogonale all'eta'), ma la coda aperiodica porta ~64% della massa ed e'
      la parte illimitata. Non costruire argomenti finito-stato sul nucleo sperando che la coda
      sia trascurabile: il nucleo e' un vincolo/impronta da rispettare, non una riduzione.
  (q) **il taglio nucleo/coda non segmenta la dinamica** (CORE-TAIL-PROFILE §82): la massa sul
      vocabolario universale e' invariante nel tempo (§81), per eta' e per alimentazione (§82:
      bucket eta' piatti 35–36% fino ad age>104000; morso-fed 36,9% vs recycle 35,4%). NON
      cercare la parte genuinamente aperiodica come sottopopolazione separabile di eventi (per
      eta', vc, o membership al vocabolario): la miscela e' omogenea, l'aperiodicita' abita la
      stessa popolazione che parla il dialetto universale.
  (r) **il nucleo non e' linguaggio di transito** (HIGHWAY-LANGUAGE §83): L_hw (linguaggio potato
      delle letture nere sulla highway pura) = 46 parole esatte, sature, identiche su 24/24
      orbite, ma sovrapposizione col nucleo 2/1.572 e massa deep-black pre-onset su L_hw 0,05%.
      A (r=3, H=104) caos profondo e transito sono linguisticamente disgiunti: NON costruire
      ponti alpha->beta su sovrapposizioni di vocabolario locale.
  (s) **il nucleo non ha antenati periodici noti — e (q) ha confini** (ROTOR-LANGUAGE §84):
      highway 0,05% (§83), rotori 4,5% degli eventi-nucleo con l'unica classe in eccesso (p15,
      x1,9) a massa-nucleo 0% esatto su 24/24 orbite; LRRRR evitato totalmente (0 su ~1,5M vs
      ~0,18% di caso); rotori r>=2 assenti dal caos anche alla baseline. La periodicita' di
      svolta E' il primo asse che segmenta la miscela nucleo/coda (delimita (q), che resta
      valida per eta'/vc), ma su classi minuscole: fatto strutturale, non leva quantitativa.
      Metodo obbligatorio per confronti simili: >=3 periodi pieni + baseline nulla condizionata.
  (t) **assW e' gratis** (LRRRR-HALO §85): nei certificati via automa finestra, sopravvissuti i
      cui archi di assunzione sono solo assW (bianco = default dello spazio vuoto) sono un
      campanello di REALIZZABILITA', non indizio di fantasma. Ispezionare i sopravvissuti e
      tentare il testimone diretto prima di scalare il raggio (qui: nero isolato ⇒ (LRRRR)^3,
      teorema-finestra falso ma ridotto al TEOREMA HALO ⟺ esatto: 9 celle bianche, r<=2).

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
  **COMPAT-EVENT/CO-RAGGIUNGIBILITA' (§70-§74), GA-GATE-ZERO (§75), ENTRY-SEED-FRONTIER (§76), ROTOR-STALL (§77), GATE-ONE-COMOVING (§78), CONSUMPTION-LEDGER (§79), DEEP-MOTIF-SATURATION (§80)**.
  La numerazione § è globale e continua.
- `alpha1/` — **sonde α1/β via distribuzione dei valori (§57), non-localita' r=4 (§58),
  hazard debito->lock (§59), modello 2D deep/bite (§60), lock->checklist T3' (§61),
  hazard/mixing checklist (§62), vettore/geometria checklist (§63), modello/compressione
  vettoriale checklist (§64), ridirezione non-locale/globale con correzione Pauli (§65),
  profilo 22-porte lock-condizionato (§66), scanner dei potenziali segmentali (§67),
  audit/no-go endpoint-monotono (§68), `Φ_compat` endpoint (§69), `Φ_compat` event-wise
  + schema T3'/co-raggiungibilita' (§70), scanner di coppie co-raggiungibili T3' (§71),
  profilo `L∞` discriminante-vs-profondita' (§72), pass-rate classi co-moving T3' (§73),
  e gate rango GF(2) sulle dogane (§74).**
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
  `door_discriminant_linf_profile.py` registra §72: sui **786** fallimenti T3' reali
  (`horizon=1600`), `depth == first_bad_offset` in 786/786. Nel frame grezzo il discriminante
  cresce fino a `L∞=36`, ma nel frame co-moving W0, sottraendo
  `floor(offset/104) * drift_phase`, collassa a `L∞<=9` (131 classi osservate).
  Conclusione operativa a §72: non costruire `door_debt_graph.py` su classi grezze
  `(phase, rel_x, rel_y, required_color)`; se mai, solo nel frame intrinseco W0. §74 ha poi
  potato il debt graph come prossimo passo automatico. Link 1 resta separato e non risolto.
  `door_comoving_class_passrate.py` registra §73: sulle 131 classi co-moving di prima morte,
  rigioca **810** tentativi e **101387** letture target; **91657** pass, **9730** fail,
  pass-rate **0.9040**. **130/131** classi hanno almeno un pass e sono miste pass/fail;
  l'unica zero-pass ha supporto 4. La top class `(0,-5,-2,0)` fa **4224 pass / 486 fail**.
  Link 3 non e' falsificato; il motore deve essere GF(2) globale, non riuso assoluto cella.
  `door_gf2_rank_gate.py` registra §74: sulle matrici GF(2) delle letture target, fase 0
  pre-onset `offset<=1600` ha **304** tentativi, **187** colonne, rango **138** (nullita'
  **49**) con `C0=0` **0.9963** e senza colonne costanti/duplicate. Fase 0 depth `80+`,
  prefisso `offset<=103`, ha rango **4/19**. Lettura corretta: il deficit shallow e' reale ma
  troppo debole per forzare ingresso; i deficit profondi sono sample-limited o quasi-W0/circolari.
  §74 pota la via GF(2) shallow; prossimo passo = Link 1 non-simulativo o consolidamento.
- `GA_stress_agent/` — stress-test §75 del piano GA/no-entry. `ga_gate_zero_audit.py` mostra
  che il prototipo `A0(r,K,D0)` NON determina T3': due anchor replayabili della stessa orbita
  collassano nello stesso stato astratto per `r<=8`, `K=80`, `D0=80`, fase 98, ma hanno
  prefisso T3' diverso (`h_512=513` vs `494`; `h_1600=1014` vs `494`). A `r=9` il patch si
  distingue. Lo stress-test sintattico separa anche due campi con stesso `A0(8,80,80)` e
  discriminante T3' a offset 138, rel `(3,9)`. Lettura: non classificare SCC no-entry finche'
  T3' non e' funzione dello stato, oppure gli stati `unknown` restano tali.
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
- `entry_seed/` — **mappatura della bocca (§76): mappa inversa + germi minimi + frontiere Q1/Q2.**
  `reverse.py` (mappa diretta/inversa sparsa, self-test round-trip 12000 passi -> griglia vuota),
  `clib.py` (loader autosufficiente di `code/libant.c`), `germ.py` (germe minimo per fase via
  troncamento raggio + greedy; out `germs_22.json`, min globale 13 celle fasi 0/103, onset 0),
  `brute.c` (ricerca forward semi minimi, reset-touched, fix bordo-scarta §76.6-j),
  `make_summary.py` (+ `seed_frontier.json`: Q1 b=1->onset 310 ... b=5->62, b=13->0; Q2 b=2->dist 0),
  `figura.py` (+ `frontiera_semi.png`).
  **§77 (rotor-stall):** `stall_geometry.py` (+ `stall_geometry.json`, `stall_footprint.png`) —
  geometria degli stalli del morso su `(7,-7)`: area-filling, molteplicita' ~1.57, bbox~len^0.767;
  la formica e' un rotor-router walk (cella = rotore a 2 stati), ma NON abeliano (uscita dipende
  dall'heading). `abelian_test.py` (escape 303/1109/1/1135 per heading) + `escape_scaling.py`
  (prova di viabilita': esponente di fuga deriva oltre 1.5, bite-stall limitato ~303 = quantita'
  diversa da #30 ⇒ strada non-abeliana NON priorita'). Livello morso, non α1. Dettaglio:
  `docs/ROTOR_STALL_ADDENDUM.md`.

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
5. (se si tocca la bocca/§76) `python entry_seed/reverse.py`: forward Python == motore C 12000 passi,
   round-trip esatto -> griglia vuota + (0,0,0). Verifica reversibilita' e convenzioni della dinamica.

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
**AGGIORNAMENTO §72:** `alpha1/door_discriminant_linf_profile.py` misura i 786 fallimenti T3'
reali: nessuna duplicazione fisica, `depth=first_bad_offset` sempre. La crescita grezza
`L∞=36` era drift del tubo W0: nel frame co-moving fase-dipendente il supporto collassa a
`L∞<=9`, con 131 classi osservate.
**AGGIORNAMENTO §73:** `alpha1/door_comoving_class_passrate.py` misura i pass-rate delle stesse
classi: 810 tentativi, 101387 letture target, pass-rate 0.9040; 130/131 classi hanno almeno un
pass e sono miste pass/fail. La top class `(0,-5,-2,0)` fa 4224 pass / 486 fail.
**AGGIORNAMENTO §74:** `alpha1/door_gf2_rank_gate.py` misura il rango GF(2): fase 0 all
pre-onset `offset<=1600` ha rango 138/187 (nullita' 49), C0=0 0.9963, senza colonne banali;
fase 0 depth `80+`, prefisso `<=103`, ha rango 4/19. Interpretazione aggiornata: dipendenze
shallow reali ma troppo deboli per UNSAT, deficit profondi sample-limited o circolari. Questo
impostava il fronte §75: Link 1 non-simulativo/consolidamento, non `door_debt_graph.py`
automatico.
**AGGIORNAMENTO §75:** stress-test GA/no-entry gate-zero: `A0(r,K,D0)` e' sound come
sovra-approssimazione, ma cieco rispetto a T3'. Con `r<=8`, `K=80`, `D0=80`, fase 98, due
storie replayabili della stessa orbita collassano nello stesso stato astratto e hanno prefisso
T3' diverso (`h_512=513` vs `494`). Stop corretto: niente classificazione SCC su `A0`; prossimo
fronte (§76) = definire `A1` con T3' deterministico/proof object, oppure propagare `unknown`.
**AGGIORNAMENTO §78:** kernel co-moving della porta `A1`: il verdetto no-entry e' funzione di uno
stato finito co-moving (footprint 44 celle, raggio strutturale rho<=9) + budget temporale `P=15`;
unknown-free a `P>=15` su 2014 attempt, oltre = `unknown` (vuoto sul campione, NON
dimostrabile-vuoto = Link 1). `delta_r` (morsi) e `A1` (porta) sono due certificati beta
COMPLEMENTARI, non un singolo automa-finestra a raggio 9.
**AGGIORNAMENTO §79:** ledger di consumo (SCOUT; simulatore indipendente validato su onset 9977 +
W0 + alternanza 0/106000). Sul transiente (7,-7) la forma ingenua del lemma di consumo e' FALSA:
creazioni di nero (~0.556/passo) > distruzioni (~0.443/passo), pool che cresce, inflow di frontiera
(B-T) ~4:1 sul consumo deep, rigenerazione dominantemente locale (eta' mediana 8). Stessa morte del
pavimento-del-morso (§57). L'ostruzione vive nella coda lunga (age>1040, max 4068) = §77 rotore
non-abeliano. Deficit-di-consumo chiuso (trappola n); oggetto vero = grafo causale di rigenerazione
ristretto alla coda lunga. Dettaglio: docs/CONSUMPTION_LEDGER_ADDENDUM.md.
**AGGIORNAMENTO §80:** positive gate (§79.6) eseguito sul Ryzen (24 orbite reali, 16 core, 22s): MORTO.
L'alfabeto dei motivi locali co-moving agli eventi deep-black non satura (r=3 ~99,4% eventi unici;
scoperta nuovi-motivi ultimo20%/primo20%=1,14; pooled unione/somma=0,979; intersezione 19/1,5M). Il
lato-alpha (detrito) NON e' finito-stato — opposto al lato-beta/porta (§78, footprint 44 / P<=15). Tre
falsificazioni in fila (deep->W0 §59, deficit §79, alfabeto finito §80): il crux di Link1 e'
irriducibilmente dinamico (coerente §28.2). Trappola (o). Dettaglio: docs/DEEP_MOTIF_SATURATION_ADDENDUM.md.
Roadmap completa:
CHAT_HANDOVER §C.
