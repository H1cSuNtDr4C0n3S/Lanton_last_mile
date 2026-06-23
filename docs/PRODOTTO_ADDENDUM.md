# PRODOTTO_ADDENDUM — Automa-prodotto temporale A(r;m,D) (§56)

Catena addenda (numerazione § globale e continua): … MORSO §36–44, RADIUS §45–55, **PRODOTTO §56**.
Bersaglio di sessione: il "r=5 morale" di RADIUS §55.4 — incorporare l'auto-consistenza di
alternanza DENTRO gli stati, così che il min cycle mean torni un bound universale su TUTTI i
cammini infiniti (anche aperiodici) e δ^alt diventi certificabile con la macchina dei certificati.

## 56. Riepilogo in una frase
L'automa-prodotto A(r;m,D) (finestra 9×9 × memoria di celle uscite) è **costruito, validato
byte-per-byte e dimostrato sound**, e come *verificatore* uccide tutti i 252 fantasmi del
catalogo r=4 con poca memoria; ma come *certificatore* di δ^alt via min-cycle-mean ha rivelato
**due ostacoli indipendenti** — (a) spezza i rotori B-T e li riespone come cicli economici,
abbassando il minimo SOTTO δ^auto; (b) la memoria spaziale esplode prima di chiudere — per cui
δ^alt **non è ancora certificato**: la sessione consegna l'infrastruttura, la soundness, e la
diagnosi precisa di cosa serve (rimozione dei B-T nel prodotto + memoria temporale compatta).

## 56.1 Costruzione e semantica (code/product_automaton.py, code/product_build.c)
Stato del prodotto = (finestra canonica heading=su, celle {U,W,B,**B***}) × **M** = insieme
ordinato di ≤ m celle visitate **uscite** dalla finestra, dentro il box ‖·‖∞ ≤ D, con eviction
deterministica. Tre politiche di memoria:
- **full** (nearest): tieni le m celle più vicine (chiave (dist, x, y) nel frame canonico);
- **black-only**: ricorda SOLO celle nere (la menzogna gratuita è "nera dimenticata letta bianca");
- **ibrida** (nere-prima): tieni m celle ma le nere hanno priorità assoluta nell'eviction.

`B*` = nera nota solo via memoria: la lettura al centro è **forzata** (niente menzogna) ma
**paga 1 come assumiB** (proietta sulla semantica base). `W*` collassa su W (costo 0, stesso
successore). Quando una cella di M rientra nella finestra viene ripristinata (nera→B*, bianca→W).

**Soundness (provata + testata, self-test §56.2):** ogni orbita reale si solleva a un cammino
del prodotto coi colori ricordati veri (una cella in M non muta senza essere visitata, e
visitarla la riporta dentro la finestra). L'eviction è solo perdita d'informazione. Il costo
assumiB lungo la proiezione è **invariante in (m,D)** (B* converte assumiB, non li crea):
quindi il min cycle mean del prodotto **è un lower bound sulla tariffa di OGNI cammino infinito
auto-consistente a orizzonte (m,D)** — l'alternanza è dentro gli stati ⇒ chiude in linea di
principio il caveat aperiodico di RADIUS §55.4. (Il limite vero è §56.4–56.5.)

## 56.2 Validazione (obbligatoria, tutta verde)
- **Self-test del prodotto** (`product_automaton.py --selftest`, 4 check):
  [1] **m=0 ≡ automa base** byte-per-byte (r=1: 15 stati; r=2: 403, parole identiche);
  [2] orbita reale (3000 passi, r=2) **mai bloccata** e **costo invariante** (=558) per ogni (m,D);
  [3] frame canonico ≡ coordinate assolute (stesso step di blocco sui testimoni r1–r3);
  [4] catalogo 252 fantasmi r=4 **tutti** bloccati da A(4;32,8) nel frame canonico.
- **Builder C ≡ Python byte-per-byte** in tutte e tre le politiche (hash identici):
  full p1m2d8/p1m4d8/p2m2d8; ibrida p2m4d5h; black-only p2m1d5b/p1m2d8b.
- **Velocità**: A(2;4,5) ibrida = 17,3M stati in **12,7 s** col C (binari identici al Python che
  ci metteva ~11 min + swap). **Regola operativa: per ogni istanza non minuscola usare SOLO il
  builder C** (vedi trappola §56.6).

## 56.3 Il prodotto come VERIFICATORE del catalogo (ghost_block_analysis.py) — successo
Copertura dei 252 fantasmi (non-dup) r=4, frame canonico, tie-break canonico:

| politica | (m,D) per 0 superstiti | nota |
|---|---|---|
| full / nearest | m=32, D=8 | a m=16,D=8 restano 3 (i più profondi) |
| black-only | non raggiunge 0 a D=8 | peggiore: le nere spaziano su tutto il box |
| **ibrida (nere-prima)** | **m=24, D=8** | la più efficiente; m=16,D=8 → 1 solo superstite |

`m` minimo per fantasma (ibrida, D=8): istogramma {8:243, 16:+8, 24:+1} → la coda profonda
richiede m≈24. Conferma quantitativa della firma RADIUS §55.2: **i fantasmi mentono a corto
raggio** e una memoria modesta, *con priorità alle nere*, li copre tutti.

## 56.4 Il prodotto come CERTIFICATORE di δ^alt — due ostacoli (il risultato vero)
Testimoni del min cycle mean del prodotto (doppio certificato: ciclo + fixpoint INTERO; check
in `code/check_witnesses.py`):

| istanza | δ = p/q | rot/drift | B-T? | alternanza | gamma_enum | realizz. |
|---|---|---|---|---|---|---|
| A(1;2,8) | **1/8** = 0.125 | +4 / (0,2) | NO-B-T | OK (no conflitto) | REJECT (fresca-L) | pow 50 |
| A(1;4,8) | 2/16 = 0.125 | +8 / (0,4) | NO-B-T | OK | REJECT (fresca-L) | pow 50 |
| A(2;2,8) | 2/70 = 0.0286 | +16 / (−3,−1) | NO-B-T | **FANTASMA d=52** | REJECT (altern.) | pow 0 |
| A(2;4,8) | 2/71 = 0.0282 | +17 / (2,−3) | B-T | FANTASMA d=64 | REJECT (B-T) | pow 1 |

Confronto coi minimi base: δ₁^auto = 3/5, δ₂^auto = 1/7. **Il min del prodotto è PIÙ BASSO del
base a ogni raggio testato** (0.125 < 0.6; 0.029 < 0.143). Due cause indipendenti:

1. **Ostacolo A — i rotori spezzati riaffiorano (TRAPPOLA NUOVA).** Il min cycle mean si calcola
   rimuovendo gli archi-rotore *del grafo corrente*. Il prodotto, con la memoria, **spezza i
   rotori B-T del base** (acquistano un B* lungo il giro): a r=1 il rotore p=5 sparisce del tutto
   (0 SCC senza-pagamenti in A(1;2,8)); a r=2 sopravvive solo il p=15, spariscono p=6, p=12. Gli
   ex-rotori, non più rimossi, rientrano nel minimo come **cicli che pagano pochissimo** (1/8,
   2/70). Ma sono **B-T-uccidibili** (parola del rotore) ⇒ cavalcabili solo finitamente ⇒ NON
   contribuiscono al liminf di un'orbita. **Correzione necessaria:** nel prodotto bisogna
   rimuovere prima del min-cycle-mean *anche* tutti i cicli B-T (rot ≢ 0 mod 4 oppure drift = 0),
   non solo i rotori-prodotto. Senza questo passo il minimo grezzo è privo di significato (è
   l'istanza al prodotto della trappola (e) di CLAUDE.md §1 + RADIUS §54.4: *il minimo del grafo
   è raggiunto solo da cicli che il piano esclude*).
2. **Ostacolo B — memoria insufficiente residua.** Il testimone NO-B-T sopravvissuto a r=2
   (A(2;2,8): 2/70, **fantasma a distanza 52**) NON è ucciso da m=2: il conflitto è oltre
   l'orizzonte della memoria. Serve m≥16 (cfr. §56.3) → ma a quel punto gli stati esplodono (§56.5).

**Risultato positivo netto:** a r=1 con m≥2 il minimo NO-B-T (1/8) è **alternanza-consistente**
ma **gamma-REJECT per "fresca-L"** — prima conferma diretta, *dentro il prodotto*, della
tricotomia δ^auto < δ^alt < δ^real: l'alternanza-a-orizzonte è strettamente più debole della
realizzabilità piena, e il gap a r=1 è esattamente la regola "fresca-L stazionaria".

## 56.5 Crescita degli stati — la memoria spaziale non scala
BFS completo (builder C), D=8 salvo dove indicato:

| | m=0(base) | m=2 | m=4 | m=8 | m=16 |
|---|---|---|---|---|---|
| r=1 | 15 | 197 | 2 895 | 829 334 | **> 40M (abort)** |
| r=2 | 403 | 14 973 | 268 790 | **> 40M (abort)** | — |

A(2;4,**5**) = 17,3M già con box ridotto. **black-only esplode di più** (A(2;2,8)b = 740k vs
15k in full): le nere ricordate spaziano su tutto il box invece di addensarsi presso la finestra.
Crescita ≈ ×15–×60 per +2 di m a r piccolo ⇒ la memoria *sufficiente* (m≈16–24, §56.3) è fuori
portata come automa completo già a r=1,2, prima ancora di toccare r=4. La rappresentazione
spaziale (m,D) è ottima per *verificare* (§56.3) ma non per *certificare* esaustivamente.

## 56.6 Trappole nuove
- **(prodotto-rotori)** spezzando i rotori, il prodotto riespone cicli B-T come paganti-poco:
  il min-cycle-mean grezzo del prodotto **non è δ^alt** e può stare sotto δ^auto. Rimuovere i
  cicli B-T PRIMA del minimo (§56.4 ostacolo A).
- **(black-only esplode)** la politica che ricorda solo le nere ha PIÙ stati della full a parità
  di m (le nere spaziano sul box), controintuitivo: non è la scelta "economica".
- **(BFS Python del prodotto)** uguale alla pipeline base ma peggio: A(2;4,5) Python = 11 min +
  swap; in una campagna lasciata girare ha thrashato la macchina ~7 h senza lavoro utile. **Mai
  BFS Python del prodotto oltre poche migliaia di stati** — solo `product_build.exe`. (Memoria
  utente aggiornata.)
- **(Monitor tail -f)** i Monitor con `tail -f` non escono mai e dopo un riavvio app restano
  orfani "in esecuzione per ore": seguire i run con Read sull'output o `until grep` che ESCE.

## 56.7 Domande aperte / prossimi passi (ordine proposto)
1. **Rimozione dei B-T nel prodotto** (ostacolo A): estendere gen_rotor_edges/min_assumeB al
   prodotto rimuovendo ogni ciclo con rot ≢ 0 mod 4 o drift = 0. Solo allora il min-cycle-mean
   del prodotto è un candidato δ^alt. Verificare a r=1,2 che risalga sopra δ^auto.
2. **Memoria temporale compatta** al posto della spaziale (ostacolo B): codificare l'ultimo
   colore visto solo per le celle toccate negli ultimi k passi, indicizzate per *tempo* di uscita
   e non per posizione — l'intuizione originale di Michael (RADIUS §55.4). Misurare se la crescita
   è sub-esplosiva rispetto a (m,D); k(ε) limitato?
3. **Prodotto a r=4 con memoria minima + ibrida** accettando un δ^alt parziale, sfruttando che
   l'ibrida copre il catalogo già a m=24 (§56.3): stimare prima gli stati col cap.
4. Solo dopo 1–3: confronto con i minimi reali su sliding window (RADIUS §55.3).

## 56.8 Inventario file di questa sessione
- `code/product_automaton.py` — prototipo + analisi + `--selftest` + `compute_delta` (ciclo+verify);
  modi `--use-c`, `--black-only`, `--black-first`, `--delta`.
- `code/product_build.c` (+ .exe) — BFS C del prodotto, 3 politiche (modo 0/1/2), validato
  byte-per-byte; suffissi prefisso '' / 'b' / 'h'.
- `code/ghost_block_analysis.py` — copertura (m,D,politica) del catalogo (frame assoluto, tie-break canonico).
- `code/check_witnesses.py` — alternanza/realizzabilità/gamma dei testimoni delta del prodotto.
- `results/product_p*_summary.json` — summary per istanza; `build/p*_{edges,outdeg,tyx}.bin`,
  `build/p*_delta_cycle*.txt` (testimoni). `build_pyval/` = binari Python per la validazione hash.
- Tempi (Ryzen 5800X, single-thread): A(2;4,5) 17,3M stati build C 12,7 s; self-test prodotto < 30 s;
  delta r=1/r=2 (istanze piccole) secondi.

## 56.9 Frase di stato dell'arte
*La memoria si può mettere dentro lo stato, e la formica vera ci entra senza mai mentire — questo
è dimostrato. Ma il sovra-automa, appena gli dai un po' di memoria, fa un dispetto: rompe i suoi
stessi rotori e li traveste da cicli economici, così il minimo crolla sotto la tariffa invece di
salire. Il prodotto è già un ottimo segugio — fiuta e uccide tutti i duecentocinquantadue
evasori noti — ma per diventare giudice deve prima imparare a non contare i giri che il piano
spegne da solo, e a ricordare nel tempo invece che nello spazio. Il "r=5 morale" è in piedi;
non ha ancora la toga.*
