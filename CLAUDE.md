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
- Verbali: si continua la numerazione dei paragrafi degli addenda (prossimo: **§56**).
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
  (f) processi lunghi: chunking con budget temporale interno e checkpoint su disco.

## 2. Convenzioni della dinamica (INVARIATE da HANDOVER §2)
- Bianco → svolta R (orario), nero → L; la cella si inverte dopo la lettura; poi mossa di 1.
- Heading: 0=su, 1=destra, 2=giù, 3=sinistra. Lettura→svolta→flip→mossa.
- W0 = parola della highway, periodo 104 (58 R, P(R)=0.558, rot=12), drift diagonale (±2,±2).
  File: `data/W0.npy` (0/1), `data/w0.txt` (L/R). Onset griglia vuota: N0=9977.
- Parola realizzabile = compatibile con QUALCHE configurazione finita: fresche libere,
  rivisite forzate dall'alternanza. R(n) censiti fino a 40 (`data/gamma_enum.pkl`).

## 3. Mappa del progetto
- `CHAT_HANDOVER.md` — stato completo del programma e roadmap.
- `docs/` — catena degli addenda: HANDOVER, HANDOVER2, ANATOMY, ALPHA (§1–28),
  GAMMA (§29–35), MORSO (§36–44), RADIUS (§45–55), PRODOTTO (§56). La numerazione § è globale e continua.
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
- CPU-bound puro (C, sweep gamma_enum): 14–15 processi `part` con `start /low`, shard per
  prefissi di scelte libere; i conteggi dei shard DEVONO sommare esattamente ai totali noti.
- Python memory-bound (BFS automa, dict grossi): 6–8 processi max (la RAM e la cache L3
  contano più dei thread); preferire un singolo processo ottimizzato + numpy vettoriale
  quando possibile. Niente hyperthreading per BFS con dict > 1 GB.
- Run > 10 min: SEMPRE checkpoint su disco (pickle dello stato BFS ogni ~5 min) e log
  append-only con timestamp, così la run è riprendibile e monitorabile.
- Ogni port C/numba di codice Python validato va rivalidato con i self-test PRIMA dell'uso.

## 5. Task operativo immediato (in ordine, fermarsi al primo fallimento)
1. `python code\window_automaton.py --selftest` — DEVE passare
   (r=1: 15 stati, h=0.8114, 1 rotore; r=2: 403 stati, h=0.7594, 3 rotori).
2. `python code\window_automaton.py --radius 3` — cross-check con `results/radius3_summary.json`
   (45971 stati, h=0.7441, 1 rotore p=15). Poi `--radius 3 --karp` → δ₃ (stima: minuti–ore;
   se lento, vettorializzare meglio o portare il Bellman–Ford in C).
3. `--radius 4`: crescita stati 15 → 403 → 45971 (×27, ×114) ⇒ atteso ~10⁶–10⁷.
   Se il BFS Python supera ~30 min stimati: port in C/numba di `build()` mantenendo ESATTAMENTE
   la semantica (mappe mapR/mapL, flip del centro PRIMA della trasformazione, celle uscite =
   ignote) e rivalidare con --selftest. Riportare: stati, entropie, rotori+verdetti, potenze
   massime realizzabili, δ₄ se fattibile.
4. Parole cicliche marcate "DA VERIFICARE" → `gamma_enum check`.
5. Solo se r=4 < ~2·10⁷ stati: tentare r=5 con cap stati e abort esplicito.
6. Scrivere `docs/RADIUS_ADDENDUM.md` (§45+) coi risultati, nello stile degli addenda.

## 6. Obiettivo strategico (perché questo task)
Teorema della Finestra (MORSO §40–40.1): ogni orbita eterna legge infinitamente spesso celle
nere fuori dalla finestra di memoria (2r+1)×(2r+1), con tasso ≥ δ_r (δ₁=3/5, δ₂=1/7), salvo
cavalcate finite (≤4 periodi) di rotori espliciti tutti uccisi da B–T/γ. La domanda a cui
r=4,5 rispondono: la stretta sui rotori resta monotona e B–T/γ-uccidibile a ogni raggio?
Se sì, il limite è un enunciato di non-località pura — il ponte verso α1 (le rivisite nere
profonde sono dove vive il formalismo dogane/checklist). Roadmap completa: CHAT_HANDOVER §C.
