# ADDENDUM §89 — RECORD-WORD CENSUS (sessione in corso)

## 89a. Le parole reali ai record y-min delle 24 orbite

**Riepilogo in una frase:** le parole che le orbite reali presentano davvero ai record
sono LONTANE dal minimo vivo (burden1 mediano ~317 a K=101, minimo 12; mai <= 6; zero
match con w101), MA il meccanismo del Cono e' verificato in natura senza eccezioni
(1620/1620 record lontani dall'onset hanno almeno una cella-residuo nera) e in tre casi
l'orbita e' passata a UNA sola cella nera dall'ingresso: l'osservabile giusto per l'anello
di occorrenza non e' la parola a fardello basso, e' il CONTEGGIO DELLE COLPEVOLI.

Strumento: `alpha1/record_word_census.py` (+`_summary.json`, `.log`; Ryzen, 14 s).
Metodo: per ciascuna delle 24 orbite lunghe (semi da `dumps_all.txt`), corsa fino
all'onset con rilevazione dei record y-min STRETTI pre-onset (assert heading=su
all'arrivo, 24/24 gate onset == header dumps); censiti solo i record sotto il bbox del
seme (semipiano davanti bianco garantito); per ogni record la parola delle ultime K
svolte (K = 18, 101), burden1/residuo via `eval_word`, e replay con lettura dei colori
REALI delle celle-residuo al tempo del record.

**Numeri (1639 record censiti, 52-99 per orbita, early scartati 5-348):**

- burden1 a K=101: min 12, mediana 317, max 3956; nessun record <= 6; a K=18: min 20,
  mediana 273 (il minimo astratto record-compatibile a K=18 e' 10, §87d: le parole REALI
  restano sopra anche il pavimento astratto).
- match esatti con w101 (copre tutta la famiglia sigma^m*tau*w101): **0** su 1639.
- parole a burden1=0 ai record: **0** (come il Teorema §88 esige per record lontani
  dall'onset); eval senza onset: 0.
- **TRIPWIRE DEL TEOREMA, 1620/1620:** per ogni record con t_on - t > onset_germe + P,
  almeno una cella del residuo e' risultata NERA nei colori reali. Zero violazioni: il
  meccanismo Cono+Finestra-K+Replay tiene su dati reali, non solo in astratto.
- Colpevoli (celle-residuo nere) ai record: scalano col burden, ma la coda bassa esiste:
  **3 record con UNA sola colpevole** (2 a burden 13, 1 a burden 31) — orbite passate a
  una cella dall'ingresso, l'evento-pigeonhole osservato in natura.

**Lettura onesta (anello 1 della chiusura):** l'ipotesi "parole vive a fardello basso
inevitabili ai record" NON e' supportata a questa scala: le parole reali ai record del
caos hanno fardello di centinaia. Caveat di survivorship (trappola h): queste 24 orbite
sono selezionate per onset alto (~250-313k) — proprio le orbite i cui record NON
convertono; la lettura e' within-orbit. Riformulazione produttiva per §89b: studiare la
DINAMICA del conteggio delle colpevoli fra record consecutivi (quanto spesso scende a 1?
cosa succede alla cella colpevole superstite fra un record e il successivo? eta' delle
colpevoli vs lag K della pre-semina §87.7c).

Inventario: `alpha1/record_word_census.py`, `record_word_census_summary.json`,
`record_word_census.log`.

## 89b. La dinamica delle colpevoli fra record consecutivi

**Riepilogo in una frase:** G(i) = colpevoli al record i e' una passeggiata quasi bilanciata
(mediana 96, P(giu')=0.43, P(su)=0.47) su detrito quasi-statico (96% delle colpevoli ancora
nere al record dopo) con coda bassa reale (7 record a G<=3), e nelle TRE autopsie a G=1 la
colpevole unica ha eta' 102/114/104 contro il minimo teorico K=101 e distanza Chebyshev
3-6: **al bordo del pigeonhole l'orbita e' salvata dalla propria scia appena invecchiata**
— la trappola (v) misurata nel punto esatto dove decide.

Strumento: `alpha1/record_guilty_dynamics.py` (+`_summary.json`, `.log`; 16 s).
Gate: stessi 1639 record e stesso conteggio tripwire di §89a (cross-check assert).

**Numeri:**

- G: min 1, mediana 96, max 1700; coda bassa: 3 record a G=1, 2 a G=2, 2 a G=3,
  48 a G<=10. Transizioni: P(giu') 0.425, P(su) 0.471, dG mediano 0 (passeggiata quasi
  bilanciata, leggera deriva in su). Intervallo fra record: mediano 94 passi (< P=104,
  i record vengono a raffiche in discesa) ma max 134058 (stalli enormi altrove).
- Persistenza: le colpevoli del record i sono ancora NERE al record i+1 nel 96% dei casi
  (mediana; media 87%) — il detrito e' quasi statico, coerente col rotore §77. Ma restano
  COLPEVOLI (nel nuovo residuo) solo ~48%: e' il residuo che si sposta con la parola,
  non il detrito che si muove.
- Eta' delle colpevoli: mediana 1856 (~18 periodi), 60% >= 10 periodi, max 235817;
  3722 istanze sono celle del SEME mai ridipinte (detrito primordiale ancora decisivo
  dopo >10^5 passi). NOTA ONESTA: la soglia eta' >= K = 101 vale nel 100% dei casi ma e'
  FORZATA per costruzione (una cella dipinta negli ultimi K passi appartiene al footprint
  e quindi non puo' stare nel residuo): e' un cross-check dell'implementazione, non una
  scoperta. La scoperta e' la DISTRIBUZIONE sopra K: il grosso del blocco e' detrito
  vecchio di 10-100+ periodi o di seme.
- Geometria: Chebyshev delle colpevoli dalla posa record: mediana 15, max 75 — coincide
  coi raggi dello Spoiler Vecchio (§87: med 15, max 68). Consistenza esterna.
- **Autopsie G=1 (l'evento-pigeonhole):** orb 0 t=55962 (burden 13, cella rel (-3,3),
  eta' 102, cheb 3), orb 18 t=2552 (burden 13, (-1,5), eta' 114, cheb 5), orb 19
  t=115004 (burden 31, (0,6), eta' 104, cheb 6). Tutte e tre: eta' = K+1..K+13, cioe' il
  detrito PIU' GIOVANE AMMISSIBILE — la scia dell'orbita stessa, appena fuori dalla
  finestra delle K svolte, a 3-6 celle dalla posa. Quando il conteggio scende a 1, cio'
  che separa il caos dall'autostrada non e' detrito antico: e' il proprio passaggio di
  ~un periodo prima.

**Lettura per la chiusura (anello 2):** il fronte del pigeonhole si restringe a una
domanda precisa: puo' un'orbita eterna fare in modo che, OGNI volta che il residuo si
svuota di detrito vecchio, la propria scia recente (eta' ~K, controllata dalle ~2K svolte
recenti = oggetto FINITO) cada nelle celle giuste? Ai tre eventi osservati e' successo.
Ma la scia recente e' funzione della parola (Teorema della Scia §86 + Finestra-K §87):
l'evento "G=1 con colpevole di eta' ~K" e' quindi un vincolo di AUTOCONSISTENZA della
parola stessa — un oggetto finito-dimensionale, attaccabile per enumerazione. §89c:
enumerare le coppie (parola, cella-colpevole-di-scia) compatibili e vedere se il vincolo
e' soddisfacibile all'infinito o si esaurisce (stile checklist §61-66, ma sul lato record).

Inventario: `alpha1/record_guilty_dynamics.py`, `record_guilty_dynamics_summary.json`,
`record_guilty_dynamics.log`.

## 89c. La scia al bordo del pigeonhole: forense + Teorema del Blocco Antico

**Riepilogo in una frase:** il modello di autoconsistenza della scia e' validato 3/3 sui
G=1 reali (la colpevole e' dipinta ESATTAMENTE al passo 0 della parola estesa di
lunghezza K+j, svolta R, mai rivisitata, e la stessa scia non sporca il resto del
residuo), mentre sulla famiglia certificata vale il **TEOREMA DEL BLOCCO ANTICO**: la
colpevole (1,1) e' fuori dal footprint di sigma^m·tau·w101 per OGNI m, quindi ai record
della famiglia la scia recente non puo' MAI salvare il pigeonhole — l'eta' del blocco
richiesto supera 405+8m e diverge con la profondita' del match.

Strumento: `alpha1/record_trail_forensics.py` (+`_summary.json`, `.log`).

**Parte 1 — forense (3/3 verde, con un fix di frame istruttivo).** Per ciascun evento
G=1 di §89b, con a = eta' e j = a-K: la parola estesa w' = svolte(t-a..t-1) e'
realizzabile, footprint in {y>=1}; la colpevole e' visitata SOLO al passo 0 (l'eta' e'
l'ultima visita), con svolta R (dipinge nero), e il germe di w' e' nero su di lei
(colore word-determinato, Finestra-(K+j)):

| orb | t | j | cella | burden | residuo-altri in footprint(w') (bianchi, ok) | assunzioni profonde |
|-----|---|---|-------|--------|----------------------------------------------|---------------------|
| 0 | 55962 | 1 | (-3,3) | 13 | 0/12 | 12 |
| 18 | 2552 | 13 | (-1,5) | 13 | 1/12 | 11 |
| 19 | 115004 | 3 | (0,6) | 31 | 0/30 | 30 |

Nota di frame (per il §5 di chiunque riusi il codice): l'heading di FINE del cammino
virtuale della parola estesa NON e' 0 in generale (dipende dall'heading reale all'inizio
dell'estensione); le posizioni relative vanno ruotate con k=(-h0)%4 come fa
`to_anchor_frame`, altrimenti il check di visita fallisce su 2 eventi su 3.

**Parte 2 — TEOREMA DEL BLOCCO ANTICO (famiglia certificata §88).** residuo = {(1,1)}
implica (1,1) fuori dal footprint; verificato direttamente per m = 0..46 e per OGNI m
via l'induzione onset-lock ((1,1) appartiene a V0, i blocchi nuovi sono disgiunti da V0
per sempre). Enunciato: **se le ultime 405+8m svolte di un'orbita sono
sigma^m·tau·w101, l'orbita non ha visitato (1,1) in quell'arco; per un'eterna
non-highway la colpevole (1,1) deve quindi avere eta' > 405+8m.** Al crescere del match
la pre-semina richiesta diverge: lungo la famiglia certificata il meccanismo che salva
le orbite reali ai G=1 (scia di eta' ~K, §89b) e' STRUTTURALMENTE indisponibile.

**Stato del pigeonhole dopo §89:** due prong misurati/dimostrati e un buco nominato.
(a) Alle orbite reali il bordo G=1 e' salvato dalla scia minima (eta' K+1..K+13) — ma le
parole reali hanno fardello alto e non appartengono a famiglie vive certificate.
(b) Sulla famiglia viva certificata la scia non puo' salvare — ma nessuna orbita reale
la presenta (0/1639). Il buco: le parole a fardello basso VIVE che le orbite eterne
potrebbero presentare ai record senza appartenere alla famiglia. §89d/§90: o si dimostra
che il vincolo di autoconsistenza (a) si esaurisce (enumerazione delle coppie
parola/cella-di-scia con G=1 possibile), o si estende il Blocco Antico dall'unica
famiglia certificata all'intero albero vivo a fardello basso (il corridoio esponenziale
del §88 Test C).

Inventario: `alpha1/record_trail_forensics.py`, `record_trail_forensics_summary.json`,
`record_trail_forensics.log`.
