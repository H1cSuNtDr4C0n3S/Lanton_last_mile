# RC2 — LEMMI 0b.U3, INVARIANTE DEL MONITOR E MAPPA TEMPORALE (v9 = verdetto /13: L-SCIA-J PROMOSSO [T] con provenienza D corretta; v8 in 03f165f, v7 in 52b09f6, v6 in f335cbf, v5 in d713a6f, v4 in 3b735d6, v3 in 91a78b6, v2 in 0f4348a, v1 in 2eb096e)

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
Aggiunte del verdetto /11 (sezioni 6–8): **L-URHO** (cofinalità per
ogni raggio fisso ρ, stessa prova di L-U3b con N_ρ finito, sotto il
fatto B–T); **L-U7a.2** (direzione utile sotto U₇ — RIDIMOSTRATA come
nuova contrappositiva per-passato: NON segue per restrizione logica da
L-U3a.2, perché la premessa ∀f ¬R_f^{U7} è PIÙ DEBOLE di ∀f ¬R_f^{U3});
**L-FL7** (Forced-L₇, stesura formale — promuovibile dopo saldatura).
Verdetto /12 (2026-07-25): **L-URHO, L-U7a.2 e L-FL7 PROMOSSI** con
gli statuti dichiarati (L-URHO: sotto il fatto B–T, come L-U3b;
L-U7a.2: [T] per-passato, con la coda "Muro con intorno N₇"
condizionale a B–T via L-URHO; L-FL7: [T] nello statuto dichiarato,
clausola "cosa NON afferma" invariata). NUOVO: **L-SCIA-J** (sez. 8b,
bozza formale in attesa di pannello) — il prefisso minimo per j
determina cella e colore della Scia indipendentemente dai bit
anteriori; fase temporale dichiarata (cella NERA a t⁻). CORREZIONE
ESSENZIALE dei quantificatori (recepita in PREREG_RC2_PONTE v13):
una contraddizione della Scia è CONDIZIONATA a deep — dimostra
deep(e) ⇒ ⊥ (ogni realizzazione ha l'evento KNOWN), NON
l'impossibilità della realizzazione: lo stato si chiama COND-KILL,
non "potato", e l'eliminazione del ramo esige la futura congiunzione
con L-OBL ⇒ deep; inoltre R_f^{U7} = ∪_{k,j} R_{f,k,j}^{U7} —
uccidere un singolo (f,k,j) NON elimina la firma: il gate per
costruire L-OBL è ∃f ∀(k,j) compatibili: COND-KILL (firma
ACTIONABLE). Errata sez. 9: bersaglio vigente = la prima L di
Forced-L₇ (il parent-step è superato dal no-go P0 del /10).
Verdetto /13 (2026-07-25): **L-SCIA-J PROMOSSO [T]** con una
riparazione di provenienza: la tabella D è la CONVENZIONE CINEMATICA
CANONICA del progetto (fondamento deduttivo); la ricostruzione dagli
anchor è una VERIFICA [C], non il fondamento. Le altre due
riparazioni /13 (matrice dichiarata CONDIZIONATA a deep con LLL
eliminato prima dal lemma; mappa first_color = 1 − req e predicato
COND-KILL completo congelati) sono recepite in PREREG_RC2_PONTE v14.

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

## 4d. L-P0 — polarità del parent-step (SALDATO dal verdetto /10: 6 firme interne R-ONLY, 2 esterne L+R, NESSUNA L-ONLY — lemma di soffitto della strategia parent-step)

**Profilo deduttivo finale:** 6 firme interne = `R-ONLY`; 2 firme
esterne = `L+R` nell'astrazione certificata; **nessuna firma è
`L-ONLY`** ⇒ L-OBL sul parent-step non può eliminare integralmente
ALCUNA firma di F₈. È il **no-go della via parent-step** (registrato in
PREREG v11): la macchina L-OBL sul parent-step NON si costruisce.

**Firme interne — deduzione promossa (catena a 6 passi del /10):**
(1) c_par è nella palla-2; (2) C3 ⇒ c_par visitata a m\* ⇒ req(c_par)
non è FREE; (3) m\* è pulito (pend₂ = 0) ⇒ req(c_par) ≠ 0;
(4) quindi req(c_par) = 1; (5) la prima lettura forward nel suffisso
è 1 − req = 0, cioè BIANCA (codifica colore del macchinario: read 0 =
bianco); (6) il parent-step è R. ∎ — la derivazione meccanica resta
come REGRESSIONE d'implementazione, non come fondamento.

**Firme esterne — L+R con modelli astratti ESPLICITI (correzione /10:
"non escluso" da solo è epistemico; il certificato di compatibilità
astratta è l'assegnazione che soddisfa C1/C3/C4-exit/U3):**
- modello R: req(c_par) = 1, prima lettura nel suffisso bianca —
  soddisfa tutti i vincoli certificati;
- modello L: req(c_par) = 0, con visita di vita PRECEDENTE richiesta
  da U3 (fuori dal seme una prima lettura di vita è bianca) — soddisfa
  tutti i vincoli certificati.
Entrambi i modelli esistono ⇒ `L+R` deduttivo nell'astrazione.

--- [testo della bozza v5, conservato sotto per la storia] ---
(BOZZA v5 eseguita sulle due firme esterne; Gate P0 del verdetto /9)

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
seconda deduzione ¬R_{f,R}^{U3}. Decisione /10: la caccia GENERICA a un
invariante per f_R è poco promettente (sotto U3 la lettura R-fresca su
cella esterna è il comportamento naturale di una cella bianca fuori dal
seme; Ledger e Scia non la contrastano direttamente) e NON si apre. La
via nuova preregistrata è **Forced-L₇** (PREREG v11 sez. 3e): evitare
il parent-step e prendere come evento distinto il PRIMO L andando
verso il passato, che sotto U₇ è un L forzato, bounded (profondità
≤ 5) e necessariamente una RILETTURA.

**Statuto.** Bozza deduttiva in attesa di pannello: l'esito `L+R` è
un'enumerazione di compatibilità sotto i SOLI vincoli certificati
elencati — non afferma la REALIZZABILITÀ di alcun ramo (trappole z/ff:
compatibilità ≠ realizzazione); la parte "firme interne ⇒ lettera
forzata da req" è dichiarata DA DERIVARE meccanicamente.

## 6. L-URHO — cofinalità dei record U_ρ per ogni raggio fisso (PROMOSSO dal verdetto /12; stessa prova di L-U3b, parametrizzata; sotto il fatto B–T)

**Definizioni.** Per ρ ≥ 0 fisso: N_ρ = intorno-ρ (Chebyshev) di
supp(seme) ∪ {origine} (FINITO: il seme è finito); record U_ρ = record
y-min stretto z_t con B_∞(z_t, ρ) ∩ (supp(seme) ∪ {origine}) = ∅;
dualità come in L-U3b(i): record U_ρ ⟺ record fuori da N_ρ.

**Enunciato.** Per ogni orbita eterna non-highway esiste una rotazione
C4-sym del frame, dipendente dall'orbita, nella quale i record U_ρ
sono infiniti; in quel frame WLOG, una vietanza di w101 su TUTTI i
record U_ρ realizza il bersaglio del Muro con intorno finito N_ρ.

**Dimostrazione.** Identica a L-U3b con 3 sostituito da ρ: (i) dualità;
(ii) fatto esterno B–T + C4-sym-equivarianza ⇒ infiniti record y-min
stretti nel frame WLOG; (iii) y_t strettamente decrescente ⇒ solo
finiti record dentro il compatto N_ρ; (iv) bersaglio del Muro con
intorno N_ρ. ∎ (SOTTO IL FATTO B–T, come L-U3b.)

## 7. L-U7a.2 — direzione utile sotto U₇ (PROMOSSO [T] dal verdetto /12 — per-passato; la coda "Muro con intorno N₇" resta condizionale al fatto B–T via L-URHO; correzione /11: NON è una restrizione logica di L-U3a.2)

**Perché la restrizione non basta (correzione /11.1).** Da
(∀f ¬R_f^{U3}) ⇒ v2^{U3} NON segue (∀f ¬R_f^{U7}) ⇒ v2^{U7}: la
premessa su U₇ è PIÙ DEBOLE (U₇-passati ⊆ U3-passati ⇒ ¬R_f^{U7} è
implicata da ¬R_f^{U3}, non viceversa). La conclusione è comunque vera
e va ridimostrata con la stessa contrappositiva per-passato.

**Enunciato.** (∀f ∈ F₈: ¬R_f^{U7}) ⟹ v2^{U7}; congiunto con U₇ (seme
fuori palla-7 ⊇ palla-2) e col corollario di T20 per restrizione a
palla-2: nessun passato U₇-valido esiste ⟹ w101 vietata a ogni record
U₇ ⟹ (L-URHO, ρ = 7, frame WLOG) Muro per w101 con intorno N₇.

**Dimostrazione (contrappositiva per-passato, nuova istanza).** Sia P
un passato U₇-valido che viola v2^{U7}: nascita pulita (pend₂ = 0;
posa fuori palla-2 automatica: origine fuori palla-7). Ogni
U₇-passato soddisfa le ipotesi dei per-passato di L-U3a.1
(B_∞(z,2) ⊆ B_∞(z,7)): T24 radicato a w101 ⇒ la nascita sta nel
sottoalbero pulito dell'ultimo nodo di pulizia m\* di P, posa(m\*) in
palla-2; il tratto pulito raggiunge una posa fuori palla (la nascita);
T25 + enumerazione dell'oracolo pigro + C1/C3/C4-exit (tutti
per-passato, validi su P) ⇒ la firma di m\* è una delle 8 residue,
realizzata da P ⇒ ∃f: R_f^{U7}. ∎
(Come per L-U3a.2: m\* ≠ nascita perché posa(m\*) ∈ palla-2 e origine
fuori palla-7 ⇒ il genitore di m\* esiste in P.)

## 8. L-FL7 — Forced-L₇ (PROMOSSO [T] dal verdetto /12, nello statuto dichiarato)

**Ipotesi.** P passato U₇-valido che presenta w101 a un record U₇;
m\* nodo di pulizia di P con posa in palla-2 (Chebyshev ≤ 2).

**Tesi.** Esiste k ∈ [1, 5] tale che il k-esimo prepend da m\* ha
lettera L; e per il MINIMO tale k (la prima L), la cella letta c_L ha
Chebyshev ≤ 2 + k ≤ 7 ed è una RILETTURA (esiste una visita precedente
di c_L in P).

**Dimostrazione.**
(a) Cinematica (L-0b0): ogni prepend sposta la posa di 1 e la cella
letta al prepend k È la posa dopo k prepend ⇒ da cheb(posa(m\*)) ≤ 2
segue cheb(cella letta al prepend k) ≤ 2 + k ≤ 7 per k ≤ 5.
(b) Non-terminazione: la nascita di P ha posa = origine, fuori da
B_∞(z_t, 7) (U₇); le celle lette dei primi 5 prepend hanno cheb ≤ 7 ⇒
nessuna può essere la nascita ⇒ il cammino backward di P sopravvive
oltre i primi 5 prepend.
(c) T23 (Bianchi che Curvano): un cammino all'indietro all-R muore
entro il 5° passo; il cammino backward di P da m\* è valido e
sopravvive (b) ⇒ i prepend 1..5 non possono essere tutti R ⇒ esiste
una L a profondità k ≤ 5.
(d) Prima L = rilettura: sia k\* il minimo; c_L ha cheb ≤ 7 ⇒ dentro
B_∞(z_t, 7) ⇒ FUORI dal supporto del seme (U₇). La lettera L è una
lettura NERA; per il mini-lemma bordo-seme (sez. 4, v3) fuori dal seme
la prima lettura di vita è BIANCA ⇒ la L non può essere una prima
lettura di vita ⇒ esiste una visita precedente di c_L in P. ∎

**Cosa NON afferma (dal /11):** non che la L sia FORGOTTEN (deciderlo
è il compito di L-OBL sull'evento), né che la sua Scia contraddica una
firma (test geometrico 8×5×3 col trasporto del colore, PREREG v13
sez. 3e). Un ramo KNOWN reale NON falsifica questo lemma: falsifica la
successiva marcatura L-OBL/deep. Precisazione /12: quando quel test
trova una contraddizione, produce COND-KILL (deep ⇒ ⊥: ogni
realizzazione ha l'evento KNOWN), NON una potatura del ramo —
l'eliminazione esige la congiunzione con una futura prova
L-OBL ⇒ deep.

## 8b. L-SCIA-J — il prefisso minimo determina la Scia (PROMOSSO [T] dal verdetto /13, con provenienza della tabella D corretta)

**Frame dell'evento (definizione).** Sia e l'evento L al passo forward
t: lettura NERA della cella p_t con heading di lettura h_t
(pre-svolta, = heading d'arrivo). Il frame dell'evento è l'unica
rotazione-C4 + traslazione che porta p_t in (0,0) e h_t a 0. Tabella
D = CONVENZIONE CINEMATICA CANONICA del progetto (fondamento
deduttivo del lemma; è la DX/DY condivisa da tutto il macchinario
certificato, `alpha1/onset_cone_lock.py`: DX = (0,1,0,−1),
DY = (−1,0,1,0)): **D = {0:(0,−1), 1:(1,0), 2:(0,1), 3:(−1,0)}**.
La ricostruzione della stessa tabella dagli anchor a verbale (impl. B
di `alpha1/prereg_fase0_geometry.py`, unicità assertata) è una
VERIFICA [C] dell'implementazione, NON il fondamento (correzione
/13.1). Lo stato all'evento
nel frame anchor è (p_t, h_t), dato da L-0b0 (lo stato backward dopo
il prepend dell'evento) ⇒ la trasformazione evento↔anchor è esplicita
nei due versi (passo 1 del trasporto, PREREG v14 sez. 3e).

**Definizione (indice j).** j = min{ i ∈ {1,2,3} : ℓ_{t−i} = R }
(definito ⟺ (ℓ_{t−1}, ℓ_{t−2}, ℓ_{t−3}) ≠ LLL). Prefisso minimo del
caso j = le svolte ℓ_{t−j}, …, ℓ_{t−1} (una R seguita da j−1 L): in
ORDINE DI PREPEND (continuazione del tratto R^{k−1}L della PREREG)
j=1: `R`; j=2: `LR`; j=3: `LLR`; in ordine forward antico→recente:
R·L^{j−1}.

**Enunciato.**
(a) (posizioni) p_{t−1} = (0,1) senza usare alcuna svolta; se
ℓ_{t−1} = L: p_{t−2} = (−1,1); se inoltre ℓ_{t−2} = L:
p_{t−3} = (−1,0) — la posizione p_{t−i} è funzione delle sole svolte
ℓ_{t−1}, …, ℓ_{t−i+1}.
(b) (Scia) la cella di scia c_j = p_{t−j} (= (0,1)/(−1,1)/(−1,0) per
j = 1/2/3, la terna del verdetto /11) è NERA immediatamente PRIMA
della lettura bersaglio (a t⁻); identità del caso, posizione e colore
sono determinati dal SOLO prefisso minimo — i bit più antichi di t−j
sono irrilevanti.
(c) (LLL, coerente con §86.1) se ℓ_{t−1} = ℓ_{t−2} = ℓ_{t−3} = L
allora p_{t−4} = (0,0): la cella dell'evento è stata visitata a t−4 e
ai passi t−3, t−2, t−1 l'automa ne dista Chebyshev 1 ⇒ l'anello-2 non
è mai attraversato dopo quella visita ⇒ (tavola di L-MON) la cella è
KNOWN a t ⇒ la lettura dell'evento è in-window, NON deep₁.

**Dimostrazione.** Relazioni forward (convenzioni di L-0b0):
p_s = p_{s−1} + D[h_s]; h_s = h_{s−1} + 1 se ℓ_{s−1} = R,
h_{s−1} − 1 se ℓ_{s−1} = L (mod 4). All'indietro dall'evento, con
(p_t, h_t) = ((0,0), 0) nel frame:
- p_{t−1} = p_t − D[h_t] = −D[0] = (0,1) (nessuna svolta usata);
- se ℓ_{t−1} = L: h_{t−1} = h_t + 1 = 1 ⇒ p_{t−2} = (0,1) − D[1] =
  (−1,1);
- se inoltre ℓ_{t−2} = L: h_{t−2} = 2 ⇒ p_{t−3} = (−1,1) − D[2] =
  (−1,0);
- se inoltre ℓ_{t−3} = L: h_{t−3} = 3 ⇒ p_{t−4} = (−1,0) − D[3] =
  (0,0).
È la mappa dei prepend di L-0b0 applicata 3–4 volte: prova (a) e la
prima parte di (c). ∎(a)
(b): al passo t−j la lettera è R = lettura BIANCA (convenzione bit
§95b: 1 = R = bianca) ⇒ il flip lascia c_j NERA. Le letture
strettamente fra t−j e t sono ai passi t−j+1, …, t−1, sulle celle
p_{t−j+1}, …, p_{t−1}: per (a) tutte distinte da c_j (verifica
finita — j=2: (−1,1) ∉ {(0,1)}; j=3: (−1,0) ∉ {(−1,1), (0,1)});
anche la lettura dell'evento è p_t = (0,0) ≠ c_j, quindi c_j resta
NERA sia a t⁻ sia dopo il passo L (rilevante per l'equivalenza delle
due convenzioni di trasporto, PREREG v14 sez. 3e punto 0). Identità
del caso (definizione di j), posizione (a) e colore usano SOLO
ℓ_{t−j}, …, ℓ_{t−1}. ∎(b)
(c): cheb da (0,0) di p_{t−3} = (−1,0), p_{t−2} = (−1,1),
p_{t−1} = (0,1) è 1 in tutti e tre i passi ⇒ dopo la visita di t−4 la
posizione non raggiunge mai distanza 2 dalla cella (0,0) ⇒ per la
tavola di L-MON lo stato resta KNOWN fino a t ⇒ verdetto in-window
alla lettura t. ∎(c)

**Cosa NON afferma (statuto /12–/13).** Il prefisso minimo determina
la Scia; NON certifica la realizzabilità globale del caso (f,k,j): i
bit anteriori e i vincoli di validità possono restringere quali (k,j)
siano realizzabili — il risultato resta LOCALE e, nell'uso del test
8×5×3, CONDIZIONALE a deep (per l'esclusione di LLL in (c) e per la
semantica COND-KILL, PREREG v14 sez. 3e). Uso di (c) nella matrice
(formulazione scelta dal /13.2): LLL è eliminato PRIMA della matrice
da (c) sotto deep — la decomposizione {j=1,2,3, LLL} dei rami è
esaustiva; la matrice 8×5×3 (senza colonna LLL) è quindi esaustiva
SOLTANTO nel dominio `deep`, mai in assoluto.

## 9. Cosa resta aperto (nessuna promozione)

- **L-OBL** (il bersaglio operativo post-/8): automa retrospettivo
  SEEK0/SEEK2/RESOLVED-{U,K,F} per evento bersaglio distinto, con OUT
  usato per certificare SEEK2; preregistrato in PREREG_RC2_PONTE v9
  sez. 3d. **Bersaglio VIGENTE (errata /12):** la prima L di
  Forced-L₇ (L-FL7, sez. 8; PREREG v13 sez. 3e) — il "primo bersaglio
  = parent-step" delle versioni precedenti è SUPERATO dal no-go P0
  del /10; la macchina si costruisce SOLO per una firma ACTIONABLE
  della matrice 8×5×3. Q_c/Γ (L-REV, sez. 3c) resta la
  sovra-approssimazione GENERALE di soundness — il suo gate deep allo
  stato mobile è ucciso da L-RESET, non la sua soundness.
- La certificazione della VIA B come implementazione (checker con
  controlli espliciti, esca, optimize==0, replay) — L-MON + L-REV sono
  la base deduttiva, non il sostituto.
- I gate di terra di 0b.0 (replay bit-identico: implementazione).
- Le 8 milestone quantitative per-firma (gate della Fase 1, invariato).
- §109: chiuso — nulla qui è una deduzione ¬R_f.
