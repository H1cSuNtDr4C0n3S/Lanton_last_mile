# ADDENDUM §101 — RECORD-DIVERGENCE: la DICOTOMIA DEL RECORD, i primi LOCK ai record, la saldatura fascia = porta

**Riepilogo in una frase:** la profondita' di divergenza d(t) del rigioco del germe —
mai censita prima — trasforma ogni record y-min in un TENTATIVO DI PORTA misurabile e
produce: (1) la **DICOTOMIA DEL RECORD** (deduttiva: rigetto nel transiente / lock
W0-like di lunghezza d−onset_germe / ingresso), che e' la forma record-ancorata di
Link 1; (2) il censimento canonico: **1639/1639 record delle 24 orbite sono rigetti
nel transiente** (d med 17 = 0,6% del transiente, colpevole piu' vicina a cheb med 3
max 8, min_ep† med 2 max 5, G† med 142 zeri 0); (3) la caccia preregistrata su
catena-3 (8000 semi freschi, 82.243 record): **F1 morto come previsto** (il bordo
min_cheb<=8 era un quantile: 112 falsificatori, max 19 — quarta soglia-record morta,
trappola qq confermata), **F2 REALIZZATO: i primi 2 LOCK W0-like profondi ai record**
(ride 269 e 384 passi = 2,6 e 3,7 periodi, 3 record = 2 EPISODI — il secondo record
del ride e' DENTRO il ride), **P3 falsificata** (i falsificatori F1 sono per lo piu'
rigetti shallow su record misti vicino al seme, non ride), e **V†: 0 violazioni su
82.243 record** (578 G†=0 tutti fisiologici = ingresso in corso entro t†); (4) la
**SALDATURA**: le parole dei 2 episodi-lock sono LA STESSA parola (101 bit identici
fra semi diversi; il record interno e' il suo shift-10) e appartengono ai **14
testimoni della fascia word-mediated di §100** — la fascia E' la classe delle
parole-porta, la predizione "record ad alto min_ep = tentativi di porta falliti"
e' realizzata su catena disgiunta. Link 1 NON cade, ma il suo evento ("lock W0-like
profondo") e' per la prima volta OSSERVATO ai record, con la geometria del nemico
(rigetto-shallow perpetuo) quantificata.

Strumenti nuovi (alpha1/): `record_divergence_census.py` (+`_summary.json`,
`_records.csv`, `.log`), `record_divergence_hunt.py` (+`_summary.json`, `.log`),
`record_divergence_lens.py`, `record_divergence_esche.py`, `record_lock_autopsy.py`.

## 101a. La DICOTOMIA DEL RECORD (deduttiva)

Setup: record y-min stretto a t con posa (rx,ry) sotto il seme (ry < y_seed_min),
t >= K=101, parola w = svolte[t−K..t). Al record l'heading e' 0 (la mossa che apre una
riga nuova scende: DY[h]=−1 solo per h=0) ⇒ il frame del record e' una PURA
TRASLAZIONE. Germe di w: footprint F(w) = celle visitate dalla parola coi colori
word-determinati (Lemma della Finestra-K §87), bianco altrove; corsa del germe G_w
dalla posa. Ipotesi (A): onset_germe(w) finito (come §98c). Orizzonte della
rilevazione **t† = max(2600, onset_germe + 2080)** (onset_verified richiede n>=2600 e
coda 2080 — lezione V† §91). Residuo-daga R†(w) = prime-letture di G_w in [0,t†)
fuori da F(w) con y_rel >= 1. **d(t) = primo indice i con svolta reale (t+i) != svolta
di G_w (i)**.

- **Lemma 0 (celle basse gratis).** Ogni cella a y_rel <= 0 e' mai-visitata prima di t
  (record stretto: ogni posizione precedente ha y >= ry+1) e non-seme (y_abs <= ry <
  y_seed_min) ⇒ bianca a t. [Terra-check lente B/E3: residuo allargato a y_rel<=0,
  colpevoli basse 0/orbita-0.]
- **Lemma 1 (co-evoluzione).** Per i < d(t) le due corse coincidono (posizioni,
  scritture); la prima differenza avviene a una PRIMA-lettura della continuazione, su
  una cella con colore reale a t diverso dal colore-germe. Per Lemma 0 + Finestra-K
  tali celle stanno in R†(w) (se d < t†) e il colore reale e' NERO (una colpevole).
  Dim: induzione forte; una cella gia' visitata dalla continuazione ha colore
  co-evoluto; F(w) coincide per Finestra-K; y_rel<=0 coincide per Lemma 0.
- **Lemma 2 (pavimento della distanza).** d(t) >= Cheb(cella di divergenza) >=
  min_cheb†(t) (mosse unitarie). [0 violazioni su 112 F1 + 1639 canonici.]
- **Lemma 3 (consumo).** A t+d la corsa REALE legge nera la cella di divergenza e la
  CONSUMA (flip a bianco), svoltando L dove il germe fa R.
- **Lemma 4 (lock del ride).** Se d >= onset_germe: le svolte reali su
  [t+onset_germe, t+d) sono la coda periodica-104 di G_w (con rot%4==0 e drift != 0,
  convenzione onset_verified): l'orbita reale esegue un tratto W0-periodico di
  lunghezza **ride = d − onset_germe** — un lock W0-like di quella profondita'.
- **Lemma 5' (Replay-Lock alla daga).** Se nessuna cella di R†(w) e' nera a t
  (G† = 0), la corsa reale esegue le svolte del germe per t† passi e la finestra
  [t+t†−2080, t+t†−104) e' 104-periodica con rot/drift della highway: il criterio
  operativo di onset del programma e' soddisfatto — e in ogni caso l'orbita esibisce
  un lock W0-like di lunghezza >= t† − onset_germe >= 2080 (20 periodi).

**DICOTOMIA DEL RECORD.** A ogni record censito vale esattamente una:
  (T) d < onset_germe — rigetto nel transiente; la colpevole di divergenza viene
      consumata a t+d; d >= min_cheb†;
  (R) onset_germe <= d < t† — **lock W0-like di ride = d − onset_germe passi**, poi
      consumo della colpevole;
  (E) d >= t† (⇔ G† = 0) — lock >= 2080 e criterio operativo d'onset soddisfatto
      (per i semi del censimento: ingresso in corso; per un'orbita ETERNA
      non-highway, sotto (A)+(B) di §98c, il caso (E) ai record profondi e'
      impossibile — e' il Rifornimento Recente in forma operativa).

**Che cosa dice per Link 1 (riduzione unidirezionale, dichiarata):** Link 1 ("lock
W0-like profondi infinite volte") **⟸** "(R) con ride >= L0, oppure (E), accade
infinite volte ai record". La negazione record-ancorata — l'ETERNA che sta
DEFINITIVAMENTE in (T) — e' ora uno scenario concreto e quantificato: mantenere per
sempre una colpevole DENTRO il transiente del germe di ogni parola presentata
(empiricamente: cheb med 3, d/onset_germe med 0,006). NB onesto: (T)-definitivo NON
nega Link 1 (lock fuori-record possibili); la dicotomia e' un criterio SUFFICIENTE
record-ancorato, non un'equivalenza.

**Struttura per drift (nuova).** La cella di divergenza di un ride vive a y_rel >= 1:
un ride muore SOLO risalendo nel visitato. Un germe con highway a drift-giu' e
transiente pulito non incontra piu' nulla (sotto il record e' vergine, Lemma 0) ⇒
classe (E) = ingresso: **vietata alle eterne**. Corollario: alle eterne, ai record il
cui germe drifta verso il basso, la colpevole e' FORZATA nel transiente (niente
scampo-ride). Censimento canonico: drift-giu' 891/1639, drift-su 748/1639. I 2
episodi-lock realizzati hanno divergenza a y_rel 16–19 (risalita nel visitato),
coerente coi violatori §99 (y_rel 21/25 alla V†).

## 101b. Censimento canonico (24 orbite, 1639 record §89a, 18,4 s)

`record_divergence_census.py`. Gate esterni (assert, tutti verdi): n_records 1639 ==
§89a; tripwire corto 1620 == §89a; somma G corta 225.012 == §89b; da_seme 3.722 ==
§89b; hist G(0..10) == §89b; hist per-record min_ep corto == §98. Tripwire nuovi
(zero violazioni): **T-DIV** (d per-svolte == d per-celle: due derivazioni
indipendenti) 1639/1639; **T-VDAGGER** (G†=0 ⇒ t_on−t <= t†) 0 casi G†=0; **T-SCALA**
sulla cella di divergenza profonda (ep <= y_rel) 1567/1567 (72 divergenze su celle
shallow di record misti).

| osservabile | valore |
|---|---|
| classi | **T 1639/1639, R 0, E 0** |
| d | med 17, min 2, max 268; d/onset_germe med 0,006 |
| onset_germe | med 2800, min 35, max 54.119 |
| cella di divergenza | y_rel med 2 max 11; cheb med 3 max 11; ep med 2 max 8 |
| min_cheb† per-record | med 3, **max 8** (hist: 1→46, 2→702, 3→470, 4→200, 5→155, 6→54, 7→11, 8→1) |
| min_ep† (813 record interamente profondi alla daga) | med 2, max 5 — chiude il flag "min_ep† indeterminato" di §100 |
| G† | med 142, max 1700, **zeri 0** |
| monotonia d ~ min_cheb | d med per min_cheb 1..8: 2/5/20/36,5/46/51,5/51/69 |
| parole | 1459 distinte/1639; ripetute fino a 11 volte su 8–10 orbite (onset_germe 714–33.065: le ripetute cross-orbita NON sono le veloci) |
| parole veloci (onset_germe<=520) | 161 record, **24/24 orbite**; min_cheb med 3 max 8 |

La quota del censimento alla V† (§101 roadmap) e' compresa: ~1639 eval a orizzonte
t† (med ~4880), 18,4 s totali — il costo temuto (~50k eval) era sovrastimato.

## 101c. Caccia preregistrata (catena-3, 8000 semi, 82.243 record, 98,5 s)

`record_divergence_hunt.py`. Preregistrazione IN TESTA AL FILE prima della run:
catena-3 BASE3 = xs(BASE ^ 0x94D049BB133111EB) = 10075261518452958373, disgiunzione
VERIFICATA contro catena-1 (5000) e catena-2 (25000); falsificatori F1/F2, predizione
P3, tripwire V†, potenza >= 5000 record con G†>=1 (realizzata: 81.665). GATE
canonici: 24/24 orbite bit-identiche al censimento §101a (6 campi per-orbita + hist
min_cheb† + hist min_ep†). Verdetto EMESSO DAL TOOL:

- **F1 (bordo spaziale) REALIZZATO — il bordo muore:** 112 falsificatori
  min_cheb† > 8, max **19** (8→19 con n; quarta soglia-record morta dopo min_ep
  5→8→12, trappola qq). Post-mortem: 87/112 su record MISTI vicino al seme
  (min_ep† non definito), 6/112 di classe R, 22/112 profondi con min_ep<4;
  onset_germe med 265 (parole medio-veloci), d med 90, **0 violazioni di Lemma 2**.
- **F2 (lock ai record) REALIZZATO:** 3 record di classe R con ride >= P =
  **2 EPISODI indipendenti** (il 2° record di rng 6149067202803567465 cade DENTRO il
  ride del 1°: contare episodi, lezione §100). Episodio A: rng 16989344815867729101,
  t=4588, onset_germe 55, **ride 269** (2,6 periodi). Episodio B: rng
  6149067202803567465, t=18142/18152, onset_germe 65/55, **ride 384** (3,7 periodi).
  Verificati **3/3 PASS bit-identici** dalla lente indipendente
  (`record_lock_autopsy.py`; piu' 8/8 sul campione F1 ai min_cheb massimi,
  2 sovrapposti agli F2).
- **P3 FALSIFICATA** (predizione preregistrata: ogni F1 ha classe R o min_ep>=4):
  103/112 la violano — la coda spaziale e' dominata da rigetti shallow su record
  misti, non da ride. La predizione era sbagliata; a verbale.
- **V†: 0 violazioni su 82.243 record.** 578 record a G†=0, TUTTI fisiologici
  (t_on − t <= t†: ingresso in corso). Il meccanismo Replay-Lock alla V-daga e'
  perfetto a scala 82k (la controparte: a V(onset+P) corto §99 aveva 2 violazioni
  su 29k — l'orizzonte della RILEVAZIONE guarisce, come da §100).
- min_ep† max su freschi: **7** (5 canonico → 7: quantile, coerente con qq).
- d max 2711 (classe T: sonde profonde nel transiente esistono).

**LA SALDATURA (fascia = porta):** le parole dei 2 episodi-lock sono **la stessa
parola di 101 bit** (semi diversi, catena disgiunta), il record interno all'episodio
B e' il suo **shift-10**, e la parola sta nei **14 testimoni della fascia
word-mediated di §100** (0 sovrapposizioni coi testimoni §99 catena-1, con la §100
catena-2 si'). La lettura §100 "onset_germe 55 == violatori d'orizzonte: aria di
ingressi mancati" e la domanda §101 di roadmap "record ad alto min_ep = tentativi di
porta falliti?" hanno ora un testimone POSITIVO su catena disgiunta: **la fascia e'
la classe delle parole-porta; i lock ai record esistono e passano da li'.**

## 101d. Stato di Link 1 dopo §101

1. L'evento di Link 1 (lock W0-like profondo) e' **osservato ai record** (2 episodi
   su 82.243 record, ~2,4e-5 per record; prima era inferito indirettamente dai 2
   violatori d'orizzonte §99). Il tasso e' irrilevante per Link 1 (serve "infinite
   volte", non densita'), ma la NON-VACUITA' della classe (R) e' fatto nuovo.
2. La dicotomia rende Link 1 implicato da: "(R)/(E) infinite volte ai record".
   Lo scenario nemico ((T)-definitivo) e' il **mantenimento perpetuo di colpevoli
   in-transiente**: geometria quantificata (cheb med 3; coda spaziale VIVA fino a 19
   e oltre — F1 — quindi niente palla fissa: il transiente stesso e' l'oggetto).
3. **Struttura per drift:** ai record con germe a drift-giu' (54% dei canonici),
   l'eterna non ha lo scampo del ride: colpevole forzata nel transiente. Il fronte
   deduttivo nuovo: che cosa DEVE pagare un'orbita per tenere il transiente di ogni
   parola drift-giu' presentata sempre sporco? (Parente della tensione camping §87v,
   ma ora l'oggetto e' finito per-parola: il read-set del transiente.)
4. **Il fronte parole veloci:** i lock realizzati passano tutti dalla fascia §100
   (onset_germe 55/65, parole condivise cross-seme, shift-classi). La fascia e'
   FINITA nel campione (14 parole, 10 classi mod shift). Se l'occorrenza della
   fascia ai record delle eterne fosse dimostrabile (i.o.), Link 1 si ridurrebbe a
   "il transiente-55 non puo' essere sempre sporco" — enunciato su UN oggetto di
   ~55 letture. L'occorrenza resta il buco (come sempre: §98.0).
5. Cosa NON e' cambiato: nessun teorema d'occorrenza; (T)-definitivo non escluso;
   trappola (i): nessuna misura sul finito decide l'eterno.

## 101e. Pannello (in sessione, PRIMA del verbale)

- **Lente A (macchinario indipendente):** `record_divergence_lens.py` — footprint
  ricostruito dalla GRIGLIA REALE al tempo t (meccanismo diverso da virtual_walk:
  se Finestra-K o virtual_walk avessero un bug, qui divergerebbe), simulatore
  proprio: **40/40 record bit-identici** (d, classe, y_rel/cheb della cella di
  divergenza). Piu' **3/3 F2 e 8/8 F1** (`record_lock_autopsy.py`).
- **Lente B (esche):** `record_divergence_esche.py` — baseline pulita (0 scatti),
  **3/3 esche beccate** (E1 footprint monco: 85/90 scatti T-DIV; E2 prime-letture
  sfasate +1: 90/90; E4 svolte reali sfasate +1: 90/90) + **terra-check Lemma 0
  verde** (residuo allargato a y_rel<=0: colpevoli basse 0). Onesta': la prima
  versione di E4 (colori a t−1) NON PUO' scattare — l'unica cella scritta a t−1 e'
  la posa a t−1, che e' footprint; i colori del residuo sono stabili sul passo.
  Istanza del corollario di metodo (cc): un'esca che non puo' fallire non e'
  un'esca; promossa a verifica e sostituita.
- **Lente logica (autocritica, esiti):** (i) la prima formulazione del Lemma 5'
  ("G†=0 ⇒ ingresso") e' stata INDEBOLITA alla forma corretta: il criterio
  operativo d'onset e' soddisfatto alla finestra t†, il "per sempre" non e' dedotto
  — per le eterne si usa la contrapposizione, per i convergenti e' l'ingresso in
  corso (misurato: 578/578 fisiologici); (ii) la riduzione a Link 1 e' dichiarata
  UNIDIREZIONALE (⟸), (T)-definitivo non nega Link 1; (iii) i 3 record F2 = 2
  episodi (consecutivi nel ride condividono il lock); (iv) P3 falsificata e
  riportata come tale, senza riscrittura post-hoc.

## 101f. Trappole (conferme e istanze)

- **(qq) confermata la quarta volta:** min_cheb† <= 8 (1639/1639 canonici) muore a
  19 su catena-3 con 112 falsificatori. Le soglie dell'orologio-record e ORA anche
  del righello-record sono quantili con data di scadenza. Nessuna nuova soglia
  enunciata in §101 (solo distribuzioni e falsificatori).
- **(pp) applicata:** i 578 G†=0 sono censiti con semantica dichiarata
  (fisiologici/violazioni), zero scarti silenziosi; il ramo E del censimento
  canonico (0 casi) e' riportato esplicitamente.
- **(cc)-corollario applicato:** esca E4-v1 incapace di scattare, riconosciuta e
  sostituita (vedi 101e).
- **(hh) etichetta:** il negativo F2=0 della classe R sui canonici (0/1639) e' della
  POLITICA "24 orbite selezionate per onset alto": la catena-3 fresca la smentisce
  (28 classe R). I negativi vanno sempre etichettati col campione.

## 101g. Domande aperte / programma §102

1. **Occorrenza della fascia:** le parole-porta (14, 10 classi mod shift) occorrono
   ai record con quale meccanismo? Sono word-determinate: enumerare le parole a
   onset_germe <= 200 realizzabili record-compatibili (K=101 e' grande, ma la fascia
   suggerisce che le realizzate siano POCHE classi); misurare il tasso di occorrenza
   per orbita e per epoca; legame con la porta/A1 §78 (fase, footprint 44).
2. **Il costo del transiente sporco (drift-giu'):** per una parola w drift-giu'
   fissata, il read-set del transiente e' finito e word-determinato; "colpevole nel
   read-set a ogni presentazione" e' un vincolo per-parola alla §89/Muro. Attaccare
   con la macchina del Muro (U1/rigioco) la versione: "esiste una parola drift-giu'
   veloce con transiente NON mantenibile"?
3. **min_cheb: crescita del massimo con n** (8→19): scala log? Misurare su catene
   piu' lunghe SOLO dentro una preregistrazione con aspettativa di morte (qq).
4. Ereditati: rientri §98g.2, scia-teorema §98g.3, separatori §97, fuggenti vs
   nere-D>=400, retro-nota §91c.3, stress-2 bianche, h1=1.

## 101h. Inventario file (alpha1/)

- `record_divergence_census.py` (+`_summary.json`, `_records.csv`, `.log`) —
  censimento canonico d/classe/ride/min_cheb†/min_ep†/G†/drift, gate §89a/b/§98,
  tripwire T-DIV/T-VDAGGER/T-SCALA.
- `record_divergence_hunt.py` (+`_summary.json`, `.log`) — caccia preregistrata
  catena-3 (F1/F2/P3/V†), gate canonici bit-identici, verdetto dal tool.
- `record_divergence_lens.py` — lente A: ricontro indipendente (footprint dalla
  griglia reale), 40/40.
- `record_divergence_esche.py` — lente B: 3 esche + terra-check Lemma 0.
- `record_lock_autopsy.py` — autopsia F2/F1 con lente indipendente (5/5 + 8/8),
  episodi e righe-nel-ride.
