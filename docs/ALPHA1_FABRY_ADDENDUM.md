# ALPHA1_FABRY_ADDENDUM — α1 via teoria della distribuzione dei valori (§57)

Catena addenda (numerazione § globale e continua): … MORSO §36–44, RADIUS §45–55,
PRODOTTO §56, **ALPHA1_FABRY §57**.
Bersaglio di sessione: attaccare α1 con la teoria della distribuzione dei valori
(Nevanlinna / Carlson / Fabry) e con una grande run empirica su orbite lunghe, per
decidere se gli **stalli di morso** sono uniformemente limitati (α1-forte) o no.
Esito: **negativo netto + ridirezione strategica**. La simulazione NON può decidere α1;
la formulazione di α1 come pavimento-del-tasso-di-morso-fresco va declassata.

## 57. Riepilogo in una frase
Su orbite lunghe fino a 3·10⁵ (run Ryzen 8.44 h, 9.8·10⁸ semi), il tasso di morso
fresco-bianco **non** ha un pavimento staccato da zero — densità→0 e stalli che crescono
~linearmente con T, anche nel caos puro lontano dal lock — quindi né α1-forte né α1
long-window (#24) sono empiricamente supportate; ma poiché ogni orbita converge (l'orbita
eterna non-highway è un controfattuale), questa è **evidenza forte, non prova**, e la
lezione vera è che α1, se vera, va dimostrata con un argomento sulle orbite eterne, non
misurata su prefissi finiti — e l'handle giusto è il tasso di non-località δ_r (Teorema
della Finestra), non il tasso di morso fresco.

## 57.1 Strumento: alpha1_engine.c (alpha1/) — validato e veloce
Simulatore C self-contained con convenzione **identica a libant.c**. Tre modi:
`search` (cerca semi a onset alto, shardabile, **early-stop all'onset**, semi riproducibili
dal solo stato RNG a 64 bit), `reseed` (riproduce un seme dal suo rngstate, dump completo
dei tempi di morso), `dump` (seme esplicito da stdin). morso = lettura **fresca-bianca**
(byte-compatibile con morso_census.py).
- **Validazione (self-test):** griglia vuota → onset **9977** esatto (= N0); (7,−7) → **106258**;
  highway densità morso **22/104**. Berlekamp–Massey su highway → complessità lineare ≈102
  (razionale); su Bernoulli(0.21) → ≈n/2 (alta complessità). Discriminatore Carlson valido.
- **FIX DI EFFICIENZA DECISIVO (trappola nuova, §57.7-a):** la v1 azzerava l'INTERA hash
  (16 MB) a ogni seme; con 14 processi paralleli questo **satura la banda di memoria** →
  1.8k semi/s totali, ~8× sotto il single-core. v2 resetta **solo le celle toccate**
  (lista `touched` + reset O(celle), non O(tabella)) → **31.7k semi/s su 14 shard**, ~17×.
  Lezione: in parallelo il collo non sono i thread ma il traffico di memoria per-seme.

## 57.2 I due test (mappano sulla biforcazione convergenza vs α1)
- **Test A — Carlson / Berlekamp–Massey (lato convergenza, rigoroso ma NON è α1).**
  Bit-sequence dei morsi bₜ. Ogni transiente caotico ha complessità lineare **L = n/2 esatta**
  (massimale) ⇒ per Fatou–Pólya–Carlson, F(z)=Σ z^{τₙ} ha il **cerchio unitario come frontiera
  naturale** (non razionale); l'highway è razionale (L≈102). Dicotomia caos/highway confermata,
  ma è la convergenza riscritta, non α1.
- **Test B — gap / Fabry (il bersaglio).** Gap gₙ=τ_{n+1}−τₙ (stalli) sui transienti lunghi.
  Max-stallo vs T, densità di morso, pavimento del tasso su finestre L.

## 57.3 Run Ryzen (alpha1/) — esecuzione e raccolta
14 shard `start /low`/BelowNormal, semi multi-cella casuali (lati 5–25, densità 0.25–0.60),
cap 8·10⁶ passi, **early-stop all'onset**, soglia di stampa onset≥100k (altrimenti 100% dei
semi convergerebbe → ~15 GB di output). 8.44 h, **9.8·10⁸ semi**, **88.521 orbite** con
onset≥100k, **BEST onset 313.358** (≈3× la sandbox 106.258). La ricerca casuale fa
**plateau ~logaritmico**: 106k(6.5k semi)→181k(5.6·10⁵)→232k(1.2·10⁷)→313k(9.8·10⁸);
il 10⁶ NON si raggiunge con semi casuali — servirebbero semi strutturati (near-highway).

## 57.4 Test within-orbit (NON distorto) — il risultato vero
Confrontare orbite di T diverso è distorto (selezione per lunghezza ⇒ starvation: trappola
§57.7-b). Il verdetto si legge **dentro** una singola orbita lunga (alpha1_within.py).
Su 24 orbite (252k–313k, file dumps_all.txt):
- Max-stall arriva a **90–104 PERIODI** (a T≲25k in #24 era 8) ⇒ cresce **~linearmente con T**
  (core ~T^1.09 includendo il punto 106k).
- Running max-stall **sale ancora nell'ultimo 30%** in **16/24** orbite.
- Densità di morso scesa a **~0.05** (da ~0.078 a 106k, ~0.13 vuota).
- Pavimento a finestra: **L=1040 floor = 0 su TUTTE**; **L=10400 floor crollato a mediana
  0.006, con UNO ZERO esatto** (orbita 268891) — il pavimento a 100 periodi tocca lo 0.
- **KILL-SHOT sulla scappatoia pre-lock:** separando caos puro (primo 70%) da pre-lock
  (ultimo 30%), **tail/core = 1.13** e il core L=10400 floor tocca comunque 0 ⇒ gli stalli
  grossi **non** sono artefatto di lock, vivono nel caos genuino.

## 57.5 Nevanlinna — cosa trasferisce e cosa no (per non riaprirlo a vuoto)
- **Trasferisce il Primo Teorema Fondamentale:** lo Z-lift t = N(t)+Z(t)−1 È in forma
  T = N + m (counting + proximity); dZ/dt=82/104 È una difettività. Bilancio, quasi tautologia.
- **NON trasferisce la relazione dei difetti Σδ≤2:** richiede struttura olomorfa e *molti*
  valori; la distribuzione binaria (morde / non morde) la rende vuota.
- **Brjuno/Yoccoz/piccoli divisori** vivono nel regime a numero di rotazione irrazionale
  (quasi-periodico), che la sessione precedente ha dimostrato **vuoto** per le highway
  (censimento "scala del diavolo": insieme finito di razionali, niente continuo
  quasi-periodico, onset first-order). Nevanlinna NON resuscita la scala del diavolo.

## 57.6 Verdetto
A scale raggiungibili (3·10⁵), **né α1-forte (stalli uniformemente limitati) né α1
long-window/liminf (#24) sono empiricamente supportate**: densità→0, stalli ~lineari in T,
pavimento del tasso non staccato da 0, e tutto questo nel caos genuino (non pre-lock).
**Caveat fondamentale, non aggirabile:** l'orbita eterna non-highway è un controfattuale
(tutto converge). Misuriamo prefissi finiti selezionati per lunghezza ⇒ **evidenza forte,
NON prova**. Non dimostra α1 falsa; rimuove il supporto empirico alle forme a pavimento
costante. Corollario metodologico: **la simulazione non può decidere α1** — qualunque soglia
osservata sul finito erode. La prova di α1 (se vera) deve venire da un argomento sulle orbite
eterne.

## 57.7 Trappole nuove
- **(a) reset-hash per-seme = collo di banda di memoria.** Azzerare l'intera tabella a ogni
  seme strozza il parallelo (memoria, non thread). Resettare **solo le celle toccate**.
- **(b) survivorship temporale (selezione per lunghezza).** Onset alto ⇔ dinamica affamata
  ⇔ densità bassa/stalli lunghi quasi per definizione. Confronto cross-seme distorto: leggere
  SOLO within-orbit. È la (a) di CLAUDE.md §1 nel tempo invece che sul bordo griglia.
- **(c) controfattuale eterno.** Ogni orbita converge ⇒ nessuna soglia finita prova un
  enunciato su orbite eterne. Vale per qualunque futura misura di tasso/pavimento.
- **(d) apofenia del massimo campionario (π·10⁵).** Il "best onset" è un MASSIMO di campione,
  cresce ~log col numero di semi; non è una costante. 313.358 è passato accanto a π·10⁵ a
  *questo* N; con più semi lo supera. Nessun attrattore.

## 57.8 Domande aperte / prossimi passi (ridirezione strategica)
1. **DECLASSARE α1-come-pavimento-del-morso-fresco.** È l'handle sbagliato: misurato, erode.
   Il "modo DC del morso" (#24) non è un invariante a pavimento positivo alle scale raggiungibili.
2. **Sonda δ_r→β (timeboxed, UNA).** Il Teorema della Finestra vive su un invariante DIVERSO:
   il tasso di lettura **nera fuori-finestra ≥ δ_r** (certificato r≤4), NON legato alla densità
   globale di morso. Domanda secca: la non-località δ_r basta da sola a far scattare il lock β,
   senza pavimento globale sul morso? Misurare δ_r sulle stesse 24 orbite lunghe: tiene il
   pavimento mentre il morso-fresco affonda?
3. **Oppure consolidare.** Il locale è sigillato, γ≤40, finestra r=4, prodotto sound: scrivibile
   come contributo a sé (riduzione a α1∧β∧γ + macchina), senza chiudere il crux.
4. **NON** riformulare α1 come liminf-che-decade e rincorrere l'esponente di decadimento:
   è di nuovo simulazione su una domanda eterna (trappola §57.7-c), stesso muro con altro nome.

## 57.9 Inventario file di questa sessione (alpha1/)
- `alpha1_engine.c` (+ .exe) — simulatore C: `search`/`reseed`/`dump`, early-stop + reset-touched,
  semi riproducibili da rngstate 64-bit. Validato (9977, 106258, 22/104).
- `alpha1_within.py` — test within-orbit: running max-stall, pavimento a finestra L.
- `status.ps1` — monitor della run (procs vivi, %, hit, best onset, ETA, top-5).
- `ALPHA1_RUN.md` — istruzioni di run/parallelizzazione.
- `onsets_shard*.txt` — hit onset≥100k (88.521 righe; rngstate riproducibili).
- `dumps_all.txt` — dump completi (tempi di morso) delle 24 orbite più lunghe (252k–313k).
- `run_started.txt`, `run_manifest.txt`, `log_shard*.txt` — metadati e progress della run.
- Tempi: build engine <5 s; search 31.7k semi/s su 14 shard; reseed di un'orbita 313k <1 s.

## 57.10 Frase di stato dell'arte
*Abbiamo chiesto al morso se il suo respiro non si fermi mai troppo a lungo. La risposta, sui
prefissi più lunghi che la macchina sa fabbricare, è che il respiro si dirada — gli stalli
crescono col tempo, la densità scende verso zero, e nemmeno la finestra da cento periodi resta
sempre piena. Ma ogni orbita che sappiamo accendere prima o poi trova l'autostrada e tace: non
possiamo interrogare quella che non si ferma mai, perché non sappiamo costruirla. Quindi non è
una sentenza, è un confine: α1 non si decide guardando, si decide dimostrando. E il punto giusto
dove dimostrare non è il morso fresco che si spegne, ma la lettura nera profonda che il Teorema
della Finestra già obbliga — quella, forse, non si dirada.*
