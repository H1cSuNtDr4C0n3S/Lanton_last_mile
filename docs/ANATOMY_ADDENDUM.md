# ADDENDUM — Anatomia del ciclo 104: frontiera, misure d'ingresso, mappa-cardine
**Data: 10 giugno 2026 — Michael Spina + Claude. Sessione: anatomia delle bocche.**

## 1. La legge della frontiera (il risultato centrale)
Il ciclo depone esattamente **22 celle vergini per periodo**, in raffiche:
F = {13–15, 27–29, 32, 38, 45–47, 55–57, 60–62, 70–72, 75, 89} (10 raffiche: 6 triple, 4 singole).
**Nessuna bocca osservata è una fase di frontiera: 0 su ~5.600 eventi d'ingresso, su 4 misure indipendenti.**
- distanza ciclica bocca→frontiera: Φ 8.08 vs altre 2.64 (p=2·10⁻⁴)
- new13 (celle vergini nei prossimi 13 passi): arco A = 0.000 esatto su tutte le 8 fasi (p=0.002)
- il segmento più lungo senza frontiera è il **corridoio silenzioso, fasi 90→12** (27 passi); l'arco A vive interamente nella sua prima metà
- l'arco B (+ le nuove fasi rare 16, 30) = micro-pause tra le raffiche di costruzione

## 2. Densità: chiusura del cerchio col gradiente backward
ρ_loc (raggio 5 attorno alla formica): bocche 0.354 ± 0.045 vs altre 0.280 ± 0.051 (p=1·10⁻⁴, percentile 81%).
Il gradiente backward convergeva a ρ(m=0)=0.329 con collasso di varianza. **Il cono si densifica fino alla densità dei segmenti-corpo del ciclo, ed entra esattamente lì: dove la highway è localmente indistinguibile da un transiente denso.** La bocca non ha densità speciale come *certificato* (§3.14 handover); ha densità speciale come *contesto locale*.

## 3. Feature proposte e loro sorte (protocollo falsificazionista)
- celle nuove nei prossimi k: **confermata** (il predittore più netto, in forma binaria: frontiera sì/no)
- densità locale del corpo: **confermata** (p=1e-4)
- lookback medio sul corpo: confermata (p=3e-4, le bocche rileggono corpo più vecchio)
- apertura del corridoio davanti alla formica: **falsificata** (p=0.40)
- celle critiche davanti (frac L nei prossimi 13/26): debole/nulla (p=0.018 / p=0.56)
- K minimo come predittore di bocca: **falsificato** (zone K=2 = fasi 69–80, 95–99: 17 fasi, quasi tutte mute; ma la bocca dominante dell'auto-riparazione, la 99, È K=2)

## 4. Stress-test di Φ: il supporto è robusto, il ranking no
Sei famiglie di seed (baseline, box 20–30, densità 0.05–0.20, densità 0.60–0.90, formica fuori centro + heading casuale, due rettangoli disgiunti), 500 run ciascuna, solo fase d'onset:
- arco A: 89–93% in TUTTE le famiglie; arco B: 6–9%; spettri quasi sovrapponibili
- top-4 sempre {0, 99, 103, 102} con 0 ≈ 43–46%
- fasi nuove rare: 16, 30, 93, 97 — tutte non-frontiera, adiacenti o interne agli archi
- **zero** parole non-W in 3.000 run

**Bias scoperto nel dato storico:** il 66.7% della fase 0 in scaling.pkl è arricchito dal filtro committed della pipeline. La misura raw dà 45.0%. Meccanismo identificato: la fase 0 è la bocca dei transienti corti (onset mediano 2308 vs 3738, MW p=3·10⁻¹²); il filtro di commitment seleziona nucleazioni rapide/pulite.

## 5. Spettro di auto-riparazione (perturbazioni della highway)
2.000 flip singoli casuali (raggio 10 dalla formica, fase casuale): **100% ri-aggancio a W, zero fughe** (rafforza la classe chirale unica); 77% invisibili (onset ≤ 2P); 467 transienti veri (mediana lunghezza ~10³, max 63.682 passi da UN solo flip).
Spettro: **99 (47.1%) ≫ 102 (22.7%) ≫ 0 (17.3%)**, poi 97, 103, 93, 30. Il 90.8% cade nelle 12 bocche note.

## 6. Mappa-cardine (deterministica, 104 flip)
Per ogni fase k: flip della cella sotto la formica → deviazione simbolica garantita → fase di ri-aggancio.
Immagine: 0 (34), 99 (30), 102 (12), 97 (7), 103 (4)… 100/104 nell'unione-Φ estesa; sole aggiunte: 83, 90, 94 (corridoio o quasi). 22 flip guariscono entro 2P.
Oggetto nuovo: la mappa-cardine è il primo passo enumerabile del problema backward (preimmagini a 1 flip; estendibile a 2 flip, a flip a distanza d).

## 7. Il quadro a due regimi
- **Bocca di vuoto (fase 0):** per costruzione è la fase d'ingresso della griglia vuota. Domina i transienti corti e gli intorni puliti.
- **Bocca di corpo (fase 99, K=2):** la fase che rilegge il corpo più vecchio (certificato a 2 periodi). Domina l'auto-riparazione da contesto denso, e cresce di peso nei transienti lunghi.
Il ranking d'ingresso è proprietà della *misura*; il supporto (segmenti senza frontiera, con corridoio dominante) è proprietà della *highway*.

## 8. Riformulazione del Lemma 1 (stato dell'arte aggiornato)
*Le bocche della highway non sono un insieme di 12 fasi: sono un insieme aperto a bassa frequenza, ma **confinato con probabilità ~1 nei segmenti privi di frontiera del ciclo** — un oggetto finito e calcolabile (la maschera F delle 22 fasi vergini), indipendente dalla misura. La massa si concentra su due modi: la bocca di vuoto (fase 0) e la bocca di corpo (fase 99). L'avvicinamento è il gradiente di densificazione del cono, che converge alla densità locale dei segmenti-corpo: il transiente entra dove la highway gli somiglia.*

## 9. Domande aperte aggiornate
1. **Il segmento muto 1–12:** il corridoio silenzioso è 90→12, ma le bocche si fermano alla fase 0. Non lo spiega la distanza dalla frontiera (24 e 25 sono bocche a 2–3 passi da una raffica tripla). Che cosa zittisce 1–12? (Candidato: analisi della "cella del peccato" — la cella letta a fase k−1 — e di che cosa la sua alterazione propaga nel blocco denso in cima al mattone.)
2. **Lemma candidato: una fase di frontiera non può essere bocca.** Supporto empirico fortissimo; cercare l'argomento (la frontiera richiede campo lontano vergine esatto; un transiente per definizione no?). Attenzione: da solo è necessario, non sufficiente.
3. Atlante-cardine completo: flip a distanza d davanti alla formica, preimmagini a 2 flip → struttura ad albero del bacino backward (calcolabile).
4. Formalizzazione Lean dei certificati: invariata, ma ora includere la maschera di frontiera F come oggetto certificato (22 passi vergini per periodo, verificabile finitamente).
5. Il massimo transiente da 1 flip (63.682 passi) con ritorno certo: la "profondità di auto-riparazione" scala? Distribuzione code dei transienti di riparazione.

## 10. Nuovi file
- `anatomy.py` → `anatomy.pkl` (14 feature × 104 fasi + K minimi per tutte le fasi: 87 K=1, 17 K=2, zone {69–80, 95–99})
- `frontier.py` → `frontier.pkl` (maschera F, traiettoria del mattone)
- `stress.py` → `stress.pkl` (6 famiglie × 500)
- `perturb.py` → `perturb.pkl` (2.000 flip)
- `figure.py` → `mouths_anatomy.png` (4 pannelli: anatomia di Z104, mattone, profilo ρ_loc, confronto spettri)
Tutti i run: secondi (mappa-cardine inclusa). Convenzioni invariate (§2 handover).

## 12. TEOREMA DELLA SOGLIA (chiusura della sessione — caratterizzazione esatta)
Per minimalità dell'onset, ogni evento-bocca in fase k ha struttura forzata all'ultimo passo: la formica a N0−1 sta sulla **cella di soglia** c₋₁(k) = pos₀ − dir(h₀) (in frame relativo: sempre (0,1)) e compie la svolta opposta a W0[k−1] ⇒ lettura opposta ⇒ **colore lasciato opposto** a quello della highway sulla stessa cella.

**Teorema.** *La fase k ammette una configurazione iniziale finita con onset esattamente in fase k ⟺ c₋₁(k) non appartiene all'orbita futura della highway dalla fase k.*
- (⟹) determinismo: la parola periodica eterna forza il colore di prima-visita di ogni cella dell'orbita futura; la rivisita di c₋₁ leggerebbe il colore peccaminoso ⇒ rottura della parola. Esatto, non statistico.
- (⟸) testimone esplicito: certificato di fase k + cella di soglia col colore peccaminoso + formica in (0,1) con heading pre-peccato. Onset = 1 verificato, parola = roll(W0,−k), periodicità eterna per induzione del certificato.
- Il check di non-rivisita è **finito**: orbita del periodo j = tubo₀ + j·drift ⇒ basta j ≤ diam(tubo₀)/|drift| + 3 (Jmax ≤ 7). Tre ingredienti finiti ⇒ interamente formalizzabile in Lean.

**Verifica numerica: coincidenza perfetta.** Fasi con soglia mai rivisitata = fasi enterable per costruzione diretta = **22 fasi**:
Φ_ent = {0, 16, 21, 24, 25, 26, 30, 31, 72, 83, 90, 91, 92, 93, 94, 97, 98, 99, 100, 101, 102, 103}.
Tutte le 19 fasi osservate (seed + perturbazioni + mappa-cardine) ⊂ Φ_ent. Conseguenze:
1. **Segmento muto 1–12 risolto:** tutte le soglie lì vengono rivisitate (ritardi 3–91 passi; il blocco denso in cima al mattone ricalpesta la propria scia).
2. **"Frontiera ⇒ non-bocca" FALSIFICATA come legge esatta:** la fase 72 è di frontiera ma enterable (testimone: 20 celle nere, onset=1). Resta valida come proxy di misura (21/22 fasi di frontiera sono mute). La legge vera è la soglia.
3. **Tre bocche predette e poi costruite, mai osservate in ~5.600 eventi:** 26 (|B|=15), 72 (|B|=20), 91 (|B|=19) — testimoni in `witnesses.pkl`. Il supporto d'esistenza è esattamente 22; la misura assegna a queste tre peso ~0 (bacino backward minuscolo: nuova domanda).
4. La condizione "corpo già costruito davanti" era il proxy statistico; la condizione esatta è **orientata e retrostante**: ciò che conta non è dove va la formica, ma che non torni mai sulla cella da cui è entrata. (L'intuizione "compatibilità orientata corpo/heading" era giusta: l'orientazione entra attraverso la cella dietro la direzione d'arrivo.)

**Lemma 1 riformulato (versione soglia):** *L'insieme delle bocche è esattamente Φ_ent (22 fasi), caratterizzato dalla condizione finita di non-ritorno sulla soglia, certificabile in Lean per ogni fase. La misura d'ingresso decide solo quanto spesso ciascuna bocca viene imboccata; il supporto appartiene alla highway.*

File nuovi: `threshold.py` → `threshold.pkl` (rivisite + enterability, 104 fasi), `witnesses.pkl` (testimoni 26/72/91).

## 13. Domande aperte aggiornate (sostituiscono §9.1–9.2)
1. **Lean:** formalizzare il Teorema della Soglia (3 ingredienti finiti: certificato 104·K passi, induzione per shift, non-ritorno con Jmax≤7). Ora è IL deliverable: caratterizzazione completa, non solo certificati.
2. **La misura:** perché 26, 72, 91 hanno peso ~0? Dimensione/struttura del bacino backward per bocca (la mappa-cardine a 2 flip come stima della crescita delle preimmagini per bocca).
3. **Il problema backward resta l'unico infinito:** ogni transiente finito raggiunge una soglia di Φ_ent. Il gradiente di densificazione come Lyapunov candidato, ora con bersaglio esatto.

## 14. SONDA GLOBALE (post-Teorema della Soglia): due falsificazioni e un quadro nuovo
**(A) Nucleazione estremale: FALSIFICATA.** η = posizione normalizzata della formica nel box visitato (0=bordo, 1=centro), 300 run con traiettoria completa. All'onset η=0.322 vs null mid-transiente 0.374 (p=0.011, debole), ma frazione *sul* bordo (η<0.1): **1% all'onset vs 13% nel null** — la highway quasi mai nucleia all'estremo della regione visitata. Il meccanismo "escursione d'angolo → bocca di vuoto" è morto: l'illimitatezza (Bunimovich–Troubetzkoy) non si aggancia così. Residuo coerente col quadro a due regimi: ingressi in fase 0 più periferici (η=0.296) di quelli in fase 99 (η=0.365).

**(B) Il candidato Lyapunov densitometrico: FALSIFICATO — e la falsificazione è la scoperta.** Deriva forward E[Δρ_loc | ρ_loc] su 56.000 coppie: **mean-reverting puro** con punto fisso ≈0.33 (+0.14 sotto 0.2, −0.07 sopra 0.5, zero crossing in [0.30,0.40), deriva globale −0.00005). Nessuna rampa pre-onset: ρ_loc resta piatto ~0.36 fino all'ultimo campione e salta a 0.407 solo *all'onset*. Quindi: **il transiente vive sempre alla densità del corpo**. Il gradiente backward ρ(m) non era una dinamica di densificazione nel tempo: era geometria condizionata (survivorship) — la regione *futura-rilevante* si concentra dal perimetro sparso al nucleo all'equilibrio. La "somiglianza per densità" tra cono e bocche è in parte tautologia dell'equilibrio: ciò che è raro, e che gioca da gate, è l'appaiamento **configurazionale**, non densitometrico. Un Lyapunov vero, se esiste, vive nello spazio delle configurazioni/parole, non nella densità.

**(C) Hazard dell'ingresso: quasi-memoryless.** 2.000 onset: vita residua E[T−b | T>b] = 5.430 → 7.200 (b: 0→8.000) poi piatta; mediana/ln2 ≈ media entro il 18%; coda ~esponenziale (q99=30k, max 67k); **mix di fasi stazionario nel tempo di onset** (fase 0: 47%→37–40%, poi stabile). Dopo un burn-in, l'ingresso si comporta come hitting a tasso ~costante λ ≈ 1/6.000 per passo di un insieme bersaglio fisso, con leggera eterogeneità tra seed.

**Quadro risultante.** Forward, il transiente è un regime effettivamente stazionario (densità all'equilibrio, hazard costante, mix di fasi stazionario); l'ingresso è il tempo di hitting dell'unione dei 22 alberi backward (= linguaggio delle finestre auto-spazzate d'ingresso, enumerabile per reversibilità con biforcazione binaria sulle celle ignote). La congettura residua, in forma linguaggio-teorica: *ogni orbita da configurazione finita produce prima o poi una finestra del cono che appartiene al linguaggio backward di una delle 22 soglie.* Il tasso d'ingresso osservato (~10⁻⁴/passo) è enormemente maggiore del matching casuale (~2^−|R|): la grammatica dei detriti della formica è altamente highway-adiacente — quantificare questo arricchimento (statistica dei pre-agganci parziali di profondità d) è la via per una teoria quantitativa del *quando*, propedeutica al *perché*.

**Trappola nuova:** non usare ρ(m) come deriva forward — è condizionato al successo. Ogni candidato Lyapunov va testato come deriva forward non condizionata (protocollo del punto B).
File: `global_probe.py` → `global_probe.pkl`.

## 15. PROFONDITÀ DI PRE-AGGANCIO D(t), NEAR-MISS E CELLE DI DOGANA
**Definizione operativa (forma simbolica, maggiorante della compatibilità con gli alberi backward):** D(t) = massima L tale che turns[t:t+L] coincide con un fattore di W0^∞, su tutte le 104 rotazioni. Calcolo vettorizzato (run-length per allineamento), 800 run, doppio null (iid calibrato a P(R)=0.533; Markov ordine 8 fittato sui transienti — protocollo anti-trappola §3.7).

**(a) Coda: arricchimento genuino oltre la grammatica generica.** Il Markov-8 riproduce il bulk (mediana 10 = reale: i fattori corti sono grammatica generica, come da §3.7). Ma: P(D≥40) reale = 40× il Markov-8; oltre d≈56 il Markov-8 produce ZERO eventi mentre il reale ha P(D≥104)=7·10⁻⁵ per passo, max bulk = 175. **Il transiente cavalca la parola esatta della highway anche per >1.5 periodi senza entrare.**
**(b) Massimo corrente:** E[D*(t)] cresce +27 simboli su 16× tempo (iid prevederebbe +4.4): crescita ~log ma con pendenza 6×, firma di coda pesante ricorrente, non deriva deterministica.
**(c) Hazard: D è una vera coordinata precursore.** P(onset entro 312 | D(t)) sale monotonicamente 5% → 61% (D da <10 a 90–100). Primo sostituto reale del Lyapunov, in forma di hazard.
**(d) MA niente rampa monotona: il candidato "crescita inevitabile fino alla soglia" è falsificato nella forma letterale.** E[D(onset−m)] resta ~13–20 fino a m≈80 e POI COLLASSA a ~7–9 per m≤13: per minimalità, l'ingresso è preceduto dal peccato, che rompe la finestra. Non si entra estendendo un match: si entra attraverso un ultimo errore. Il Teorema della Soglia riappare al livello simbolico.

**(e) I near-miss hanno struttura di fase esatta (la scoperta della sezione).** 204 cavalcate profonde (D≥80, bulk, 600 run):
- iniziano al 96.6% in fasi di Φ_ent (fase 0: 121/204) — *i falsi ingressi tentano le stesse porte dei veri*;
- deragliano all'86.8% in Φ_ent, con iper-concentrazione in **fase 98: 145/204** (poi 99: 32) — quasi mai in frontiera (6.9%);
- il 100% attraversa fasi enterable senza agganciarsi: il match simbolico non basta, il gate è configurazionale.

**(f) Le celle di dogana (identificazione esatta).** Le letture del ciclo con lookback > P sono cinque: fasi 76, 77, 80 (celle (−6,0),(−5,0),(−4,0), lookback 108–116) e **fasi 98, 99 (celle (−3,1),(−2,1), lookback 108)** — esattamente i generatori delle zone K=2. Per un ingresso in fase 0: queste celle vengono scritte ~10–36 passi PRIMA dell'aggancio e rilette 76–99 passi DOPO — sono **soglie ritardate**: portano memoria pre-cavalcata dentro il futuro della cavalcata. L'ingresso vero richiede: soglia (0,1) sepolta (mai riletta, Teorema 2) + dogane superate (rilette col colore giusto). I falsi ingressi muoiono in massa allo sportello della fase 98. Questo unifica: il K=2 "anomalo" di 98/99 (§3.13) = il collo di bottiglia dinamico dell'ingresso; la dominanza della 99 nell'auto-riparazione (contesto denso supera la dogana nativamente); la dominanza della 0 nei transienti corti (contesto pulito = dogane da costruire ex novo, spesso giuste per costruzione recente).

**Riformulazione del meccanismo d'ingresso:** *entrare nella highway = bloccare la parola in una fase la cui soglia resta sepolta e le cui celle di dogana, scritte dal passato del transiente, superano le riletture profonde del ciclo. D(t) misura il primo requisito; le dogane sono il secondo. Il problema globale del hitting si decompone: ricorrenza dei pre-agganci profondi (empiricamente garantita, coda pesante) × probabilità di dogana (empiricamente ~stazionaria) — da qui l'hazard quasi-costante del §14C.*

Domande aperte aggiunte: (i) statistica congiunta (D, stato delle dogane) → modello di rinnovo completo del hazard; (ii) le dogane di TUTTE le 22 porte (qui solo fase 0); (iii) perché le dogane 76/77/80 vengono quasi sempre superate e la 98 quasi mai (geometria riga y=1 vs y=0 nel frame della porta?).
File: `depth.py` → statistiche D(t); analisi near-miss/dogane inline (sezione e).

## 16. TEOREMA DELLA DOGANA: il verdetto è scritto alla partenza
**Setup.** 500 run, 754 finestre fase-0 (lock con D≥40, oppure ingresso vero). Per ogni finestra: snapshot dello stato al momento del lock, lettura delle 5 dogane tardive nel frame della porta, confronto col colore richiesto dal certificato. Self-test del frame sull'ancora highway: OK. Colori richiesti: **tutte e cinque NERE**.

**(a) Teorema (esclusione deterministica).** Se al lock una cella a memoria ritardata ha colore sbagliato, il deragliamento al suo sportello è CERTO: per lookback > offset, l'orbita della cavalcata non la tocca prima della lettura, quindi il colore al lock è il colore letto. Dati: P(ingresso | dogana 98/99 sbagliata) = **0.000 su 430 finestre** — zero eccezioni, com'è dovuto. *Il destino della cavalcata è interamente deciso dallo stato delle dogane al momento del lock: i near-miss non falliscono, sono già falliti.*

**(b) Quasi-sufficienza.** P(ingresso | 5 dogane giuste) = **0.918** (231 finestre). Il residuo ~8% muore alle dogane precoci non ancora verificate a D=40 (offsets 43/44/50 — la lista completa delle letture ritardate del periodo 1 in fase 0 è di DIECI celle: offsets 12, 33, 43, 44, 50, 76, 77, 80, 98, 99) o ai check del periodo 2.

**(c) Ipotesi geometrica di Michael: confermata.** Tassi di correttezza nei near-miss: riga y=0 (riga della porta): 0.782 / 0.577 / 0.648; **riga y=1 (la riga della colpa, dove giace anche la soglia (0,1)): 0.520 / 0.247** — e 0.25 ≈ base rate dei detriti per il nero richiesto (ρ≈0.33): la cella (−2,1) è semplicemente *non costruita* dall'avvicinamento; le celle della riga della porta sono arricchite dalla dinamica del lock. Le dogane facili sono dentro il corpo che il lock stesso assembla; le critiche sono sul bordo retrostante, eredità nuda del rumore del transiente.

**(d) Compressione del certificato (riformulazione strutturale).** Per una cavalcata a parola bloccata, le celle prime-visitate con lookback ≤ offset sono ENDOGENE (scritte correttamente dalla cavalcata stessa). Il gate esogeno dell'ingresso si riduce a una **checklist finita read-only al momento del lock**: (i) le celle a memoria ritardata (devono avere il colore del certificato), (ii) la traccia di frontiera (le celle vergini dello schedule devono essere bianche — automatico fuori dal raggio dei detriti, quindi vincolo finito), (iii) la soglia (deve restare sepolta — Teorema 2). Non |R|=42 vincoli: ~10 + frontiera-nei-detriti + 1.

**(e) Fattorizzazione esatta dell'hazard.** P(dogana 98/99 OK tra i tentativi) = 324/754 = 0.43; tutte e cinque = 0.31; × 0.918 ≈ 0.28 = quota di tentativi che diventano ingressi (212/754 = 0.28 ✓). L'hazard quasi-memoryless del §14C è ora meccanicamente spiegato: *tasso di lock × probabilità stazionaria della checklist*.

**Forma finale del problema globale.** Il transiente produce ricorrentemente lock simbolici alle porte (coda pesante di D, §15); a ogni lock il verdetto è già scritto in una checklist finita di celle; la congettura residua è: **nessuna orbita finita può produrre per sempre lock con checklist sbagliata** (più l'esclusione di asintotiche alternative). Equivalentemente: la successione degli stati-checklist ai tempi di lock non può evitare in eterno l'evento "tutto giusto".

Domande aperte: (i) checklist complete per tutte le 22 porte (qui solo fase 0) — la mappa universale offset/lookback per fase; (ii) la dinamica della checklist tra lock consecutivi: quanto è mixing? c'è un ostacolo di parità/invarianza che potrebbe proteggerla per sempre (da escludere!)? (iii) D⁺ formale = profondità filtrata dalla checklist: hazard atteso a gradino.
File: `customs.py` → `customs.pkl`.

## 17. CACCIA ALL'ANTI-TEOREMA: la checklist non è protetta (a questa risoluzione)
**Setup.** 800 run, 648 con almeno un lock fase-0, sequenze di lock in ordine temporale entro run (fino a 12), stato della dogana critica c(−2,1) letto a ogni lock. Quattro test, quattro null.

**(1) Transizioni libere.** Tra lock consecutivi della stessa run: P(sbagliata→giusta) = 0.449, P(giusta→giusta) = 0.431, marginale 0.443 — indistinguibile da ricampionamento iid. Nessuna memoria intrappolata. (Il marginale 0.44 qui è pooled su tutti i lock; lo 0.25 del §16 era condizionato ai near-miss.)
**(2) Nessuna sovradispersione.** Lock falliti prima dell'ingresso (372 ingressi in fase 0): media 0.51, var 0.69 vs 0.77 geometrica — semmai sottodisperso; max 6 fallimenti consecutivi; nessuna coda di "run maledette".
**(3) Nessuna classe di parità/posizione/heading.** Screening su t mod 2 (la parità conservata x+y+t ≡ 0 vincola insieme tempo e posizione: testate come una), t mod 4, parità della porta, heading: chi² p = 0.38–0.92, tutti null. Unico segnale debole: P(giusta) cala col lock index (0.546 → 0.275 al 4°, n=40, ~2σ) — compatibile con selezione/rumore, e il test (5) sotto esclude eterogeneità run-level.
**(4) Il meccanismo del rimescolamento, identificato.** Le porte di lock consecutivi distano L1 mediana 15 celle (q25/q75: 5/27); la cella critica assoluta NON è mai la stessa in lock consecutivi: **0/465**. Ogni tentativo ricampiona la checklist da un punto fresco del campo di detriti. Una protezione richiederebbe una cospirazione *globale* del campo — pre-avvelenare ogni futura posizione di porta — che l'orbita stessa riscrive di continuo. Questo è il germe del lemma di mixing.
**(5) Nessuna eterogeneità tra run:** var dei tassi per run / attesa binomiale = 0.93.

**Caveat di potenza:** ~1.100 lock, solo porta fase 0, lista finita di invarianti candidate. La caccia va estesa (altre porte, mod 8/16, stato congiunto della checklist, invarianti di storia) prima di dichiarare il deserto — ma i candidati naturali sono null puliti.

**Stato del programma dopo §12–17.** La congettura è ridotta a due bersagli matematici:
- **(α) Lemma di ricorrenza dei lock:** ogni orbita finita che non entra mai produce lock simbolici alle porte infinitamente spesso. (Unico alleato noto: illimitatezza di Bunimovich–Troubetzkoy; il collegamento è aperto — la nucleazione NON è di bordo, §14A.)
- **(β) Lemma di non-cospirazione (mixing):** la checklist agli istanti di lock non può restare eternamente sbagliata. Germe dell'argomento: la porta migra, la cella critica non si riusa, le transizioni sono libere; una protezione eterna richiederebbe un invariante globale del campo di detriti, e lo screening non ne trova.
α ∧ β ∧ (esclusione di asintotiche alternative) ⇒ congettura. La parte locale (Teoremi 1, 2, dogana) è finita e Lean-abile.
File: `antitheorem.py` → `antitheorem.pkl`.

## 11. Trappole nuove
- Le frequenze delle bocche da pipeline committed NON sono la misura raw: il filtro arricchisce la fase 0 (66.7% → 45.0%). Riportare sempre la misura.
- "12 bocche" è un'istantanea della misura, non l'invariante: l'invariante è il confinamento nei segmenti non-frontiera.
- new104 = 22 è costante per definizione (celle del mattone): non usarla come feature.
