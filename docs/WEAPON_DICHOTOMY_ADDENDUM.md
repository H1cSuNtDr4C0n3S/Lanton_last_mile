# ADDENDUM §90 — DICOTOMIA, ARMA, MURO DIETRO L'UNO

**Riepilogo in una frase:** la dicotomia §89d e' stata DECISA sul campo: i passati di
w101 che visitano (1,1) esistono (dal prof. 49, mai entro 46: esaustivo), quelli che la
lasciano bianca sono PAROLE-ARMA (burden1 = 0, ingresso incondizionato — 30/30 nel
campione) ma muoiono all'indietro con un muro esatto e uniforme [1x12, 0], quelli che la
lasciano nera muoiono entro 4; ne emerge il TEOREMA-BERSAGLIO "MURO DIETRO L'UNO"
(vietanza di w101 ai record di orbite a storia lunga), gia' coerente con ogni misura
(§89a: zero w101 su 1639 record reali), ridotto a DUE enunciati universali finiti
ancora aperti (§91).

Strumenti: `alpha1/prepend_box_automaton.py`, `record_target_hunt.py`,
`record_cover_census.py`, `record_ancient_block_tree.py --depth 46` (tutti +json +log).

## 90a. L'automa dei prepend a scatola: costruito, validato, NON conclusivo

Sovra-approssimazione: camminatore all'indietro ESATTO dentro una scatola attorno a
(1,1) (requisito a 3 stati per cella: libera / prossima-lettura-bianca / -nera,
alternanza ancorata alle prime letture di w101), LIBERO fuori; y>=1 esatto ovunque;
da fuori si entra solo con successore fuori-scatola ((1,1) ha successori solo nel
colletto: nessun ingresso diretto). Validazione V1 VERDE: il binario reale di 624
prepend (§88) e' ammesso transizione per transizione.

Esito: (1,1) RAGGIUNGIBILE nell'astratto (witness in 5/14 passi-scatola, scatole 15 e
28 celle). Lezione metodologica (gemella della trappola c): in una sovra-approssimazione
si trasferisce SOLO l'irraggiungibilita'; la raggiungibilita' astratta non dimostra
nulla. L'esterno-libero e' troppo generoso per chiudere: il vero automa dei prepend
richiede lo stato di bordo completo (§56-style, con i suoi ostacoli di esplosione).

## 90b. Il corno (b) e' REALE e produce LA PAROLA-ARMA — vacua

La caccia concreta guidata (best-first sulla distanza della coda da (1,1),
`record_target_hunt.py`, 0.1 s) REALIZZA il corno (b): esiste un passato
record-compatibile che visita (1,1), profondita' 57:
`LRLRLRLLRLLLLRLRRLLLLRRLLLLRRLRRLRRRRLLLLRLRRLRRRRLLLLRLL` (+ w101).
Coerenza: lo sweep esaustivo (ora spinto a 46: 5.5M nodi, **zero visite** fino a 46
=> eta'((1,1)) > 147 a ogni record-w101) non poteva vederla (57 > 46).

L'estensione lascia (1,1) BIANCA e il germe rigioca la corsa di w101 identica
(onset 160): footprint cresciuto, residuo VUOTO — **burden1 = 0. LA PAROLA-ARMA
(K = 158) del §87e esiste.** A ogni record y-min con quelle 158 svolte l'ingresso in
autostrada e' INCONDIZIONATO.

MA (trappola (w), verificata subito): il muro sopra l'arma e' `[0]` — **D = 0**, nessun
prepend valido. La prima arma e' la vacuita' in forma pura: coprire la cella del residuo
vieta il passato istantaneamente.

## 90c. Censimento delle coprenti: 30 armi, muri esatti, uniformita'

`record_cover_census.py` (60 estensioni coprenti campionate best-first, prof. 49..129 —
campione NON esaustivo, dichiarato):

- **bianche 30/30 = armi** (burden1 = 0, onset 160): lasciare (1,1) bianca fa rigiocare
  la corsa identica e svuota il residuo — nel campione la coincidenza e' perfetta;
- **nere 30/30 = fardelli enormi** (burden1 69..1976): leggere nero su (1,1) fa
  divergere la corsa del germe subito e il conto esplode;
- vitalita' all'indietro: nere D <= 4; bianche D = 0 (le corte) oppure **D = 12 ESATTO**
  (le profonde): muro esaustivo `[1,1,1,1,1,1,1,1,1,1,1,1,0]` — dodici prepend FORZATI
  (catena unica), poi estinzione totale — IDENTICO per le armi a prof. 77, 105 e 129.
  L'uniformita' del 12 attraverso profondita' diverse indica un meccanismo comune
  (la geometria della copertura costringe la coda): congettura del muro,
  **burden1 = 0 => D <= 12**.

La congettura §88 ("D illimitato => burden1 >= 1") NON e' falsificata: esce RAFFORZATA
nella forma quantitativa sopra. Nessuna arma viva; il livello 1 resta il pavimento vivo
osservato.

## 90d. TEOREMA-BERSAGLIO: il Muro dietro l'Uno (enunciato esatto, 2 lacune)

A un record y-min con suffisso w101, il passato reale dell'orbita e' un'estensione
record-compatibile (automatico ai record stretti). Allora:

1. se il passato NON visita mai (1,1): il nero su (1,1) (obbligato per le eterne, Parola
   Viva §88) viene dal SEME INIZIALE; i record B-T marciano fuori da ogni seme finito
   => ai record tardivi questo corno muore;
2. se il passato visita (1,1) e la lascia BIANCA: la parola estesa e' un'ARMA =>
   ingresso incondizionato => vietato alle eterne; e comunque il passato non si estende
   oltre D <= 12 all'indietro => nessuna orbita con storia > prof.+12 puo' trovarsi qui;
3. se la lascia NERA: il passato muore all'indietro entro D <= 4 => idem.

**Se (2) e (3) valgono UNIVERSALMENTE (oggi: campione 60/60 + 3 muri esaustivi), nessuna
orbita con storia sufficientemente lunga puo' presentare w101 a un record y-min: la
prima parola VIETATA ai record.** Coerenza esterna gia' in atti: §89a, zero occorrenze
di w101 su 1639 record reali.

Le due lacune per §91 (entrambe finite-flavored, su un insieme infinito ma strutturato):
- **U1 (bianche = armi):** ogni coprente che lascia (1,1) bianca ha burden1 = 0.
  Candidato teorema: la corsa del germe di w101 rigioca identica se l'estensione non
  tocca V \ {(1,1)} con colori sbagliati — da dimostrare o delimitare;
- **U2 (morte del coprente):** ogni coprente ha D limitato (misurato: <= 12).
  Candidato: la geometria della copertura (raggiungere (1,1) dentro il colletto B-nero)
  costringe la coda in un vicolo con muro — l'oggetto giusto per l'automa di bordo
  o per un lemma alla HALO (§85).

Se U1+U2 cadono, cade il primo mattone di vietanza; la scala a Link 1 diventa: estendere
la vietanza dalle singole parole a una famiglia INEVITABILE ai record (il conteggio
delle colpevoli §89b scende a 1 solo con scia minima; le parole a scia minima sono
enumerabili). Roadmap §91: U1, U2, poi il censimento delle parole-di-record a scia
minima.

## 90e. Trappole nuove / promemoria

- **(z) la raggiungibilita' astratta non e' un risultato** (gemella di (c), lato
  prepend): un automa sovra-approssimante che dichiara raggiungibile un bersaglio non
  dice nulla sulla realta'; solo l'irraggiungibilita' si trasferisce. Prima di allargare
  scatole/stati, tentare la REALIZZAZIONE concreta guidata (qui: trovata in 0.1 s dove
  lo sweep cieco non arrivava, con bussola = distanza della coda dal bersaglio).
- Il muro D=12 delle armi e' stato accertato con enumerazione esaustiva livello per
  livello e budget freschi DOPO che una bisezione con budget condiviso aveva dato 17
  valori identici (sintomo alla (b): uniformita' sospetta => ricontrollo con metodo
  indipendente; qui l'uniformita' era REALE).

## 90f. Inventario file (alpha1/)

- `prepend_box_automaton.py` (+json, +log) — automa a scatola, V1 verde, witness astratti.
- `record_target_hunt.py` (+json, +log) — caccia guidata: corno (b) realizzato a prof. 57.
- `record_cover_census.py` (+json, +log) — 60 coprenti: 30 armi bianche, 30 nere, muri.
- `record_ancient_block_tree.py` — sweep esteso a prof. 46 (5.5M nodi, zero visite,
  eta' > 147); summary aggiornato, log `record_ancient_block_tree46.log`.
