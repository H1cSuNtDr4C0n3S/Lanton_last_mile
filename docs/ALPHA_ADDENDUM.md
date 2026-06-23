# ADDENDUM α — Localizzazione dei lock e checklist esatte: α2 chiuso, T3 promosso a equivalenza
**Data: 10 giugno 2026 — Michael Spina + Claude. Sessione: dal programma a due lemmi (HANDOVER2) alla chiusura di α2 e di T3′.**
**Prerequisiti: HANDOVER.md §2 (convenzioni, INVARIATE), ANATOMY_ADDENDUM.md §12–17, HANDOVER2.md. Numerazione continuata: §18–25.**

## 18. Riepilogo in una frase
La localizzazione alle porte (α2) è ora un **lemma finito con dimostrazione** (bound D ≤ r(k), corollario: lunghezza ≥ 116 ⇒ porta); il Teorema della Dogana è promosso a **equivalenza esatta** (ingresso ⟺ checklist esogena giusta, confusione 250+588 / 0+0); il residuo globale è ridotto a α1 (ricorrenza) + β (non-cospirazione) + γ, e per α1 esiste ora una riformulazione puramente simbolica della congettura.

## 19. LEMMA α2 (localizzazione) — enunciato, dimostrazione, validazione

### 19.1 Definizioni esatte (convenzioni di frame)
- **Occorrenza di fase k al tempo t, lunghezza L:** turns[t:t+L] = (W0^∞ a partire dall'indice k)[0:L]. Per L ≥ 20 la fase è unica (§19.4).
- **Left-maximal:** t ≥ 1 e turns[t−1] ≠ W0[(k−1) mod 104].
- **r(k), ritardo di rivisita della soglia:** ancorata la highway in fase k con formica in pos₀, heading h₀, sia c₋₁(k) = pos₀ − dir(h₀) (frame relativo: (0,1)). r(k) = min{o ≥ 0 : la cella occupata dall'orbita all'offset o è c₋₁(k)}. r(k) = ∞ ⟺ k ∈ Φ_ent (Teorema della Soglia, §12).

### 19.2 Lemma α2
*Sia turns[t:t+L] un'occorrenza left-maximal di fase k, t ≥ 1, in un'orbita qualunque (qualunque configurazione iniziale, anche infinita). Allora L ≤ r(k).*

**Dimostrazione.**
(i) *Identità di frame.* Le svolte determinano la traiettoria relativa: poiché turns[t:t+L] coincide con la parola della highway in fase k, le posizioni e gli heading dell'orbita per i primi L passi, nel frame (pos(t), h(t)), coincidono con quelli dell'orbita-highway di fase k.
(ii) *La cella del peccato è la soglia.* La formica si muove DOPO la svolta, quindi pos(t−1) = pos(t) − dir(h(t)) = c₋₁(k) nel frame.
(iii) *Il peccato fissa il colore.* turns[t−1] ≠ W0[k−1] ⟺ la lettura a t−1 è opposta a quella che la highway compie alla sua visita di fase k−1 della stessa cella ⟺ il colore lasciato a t−1 è l'opposto del colore post-visita della highway.
(iv) *Morte alla prima rivisita.* Per definizione di r(k), l'orbita della finestra non tocca c₋₁(k) ad alcun offset < r(k); il colore peccaminoso persiste. All'offset r(k) il certificato richiede la lettura del colore post-visita della highway (alternanza); la finestra legge l'opposto ⇒ svolta opposta ⇒ mismatch all'offset r(k) ⇒ L ≤ r(k). ∎

**Caso escluso:** t = 0 (finestra all'inizio dell'orbita: nessun peccato; la soglia può avere il colore giusto per condizione iniziale, e il bound non vale). Irrilevante per il programma (al più un'occorrenza per orbita).

### 19.3 Corollario di localizzazione
R* := max{r(k) : k ∉ Φ_ent} = **115** (fase 69; poi 73, 74, 95, 96 a 107).
*Ogni occorrenza left-maximal di lunghezza ≥ 116 inizia in una delle 22 porte.*
**ATTENZIONE (correzione di HANDOVER2):** "ritardi 3–91" valeva per il solo segmento muto 1–12. Le cinque fasi mute con r(k) > 104 (69, 73–74, 95–96) sono tutte nelle zone K=2 {69–80, 95–99}: la loro soglia viene rivisitata solo nel secondo periodo (lookback > P). Una fase muta può quindi sostenere una cavalcata di oltre un periodo intero. La costante del corollario è 116, non 92.

### 19.4 Orizzonte di ambiguità delle fasi
max prefisso comune tra rotazioni distinte di W0^∞ = **19**. Sopra L = 19 l'attribuzione di fase è unica; sotto è ambigua. Conseguenza metodologica: ogni statistica di fase su lock con D < 20 è mal definita.

### 19.5 Tabella completa r(k) (82 fasi mute; per Lean: 104 verifiche finite, Jmax invariato)
1:19, 2:7, 3:7, 4:3, 5:3, 6:75, 7:27, 8:27, 9:91, 10:11, 11:7, 12:7, 13:3, 14:3, 15:11, 17:7, 18:7, 19:3, 20:3, 22:79, 23:79, 27:3, 28:3, 29:87, 32:7, 33:3, 34:3, 35:7, 36:67, 37:3, 38:3, 39:67, 40:75, 41:63, 42:63, 43:39, 44:7, 45:3, 46:3, 47:7, 48:59, 49:3, 50:3, 51:27, 52:27, 53:55, 54:11, 55:3, 56:3, 57:91, 58:79, 59:7, 60:3, 61:3, 62:7, 63:91, 64:3, 65:3, 66:43, 67:43, 68:79, 69:115, 70:3, 71:3, 73:107, 74:107, 75:15, 76:11, 77:11, 78:7, 79:7, 80:3, 81:3, 82:15, 84:11, 85:11, 86:7, 87:7, 88:3, 89:3, 95:107, 96:107.

### 19.6 Validazione numerica (250 run baseline, ~200.000 occorrenze left-maximal con L ≥ 10, estrazione PER-ALLINEAMENTO)
- **Violazioni di L ≤ r(k): 0 su 82 fasi mute.**
- **Saturazione esatta del bound (max osservato = r(k)): 61/82 fasi.** Il bound è teso: il lock più profondo muore di norma esattamente allo sportello della soglia.
- Max osservato fasi mute: 78 (fase 23, r=79). Max osservato porte: 165 (porta 0).
- File: `alpha2_death.py` → `alpha2_death.pkl`.

## 20. T3′ — IL TEOREMA DELLA DOGANA PROMOSSO A EQUIVALENZA ESATTA

### 20.1 Schedule esogeno E(k)
Ancorata la highway in fase k, per offset o crescente: la lettura all'offset o è **esogena** se la cella non è stata visitata ad alcun offset precedente entro la finestra (prime-visite entro finestra: unifica dogane con lookback > offset, celle di corpo lette presto, e depositi vergini). E(k) = {(o, cella relativa, colore richiesto)} dove il colore richiesto è quello del campo della highway a quella lettura.

**Struttura universale (calcolata per tutte le 22 porte, `gate_checklists.pkl`):**
- Periodo 1: 38–52 letture esogene (38–40 per le porte degli archi bassi; 48–52 per le porte del corridoio 83–94, che rileggono più corpo vecchio).
- Periodo 2: le 22 vergini **+ 0–2 celle ritardate extra, esattamente per le porte adiacenti alle zone K=2**: 72 → (offset 112, cella (2,0), nera); 97 → (105, (−1,2), nera), (106, (−1,1), nera); 98 → (104, (2,2), nera), (105, (1,2), nera); 99 → (104, (−2,2), nera).
- Periodo ≥ 3 (e ≥ 2 per tutte le altre): SOLO i 22 depositi vergini (bianco richiesto) ⇒ automatici fuori dal supporto dei detriti.
**L'orizzonte esogeno non banale è esattamente 2 periodi**; oltre, resta la sola traccia di frontiera fino all'uscita dal bounding box dei detriti (finita, perché drift ≠ 0).

### 20.2 Teorema T3′ (equivalenza)
*Per un'orbita da configurazione finita e t ≥ 1: turns[t:] = parola eterna di fase k ⟺ il campo al tempo t, letto attraverso il frame (pos(t), h(t)) sulle posizioni di E(k), coincide con i colori richiesti (con le vergini oltre il bounding box automatiche). L'onset è il minimo t siffatto, e in tale t la finestra è left-maximal (minimalità ⇒ peccato).* 
**Dimostrazione (schema).** (⟸) Induzione sull'offset: se tutte le letture esogene sono giuste, ogni lettura è giusta — le endogene per induzione (una cella prima-visitata all'offset o₁ < o viene lasciata dalla cavalcata con lo stesso colore della highway, perché letture e flip coincidono fino a o); quindi ogni svolta coincide, per sempre. (⟹) banale. Finitezza del predicato: oltre il bounding box dei detriti il campo è bianco e il richiesto è bianco (vergini). Tre ingredienti Lean: induzione endogena, certificato E(k) (finito), uscita delle vergini dal box (bound tipo Jmax).

### 20.3 Validazione: confusione esattamente diagonale
250 run baseline, 838 finestre (lock per-allineamento left-maximal con D ≥ 40 alle porte, campionati ≤ 8/run, + tutti gli ingressi veri), checklist valutata READ-ONLY sullo snapshot all'apertura della finestra (60 periodi di schedule precomputati, troncamento al bounding box):
- pred SI / reale SI: **250** — pred NO / reale NO: **588** — falsi positivi: **0** — falsi negativi: **0**.
- **P(ingresso | checklist OK) = 1.0000; P(ingresso | checklist ¬OK) = 0.0000.**
- Porte rappresentate: 17/22 (anche le fantasma 26, 91, 92 producono lock; nessun loro ingresso nel campione, coerente con peso ~0).
- Lo 0.918 del §16 è spiegato e superato: era la checklist troncata alle 5 dogane tardive. Il residuo 8.2% stava nelle prime-visite di P1 a offset > 40 e nelle celle extra di P2.
- File: `checklist_final.py` → `checklist_final.pkl`; tassonomia: `gate_taxonomy.py` → `gate_checklists.pkl`.

### 20.4 Tassonomia delle morti (validazione della compressione §16d come legge esatta)
**748/748 morti osservate alle porte (lock D ≥ 30) cadono su offset di E(k); zero su letture endogene.** Spettri di morte per porta (top): porta 0 → offset 99, 77, 98, 45, 71 (dogane + frontiera); porta 103 → 45, 46, 99; porta 102 → 100; porta 100 → 102. Le morti tardive delle porte 97–103 si concentrano sugli offset ~99–105 = gli sportelli profondi della zona K=2 nel loro frame — il collo di bottiglia della fase 98 (§15e) generalizza a tutta la famiglia.

## 21. Catena locale completa (stato finale, tutta finita e Lean-abile)
- **T1 (highway):** certificato 104·K + induzione per shift.
- **T2 (soglia):** k ∈ Φ_ent (22 porte) ⟺ r(k) = ∞, check finito (Jmax ≤ 7).
- **α2 (localizzazione):** occorrenza left-maximal di lunghezza ≥ 116 ⇒ porta. [QUESTO ADDENDUM]
- **T3′ (equivalenza):** parola eterna da t ⟺ checklist esogena E(k) giusta al tempo t. [QUESTO ADDENDUM]
Residuo globale: **α1** (ogni orbita eterna non-W produce occorrenze left-maximal profonde ricorrentemente — con α2, automaticamente alle porte) ∧ **β** (la checklist agli istanti di lock non può restare eternamente sbagliata) ∧ **γ** (esclusione di altre asintotiche) ⇒ congettura.

## 22. Risultati collaterali della sessione (probe su α1)

### 22.1 Stazionarietà forward del tasso di lock (trappola §14B evitata al secondo tentativo)
150 run lunghe (onset > 30k), finestre di tempo ASSOLUTO, censura ultimi 5000 pre-onset:
- D≥40: 1.27e-3 → plateau ~7.0–7.4e-4 dopo burn-in ~20k passi (il transiente giovane locka di più: coerente con la fase 0 bocca dei transienti corti).
- D≥56: ~2.1e-4 → ~1.2–1.5e-4; D≥80: piatto ~2e-5 entro il rumore.
- **Nessun decadimento verso zero.** Gap inter-lock: q99/μ = 5.1–5.4 (esponenziale: 4.61), coda lievemente pesante (mistura di tassi), max gap 41.621 (d=56).
- FALSIFICATO il primo probe ("tasso crescente nella seconda metà della run"): era survivorship — i lock profondi predicono l'ingresso, condizionare alla fine li arricchisce. Stesso identico errore di ρ(m), autocatturato.
- Uniformità tra famiglie (baseline / densa 0.6–0.9 / sparsa grande): tassi entro fattore ~3, code simili.
- File: `alpha_gaps.py` → `alpha_gaps.pkl`; `alpha_stationarity.py` → `alpha_long_meta.pkl`.

### 22.2 La localizzazione è emergente nella profondità (ora superata da α2, resta come misura)
Frazione di lock in Φ_ent: 0.22 a D≥40 (= base rate 22/104), 0.66–0.69 a D≥56, 0.89–0.99 a D≥80. α2 spiega il meccanismo: le fasi mute muoiono entro r(k).

### 22.3 La misura dei lock superficiali non è grammatica pura
Probabilità Markov-8 del fattore di lunghezza 40 per fase: rank 1 = fase 36; ma l'arricchimento dinamico osservato non segue il ranking grammaticale (la fase 0 è rank 64 per grammatica e tra le dominanti osservate). L'arricchimento configurazionale oltre la grammatica è presente già a profondità 40. (Nota: le statistiche di fase pooled di questo probe sono parzialmente artefatte, §23; il fatto qualitativo regge.)

### 22.4 Riformulazione simbolica della congettura (il linguaggio della formica)
- **Caratterizzazione esatta della realizzabilità:** una parola di svolte determina il cammino; è realizzabile ⟺ le letture successive di ogni cella si alternano (prima lettura libera = colore iniziale arbitrario). Poiché lo stato al tempo t di una configurazione finita è una configurazione finita, **linguaggio dei fattori = linguaggio delle parole giocabili da zero**.
- Parole proibite a L=5: {R⁵, L⁵, LRRRL, RLLLR} (chiuse per complemento = riflessione). Conteggi esatti realizzabili L=5…16: 28, 50, 88, 154, 448, 1300, 3680, 10412. Entropia ≈ 0.75–0.81 bit/simbolo: sotto-shift proprio.
- **Il censimento empirico dei transienti SATURA il linguaggio esatto fino a L=12** (conteggi identici): a piccola scala il transiente è pieno sul sotto-shift; tutta la struttura del "quando" vive nella misura, non nel supporto.
- **Forma simbolica della congettura:** sia L_∞ = {parole infinite di svolte: (i) letture alternate su ogni cella, (ii) solo finitamente molte prime-visite leggono nero}. Congettura ⟺ ogni w ∈ L_∞ è definitivamente una rotazione di W0^∞. La condizione (ii) è il sostituto simbolico della finitezza della configurazione — il candidato ponte per α1 al posto della nucleazione di bordo (morta, §14A): tensione combinatoria tra "infinite prime-visite bianche (R forzate)", parole proibite, ed evitamento eterno dei fattori lunghi di W0.
- File: `alpha_grammar.py` (Markov-8 + censimento; censimento esatto inline).

## 23. Trappole nuove (cumulative con HANDOVER.md §7 e HANDOVER2 §4)
- **La left-maximalità pooled (D[t−1] ≠ D[t]+1 sul massimo tra allineamenti) è ROTTA:** l'estrazione dei lock va fatta per-allineamento. Le "fasi dominanti 40/41" e le "fasi 29 a D≥80" dei probe pooled erano artefatti di tie-breaking.
- Ogni attribuzione di fase con D < 20 è ambigua (orizzonte 19).
- Non condizionare il tasso di lock alla posizione nella run (survivorship): finestre di tempo assoluto + censura pre-onset.
- Il censimento del linguaggio empirico va fatto PER-RUN: la concatenazione inietta finestre spurie ai bordi (R⁵ "vista" per contaminazione).
- "Ritardi 3–91" (HANDOVER2 §1.3) vale per il segmento 1–12, NON è il max globale: R* = 115. La costante di localizzazione è 116.
- La validazione diagonale di T3′ è su famiglia baseline: il teorema non dipende dalla misura, ma la diagonale va replicata su famiglie avverse prima del verbale definitivo del programma. [FATTO: §25]
- **L'orizzonte della checklist NON è 2 periodi + margine fisso:** è il bounding box dei detriti, che nelle configurazioni con corpi-highway preesistenti (perturbazioni) raggiunge centinaia di periodi. Implementazioni con schedule troncato (es. 60 periodi) producono falsi positivi su quei regimi. Lo schedule va precomputato a ≥ (diam(bbox)/2) periodi (qui: 1200).

## 24. Domande aperte aggiornate (priorità)
1. **Lean del pacchetto a quattro** (T1, T2, α2, T3′). Nuovi ingredienti finiti: tabella r(k) certificata (104 check), identità di frame (lemma di determinismo già implicito in T2), induzione endogena di T3′, uscita delle vergini dal box. α2 e T3′ riusano l'infrastruttura di T2.
2. **α1, fronte linguistico:** formalizzare L_∞; primo bersaglio finito: esiste L tale che ogni parola di L_∞ con un suffisso privo di fattori-W0 di lunghezza ≥ 116 viola (i) o (ii)? Anche solo bound quantitativi (densità minima di occorrenze profonde) sarebbero il primo risultato di ricorrenza.
3. **β esteso:** replicare la caccia all'anti-teorema su tutte le porte con le checklist universali ora disponibili (stato congiunto della checklist, mod 8/16, invarianti di storia) + famiglie avverse costruite per ingannare la checklist.
4. **Diagonale su famiglie avverse** (costo: minuti) — chiude la trappola §23 ultima.
5. **Misura delle porte fantasma:** 26, 91, 92 producono lock (3, 2, 1 nel campione) ma mai ingressi — il bacino backward minuscolo ora è misurabile come P(checklist OK | lock alla porta) per porta: la teoria quantitativa del ranking è a portata.
6. **(c) arricchimento dinamico:** ora con l'oggetto esatto (lock valido = lock + checklist), la statistica P_dyn/P_Markov-8 in funzione della profondità è la teoria del tempo d'ingresso.

## 25. STRESS-TEST AVVERSO: i quattro teoremi locali sono misura-indipendenti

### 25.1 Protocollo
8 famiglie: sparsa grande (20–30, 0.05–0.20), densa (20–30, 0.60–0.90), box grande (30–40, 0.25–0.55), formica fuori centro + heading casuale, due rettangoli disgiunti, perturbazioni della highway (stato a N0+60P + 1 flip entro raggio 10), testimoni 26/72/91 disturbati (1–3 flip raggio 12), testimoni costruiti per 83/94 + disturbati. Estrazione lock per-allineamento, esclusione t=0, checklist completa E(k) con orizzonte 1200 periodi (valutatore vettorizzato), matrice predetto/osservato.

### 25.2 Risultati complessivi (~660 run, ~2.100 finestre valutate)
| criterio | esito |
|---|---|
| violazioni α2 (fasi mute, tutte le famiglie) | **0** |
| morti su offset endogeni | **0 / 2.275** |
| T3′: ingressi predetti / reali | **662 / 662** |
| T3′: near-miss predetti / reali | **1.438 / 1.438** |
| falsi positivi / falsi negativi | **0 / 0** |
| porte con finestre valutate | **22/22** |
| porte con ingressi osservati e predetti | 0, 24, 25, 30, 31, 83, 93, 94, 97, 98, 99, 100, 102, 103 (+ quelle delle sessioni precedenti) |

I testimoni puri costruiti per 83 e 94 (costruzione T2: certificato K=1 + soglia peccaminosa + formica in (0,1)) danno onset=1 con fase corretta, e la checklist li predice.

### 25.3 La scoperta collaterale: i mega-near-miss (fisica delle collisioni di bracci)
Nella famiglia delle perturbazioni esistono cavalcate left-maximal di **440+ periodi (L fino a ~46.000) che muoiono**: la formica costruisce un braccio-highway genuino per oltre 1.250 celle di territorio vergine e si schianta sul blob di detriti originale, esattamente sulla prima lettura esogena nera del suo schedule di frontiera. Autopsia di un esemplare: lock a (−1026,−778), morte a (−137,109), distanza 1.256 ≈ 441 × |drift|, patch alla morte = corpo denso del blob. Tre fatti teorici:
1. **T3′ regge anche qui:** la cella della collisione era nera e leggibile al lock — il verdetto era scritto 441 periodi prima. La diagonale include questi esemplari.
2. Il "max bulk D = 175" del §15 era una proprietà della misura baseline, non un limite dinamico: la profondità dei near-miss è illimitata al crescere della scala dei detriti.
3. Per α1/β: il tempo tra lock e verdetto può essere macroscopico, ma resta read-only al lock — la struttura di rinnovo (lock → verdetto già scritto) è invariante di scala.

### 25.4 Dichiarazione
**I quattro teoremi locali (T1, T2, α2, T3′) sono misura-indipendenti entro stress-test avversi su 8 famiglie, con copertura completa delle 22 porte. La congettura residua è α1 ∧ β ∧ γ.**

## 26. Frase di stato dell'arte
*Il locale è chiuso: le porte sono 22 (T2), nessuna cavalcata fuori porta supera 115 passi perché la colpa rientra sempre nel futuro causale (α2), e alla porta il verdetto è una checklist finita di celle lette una volta sola, che decide l'ingresso senza eccezioni in entrambe le direzioni (T3′). La congettura è ora interamente concentrata in tre enunciati globali: bussare è inevitabile (α1), il caso non ha complici (β), e non esistono altre eternità (γ).*

## 27. Inventario file di questa sessione (in ant_pkg/)
- `alpha_gaps.py` → `alpha_gaps.pkl` (3 famiglie × 300 run: tassi, gap, code)
- `alpha_stationarity.py` → `alpha_long_meta.pkl` (150 run lunghe: stazionarietà forward, fasi pooled, gap censurati)
- `alpha_grammar.py` (Markov-8 per fase; censimento linguaggio; il check esatto di realizzabilità è inline, 10 righe: cammino + alternanza)
- `alpha2_death.py` → `alpha2_death.pkl` (orizzonte ambiguità, bound r(k), morti per fase, violazioni=0)
- `gate_taxonomy.py` → `gate_checklists.pkl` (schedule esogeni 3 periodi × 22 porte; validazione 748/748)
- `checklist_final.py` → `checklist_final.pkl` (schedule 60 periodi; confusione 250/588/0/0 baseline)
- `adv_core2.py` (stress-test: valutatore checklist vettorizzato a 1200 periodi, analisi per-allineamento vettorizzata) → `adv_part1.pkl`, `adv_part2.pkl`, `adv_rare.pkl` (§25; adv_core.py = v1 deprecata, orizzonte 60)
- fronte α1 (§28): enumerazione/entropia e morsi inline; `k1_exhaustive.pkl` (6561 difetti singoli)
Tempi: tutto in secondi tranne checklist_final (~110 s) e le famiglie dello stress-test (~20–30 s ciascuna; precompute schedule ~25 s).

## 28. APERTURA DEL FRONTE α1 (stesso giorno, dopo il sigillo del bordo)

### 28.1 Il cancello falsificazionista: l'alternanza da sola non può dare α1
- **Testimone analitico:** (RL)^∞ ha cammino auto-evitante (scala diagonale, zero rivisite) ⇒ alternanza-consistente per vuoto; il massimo fattore alternante di W0^∞ è **5** ⇒ (RL)^∞ evita tutti i fattori di W0 di lunghezza ≥ 6 per sempre; ogni sua realizzazione richiede infinite prime-visite nere ⇒ viola (ii). 
- **Quantificazione (enumerazione esatta, DFS con undo):** R(n) realizzabili = 1300, 10412, 81498, 226538, 630112 per n=12,16,20,22,24; evitanti i fattori di W0 di lunghezza ≥ 16: A(24)=612544. Entropia: 0.738 → **0.734** bit/simbolo. Evitare la highway costa al sotto-shift 0.004 bit.
- **Verdetto:** nessun argomento di solo sotto-shift/entropia può dare α1; tutto il peso è sulla condizione (ii).

### 28.2 Teorema di struttura: L_∞ è numerabile (il problema non è entropico)
In una parola di L_∞ ogni lettura è determinata: prima visita ⇒ bianca (R) salvo le k celle-difetto (nere, L); rivisita ⇒ alternanza forzata. La parola è quindi l'unico punto fisso della ricorsione cammino↔letture dato l'insieme finito dei difetti: **L_∞ ↔ configurazioni finite, biiettivamente (a meno di celle mai visitate) ⇒ L_∞ numerabile.** Un insieme numerabile è invisibile a qualunque argomento entropico o di misura: la dimostrazione di α1 deve attraversare la dinamica. Formulazione a difetti: la parola della griglia vuota è la soluzione di vuoto; i k difetti la perturbazione ⇒ programma di induzione su k.

### 28.3 Caso base k=1: verificato esaustivamente
Box 81×81 (tutte le 6561 posizioni del difetto singolo, heading 0): **6561/6561 entrano**, zero fasi non-porta. 4930 invisibili (onset=9977). Spettro porte: 0 (5680), 99 (256), 24 (191), 103, 102, 25, 100, 97, 98, 30, 93, 16, 31, 101. **Record: difetto (7,−7) ⇒ onset 106.258** — il transiente più lungo noto da configurazione minima. Onestà sulla portata: il box è certificato; k=1 completo (tutto Z²) si riduce a "i flip sul tubo lontano si riagganciano" (empiricamente 100%, §5 anatomia + cardine), MA la riduzione a casi finiti per shift-periodicità richiede un bound sulle escursioni di riparazione che i mega-bracci (§25.3) negano a priori. k=1 completo NON è ancora finito. File: `k1_exhaustive.pkl`.

### 28.4 LEMMA DEL MORSO (frontiera ≤ 4) — la falsificazione dell'autosimilarità e ciò che la sostituisce
**Lemma.** In qualunque orbita, un run massimale di letture fresche-bianche ha lunghezza ≤ 4. (Fresca-bianca ⇒ R; quattro R consecutive chiudono il ciclo di 4 celle e riportano la formica sulla prima, flippata ⇒ la quinta lettura è rivisita.) In L_∞ vale definitivamente (fresche-nere finite).
- Empirico (200 run, ~700k passi): run di freschezza mediana 3, max **4 esatto** — il bound è teso.
- **Le escursioni vergini non esistono:** la formica non cammina nel vergine, lo morde (≤ 4 celle) rimasticando celle vecchie tra un morso e l'altro. L'ipotesi "escursione profonda ⇒ attrazione della griglia vuota" è falsificata nella forma letterale.
- Il campo di battaglia di α1, riformulato: un'orbita eterna deve consumare infinita frontiera (B–T) attraverso morsi R ≤ 4 immersi nella grammatica delle rivisite — dove alternanza e passato vincolano. La highway consuma con morsi ≤ 3 (raffiche F: 6 triple + 4 singole, 22/periodo, frazione 0.212); il transiente a 0.145.
- Hazard di lock(D≥40 entro 312) vs frazione fresca (ultimi 104 passi): 0.25 → 0.36–0.38, debole e con plateau. La freschezza aiuta poco: il gate resta configurazionale.

### 28.5 Domande aperte del fronte (per la prossima sessione)
1. Grammatica dei morsi: classificare i contesti di rivisita tra morsi consecutivi; un'orbita eterna che evita i fattori di W0 lunghi che vincoli ha sul suo flusso di morsi? (La highway è l'unico consumatore periodico noto: esistono altri schemi di consumo eterno compatibili con l'alternanza + (ii)? Collegamento diretto con γ.)
2. Induzione sui difetti: k=2 esaustivo su box ridotto (coppie di celle, quoziente per simmetria) — il primo caso dove i difetti interagiscono.
3. Bound sulle escursioni di riparazione per chiudere k=1 completo (collega α1 al §25.3).
4. Bilancio di frontiera: per B–T l'orbita eterna ha infiniti morsi; il tasso di morso (0.145 transiente, 0.212 highway) è limitato inferiormente? Un'orbita può avere tasso di morso → 0? (Se sì come, se no perché: candidato primo lemma quantitativo del fronte.)
