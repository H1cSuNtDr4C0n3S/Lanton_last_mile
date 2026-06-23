# ADDENDUM MORSI — Grammatica dei morsi, legge del territorio, Teorema della Finestra
**Data: 11 giugno 2026 (seconda sessione) — Michael Spina + Claude. Fronte α1 via morsi, su indicazione strategica di Michael: "non inseguire il periodo 104, insegui la struttura che renderebbe necessario inseguirlo".**
**Prerequisiti: GAMMA_ADDENDUM §29–35, ALPHA_ADDENDUM §28. Numerazione continuata: §36–42.**

## 36. Riepilogo in una frase
Tre risultati: (1) la grammatica dei morsi del transiente è highway-adiacente a livello di blocchi (63% morsi tripli, gap concentrati su 2 e 7 = i gap della highway); (2) prima legge quantitativa del bilancio di frontiera: territorio A(t) ~ t^0.756 (R²=0.984) ⇒ **tasso di morso ~ t^(−0.244), nessun pavimento** — con digiuni osservati fino a ~3.000 passi; (3) **TEOREMA DELLA FINESTRA**: ogni orbita eterna legge infinitamente spesso celle nere fuori dalla propria finestra di memoria locale 5×5 — il primo lemma incondizionato del fronte α1, prodotto dall'automa dei morsi a raggio 2 + γ-checker + B–T.

## 37. Censimento dei morsi (tre misure)
Morso = run massimale di letture fresche-bianche (Lemma del morso: ≤ 4, riconfermato: max 4 esatto, 15 occorrenze su 49k morsi).

| misura | tasso | distribuzione lunghezze | gap dominanti |
|---|---|---|---|
| linguaggio esatto, uniforme su R(20) | 0.455 | 1: 60%, 2: 31%, 3: 8%, 4: 0.8% | 1, 2 |
| transiente dinamico (150 run baseline, non distorto) | 0.131 pooled / 0.178 per-run | **3: 63%**, 1: 28%, 2: 9% | **2, 7** |
| highway (maschera F) | 0.2115 | 6 triple + 4 singole | 2,5,6,7,11,13,27 |

**La misura dinamica è lontanissima dall'uniforme sul linguaggio e vicina alla highway:** domina il morso triplo (P(3|3)=0.727 — catene di triple) e i gap 2 e 7 sono esattamente le lunghezze-gap del ciclo. Versione a livello-blocchi della "grammatica highway-adiacente" del §14.

**Due bug catturati e corretti in corsa (→ trappole §41):** (a) pop mancante nel ramo rivisita del DFS Python (statistiche (B) della prima passata: spazzatura con rapporti interi impossibili — il sintomo che le ha tradite); (b) **survivorship da bordo griglia**: i run con onset precoce uscivano dalla griglia 1024 percorrendo la highway e venivano scartati ⇒ onset mediano apparente 43k invece di 3.3k. Fix: onset detection incrementale con stop anticipato. Tutte le statistiche (A) pre-fix erano condizionate ai transienti lunghi.

## 38. Legge del territorio (risposta empirica a §28.5.4)
Su 150 transienti puliti: corr(log n₀, tasso per-run) = **−0.941**. Il meccanismo: A(t) = celle fresche-bianche cumulative ~ t^α con **α = 0.756 (R² = 0.984)** ⇒ tasso di morso istantaneo ~ t^(−0.244). Per quartile d'età: 0.238 → 0.176 → 0.153 → 0.144.
- **Il tasso di morso non ha pavimento:** digiuni (gap inter-morso) ≥ 312 passi: 227 occorrenze; ≥ 1040: 9; max ~3.000. Il 13.9% dei passi del transiente vive dentro digiuni ≥ 312.
- Nota: α ≈ 3/4 — compatibile con crescita compatta a raggio r ~ t^(3/8) (subdiffusiva). Da verificare se α è universale tra famiglie.
- Per α1: ogni argomento di ricorrenza deve sopravvivere a intervalli di inedia macroscopici; "consumo di frontiera a tasso limitato inferiormente" è FALSO in finestra finita. La domanda giusta diventa: α < 1 può persistere per sempre? (Bilancio integrale, non puntuale.)

## 39. L'automa dei morsi (sovra-approssimazione a finestra)
Stato = finestra (2r+1)×(2r+1) attorno alla formica, frame canonico heading=su, celle ∈ {ignota, bianca, nera}; transizione = lettura→svolta→flip→mossa→ricanonicalizzazione; le celle che escono vengono dimenticate (**leak**: rientrano ignote). Il linguaggio dell'automa CONTIENE il realizzabile ⇒ ogni teorema "ogni cammino infinito fa X" si trasferisce alle orbite. Archi tipati: forzati (centro noto), assumiW / assumiB (centro ignoto).

| r | stati | entropia | esatto fino a | entropia senza-assumiB |
|---|---|---|---|---|
| 1 | 15 | 0.8114 | n = 8 | **0.0000** |
| 2 | 403 | 0.7594 | (leak oltre) | **0.0000** |
| (esatto) | — | 0.734 | — | — |

Il conteggio cammini raggio-1 coincide ESATTAMENTE con R(n) fino a n=8 (28, 50, 88, 154 ricostruiti dalla finestra 3×3), poi il leak cresce (+5.8% a n=10, +98% a n=24). L'entropia converge a 0.734 al crescere di r.

## 40. TEOREMA DELLA FINESTRA (il risultato della sessione)
**Fatto chiave (calcolato, r=1 e r=2):** il sottografo senza archi assumiB ha entropia 0 e la sua parte ricorrente è un'unione di rotori deterministici. Cicli espliciti:
- r=1: {RRRRL} (la spirale quadrata; rot=3 ≢ 0 mod 4 ⇒ limitata ⇒ B–T).
- r=2: {RRRLLR (rot=2), RRRRLRRRRLLLLRL (p dispari ⇒ rot dispari), RRRLLRRRRLLR (rot=4 ma **drift=0**, verificato col γ-checker)} — tutti a cammino limitato ⇒ tutti esclusi da Bunimovich–Troubetzkoy.

**Teorema.** *Ogni parola infinita realizzabile o usa archi assumiB infinitamente spesso, o è definitivamente periodica su uno dei cicli sopra — tutti impossibili per orbite. Quindi: ogni orbita eterna da configurazione finita legge infinitamente spesso celle nere situate fuori dalla propria finestra di memoria 5×5.* Poiché le prime-visite nere sono finite (cond. ii), segue: **ogni orbita eterna compie infinite rivisite nere profonde — ritorni su celle nere dopo un'escursione spaziale oltre raggio 2.**

Lettura: la dinamica eterna non può vivere di memoria locale; il passato vincola ricorrentemente attraverso il nero lontano. È la versione incondizionata e spaziale di ciò che le dogane dicono per le cavalcate: la memoria profonda è obbligatoria, e quindi il formalismo lock/checklist morde su ogni orbita eterna, non solo su quelle che tentano le porte. Il leak (celle dimenticate) non è più solo la trappola dell'astrazione: è esattamente l'oggetto che il teorema costringe a usare.

**Il metodo scala:** a raggio r la tricotomia produce un insieme finito esplicito di cicli C_r, ognuno uccidibile per parità/drift (B–T) o dal γ-checker. Ogni raggio in più spinge la struttura forzata più lontano.

## 41. Trappole nuove (cumulative)
- **Survivorship da bordo griglia:** simulazioni con cap di passi e bound spaziale scartano i run a onset precoce (la highway esce dalla griglia) ⇒ campione condizionato ai transienti lunghi. Sintomo: onset mediano 43k vs 3.3k reale. Antidoto: onset detection incrementale con stop, griglia dimensionata su (cap−onset_min)·|drift|/P.
- DFS Python con stack condiviso: il ramo a svolta forzata DEVE fare pop come il ramo libero. Sintomo dei dati corrotti: rapporti interi esatti tra conteggi indipendenti.
- Il leak dell'automa NON permette di imporre le condizioni di L_∞ dentro l'astrazione (ignota ≠ fresca): solo enunciati "ogni cammino fa X" si trasferiscono. Mai dedurre "esiste orbita che fa Y" dall'automa.
- "Eventualmente periodico" dal sottografo a entropia 0 richiede che le SCC ricorrenti siano rotori (nessun branching interno): verificato qui, da riverificare a ogni raggio.
- I tassi di morso di §28.4 (0.145) e di questa sessione (0.131/0.178) differiscono per peso del campione (età dei transienti): il tasso NON è una costante, dipende dall'età — confrontare solo a età fissata.

## 42. Domande aperte (priorità) e pacchetto PC
1. **Raggio 3–4 dell'automa** (stati stimati ~10⁴–10⁵): cicli C_3, C_4, entropia → 0.734, e soprattutto: il teorema si rafforza a "rivisite nere a escursione ≥ r per ogni r"? Se i cicli senza-assumiB restano tutti B–T/γ-uccidibili a ogni raggio, il limite è un enunciato di non-località pura. **→ Primo pacchetto per il PC di Michael (Ryzen 5800X)**: parallelizzazione per shard di BFS + enumerazione cicli; bloccato solo dalla lettura di C:\Langton_research\claude.md (MCP Filesystem in timeout oggi — riavviare Claude Desktop).
2. **Quantificare il teorema:** tasso minimo di rivisite nere profonde per passo? (Dalla SCC piena del grafo: ogni ciclo del grafo completo contiene almeno un arco nero — frequenza minima calcolabile per raggio.)
3. **α universale?** Stimare α su famiglie diverse (densa, sparsa, box grandi) e su finestre interne lunghe; collegare ad A(t) ~ t^(3/4) ⇔ r(t) ~ t^(3/8).
4. **Ponte morsi→dogane:** le rivisite nere profonde del teorema sono esattamente le letture a lookback spaziale che la checklist E(k) certifica alle porte. Formalizzare: ogni rivisita nera profonda apre una finestra di vincolo tipo-dogana anche FUORI dalle cavalcate?
5. k=2 esaustivo: resta in coda come controllo (invariato da §28.5.2).

## 43. Inventario file di questa sessione (in ant_pkg/)
- `morso_census.py` (+fix) → `morso_census.pkl` (versione distorta, conservata per la trappola), `morso_census_clean.pkl` (censimento pulito, 150 run)
- `morso_automaton.py` → `morso_automaton.pkl` (raggio 1: stati, conteggi vs R(n), entropie, SCC)
- analisi raggio 2 e cicli: inline (sezioni sopra); `cyc12.txt` (ciclo p=12, REJECT drift=0)
- Tempi: censimento ~3 min; automa r=1 ~10 s; r=2 ~40 s.

## 44. Frase di stato dell'arte
*Il transiente mastica frontiera con la grammatica della highway ma a un tasso che decade come una potenza della sua età, e può digiunare per migliaia di passi; eppure nessuna orbita può vivere di sola memoria locale: chi non guarda mai il nero lontano finisce in una spirale che il piano non concede. L'eternità, per la formica, è obbligata a ricordare in profondità — e lì, in quella memoria profonda, abitano le dogane.*

## 40.1 Aggiornamento (stessa sessione, più tardi): raggio 3 e quantificazione
**Raggio 3 eseguito in sandbox (45.971 stati, ~1 s):** entropia 0.7441 (→ 0.734), entropia senza-assumiB ancora 0.000000, e i superstiti si RESTRINGONO: un solo rotore, il ciclo p=15 LLLLRLRRRRLRRRR (rot=3 ⇒ limitato ⇒ B–T). **Teorema della Finestra esteso a 7×7, e la stretta è monotona: |C_1|=1, |C_2|=3, |C_3|=1.**

**Quantificazione (due ingredienti):**
1. **Potenze massime realizzabili dei rotori** (quanto a lungo un'orbita può cavalcarli): LRRRR → 3; LLRRRR → 2; (LLRRRR)² → 1; LLLLRLRRRRLRRRR → 4. Le cavalcate dei rotori sono finite e CORTE: il passaggio dal grafo ridotto al liminf di orbita usa queste costanti esplicite.
2. **Min cycle mean del peso assumiB sul grafo privato degli archi-rotore** (binary search + Bellman–Ford vettorizzato, O(V) memoria): raggio 1 → **0.600** (3 nere profonde ogni 5 passi); raggio 2 → **1/7 ≈ 0.1429**.

**Enunciato quantificato:** ogni comportamento eterno che non sia una cavalcata (finita, ≤ 4 periodi) di un rotore deve leggere celle nere fuori dalla finestra di memoria con frequenza asintotica ≥ δ_r (δ₁ = 3/5, δ₂ = 1/7; δ₃ da calcolare sul PC — Bellman–Ford a 46k stati × 30 bisezioni, primo carico per il Ryzen).

**Trappola registrata:** il min cycle mean sul grafo PIENO è banalmente 0 (i rotori hanno zero archi neri); la quantificazione ha senso solo dopo la rimozione degli archi-rotore, e il trasferimento alle orbite richiede il punto 1.
