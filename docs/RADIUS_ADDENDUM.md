# ADDENDUM RAGGI — Automa a finestra r=3,4: Teorema della Finestra a 9×9, δ₃ e δ₄ esatti
**Data: 12 giugno 2026 — prima sessione sul PC di Michael (Ryzen 7 5800X), Claude Code.**
**Prerequisiti: MORSO_ADDENDUM §39–40.1, CHAT_HANDOVER §B.2–C. Numerazione continuata: §45–53.**

## 45. Riepilogo in una frase
Il Teorema della Finestra si estende alla finestra 9×9 (r=4, 27,3 milioni di stati): l'entropia del sottografo senza-assumiB è ancora **0**, la parte ricorrente è un'unione di **66.913 rotori deterministici** con sole **3 parole cicliche distinte, tutte uccise da B–T** (nessuna richiede il γ-checker) — e la quantificazione è ora **esatta e certificata a ogni raggio: δ₁ = 3/5, δ₂ = 1/7, δ₃ = 1/64, δ₄ = 2/313**, ciascuna con ciclo testimone esplicito e lower bound da fixpoint intero.

## 46. Pipeline C (perché e come; tutto rivalidato)
Il BFS Python muore a r=4 ma non dove ce lo aspettavamo: arriva quasi in fondo (27,2M stati, 6,3 GB di RSS, ~8,5 min), è la fase di analisi (dict di adiacenze + etichette per arco in Python puro) che avrebbe sforato i 16 GB della macchina. Port:
- `code/window_build.c` — BFS con semantica IDENTICA a `build()` (mappe mapR/mapL, flip del centro PRIMA della trasformazione, celle uscite = ignote, ordine di scoperta FIFO): stati impacchettati a 2 bit/cella (21 B a r=4), hash FNV-1a open addressing; archi e outdeg in streaming su disco. **r=4 in 20 secondi, ~1,5 GB.**
- `code/analyze_radius.py` — analisi memory-lean: src ricostruito da outdeg (`repeat`), entropia = stessa power iteration di `entropy()` ma su CSR scipy (early-stop a λ stabile; 185 iterazioni a r=4), SCC col Tarjan compilato di scipy (`connected_components(connection='strong')`), rotori estratti raggruppando i soli nodi ricorrenti con un argsort.
- **Validazione:** `--selftest` riproduce r=1,2,3 all'identico (stati, archi, conteggi per tipo, entropie, numero e taglie delle SCC, parole, verdetti) contro i summary certificati; il cross-check r=3 (45.971 stati, h=0.7441, 1 rotore p=15) era già passato col codice Python originale su questo PC.

## 47. Risultati r=4 (finestra 9×9)
| r | stati | archi | entropia piena | senza-assumiB | SCC ric. | parole distinte |
|---|---|---|---|---|---|---|
| 1 | 15 | 26 | 0.8114 | 0 | 1 | 1 |
| 2 | 403 | 554 | 0.7594 | 0 | 8 | 3 |
| 3 | 45.971 | 59.508 | 0.7441 | 0 | 1 | 1 |
| 4 | **27.297.183** | 34.406.140 | **0.7367** | **0** | **66.913** | **3** |

(crescita stati ×27, ×114, ×594; entropia piena ↘ 0.734 = entropia esatta del realizzabile; archi r=4: 20.188.226 forzati, 7.108.957 assumiW, 7.108.957 assumiB)

**Cicli espliciti C₄ (canonici) e verdetti** — tutti confermati indipendentemente dal γ-checker (`gamma_enum check`):
- p=10 `LLRRLLRRRR` — rot=+2 ≢ 0 mod 4 ⇒ limitato ⇒ **B–T** (7 SCC)
- p=20 `(LLRRLLRRRR)²` — rot=+4, **drift=(0,0)** ⇒ limitato ⇒ **B–T** (66.905 SCC: quasi tutta la massa ricorrente è traslati di questa parola)
- p=74 `LLLLRLLLLRLRRRRLRRRRLLLLRLRRRRLRRRRLLLLRLLRRRRLLRLRRRRLRRRRLLLLRLRRRRLRRRR` — rot=+10 ≢ 0 mod 4 ⇒ **B–T** (1 SCC; contiene fattori del vecchio rotore p=15)

**Potenze massime realizzabili:** p10 → 2, p20 → 1, p74 → 2. Le cavalcate dei rotori a r=4 durano al massimo **2 periodi** (a r≤3 erano ≤ 4).

**Fatto strutturale nuovo: C₄ ∩ C₃ = ∅.** Il rotore p=15 di r=2,3 NON è più ricorrente a 9×9 (la finestra più grande ne vede la non-chiudibilità); al suo posto compaiono p=10/20/74. La "stretta" sui rotori è monotona come FORZA dell'enunciato (ogni raggio uccide tutto), ma NON è un annidamento insiemistico delle parole.

**TEOREMA (esteso).** *Ogni orbita eterna da configurazione finita legge infinitamente spesso celle nere fuori dalla propria finestra di memoria 9×9 ⇒ infinite rivisite nere a escursione ≥ 4.* La domanda §42.1 ("la stretta resta B–T/γ-uccidibile a ogni raggio?") ha risposta **sì anche a r=4**, e per la prima volta senza nemmeno bisogno del γ-checker.

## 48. Quantificazione esatta: δ₁ = 3/5, δ₂ = 1/7, δ₃ = 1/64, δ₄ = 2/313
Il Bellman–Ford a bisezione di `--karp` è O(V·E)×30: infattibile a r=4. Sostituito da `code/min_assumeB.c`, che sfrutta un fatto strutturale **verificato a runtime, non assunto**: *il sottografo noB privato degli archi-rotore è un DAG* (tutti i cicli noB vivono nei rotori — è il Teorema stesso; il programma fa il sort topologico di Kahn e ABORTISCE se non copre tutti i nodi; a r=4: DAG confermato su 25.520.698 nodi). Un "round" = una passata di rilassamento esatto in ordine topologico (noB) + un rilassamento degli archi assumiB: i fixpoint arrivano in 3–5 round invece di ~V.

**Schema di certificazione** (la bisezione float è solo un localizzatore euristico):
1. bisezione → ciclo testimone esplicito estratto dai predecessori, con media esatta p/q (**upper bound**);
2. `verify p q` in aritmetica intera (pesi q·w − p, int64): fixpoint ⇒ nessun ciclo con media < p/q (**lower bound**). Insieme: δ_r = p/q esatto.

| r | δ_r | testimone | validazione |
|---|---|---|---|
| 1 | **3/5** = 0.6 | q=5, p=3 | = --karp Python ✓ |
| 2 | **1/7** ≈ 0.1429 | q=7, p=1 | = --karp Python ✓ |
| 3 | **1/64** = 0.015625 | q=64, p=1 | = --karp Python su questo PC (0.015625 ± 2⁻³⁰) ✓ |
| 4 | **2/313** ≈ 0.006390 | q=313, **p=2** | nuovo (bisez. 22 min + verify 4 s) |

I testimoni sono in `build/r*_delta_cycle.txt` e annotati nei summary (`min_assumeB_rate_norotor_exact`). Il testimone δ₃ (64 passi, 1 nera) cavalca il rotore p=15 pagando una sola lettura nera per richiudersi; il testimone δ₄ (313 passi, 2 nere) è un mosaico di blocchi highway-like `LLLLRLRRRRLRRRR`-simili. **r=4 è il primo raggio in cui il ciclo ottimo paga più di una nera (p=2).**

**Enunciato quantificato aggiornato:** ogni comportamento eterno che non sia una cavalcata finita (≤ 2 periodi a r=4) di un rotore esplicito legge celle nere fuori dalla finestra 9×9 con frequenza asintotica ≥ **2/313**.

## 49. r=5: NON tentato (regola di CLAUDE.md §5.5)
r=4 ha 27,3M stati > cap 2·10⁷ ⇒ stop. Estrapolando la crescita (×594 sull'ultimo passo, in accelerazione) r=5 ≳ 10¹⁰ stati: fuori scala per qualunque forza bruta su questa macchina. Per andare oltre servono potature teoriche, non hardware (v. §51.4).

## 50. Trappole nuove (cumulative, da aggiungere alla lista)
- **Estrazione per-SCC con scansioni full-array:** `flatnonzero(labels==lab)` dentro il loop sulle componenti è O(#SCC·N) — a r=4 (66.913 SCC × 27M nodi) sono ORE. Antidoto: un solo argsort dei nodi ricorrenti + split per label. (Bug reale di questa sessione, colto dal monitoraggio.)
- **La bisezione con cap basso sui round è euristica:** un fixpoint lento può venire scambiato per ciclo negativo. MAI riportare il risultato della bisezione da solo: il valore è esatto solo col doppio certificato (ciclo esplicito + fixpoint intero alla soglia). Il cap serve solo a trovare il candidato in fretta.
- **Il limite pratico del codice Python originale è r=3 su 16 GB:** il BFS regge (27M stati ≈ 6,3 GB), è l'analisi a dict che esplode. Qualunque estensione passa dai binari compatti (2 bit/cella) + scipy.
- **Niente annidamento dei rotori tra raggi:** C₄ ∩ C₃ = ∅. Mai assumere che i cicli di raggio r+1 raffinino quelli di raggio r; ogni raggio va ricalcolato e riucciso da zero.
- (igiene) `gen_rotor_edges.py`/`gen_reduced.py` replicano la semantica del `--karp` Python: si rimuovono TUTTI gli archi (s,d) la cui coppia coincide con un arco-rotore, di qualunque tipo. Cambiare questa convenzione cambia δ_r.

## 51. Domande aperte (priorità)
1. **Legge di δ_r?** 3/5, 1/7, 1/64, 2/313 ≈ 1/5²·... — i reciproci: 1.67, 7, 64, 156.5. Il decadimento rallenta (rapporti ×4.2, ×9.1, ×2.4). C'è una forma chiusa legata alle lunghezze dei rotori (5, 6/12/15, 15, 10/20/74) e alle loro potenze massime? Il salto a p=2 nel testimone δ₄ suggerisce che il regime "1 nera ogni cavalcata massimale" si rompe a r=4.
2. **Geografia dei rotori:** i 66.913 rotori sono traslati di sole 3 parole (66.905 × p20, 7 × p10, 1 × p74). Classificare le classi di traslazione (= posizioni del pattern nella finestra canonica): la multiplicità ~N^(?) del p=20 dice qualcosa sulla misura delle trappole locali?
3. **Ponte rivisite profonde → dogane** (invariato da §42.4, ora con tasso 2/313 esplicito a escursione ≥ 4).
4. **r=5 con potatura teorica:** idee candidate — quoziente per simmetria (il frame canonico fissa l'heading ma non sfrutta la chiralità), potatura delle celle non raggiungibili dal centro entro il leak, o automa "lazy" che materializza solo la parte ricorrente. Serve un'idea, non un PC più grosso.
5. **Indebolire il bisogno del γ-checker:** a r=4 B–T basta da solo. Congettura: per ogni r, ogni parola di rotore ha rot ≢ 0 mod 4 oppure drift = 0. Se dimostrata strutturalmente (dalla geometria dei rotori in finestra), il Teorema della Finestra diventa autosufficiente a ogni raggio.

## 52. Inventario file di questa sessione
- `code/window_build.c` (+ exe) — BFS C, semantica identica a `build()`; r=4 in 20 s.
- `code/analyze_radius.py` — analisi scipy con `--selftest` contro i certificati r=1,2,3.
- `code/gen_rotor_edges.py`, `code/gen_reduced.py` — archi-rotore e riduzione alla parte ciclica (r=4: 93,5% dei nodi — la riduzione aiuta poco, il guadagno vero è il DAG).
- `code/min_assumeB.c` (+ exe) — min cycle mean su DAG+B con doppio certificato; `code/finalize_deltas.py` — annotazione dei summary.
- `build/` — binari r1–r4 (pool 2bit/cella, edges, outdeg; r4 ≈ 750 MB) + testimoni `r*_delta_cycle.txt`.
- `results/radius{1..4}_summary.json` (con `min_assumeB_rate_norotor_exact`), `radius4_cycles.txt`, log delle run (`radius4_build.log` = run Python uccisa, `radius4_c.log`, `delta4_bisect.log`, `radius3_karp.log`).
- Tempi (Ryzen 5800X, single-thread): build r4 20 s; analisi r4 68 s; γ-cross-check ~0 s; bisezione δ₄ 1305 s; verify δ₄ 4 s.

## 53. Frase di stato dell'arte
*A nove per nove la finestra non perdona: ventisette milioni di modi di ricordare localmente, e tutti quelli eterni si riducono a tre giri di valzer — due spirali e un mosaico — che il piano spegne da solo, senza nemmeno scomodare il γ-checker. Chi vuole l'eternità deve pagare il nero lontano almeno due volte ogni trecentotredici passi: la memoria profonda non è più solo obbligatoria, ha una tariffa esatta.*

## 54. Aggiornamento (stessa sessione, su direttiva di Michael): autopsia del testimone δ₄ e debito sulle orbite reali
Riallineamento strategico: non inseguire r=5; il leak non è più un difetto dell'astrazione ma una **quantità conservativa da far pagare** ("tariffa"). Bersaglio: il lemma di conversione del debito (§54.3). Prima, due misure.

### 54.1 Autopsia del ciclo testimone (313 passi, 2 nere) — il miglior evasore è un FANTASMA del leak
Estrazione annotata (`min_assumeB extract` + `r4c_nodes.bin` + pool degli stati):
- **Composizione:** 212 archi forzati, 99 assumiW, 2 assumiB; rot = +57 (≢ 0 mod 4), drift = (1,−2); bounding box 10×9; **65 celle distinte in 313 passi = 79,2% di rivisite interne** (fino a 16 visite sulla stessa cella): il ciclo ritarda il pagamento con un riciclo locale intensissimo.
- **Grammatica:** 36 morsi, di cui **28 tripli** (78%) — la stessa firma highway-adiacente del transiente reale (§37); copertura W0 mediana 19, fattore W0 massimo 34/104; contiene per intero il rotore p=15 di r=3 e il p=10 di r=4, e 44/74 del p=74. È un mosaico di blocchi quasi-W0 cucito da raffiche L.
- **I due pagamenti sono meccanismi DIVERSI** (finestre 9×9 ai due istanti: 46/81 celle uguali, nessuna relazione C4): allo step 60 la cella nera (0,−4) non è mai stata visitata nel periodo (riciclo dal giro precedente); allo step 188 la cella (−2,−2) era stata visitata 4 volte NELLO STESSO periodo (ultimo allo step 120) ed era poi **uscita dalla finestra ed è stata dimenticata** — riciclo a corto raggio reso possibile solo dal leak.
- **FATTO CENTRALE: potenza massima realizzabile = 0.** La parola del testimone viola l'alternanza già alla prima ripetizione: **nessun segmento di nessuna orbita reale può leggere questa sequenza di svolte, nemmeno una volta**. Il minimo 2/313 è raggiunto solo da cammini-fantasma che il leak rende coerenti nell'automa ma il piano vieta. Conseguenze: (a) δ₄ = 2/313 resta un lower bound SANO per le orbite (direzione giusta della sovra-approssimazione); (b) il pavimento vero sulle orbite è **strettamente più alto**: nasce la grandezza bersaglio **δ₄^real = min cycle mean sui soli cicli con parola realizzabile** (richiede uno stadio-2 tipo T2/γ dentro l'ottimizzazione, non solo dopo).

### 54.2 Debito sulle orbite reali (griglia vuota, semantica di memoria ESATTA della finestra 9×9)
`orbit_debt.py` replica la memoria dell'automa (una cella è nota solo se letta e mai uscita dalla finestra da allora) sull'orbita vera; l'onset ricalcolato con questa semantica è **9977 esatto** (validazione incrociata).
- **Transiente:** 0,1775 nere profonde/passo (finestre da 1000: 0,115–0,249, nessun decadimento visibile su quest'orizzonte); **età del detrito: mediana 684 passi, quartili 168–1848, max 6848**. Il transiente paga la tariffa riciclando detrito ANTICO, ordini di grandezza oltre l'orizzonte della finestra: gli assumiB reali non sono rivisite "appena dimenticate".
- **Highway:** esattamente **16 nere profonde a periodo** (fasi fisse mod 104: 0,2,3,11,12,33,44,50,76,77,80,81,82,98,99,101,102), tasso 0,1529/passo = **24× il pavimento δ₄**; età 40–116: la highway ricicla il proprio scarico fresco, a un'età limitata dal periodo. Anche l'eternità "buona" paga — pagare non distingue la highway, è il COME si paga (età e regolarità del detrito) che la distingue.

### 54.3 Lemma di conversione del debito (bersaglio della prossima fase; formulazione di Michael)
**Lemma (da dimostrare).** *Sia un'orbita reale da configurazione finita la cui traccia nel window-automaton r=4 visita infinitamente spesso archi assumiB. Se il cammino non è definitivamente rotore né highway, allora infinitamente molti di quegli assumiB sono prime-visite nere reali.* (Versione forte: con densità positiva.)

Catena risultante: orbita eterna non-highway → (r=4) o rotore o densità assumiB ≥ 2/313 → rotori esclusi da B–T → infinite assumiB → (lemma) infinite prime-visite nere → impossibile da configurazione finita. **La congettura si riduce al lemma + caso periodico (γ).**

Munizioni da questa sessione per il lemma: (i) i minimizzatori puri del debito violano l'alternanza (54.1) — l'evasione massimale è già impossibile per le orbite, serve quantificare quanto sopra 2/313 sta il pavimento realizzabile; (ii) il riciclo eterno a corto raggio ha la firma dei rotori (uccisi); il riciclo ad ampio raggio costringe a tornare su detrito che nel frattempo... è qui che vive il lemma: il detrito si consuma (ogni rivisita flippa) e l'alternanza lo vincola.

### 54.4 Trappola nuova + inventario aggiuntivo
- **Trappola:** il min cycle mean del grafo può essere raggiunto SOLO da cicli irrealizzabili. Mai leggere il testimone come "comportamento possibile": l'enunciato sano resta "ogni cammino paga ≥ δ", MAI "esiste un'orbita che paga δ". (Istanza nuova della trappola (c) di CLAUDE.md §1.)
- File: `code/autopsy_delta4.py`, `code/orbit_debt.py`; `min_assumeB.c` esteso (modo `extract <mu>`, output annotato `r4c_delta_cycle_annot.txt`); `gen_reduced.py` esteso (`r4c_nodes.bin` = mappa id ridotti → originali). Tempi: estrazione annotata ~3 min, autopsia ~5 s, orbit_debt ~10 s.

### 54.5 Prossima sessione (ordine concordato)
1. **δ₄^real:** escludere iterativamente i cicli ottimi irrealizzabili (taglio del ciclo trovato → ri-bisezione → check realizzabilità) finché il testimone è realizzabile: dà il vero pavimento delle orbite a r=4 e forse il meccanismo del lemma.
2. Classificazione degli archi assumiB nelle SCC minimizzanti (geografia del pagamento).
3. Statistica del detrito su famiglie di configurazioni iniziali finite (l'età mediana ~700 è universale?).
4. Formalizzazione del debt lemma (e solo dopo, eventuale r=5 potato).
*(Eseguito nella stessa sessione: vedi §55.)*

## 55. Il minimo del sovra-automa è raggiunto fuori dal linguaggio della formica (δ^auto / δ^alt / δ^real)
Direttiva di Michael: separare formalmente **δ₄^auto = 2/313** (minimo del sovra-automa, certificato in §48), **δ₄^alt** (minimo sui cicli la cui parola periodica passa il check di alternanza globale) e **δ₄^real** (minimo sui cicli realizzabili come sottotracce di orbite da configurazione finita); calcolare δ₄^alt per taglio iterativo dei fantasmi, PRIMA di δ₄^real.

### 55.1 Procedura (taglio iterativo, riprendibile)
`altmin_driver.py` + `min_assumeB extract --cuts`: estrai il ciclo minimo del grafo corrente → check di alternanza sulla parola ciclica (`first_conflict`, cap 50 potenze) → se fantasma, classifica il PRIMO conflitto (cella, offset, distanza temporale, stesso/cross-periodo) e taglia i suoi soli archi assumiB → ripeti. Tagli append-only (`build/r4c_cuts.txt`), catalogo completo in `results/delta4_alt_catalog.jsonl` (parola, tipi, archi-B, conflitto per ogni ciclo).

### 55.2 Risultato: 252 fantasmi, ZERO sopravvissuti — barriera a 7× il minimo
260 iterazioni (~3,7 h), 252 cicli distinti estratti in costo crescente da 2/313 = 0.0064 fino a **0.0455 = 7,1 × δ₄^auto = 2,9 × δ₃**: **ogni singolo ciclo viola l'alternanza globale**. Nessun ciclo alternanza-consistente esiste sotto quota ~0.0455 nella sequenza di taglio. La regione economica del grafo non è un'anomalia puntuale (il fantasma del §54.1): è un'intera regione non fisica.

**Firma dei fantasmi (252 esemplari, nessun duplicato):**
- distanza temporale del primo conflitto: min 20, mediana 64, **max 124** — SEMPRE limitata, nella fascia "appena oltre l'orizzonte della finestra": la cella esce dalla 9×9, viene dimenticata, e il ciclo la rilegge col colore comodo entro ~124 passi;
- 234/252 violano già nel primo periodo, 18 nel secondo, nessuno oltre;
- celle di conflitto ammassate intorno all'origine ((0,0): 24 casi; le 6 più frequenti tutte in ‖·‖∞ ≤ 1);
- **72/252 sono NO-B-T** (rot ≡ 0 mod 4 e drift ≠ 0): cicli che B–T non ucciderebbe e muoiono SOLO per alternanza — l'alternanza fa lavoro genuinamente nuovo, non ridondante;
- al salire della soglia i cicli si fanno barocchi (q fino a 1570, fino a 61 assumiB) ma il conflitto resta corto: l'evasione non scala.

**Onestà (limite del metodo):** il valore è il minimo del grafo TAGLIATO: ogni taglio è certificato da un fantasma esplicito, ma un ciclo consistente più economico potrebbe in principio passare per un arco tagliato. Quindi 0.0455 è una barriera *relativa alla sequenza di taglio*, non un lower bound certificato di δ₄^alt. La certificazione esaustiva ("ogni ciclo sotto ε è fantasma") è il contenuto del Lemma A.

### 55.3 Minimi reali su sliding window (la controprova empirica)
`orbit_windows.py`, griglia vuota + 3 IC random (16 nere): il MINIMO (non la media) del tasso di nere profonde su qualunque finestra reale non-highway è
| L | min nere profonde | tasso | vs δ₄^auto |
|---|---|---|---|
| 313 | 25–28 | 0.080–0.089 | 12,5–14× |
| 626 | 62–70 | 0.099–0.112 | 15,5–17,5× |
| 1000 | 114–118 | 0.114–0.118 | ~18× |
| 5000 | 815 | 0.163 | 25,5× |
Uniforme tra configurazioni iniziali e età; i minimi CRESCONO con L (nessuna finestra lunga economica). Il pavimento dinamico reale è un ordine di grandezza sopra δ₄^auto — coerente con la barriera dei fantasmi.

### 55.4 Lemma A e Lemma B (bersagli formali, formulazione di Michael)
**Lemma A (alternanza taglia i fantasmi — computazionale/certificabile).** *Ogni cammino periodico del window-automaton r=4 sotto una tariffa ε viola l'alternanza globale oppure è B–T-uccidibile.* Evidenza: 252/252 fino a ε ≈ 0.0455; i 72 NO-B-T muoiono comunque di alternanza.
**Lemma B (la memoria antica non può essere eternamente economica — il ponte dinamico).** *In un'orbita reale da configurazione finita, una sequenza infinita di assumiB profondi a tariffa bassa e senza lock W0 profondi non può essere spiegata solo come detrito antico.*

**Via di certificazione per il Lemma A suggerita dalla firma:** i conflitti hanno distanza temporale LIMITATA (≤124 ≈ piccolo multiplo del tempo di attraversamento della finestra). Un automa-prodotto con check di auto-consistenza sugli ultimi k ≈ 128 passi (memoria temporale, non spaziale) ucciderebbe ogni fantasma catalogato — il "r=5 morale" senza l'esplosione a 10¹⁰ stati. Da quantificare: crescita degli stati del prodotto e se k(ε) resta limitato al crescere di ε.

**Caveat per il passaggio alle orbite (registrato):** il min cycle mean limita il liminf di OGNI cammino infinito del grafo, ma un cammino aperiodico reale può percorrere segmenti di cicli fantasma senza mai completarne la ripetizione inconsistente. Il Lemma A sui cicli NON limita da solo le orbite aperiodiche: serve la versione "ogni cammino infinito alternanza-consistente ha liminf ≥ δ^alt" (l'oggetto giusto è l'automa-prodotto di cui sopra, dove l'alternanza a orizzonte k è interna agli stati e il min cycle mean torna a fare da bound universale).

### 55.5 Inventario e tempi
- `code/altmin_driver.py` (driver riprendibile), `min_assumeB.c` esteso (`extract <mu> [rounds] [cutsfile]`), `code/orbit_windows.py`, `code/catalog_stats.py`.
- `results/delta4_alt_catalog.jsonl` (252 fantasmi completi di parola e conflitto), `build/r4c_cuts.txt` (~600 archi-B tagliati), log `delta4_alt*.log`.
- Tempi: ~70 s/iterazione (estrazione C ~60 round su 32M archi + check Python); 2 tornate: 60 it. (57 min) + 200 it. (3 h 41).

### 55.6 Frase di stato dell'arte
*Il minimo del sovra-automa è raggiunto fuori dal linguaggio della formica: duecentocinquantadue evasori, nessuno che sappia mentire per più di centoventiquattro passi. Il leak regala crediti di memoria, ma l'alternanza è un creditore che non dimentica: chiunque provi a pagare poco viene colto in contraddizione entro un giro. La prima correzione del leak non ha bisogno della finitezza — basta la grammatica.*
