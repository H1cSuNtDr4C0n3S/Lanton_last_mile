# Rotor-Stall Geometry Addendum (§77)

Riepilogo in una frase: gli stalli del morso (run di non-scoperta) non sono ne' corridoi 1D ne'
rotori puntiformi ma macchie area-filling a molteplicita' limitata (~1.57 passi/cella, bbox~len^0.77)
su detrito invecchiato, cioe' la firma di un rotor-router walk; ma il rotore e' NON abeliano in modo
netto (test §77.6: stessa config, escape 303/1109/1/1135 per heading) e la prova di viabilita'
(§77.7) tira CONTRO la strada — i bite-stalli sono LIMITATI ~303 fino a T~1e5 (quantita' diversa
dallo stallo crescente di #30) e l'esponente di fuga deriva verso il bound abeliano invece di
restarci sotto, quindi rotor-router-per-il-morso e' la mossa sbagliata: la quantita' che bounderebbe
e' gia' limitata, e tutto resta livello morso, non α1/Link 1.

## 77.1 Obiettivo e correzione di rotta

Spunto di Michael: usare il lavoro su Z (identita' `Z(t)=t-N(t)+1`, N=celle distinte) come feature
verso α1. Poiche' `dZ/dt = 1 - dN/dt` e `dN/dt = 1` esattamente quando la formica morde (legge
cella fresca), Z e il processo binario del morso `b(t)` sono la stessa informazione. La domanda
naturale e' sugli STALLI del morso: run massimali di `b=0` (non-scoperta).

Correzione Faraday-Maxwell, prima di calcolare. "Stalli limitati" si spacca in due:
- **stalli FINITI**: gratis. Bunimovich-Troubetzkoy da' illimitatezza (`N(t)->∞`), quindi infiniti
  morsi, quindi nessuna run di `b=0` infinita. Nessun stallo eterno, senza fatica.
- **stalli UNIFORMEMENTE limitati** (= pavimento del morso, modo DC #24): FALSIFICATO (#30, gli
  stalli crescono ~lineari fino a T~3·10⁵). Roadmap §C-1 lo aveva gia' declassato.

Quindi la domanda combinatoria utile NON e' "sono limitati" (risposta: no) ma **gli stalli sono
LOCALI o NON-LOCALI?** Uno stallo locale (rotore su detrito recente, regione piccola) e' uccidibile
da un automa a finestra finita; uno non-locale (vagabondaggio su detrito antico) no. Questo decide
se Z alimenta un lever o no. La diagnosi non risultava fatta nel repo (§58 misura il tasso
non-locale, non la composizione spaziale degli stalli).

## 77.2 Geometria degli stalli (misurata)

Orbita-record `(7,-7)`, fase caotica fino a onset 106258 (`entry_seed/stall_geometry.py`,
`stall_geometry.json`):

```text
Z slope (caos)      = 0.7953        (coerente con identita' e #23)
bite rate (caos)    = 0.2047
n stalli            = 9824          len max 303, mediana 7
bbox ~ len^0.767    (R2 0.924)      [0.5 = area-filling 2D, 1.0 = corridoio 1D]
molteplicita' len/celle: mediana 1.571, q90 1.625   (passi per cella distinta nel patch)
stallo piu' lungo: len=303, celle distinte=149, bbox=20, eta' max cella letta=3756
```

Lettura: gli stalli **non sono corridoi** (esponente 0.77, non 1.0) e **non sono rotori
puntiformi** (molteplicita' solo ~1.6, non alta). Sono macchie compatte, lievemente frastagliate,
area-filling, che la formica spazza ~1.6 volte per cella, su celle scritte migliaia di passi prima
(ritorno su detrito invecchiato). Footprint dello stallo piu' lungo in `entry_seed/stall_footprint.png`:
blob connesso, hotspot di rivisita radi.

## 77.3 Identificazione: la formica e' un rotor-router walk

La firma "area-filling a molteplicita' limitata su sfondo statico" e' quella di un rotor-router
walk, e non per analogia. Durante uno stallo (e in realta' sempre) **ogni cella e' un rotore a 2
stati**: il colore fa toggle bianco↔nero a visite successive, quindi la svolta alla cella alterna
R,L,R,L,... a ogni visita, deterministicamente, indipendentemente dall'heading d'arrivo. La formica
e' un cammino a rotori che riempie il patch del proprio detrito.

Questo apre la famiglia dei **teoremi di fuga/range dei rotor-router** (Holroyd-Propp; Levine-Peres):
per il rotor walk su Z² esistono limiti inferiori sul numero di siti distinti visitati in n passi
(range), che e' esattamente `N(t)` — cioe' il pavimento del morso, ma per via teorica, non per
simulazione. E' la prima volta che Z indica un lever con teoremi veri dietro, invece di un
potenziale ad hoc (§67-§69 falsificati) o un automa che esplode.

## 77.4 L'ostruzione non-abeliana (caveat duro)

La formica NON e' il rotor-router abeliano standard. Nel modello abeliano la direzione d'uscita
dipende solo dallo stato del rotore (indipendente dall'arrivo); per la formica l'uscita assoluta e'
`heading_in ± 1`, quindi dipende anche dall'heading d'ingresso. Conseguenza: i bound di fuga
abeliani e la proprieta' abeliana (che danno i teoremi forti) NON si trasferiscono diretti. Serve la
variante non-abeliana, e quella parte di letteratura e' molto piu' magra. La firma R,L,R,L per cella
e' invariante all'heading, ma la GEOMETRIA del cammino no — ed e' la geometria che entra nei bound
di range.

## 77.5 Limite logico (cosa NON dice)

Distinzione che va tenuta ferma: questo addendum analizza gli **stalli del MORSO** (run di `b=0`),
che sono il livello #24/#30 — DECLASSATO come pavimento. Lo "stallo" di **α1** e' un'altra cosa: il
fallimento ETERNO di ingresso in autostrada (≈ Link 1), enunciato grossolano-temporale, non
locale-in-tempo. E l'α1 della riduzione `α1∧β∧γ` e' il tasso di lettura nera FUORI-FINESTRA `δ_r`
(§58, che NON erode, mediana 0.2334), non il tasso di morso (che erode). Quindi:
- il morso che erode (assunto da #24/#30) NON e' verificato su questa orbita: su `(7,-7)` il bite
  rate e' 0.20 (sano) e i bite-stalli sono LIMITATI ~303, invarianti da T~1e4 a 1e5 (vedi §77.7).
  Quindi il "bite-stall" qui misurato e' una quantita' DIVERSA dallo stallo crescente di #30 (che
  raggiunge ~1e4): #30 misura probabilmente i buchi tra letture nere fuori-finestra, o usa orbite a
  patch random / T molto piu' grandi. Da riconciliare prima di chiamarlo "il declassato".
- valore di §77: caratterizza la TESSITURA del caos, e il framing rotor-router potrebbe dare un
  limite inferiore SUBLINEARE su `N(t)` (es. `N(t) >= C·t^{2/3}` stile range rotor-router), che
  settlerebbe RIGOROSAMENTE se il tasso di morso ->0 e' strutturale (probabile) invece che
  empirico — confermando la declassificazione invece di assumerla;
- §77 NON e' una via per α1/Link 1, che resta il crux separato (priorita' §78, eredita la §76
  originaria: A1 con T3' deterministico / propagare unknown).

Inoltre, conferma una chiusura: il patch cresce con la lunghezza dello stallo (bbox~len^0.77) e gli
stalli crescono con T (#30), quindi **nessun raggio d'automa fisso contiene tutti gli stalli in
eterno** — l'automa a finestra a raggio fisso non puo' da solo limitare gli stalli. Coerente con il
fatto che il toolkit a finestra non morde da solo su α1.

## 77.6 Test di abelianita' (ESEGUITO) — esito: non-abeliano netto

Test (`entry_seed/abelian_test.py`, `abelian_test.json`): congelati colori + celle-visitate
all'inizio dello stallo piu' lungo (`t=4680`, len 303, entry `(20,6)`, patch 705 celle visitate),
rilanciata la formica dalla stessa cella con i 4 heading; escape = primo passo su cella fresca.

```text
heading 0 (reale): escape dopo  303 passi, exit (2,9)   [riproduce lo stallo reale]
heading 1:         escape dopo 1109 passi, exit (20,-7)
heading 2:         escape dopo    1 passo,  exit (21,6)
heading 3:         escape dopo 1135 passi, exit (17,12)
```

Verdetto: **NON abeliano, in modo netto.** Sulla stessa configurazione di rotori (colori) il tempo
di permanenza varia di ~3 ordini di grandezza (1 -> 1135) e l'uscita cambia con l'heading. La
config dei rotori da sola NON determina la dinamica: l'heading e' essenziale e dominante. I teoremi
di fuga/range ABELIANI non si agganciano — l'ostruzione di §77.4 non e' marginale, e' il primo
ordine.

Rovescio (geometria favorevole). Lo scaling lunghezza-vs-area degli stalli e':

```text
L ~ area_patch^0.785  (R2 0.955),  molteplicita' L/area = 1.57
bound rotor-router (abeliano):  n <= C·area^1.5
```

cioe' la formica fugge dai patch MOLTO piu' in fretta di quanto il caso peggiore abeliano
permetterebbe (esponente 0.785 << 1.5, ogni cella visitata ~1.6 volte). Quindi la geometria
sarebbe favorevolissima a un bound: **manca il teorema, non la struttura.** Il blocco e' la regola
di rotazione heading-dipendente, non un patch sfavorevole.

Conseguenza per il programma: la via "pavimento del morso via rotor-router" e' aperta SOLO se esiste
(o si sviluppa) un bound di range per rotor-walk NON abeliani con rotazione heading-relativa — una
domanda di letteratura matematica, non di simulazione. Se quel bound desse `N(t) >= C·t^{2/3}`,
confermerebbe `N(t)` sublineare (tasso di morso ->0 strutturale). Resta livello morso (declassato),
non α1. Il crux α1/Link 1 resta la priorita' §78 (A1 con T3' deterministico / propagare unknown).

## 77.7 Prova di viabilita' della strada non-abeliana (ESEGUITA) — esito: tira contro

Domanda decisiva, taglia-sessione: l'esponente `gamma` in `L ~ area_patch^gamma` (L = lunghezza
bite-stallo, area = celle distinte) e' stabile SOTTO il bound abeliano 1.5 attraverso orbite e
scale, o deriva? (`entry_seed/escape_scaling.py`, `escape_scaling.json`.)

```text
cross-orbit gamma_global: (7,-7)=0.785  (0,-14)=0.952  (10,-10)=1.121  (11,8)=1.122
  [N.B. piu' l'orbita e' lunga, piu' gamma_global e' basso: artefatto del range-x campionato]
curvatura (7,-7), fit quadratico log L vs log area (coeff quad +0.209 > 0):
  esponente LOCALE: area 15 -> 0.81 ;  30 -> 1.10 ;  60 -> 1.39 ;  120 -> 1.68
sparsita': stalli per area [10,20)=74 [20,40)=952 [40,80)=12 [80,160)=10 [>=160]=0
bite-stall MAX = 303 su TUTTE le orbite (anche griglia-vuota-equiv, onset 9977; e (7,-7), onset 106k)
```

Tre letture, tutte contro la strada come bet immediato:
1. **Esponente non scala-stabile**: cresce con l'area (0.81 -> 1.68) e attraversa il bound abeliano
   1.5 verso area ~100 — l'opposto di cio' che serve a un bound di fuga (la formica indugia di PIU'
   per patch alle scale grandi, non di meno).
2. **Non de-riscabile a buon mercato**: sopra area 40 i punti sono ~22; la coda grande e' troppo
   rara a T~1e5, e andare oltre riporta il muro del finito. La premessa geometrica non si puo'
   testare pulita alle scale accessibili.
3. **La quantita' giusta non e' il morso**: il bite-stall e' LIMITATO ~303 (non cresce 1e4->1e5),
   quindi un bound rotor-router lo "aggiusterebbe" dove non serve. La quantita' che davvero cresce
   (#30, ~1e4) e' un altro osservabile (probabile: buchi nero-fuori-finestra), che il framing
   morso/rotore non tocca. La salita di gamma e' solo curvatura vicino al massimo limitato, non
   lingering illimitato.

Caveat all'onesta': il cross-orbit e' debole (diverse orbite cella-singola lontana riducono alla
griglia vuota, perche' la cella e' raggiunta solo dopo l'onset); il superamento di 1.5 e' estrapolato
da pochi stalli grandi. Ma la direzione e' netta, e somma al mismatch di livello di §77.5. Decisione:
NON fare della strada non-abeliana la priorita' immediata; tornare al crux δ_r/Link 1 (§78).

## 77.8 Inventario file

- `docs/ROTOR_STALL_ADDENDUM.md` — questo addendum (§77).
- `entry_seed/stall_geometry.py` — analisi geometria stalli su `(7,-7)`; fit scaling + molteplicita'.
- `entry_seed/stall_geometry.json` — numeri certificati (bbox~len^0.767, molt. 1.571, stallo max 303).
- `entry_seed/stall_footprint.png` — footprint dello stallo piu' lungo (blob area-filling).
- `entry_seed/abelian_test.py` (+ `abelian_test.json`) — test §77.6: 4 heading su patch congelato,
  esito non-abeliano netto (escape 303/1109/1/1135), scaling L~area^0.785.
- `entry_seed/escape_scaling.py` (+ `escape_scaling.json`) — prova di viabilita' §77.7: esponente di
  fuga deriva su (0.81->1.68, attraversa 1.5 ~area 100), bite-stall limitato ~303, tira contro.
- Dipende da `entry_seed/clib.py` (motore C, vuota->9977, (7,-7)->106258).
