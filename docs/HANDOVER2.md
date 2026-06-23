# HANDOVER 2 — Formica di Langton: dalle bocche al Teorema della Soglia, alle dogane, ai due lemmi residui
**Data: 10 giugno 2026 — Michael Spina + Claude. Sessione: anatomia → caratterizzazione esatta delle bocche → scomposizione causale dell'ingresso → riduzione della congettura a due lemmi.**
**Prerequisito: HANDOVER.md (sessione precedente, incluso nel tar). Convenzioni §2 di quel file INVARIATE e qui assunte: regola, heading, W0 (in `W0.npy`), onset canonico griglia vuota N0 = 9977, fase k ≡ parola roll(W0,−k), criterio committed, famiglia seed baseline (box 7–15, dens 0.25–0.55, formica centro heading 0). Dettagli completi di ogni risultato: `ANATOMY_ADDENDUM.md` §12–17 (incluso). Questo file è la mappa.**

## 0. Stato in una frase
La parte locale è matematica finita (tre teoremi certificabili in Lean); la congettura globale è ridotta a: **(α) lemma di ricorrenza dei lock + (β) lemma di non-cospirazione della checklist + esclusione di asintotiche alternative.**

## 1. Catena dei risultati di questa sessione (con falsificazioni)

### 1.1 Anatomia del ciclo (addendum §1–3)
- Il ciclo depone esattamente 22 celle vergini/periodo in 10 raffiche: F = {13–15, 27–29, 32, 38, 45–47, 55–57, 60–62, 70–72, 75, 89}.
- Bocche concentrate nei segmenti senza frontiera; corridoio silenzioso = fasi 90→12; arco A nella sua prima metà; arco B = micro-pause.
- ρ_loc bocche 0.354 vs 0.280 (p=1e-4). Falsificate: apertura corridoio (p=0.40), frac-L simbolica (debole), K come predittore di bocca.
- Zone K=2 (certificato a 2 periodi): fasi {69–80, 95–99}, generate dalle 5 letture con lookback > P (vedi 1.5).

### 1.2 Misure d'ingresso (addendum §4–5): il supporto è della highway, il ranking della misura
- 6 famiglie di seed × 500: arco A 89–93% ovunque, top {0,99,103,102} stabile; zero parole non-W su 3.000 run.
- **Bias storico scoperto:** fase 0 al 66.7% in scaling.pkl era arricchita dal filtro committed; misura raw = 45.0%. Meccanismo: fase 0 = bocca dei transienti corti (onset mediano 2308 vs 3738, p=3e-12).
- Auto-riparazione (2.000 flip singoli): 100% ri-aggancio a W, zero fughe; spettro dominato da 99 (47%) — la bocca di corpo. Due regimi: bocca di vuoto (0) / bocca di corpo (99, K=2).
- Mappa-cardine (104 flip deterministici della cella sotto la formica): 100/104 ricadono nel supporto esteso.

### 1.3 TEOREMA DELLA SOGLIA (addendum §12) — il risultato centrale
Per minimalità dell'onset, ogni ingresso in fase k ha la formica a N0−1 sulla **cella di soglia** c₋₁(k) = pos₀ − dir(h₀) (frame relativo: sempre (0,1)) dove compie la svolta opposta a W0[k−1] ⇒ colore lasciato opposto a quello della highway.
**Teorema: fase k ammette configurazione finita con onset esattamente in k ⟺ c₋₁(k) non appartiene all'orbita futura della highway dalla fase k.**
- (⟹) determinismo (la parola eterna forza i colori di prima-visita); (⟸) testimone esplicito (certificato + soglia peccaminosa + formica in (0,1)).
- Check di non-ritorno FINITO via drift: orbita del periodo j = tubo₀ + j·drift ⇒ Jmax ≤ 7.
- Verifica: non-rivisitate (60 periodi) = enterable (costruzione diretta) = **22 fasi esatte**: Φ_ent = {0,16,21,24,25,26,30,31,72,83,90,91,92,93,94,97,98,99,100,101,102,103}. Tutte le 19 osservate ⊂ Φ_ent.
- **Segmento muto 1–12 risolto** (soglie rivisitate, ritardi 3–91). **"Frontiera ⇒ non-bocca" FALSIFICATA come legge esatta dalla fase 72** (di frontiera ma enterable); resta proxy di misura (21/22).
- **Tre bocche predette e costruite, mai osservate in ~5.600 eventi: 26 (|B|=15), 72 (|B|=20), 91 (|B|=19)** — testimoni in `witnesses.pkl` (celle nere, formica (0,1), heading pre-peccato).

### 1.4 Sonda globale (addendum §14): due falsificazioni che ridisegnano la montagna
- **Nucleazione di bordo: FALSIFICATA** (sul bordo del box visitato: 1% all'onset vs 13% null). L'illimitatezza (Bunimovich–Troubetzkoy, unico teorema globale noto) non si aggancia ingenuamente.
- **Lyapunov densitometrico: FALSIFICATO.** ρ_loc forward è mean-reverting puro con punto fisso ≈0.33, deriva globale nulla, NESSUNA rampa pre-onset. Il transiente vive sempre a densità del corpo; ρ(m) era survivorship (geometria condizionata al successo). TRAPPOLA: ogni candidato Lyapunov va testato come deriva forward NON condizionata.
- **Hazard quasi-memoryless:** vita residua ~costante dopo burn-in (λ ≈ 1/6.000 per passo), mix di fasi stazionario. Frame giusto: ingresso = hitting di un linguaggio finito-generato.
- **Reversibilità (struttura chiave):** la formica è reversibile; il bacino backward di ogni bocca è un albero binario esatto di stati parziali (biforcazione sulle celle ignote, prefissi forzati = i canali; C(n)~n^0.70 = statistica di crescita dell'albero).

### 1.5 D(t), near-miss, dogane (addendum §15)
- **D(t)** = max match di turns[t:] con fattori di W0^∞ (104 rotazioni). Bulk = grammatica generica (Markov-8 lo riproduce); coda REALE: P(D≥104)=7e-5/passo, max 175 — il transiente cavalca la parola esatta >1.5 periodi senza entrare. Hazard P(ingresso entro 312|D): 5%→61%, primo precursore vero.
- **Niente rampa monotona:** E[D(onset−m)] collassa a 7–9 negli ultimi 13 passi — si entra attraverso il peccato, non estendendo il match (Teorema della Soglia al livello simbolico).
- **Near-miss:** 204 cavalcate D≥80: partono al 96.6% dalle porte di Φ_ent (fase 0: 121), deragliano all'87% in Φ_ent con iper-concentrazione in **fase 98 (145/204)**.
- **Celle di dogana:** le letture con lookback > P sono 5/ciclo: offsets 76,77,80 (celle (−6,0),(−5,0),(−4,0)) e **98,99 (celle (−3,1),(−2,1), lookback 108)**. Per fase 0, la lista COMPLETA delle letture ritardate (lookback > offset) del periodo 1: offsets 12,33,43,44,50,76,77,80,98,99 — 10 celle. Colori richiesti delle 5 tardive: tutte NERE.

### 1.6 TEOREMA DELLA DOGANA (addendum §16): il verdetto è scritto alla partenza
Per lookback > offset, la cavalcata non tocca la cella prima della rilettura ⇒ il colore al lock È il colore letto.
- **P(ingresso | dogana 98/99 sbagliata al lock) = 0.000 su 430 — esatto, deterministico.** I near-miss sono già falliti quando partono.
- P(ingresso | 5 dogane giuste) = **0.918** (residuo: dogane precoci 43/44/50 e periodo 2).
- Geometria: dogane facili su riga y=0 (riga della porta, pass 0.58–0.78, costruite dal lock stesso); critiche su **riga y=1 = la riga della colpa** (0.52 / 0.25 ≈ base rate detriti per il nero). Soglia e dogane critiche sulla stessa riga: lì il passato deve sparire e lì accanto deve restare giusto.
- **Compressione del certificato:** per cavalcata a parola bloccata, le celle con lookback ≤ offset sono endogene (le scrive la cavalcata). Gate esogeno = checklist read-only finita: ~10 celle ritardate + traccia di frontiera bianca dentro il raggio detriti + soglia sepolta. NON |R|=42 vincoli.
- **Fattorizzazione esatta dell'hazard:** 0.31 (checklist OK tra i tentativi) × 0.918 = 0.28 = quota osservata di tentativi→ingressi. Il quasi-memoryless è spiegato: tasso di lock × probabilità stazionaria della checklist.

### 1.7 Caccia all'anti-teorema (addendum §17): 4 null
Transizioni dogana critica tra lock consecutivi ~iid (0.449/0.431/0.443); fallimenti pre-ingresso sotto-dispersi vs geometrica; parità (t mod 2 ≡ parità porta per x+y+t≡0 conservata), t mod 4, heading: chi² 0.38–0.92; eterogeneità run ratio 0.93. **Meccanismo del mixing: la porta migra (L1 mediana 15), la cella critica assoluta MAI riusata (0/465).** Una protezione richiederebbe cospirazione globale del campo. Caveat: ~1.100 lock, solo porta fase 0, lista finita di invarianti.

## 2. Formulazione corrente del programma
**Locale (finito, Lean-abile):**
- T1 (highway): certificato 104·K passi + induzione per shift.
- T2 (soglia): bocca ⟺ non-ritorno di c₋₁(k); |Φ_ent| = 22; testimoni espliciti.
- T3 (dogana): verdetto della cavalcata = checklist read-only al lock; esclusione deterministica.
**Globale (residuo):**
- (α) Ricorrenza dei lock: ogni orbita finita che non entra produce lock alle porte infinitamente spesso.
- (β) Non-cospirazione: la checklist agli istanti di lock non può restare eternamente sbagliata.
- (γ) Esclusione di asintotiche alternative (altre parole periodiche / aperiodicità eterna).
α ∧ β ∧ γ ⇒ congettura.

## 3. Domande aperte (priorità)
1. **Lean del pacchetto locale** (T1+T2+T3). T2 ha 3 ingredienti finiti (certificato, induzione shift, non-ritorno con Jmax≤7). Per T3: formalizzare lookback>offset ⇒ esclusione. Primo deliverable pubblicabile, ora compiuto concettualmente.
2. **Lemma α:** unico punto dove l'illimitatezza può servire (NON via bordo, §1.4). Idea da esplorare: D(t) ha coda pesante in ogni regime osservato — esiste un argomento combinatorio per cui un'orbita illimitata eterna deve produrre fattori di W0^∞ arbitrariamente lunghi? (Collegamento possibile: struttura dei blocchi LLRR / grammatica delle svolte su celle rivisitate.)
3. **Lemma β:** trasformare il meccanismo "porta migrante + cella mai riusata" in argomento. Estendere prima la caccia all'anti-teorema: altre porte, mod 8/16, stato congiunto della checklist, invarianti di storia, famiglie di seed avverse (costruite ad hoc per ingannare la checklist?).
4. **Checklist universali:** mappa offset/lookback/colore-richiesto per TUTTE le 22 porte (fatta solo fase 0). Le porte hanno dogane critiche diverse? La 99 (bocca di corpo) ha checklist più "naturale" per i detriti densi?
5. **γ:** zero non-W in ~5.600 eventi + classe chirale unica; serve un argomento (legato a T2: ogni parola periodica eterna ha le sue soglie — la classificazione delle parole ammissibili è un problema a sé).
6. **Misura delle 3 bocche fantasma (26, 72, 91):** perché peso ~0? Albero backward a 2 flip per stimare la crescita delle preimmagini per porta.
7. Domanda fine: perché il supporto osservato satura a 19/22 — esiste una misura naturale che le trova tutte?

## 4. Trappole (cumulative — quelle vecchie in HANDOVER.md §7 restano valide)
- Le frequenze da pipeline committed NON sono la misura raw (fase 0: 66.7% vs 45.0%).
- "12 bocche" e "frontiera ⇒ non-bocca" sono istantanee/proxy: l'invariante è il non-ritorno della soglia (22 fasi).
- ρ(m) e ogni quantità ancorata all'onset sono condizionate al successo: i candidati Lyapunov si testano come deriva forward non condizionata.
- La coerenza k-gram corta è grammatica generica (Markov-8 la riproduce): per D(t) contano solo le code oltre d≈56, con doppio null.
- new104 = 22 è costante per definizione.
- Il marginale della dogana dipende dal condizionamento: 0.25 nei near-miss, 0.44 pooled sui lock.
- snap_grid è già 2D (g[y+H, x+H]); `LIB` in antlib.py cerca /home/claude/ant/libant.so — compilare e copiare lì, o patchare il path.

## 5. Inventario file (questo tar, dir ant_pkg/)
**Sessione precedente (invariati):** HANDOVER.md, libant.c (+ libant.so compilata), antlib.py, W0.npy, pipeline.py, tests.py, causal.py (+causal_table.csv, causal_cone.png), runway.py (fixpoint.pkl), scaling.py (scaling.pkl, 2.000 run), mouths.py, runs.pkl.
**Questa sessione:**
- `ANATOMY_ADDENDUM.md` — il verbale completo §1–17. LEGGERLO DOPO QUESTO FILE.
- `anatomy.py` → anatomy.pkl (14 feature × 104 fasi, K minimi per tutte)
- `frontier.py` → frontier.pkl (maschera F, traiettoria mattone)
- `stress.py` → stress.pkl (6 famiglie × 500); `perturb.py` → perturb.pkl (2.000 flip)
- `threshold.py` → threshold.pkl (rivisite + enterability, 104 fasi); `witnesses.pkl` (testimoni 26/72/91)
- `figure.py` → mouths_anatomy.png (4 pannelli di sintesi)
- `global_probe.py` (estremalità + deriva forward; il .pkl da 33MB NON è nel tar: rigenerabile in ~90 s)
- `depth.py` (D(t), doppio null, hazard, rampa); depth_meta.pkl
- `customs.py` → customs.pkl (754 finestre, dogane, predittore)
- `antitheorem.py` → antitheorem.pkl (sequenze di lock, transizioni, screening)
Tempi: tutto in secondi tranne global_probe (~90 s) e perturb (~5 s). gcc -O3 -march=native -shared -fPIC libant.c -o libant.so; mkdir -p /home/claude/ant && cp libant.so /home/claude/ant/.

## 6. Frase di stato dell'arte
*La highway non nasce: viene ammessa. Le porte sono esattamente 22, caratterizzate dal non-ritorno della soglia; il verdetto di ogni tentativo è una checklist finita già scritta nello stato al momento del lock; e nulla di ciò che abbiamo testato — parità, posizione, heading, storia — sa tenere chiuse tutte le porte per sempre. Restano da dimostrare due lemmi: che bussare è inevitabile (α), e che il caso non ha complici (β).*
