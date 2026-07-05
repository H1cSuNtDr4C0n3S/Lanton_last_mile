# ADDENDUM §98 — L'ANELLO DI OCCORRENZA: LA SCALA, IL RIFORNIMENTO RECENTE, min_ep<=5

**Riepilogo in una frase:** l'anello di occorrenza (scala §91c punto 4: dalla vietanza di
w101 a una famiglia INEVITABILE ai record) e' stato riformulato in unita' di EPOCHE-RECORD
e ha prodotto tre fatti: (1) il **LEMMA DELLA SCALA** (deduttivo, terra-verificato su
188.234 colpevoli profonde, T1-T4 zero violazioni): ai record profondi la pre-semina
antica NON esiste — ogni colpevole e' auto-dipinta dopo l'apertura della propria riga,
entro y_rel <= k_max epoche; (2) il censimento in epoche: eta' mediana 3 epoche (contro
2002 passi — il "detrito antico" di §89b era un artefatto dell'orologio, trappola nn) e,
al livello per-record che il pannello ha imposto (lente C, ROSSO riparato in sessione):
**min_ep <= 5 su 1174/1174 record profondi** — ogni record profondo reale ha una
colpevole dipinta nelle ultime 5 epoche — con lato-scia molto piu' forte del previsto
(91,5% dei record ha una colpevole word-proximal eta'<=2K, mediana del minimo 107 = K+6,
il pattern delle autopsie G=1 §89b; 88,2% ne ha una dipinta entro P dall'apertura della
riga, min_lag mediano 0 = la scala si rifornisce da sola); (3) la via "enumerazione
(parola, cella-di-scia) a profondita' fissa" NON e' pero' una famiglia inevitabile:
l'8,5% dei record profondi non ha NESSUNA colpevole entro 2K (coda fino a 24.464 passi)
=> ogni finestra-parola fissa lascia una coda scoperta, e G=1 (l'unico punto dove la
scia DECIDE da sola) non e' dimostrato inevitabile (raro nel campione: min 1, med 87).
L'inevitabilita' sopravvive al livello EVENTO, condizionale e dichiarato tale:
TEOREMA DEL RIFORNIMENTO RECENTE (ipotesi A/B/C esplicite, §98c). Il fronte nuovo e
esatto: la geometria dei RIENTRI e il perche' del min_ep <= 5.

Strumento: `alpha1/record_supply_census.py` (+`_summary.json`, `.log`; Ryzen, 15 s).
Pannello scettici: 3 lenti IN SESSIONE, 1 ROSSO riparato PRIMA del verbale (§98e).

## 98.0 Che cos'era l'anello di occorrenza, e che cosa e' adesso

Stato prima di §98: il Muro dietro l'Uno (§90d/§91c, modulo Ledger Sporco v2 §94-§97)
vieta w101 ai record lontani delle eterne — ma nessuna orbita la presenta (0/1639,
§89a): vietanza senza occorrenza non cattura nulla. Il punto 4 della scala a Link 1
chiedeva una famiglia di parole INEVITABILE ai record; §89a aveva spostato l'osservabile
sul conteggio delle colpevoli G; §89c aveva nominato l'enumerazione delle coppie
(parola, cella-di-scia), mai eseguita (§90-§97 sono andati su w101/Muro).

Dopo §98 l'anello ha questa forma:
- **la domanda "quale parola occorre" non ha una risposta a famiglia finita a
  profondita' fissa**: la coda dell'8,5% dei record profondi e' rifornita interamente
  fuori da ogni finestra-parola limitata provata (fino a 2K; code osservate a 24.464
  passi) — nel campione, e con la direzione del bias dichiarata (§98d);
- **la domanda giusta e' per-evento**: in epoche-record il rifornimento e' universale
  e strettissimo (min_ep <= 5, 1174/1174). Sotto le ipotesi A/B/C di §98c, un'orbita
  eterna DEVE eseguire per sempre l'evento pittura-e-preserva in ogni finestra
  scorrevole di k* epoche. Questo e' il sostituto sano della "famiglia inevitabile":
  un enunciato di dinamica della scala dei record, senza quantificatori su parole
  (ma con le ipotesi per-parola SPOSTATE, non dissolte — lente C, §98e).

## 98a. Strumento e censimento (24 orbite, stessi 1639 record di §89a/b)

`record_supply_census.py` riusa la pipeline §89 (run_collect_records, eval_word K=101,
replay deterministico con tripwire svolte==riferimento) e aggiunge: tempi di prima
visita per riga, ultima pittura a nero per cella, conteggio epoche, minimi per-record.

**Gate esterni (tutti assert, tutti verdi):** n record censiti 1639 == §89a; tripwire
G>=1 1620 == §89a; n colpevoli totali 225.012 == §89b; da_seme 3.722 == §89b; istogramma
G(0..10) == §89b; eta' (med, max) == §89b. Onset == header dumps 24/24.

**Tripwire nuovi (zero violazioni):**
- T1 (autofornitura): 188.234/188.234 colpevoli profonde (riga < y_seed_min) mai di
  seme e sempre dipinte dall'orbita;
- T2 (scala, passi): paint_t >= t_record(riga della cella), 188.234/188.234;
- T3 (terra): prima visita della riga -m == t del record m-1, 1.854/1.854 righe
  (misurata nel replay, non assunta);
- T4 (scala, epoche): #record in (paint_t, t] <= y_rel, 188.234/188.234.

**Numeri per-cella (colpevoli profonde, n=188.234):**

| osservabile | valore |
|---|---|
| eta' in EPOCHE (ep) | med 3, max 31; cum: <=1 22,9%, <=3 59,1%, <=5 78,0%, <=8 91,5%, <=13 97,8%, <=31 100% |
| eta' in PASSI | med 2002, max 235.817, >=10P 60,2% (la coda "antica" di §89b) |
| y_rel | med 13, max 61; k_max residuo per record: med 19, max 75 |
| lag pittura dall'apertura della riga | med 26.645 passi; <=P 5,2%, <=10P 12,5%; esp=1 4,0% |
| quota di rientro q = y_rel - ep (identita' esatta) | med 9, max 55; cum: <=13 73,5%, <=21 92,6% |
| word-proximal: eta' <= 2K | 10,6% (<=5P: 27,5%) |

**Numeri per-record (1.174 record interamente profondi — riparazione lente C):**

| osservabile (minimo sulle colpevoli del record) | valore |
|---|---|
| min_ep | med 2, **max 5** (hist: 1->566, 2->397, 3->182, 4->26, 5->3) |
| min_age | med **107** (= K+6), max 24.464; ha-giovane <=2K: **91,5%**, <=5P 94,8%, <=10P 95,9% |
| min_lag dall'apertura riga | med **0**; ha-colpevole-di-discesa <=P: **88,2%**, <=10P 93,5% |
| G | min 1, med 87 |

Lettura dei due livelli (lezione del pannello, trappola oo): per-CELLA il grosso della
massa di rifornimento e' vecchio in passi e da escursione (60% >= 10P, lag med 26.645);
per-RECORD il minimo e' quasi sempre giovanissimo — a quasi ogni record profondo c'e'
ALMENO una colpevole di scia recente (107 passi = appena fuori finestra) o di discesa
(min_lag 0: dipinta al record che ha aperto la sua riga — la scala si rifornisce da
sola), e SEMPRE una entro 5 epoche. I due quadri non si contraddicono: i record a G~87
portano ~87 celle per lo piu' vecchie E una-due giovanissime.

## 98b. LEMMA DELLA SCALA (deduttivo) e l'artefatto dell'orologio

**Lemma della Scala.** Ipotesi: partenza alla riga 0, mosse unitarie, record y-min
STRETTI. Allora: (i) la riga assoluta -m e' visitata per la prima volta esattamente al
record m-1 della scala (per stare a riga -m serve y < y_min corrente, che E' il record;
i minimi scendono di 1 alla volta); (ii) a un record censito, ogni cella-residuo con
riga r < y_seed_min non e' di seme, quindi se e' nera la sua ultima visita e' stata una
svolta R dell'orbita: DIPINTA (autofornitura), con paint_t >= t_record(riga) (dipingere
richiede visitare, la riga apre al suo record; l'uguaglianza e' ammessa: la cella-posa
del record e' dipinta nera al record stesso — misurato, min_lag mediano 0);
(iii) ep := #record in (paint_t, t] (incluso il record d'uso; ep >= 1 perche' la
lettura dei colori precede il passo t) soddisfa ep <= y_rel. QED.

Identita' di contorno (aritmetica dai conteggi della scala): la quota di rientro
q = riga_colpevole - y_min(paint_t) soddisfa **q = y_rel - ep esattamente**: "dipinta
poche epoche fa" e "dipinta in un'escursione scesa a ~q righe dal minimo di allora"
sono la stessa misura vista dai due capi.

**L'artefatto dell'orologio (trappola nn).** §89b leggeva "detrito quasi statico, eta'
mediana 18 periodi, pre-semina antica decisiva dopo 10^5 passi". In epoche-record la
stessa popolazione ha eta' mediana 3 e massimo 31: il detrito e' "antico" solo perche'
gli intervalli fra record sono enormi (fino a 134.058 passi osservati). Nella scala dei
record il rifornimento e' recentissimo, e nessuna colpevole profonda precede l'apertura
della propria riga (T2): la pre-semina antica ai record profondi non esiste come
risorsa. Esiste solo il rifornimento continuo.

## 98c. TEOREMA DEL RIFORNIMENTO RECENTE (condizionale; ipotesi A/B/C esplicite)

**Enunciato.** Sia O un'orbita eterna non-highway e t un suo record y-min stretto con
posa sotto il seme e residuo interamente profondo, con parola w = ultime K svolte.
Ipotesi (per-parola): (A) il germe di w ha onset finito; (B) certificato d'orizzonte
alla V† (lezione §91: le prime letture fino all'orizzonte di RILEVAZIONE T=2600, non
solo onset+P) — e il certificato deve investire TRE oggetti: il residuo, k_max(w), e la
classificazione "record profondo" (lente C: un record profondo per V(onset+P) puo' non
esserlo per V†). Allora almeno una cella del residuo di w e' nera al tempo t (Cono §87:
davanti e riga-0 bianche gratis; Finestra-K: footprint word-determinato; Replay-Lock:
residuo tutto bianco => la corsa rigioca il germe => onset => contraddice l'eternita'),
e per il Lemma della Scala quella cella e' stata dipinta da O nelle ultime
y_rel <= k_max(w) epoche-record.

**Corollario (l'evento inevitabile, forma uniforme).** Sotto (A) per OGNI K-parola
presentabile e (B) per ciascuna, posto (C) k* = sup di k_max† sulle K-parole valide
(esiste finito per finitezza di 2^K dato (A), ma e' una costante ESISTENZIALE non
calcolata — il 75 del censimento e' un massimo campionario all'orizzonte corto, NON
quella costante, cosi' come ep_max 31 < y_rel max 61 e' campione e non bound), ogni
eterna non-highway esegue, in ogni finestra scorrevole di k* epoche-record che termina
a un record profondo tardivo, almeno un evento "pittura-e-preserva": svolta R su una
cella a quota di rientro <= k*, mai piu' riletta fino all'uso.

**Caveat (onesta', trappole i/h):**
1. (A) e' SEMI-decidibile (simulazione con cap): il complemento non e' certificabile
   con corsa finita. Ipotesi APERTA, con supporto empirico dichiarato come evidenza e
   non prova (zero buchi K<=14 §87b; 1639/1639 parole reali qui). Una K-parola con
   germe senza onset sarebbe essa stessa un controesempio alla congettura in forma di
   configurazione finita: la circolarita' e' dichiarata;
2. il censimento usa V(onset+P) come §89a: il tripwire 1620/1620 sul residuo-
   sottoinsieme e' empiricamente PIU' forte del necessario, ma un suo ipotetico
   fallimento NON avrebbe falsificato il teorema in forma V† (asimmetria dichiarata);
3. il teorema forza l'ESISTENZA dell'evento, non un tasso: i numeri di §98a (ep med 3,
   min_ep <= 5, q med 9) sono misure sulle 24 orbite (selezionate per onset alto,
   trappola h; lettura within-orbit), non parti dell'enunciato.

## 98d. La via-parola: che cosa muore e che cosa no (verdetto corretto dal pannello)

La prima stesura di questo paragrafo enunciava un no-go dalle frazioni per-cella
(10,6% word-proximal). La lente C lo ha bocciato (non-sequitur per-cella/per-evento,
trappola oo) e la statistica per-record — calcolata in sessione — ribalta il colore
del quadro pur salvando la conclusione strategica:

1. **La scia e' quasi-universale ai record reali** (sorpresa, in direzione opposta al
   no-go ingenuo): il 91,5% dei record profondi ha una colpevole word-proximal
   (min_age med 107 = K+6 — la scia appena fuori finestra, lo stesso oggetto delle
   autopsie G=1 §89b) e l'88,2% ne ha una dipinta entro P dall'apertura della riga.
   Il vincolo di autoconsistenza di §89c governa quindi MOLTO piu' del bordo G=1.
2. **Ma non e' inevitabile a profondita' fissa**: 100/1174 record profondi (8,5%) non
   hanno NESSUNA colpevole entro 2K, con coda del minimo fino a 24.464 passi; le
   frazioni scoperte restano non nulle a ogni soglia provata (5P: 5,2%; 10P: 4,1%).
   Un'eterna puo' vivere nella coda: una famiglia di parole a profondita' fissa W
   lascia scoperti i record il cui rifornimento minimo supera W, e il campione mostra
   che esistono e non sono rarita' da survivorship inversa (qui il bias di selezione
   AIUTEREBBE la scia: orbite a onset alto = tante escursioni; la coda c'e' comunque).
3. **G=1 non e' dimostrato inevitabile** (riformulazione imposta dalla lente C: la
   mediana 87 su 24 orbite selezionate prova rarita' nel campione, non una modalita'
   per le eterne): il punto dove la scia DECIDE da sola resta un bordo, mappato
   (§89b/c) ma senza teorema di ritorno.

Verdetto sull'enumerazione §89c (mai eseguita): POTATA, senza esecuzione, con la
motivazione corretta — non "il rifornimento non e' di scia" (falso al livello
per-record) ma: (a) il suo evento-bersaglio (G=1 salvata dalla scia) non e' dimostrato
inevitabile; (b) la sua copertura a profondita' fissa e' bucata dalla coda dell'8,5%;
(c) il suo esito, in entrambi i rami (esaurimento/esplosione), non deciderebbe quindi
nessun enunciato per le eterne. La scia quasi-universale (91,5%) e' pero' un fatto
NUOVO e positivo: la coppia (parola, cella-di-scia) e' il meccanismo DOMINANTE di
rifornimento ai record reali — solo, non e' una gabbia.

**Stato della scala a Link 1 dopo §98:** punto 4 riformulato — *(4') dimostrare che il
rifornimento perpetuo (pittura-e-preserva in ogni finestra di k* epoche, quota <= k*)
e' incompatibile con la non-entrata* — oppure trovare l'ostruzione inversa. Con il
sotto-bersaglio quantitativo nuovo e falsificabile: perche' min_ep <= 5? (Se il "5" e'
struttura e non campione, la finestra vera dell'evento inevitabile e' costante, non
k*.) Il Muro (punti 1-3, w101) resta il ramo vietanza, non toccato da §98.

## 98e. Pannello scettici (3 lenti in sessione, PRIMA del verbale — lezione §93/§94)

- **Lente A (ricontro indipendente): VERDE.** Macchinario riscritto da zero (griglia a
  insieme-di-nere, colori/paint_t ricostruiti dalla TRAIETTORIA+turns invece che dal
  replay a griglia — meccanismo diverso), orbite 0/13/22: 18/18 campi bit-identici
  (records, deep_records, colpevoli_profonde, ep_sum, ep_max, G_sum), onset == header
  3/3, tripwire T1/T4 della lente mai scattati su 29.019 colpevoli.
- **Lente B (esche di falsificabilita'): VERDE, 4/4 beccate** con controllo positivo
  (baseline bit-identica prima delle mutazioni): M1 bisect_left su hi -> T4 "ep 0
  fuori [1,1]"; M2 riga sotto -> T2 "paint 937 < apertura 1306"; M3 seme dipinto a
  t=0 -> gate §89b "da_seme 0 != 3722"; M4 senza filtro y<y_seed_min -> gate §89a
  "n record != §89a". Rete a due strati verificata: tripwire interni per la semantica
  della scala, gate incrociati per le corruzioni di classificazione.
- **Lente C (logica): ROSSO, riparato in sessione.** Due non-sequitur veri nella bozza:
  (1) no-go dedotto da frazioni per-cella dove serve l'esiste-per-record — riparato
  aggiungendo i minimi per-record al censimento (i numeri hanno RIBALTATO il colore:
  91,5% scia-proximal; il no-go sopravvive solo nella forma-coda, §98d); (2) "anello
  chiuso / famiglia-evento senza ipotesi di parola" — degradato a riformulazione
  CONDIZIONALE con (A) germe-onset per-parola (semi-decidibile, ipotesi aperta),
  (B) V† su tre oggetti, (C) k* esistenziale non calcolato. Piu' gialli recepiti:
  ">=" nell'apertura riga, convenzione ep dichiarata, ipotesi della scala esplicite,
  "illimitato" -> "fino a 134.058 osservato", n=3 per le autopsie G=1, direzione del
  bias di survivorship dichiarata.

## 98f. Trappole nuove

- **(nn) l'eta' e' relativa all'orologio** (§98b): "detrito antico / quasi statico /
  pre-semina" cambiano segno cambiando unita' (passi vs epoche-evento). §89b leggeva
  staticita' dove la scala dei record vede rifornimento a mediana 3 epoche. Prima di
  dichiarare una risorsa "antica" (e attaccarla alla Blocco Antico), misurarla
  nell'orologio degli eventi che la consumano. Parente di (h) e della lezione §72.
- **(oo) le frazioni per-cella non decidono enunciati per-evento** (§98d, beccata
  dalla lente C prima del verbale): un meccanismo che deve valere "almeno una volta
  per evento" va misurato sui minimi per-evento, non sulla massa per-cella — la massa
  e' dominata dagli eventi grossi (G~87) e puo' nascondere un minimo quasi-universale
  (91,5%) o, dualmente, una coda scoperta (8,5%). Parente di (hh) (il floor e' della
  politica) e di (h).

## 98g. Domande aperte / prossimo (§99)

1. **min_ep <= 5: struttura o campione?** Il fatto piu' stretto del censimento
   (1174/1174, hist 566/397/182/26/3 — decadimento rapido). Se e' struttura, l'evento
   inevitabile ha finestra COSTANTE (5 epoche), non k*: enunciato-bersaglio
   falsificabile ("esiste un record profondo reale con min_ep > 5?" — cercarlo su
   orbite non selezionate per onset alto, per sterilizzare la trappola h).
2. **Geometria dei RIENTRI**: l'evento inevitabile e' una svolta R a quota <= k_max,
   1-3 epoche prima dell'uso, mai riletta fino al record. Oggetto suggerito: i
   SEGMENTI di rientro (sotto-cammini co-moving al MINIMO CORRENTE, non alla parola)
   — profondita' di rientro, drift x rispetto alla colonna dei record, identita'
   R-L=Delta B (§96) sul segmento; collegare al rotore §77 (le escursioni sono gli
   stalli) e alla coda lunga §79.
3. **La scia quasi-universale** (91,5%, min_age med K+6): perche' i record reali
   arrivano quasi sempre con una colpevole appena-fuori-finestra? E' un teorema di
   scia alla §86 (le 3 celle di scia arricchite) esteso alla profondita' K, o
   contingenza? Se diventasse teorema, la coda dell'8,5% sarebbe l'unico habitat
   possibile per un'eterna — fronte enumerabile NUOVO (i record senza scia giovane).
4. Ereditati: esperimenti separatori §97 (collo), fuggenti nuove vs nere-D>=400,
   retro-nota §91c.3, stress-2 bianche, h1=1.

## 98h. Inventario file

- `alpha1/record_supply_census.py` (+`record_supply_census_summary.json`,
  `record_supply_census.log`) — censimento autofornitura/scala/epoche, T1-T4, gate
  §89a/b, minimi per-record (riparazione lente C), per-orbita per la lente A.
- `docs/OCCURRENCE_SUPPLY_ADDENDUM.md` — questo addendum.
- Pannello: script delle lenti nello scratchpad di sessione (lens_a_recount.py,
  make_mutants.py + rsc_M1..M4); esiti integrali a verbale in §98e.
