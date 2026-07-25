# RC2 — LEMMI 0b.U3, INVARIANTE DEL MONITOR E MAPPA TEMPORALE (v5 = bozza Gate P0 di polarità sulle firme esterne; v4 in 3b735d6, v3 in 91a78b6, v2 in 0f4348a, v1 in 2eb096e)

**Statuto (aggiornato dal verdetto del titolare 2026-07-25/6):**
- **PROMOSSI** (con le correzioni notazionali del pannello, applicate
  nel corpo): L-U3a.1, L-U3a.2, L-MON.
- **L-U3b: CHIUSO "sotto il fatto B–T"** — condizionale dichiarato al
  fatto esterno B–T, NON prova autonoma di B–T.
- **L-U3a.3: statuto precisato** — non dimostra che la bicondizionale
  X6 sia falsa in U3; dimostra che la PROVA precedente della direzione
  R_f ⇒ ¬v2 non si relativizza (costruisce un altro passato, non-U3).
- **L-0b0 cinematica/lettere: PROMOSSO [T] dal verdetto /7 e CHIUSO
  nello statuto dichiarato dal verdetto /8** (inversione
  esatta di posa e heading; uguaglianza della cella letta;
  corrispondenza delle lettere; j(k) senza seconda induzione;
  C4-sym-equivarianza; non-morte geometrica distinta dai colori). La
  metà-colori: alternanza sulle riletture [T] via req + CONDIZIONE AL
  BORDO DEL SEME (errata /7, sotto) per la corrispondenza completa sui
  passati reali.
- **NUOVO (verdetto /8): L-RESET** — no-go deduttivo [T]: la visita
  resetta {U,K,F} a K ⇒ Pre_visita({K}) = {U,K,F}; il powerset dello
  stato corrente NON può certificare deep al momento della visita
  (sezione 4c). Il bersaglio operativo passa a L-OBL (obbligazione
  retrospettiva per evento, PREREG_RC2_PONTE v9 sez. 3d).
- **Convenzione DEFINITIVA di indicizzazione (verdetto /7, punto 2):
  0-based** ovunque da qui in avanti (come il codice e L-MON); L-0b0 è
  enunciato in 1-based con raccordo esplicito t = s − 1 — ogni uso
  futuro (L-REV, 0b.1, tool) traduce UNA volta qui.
Il replay resta una verifica dell'implementazione, non parte delle
prove. NON è dimostrato: RC2; la finitezza/soundness della macchina
backward (L-REV, preregistrato in PREREG_RC2_PONTE v7); alcuna
¬R_f^{U3}. §109 resta chiuso; Fase 1 resta chiusa. Ogni enunciato cita
i teoremi consolidati (A-Tn = docs/CONSOLIDATION_108_A.md).
Collisione terminologica risolta (verdetto /6): **C4-sym** = simmetria
rotazionale della regola (L-U3b); **C4-exit** = il vincolo sul genitore
derivato da valid() (il "C4" storico di §96a).

## 1. Definizioni (simboli distinti, decisione operativa punto 1)

- **Record U3:** record y-min stretto z_t (definizione canonica A5)
  con **B_∞(z_t, 3) ∩ (supp(seme) ∪ {origine}) = ∅**.
- **Passato U3-valido:** passato reale completo che presenta w101 a un
  record U3 (origine = posa di nascita, nel frame anchor).
- **R_f^{U3}** (f ∈ F₈): "esiste un passato U3-valido con un nodo di
  pulizia di firma f".
- **v2^{U3}:** restrizione di v2 (Ledger Sporco, O10/T22) ai passati
  U3-validi: "ogni passato U3-valido con posa di nascita fuori
  palla-2 ha pend₂(nascita) ≥ 1". NB: per un passato U3-valido la
  clausola "posa fuori palla-2" è AUTOMATICA (l'origine è fuori
  palla-3 ⊇ palla-2 per definizione di U3).
- **N₃:** intorno-3 (Chebyshev) di supp(seme) ∪ {origine}; il seme è
  finito (configurazione iniziale finita) ⇒ N₃ è finito.

## 2. L-U3b — cofinalità dei record U3 (CHIUSO sotto il fatto B–T; rider WLOG-C4-sym)

**Enunciato (con rider esplicito).** Per ogni orbita eterna non-highway
esiste una rotazione C4 del frame, DIPENDENTE DALL'ORBITA, nella quale i
record y-min stretti U3 sono infiniti; in quel frame WLOG, una vietanza
di w101 valida a TUTTI i record U3 realizza il bersaglio del Muro
(A-T17) con intorno finito = N₃.

**Dimostrazione (condizionale al fatto esterno B–T; chiusura /6 come
condizionale dichiarato).** (i) z ∉ N₃ ⟺ dist_∞(z, supp(seme) ∪
{origine}) > 3 ⟺ B_∞(z,3) ∩ (supp(seme) ∪ {origine}) = ∅: quindi
"record U3" = "record y-min stretto fuori da N₃".
(ii) Fatto ESTERNO B–T (teorema di letteratura, citato come tale — la
fonte a verbale del rider è CONE_LOCK §87.6, NON la parentetica di
A-T17, che non ha statuto proprio nei quattro strati): ogni orbita
eterna è illimitata ⇒ la bounding box cresce ⇒ almeno UNA delle quattro
pareti avanza infinite volte ⇒ infiniti record stretti in ALMENO UNA
direzione; la regola è C4-sym-EQUIVARIANTE (una rotazione di 90° del
piano con rotazione degli heading coniuga la dinamica senza scambiare
R/L) ⇒ esiste una rotazione del frame, dipendente dall'orbita, in cui
la direzione avanzante è y-min: in quel frame i record y-min stretti
sono infiniti (è esattamente il "WLOG per C4-simmetria" di §87.6, qui
reso ESPLICITO come parte dell'enunciato).
(iii) Lungo la successione dei record y-min stretti la quota y_t è
strettamente decrescente ⇒ tutti tranne al più un numero finito cadono
fuori dal compatto N₃ ⇒ infiniti record U3 nel frame WLOG.
(iv) Il bersaglio del Muro è "presentare w101 come suffisso è
impossibile a ogni record y-min stretto con posa fuori da un intorno
finito dell'origine/seme" (nella stessa convenzione WLOG in cui è
formulata l'intera linea dei record, §87.6): una vietanza su tutti i
record U3 lo realizza letteralmente con l'intorno N₃.
∎ (SOTTO IL FATTO B–T: il lemma è chiuso dal pannello /6 come
condizionale dichiarato al teorema esterno B–T + C4-sym-equivarianza;
non è, e non pretende di essere, una prova autonoma di B–T.)

## 3. L-U3a — restrizione puntuale della catena X6 a U3 (direzione utile)

### 3.1 L-U3a.1 — i per-passato restringono gratis

**Enunciato.** T24 (Passo di Pulizia + Tratto Pulito), T25 (Dicotomia
del Tratto Pulito), i vincoli C1/C3/C4-exit dell'oracolo v2 (§96a),
l'ENUMERAZIONE esaustiva delle 40 firme dell'oracolo pigro (§95d: 25
confinate deduttivamente / 15 firme-exit; parte enumerativa di T26:
7/15 uccise da C1/C3/C4-exit ⇒ 8 residue) e il Lemma dell'exit-step
(§96b) valgono per ogni passato U3-valido.

**Dimostrazione (con le ipotesi EFFETTIVE di ciascun enunciato,
correzione della lente).** T24/T25/C1/C3 e l'oracolo pigro NON hanno
alcuna ipotesi spaziale sulla palla: vivono al livello parola/ledger
del camminatore (T24: "per OGNI passato completo che presenta w101 a un
record, senza case-split", §95b; l'oracolo è una sovra-approssimazione
UNIVERSALE — la conoscenza lazy è sottoinsieme di ogni conoscenza
reale). C4-exit usa solo valid() (ogni cella letta ha y ≥ 1). Tutti
sono quantificati universalmente su classi che CONTENGONO i passati
U3-validi ⇒ la restrizione di un ∀ a un sottoinsieme è valida.
L'ipotesi spaziale entra SOLTANTO al livello di v2/T20/T22 — e lì il
suo ruolo preciso è quello dichiarato in L-U3a.2. ∎

### 3.2 L-U3a.2 — la direzione utile al Muro

**Enunciato (con l'attribuzione precisa dell'ipotesi spaziale,
verdetto /6: U3 NON serve a definire v2 — serve, col ledger T20/T22, a
trasformare pend₂ ≥ 1 in contraddizione).**
(∀f ∈ F₈: ¬R_f^{U3}) ⟹ v2^{U3}. Poi, separatamente: per il COROLLARIO
di T20 per restrizione a palla-2 (pend₂(nascita) ≥ 1 ⟺ ≥ 1 cella nera
di SEME in palla-2 visitata — il pending è per-cella; uso già canonico
in T22), v2^{U3} esige una cella di seme in palla-2 a ogni nascita; U3
NEGA il seme in palla-3 ⊇ palla-2 ⇒ la congiunzione è una
contraddizione ⇒ **nessun passato U3-valido esiste** ⟹ w101 vietata a
ogni record U3 ⟹ (con L-U3b, nel frame WLOG) **Muro per w101 con
intorno N₃**.

**Dimostrazione (contrappositiva della prima implicazione).** Sia P un
passato U3-valido che viola v2^{U3}: nascita con pend₂ = 0 (pulita; la
posa è fuori palla-2 automaticamente). Per T24 radicato a w101
(pend₂(w101) = 6) la nascita appartiene al sottoalbero pulito
dell'ULTIMO nodo di pulizia m* di P, con posa(m*) in palla-2. Il tratto
pulito da m* raggiunge una posa fuori palla (la nascita stessa, fuori
palla-3): per T25 (dicotomia) il primo passo fuori esiste; per
l'enumerazione dell'oracolo pigro (L-U3a.1) la firma (cella, heading)
di m* è una delle 15 firme-exit, e per C1/C3/C4-exit (validi su P,
L-U3a.1) è una delle 8 RESIDUE. Nota di completezza: m* ≠ nascita,
perché posa(m*) ∈ palla-2 mentre l'origine è fuori palla-3 — dunque il
genitore di m* è un nodo di P e C3/C4-exit si applicano. m* è un nodo di P,
che è U3-valido ⇒ R_f^{U3} per quella f. ∎
(Caso nascita sporca: pend₂ ≥ 1 = v2^{U3} soddisfatta su P; caso
"nascita in palla": non esiste sotto U3.)

### 3.3 OSSERVAZIONE L-U3a.3 — la bicondizionale X6 NON relativizza in silenzio (statuto preciso, verdetto /6: NON è dimostrato che la bicondizionale sia FALSA in U3; è dimostrato che la prova precedente della direzione R_f ⇒ ¬v2 non si relativizza, perché costruisce un ALTRO passato, non-U3)

La direzione opposta di T26 ("firma realizzata ⟹ v2 falsa", via Lemma
dell'exit-step) NON passa a U3 con la stessa costruzione: il testimone
clean-far prodotto dall'exit-step ha posa (= origine del candidato
passato-nascita) sulla CELLA D'USCITA della firma. Deduzione geometrica
(primaria, indipendente dal censimento): posa(m*) ∈ palla-2, il passo
d'uscita è unitario e la cella d'uscita è fuori palla-2 ⇒ la cella
d'uscita ha Chebyshev ESATTAMENTE 3 dal record — vale per QUALUNQUE
firma-exit, presente o futura. Conferma di terra: le 8 celle d'uscita
censite dalla Fase 0 (`alpha1/prereg_fase0_geometry_summary.json`)
hanno tutte Chebyshev 3. ⇒ il testimone ha origine DENTRO B_∞(z_t,3) ⇒
NON è un passato U3-valido. Quindi:
- R_f^{U3} ⟹ ¬v2^{U3} **non segue** dalla catena X6 così com'è
  (potrebbe valere per altre costruzioni: APERTO, non affermato);
- resta vero e invariato: un testimone di QUALUNQUE firma falsifica v2
  nell'universo U0 (F1-v2 della prereg RIENTRO-SCIA);
- per il Muro serve SOLO la direzione L-U3a.2, che regge.
Dicitura DECISA dal verdetto /6: 0b.U3-a = "direzione utile
relativizzata", non bicondizionale (applicata in PREREG_RC2_PONTE v7,
sezione 2b).

## 4. L-MON — invariante del monitor (Via B, forma del verdetto 2026-07-25/5)

**Semantica forward di riferimento (dal macchinario certificato C6,
`alpha1/halo_occupancy_profile.py`, righe 152–222).** Al passo t (ant
in c, che legge c): (1) i predicati sono calcolati PRIMA di ogni
aggiornamento: visited := c ∈ last; deep1 := visited ∧ c ∉ known
(righe 157–158; NEL MACCHINARIO sono valutati solo alle letture NERE,
ramo `if isb:` riga 155 — il monitor ESTENDE la stessa formula
color-free a ogni lettura, e il replay della Via B confronta dove
entrambi sono definiti); (2) last[c] := t; known ∋ c (214–215,
INCONDIZIONATI a ogni passo); (3) mossa unitaria (217); (4)
known.discard di OGNI cella dell'anello Chebyshev-2 attorno alla NUOVA
posizione (219–222, incondizionato). last = celle visitate almeno una
volta; known ⊆ last.

**Convenzione temporale (dichiarata una volta per tutte, verdetto /6):
last_t, known_t e S_t denotano lo stato IMMEDIATAMENTE PRIMA della
lettura del passo t.** Nessun altro uso di t⁻ nel seguito.

**Invariante (per ogni cella fissata c, da S_t del verdetto):**
S_t(c) = UNSEEN se c ∉ last_t; KNOWN se c ∈ known_t; FORGOTTEN se
c ∈ last_t \ known_t. Con known_t ⊆ last_t i tre casi sono disgiunti ed
esaustivi.

**Teorema (equivalenza monitor ↔ known/last).** La tavola totale del
monitor (PREREG_RC2_PONTE v5/v6, ordine a 4 passi) calcola esattamente
S_t(c) per ogni c e ogni t; corollario:
**la lettura del passo t su c è deep₁ ⟺ S_t(c) = FORGOTTEN** (e
fresh ⟺ UNSEEN, in-window ⟺ KNOWN).

**Dimostrazione (induzione sui passi).**
- known ⊆ last: l'inserimento in known (2) è simultaneo a last[c] := t;
  il discard (4) solo rimuove. ∎ (sotto-invariante 0)
- Sotto-invariante 1 (completezza dell'anello): dopo il punto (4) di
  ogni passo, ogni cella di known dista ≤ 1 (Chebyshev) dalla posizione
  corrente. Base: known vuoto. Passo: la cella visitata entra a
  distanza 0 e dopo la mossa unitaria dista 1; ogni altra cella di
  known distava ≤ 1 e dopo la mossa dista ≤ 2 (la mossa è unitaria,
  la metrica è Chebyshev); se dista esattamente 2 è sull'anello ed è
  rimossa da (4); le rimanenti distano ≤ 1. ∎ — quindi NESSUNA cella
  known può superare la distanza 2 senza attraversare l'anello: il
  discard del solo anello-2 è completo, e la transizione
  KNOWN→FORGOTTEN del monitor ("posizione dopo la mossa a Chebyshev
  2") coincide col punto (4).
- Base dell'induzione principale: t = 0, last = known = ∅ ⇒
  S_0 ≡ UNSEEN = stato iniziale del monitor. ∎
- Passo, caso c = cella letta: il verdetto usa lo stato PRE-aggiornamento
  (1) = S_t(c) (convenzione temporale sopra) — righe 1/3/6 della tavola
  (fresh/in-window/deep dai
  tre casi di S); poi (2) mette c in last ∩ known ⇒ S = KNOWN =
  "visita ⇒ KNOWN"; dopo la mossa (3) c dista 1 dalla nuova posizione
  ⇒ non è sull'anello ⇒ (4) non la tocca ⇒ resta KNOWN (righe 1/3/6
  della tavola + impossibilità geometrica: distanza 1 ≠ 2). ∎
- Passo, caso c ≠ cella letta: (2) non tocca c; se c è sull'anello-2
  della nuova posizione: se c ∈ known ⇒ discard ⇒ c ∈ last \ known ⇒
  S: KNOWN → FORGOTTEN (riga 4); se c ∉ known il discard è un no-op ⇒
  UNSEEN resta UNSEEN (guardia: la distanza 2 non crea visite
  precedenti), FORGOTTEN resta FORGOTTEN (righe 2 e 7). Se c non è
  sull'anello: nessun aggiornamento ⇒ stato invariato (righe 2, 5, 7).
  ∎
- Corollario: deep1 (riga 158) = visited ∧ c ∉ known = c ∈ last \ known
  = [S_t(c) = FORGOTTEN]; fresh = c ∉ last = UNSEEN; in-window =
  c ∈ known = KNOWN. ∎

**Ipotesi usate (dichiarate):** mossa unitaria per passo (dinamica
canonica CLAUDE.md §2); l'ordine (1)(2)(3)(4) del macchinario C6. Il
replay (Gate 0b.3 / certificazione Via B) verifica l'IMPLEMENTAZIONE
del monitor contro questo lemma, non il lemma.

## 4b. L-0b0 — mappa temporale backward–forward (bozza dimostrata, in attesa di pannello; punto 4 della decisione /6)

**Convenzioni.** Dinamica forward (CLAUDE.md §2): al passo s l'automa in
posizione p_s con heading h_s legge la cella p_s con lettera ℓ_s
(R = lettura bianca, L = nera); svolta h_{s+1} = h_s + 1 se R (orario) /
h_s − 1 se L (mod 4); flip; mossa p_{s+1} = p_s + D[h_{s+1}].
Camminatore all'indietro (§92a): stato (posa, h); prepend della lettera
b: cella letta cn = posa − D[h]; heading nuovo = h − 1 se R / h + 1 se
L; posa nuova = cn. Passato completo di lunghezza T = N + 101 che
presenta w101 al record; stato forward finale (p_{T+1}, h_{T+1}) =
anchor (origine, heading-su). L'INPUT del camminatore è la sequenza
rovesciata ℓ_T, …, ℓ_1 (dichiarazione esplicita, correzione della
lente). Tutte le coordinate nel frame anchor; le relazioni forward
valgono invariate nel frame ruotato per C4-sym-equivarianza (L-U3b):
la rotazione ruota coerentemente coordinate e heading
(rot_k(D[h]) = D[h+k]).
Il camminatore qui è la MAPPA CINEMATICA PURA (posa, h); per il replay
di un passato reale la macchina con guardie non muore mai: la gamba
y ≥ 1 segue dal record STRETTO (definizione canonica A5: ogni cella
letta prima del record ha y ≥ 1 nel frame anchor, e il record stesso
non è mai stato letto prima), la gamba req è la coerenza dei colori
(mini-lemma sotto).

**Enunciato (chiude la mappa (iii) di 0b.0).** Per ogni k ∈ [0, N]:
dopo k prepend il camminatore è nello stato
**(posa_k, h_k) = (p_{N−k+1}, h_{N−k+1})** — posizione e heading del
passo forward N−k+1 (per k = 0: lo stato d'ingresso di w101); e per
k ≥ 1 la cella letta dal k-esimo prepend è **p_{j(k)}** con lettera
**ℓ_{j(k)}**, j(k) = N − k + 1: posizione, heading, cella letta e
lettera del prepend k coincidono con quelli del passo forward j(k).

**Dimostrazione (UNICA induzione su m ∈ [0, T] prepend dall'anchor;
ristrutturata su indicazione della lente — la base non usa il passo).**
Base m = 0: lo stato è l'anchor (p_{T+1}, h_{T+1}) PER DEFINIZIONE del
frame (nessun contenuto).
Passo: sia lo stato dopo m prepend (p_{s+1}, h_{s+1}) con
s = T − m. Il prepend m+1 processa la lettera ℓ_s. Cella letta:
cn = p_{s+1} − D[h_{s+1}] = p_s (dalla mossa forward
p_{s+1} = p_s + D[h_{s+1}]). Heading nuovo: se ℓ_s = R,
h_{s+1} − 1 = h_s (dalla svolta forward h_{s+1} = h_s + 1); se
ℓ_s = L, h_{s+1} + 1 = h_s. Posa nuova = cn = p_s. Quindi lo stato
dopo m+1 prepend è (p_s, h_s) e la cella letta è p_s con lettera
ℓ_s. ∎
Specializzazioni: m = 101 dà (p_{N+1}, h_{N+1}) = lo stato d'ingresso
di w101 — l'identità con l'exact_state del CODICE (che è la traccia
forward ri-ancorata, non un processamento all'indietro) è esattamente
questa istanza del lemma; k = m − 101 dà l'enunciato con
j(k) = N − k + 1.

**Mini-lemma dei colori (v3 = ERRATA del verdetto /7: separa
ALTERNANZA e BORDO-SEME — la v2 li sovrapponeva).**
(a) ALTERNANZA (deduttiva, certificata da req): per ogni cella, ogni
RILETTURA vede il FLIP della lettura precedente (la cella si inverte
dopo la lettura e non cambia altrimenti, CLAUDE.md §2); il ledger req
implementa esattamente questo (req(c) = flip(colore letto), aggiornato
a ogni visita, §92a) ⇒ **req-coerenza ⟺ alternanza corretta SULLE
RILETTURE**. ∎
(b) BORDO-SEME (condizione AGGIUNTIVA, NON certificata da req): nel
codice una cella FREE accetta entrambe le letture — la parola
ricostruisce un SEME INDOTTO, non verifica un seme fissato. Per un
passato completo sul seme S va aggiunta la condizione al bordo:
firstread(c) = NERO se c ∈ S, BIANCO se c ∉ S. Sotto U3, per le celle
sorvegliate (entro B_∞(z_t, 3), dove il seme è assente): prima lettura
BIANCA.
**Statuto per strato di 0b.0 (aggiornato /7):** (i)/(ii)/(iii) e la
metà-lettere di (iv): **[T] PROMOSSI** (verdetto /7); metà-colori di
(iv): [T] per l'alternanza sulle riletture + condizione al bordo del
seme DICHIARATA (la corrispondenza completa sui passati reali la
richiede); i gate G0 §92a (1500×2, campionario) e §93a restano
verifiche [C] dell'IMPLEMENTAZIONE, come il replay di terra di 0b.0
(10 controesempi §94 + ≥100 estensioni). Indici: convenzione DEFINITIVA
0-based (statuto in testa); L-0b0 resta 1-based col raccordo t = s − 1.

## 4c. L-RESET — il reset della visita è un no-go esatto per il Pre dello stato corrente ([T], registrato dal verdetto /8)

**Tavola forward per l'alfabeto locale a_c = (v_c, r_c)** (collasso
della tavola totale di L-MON sui tre eventi raggiungibili):

| stato prima | visita (1,0) | no visita, anello 2 (0,1) | altro (0,0) |
|-------------|--------------|---------------------------|-------------|
| U           | K            | U                         | U           |
| K           | K            | F                         | K           |
| F           | K            | F                         | F           |

**Enunciato.** ∀ s ∈ {U, K, F}: δ_c(s, visita) = K. Quindi
**Pre_{(1,0)}({K}) = {U, K, F}**: attraversando all'indietro la lettura
candidata, l'inverso del monitor non può sapere se immediatamente prima
la cella fosse UNSEEN, KNOWN o FORGOTTEN — la visita CANCELLA il
passato dello stato.

**Dimostrazione.** Immediata dalla colonna "visita" della tavola (righe
1/3/6 della tavola totale di L-MON: UNSEEN+visita→KNOWN,
KNOWN+visita→KNOWN, FORGOTTEN+visita→KNOWN). ∎

**Corollario (il ROSSO di utilità del /8).** U3 + lettera L eliminano
U, ma lasciano Q_c = {K, F} ≠ {F}: il gate deep su Q_c allo stato
temporale mobile NON può mai scattare al momento della visita. NON è
una falsificazione di RC2: è la falsificazione della speranza che il
semplice Pre dello stato corrente certifichi retroattivamente il
pre-stato della visita. Il bersaglio operativo corretto è
l'OBBLIGAZIONE RETROSPETTIVA per evento distinto (L-OBL,
PREREG_RC2_PONTE v9 sez. 3d): non conservare lo stato monitor
corrente, ma scandire il passato dall'evento bersaglio (SEEK0/SEEK2)
fino alla visita precedente o alla nascita.

## 4d. L-P0 — polarità del parent-step (BOZZA eseguita sulle due firme esterne, in attesa di pannello; Gate P0 del verdetto /9)

**Setup (punto 1 del Gate P0).** L'evento parent della firma
f = (c\*, h\*) nel frame anchor: il passo del genitore di m\* legge
c_par = c\* + D[(h\*+1)&3] con h_par = (h\*+1)&3 (geometria del passo di
pulizia, §95h; per le due firme esterne c_par è nell'anello Chebyshev 3:
(−2,3) per ((−2,2), h=1) e (3,2) per ((2,2), h=0) — output Fase 0,
`alpha1/prereg_fase0_geometry_summary.json`). La lettera del parent-step
è la lettura di c_par.

**Punto 2 — la lettera NON è determinata dalla firma (per le firme
esterne).** I vincoli certificati disponibili al nodo m\* sono: C1 (le
nove di palla-2: req=1), C3 (c_par visitata a m\*), C4-exit (y ≥ 1),
U3 (seme e origine fuori da B_∞(z_t,3)). Nessuno di essi fissa
req(c_par) per c_par FUORI dalla palla-2: C1 parla solo delle nove; C3
dà la visita, non la lettera; C4-exit è soddisfatto (y = 3 ≥ 1 e y = 2
≥ 1). Quindi la firma da sola non determina la polarità. [Per contrasto,
per le 6 firme INTERNE c_par è in palla-2 e C3/§96a danno req(c_par)=1
a m\*: la derivazione della lettera dal req va fatta MECCANICAMENTE col
macchinario §96, non a mano — dichiarato fuori da questa bozza.]

**Punti 3–4 — enumerazione deduttiva dei due casi (firme esterne).**
- Ramo R (lettura bianca): compatibile — sotto U3, c_par è fuori dal
  supporto del seme ⇒ una prima-lettura-di-vita è BIANCA (mini-lemma
  bordo-seme, sez. 4 di questo documento) ⇒ il ramo R-fresco è
  naturale; anche una rilettura con parità giusta dà R. Nessun vincolo
  certificato lo esclude.
- Ramo L (lettura nera): non escluso — esige una visita PRECEDENTE di
  c_par con parità di alternanza giusta (sotto U3 la prima lettura è
  bianca, quindi L ⇒ rilettura); nessun vincolo certificato esclude
  tale storia.
**ESITO P0 (bozza): `L+R` per ENTRAMBE le firme esterne.**

**Punto 5 — dichiarazione anticipata (obbligatoria dal /9).** Con esito
`L+R`, **L-OBL da solo NON può provare ¬R_f^{U3} su nessuna delle due
firme esterne**: attacca solo R_{f,L}^{U3}; per ¬R_f^{U3} serve una
seconda deduzione ¬R_{f,R}^{U3} (invariante separato per f_R — APERTO,
nessun candidato dichiarato). Conseguenza operativa (decisione /9,
punto 4): finché non esiste una via dichiarata per il ramo R, L-OBL è
registrato come **RIDUZIONE PARZIALE** e la macchina completa di
Γ(n,e) NON viene costruita.

**Statuto.** Bozza deduttiva in attesa di pannello: l'esito `L+R` è
un'enumerazione di compatibilità sotto i SOLI vincoli certificati
elencati — non afferma la REALIZZABILITÀ di alcun ramo (trappole z/ff:
compatibilità ≠ realizzazione); la parte "firme interne ⇒ lettera
forzata da req" è dichiarata DA DERIVARE meccanicamente.

## 5. Cosa resta aperto (nessuna promozione)

- **L-OBL** (il bersaglio operativo post-/8): automa retrospettivo
  SEEK0/SEEK2/RESOLVED-{U,K,F} per evento bersaglio distinto, con OUT
  usato per certificare SEEK2; preregistrato in PREREG_RC2_PONTE v9
  sez. 3d; primo bersaglio = un parent-step delle due firme a genitore
  esterno. Q_c/Γ (L-REV, sez. 3c) resta la sovra-approssimazione
  GENERALE di soundness — il suo gate deep allo stato mobile è ucciso
  da L-RESET, non la sua soundness.
- La certificazione della VIA B come implementazione (checker con
  controlli espliciti, esca, optimize==0, replay) — L-MON + L-REV sono
  la base deduttiva, non il sostituto.
- I gate di terra di 0b.0 (replay bit-identico: implementazione).
- Le 8 milestone quantitative per-firma (gate della Fase 1, invariato).
- §109: chiuso — nulla qui è una deduzione ¬R_f.
