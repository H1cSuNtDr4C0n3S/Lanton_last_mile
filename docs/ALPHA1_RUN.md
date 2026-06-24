# ALPHA1_RUN — sweep Ryzen per il test gap/Fabry di α1 (consegna sessione gap-staircase)

**Bersaglio.** Rimuovere il bias di selezione del risultato sandbox e decidere, su orbite
T≳10⁶–10⁷, se gli **stalli di morso** (run consecutivi senza fresca-bianca) sono
*uniformemente limitati* (α1 forte) o crescono indefinitamente (solo α1 long-window di #24).

**Convenzione.** Identica a `code/libant.c` (validata: griglia vuota → onset 9977; highway
densità morso 22/104). morso = lettura **fresca-bianca** (come `morso_census.py`).

## File (in questa cartella)
- `alpha1_engine.c` — motore C self-contained. Modi: `search` (cerca semi a onset alto,
  shardabile, semi riproducibili dal solo stato RNG a 64 bit), `dump`/`reseed` (dump
  completo dei tempi di morso di un'orbita).
- `alpha1_within.py` — **il test che conta**: statistiche *dentro una singola orbita*
  (running max-stall vs t; pavimento del tasso su finestre L). numpy only.
- Risultato sandbox da battere: max-stall del core ~ T^0.73 (R²0.88), densità ~ T^−0.20
  (R²0.89), su T≤10⁵ — ma confuso dalla selezione per lunghezza.

## Build (Strawberry gcc)
```
gcc -O3 -o alpha1_engine.exe alpha1_engine.c
```

## 1) Caccia ai semi lunghi (CPU-bound puro → 14–15 shard `start /low`, §4 CLAUDE.md)
Semi multi-cella casuali; tieni gli onset più alti. Esempio per shard k di 15:
```
for /L %k in (0,1,14) do start /low cmd /c ^
  "alpha1_engine.exe search %k 15 20000000 8000000 5 25 > onsets_shard%k.txt"
```
- `20000000` semi per shard, cap `8000000` passi, lati patch 5..25.
- I conteggi non devono sommarsi a nulla di noto (è una ricerca), ma **gli shard sono
  disgiunti per RNG**: nessun seme duplicato fra shard.
- Unisci e ordina: `sort /R /+1 ...` oppure in Python. Tieni i top ~50 per onset.
- **Checkpoint**: ridireziona già su file (append-only); ogni shard è ripartibile cambiando
  il range di semi (aggiungi un offset al loop se riprendi).

## 2) Dump delle orbite lunghe
Per ogni `rngstate` nei top-K:
```
alpha1_engine.exe reseed 20000000 <rngstate> 5 25 > dump_<id>.txt
```
(Il cap 20M ≥ onset garantisce di catturare tutto il transiente + coda highway.)

## 3) Il test decisivo (bias rimosso)
```
python alpha1_within.py dump_*.txt
```
Leggi, per le orbite con T≳10⁶:
- **running max-stall**: se SATURA (non sale più nell'ultimo 30%) ⇒ stalli limitati
  *dentro* l'orbita ⇒ α1-forte sopravvive al test non-distorto.
  Se CONTINUA A SALIRE ⇒ nessun limite uniforme (sandbox a T≤10⁵: saliva sempre).
- **pavimento a finestra L=10400**: se resta staccato da 0 e stabile al crescere di t,
  regge la forma long-window/liminf di #24; se → 0, anche quella cede.

## Trappole (oltre §56.6 e CLAUDE.md §1)
- **(selezione per lunghezza)** confrontare orbite di T diverso è distorto (onset alto ⇒
  dinamica affamata ⇒ densità bassa/stalli lunghi quasi per definizione). Il verdetto si
  legge SOLO *dentro* una singola orbita lunga (alpha1_within), non fra semi diversi.
- **(controfattuale eterno)** l'orbita eterna non-highway non esiste in questa famiglia:
  ogni cosa converge. Anche "max-stall saturante a T=10⁷" è **evidenza**, non prova: α1
  quantifica su orbite eterne non istanziabili. Questo muro non si buca con la simulazione.
- **(cap < onset)** se `reseed`/`dump` esce con `periodic=0` o onset = cap, il cap è troppo
  basso: rialza maxSteps. Onset reali in questa famiglia possono superare 10⁶.

## Cosa riportare nel verbale (§57, stile addenda)
Tabella: id, T, densità, running-max-stall finale (in periodi), "sale ancora? S/N",
pavimento L∈{1040,3120,10400}. Più: il running-max-stall(t) plottato per la 2–3 orbite più
lunghe. Conclusione netta su quale FORMA di α1 (uniforme vs long-window) regge a T~10⁶–10⁷.
