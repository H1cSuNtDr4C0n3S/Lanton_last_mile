# Cone Lock Addendum (§87) — Cono Bianco, Spoiler Vecchio e forense degli onset

Riepilogo in una frase: il calcolo dei lock (§86b) esteso alle corse reali produce tre lemmi esatti
(Replay-Lock, Cono, Finestra-K) e un teorema condizionato al censimento — lo SPOILER VECCHIO: in
ogni orbita eterna non-highway deve esserci, in OGNI istante, un nero di eta' >= K entro un raggio
mediano ~15 dalla formica (certificato per ogni K <= 14) — mentre la forense delle 24 orbite mostra
che il caos reale entra in autostrada attraverso il germe MINIMO (13-17 neri, mediana 13 = il minimo
teorico §76) e il kill-gate §79.1 chiude come atteso; Link 1 non cade oggi, ma per la prima volta ha
un enunciato dinamico esatto, con checklist per-parola di poche celle ai pose-record.

## 87.1 Lemma del Replay-Lock (esatto)

**Enunciato.** Sia data una corsa finita di T passi da posa (x,y,h) su ambiente E. Sia V_T
l'insieme delle celle lette durante la corsa, ciascuna col colore che aveva in E al tempo 0.
Allora:
- (sufficienza) ogni ambiente E' che coincide con E su V_T produce, dalla stessa posa, la stessa
  parola di svolte e la stessa traiettoria per T passi;
- (necessita' per-cella) cambiare il colore iniziale di una qualunque cella di V_T lascia la
  parola invariata fino alla prima lettura di quella cella e la cambia esattamente li'.

**Dimostrazione.** Induzione sui passi: la lettura al passo t o e' una prima lettura (colore =
iniziale, uguale per ipotesi su V_T) o e' una rilettura (colore = ultima scrittura della formica,
uguale per induzione, perche' traiettoria e svolte coincidono fino a t). Per la necessita': fino
alla prima lettura della cella modificata nulla e' cambiato; alla prima lettura il colore letto e'
l'altro, quindi la svolta e' l'altra. QED.

V_T coi suoi colori e' quindi il **lock esatto** della corsa: condizione sufficiente e
word-minimale (nessun sottoinsieme proprio determina la parola). Verifica meccanica
(`alpha1/onset_cone_lock.py`, self-test §5): 1000 ambienti junk fuori V => parola identica;
200 flip dentro V => la parola cambia esattamente alla prima lettura. Tutto verde.

## 87.2 Lemma del Cono (i lock d'ingresso di §76 diventano condizionali universali)

Applicando il Replay-Lock alle corse d'ingresso certificate a §76 (gate esatti riprodotti qui:
vuota 9977, b1 310, b2 162, b3 142, (7,-7) 106258 — 5/5):

| germe | lock (onset+20 periodi) | blob (pre-onset) | raggio | affitto |
|---|---|---|---|---|
| vuota | 1816 celle, 0N/1816B | 1376 | 29 | 22/periodo, p0=0 |
| b1 (0,-2) | 544 celle, 1N/543B | 104 | 9 | 22/periodo, p0=0 |
| b2 | 497 celle, 2N/495B | 57 | 5 | 22/periodo, p0=0 |
| b3 | 490 celle, 3N/487B | 50 | 5 | 22/periodo, p0=0 |
| (7,-7) | 8704 celle, 1N/8703B | 8264 | 72 | 22/periodo, p0=0 |

**Affitto periodico esatto:** in TUTTI i casi le celle nuove per periodo post-onset sono
esattamente 22 e l'insieme co-moving si stabilizza dal periodo 0 (traslazione esatta di drift
(+-2,+-2)). Il lock eterno e' quindi **finitamente descritto**: blob + striscia periodica di 22
celle/periodo. (Bug corretto durante la sessione: il drift va calcolato dall'heading REALE
all'onset, h(t) = h0 + #R - #L mod 4, non da h=0.)

**Lemma del Cono.** In QUALSIASI orbita, a QUALSIASI istante: se tutte le celle del cono
C(posa(t)) (lock ruotato/traslato sulla posa corrente) hanno i colori richiesti — per la vuota:
tutte bianche — l'orbita replica la corsa d'ingresso ed entra in autostrada. Poiche' i neri di
un'orbita sono in numero finito a ogni istante, la parte semi-infinita della striscia oltre il
supporto nero corrente e' bianca gratis: la condizione e' finita.

**Corollario (prima forma di Link 1 con denti).** Un'orbita eterna non-highway deve avere, in
ogni istante t, almeno una cella nera dentro il Cono Bianco C_0(posa(t)) — blob raggio 29 +
striscia — e, per ciascun germe della libreria, o un nero nella parte bianca-richiesta o il
pattern del germe sbagliato. Le 3 celle di scia {(0,1),(-1,1),(-1,0)} stanno nel blob in tutti i
casi: **la formica porta con se' il proprio spoiler** (aggancio diretto al Teorema della Scia
§86 — e' il motivo strutturale per cui il caos non fa onset spontaneo).

## 87.3 Lemma della Finestra-K e Teorema dello Spoiler Vecchio

**Lemma della Finestra-K** (duale del Replay-Lock, determinazione all'indietro). Per ogni istante
t >= K di ogni orbita, con w = svolte(t-K..t-1): (a) w e' realizzabile (riletture coerenti, senso
word_lock §86b); (b) il footprint F(w) delle celle toccate negli ultimi K passi e i loro colori
AL TEMPO t sono funzione di w sola. Dimostrazione: ogni lettura della finestra o e' prima-lettura
nella finestra (colore rivelato dalla svolta) o rilettura (nota per induzione); ogni scrittura e'
il flip della lettura. QED. **Verificato su dati reali** (self-test A: 3 orbite junk, 150 sonde a
t casuali, colori predetti vs campo reale ricostruito per replay: 0 mismatch).

**Costruzione.** Per ogni w realizzabile: germe(w) = colori di F(w) (frame anchor, posa finale in
origine heading-su) + bianco altrove. Se germe(w) fa onset, per il Lemma del Cono vale il
condizionale esatto: a ogni t con svolte recenti w, se V(w) \ F(w) e' tutto bianco al tempo t,
l'orbita entra.

**Censimento (`alpha1/kwindow_spoiler_census.py`), cap 2M, tutto verde:**

| K | realizzabili / 2^K | onset | NO-onset | onset min/med/max | raggio spoiler min/med/max |
|---|---|---|---|---|---|
| 6 | 50 / 64 | 50 | **0** | 196/2775/21409 | 7/23/45 |
| 8 | 154 / 256 | 154 | **0** | 194/2461/30937 | 7/17/45 |
| 10 | 448 / 1024 | 448 | **0** | 192/1593/30937 | 7/15/46 |
| 12 | 1300 / 4096 | 1300 | **0** | 190/1540/50550 | 7/15/61 |
| 14 | 3680 / 16384 | 3680 | **0** | 172/1526/50550 | 7/15/68 |

**TEOREMA DELLO SPOILER VECCHIO (scala K <= 14, condizionato solo al censimento sopra).**
Un'orbita eterna non-highway deve avere, in OGNI istante t >= K, almeno una cella nera in
V(w(t)) \ F(w(t)): un nero NON toccato negli ultimi K passi (eta'-di-tocco >= K), a distanza
Chebyshev <= 68 (mediana 15) dalla formica. Vale per ogni K in {6,8,10,12,14} simultaneamente.

**Lemma collaterale (streak cappate).** LLLLL e RRRRR sono irrealizzabili: quattro svolte uguali
chiudono un quadrato e riportano sulla cella di partenza, gia' riscritta del colore opposto; la
quinta svolta uguale richiederebbe di rileggere il colore originario. Contraddizione. Quindi in
OGNI orbita le streak di L e di R sono <= 4. (Elementare, ma qui certificato dal filtro di
realizzabilita': all-L e all-R scartate a ogni K >= 5.)

## 87.4 Forense degli onset reali (24 orbite, gate 24/24)

`alpha1/onset_forensics.py` ricalcola gli onset delle 24 orbite lunghe (semi da rngstate, motore
Python con onset_verified esatto): **24/24 identici agli header di dumps_all.txt** (313358 ...
251853). Tripwire di replay e sotto-corse: 0 divergenze. All'anchor t_on:

- **Il germe reale e' il germe minimo.** Neri ambientali consumati dalla highway neonata nei 20
  periodi post-onset: min 13, mediana 13, max 17, raggio <= 7 (mediana 6). Tredici e' ESATTAMENTE
  il supporto del germe minimo §76: il caos entra dalla porta piu' stretta possibile.
- **Interfaccia a rasoio.** Profondita' d'interfaccia 1 periodo (2 nelle orbite 2, 9, 22 con
  massa 16-17); dal periodo 2 in poi la frazione di territorio mai visitato e' 0.995-1.0: la
  highway nasce e vola immediatamente nel fresco.
- **Nasce al bordo e punta fuori.** f_bordo = Cheb(posa)/R_visitato: mediana ~0.68 (min 0.29,
  max 0.92); drift del primo periodo verso l'esterno in 23/24 (eccezione: orbita 12).
- Ultime 8 svolte pre-onset registrate per orbita (materiale per §88).

## 87.5 Kill-gate §79.1: SCARICATO (negativo, come atteso)

Il gate in coda da §79 chiedeva: il verdetto "questo evento deep-black portera' a lock W0" e'
funzione di un footprint finito co-moving con P bounded? Il Replay-Lock da' la risposta esatta:
il verdetto "onset entro l'orizzonte" da un anchor qualunque e' funzione ESATTA (sufficiente e
word-minimale) dell'insieme delle prime-letture dall'anchor all'orizzonte. Misura su 24 orbite,
anchor a t_on - Delta:

| Delta (periodi) | raggio decisivo min/med/max |
|---|---|
| 2 | 9 / 18 / 46 |
| 10 | 20 / 38 / 77 |
| 100 | 66 / 93.5 / 149 |
| 1000 | 82 / 118 / 150 |

Il raggio decisivo cresce con l'anticipo senza stabilizzare: **nessun programma a footprint
limitato decide deep->W0**. Onesta': il footprint prime-letture e' word-minimale, non
necessariamente verdetto-minimale; ma i determinanti piccoli sono gia' esclusi (§59, §78-§80).
Il path deep->W0 come direttrice chiude definitivamente; l'oggetto vivo resta la coda lunga
(§79.6.2) e ora, soprattutto, la via dei record (§87.6).

## 87.6 Profilo direzionale: la via dei pose-record (verso §88)

Fatto B-T: un'orbita eterna e' illimitata, quindi (WLOG per C4-simmetria) stabilisce infiniti
record y-min. A un record stretto: la formica arriva heading-su su una cella MAI visitata;
l'intero semipiano {y_rel < 0} E la riga {y_rel = 0} sono mai-visitati => bianchi gratis; il
footprint F(w) giace per forza in {y_rel >= 1}.

`alpha1/spoiler_quadrant_profile.py` (gate: onset identici al censimento, 1300+3680 OK) misura
per ogni parola il **burden1** = |spoiler ∩ {y_rel >= 1}| (le sole celle che a un record possono
ospitare uno spoiler) e la **record-compatibilita'** (footprint ⊆ {y_rel >= 1}):

| K | record-compatibili | burden1 min (rec) | parola campione |
|---|---|---|---|
| 12 | 418 / 1300 | 18 | LRLLLLRLRLLR (onset 196) |
| 14 | 1176 / 3680 | 16 | RLRRLRLLLLRLRL (onset 172) |
| 16 | 3026 / 10412 | 14 | LLRLRRLRLLLLRLRL (onset 172) |
| 18 | 8418 / 29128 | 10 | LRLLRLRRLRLLLLRLRL (onset 172) |

**Teorema della checklist ai record (condizionato al censimento).** A ogni pose-record y-min di
un'orbita eterna, dette w le ultime K svolte (necessariamente record-compatibili), deve esserci
un nero di eta' >= K in una checklist di sole burden1(w) celle specifiche (minimo 10 a K=18).
Nessuna parola-arma (burden1 = 0) esiste a K <= 18 nel censimento completo. Ma il minimo scende
con K (18 -> 16 -> 14 -> 10) e l'enumerazione e' esponenziale-mite (~x2.8 ogni +2): da qui la
caccia mirata di §87e.

Nota onesta (perche' i campioni a 2 celle NON contano): a K=14 esistono parole con burden1 = 2
(es. LRLLRLRLRLLRLL, celle (-2,1),(1,1)), ma il loro footprint tocca y_rel <= 0: non possono
presentarsi a un record. Il filtro di compatibilita' e' essenziale; senza, l'arma e' un miraggio.

## 87.6-bis (§87e) La caccia all'arma e il RESIDUO DEI CINQUE

Osservazione chiave: per l'arma non serve il censimento completo a scala K — basta UNA parola
record-compatibile con burden1 = 0 a QUALSIASI K, verificata con una sola simulazione (il
condizionale al record e' incondizionato dato l'onset del suo germe). `alpha1/record_weapon_hunt.py`
fa beam search (beam 300) per PREPEND di passi piu' vecchi: il suffisso relativo all'anchor non
cambia, il footprint cresce all'indietro e puo' coprire celle di spoiler (che diventano parte del
germe, coi colori forzati dalla parola); onset e burden ri-simulati a ogni nodo, pota sound
(irrealizzabile o footprint fuori {y>=1}, vincolo vero di ogni passato di record).

Risultato (K=10 -> 40 in 16 s): burden1 minimo 19 -> 18 -> 16 -> 14 -> 11 -> 10 -> 9 -> 8 -> 7
-> 6 -> 5, poi **PLATEAU a 5 da K=32 a K=40** con residuo STABILE:

```text
RESIDUO DEI CINQUE: {(-4,1), (-3,1), (-2,1), (1,1), (2,1)}
(riga a profondita' 1, tre celle a sinistra e due a destra della colonna d'ingresso;
 campione K=32: LRLLRLRRLRRLRRLRLLRLRRLRLLLLRLRL, onset 168, ri-verificato indipendente)
```

Lettura iniziale (container, beam 300): plateau su 9 valori di K consecutivi, sospetta
ostruzione strutturale — con l'avvertenza esplicita che un beam e' greedy e il 5 NON era un
pavimento dimostrato.

**AGGIORNAMENTO (Ryzen, beam 5000, kmax 60, 76 s, parallelo):** l'avvertenza era fondata. Il
plateau a 5 era un artefatto del beam. La discesa riprende: 5 (K=32) -> 4 (K=35, esce (-4,1) e
(-3,1)) -> 3 (K=40) -> **2 (K=58 e K=60)**, ancora in discesa quando kmax ha fermato la corsa.
Residui a 2 celle: {(-2,1),(0,2)} a K=58 e {(-2,1),(1,1)} a K=60 (campione K=60:
LRLLRLRRLLLLRRLLLLRRLRRLRRLRRRRLLLLRLLRLRRLRLRLLRLLRLLRLRLRL, onset 156). La cella **(-2,1)**
e' la costante di ogni campione dal K=26 in poi: l'ultima sentinella. Gli onset dei germi
SCENDONO con K (172 -> 168 -> 156): piu' passato dichiarato, ingresso piu' rapido. Il RESIDUO
DEI CINQUE va quindi riletto come tappa, non ostruzione.

**AGGIORNAMENTO 2 (run Ryzen beam 8000 kmax 160 + analisi di vacuita' — la scoperta vera).**
Il run largo NON riproduce il 2 stabilmente: i rami a fardello 2 vivono a K=60-70 (tre famiglie,
residui {(-2,1),(1,1)} e {(-2,1),(0,2)}), poi a K=71 TUTTE le loro estensioni muoiono e il beam
collassa in un CICLO LIMITE periodico a fardello 4 (blocchi `LLRLLLLR` pompati; candidati che
ciclano con periodo 8). Diagnosi al microscopio (DFS esaustiva sui prepend):

- i campioni a fardello 2 (K=58/60/66/70) hanno 0-1 prepend validi e si ESTINGUONO all'indietro
  entro profondita' 3: NESSUN passato record-compatibile lungo li puo' produrre. Il loro
  enunciato ai record e' **VACUO** per orbite eterne.
- perfino il campione P(0) del ciclo (K=124, fardello 4) ha UNA sola estensione per 6 livelli e
  si estingue a profondita' 7; il ciclo del beam era una STAFFETTA di 8 lignaggi fratelli
  sfasati, ognuno mortale. La famiglia interna P(n) = inserzione di `LLRLLLLR`^n (fardello 4 e
  residuo {(-2,1),(0,2),(1,1),(2,1)} INVARIANTI fino a K=444) e' reale ma i suoi membri non
  sono suffissi l'uno dell'altro: non certifica un passato illimitato.

**Lezione strutturale (il probabile teorema sotto):** coprire le celle di spoiler col footprint
COSTRINGE il passato — i germi a fardello basso si vietano da soli la storia. Esiste un
trade-off fardello <-> profondita'-del-passato D(w) (= max catena di prepend validi; l'albero e'
finitamente ramificato, quindi D(w)=infinito <=> illimitato, Konig). Ogni suffisso di record di
un'orbita eterna ha D = infinito (il suo passato reale E' l'estensione). Criterio dell'arma
CORRETTO: burden1(w) = 0 **e** D(w) illimitato. Il cacciatore v3 introduce il filtro di
vitalita' `--viable-k` (ammessi solo candidati con catena di prepend >= k) e il beam
stratificato per firma di residuo `--per-class` (anti-staffetta). Congettura da decidere a §88:
per ogni w record-compatibile con D(w) illimitato vale burden1(w) >= 1? (Se si', questa via
verso Link 1 chiude onestamente; se no, l'arma esiste.)

## 87.7 Link 1 riformulato (stato esatto del crux)

Prima di §87 Link 1 era: "orbita eterna non-highway => lock W0-like profondi infinite volte",
senza che "lock W0-like" fosse un oggetto. Ora:

1. l'oggetto e' esatto: i lock d'ingresso (blob + affitto periodico 22) e, per ogni parola
   recente, il cono del germe di finestra-K;
2. l'enunciato dinamico e' esatto e dimostrato-condizionato: **eterna => spoiler vecchio (eta'
   >= K) entro raggio ~15-68 in OGNI istante, per ogni K <= 14; ai record, dentro una checklist
   di >= 16 celle**;
3. il meccanismo reale d'ingresso e' misurato: germe minimo (13) al bordo, interfaccia 1 periodo;
4. cio' che manca per far cadere Link 1 e' UNO di: (a) una parola record-compatibile con
   burden1 = 0 (la caccia §87e si e' fermata a un plateau di 5 celle — il Residuo dei Cinque —
   non dimostrato pavimento); (b) un argomento che chiuda il pigeonhole sulle 5 celle usando la
   dinamica fra record consecutivi; (c) un argomento che la scorta di detrito vecchio richiesta
   dallo Spoiler Vecchio e' incompatibile con l'illimitatezza B-T (il detrito e' statico: la
   formica non lo trasporta, puo' solo dipingere celle giovani — un'orbita eterna deve aver
   PRE-SEMINATO ogni luogo che visitera'; il camping rifornisce con lag K, e qui vive la
   tensione, non ancora la contraddizione).

Link 1 NON cade in questa sessione. Ma per la prima volta ha un enunciato con i denti, due
attacchi nominati e un piano di misura che li decide.

## 87.8 Trappole nuove

- **(v) lo spoiler puo' essere la propria scia invecchiata.** Non dedurre dallo Spoiler Vecchio
  che il caos "muoia di solitudine": una cella dipinta K+1 passi fa e' gia' "vecchia" a scala K,
  e il caos si sposta ~0 in 14 passi (rotore §77). Nessun K finito chiude per camping. La leva
  non e' l'esistenza dello spoiler ma la sua GEOMETRIA ai record (burden1) e il costo di
  pre-seminare il futuro contro B-T. Non riaprire argomenti "il caos resta senza neri vicini".
- **(w) fardello basso ≠ parola viva: il germe puo' vietarsi il passato.** Un enunciato
  "ai record con suffisso w serve uno spoiler in N celle" e' VACUO per orbite eterne se w non
  ammette estensioni all'indietro record-compatibili di profondita' arbitraria (D(w) finito).
  I minimi di fardello trovati per beam senza filtro di vitalita' (2 a K=58-70; P(0) a
  fardello 4) sono tutti vacui: estinzione all'indietro entro profondita' 3-7. Prima di
  enunciare qualsiasi teorema-parola ai record, certificare la vitalita' (catena di prepend
  lunga, idealmente un ciclo di prepend). Il minimo che conta e' sul sottoinsieme VIVO.

## 87.9 Roadmap §88

1. **Trade-off fardello <-> passato (il nuovo crux di questa via):** decidere la congettura
   "D(w) illimitato => burden1(w) >= 1". Strumenti: cacciatore v3 (`--viable-k`, `--per-class`)
   sul Ryzen per il minimo VIVO empirico; automa dei prepend (stato = bordo iniziale della
   camminata virtuale) per cercare cicli di prepend certificati a fardello basso, o per un
   argomento di impossibilita'. Se il minimo vivo resta >= 1 e si capisce PERCHE', il pigeonhole
   si sposta sulle celle del residuo vivo minimo (oggi: il Quattro {(-2,1),(0,2),(1,1),(2,1)},
   vitalita' della famiglia ancora da certificare) e sulla dinamica fra record consecutivi
   (la riga y_rel=1 del record corrente era la riga-record del passaggio precedente).
2. **Dinamica dei record:** quali parole record-compatibili OCCORRONO davvero ai record delle 24
   orbite (e con che frequenza)? Se le parole a basso burden1 sono inevitabili ai record, il
   pigeonhole diventa l'attacco.
3. **Record doppi / angoli:** ai vertici del rettangolo di bounding due semipiani sono bianchi
   gratis; 5 parole a K=14 hanno il quadrante dietro-dx spoiler-free — analisi dedicata.
4. In coda: certificazione Ryzen §85-§87 (bit-identica); lock delle 46 parole L_hw (§83 — NB:
   motivi r=3, non parole di svolta: chiarire prima l'oggetto giusto).

## 87.10 Inventario file

- `alpha1/onset_cone_lock.py` + `onset_cone_lock_summary.json` (§87a: Replay-Lock, coni, affitto)
- `alpha1/kwindow_spoiler_census.py` + `kwindow_spoiler_summary.json` + `kwindow_spoiler_run.log`
  (§87b: censimento germi finestra-K)
- `alpha1/onset_forensics.py` + `onset_forensics_summary.json` + `onset_forensics_run.log`
  (§87c: forense 24 orbite + kill-gate §79.1)
- `alpha1/spoiler_quadrant_profile.py` + `spoiler_quadrant_summary.json` +
  `spoiler_quadrant_run.log` (§87d: burden1 ai record, K=12-18)
- `alpha1/record_weapon_hunt.py` + `record_weapon_summary.json` + `record_weapon_run.log`
  (§87e: caccia all'arma, Residuo dei Cinque)

## 87.11 Frase di stato dell'arte

*Il caos non entra mai per caso: entra dalla porta piu' stretta che esista, tredici neri al bordo
del mondo. E per non entrare mai, dovrebbe ricordarsi di sporcare in anticipo ogni angolo del suo
futuro: lo Spoiler Vecchio esige un testimone anziano accanto alla formica in ogni istante
dell'eternita'. Non l'abbiamo ancora colto in fallo. Ma la caccia ha stretto il cerchio fino a
cinque celle sulla prima riga dietro ogni record — il Residuo dei Cinque — e adesso sappiamo
esattamente dove guardare, e a quali appuntamenti deve presentarsi.*
