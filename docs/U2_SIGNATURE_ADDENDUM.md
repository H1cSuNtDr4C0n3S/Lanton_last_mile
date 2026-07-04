# ADDENDUM §96 — U2-LONTANO 4: vincoli sulle firme-exit, il COLLO DELLA PULIZIA, tripwire CP, identita' chirale

**Riepilogo in una frase:** i vincoli di raggiungibilita' deduttivi C1 (il "muro
delle nove": w101 visita 9/10 celle di palla ⇒ a ogni nodo pulito hanno req=1),
C3 (la cella del genitore e' visitata) e C4 (la cella del genitore ha y≥1)
uccidono **7 delle 15 firme-exit** dell'oracolo §95d — inclusa la promozione a
fatto DEDUTTIVO del confinamento della firma reale ((−1,2),3) — lasciando **8
firme residue, tutte a exit-diretta**, per le quali vale la collezione:
*exit-step sempre realizzabile* ⇒ **v2 vera ⟺ nessuna delle 8 e' realizzabile
come nodo di pulizia**; le cacce per-firma (1242 job, 733M passi, 4 politiche,
controllo positivo obbligatorio) non ne realizzano NESSUNA e censiscono **603
pulizie reali TUTTE con la stessa firma ((−1,2), heading sx h=3)** — il
**COLLO DELLA PULIZIA**: la palla si pulisce da una porta sola (empirico,
etichettato PC-only dal pannello; candidato-teorema per §97). In parallelo: l'intuizione di Michael
(violazione di parita' debole ↔ chiralita' della formica) e' stata valutata e
ha fruttato (1) l'**identita' chirale R−L=ΔB** (deduttiva, gia' implicita a
§79; il winding della highway 12 = 58−46 E' la carica nera per periodo;
heading ≡ ΔB mod 4) e (2) il **TRIPWIRE SPECCHIO** (`mirror_tripwire.py`,
M0–M4 verdi): la coniugazione CP (x→−x, dx↔sx, R↔L **e scambio della
regola**) e' verificata esatta su dinamica forward, exact_state/pend₂,
clean_subtree e oracolo — e in-run ha beccato DUE assunzioni di simmetria
sciatte (bit-swap nudo = mondo a colori invertiti, 256/256 req flippate;
l'insieme delle firme-exit NON e' M-chiuso perche' l'oracolo e' chirale,
diff simmetrica 12): il tripwire funziona da subito come rilevatore di
confusioni P-vs-CP, che e' esattamente il suo scopo.

Strumenti nuovi: `alpha1/u2_far_clean_oracle_v2.py`,
`alpha1/u2_far_signature_hunt.py`, `alpha1/mirror_tripwire.py` (+ summary).

## 96a. Oracolo v2: i vincoli C1/C3/C4 (7 firme uccise su 15)

**C1 — il muro delle nove (deduttivo).** `exact_state(w101)` visita 9 delle 10
celle di palla-2 utili ({|x|≤2, y∈{1,2}}): manca solo **(1,1)** (GATE W1 —
coerente col Blocco Antico §89: (1,1) e' fuori dal footprint di w101). Ogni
suffisso di ogni albero radicato a w101 contiene w101 ⇒ le 9 celle sono
VISITATE a ogni nodo ⇒ a ogni nodo con pend₂=0 hanno req≠0, cioe' **req=1**.
Nel tratto pulito una cella req=1 e' morta (R irrealizzabile, L aprirebbe
pend₂): l'unica cella di palla percorribile dal tratto e' (1,1), al piu' una
volta.

**C3 — la catena del genitore.** Il passo di pulizia arriva dalla cella
c_par = c* + D[(h*+1)&3], letta dal passo del genitore ⇒ visitata a m* ⇒ se
in palla, req=1.

**C4 — la riga zero.** c_par e' una cella letta ⇒ y≥1 (valid()). La firma
((2,1),3) ha c_par=(2,0): **nessun genitore possibile, firma irrealizzabile.**

Esito (`u2_far_clean_oracle_v2.py`, gate W1/O0/E1/E2 verdi, esca E1 = senza
vincoli riproduce esattamente le 15 di §95d, esca E2 = C1 monco cambia le
residue): **32/40 firme non-exit (27 confinate + 5 C4-irrealizzabili),
7/15 exit uccise**, tra cui la promozione del confinamento della firma reale
((−1,2),3) da fatto concreto (req((0,2))=1 misurato) a **fatto deduttivo**
(le nove). Restano **8 firme residue**, tutte con exit al PRIMO passo (la
conoscenza in-palla non puo' bloccare un passo che esce subito):
`(−2,1)h1, (−2,2)h0, (−2,2)h1, (−1,2)h0, (0,2)h0, (1,2)h0, (2,2)h0, (2,2)h3`.

**Lemma della Catena di Chiusura** (riscritto dal pannello — la prima
versione "ingresso fresco dal bordo" era un BUCO, vedi 96e): al nodo di
pulizia m* di firma (c*, h*), i passi immediatamente precedenti in palla
sono R su celle p_k distinte da {c*, p1..p_{k−1}} per k≤3, e i pending si
ACCUMULANO all'indietro (ogni R in palla della catena e' R-su-pending:
pend₂(n_k) ⊇ {c*, p1, ..., p_{k−1}} — sotto w101 le nove sono sempre
visitate, mai fresche). Il run di R in palla e' ≤3: il 4° passo all'indietro
non puo' essere R (p4 = c* renderebbe req(c*)=1 al genitore ⇒ pulizia
irrealizzabile) ed e' forzatamente **L su c* stessa** (l'apertura del
pending di c*), con p5 = c*+D[h*−1] vicino di c*: la catena puo' proseguire
in palla indefinitamente con aperture L — NESSUN enunciato di ingresso dal
bordo. Conferma di terra (lente indipendente): run-R = 3 e pattern RRRRL
attorno a TUTTI gli 8 nodi puliti reali.

## 96b. La riduzione finale: v2 ⟺ 8 firme irrealizzabili

**Lemma dell'exit-step.** Da un nodo di pulizia realizzato con firma residua,
il passo verso la cella d'uscita cn (fuori palla, y≥1) e' SEMPRE realizzabile:
se cn e' FREE entrambe le letture vanno; se e' visitata la lettura forzata
(=req) e' realizzabile per definizione; in ogni caso pend₂ resta 0 (cn fuori
palla) e la posa e' fuori. ⇒ **realizzare una firma residua ⟹ testimone
clean-far ⟹ v2 falsa.** Con la Dicotomia §95 e l'oracolo v2:
**v2 ⟺ nessuna delle 8 firme residue e' realizzabile come nodo di pulizia.**
Il fronte, da "ogni possibile stato pulito" (§94), e' ora **8 oggetti finiti
etichettati (cella, heading)**.

## 96c. Cacce per-firma: il COLLO DELLA PULIZIA (negativo etichettato PC-only)

`u2_far_signature_hunt.py` (run finale post-pannello, azioni B2/B3): per
ciascuna delle 8 residue + il **controllo positivo ((−1,2),3)** (GATE S0: se
il cacciatore non ritrova la firma realizzabile nota, il negativo non vale),
4 politiche (PA milestone-greedy con steering finale verso (c_par, h_par);
PB passeggiate profonde random; PC mutazione dei testimoni §94/§95;
PD "palla-cameriere" aggiunta dal pannello per campionare il corno
apertura-L-in-palla del Lemma della Catena), 36 fuggenti + 10
parole-testimone come basi, 1242 job, 4 restart × 150k passi, **733M passi
totali** (12 worker, 226 s):

- **8 firme residue: 0 hit** (82,8M passi di caccia per firma);
- controllo positivo: **20 hit** (S0 verde);
- censimento per-politica di OGNI transizione pend₂ 1→0: **603 pulizie,
  TUTTE con firma ((−1,2), 3) e TUTTE da PC** — PA, PB e PD non hanno
  prodotto NEMMENO UNA pulizia in 733M passi.

**Lettura onesta (il pannello l'ha imposta, azione B2):** il potere positivo
dimostrato copre la SOLA famiglia PC (mutazione dei dintorni dei testimoni
noti): pulire la palla da zero e' talmente raro che le cacce cieche non ci
riescono MAI. Il negativo sulle 8 residue resta un negativo, etichettato
"PC-only" (trappola hh dichiarata); il corno apertura-L e' stato campionato
da PD senza esito positivo NE' negativo informativo (PD non pulisce affatto).

**Il collo della pulizia (empirico, candidato-teorema §97):** 603+597 pulizie
osservate in due run, TUTTE con la stessa firma: la palla-2 si pulisce SOLO
chiudendo per ultima (−1,2), arrivando da c_par=(−1,1) con h_par=0 (firma
h*=3). Se promosso a teorema ("ogni nodo di pulizia ha firma ((−1,2),3)"),
v2 e' TEOREMA per l'oracolo v2 (quella firma e' confinata da C1) e il **Muro
si chiude senza pavimento**. La via realistica non sono cacce piu' grosse ma
l'enumerazione (96g.1).

## 96d. L'intuizione chirale (valutazione, esiti)

Proposta di Michael: analogia con la violazione di parita' dell'interazione
debole — la regola R-su-bianco/L-su-nero e' massimalmente chirale (V−A), P da
sola violata, "CP" (specchio + scambio RL) esatta.

**(1) Identita' chirale R−L=ΔB (adottata come assioma disponibile).**
Deduttiva in una riga: ogni R dipinge un nero (+1), ogni L lo cancella (−1) ⇒
su ogni segmento ΔB = #R − #L; R/L ruotano h di ±1 ⇒ Δheading ≡ ΔB (mod 4).
Verifica meccanica: 200 config casuali, 0 violazioni; **W0: 58−46 = 12 = rot
esatto** (il winding dell'autostrada E' la carica nera netta per periodo,
mod 4 = 0 = heading periodico); i controesempi §94 hanno tutti R−L ≡ 1
(mod 4) (coerenza di frame). ONESTA': l'identita' era GIA' implicita a §79
(creazioni−distruzioni = 58984−47016 = +11968 = crescita del pool) — non e'
un fatto nuovo, e' la sua forma pulita di legge di conservazione. Non e'
entrata nei certificati §96 (il ledger dei pending vive su GF(2), l'identita'
e' Z/Z4): resta disponibile per il per-pose PP0 (§94d, da raffinare) come
coordinata affine Z/4 che accoppia composizione della parola e heading.

**(2) Tripwire specchio (adottato, `mirror_tripwire.py`, M0–M4 verdi).**
Involuzione M: (x,y)→(−x,y), heading dx↔sx, bit R↔L **+ scambio della regola**
(l'interprete specchio legge read=bit invece di read=1−bit). Gate: M0 dinamica
forward coniugata esatta (25 semi; onset vuota 9977 in entrambi gli universi);
M1 esca: P da sola DIVERGE (la violazione di parita' c'e' e il checker la
vede); M2 exact_state/pend₂ commutano con M via interprete specchio; M3
clean_subtree bit-identico; M4 oracolo coniugato (exit_specchio ==
M(exit_standard)), con esca: l'insieme exit NON e' M-chiuso in se' (diff 12).
**Lezione metodologica pagante gia' in-run (2 volte):** (i) il bit-swap nudo
senza scambio della regola produce il mondo a COLORI INVERTITI (256/256 req
flippate sul controesempio 0): scambiare i dati senza scambiare la semantica
non e' la simmetria; (ii) l'oracolo e' intrinsecamente chirale (lo spiral
confinato e' all-R): pretendere M-chiusura dell'insieme exit era un'assunzione
sciatta, la coniugazione giusta passa per l'oracolo specchio. Il tripwire e'
esattamente il rilevatore di questa classe di bug (parente di §86.6/§89c).

## 96e. Pannello §96 (3 lenti, in sessione)

- **Lente logica** (claim A–F): A/B/C/F REGGONO (A: giustificazione di frame
  verbalizzata — l'anchor e' definito dall'estremita' recente condivisa,
  la dinamica e' equivariante ⇒ il footprint di w101 e' lo stesso a ogni
  nodo; F: m_head=(−h)%4 e' la riflessione dei versori e M∘rot_k=rot_{−k}∘M
  ⇒ la coniugazione x→−x sopravvive all'anchor; il flip totale del bit-swap
  nudo e' DEDUTTIVO, non solo misurato). D REGGE deduttivamente con caveat
  sulla forza del negativo (B2, chiuso: vedi 96c). **E BUCO**: "pend₂={c*} a
  ogni livello" era falso (i pending si accumulano) e "ingresso dal
  bordo/fresco" era falso (il 4° passo e' L su c*, la catena puo' restare in
  palla) — riscritto come Lemma della Catena di Chiusura (96a), nucleo
  numerico (run-R ≤3) salvo e confermato di terra.
- **Lente macchinario indipendente**: VERDE 37/37, 0 mismatch (footprint 9
  celle bit-identico; firme dei 23 stati §95 e degli 8 controesempi = unica
  ((−1,2),3); oracolo v1/v2 rienumerato: 15 e 8 firme identiche; 3/3 esche
  del verificatore beccate; bonus: pattern RRRRL e run-R={3:8} — la versione
  corretta di (E) confermata prima ancora della riscrittura). Caveat
  dichiarato: i cert_rows §95 non salvano le parole complete ⇒ verificati i
  campi registrati (la riderivazione completa e' sui 10 controesempi).
- **Lente esche sui checker**: 4/4 beccate (M1: senza C4 risorge esattamente
  e solo ((2,1),3) — C4 necessario per UNA firma, ma necessario; M2:
  footprint corrotto beccato dal gate W1, che e' il gate portante; M3:
  m_head corrotto 0↔2 beccato da M0 — M2 e' strutturalmente cieco a quello
  swap perche' gli heading di posa del set sono quasi tutti dispari,
  verbalizzato nel docstring del tripwire; M4: controllo corrotto ⇒ S0
  ROSSO, e la caccia ridotta ha potere positivo vero — esca non vacua).

Azioni bloccanti B1–B4 del pannello: TUTTE chiuse in sessione (B1 riscrittura
di (E); B2 censimento per-politica strumentato e ri-run; B3 politica PD per
il corno apertura-L + etichetta PC-only sul verdetto; B4 docstring/codice
allineati e conteggio oracolo separato in confinate/C4-irrealizzabili).

## 96f. Trappole nuove

- **(kk) scambiare i dati senza scambiare la semantica non e' la simmetria**
  (TRIPWIRE-CP §96): l'immagine speculare di un'orbita ha i bit scambiati E
  la regola scambiata; interpretare i bit scambiati con la regola standard
  da' il mondo a colori invertiti (req tutte flippate), che e' un universo
  DIVERSO. Ogni test di simmetria deve coniugare l'interprete, non solo
  l'input; un insieme derivato da un oggetto chirale (oracolo all-R) non e'
  M-chiuso e non deve esserlo. Parente di (d) (canon) e dei bug di frame
  §86.6/§89c; il tripwire specchio e' il rilevatore standard da oggi.

## 96g. Domande aperte / programma §97

1. **Teorema del Collo della Pulizia** (il bersaglio): ogni nodo di pulizia
   ha firma ((−1,2),3). Vie: (a) enumerazione esaustiva degli ingressi in
   palla con pend₂={c*} (catena all-R ≤3 passi dal bordo, 96a: il pre-entry
   e' fuori palla, i punti d'ingresso sono FINITI — enumerare (cella
   d'ingresso, heading, c*) e uccidere per req/geometria); (b) vincoli
   d'ordine sulla chiusura dei pending (perche' (−1,2) e' sempre l'ultima?
   whack-a-mole §93/§94 visto come DAG delle chiusure).
   Se il teorema cade: v2 TEOREMA ⇒ Muro chiuso al raggio 2 + intorno.
2. Se (1) resiste: cacce piu' profonde per-firma (budget 10×, politiche
   nuove) o realizzazione di una firma ⇒ v2 falsa e si riparte.
3. Identita' chirale nel per-pose PP0 (Z/4, §94d da raffinare) — bassa
   priorita', alto rapporto costo/beneficio incerto.
4. Ereditati: fuggenti nuove vs nere-D≥400 (§94f.4); retro-nota §91c.3;
   stress-2 bianche; h1=1 (§92).

## 96h. Inventario file (alpha1/)

- `u2_far_clean_oracle_v2.py` (+`_summary.json`) — oracolo v2 con C1/C3/C4,
  gate W1/O0/E1/E2; 8 firme residue.
- `u2_far_signature_hunt.py` (+`_summary.json`, `.log`) — cacce per-firma
  con controllo positivo (S0) e censimento globale delle pulizie.
- `mirror_tripwire.py` (+`_summary.json`) — tripwire CP, gate M0–M4;
  interpreti back_state/clean_subtree/oracolo parametrizzati per chiralita'.
