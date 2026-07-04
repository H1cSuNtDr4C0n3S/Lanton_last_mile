# ADDENDUM §94 — U2-LONTANO 2: censimento born-near sulla famiglia, pannello §93 completato (2/3), PAVIMENTO DEL LEDGER FALSIFICATO, parity-flux

**Riepilogo in una frase:** il censimento Nascita Vicina e' stato esteso dall'intera
famiglia rigenerata (273.493 coprenti-nere distinte, 6,2x la campagna §92, 50 config
di copertura vs le 43 citate a §92c: **273.459 CERTIFICATE born-near, 34 fuggenti,
ZERO alberi esauriti con min-pend=0**, r_seed ≤ 63), il pannello §93 e' stato
completato su 2 lenti su 3 (caccia, macchina-palla2; nascita-vicina uccisa DI NUOVO
dal limite di sessione, debito x2) con tutti i numeri §93 riprodotti bit-identici da
macchinari indipendenti MA con un **BUCO convergente da entrambe le lenti: la
CONGETTURA DEL PAVIMENTO DEL LEDGER (pend₂ ≥ 2, e anche la variante ≥ 1
incondizionata) e' FALSIFICATA** — estensioni valide delle fuggenti raggiungono
pend₂ = 0 (posa di nascita (−1,2), DENTRO la palla) e pend₂ = 1 = {(0,2)} con posa
(0,3) FUORI palla; 10 controesempi verificati di terra e salvati
(`alpha1/u2_far_pend2_counterexamples.json`); il fatto sopravvissuto e' la forma
CONDIZIONATA ALLA POSA — **mai visto pend₂ = 0 con posa fuori palla** (~120M passi
caccia-lente + ~37M nodi macchina-lente + 1,29G della campagna §93) — che basta
comunque al Muro (l'ipotesi del record esclude seme E origine dalla palla); in
parallelo e' stata costruita la pipeline **parity-flux** (caccia a invarianti GF(2)
su feature di stato del camminatore + chiusura induttiva alla Houdini) che ha
prodotto la storia metodologica piu' istruttiva della sessione: l'invariante
campionato phi_colonna0 = p(0,1)+p(0,2)+[posa=(0,2)] ≡ 1 — 762k stati concordi,
costante uniforme su 42/42 fuggenti note — e' stato RIFIUTATO dal checker di
chiusura (non induttivo) e POI falsificato dai controesempi del pannello: **il
checker funziona, il campione mente** (trappola nuova gg).

Strumenti nuovi: `alpha1/u2_far_born_near_census.py`, `u2_far_parity_flux.py`,
`u2_far_flux_closure.py`, `u2_far_flux_perpose.py`,
`u2_far_pend2_counterexamples.json` (+ summary JSON e log).

## 94a. Censimento born-near sulla famiglia intera (§93h.3)

Lo script della campagna §92 non era stato salvato (solo i witnesses): la campagna
e' stata RIGENERATA (`u2_far_born_near_census.py`, 8 worker BelowNormal, politiche
randomizzate + steering, cap 40k nere/worker, 12,4M passeggiate, 253 s totali):

- **273.493 coprenti-nere distinte** (§92: 43.726) in **50 config di copertura**
  distinte (config = `(h1, req|S_CORE)` alla copertura, la nozione della macchina
  §92; §92c ne aveva citate 43; §90c ne vedeva 2 — GATE GC0 riprodotto ESATTO).
- **273.459 CERTIFICATE born-near** (albero esaurito + min-pend>0 su tutti i nodi),
  r_seed ≤ **63**; **34 fuggenti** (tutte a cap big 3M nodi/450 prof.);
  **ZERO alberi esauriti con min-pend = 0**: la gamba-2 del Lemma §93c non ha
  ancora trovato un solo caso scoperto.
- **Le fuggenti sono concentrate**: 31/34 in UNA config (h1=3, 52 parole, che
  contiene anche 21 certificate) + 3 config singleton ⇒ la fuga e' una proprieta'
  PER-PAROLA, non per-config.
- **Scala D arricchita** (trappola bb, di nuovo): oltre alle classi §92
  0/4/8/12/48/56 compaiono **28, 32, 52, 60, 64** (code della famiglia mai viste
  dalle campagne precedenti).
- Identita' delle fuggenti: le 34 = le **6 nere400 di §92 + 28 NUOVE** (mai viste);
  i 2 jackpot sono correttamente CERTIFICATI (alberi finiti D 48/56, come §92).
- Gate: GC0 (60 coprenti §90c → esattamente 2 config), GC1 (42 testimoni finiti
  bit-identici al summary §93 — pairing per INDICE: i nomi `cc90c_prof*` NON sono
  unici, 48 righe / 35 nomi distinti), GC2 (8 alberi cross-validati col solo
  `valid()` di terra, (D, min_pend) bit-identici), GC3 (soglie minime asseribili:
  ≥30 config, ≥10k nere, ≥1 config nuova), GC4 (100 hit ricontrollate). Tutti
  verdi, e GC1 e' FALLITO davvero alla prima stesura (pairing per nome) — il gate
  puo' fallire.

## 94b. Pannello §93 (debito §93h.1): 2 lenti su 3, numeri tutti REGGONO, un BUCO

Lente **nascita-vicina**: MORTA per limite di sessione (seconda volta — DEBITO §95).
Mitigazione parziale: GC1/GC2 del censimento rifanno D_true/min_pend bit-identici
sui 42 testimoni + cross-validazione `valid()`; la logica delle due gambe resta
non ri-attaccata da lente dedicata.

Lente **caccia** (macchinario riscritto da zero, 4 esche beccate — una riformulata
onestamente dopo essersi scoperta vacua):
- C1 REGGE: contabilita' per-raggio §93d riprodotta ESATTA dai summary (R=2
  2/37.151 ... R=16 43/432M; precisazione: a R=12/16 il min sui soli bersagli-fuga).
- C2 REGGE: goal (pend_in==0 E nascita cheb>R) e monotonia corretti.
- C4 IMPRECISIONE: il controllo negativo D4/D12 dello script e' vacuo cosi' come
  scritto (`tree_exhausted` irraggiungibile: l'esaurimento e' dei sottoalberi
  committati, 144/144); il fatto matematico e' stato chiuso dalla lente per
  enumerazione indipendente (alberi 4/12/57/49 nodi bit-identici a
  `u2_far_pend2_floor`).
- C5 REGGE: corsa forzata 48/48 righe bit-identiche col motore della lente.
- **C3 BUCO** (vedi 94c).

Lente **macchina-palla2** (reimplementazione indipendente completa, 4 esche beccate):
- M1 REGGE (soundness OUT/cella-giovane), M2 REGGE (B0–B3 + B2 rifatto con
  prime-letture forward su 8/8: pend₂=5 alla copertura per tutti), M4 REGGE
  (decomposizione del corno 3 esaustiva).
- M3-conteggi REGGE bit-identico (3.436.966 stati; novita' di dettaglio: i 1.376
  puliti-lontani = 96 OUT + 1.280 in-striscia-far).
- **M3-vicini IMPRECISIONE**: il "3.396 pend₂=0 vicini" di §93f e' il TOTALE
  pend₂=0 (include i 1.376 lontani): i vicini veri sono **2.020**. Correzione a
  §93f e al campo `stati_pend0_vicini` del summary.
- **M3-fantasmi BUCO** (vedi 94c).

## 94c. LA FALSIFICAZIONE: il pavimento del ledger e' FALSO

Due lenti, macchinari diversi, euristiche diverse, stessi verdetti (e la lente
macchina ha trovato i suoi testimoni in **~7 secondi / 660k nodi** con una DFS
greedy mirata — dove la campagna §93 con 1,29G nodi non aveva visto nulla):

- **pend₂ = 0 e' RAGGIUNGIBILE** da estensioni valide delle fuggenti
  (nere400[0,1,2,5]): posa di nascita **(−1,2)** (cheb 2, DENTRO la palla),
  estensioni 609–1037 prepend. Quadrupla certificazione della lente caccia
  (ricalcolo prime-letture, `valid()`, replay forward puro, rigioco nel Walker
  dello script §93) + **verifica di terra di questa sessione**
  (`valid()` + `exact_state`): 10/10 controesempi confermati,
  salvati in `alpha1/u2_far_pend2_counterexamples.json`.
- **pend₂ = 1 = {(0,2)} con posa (0,3) FUORI palla** (cheb 3): il pavimento ≥ 2
  cade anche nella forma condizionata; resta solo ≥ 1.
- Cadono: la congettura §93d (pend₂ ≥ 2), il "reale mai sotto 2" di §93f, il
  "residuo al minimo sempre {(−1,1),(0,1)}" di §93e (il minimo vero lascia
  {(0,2)} o NULLA: il debito puo' uscire interamente dalla palla-2 — pend₃ dei
  nodi puliti = 4–6 celle tipo (0,3),(1,3),(3,1),(3,2)).
- Il floor "2" della campagna §93 era **survivorship della politica di caccia**
  (trappola bb auto-applicata ma insufficiente: una sola famiglia di politiche).

**Cosa SOPRAVVIVE (forma riparata, convergente dalle due lenti):**
1. **Mai visto pend₂ = 0 con posa fuori palla** (~120M passi + ~37M nodi + 1,29G
   della campagna §93; i 1.376 clean-far astratti restano NON realizzati e restano
   i falsificatori candidati). Enunciato-bersaglio riparato (LEDGER SPORCO v2):
   **posa (nascita) fuori palla-2 ⇒ pend₂ ≥ 1** ⇒ ≥ 1 cella di seme in palla-2 —
   che BASTA per il Muro: l'ipotesi del record esclude seme E origine dalla palla
   (nascita in-palla e' gia' esclusa dalla gamba-origine).
2. **I nodi puliti sono quasi-morti all'indietro**: sottoalberi dei prepend sopra
   i pend₂ ≤ 1 esauriti in 17–71 nodi (lente macchina). Pulire la palla costa la
   vita all'indietro (parente di (w)/(aa)) ⇒ programma §95: **chiusura per
   vitalita'** — se ogni nodo pend₂=0-in-palla ha albero finito piccolo, la
   Nascita Vicina si applica LI' e il Muro si chiude senza alcun pavimento.
3. BFS solo-in-striscia dai 47.312 cover astratti (171.018 stati): pend₂=0 solo
   con pose in palla, MAI clean-far ⇒ ogni cammino astratto verso i 1.376 passa
   da OUT (localizzazione coerente con §93f).

## 94d. Parity-flux: lo strumento, e la lezione (il checker batte il campione)

Pipeline nuova (via (b) di §93h.2): camminate all'indietro ESATTE sulle 8 fuggenti
(nessuna striscia, nessuna astrazione OUT), feature GF(2) di stato (pending/visited
per le 33 celle di W = x∈[−6,4], y∈{1,3}, posa one-hot, heading, parita', bias),
base incrementale delle differenze ⇒ nullspace = funzionali costanti lungo ogni
cammino (`u2_far_parity_flux.py`); poi **promozione deduttiva** con chiusura alla
Houdini sull'enumerazione ESAUSTIVA dei 526 tipi-di-passo localmente validi
(`u2_far_flux_closure.py`: qui l'OUT non puo' mordere — req|W vive nelle feature e
le visite sono pose; gate FC0 controllo positivo par(x+y)+par(h), FC1 esca a delta
corrotto).

Storia istruttiva:
- Su 762.476 stati campionati emergono 39 invarianti (37 uniformi tra le 8 parole),
  3 con supporto in palla; il piu' bello: **phi_colonna0 = p(0,1) + p(0,2) +
  [posa=(0,2)] ≡ 1** (firma whack-a-mole di colonna 0), costante iniziale = 1 su
  **42/42 fuggenti note** (8 §92 + 34 censimento) e = 0 solo su parole ad albero
  finito. Corollario SE VERO: alla nascita fuori palla pend₂ ≥ 1 = Ledger Sporco v2.
- La chiusura globale lo RIFIUTA (killer: passi da posa (0,2) verso (0,3) pendente
  — servono fatti condizionali alla posa); la chiusura per-posa
  (`u2_far_flux_perpose.py`, dominio affine per classe di posa) NON lo certifica
  (0/33 classi al punto fisso).
- I controesempi del pannello lo FALSIFICANO: ai nodi pend₂=0 con posa (−1,2),
  phi_colonna0 = 0. **Il rifiuto del checker era corretto; PF1 ("min pend₂
  osservato = 2") era survivorship della politica di camminata.**
- Nota onesta: il gate PP0 del per-pose (controllo positivo) e' ROSSO al punto
  fisso — la chiusura per-posa attuale e' troppo aggressiva (classi povere di
  campioni uccidono a cascata); da raffinare PRIMA di riusarla come certificato.
  Il verdetto negativo su phi_colonna0 resta valido (coerente coi controesempi).

## 94e. Trappole nuove

- **(gg) l'invariante campionato non e' un fatto — la chiusura induttiva e' il
  gate** (PARITY-FLUX §94): un funzionale costante su 762k stati campionati, con
  costante uniforme su 42/42 parole, puo' essere FALSO (phi_colonna0, falsificato
  dai controesempi del pannello negli angoli che la politica di camminata non
  raggiunge). Se Houdini/chiusura non lo promuove, trattarlo come artefatto:
  il killer-step della chiusura indica ESATTAMENTE l'angolo da campionare.
  Parente di (i) (controfattuale) e (bb) (survivorship delle estensioni).
- **(hh) il floor di una caccia e' survivorship anche a 10^9 nodi se la famiglia
  di politiche e' una sola** (PANNELLO §94): la campagna §93 (1,29G nodi, greedy
  DFS-milestone) dava floor 2; una DFS greedy MIRATA diversa trova pend₂=0 in 7
  secondi / 660k nodi. Istanza quantificata di (bb): per un NEGATIVO servono
  politiche indipendenti multiple (e anche cosi' resta un negativo, non un
  teorema). Corollario: i floor citati come "misurati" vanno sempre etichettati
  con la politica che li ha prodotti.

Correzioni ai verbali precedenti: §93d congettura FALSIFICATA (94c); §93e residuo
{(−1,1),(0,1)} = artefatto di politica; §93f "3.396 vicini" → 2.020 vicini veri
(3.396 = totale pend₂=0); §93f "il reale non sa fare pulizie" FALSO (sa farle, ma
— evidenza attuale — solo con posa in palla).

## 94f. Domande aperte / programma §95

1. **Lente nascita-vicina** (debito x2): logica delle due gambe del Lemma §93c
   sotto attacco dedicato con macchinario indipendente.
2. **Chiusura per vitalita' dei puliti** (la via nuova, 94c.2): dimostrare che
   ogni nodo pend₂=0 (posa in palla) ha albero dei prepend sopra di se' FINITO
   (evidenza: 17–71 nodi) ⇒ Nascita Vicina applicata a quei rami ⇒ Muro chiuso
   al raggio 2 + intorno SENZA pavimento. Meccanizzabile con
   `wall_exhaustive` sopra i nodi puliti raggiunti dalle cacce.
3. **Ledger Sporco v2** (posa fuori ⇒ pend₂ ≥ 1): promozione deduttiva — per-pose
   raffinato (PP0 verde prima di tutto), oppure macchina C a striscia allargata
   (§93h.2-a), oppure uccisione/realizzazione dei 1.376 clean-far astratti.
4. **Censimento**: le 34 fuggenti nuove vs le 34 nere-D≥400 di §92 (stesse
   parole? stessa config?); classificare i corridoi di fuga.
5. Retro-nota §91c.3 (ereditata, non fatta questa sessione).
6. Ereditati §92: stress-2 bianche; h1=1 mai realizzata.

## 94g. Inventario file (alpha1/)

- `u2_far_born_near_census.py` (+`_summary.json`, `.log`) — censimento famiglia
  intera: campagna 8 worker + config `(h1, req|S_CORE)` + verdetto born-near
  per parola + gate GC0–GC4. Run 253 s.
- `u2_far_parity_flux.py` (+`_summary.json`, `.log`) — caccia invarianti GF(2)
  su feature di stato (nullspace delle differenze), gate PF0–PF3. Run 3 s.
- `u2_far_flux_closure.py` (+`_summary.json`, `.log`) — chiusura induttiva
  globale (526 tipi-di-passo, Houdini), gate FC0–FC2. Run < 1 s.
- `u2_far_flux_perpose.py` (+`_summary.json`, `.log`) — chiusura per-posa
  (dominio affine per classe); PP0 rosso al punto fisso: da raffinare (94d).
- `u2_far_pend2_counterexamples.json` — i 10 controesempi del pannello,
  ri-verificati di terra (parole complete L/R, posa di nascita, pend₂).

## 94h. Pannello di scettici (2 lenti su 3 complete)

- **lente caccia** (C1/C2/C5 REGGE, C4 IMPRECISIONE, C3 BUCO): riproduzioni
  bit-identiche di §93b/§93d; 4 esche beccate (l'esca (b) ha smascherato la
  propria prima formulazione come vacua — riformulata con check in-run).
- **lente macchina-palla2** (M1/M2/M3-conteggi/M4 REGGE, M3-vicini IMPRECISIONE,
  M3-fantasmi BUCO): fase 1 e BFS post-copertura riprodotte bit-identiche con
  macchina indipendente (encoding diverso); 4 esche beccate.
- **lente nascita-vicina**: uccisa dal limite di sessione (debito §95, punto 1).
