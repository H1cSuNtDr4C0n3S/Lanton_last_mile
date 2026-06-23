# ADDENDUM γ — Code periodiche eterne: enumerazione esaustiva, periodo minimo > 41
**Data: 11 giugno 2026 — Michael Spina + Claude. Sessione: apertura del fronte γ dopo il sigillo del bordo (ALPHA_ADDENDUM §18–28).**
**Prerequisiti: HANDOVER.md §2 (convenzioni, INVARIATE), ALPHA_ADDENDUM §22.4, §28. Numerazione continuata: §29–33.**

## 29. Riepilogo in una frase
γ ha il suo primo enunciato quantitativo: **nessuna parola di periodo ≤ 41 può essere la coda eterna del linguaggio di svolte di un'orbita da configurazione finita** — verificato per enumerazione esaustiva di 3,31 miliardi di parole realizzabili (1,65 miliardi di candidate al check completo), zero superstiti; il checker rideriva gratis la chiralità (W̄ muore alla prima raffica di frontiera) e il formalismo è lo stesso di L_∞ (§22.4), quindi tutto il pacchetto è Lean-adiacente.

## 30. Formalizzazione: coda periodica eterna ammissibile

### 30.1 Definizione
w ∈ {L,R}^p è una **coda eterna ammissibile** se w^∞ può essere il suffisso esatto del linguaggio di svolte di un'orbita da configurazione finita (cioè: esiste un'orbita e un tempo t₀ con turns[t₀:] = w^∞).

### 30.2 Tre condizioni necessarie, tutte finite
**(C1) rot(w) ≡ 0 (mod 4) e drift ≠ 0.** Se rot ≢ 0 mod 4, il drift su 2p o 4p passi si annulla algebricamente (∑ᵢ Rⁱv = 0 per R rotazione di 90° o 180°) ⇒ cammino spazialmente periodico ⇒ limitato. Idem rot ≡ 0 con drift nullo. Un cammino limitato consistente definisce un'orbita reale della formica su una configurazione (i colori = prime letture), e Bunimovich–Troubetzkoy esclude orbite limitate per qualunque configurazione. **Corollario di parità: rot(w) ≡ p (mod 2), quindi p dispari ⇒ rot dispari ⇒ mai ≡ 0 mod 4 ⇒ nessuna coda di periodo dispari, analiticamente.** L'enumerazione serve solo per p pari.

**(C2) Alternanza eterna** (= condizione (i) di L_∞): sul cammino di w^∞, le svolte alle visite successive di ogni cella si alternano. Prima svolta libera (colore pre-coda libero).

**(C3) Zero prime-visite L in regime stazionario** (= condizione (ii), finitezza della configurazione). Il cammino è esattamente periodico-con-drift: pos(t+p) = pos(t)+d per ogni t ≥ 0. I tubi di periodo j sono traslati T+(j−1)d; il pattern di freschezza del tubo j dipende solo dai j′ con (j−j′)·|d|∞ ≤ diam(T), quindi si stabilizza per j > diam/|d|∞ + 1 ≤ p+2 e da lì il conteggio di prime-visite-L per periodo è **costante**. Se > 0 ⇒ infinite prime-visite nere ⇒ la configurazione pre-coda dovrebbe essere infinita. Quindi nel regime stazionario ogni prima visita legge bianco (svolta R); le eccezioni vivono solo nella testa finita (analogo della regione di certificato R).

### 30.3 Check finito
Simulazione di w^∞ per M = 2p+10 periodi, testa libera J0 = p+4 periodi:
- alternanza verificata su tutta la finestra; ogni classe di vincolo (cella-relativa, lookback ≤ p+1 periodi) ha un rappresentante interamente nel regime stazionario entro 2p+3 ≤ M;
- prime-visite nei periodi (J0, M] devono essere R;
- eternità per induzione di shift (stesso schema di T1: lo stato della finestra attiva al periodo j+1 è il traslato di quello al periodo j).
Direzione usata: **necessità** (basta per l'esclusione γ). La sufficienza (parola ammissibile ⇒ testimone costruibile, T2-style: testa = insieme di difetti) resta da formalizzare — vacua qui, zero superstiti.

## 31. Implementazione e validazione (`gamma_enum.c`)

### 31.1 DFS con rivisita forzata
Osservazione strutturale (la stessa di §28.2): durante l'enumerazione, **il branching avviene solo alle prime visite** — la rivisita forza la svolta per alternanza. Le foglie del DFS sono esattamente le parole realizzabili R(p) del censimento §22.4/§28.1. Filtri al leaf: rot mod 4, drift ≠ 0, poi full-check con early-exit. Modo `part P K IDX` per partizionare sulle prime K scelte libere (validato: i chunk sommano esattamente al totale).

### 31.2 Batteria di validazione (tutta passata)
| test | atteso | esito |
|---|---|---|
| conteggi foglie vs censimento §28.1 (p=12,16,20,22,24) | identici | **identici** (1300, 10412, 81498, 226538, 630112) |
| W0 (p=104) | PASS | PASS (rot=12, drift diagonale ±2) |
| roll(W0,−37) | PASS | PASS |
| **W0 specchiata** | FAIL | **FAIL fresca-L al periodo 109, offset 13 = prima raffica di frontiera F** |
| (RL)^∞ | FAIL (§28.1) | FAIL fresca-L |

La chiralità (classe unica, HANDOVER §3.3) **ricade dal formalismo delle parole**: la specchiata pretende 22 prime-visite nere per periodo. Il punto esatto di morte (offset 13, prima cella di F) è la versione simbolica del "la riflessione espelle dal bacino".

## 32. TEOREMA (γ, periodi piccoli) — risultato della sessione

*Nessuna orbita della formica di Langton da configurazione iniziale finita ha un linguaggio di svolte definitivamente periodico di periodo minimo ≤ 41.*
(p dispari: esclusi dalla parità di rot, §30.2; p pari ≤ 40: enumerazione esaustiva, zero superstiti.)

### 32.1 Tabella esaustiva (p pari 2–40)
| p | realizzabili R(p) | candidate (rot0 ∧ drift≠0) | morte alternanza | morte fresca-L | superstiti |
|---|---|---|---|---|---|
| 2 | 4 | 2 | 0 | 2 | 0 |
| 4 | 16 | 6 | 0 | 6 | 0 |
| 6 | 50 | 24 | 10 | 14 | 0 |
| 8 | 154 | 70 | 24 | 46 | 0 |
| 10 | 448 | 224 | 92 | 132 | 0 |
| 12 | 1.300 | 630 | 300 | 330 | 0 |
| 14 | 3.680 | 1.838 | 996 | 842 | 0 |
| 16 | 10.412 | 5.128 | 2.842 | 2.286 | 0 |
| 18 | 29.128 | 14.544 | 8.518 | 6.026 | 0 |
| 20 | 81.498 | 40.412 | 23.936 | 16.476 | 0 |
| 22 | 226.538 | 113.212 | 69.320 | 43.892 | 0 |
| 24 | 630.112 | 313.166 | 194.980 | 118.186 | 0 |
| 26 | 1.743.968 | 871.706 | 554.530 | 317.176 | 0 |
| 28 | 4.830.046 | 2.403.460 | 1.547.214 | 856.246 | 0 |
| 30 | 13.325.634 | 6.661.480 | 4.357.486 | 2.303.994 | 0 |
| 32 | 36.787.216 | 18.322.256 | 12.099.522 | 6.222.734 | 0 |
| 34 | 101.244.706 | 50.616.546 | 33.844.004 | 16.772.542 | 0 |
| 36 | 278.801.206 | 138.952.350 | 93.683.784 | 45.268.566 | 0 |
| 38 | 765.819.108 | 382.882.508 | 260.747.960 | 122.134.548 | 0 |
| 40 | 2.104.643.014 | 1.049.468.480 | 719.792.124 | 329.676.356 | 0 |
| **Σ** | **3.308.178.238** | **1.650.668.042** | | | **0** |

Coerenza interna: alternanza + fresca-L + superstiti = candidate, esatto a ogni p.

### 32.2 Letture collaterali
- **Estensione del censimento R(p) fino a 40** (nuovi: 26–40). Entropia delle code stabilizzata: h ≈ 0,729–0,735 — coerente con lo 0,734 di §28.1, terza misura indipendente (con la p(k) empirica 2026-06-07 del vecchio fronte fa quattro, tutte concordi).
- **Anatomia delle morti:** ~68% alternanza al wrap, ~32% fresca-L (a p grandi). La condizione chirale (C3) è il filtro secondario ma è quello che porta tutto il contenuto "finitezza della configurazione": senza, sopravviverebbero le scale infinite tipo (RL)^∞.
- W0 a p=104 resta l'unica coda eterna nota; il teorema dice che **qualunque altra eternità periodica ha periodo ≥ 42** (e quella vera ha 104 — il gap 42–102 è il prossimo bersaglio di forza bruta, vedi §33).

## 33. Trappole nuove e domande aperte

### 33.1 Trappole
- Il check è di **sola necessità**: un eventuale superstite NON è automaticamente una coda eterna — richiede il secondo stadio (verifica con M esteso + costruzione del testimone T2-style). Con zero superstiti il punto è vacuo ma va ricordato se si estende p.
- La testa libera J0 = p+4 è larga (stabilizzazione reale ≤ diam/|d|∞+2): non stringerla senza ricontrollare il caso |d|∞ = 1 con tubo lungo.
- I processi in background muoiono col cleanup del sandbox: chunking con budget temporale interno (`run40.sh`), i chunk devono sommare esattamente (validato a p=12 e con identità interna a 38, 40).
- Il drift di W0 esce (−2,2) in questo frame: stessa diagonale |2|,|2| di HANDOVER §1, segno dipendente dall'orientazione degli assi — non è una discrepanza.

### 33.2 Domande aperte (priorità)
1. **Gap 42–102:** p=42 costa ~×2,75 (≈ 5,8 G foglie, ~25 min di CPU spalmabili in chunk), p=44 ~×7,6. La forza bruta arriva realisticamente a ~48–52; oltre serve **potatura teorica**: (a) bound sul tasso di morso per code ammissibili (in regime stazionario, fresche per periodo f = |T \ (T+d)| ≥ 1, tutte R; la highway ha f=22 — esiste un bound inferiore f ≥ f(p) che strozzi i periodi medi?); (b) usare il Lemma del morso (≤4) come vincolo DFS aggiuntivo sulle code (gratis: già implicito nell'alternanza? verificare se prune extra).
2. **Sufficienza + Lean:** chiudere il biimplicato (ammissibile ⟺ coda di un'orbita) con la costruzione del testimone, e formalizzare il pacchetto: parità (banale), B–T (citato), C2/C3 con induzione di shift — riusa l'infrastruttura di T1/T2.
3. **γ aperiodico:** questo teorema copre solo le asintotiche periodiche. L'aperiodicità eterna resta intoccata (ed è la parte di γ che si intreccia con α1 via L_∞).
4. **Ponte con la grammatica dei morsi (§28.5.1):** l'enumeratore con rivisita-forzata È il generatore del linguaggio dei morsi; strumentarlo per classificare i contesti di rivisita tra morsi consecutivi è una modifica da un'ora.

## 34. Inventario file di questa sessione (in ant_pkg/)
- `gamma_enum.c` — enumeratore (sweep / part / check), gcc -O3. Validazione inclusa nel modo check.
- `w0.txt`, `w0_rot37.txt`, `w0_mirror.txt`, `rl.txt` — parole di test.
- `gamma38.log`, `gamma40.log`, `run40.sh` — chunk e runner con budget.
- `gamma_enum.pkl` — tabella completa + note di validazione.
Tempi: p ≤ 36 in ~5 min totali; p=38 ~11 min (4 chunk); p=40 ~30 min (16 chunk).

## 35. Frase di stato dell'arte
*Il locale era chiuso; ora anche l'eternità ha un prezzo minimo: nessuna parola di periodo fino a 41 sa essere per sempre — o il wrap la tradisce sull'alternanza, o pretende infinite prime visite nere che nessuna configurazione finita può pagare. L'unica eternità periodica nota resta la highway, e qualunque rivale deve presentarsi con un periodo di almeno 42.*
