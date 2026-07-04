# ADDENDUM §91 — U1 DIMOSTRATO (Rigioco Bianco), U2 RIDOTTO AL NERO

**Riepilogo in una frase:** U1 e' un TEOREMA (corollario di Replay-Lock §87a + residuo
certificato §88; verifica meccanica G1-G4 verde, attacco con 1859 armi fresche fallito)
e questo CHIUDE incondizionatamente il ramo bianco del Muro dietro l'Uno per le orbite
eterne; la lacuna residua si riduce a **U2-NERO** — "ogni coprente che lascia (1,1)
nera muore all'indietro entro D <= 4" — su una tasca geometrica misurata di poche celle
in due righe (certificato finito alla-HALO progettato, §92).

Strumenti: `alpha1/u1_replay_theorem.py`, `alpha1/u2_cover_rail_map.py` (+json +log).

## 91a. TEOREMA DEL RIGIOCO BIANCO (U1)

**Enunciato.** Sia w101 la Parola Viva (§88: burden1 = 1, residuo = {(1,1)},
certificato). Ogni estensione all'indietro realizzabile e record-compatibile di w101
la cui ULTIMA visita a (1,1) la lascia BIANCA produce una parola con burden1 = 0 e
onset 160: una PAROLA-ARMA.

**Dimostrazione (versione V†, riparata — vedi nota sul pannello).**
1. Il verdetto di rilevazione `onset_verified` e la V della corsa sono funzione delle
   SVOLTE fino all'orizzonte di rilevazione T = 2600; per Replay-Lock §87a le svolte
   fino a T dipendono solo dai colori iniziali di **V† = prime letture della corsa
   entro T** (576 celle — non solo le 81 di V = letture entro onset+P).
2. residuo(w101) = {(1,1)} (certificato §88) e, CHECK NUOVO G1b:
   **V† ∩ {y>=1} ⊆ F ∪ {(1,1)}** — oltre l'onset la corsa legge solo celle a y<=0
   fuori dal footprint (verificato: zero celle extra).
3. Ogni estensione record-compatibile ha footprint in {y>=1}: le sue celle nuove
   intersecano V† al piu' in {(1,1)} (le celle a y<=0 sono intoccabili da qualsiasi
   passato di record stretto).
4. Sulle celle di F i colori finali del germe esteso coincidono con quelli del germe di
   w101: le visite dell'estensione sono tutte piu' antiche della finestra, e le ultime
   scritture su F appartengono alla finestra w101, identica per ogni estensione.
5. Se l'ultima visita a (1,1) la lascia bianca (= il colore vergine che la corsa legge
   li'), il germe esteso ristretto a V† e' identico al germe di w101: svolte identiche
   fino a T, stesso verdetto di rilevazione (onset 160), stessa V.
6. residuo(esteso) = (V \ F') ∩ {y>=1} con F' ⊇ F ∪ {(1,1)}: vuoto per il punto 2. QED.

**Nota metodologica (il buco trovato dal pannello di scettici).** La prima stesura
usava V (81 celle, orizzonte onset+P = 264) al posto di V†: non-sequitur d'orizzonte,
dimostrato dallo scettico con un controesempio di logica (nero a (-3,-6), prima lettura
a t=277: onset rilevato 314, V diversa). Il controesempio vive a y = -6, quindi NON e'
record-compatibile: rompeva la dimostrazione, non il teorema. La riparazione (V† al
posto di V) richiede il check G1b, che passa con zero celle extra. Lezione: negli
argomenti di replay l'orizzonte giusto e' quello della RILEVAZIONE, non dell'evento.

**Verifica meccanica e attacco (`u1_replay_theorem.py`, tutto verde):**
G1 ricalcolo indipendente del residuo e dell'inclusione su V (|V| = 81, onset 160);
G1b inclusione su V† (576 prime letture fino a T=2600): zero celle extra;
G2 punto 4 su 60/60 estensioni del censimento §90c (colori su F bit-identici);
G3 30/30 coprenti-bianche: onset e INTERA V identici, residuo vuoto;
G4 attacco con caccia a restart rumorosi: **1859 coprenti-bianche fresche** (3718
coprenti totali) — zero controesempi.

**Corollario (ramo bianco chiuso per le eterne).** A un record y-min STRETTO (heading
su, semipiano davanti e riga 0 mai visitati: le condizioni del Cono §87) il cui passato
lascia (1,1) bianca, le ultime 101+j svolte sono una parola-arma: per Cono +
Finestra-K + Replay-Lock l'ingresso in autostrada segue incondizionatamente. Nessuna
orbita eterna non-highway puo' trovarsi in questo ramo — SENZA bisogno di alcun bound
sulla vitalita' dell'arma. (Il muro D = 12 delle armi profonde — D = 0 per le corte —
resta un fatto strutturale notevole, non piu' un anello della catena.)

## 91b. U2 ridotto al NERO, e la geometria della tasca

Il Muro dietro l'Uno (§90d) per le orbite ETERNE ora richiede solo:

- corno 1 (mai coprire): nero su (1,1) dal seme iniziale; i record B-T marciano fuori
  da ogni seme finito — chiuso ai record tardivi;
- corno 2 (coprire bianco): CHIUSO da U1 (sopra);
- corno 3 (coprire nero): serve **U2-NERO**: ogni coprente che lascia (1,1) nera muore
  all'indietro entro D limitato. Misurato (`u2_cover_rail_map.py`, 60 muri esaustivi):
  nere D <= 4 (muri `[0]` o `[1,1,1,1,0]`), bianche D <= 12 (muro `[1x12,0]` esatto e
  identico a prof. 77/105/129 — non piu' necessario ma confermato).

Geometria della tasca (l'ingrediente per il certificato finito): le continuazioni
forzate dopo la copertura vivono in **15 celle totali su due sole righe** (y assolute
{1,2}; bbox relativo a (1,1): x in [-6,2], y in [0,1]) e muoiono per `y<1` o
irrealizzabilita'. Il coprente e' schiacciato tra il muro dei record (y >= 1) e il
footprint denso di w101: un vicolo, non un territorio.

**Progetto del certificato (§92):** analisi esatta-in-striscia con requisiti a 2-3
stati per cella (parita' di visita sui footprint, libera/fissata sulle altre),
partenza = tutte le configurazioni di copertura-nera ammissibili, semantica
"uscita dalla striscia = sopravvivenza" (sovra-approssimazione nella direzione GIUSTA:
se anche il camminatore rilassato muore sempre, il reale muore sempre — il duale sano
della trappola (z)). La striscia misurata e' cosi' piccola che lo spazio degli stati
raggiungibili dovrebbe restare trattabile; in caso contrario, restringersi alle sole
coperture nere (bbox [0,2]x[0,1]) prima di allargare.

## 91c. Stato della scala a Link 1 (aggiornato, con le correzioni del pannello)

1. ~~U1~~ DIMOSTRATO (versione V†).
2. U2-NERO: aperto, finito-flavored, tasca minuscola (§92).
3. Con U2-NERO il TEOREMA DEL MURO si chiude nella forma CORRETTA (il pannello ha
   smontato la versione "storia lunga"): **per un'orbita ETERNA non-highway, a ogni
   record y-min STRETTO con posa fuori da un intorno finito dell'origine/seme
   (Cheb ~<= 13 + bbox del seme), presentare w101 e' impossibile.** Incollaggio dei
   corni: (1) mai coprire ⇒ il nero su (1,1) viene dal seme ⇒ solo record vicini al
   seme; (2) coprire-bianco ⇒ arma ⇒ ingresso (U1): vietato alle eterne ovunque;
   (3) coprire-nero ⇒ per U2-NERO la storia si estende al piu' D <= 4 oltre la
   coprente ⇒ la visita a (1,1) avviene nei primi <= 4 passi di VITA dell'orbita ⇒
   la cella (1,1) del record giace a Cheb <= ~5 dall'origine ⇒ solo record vicini
   all'origine. B-T da' infiniti record fuori da ogni intorno finito ⇒ vietanza ai
   record lontani. NB: le orbite CONVERGENTI possono presentare w101 (e' l'ingresso
   forzato, non una violazione); "storia lunga" da sola NON basta — l'ipotesi giusta
   e' spaziale. Coerenza esterna: §89a, 0/1639 nei record reali.
4. Poi: dalla vietanza di una parola alla vietanza di una famiglia INEVITABILE ai
   record (le parole a scia minima di §89b, dove il conteggio delle colpevoli tocca 1).

**RETRO-NOTA (§94, chiude il debito §93h.4):** l'incollaggio del corno 3 al punto 3
("U2-NERO ⇒ D ≤ 4 ⇒ Cheb ≤ ~5") e' MORTO a §92 (D=∞ certificato, trappola aa/bb).
Dopo §93-§94 il corno 3 e' SPEZZATO e riformulato cosi':
(3a) coprente-nera ad albero dei prepend FINITO ⇒ LEMMA DELLA NASCITA VICINA (§93c):
     origine E una cella nera di seme entro r_seed dal record — censimento §94:
     273.459/273.493 parole della famiglia certificate, r_seed ≤ 63, zero alberi
     esauriti con min-pend = 0 ⇒ l'intorno del Muro cresce da "~5" a r_seed+bbox;
(3b) coprente-nera FUGGENTE (34 note) ⇒ APERTO. Il pavimento pend₂ ≥ 2 di §93d e'
     stato FALSIFICATO a §94 (pend₂=0 raggiungibile con posa in palla); il bersaglio
     vivo e' il LEDGER SPORCO v2 (posa di nascita fuori palla-2 ⇒ pend₂ ≥ 1, mai
     violato su ~160M+1,29G nodi) oppure la chiusura per vitalita' (i nodi puliti
     hanno sottoalberi all'indietro 17-71 nodi ⇒ Nascita Vicina su quei rami).
     Dettagli: docs/U2_FAR_ADDENDUM.md §93, docs/U2_FAR_PANEL_ADDENDUM.md §94.

## 91d. Inventario file (alpha1/)

- `u1_replay_theorem.py` (+`_summary.json`, `.log`) — teorema U1: ingredienti G1-G4 e
  attacco (1859 armi fresche, 0 controesempi).
- `u2_cover_rail_map.py` (+`_summary.json`, `.log`) — geometria della tasca: 60 muri
  esaustivi con celle, cause di morte, bbox.
