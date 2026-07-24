# PREREG RC2 — IL PONTE SCIA forward→backward (Fase 0b, pre-§109) (v2 = ERRATA-RC2 applicata; v1 in b85b7db)

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
  lemma (inclusa la convenzione di verso backward vs forward);
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

## 2b. Scelta dell'universo (obbligatoria, ERRATA-RC2.3)

Due universi ammessi; ogni enunciato di Fase 0b DEVE dichiarare quale usa:
- **U0 (attuale):** passato reale completo che presenta w101 a un record
  y-min stretto — il seme è escluso SOLO dalla palla-2 (ipotesi del
  Muro). Nell'anello 3 una L può essere prima lettura di una cella nera
  di seme: lì la componente RILETTA non è deducibile da T20 e i punti
  restano `unknown`.
- **U3 (ipotesi strategica del titolare, DA LAVORARE):** record
  sufficientemente lontani con
  **B_∞(z_t, 3) ∩ (supp(seme) ∪ {origine}) = ∅** — elimina l'ambiguità
  "L fresca da seme" nell'anello 3. Plausibilità dichiarata (NON
  dimostrata): sufficiente al Muro, perché servono record tardivi
  lontani. OBBLIGO: il passaggio ai quantificatori di X6
  (v2 ⟺ T24–T25 ⟺ T26) va RIDIMOSTRATO sotto U3 — non può essere
  inserito silenziosamente in R_f; finché non è ridimostrato, ogni
  risultato sotto U3 porta l'etichetta "condizionale a U3".

## 3. Lemma 0b.2 — località e completezza del dominio (da certificare)

Da dimostrare: il verdetto di marcatura (marcato / non-marcato /
`unknown`) è funzione di un INTORNO FINITO DICHIARATO dello stato
backward — raggio r_0b e profondità di storia d_0b ESPLICITI — cosicché
il dominio D_RC2 delle configurazioni locali ammesse ai punti candidati
è FINITO e la sua enumerazione è COMPLETA (non un campione: due
implementazioni concordi su un campione NON bastano, ERRATA-1.6). Ogni
parametro sound "per caso fattuale" va verificato con controllo
esplicito a ogni valore di raggio (trappola mm).

## 4. Gate 0b.3 — enumerazione + replay forward (solo dopo 0b.0–0b.2)

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
