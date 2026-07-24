# RC2 — LEMMI 0b.U3 E INVARIANTE DEL MONITOR (bozze deduttive pre-§109, IN ATTESA DI PANNELLO)

**Statuto (vincolante):** bozze deduttive richieste dall'ordine dei
lavori (decisione operativa 2026-07-25/2, aggiornata /4, punti 1–3) e
dalla clausola 3 del verdetto 2026-07-25/5 (forma ufficiale del lemma
del monitor). NESSUN
certificato macchina è incluso: il replay resta una verifica
dell'implementazione, non parte della prova. Queste NON sono deduzioni
¬R_f: §109 resta chiuso; Fase 1 resta chiusa. Ogni enunciato cita i
teoremi consolidati (A-Tn = docs/CONSOLIDATION_108_A.md; convenzioni
della testa docs/CONSOLIDATION_108.md). Nulla è "chiuso" finché il
pannello del titolare non lo salda.

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

## 2. L-U3b — cofinalità dei record U3 (con rider WLOG-C4; corretto dal ROSSO della lente logica)

**Enunciato (con rider esplicito).** Per ogni orbita eterna non-highway
esiste una rotazione C4 del frame, DIPENDENTE DALL'ORBITA, nella quale i
record y-min stretti U3 sono infiniti; in quel frame WLOG, una vietanza
di w101 valida a TUTTI i record U3 realizza il bersaglio del Muro
(A-T17) con intorno finito = N₃.

**Dimostrazione (condizionale al fatto esterno B–T; in attesa di
saldatura del pannello).** (i) z ∉ N₃ ⟺ dist_∞(z, supp(seme) ∪
{origine}) > 3 ⟺ B_∞(z,3) ∩ (supp(seme) ∪ {origine}) = ∅: quindi
"record U3" = "record y-min stretto fuori da N₃".
(ii) Fatto ESTERNO B–T (teorema di letteratura, citato come tale — la
fonte a verbale del rider è CONE_LOCK §87.6, NON la parentetica di
A-T17, che non ha statuto proprio nei quattro strati): ogni orbita
eterna è illimitata ⇒ la bounding box cresce ⇒ almeno UNA delle quattro
pareti avanza infinite volte ⇒ infiniti record stretti in ALMENO UNA
direzione; la regola è C4-EQUIVARIANTE (una rotazione di 90° del piano
con rotazione degli heading coniuga la dinamica senza scambiare R/L) ⇒
esiste una rotazione del frame, dipendente dall'orbita, in cui la
direzione avanzante è y-min: in quel frame i record y-min stretti sono
infiniti (è esattamente il "WLOG per C4-simmetria" di §87.6, qui reso
ESPLICITO come parte dell'enunciato).
(iii) Lungo la successione dei record y-min stretti la quota y_t è
strettamente decrescente ⇒ tutti tranne al più un numero finito cadono
fuori dal compatto N₃ ⇒ infiniti record U3 nel frame WLOG.
(iv) Il bersaglio del Muro è "presentare w101 come suffisso è
impossibile a ogni record y-min stretto con posa fuori da un intorno
finito dell'origine/seme" (nella stessa convenzione WLOG in cui è
formulata l'intera linea dei record, §87.6): una vietanza su tutti i
record U3 lo realizza letteralmente con l'intorno N₃.
[niente ∎: il passo (ii) usa B–T esterno + C4-equivarianza — il
pannello salda o respinge il lemma di cofinalità in questa forma.]

## 3. L-U3a — restrizione puntuale della catena X6 a U3 (direzione utile)

### 3.1 L-U3a.1 — i per-passato restringono gratis

**Enunciato.** T24 (Passo di Pulizia + Tratto Pulito), T25 (Dicotomia
del Tratto Pulito), i vincoli C1/C3/C4 dell'oracolo v2 (§96a),
l'ENUMERAZIONE esaustiva delle 40 firme dell'oracolo pigro (§95d: 25
confinate deduttivamente / 15 firme-exit; parte enumerativa di T26:
7/15 uccise da C1/C3/C4 ⇒ 8 residue) e il Lemma dell'exit-step (§96b)
valgono per ogni passato U3-valido.

**Dimostrazione (con le ipotesi EFFETTIVE di ciascun enunciato,
correzione della lente).** T24/T25/C1/C3 e l'oracolo pigro NON hanno
alcuna ipotesi spaziale sulla palla: vivono al livello parola/ledger
del camminatore (T24: "per OGNI passato completo che presenta w101 a un
record, senza case-split", §95b; l'oracolo è una sovra-approssimazione
UNIVERSALE — la conoscenza lazy è sottoinsieme di ogni conoscenza
reale). C4 usa solo valid() (ogni cella letta ha y ≥ 1). Tutti sono
quantificati universalmente su classi che CONTENGONO i passati
U3-validi ⇒ la restrizione di un ∀ a un sottoinsieme è valida.
L'ipotesi spaziale del Muro entra SOLTANTO in v2/T20/T22, dove U3 la
implica per monotonia delle palle (B_∞(z_t,2) ⊆ B_∞(z_t,3): U3 esclude
seme e origine anche dalla palla-2). ∎

### 3.2 L-U3a.2 — la direzione utile al Muro

**Enunciato.** (∀f ∈ F₈: ¬R_f^{U3}) ⟹ v2^{U3}. Congiunto con U3 (seme
fuori palla-3) e col COROLLARIO di T20 per restrizione a palla-2
(pend₂(nascita) ≥ 1 ⟺ ≥ 1 cella nera di SEME in palla-2 visitata — il
pending è per-cella; uso già canonico in T22): (∀f: ¬R_f^{U3}) ⟹ nessun
passato U3-valido esiste ⟹ w101 vietata a ogni record U3 ⟹ (con L-U3b,
nel frame WLOG) **Muro per w101 con intorno N₃**.

**Dimostrazione (contrappositiva della prima implicazione).** Sia P un
passato U3-valido che viola v2^{U3}: nascita con pend₂ = 0 (pulita; la
posa è fuori palla-2 automaticamente). Per T24 radicato a w101
(pend₂(w101) = 6) la nascita appartiene al sottoalbero pulito
dell'ULTIMO nodo di pulizia m* di P, con posa(m*) in palla-2. Il tratto
pulito da m* raggiunge una posa fuori palla (la nascita stessa, fuori
palla-3): per T25 (dicotomia) il primo passo fuori esiste; per
l'enumerazione dell'oracolo pigro (L-U3a.1) la firma (cella, heading)
di m* è una delle 15 firme-exit, e per C1/C3/C4 (validi su P, L-U3a.1)
è una delle 8 RESIDUE. Nota di completezza: m* ≠ nascita, perché
posa(m*) ∈ palla-2 mentre l'origine è fuori palla-3 — dunque il
genitore di m* è un nodo di P e C3/C4 si applicano. m* è un nodo di P,
che è U3-valido ⇒ R_f^{U3} per quella f. ∎
(Caso nascita sporca: pend₂ ≥ 1 = v2^{U3} soddisfatta su P; caso
"nascita in palla": non esiste sotto U3.)

### 3.3 OSSERVAZIONE L-U3a.3 — la bicondizionale X6 NON relativizza in silenzio (fatto emerso in stesura, da pannellare)

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
Conseguenza editoriale: 0b.U3-a va inteso come "restrizione della
direzione utile", NON come bicondizionale relativizzata; il pannello
decide la dicitura definitiva.

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

**Invariante (per ogni cella fissata c, da S_t del verdetto):**
S_t(c) = UNSEEN se c ∉ last_t; KNOWN se c ∈ known_t; FORGOTTEN se
c ∈ last_t \ known_t. Con known_t ⊆ last_t i tre casi sono disgiunti ed
esaustivi.

**Teorema (equivalenza monitor ↔ known/last).** La tavola totale del
monitor (PREREG_RC2_PONTE v5/v6, ordine a 4 passi) calcola esattamente
S_t(c) per ogni c e ogni t; corollario:
**lettura di c è deep₁ ⟺ S_{t⁻}(c) = FORGOTTEN** (e fresh ⟺ UNSEEN,
in-window ⟺ KNOWN).

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
  (1) = S_{t⁻}(c) — righe 1/3/6 della tavola (fresh/in-window/deep dai
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
  = [S_{t⁻}(c) = FORGOTTEN]; fresh = c ∉ last = UNSEEN; in-window =
  c ∈ known = KNOWN. ∎

**Ipotesi usate (dichiarate):** mossa unitaria per passo (dinamica
canonica CLAUDE.md §2); l'ordine (1)(2)(3)(4) del macchinario C6. Il
replay (Gate 0b.3 / certificazione Via B) verifica l'IMPLEMENTAZIONE
del monitor contro questo lemma, non il lemma.

## 5. Cosa resta aperto (nessuna promozione)

- La certificazione della VIA B come implementazione (checker con
  controlli espliciti, esca, optimize==0, replay) — il lemma L-MON è la
  sua base deduttiva, non il suo sostituto.
- La mappa (iii) di 0b.0 (corrispondenza posa/heading backward–forward)
  e i suoi gate di terra.
- La dicitura definitiva di 0b.U3-a alla luce di L-U3a.3 (pannello).
- Le 8 milestone quantitative per-firma (gate della Fase 1, invariato).
- §109: chiuso — nulla qui è una deduzione ¬R_f.
