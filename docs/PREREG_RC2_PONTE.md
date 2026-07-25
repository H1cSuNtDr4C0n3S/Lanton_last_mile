# PREREG RC2 — IL PONTE SCIA forward→backward (Fase 0b, pre-§109) (v9 = L-RESET no-go + L-OBL obbligazione retrospettiva come bersaglio operativo; v8 in 91a78b6, v7 in 0f4348a, v6 in 2eb096e, v5 in 26bcc2e, v4 in 8476472, v3 in bb52c5c, v2 in 134f117, v1 in b85b7db)

**Statuto (vincolante):** preregistrazione dell'ENUNCIATO e dell'AUDIT
dell'antecedente per il lemma-ponte RC2 (mandato del titolare post-Fase 0,
verdetto 2026-07-25: "enunciato matematico RC2 con audit dell'antecedente;
macchina soltanto dopo"). NON asserisce il ponte, NON contiene risultati,
NON costruisce macchine, NON tocca la Fase 1 (chiusa: mancano ancora le 8
milestone quantitative per-firma). Requisiti operativi ereditati
dall'ERRATA classificatoria di Fase 0: ogni checker di Fase 0b usa
CONTROLLI ESPLICITI (niente assert nudi: fail-open sotto `python -O`) e
registra `sys.flags.optimize == 0` nel summary.

## 0. Oggetto e posta in gioco

RC2 (docs/PREREG_RIENTRO_SCIA.md §1) vuole usare il Teorema della Scia
(§86.1, A-T5) sul camminatore all'indietro ai punti di uscita/rientro.
§86.1 è certificato in dinamica FORWARD con antecedente ESATTO: "t lettura
NERA deep₁ (cella VISITATA, fuori dalla finestra viva 3×3)". Il verdetto
post-Fase 0 fissa il punto: le due firme a genitore esterno individuate
dalla Fase 0 ((−2,2) h=1 e (2,2) h=0, unica sorgente
`alpha1/prereg_fase0_geometry_summary.json`) sono bersagli SOLO
CONDIZIONATAMENTE — il vantaggio esiste se il bordo-genitore può essere
identificato con un evento cui si applica DAVVERO l'antecedente della
Scia; "essere un rientro" da solo non basta.

## ERRATA-RC2 (verdetto del titolare 2026-07-25, post-b85b7db — vincolante, applicata nel corpo)

La v1 preregistrava il PROTOCOLLO di costruzione, non un lemma chiuso (la
mappa (iii) di 0b.0 e i parametri r_0b/d_0b restano DA FISSARE nel lemma),
e conteneva quattro difetti, corretti qui:
1. **Le ultime tre svolte non certificano deep₁.** La geometria di §86
   dimostra LLL ⇒ non-deep, NON il converso non-LLL ⇒ deep; usarla per
   marcare positivamente deep sarebbe CIRCOLARE (§86 assume già deep). La
   definizione operativa vera è quella del macchinario forward
   (`halo_occupancy_profile.py`: deep1 = visited ∧ c ∉ known = RILETTA +
   DIMENTICATA). M1 è riformulata su known/forgotten; la ricostruzione
   dalle svolte resta SOLO come filtro di esclusione (LLL ⇒ non marcare),
   mai come certificato positivo.
2. **"Visitata dopo il passo" ≠ "già visitata prima".** C3 certifica che
   c_par è visitata a m* perché il passo l'ha APPENA letta; la Scia esige
   una visita PIÙ ANTICA della lettura stessa. Il proof object deve
   esibire la visita precedente, l'uscita dalla finestra e l'assenza di
   riletture successive.
3. **Il seme è escluso in palla-2, non nell'anello 3.** T20 permette
   "L ⇒ rilettura" solo FUORI dal supporto del seme; proprio i due
   bersagli privilegiati hanno c_par nell'anello 3, dove una L potrebbe
   essere PRIMA lettura di una cella nera di seme. Scelta dell'universo
   esplicita (sezione 2b); un'eventuale restrizione ai record lontani NON
   si inserisce silenziosamente in R_f: il passaggio ai quantificatori di
   X6 va ridimostrato.
4. **Verdetti non disgiunti nella v1** ("certificato" anche vacuo e
   "unknown-dominato" potevano coesistere). Partizione corretta in
   sezione 4: GATE NON RAGGIUNTO / PONTE FALSO / VALIDO-E-UTILE /
   VALIDO-MA-INUTILE.

## DECISIONE OPERATIVA post-ERRATA-RC2 (verdetto del titolare 2026-07-25/2 — vincolante)

ERRATA-RC2 accolta; M1-v2 coincide col predicato operativo
deep₁(t) ⟺ visited(t) ∧ c_t ∉ known_t. Decisioni:
- **universo SCELTO = U3** (sezione 2b): tentare PRIMA il lemma di
  trasferimento dei quantificatori (0b.U3-a/b);
- **kill-gate principale di 0b.2:** un certificato finito per singolo
  punto NON implica una profondità uniforme d_0b (la visita precedente
  può essere arbitrariamente antica; "assenza di riletture" può non
  essere decidibile da alcun suffisso di lunghezza fissa). d_0b NON va
  MAI scelto da un massimo censito (trappola qq);
- **ordine dei lavori (aggiornato 2026-07-25/8):** (1) 0b.U3-a
  (direzione utile relativizzata) / 0b.U3-b: L-U3a.1/2 PROMOSSE e
  L-U3b CHIUSA sotto il fatto B–T; (2) L-MON PROMOSSO; **L-0b0
  CHIUSO** (/7, /8); **L-RESET registrato [T]** (/8: la visita resetta
  tutto a K — no-go per il gate deep dello stato mobile); (3) bersaglio
  operativo = **L-OBL** (sez. 3d: automa retrospettivo
  SEEK0/SEEK2/RESOLVED per evento distinto; OUT certifica SEEK2; un
  evento per volta; primo bersaglio = un parent-step delle due firme
  esterne; se sopravvive un ramo KNOWN reale, quella marcatura è
  falsificata e NON si raffinano i portali automaticamente), con
  L-REV/Q_c (sez. 3c) mantenuto come sovra-approssimazione generale di
  soundness; (4) Via A OPZIONALE e diagnostica; (5) costruzione/
  certificazione della Via B SOLO dopo L-OBL; (6) 0b.3 solo dopo.
  Fase 1 e §109 restano chiusi;
- **nessuna enumerazione 0b.3** finché monitor/località (0b.2) e mappa
  (0b.0) non sono TEOREMI e 0b.U3 non è chiuso. Fase 1 resta chiusa.

## PRECISAZIONI FORMALI (verdetto del titolare 2026-07-25/3 — vincolanti, applicate nel corpo)

1. **Quantificatori della Via A.** Una coppia trovata a un dato d
   falsifica SOLTANTO quel d (∃P,Q: suffix_d(P)=suffix_d(Q) ∧
   M(P)≠M(Q)); una griglia finita di valori NON può decidere l'enunciato
   globale ∃d₀ ∀P,Q: suffix_{d₀}(P)=suffix_{d₀}(Q) ⇒ M(P)=M(Q).
   Semantica dei verdetti e chiave di equivalenza delle coppie congelate
   in Via A (sezione 3).
2. **Tavola del monitor congelata** con guardie e ordine temporale:
   "distanza Chebyshev 2 ⇒ FORGOTTEN" vale SOLO partendo da KNOWN (da
   UNSEEN il raggiungimento della distanza 2 non può creare una visita
   precedente); il verdetto si emette sullo stato PRECEDENTE alla
   lettura, poi la visita resetta a KNOWN (sezione 3, Via B).

## PRECISAZIONI FORMALI 2 (verdetto del titolare 2026-07-25/4 — vincolanti, applicate nel corpo)

1. **La monotonia in d non seguiva dalla definizione v4.** M_c valutato
   "al confine del suffisso" ha un confine MOBILE: cambiando d cambia
   l'istante osservato, e nel tratto comune successivo una rilettura di
   c può resettare il monitor a KNOWN — l'"a fortiori d' ≤ d" era FALSO
   senza definizione aggiuntiva. Correzione adottata (la seconda delle
   due ammesse): si fissa l'EVENTO bersaglio e = (P, t, c) e si valuta
   M_c(e) = M_c(t⁻) a istante FISSO; O_d(e) = proiezione dichiarata dei
   passi t−d, …, t−1; l'uccisione dei d' ≤ d vale SOLO sotto annidamento
   verificato O_{d'} = ρ_{d→d'}(O_d) (sezione 3, Via A).
2. **La tavola del monitor non era totale:** mancava la riga
   KNOWN + nessuna visita + distanza ≠ 2 ⇒ KNOWN (essenziale: dopo una
   visita il primo passo porta normalmente a distanza 1 e la cella deve
   restare KNOWN). Tavola resa esaustiva + ordine esatto a 4 passi
   (sezione 3, Via B).
3. **Via A retrocessa a OPZIONALE E DIAGNOSTICA:** non è necessaria se
   la Via B viene certificata. Ordine operativo aggiornato nella
   DECISIONE OPERATIVA.

## CLAUSOLE DI CHIUSURA (verdetto del titolare 2026-07-25/5 — vincolanti, applicate nel corpo)

1. **Guardia ANTI-LEAKAGE per O_d (Via A).** O_d(e) NON deve contenere:
   M_c(e); `known(c)` o lo stato del monitor di c; il proof object
   visita–dimenticanza; informazioni calcolate usando passi anteriori a
   t−d; qualunque campo equivalente al verdetto da predire. Altrimenti
   la Via A diventerebbe vera PER COSTRUZIONE. La clausola (iii) della
   chiave di equivalenza va letta come "tutta l'informazione AMMESSA E
   NON-LEAKING"; ogni componente di O_d deve avere una procedura di
   calcolo che usa SOLTANTO i passi t−d, …, t−1.
2. **Precondizione di 0b.3 corretta:** "Via A decisa" era troppo debole
   (poteva essere morta o unknown). Condizione corretta:
   **Via A PROVATA con d₀ esplicito ∨ Via B CERTIFICATA** — solo un
   esito POSITIVO fornisce la rappresentazione finita necessaria a
   D_RC2.
3. **Forma ufficiale del lemma del monitor (Via B).** Per ogni cella
   fissata c, invariante da dimostrare per induzione sugli
   aggiornamenti last/known del simulatore forward:
   S_t(c) = UNSEEN se c ∉ last_t; KNOWN se c ∈ known_t; FORGOTTEN se
   c ∈ last_t \ known_t (con known_t ⊆ last_t i tre casi sono disgiunti
   ed esaustivi). Corollario immediato:
   **lettura di c è deep₁ ⟺ S_t(c) = FORGOTTEN.**
   Il replay resta una VERIFICA DELL'IMPLEMENTAZIONE, non parte della
   prova.

## 1. Lemma 0b.0 — corrispondenza temporale backward–forward (da certificare)

Enunciato da dimostrare (nessuna parte è asserita qui). Sia P un passato
completo che presenta w101 a un record y-min stretto (frame anchor: posa
finale in origine, heading-su; convenzione bit §95b: 1 = R = lettura
BIANCA, 0 = L = lettura NERA), di lunghezza totale T = 101 + N (N =
numero di prepend). Allora per ogni k ∈ [1, N]:
- (i) il k-esimo prepend del camminatore corrisponde al passo forward di
  indice j(k) = N − k + 1 (il prepend più profondo = il passo più
  antico dell'orbita);
- (ii) la cella letta dal prepend k (cn = posa − D[h], §97a) è, nel frame
  anchor, la cella letta dal passo forward j(k);
- (iii) posa e heading del camminatore al depth k determinano posizione e
  heading forward a j(k) tramite una mappa esplicita DA SCRIVERE nel
  lemma (inclusa la convenzione di verso backward vs forward)
  [aggiornamento post-/6: la mappa è SCRITTA e dimostrata in bozza —
  L-0b0, docs/RC2_LEMMI_0B.md v2, in attesa di pannello; restano da
  fissare solo r_0b/d_0b, superati dalla Via B/L-REV];
- (iv) la lettera del prepend è la svolta del passo forward j(k), e il
  colore letto forward coincide col colore richiesto dal req backward.
Metodo: deduzione dalle definizioni del camminatore (§92a, §95b) + gate
di terra OBBLIGATORIO: replay forward dei 10 controesempi §94 e di ≥ 100
estensioni casuali, confronto passo-passo bit-identico (stile N4/§97e).
Una divergenza qualsiasi = lemma rosso.

## 2. Lemma 0b.1 — audit dell'antecedente (il cuore, falsificabile)

**Marcatura M1-v2 (fissata QUI; sostituisce la M1 della v1 per
ERRATA-RC2.1/2; ogni modifica = nuova preregistrazione):** un prepend k è
RC2-marcato se, sul SOLO stato backward dichiarato, valgono TUTTE:
- (a) la lettera è L (lettura nera; decidibile: semantica req §92a);
- (b) **RILETTA:** esiste una visita della cella letta PIÙ ANTICA del
  passo j(k) stesso — la visita fatta dal passo corrente NON conta
  (distinzione temporale ERRATA-RC2.2);
- (c) **DIMENTICATA:** dopo l'ultima visita precedente la cella è USCITA
  dalla memoria di finestra r=1 (`known`) ed è rimasta senza riletture
  fino a j(k) — definizione operativa allineata al macchinario forward
  (`halo_occupancy_profile.py`: deep1 = visited ∧ c ∉ known);
- (d) nessuna di (b)/(c) è decisa per congettura o per geometria delle
  svolte: o dedotte dallo stato dichiarato col proof object (sotto), o
  il punto è `unknown` e NON è marcato.
La ricostruzione dalle ultime ≤ 3 svolte (§86.1) è ammessa SOLO come
filtro di ESCLUSIONE (LLL ⇒ non-deep ⇒ non marcare); MAI come
certificato positivo di deep: il converso non-LLL ⇒ deep non è dimostrato
e usarlo sarebbe circolare (ERRATA-RC2.1).

**Proof object per-punto (obbligatorio per marcare):** (i) la visita
precedente ESIBITA (indice del passo/prepend che la compie); (ii)
l'uscita dalla finestra dopo quella visita (distanza ≥ 2 raggiunta);
(iii) l'assenza di riletture fra quella visita e j(k).
Vie ammesse per (b): il ledger (§93a: L su pending irrealizzabile ⇒ ogni
L su cella non-di-seme è rilettura; pending finali = seme nero visitato,
T20) — con la LIMITAZIONE ERRATA-RC2.3: T20 deduce "L ⇒ rilettura" solo
FUORI dal supporto del seme; in palla-2 l'ipotesi del record esclude il
seme, nell'ANELLO 3 no — lì la deduzione richiede l'ipotesi spaziale
della sezione 2b, altrimenti il punto è `unknown`. Questo è il punto
dove il ponte può morire in vacuità (esito VALIDO-MA-INUTILE, sez. 4).

**PONTE (enunciato da certificare):** ogni prepend M1-v2-marcato
soddisfa, nel replay forward, l'antecedente esatto di §86.1: lettura
nera ∧ cella VISITATA-PRIMA ∧ fuori dalla finestra viva.
**FALSIFICATORE (F-0b.1 v2, forma del verdetto):** UN SOLO parent-step o
prepend L marcato che nel replay forward risulti PRIMA LETTURA oppure
ancora `known` ⇒ M1-v2 MORTA (riformulare con nuova preregistrazione o
abbandonare RC2). Il testimone va riportato PRIMA di ogni assert
d'esaurimento (trappola ii).

Conseguenza dichiarata della marcatura (non un risultato): i rientri a
lettera R (lettura bianca) sono fuori marcatura per definizione — RC2,
se certificato, vincola SOLO i punti L. Se ai punti utili delle due
firme-bersaglio il traffico è R-dominato, il vantaggio condizionale
svanisce: va misurato, non presunto.

## 2b. Universo: U3 SCELTO (decisione operativa 2026-07-25/2)

- **U0 (di riferimento):** passato reale completo che presenta w101 a un
  record y-min stretto — il seme è escluso SOLO dalla palla-2 (ipotesi
  del Muro). Nell'anello 3 una L può essere prima lettura di una cella
  nera di seme: lì la componente RILETTA non è deducibile da T20 e i
  punti restano `unknown`.
- **U3 (SCELTO):** record con
  **B_∞(z_t, 3) ∩ (supp(seme) ∪ {origine}) = ∅** — elimina l'ambiguità
  "L fresca da seme" nell'anello 3. Base di plausibilità (dichiarata,
  non ancora un lemma): T17 registra che B–T dà infiniti record fuori da
  OGNI intorno finito ⇒ con l'intorno di raggio 3, U3 dovrebbe essere
  COFINALMENTE disponibile lungo ogni orbita eterna non-highway.
  Obblighi formali PRIMA di usare U3 (lemma di trasferimento, da
  tentare per primi):
  - **0b.U3-a (RINOMINATA dal verdetto 2026-07-25/6: "direzione utile
    relativizzata", NON bicondizionale):** restrizione a U3 della SOLA
    direzione utile al Muro — (∀f: ¬R_f^{U3}) ⟹ v2^{U3} — perché la
    bicondizionale X6 NON relativizza in silenzio (L-U3a.3 di
    docs/RC2_LEMMI_0B.md: il testimone exit-step nasce a Chebyshev 3,
    dentro B_∞(z_t,3), quindi non-U3); nessun inserimento silenzioso in
    R_f. Bozze: L-U3a.1/2 (PROMOSSE dal pannello /6).
  - **0b.U3-b:** la restrizione è SUFFICIENTE al Muro (i record U3 sono
    cofinali: la vietanza sui soli record U3 basta alla contraddizione
    con B–T). Bozza: L-U3b, CHIUSA "sotto il fatto B–T" con rider
    WLOG-C4-sym esplicito (pannello /6).
  Etichetta post-/6: i risultati sotto U3 sono "condizionali al fatto
  B–T" (via L-U3b, chiuso come condizionale dichiarato); resta in
  attesa di pannello solo la bozza L-0b0.

## 3. Lemma 0b.2 — località e completezza del dominio (due vie, decisione 2026-07-25/2)

Da ottenere: il verdetto di marcatura (marcato / non-marcato / `unknown`)
funzione di informazione backward FINITA e DICHIARATA, così che il
dominio D_RC2 sia finito e la sua enumerazione COMPLETA (non un campione,
ERRATA-1.6). Kill-gate dichiarato: la visita precedente può essere
arbitrariamente antica ⇒ un d_0b uniforme può NON esistere.

**Via A — esiste un d_0b uniforme? (OPZIONALE E DIAGNOSTICA — non
necessaria se la Via B è certificata; definizione per EVENTO,
precisazione 2026-07-25/4).** Enunciato globale in gioco:
∃d₀ ∀e,e' (eventi in U3): O_{d₀}(e) = O_{d₀}(e') ⇒ M_c(e) = M_c(e').
Definizioni (la versione v4 "al confine del suffisso" aveva un confine
MOBILE e l'a-fortiori era falso): si fissa l'EVENTO bersaglio
e = (P, t, c) — passato valido P, istante t della lettura candidata,
cella bersaglio c; **M_c(e) = stato del monitor di c a t⁻** (istante
FISSO, indipendente da d); **O_d(e) = proiezione DICHIARATA dei passi
t−d, …, t−1**. Le proiezioni devono essere ANNIDATE:
O_{d'}(e) = ρ_{d→d'}(O_d(e)) per ogni d' ≤ d (restrizione agli ultimi
d' passi); se una componente dello stato dichiarato non è ricostruibile
per restrizione, l'annidamento NON vale e la coppia uccide SOLO il d
testato.
FALSIFICATORE PER SINGOLO d: coppia di eventi e, e' con O_d(e) =
O_d(e') e M_c(e) ≠ M_c(e'). Sotto annidamento verificato: O_d uguali ⇒
O_{d'} uguali ∀ d' ≤ d ⇒ la coppia uccide anche ogni d' ≤ d; nulla sui
d maggiori.
**Semantica dei verdetti (congelata):**
- coppia trovata a d ⇒ quel d UCCISO (e ogni d' ≤ d SOLO sotto
  annidamento verificato delle proiezioni);
- nessuna coppia su tutta la griglia ⇒ verdetto SOLO `unknown`
  sull'enunciato globale — MAI "d_0b esiste": una griglia finita non
  decide ∃d₀;
- Via A VERDE (d_0b esiste) ⇒ esige una PROVA UNIFORME (deduzione valida
  per ogni coppia), non l'assenza di coppie nella griglia;
- Via A DEFINITIVAMENTE MORTA ⇒ esige una famiglia parametrica /
  pumping argument: ∀d ∃(P_d, Q_d) coppia falsificante.
**Chiave di equivalenza delle coppie (congelata):** ogni coppia deve
(i) appartenere INTERAMENTE a U3 (entrambi i passati); (ii) riferirsi
alla stessa firma, stessa cella bersaglio c e stessa convenzione anchor;
(iii) coincidere su TUTTA l'informazione AMMESSA E NON-LEAKING dichiarata
in O_d (clausola anti-leakage 2026-07-25/5: O_d NON contiene M_c(e),
known(c)/monitor di c, il proof object visita–dimenticanza, informazioni
calcolate da passi anteriori a t−d, né campi equivalenti al verdetto da
predire; ogni componente ha una procedura di calcolo che usa SOLO i
passi t−d, …, t−1) — non soltanto i bit del suffisso, qualora O_d
includa altre componenti ammesse (req note, pend₂, monitor di ALTRE
celle).
Regole operative: d_0b non si sceglie MAI da un massimo censito
(trappola qq); la caccia alle coppie va fatta su una griglia di d
dichiarata prima della run, con enumerazione/ricerca meccanica
sull'albero dei prepend (mai coppie costruite a mano); aspettativa
dichiarata: REALISTICA la morte dei singoli d — il quadro §90b (visita
di (1,1) a prof. 57 dietro w101, sweep esaustivo zero a 46) suggerisce
che coppie del genere esistano, ma ogni coppia va REALIZZATA
meccanicamente, non dedotta a mano.

**Via B — monitor finito per cella bersaglio (la DIREZIONE STRATEGICA;
preregistrato QUI; tavola TOTALE, precisazione 2026-07-25/4).** Per
ogni cella bersaglio c, automa a 3 stati {UNSEEN, KNOWN, FORGOTTEN}.
**ORDINE ESATTO per passo (congelato):**
1. emettere il verdetto fresh/in-window/deep sullo stato PRE-lettura;
2. visita ⇒ KNOWN;
3. effettuare la mossa;
4. eventuale attraversamento dell'anello Chebyshev 2 ⇒ FORGOTTEN
   (guardia: SOLO partendo da KNOWN).
Tavola esaustiva (ogni caso coperto):

| stato prima | evento                                                | verdetto  | stato dopo |
|-------------|-------------------------------------------------------|-----------|------------|
| UNSEEN      | visita di c                                           | fresh     | KNOWN      |
| UNSEEN      | nessuna visita (qualunque distanza)                   | —         | UNSEEN     |
| KNOWN       | visita di c                                           | in-window | KNOWN      |
| KNOWN       | nessuna visita; posizione dopo la mossa a Chebyshev 2 | —         | FORGOTTEN  |
| KNOWN       | nessuna visita; distanza dopo la mossa ≠ 2            | —         | KNOWN      |
| FORGOTTEN   | visita di c                                           | **deep**  | KNOWN      |
| FORGOTTEN   | nessuna visita                                        | —         | FORGOTTEN  |

Guardie essenziali: "Chebyshev 2 ⇒ FORGOTTEN" vale SOLO partendo da
KNOWN — da UNSEEN il raggiungimento della distanza 2 NON crea una
visita precedente (UNSEEN resta UNSEEN); e dopo una visita il primo
passo porta normalmente a distanza 1: la cella RESTA KNOWN finché
l'anello 2 non viene attraversato.
Il monitor riassume un intervallo arbitrariamente lungo SENZA pretendere
un d_0b uniforme; nel camminatore backward diventa un'obbligazione
finita o una transizione non-deterministica CONTROLLATA (unknown-safe:
lo stato non noto non produce mai marcatura). Obblighi di certificazione
della Via B: (i) equivalenza monitor ↔ `known` del simulatore forward
DIMOSTRATA PER INDUZIONE (non solo testata); (ii) replay completo: UNA
sola discrepanza sul predicato deep UCCIDE il monitor; (iii) esca
obbligatoria sul checker; (iv) controlli espliciti + optimize==0.

**Test minimo falsificabile prima di 0b.3 (i 4 punti del verdetto):**
1. caccia alla coppia falsificante di d_0b (Via A);
2. induzione monitor ↔ `known` del simulatore (Via B, se attivata);
3. replay completo con kill su una discrepanza del predicato deep;
4. lemma di restrizione U3 per T24–T26 (0b.U3-a) + sufficienza (0b.U3-b).
Ogni parametro sound "per caso fattuale" va verificato con controllo
esplicito a ogni valore di raggio (trappola mm).

## 3c. L-REV — monitor inverso a sottoinsiemi (PREREGISTRATO /6, integrato /7; dopo il verdetto /8 resta la SOVRA-APPROSSIMAZIONE GENERALE di soundness — il bersaglio OPERATIVO è L-OBL, sez. 3d: il gate deep su Q_c allo stato mobile è UCCISO da L-RESET, Pre_visita({K}) = {U,K,F}, e U3+L lascia {K,F} ≠ {F})

L-MON dimostra il monitor deterministico IN AVANTI; la macchina lavora
ALL'INDIETRO, dove la transizione non è in generale invertibile. Il
replay non può sostituire la deduzione universale. Oggetto
preregistrato (ipotesi del titolare: "monitor inverso a sottoinsiemi
con collasso esterno"):
- **Stato backward INSIEMISTICO:** per ogni cella sorvegliata
  c ∈ C_RC2, Q_c ⊆ {U, K, F}, **Q_c ≠ ∅** — una stessa osservazione
  inversa può provenire da più stati; conservare un solo stato
  produrrebbe falsi `deep`. Ogni prepend applica la RELAZIONE INVERSA
  COMPLETA della tavola forward (derivata A MANO dalle righe della
  tavola totale v5, poi enumerata ESAUSTIVAMENTE su ogni combinazione
  stato/evento — mai campionata).
- **Marcatura deep:** ammessa SOLO quando Q_c ⊆ {F} (equivalentemente
  Q_c = {F}, essendo Q_c ≠ ∅). Una marcatura deep con U o K ancora
  compatibili UCCIDE RC2.
- **CONCRETIZZAZIONE (il predicato matematico della soundness,
  verdetto /7.2 — senza di questo l'induzione di contenimento non ha
  tesi formale):** Γ(n) = insieme dei passati U3 reali COMPATIBILI col
  nodo backward n. Invariante da dimostrare:
  **Q_c(n) ⊇ { S^P_{τ(n)}(c) : P ∈ Γ(n) }** per ogni c ∈ C_RC2, dove
  τ(n) = istante forward associato a n dalla mappa L-0b0 (convenzione
  0-based definitiva; raccordo t = s − 1). Da esplicitare PRIMA della
  prova: caso base Q_c(n₀); definizione di τ(n); trasferimento
  padre–figlio; vincoli ledger/U3 applicati nel trasferimento;
  dimostrazione che NESSUN elemento concreto viene perso.
- **ALFABETO LOCALE degli eventi (congelato, /7.3):** per ogni cella c,
  a_c = (v_c, r_c): v_c = 1 se il passo legge c; r_c = 1 se dopo la
  mossa la distanza da c è esattamente 2. Casi cinematicamente
  raggiungibili: **(1,0), (0,1), (0,0)** — (1,1) impossibile (la cella
  appena letta dista 1 dopo la mossa unitaria). Con la tavola forward
  δ_c di L-MON, la relazione backward è ESATTAMENTE
  **Pre_{a_c}(Q) = { s ∈ {U,K,F} : δ_c(s, a_c) ∈ Q }**. L'evento NON
  contiene deep, known né informazione equivalente al verdetto
  (anti-leakage, coerente col /5).
- **Natura MARGINALE del prodotto (/7.5, dichiarata):**
  ∏_{c∈C_RC2} Q_c(n) è una sovra-approssimazione MARGINALE: dimentica
  le correlazioni fra celle e NON è l'insieme esatto delle
  configurazioni congiunte. Sound per risultati negativi e per la
  marcatura deep su singola cella, PURCHÉ nessun margine concreto venga
  escluso (parte dell'invariante di concretizzazione).
- **Soundness (da dimostrare per induzione sull'invariante di
  concretizzazione):** ogni storia reale resta CONTENUTA nello
  stato-insieme backward a ogni profondità. UN SOLO predecessore reale
  escluso uccide la soundness.
- **Finitezza: frame ANCHOR FISSO (/7.4 — disambiguazione della
  clausola v7, che chiedeva una "chiusura sotto traslazione"
  matematicamente impossibile per un insieme finito):** C_RC2 =
  insieme FINITO di celle ASSOLUTE nel frame anchor; NESSUNA chiusura
  per traslazione richiesta. (Lo schema relativo quozientato resta
  un'alternativa futura, NON adottata.)
- **COLLASSO OUT UNICO (prima mossa, ipotesi /7):** congelato
  **K = ∪_{c∈C_RC2} B_∞(c, 2)**: ogni escursione interamente fuori da
  K ha effetto monitor U↦U e F↦F; uno stato KNOWN che esce da K deve
  attraversare l'anello 2 della propria cella ⇒ KNOWN↦F. Si parte
  dunque con UN SOLO macro-stato OUT che ammette
  sovra-approssimativamente ogni rientro di frontiera: certamente
  sound. Il gate di utilità decide se è troppo grossolano: SOLO se
  produce sempre Q_c ≠ {F} si raffinano i portali.
- **Test minimo falsificabile di L-REV (aggiornato /7, OTTO punti,
  prima del tool principale):**
  1. errata del mini-lemma dei colori col bordo-seme
     [FATTA: RC2_LEMMI_0B v3];
  2. indici DEFINITIVI: 0-based (come codice e L-MON; L-0b0 raccordato
     con t = s − 1) [FISSATO];
  3. definire Γ(n), Q_c(n), caso base e istante τ(n);
  4. enumerare i 3×3 casi stato/evento raggiungibili e verificare
     esattamente Pre;
  5. provare l'inclusione concreta per un SINGOLO passo;
  6. estenderla per induzione a ogni profondità;
  7. **esca U/F sul monitor astratto COLOR-FREE** (non solo sui passati
     U3, dove una L fresca può già essere esclusa): fondere UNSEEN e
     FORGOTTEN deve produrre almeno un falso `deep`, altrimenti il
     checker è vacuo;
  8. gate di utilità: Q_c = {F} su almeno un parent-step o punto
     d'escursione RC2 rilevante; altrimenti VALIDO-MA-INUTILE.
- Requisiti operativi: controlli espliciti (niente assert nudi),
  sys.flags.optimize == 0 registrato, tripwire CP, esca sul checker.

## 3d. L-OBL — obbligazione retrospettiva per evento distinto (PREREGISTRATO, verdetto 2026-07-25/8: il bersaglio operativo che sostituisce il gate deep di L-REV)

**Motivazione (L-RESET, RC2_LEMMI_0B v4, [T]):** la visita resetta
{U,K,F} a K ⇒ Pre_visita({K}) = {U,K,F}; U3 + lettera L eliminano U ma
lasciano Q_c = {K,F} ≠ {F} ⇒ il gate deep sul powerset dello stato
corrente NON può mai scattare al momento della visita. Non è una
falsificazione di RC2: è la falsificazione della speranza che il Pre
dello stato corrente certifichi retroattivamente il pre-stato.

**Oggetto.** Per un SINGOLO evento bersaglio distinto e (lettura
candidata della cella c al tempo τ(e)): partendo immediatamente PRIMA
della lettura bersaglio e scandendo il passato verso tempi più antichi,
automa di obbligazione:
- **SEEK0**: nessun attraversamento dell'anello 2 di c ancora
  incontrato;
- **SEEK2**: almeno un attraversamento dell'anello 2 incontrato;
- incontro della VISITA PRECEDENTE di c: da SEEK0 ⇒ **RESOLVED-K**; da
  SEEK2 ⇒ **RESOLVED-F**;
- nascita raggiunta senza visita precedente ⇒ **RESOLVED-U**.
Classificazione bersaglio (da dimostrare, punto 6 del test): nessuna
visita precedente ⇒ U; visita precedente senza uscita dall'anello 2 ⇒
K; visita precedente con uscita prima del target ⇒ F.
**Ruolo di OUT (corretto dal /8):** certificare SEEK2 — uscire da K
forza SEEK0 → SEEK2 (una traiettoria unitaria deve attraversare
l'anello 2) — NON invertire il reset della visita.
**Disciplina di stato finito:** UN SOLO evento distinto per volta, per
firma/punto rilevante (obbligazioni simultanee per ogni L = numero non
limitato di obblighi pendenti: VIETATO).
**Ordine di applicazione dei filtri:** U3 e lettera L si applicano SOLO
DOPO la classificazione (servono a escludere U, non a decidere K/F).
**Gate operativo (congelato):**
- ogni ramo compatibile risolve F ⇒ marcatura;
- almeno un ramo compatibile risolve K ⇒ NON marcato;
- ramo non risolto o astrazione incapace di decidere ⇒ `unknown`.
**Falsificatore:** se su un parent-step reale sopravvive un ramo KNOWN
compatibile, QUELLA marcatura RC2 è falsificata — e NON si raffinano
automaticamente i portali.
**Primo bersaglio:** UN singolo parent-step delle due firme a genitore
esterno ((−2,2) h=1 e (2,2) h=0, Fase 0).

**Test minimo falsificabile di L-OBL (sostituisce i punti 3–6 del test
/7 come prerequisiti operativi; 1–2 e 7–8 del /7 restano validi):**
1. L-RESET registrato [FATTO: RC2_LEMMI_0B v4, sez. 4c];
2. evento bersaglio e distinto, uno per volta;
3. definire **Γ(n, e)** (non soltanto Γ(n));
4. costruire l'automa SEEK0/SEEK2/RESOLVED-{U,K,F};
5. dimostrare: la PRIMA visita incontrata andando indietro è
   precisamente l'ULTIMA visita precedente andando avanti;
6. dimostrare le tre classificazioni (SEEK0 + visita precedente ⇒ K;
   SEEK2 + visita precedente ⇒ F; nascita senza visita ⇒ U);
7. applicare U3 e lettera L soltanto DOPO la classificazione;
8. gate operativo come sopra (F su tutti i rami ⇒ marca; un K ⇒ no;
   irrisolto ⇒ unknown).

## 4. Gate 0b.3 — enumerazione + replay forward (solo dopo 0b.0, 0b.U3-a/b e [Via A PROVATA con d₀ esplicito ∨ Via B CERTIFICATA — e la Via B ora presuppone L-OBL dimostrato, sez. 3d, con L-REV/Q_c come strato di soundness, sez. 3c])

Enumerare D_RC2 per intero; per ogni elemento: replay forward e verifica
dell'antecedente con checker a CONTROLLI ESPLICITI; esca obbligatoria
(elemento corrotto ⇒ il checker DEVE fallire); tripwire CP M0–M4 sul
macchinario nuovo (trappola kk); `sys.flags.optimize == 0` registrato
nel summary. Il criterio di UTILITÀ va congelato PRIMA del gate: punto
marcato sul parent-step o sull'escursione di una firma di F₈ (in
particolare le due a genitore esterno).
**Esiti ammessi (PARTIZIONE: mutuamente esclusivi ed esaustivi, emessi
dal tool — ERRATA-RC2.4):**
- **GATE NON RAGGIUNTO:** uno dei Lemmi 0b.0–0b.2 non è chiuso o un gate
  operativo è rosso — NESSUN verdetto sul ponte;
- **PONTE FALSO (F-0b.1 v2):** testimone esplicito a verbale;
- **PONTE VALIDO-E-UTILE:** antecedente verificato su TUTTI i punti
  marcati (≥ 1) E almeno un punto marcato soddisfa il criterio di
  utilità — RC2 utilizzabile nelle macchine di Fase 2/3, RISTRETTO ai
  punti marcati;
- **PONTE VALIDO-MA-INUTILE:** antecedente verificato su tutti i punti
  marcati, anche VACUAMENTE (zero punti marcati), ma nessun punto
  soddisfa il criterio di utilità — include il caso unknown-dominato.
  RC2 non entra in nessuna macchina; esito negativo onesto, si archivia.

## 5. Cosa questo documento NON fa

Non asserisce il ponte né alcuna irrealizzabilità ¬R_f; non costruisce
macchine ("macchina soltanto dopo"); non apre la Fase 1 (servono le 8
milestone quantitative per-firma, verdetto sotto-soglia = solo
`unknown`); non modifica il Teorema della Scia (§86.1 resta forward, con
le sue ipotesi). Trappole di guardia per l'esecuzione: (c)/(z) l'astratto
non trasferisce; (ii) testimone-prima-di-assert; (kk) coniugare
l'interprete; (ll) washout; (mm) niente confronti sotto cap, parametri
assertati; (u) ogni statistica di vicinato va scontata della scia; (ee)
minimi su TUTTI i nodi quando servono.
