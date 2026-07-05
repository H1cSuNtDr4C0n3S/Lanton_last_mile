# ADDENDUM §100 — CODA DOPPIA REALIZZATA, GUARIGIONE ALLA V†, LA FASCIA WORD-MEDIATED

**Riepilogo in una frase:** la caccia preregistrata a §99d ha UCCISO anche la candidata
a due orologi — su 25.000 semi di catena disgiunta (verificata), 4 falsificatori
(min_ep>8 E min_age>10P; = 2 episodi indipendenti, verificati 4/4 bit-identici dalla
lente) e coda min_ep fino a 12: il "vuoto" di §99 era piccolo-n al livello giusto
(0/3 episodi vs tasso episodico 20/34 = 0,59, p ~ 7%: compatibile al margine) — terza
morte preregistrata in tre sessioni, e stavolta con la prova che non c'e' NIENTE da
cercare sotto il soffitto deduttivo: i falsificatori realizzano **ep = y_rel con
uguaglianza** (q=0), il bound della Scala e' TIGHT; l'autopsia dei 2 violatori
d'orizzonte §99c mostra la **guarigione alla V†** (2/2: la corsa e' deviata a d=542 e
750 da una colpevole-† NERA reale a y_rel 21/25, oltre l'orizzonte corto; l'unica
profonda rispetta ep<=y_rel: la Scala e' horizon-free perche' deduttiva); e la coda
alta dell'orologio-record e' **word-mediated come REGIME, non come famiglia della
soglia**: 45 testimoni -> 14 parole (vs attese ~42 dal coupon-collector: effetto a
>20 sigma; 3 delle 4 parole cross-catena sono le 3 pesanti) MA la baseline
stratificata mostra la concentrazione gia' a min_ep=4 (297 -> 119 distinte, top
molteplicita' 60) — gradiente 90% -> 42% -> 31% di distinte, il §99b sotto altro
nome. Trappola nuova (qq): le soglie dell'orologio-record sono quantili con data di
scadenza, e min_ep e' un osservabile della coppia (orbita, orizzonte di rilevazione)
— lo stesso record vale G=0 all'orizzonte corto e ep=19 alla V†.

Strumenti: `alpha1/record_minep_hunt.py --chain2` (+`record_minep_hunt_summary2.json`,
`record_minep_hunt2.log`; 25k semi, 220 s), `alpha1/v_dagger_autopsy.py` (+json/log).
Pannello: 2 lenti in sessione (lente 1 VERDE, lente 2 GIALLO con 1 ROSSO riparato).

## 100a. La caccia preregistrata (verdetto: CODA DOPPIA REALIZZATA)

Operazionalizzazione di §99d: catena-2 BASE2 = xs(BASE ^ 0xD1B54A32D192ED03) =
5213087935039776180 (disgiunzione VERIFICATA in-run contro i 5000 semi di catena-1;
riverificata dalla lente), 25.000 semi, falsificatore = record profondo G>=1 con
min_ep > 8 E min_age > 1040, verdetto EMESSO DAL TOOL (elimina gradi di liberta'
alla lettura). Deviazioni dichiarate: (a) soglia di potenza codificata 20 vs "~30
attesi" in §99d — mai attivata (il ramo eseguito e' quello esistenziale); (b) le
modifiche al tool (--chain2, verdetto) sono committate con questo verbale.

Numeri (gate canonici 24/24 bit-identici a §98, ora con istogramma per-record e
zero-G0; 24.997 orbite ok, 3 semi scartati dichiarati, no-onset 0):

- 254.319 record censiti, 36.151 profondi, 34.928 con colpevoli, 1.223 a G=0
  (tutti entro l'orizzonte del germe: ingressi in corso; violazioni-orizzonte
  profonde **0** — vedi sotto);
- min_ep hist: 14938 / 11394 / 6810 / 1514 / 227 / **28 / 10 / 3 / 1 / 1 / 1 / 1**,
  MAX 12 (era 5 a §98 su n=1.174, 8 a §99 su n=6.980: il massimo sale con n,
  senza saturazione — quantile, come previsto);
- **FALSIFICATORI: 4** (rng 7997830615314335065 t=4098/4108, min_ep 11/12, min_age
  3063/3073; rng 18402929353606185973 t=7720/7730, min_ep 9/10, min_age 5040/5050)
  = **2 episodi indipendenti** (coppie di record consecutivi con le stesse colpevoli
  fisiche; la falsificazione esistenziale regge con 1). Verificati 4/4 bit-identici
  su tutti i campi (lente 1, macchinario a passata singola con storia per-cella).
- ep>5 & age>10P: 28/45 record (20/34 episodi). Il confronto con §99 al livello
  giusto: §99 aveva 0/3 EPISODI, p(0/3 | 0,59) ~ 7% — compatibile al margine.
  La versione a livello record (0/6 vs 28/45, p ~ 0,3%) si autoconfuterebbe:
  contare gli episodi, non i record (lezione F4 §99e, ora regola).

**Che cosa muore:** la candidata "ep>8 => age<=10P" e ogni programma "trova la
costante giusta dell'orologio-record". **Che cosa NON muore (e come):**

1. **ep <= y_rel e' TIGHT**: i falsificatori realizzano l'uguaglianza — a t=4108
   la colpevole (-8,-8) ha ep = 12 = y_rel (quota di rientro q = 0, lag 0: cella
   dipinta al record che ha aperto la sua riga, mai riletta per 12 epoche). Non
   esiste spazio per una costante intermedia sotto y_rel: il soffitto deduttivo
   della Scala e' raggiunto in natura. Questo e' l'argomento definitivo contro
   nuove cacce alla costante.
2. Il Teorema del Rifornimento Recente §98c (condizionale A/B/C) — non usava
   nessuna costante misurata.
3. Come TREND (mai costante): la scia quasi-universale, stabile fra catene
   disgiunte (frac min_age<=2K: 91,5% canonici -> 82,0% catena-1 -> 82,7% catena-2).
4. T1-T4 della Scala: zero violazioni anche su ~254k record freschi.

**Tensione a verbale (lente 2):** violazioni-orizzonte profonde 0/1.223 G0 in
catena-2 contro 1/230 in catena-1 (p(0|tasso catena-1) ~ 0,5%) — fortuna, o il
fenomeno e' clusterizzato/word-mediated (i 2 violatori §99c condividono burden 36 e
onset_germe 55). E il tool censisce i G0 solo sui PROFONDI: i record misti di
catena-2 non sono stati riscanditi (il violatore misto di §99c venne dallo script
di lente). L'istogramma min_ep resta un oggetto all'orizzonte V(onset+P), come il
falsificatore preregistrato: coerente, ma da dire.

## 100b. Autopsia dei violatori: la guarigione alla V† (2/2, esistenziale)

`v_dagger_autopsy.py` sui 2 violatori §99c (ri-verifica: residuo corto 36/36
bianco riprodotto): corsa del germe per 2600 passi vs svolte reali da t —

| violatore | d divergenza | cella rel | y_rel | germe/reale | anagrafe reale |
|---|---|---|---|---|---|
| rng 7589057972138690721, t=13356 | 542 | (-11, 21) | 21 | bianco / **NERO** | dipinta, eta' 6698, **ep 19**, lag 4420 |
| rng 17133539851518799906, t=12164 | 750 | (-15, 25) | 25 | bianco / **NERO** | dipinta, eta' 1842, ep 4 (riga sopra il seme) |

Tripwire: d >= orizzonte corto (159) in entrambi (la diagnosi §99c e' esatta:
la deviazione vive in V† \ V); cella fuori footprint, prima lettura del germe == d.
Verificate 2/2 bit-identiche dalla lente (17+16 campi).

Lettura con i caveat della lente: (i) l'autopsia trova la PRIMA cella di
divergenza — il primo guaritore genuino (prima di d ogni lettura fuori-footprint
concorda) — NON il residuo V† completo: min_ep† del record resta indeterminato;
"ep alla V† raggiunge 19 in almeno una colpevole" e' la frase corretta (la coda †
piu' lunga e' ipotesi, non misura); (ii) guarigione ESISTENZIALE su n=2, nessun
tasso; il censimento §98 rifatto alla V† resta da quotare (§100g); (iii) la † del
violatore 2 e' shallow (riga 5, fascia del seme): guarisce il meccanismo G>=1
(ipotesi B di §98c), non estende la contabilita' profonda; (iv) il positivo vero:
l'unica † profonda rispetta ep <= y_rel (19 <= 21, q=2) — **la Scala e'
horizon-free perche' deduttiva**; cambia l'orizzonte, non il soffitto.

## 100c. La fascia word-mediated (promozione NEGATA dalla baseline stratificata)

I 45 testimoni ep>5 di catena-2 usano **14 parole distinte** (31%), con
molteplicita' [18, 7, 6, 2, 2, 2, 1x8]; le 14 collassano a **10 classi modulo
shift <= 20** (le coppie consecutive sono cognate per shift); le 3 parole pesanti
sono ESATTAMENTE 3 delle 4 comuni con la catena-1 (catene disgiunte). Contro il
confondente di taglia (lente 2, quantificato): 45 estrazioni dalla baseline
ordinaria (431 record profondi -> 390 distinte, top molteplicita' 7) darebbero
41,6-42,3 distinte attese e P(molteplicita' max >= 4) <= 7% — osservata 18, su 18
orbite distinte: effetto a >20 sigma, il coupon-collector non spiega nulla.

MA la promozione a "famiglia della coda" e' NEGATA dalla baseline STRATIFICATA
(richiesta dalla lente, eseguita in sessione su catena-1): a min_ep = 4 la
concentrazione c'e' GIA' — 297 record -> 119 distinte (40%), top molteplicita'
**60**; a min_ep = 5: 44 -> 31 (70%); pooled 4-5: 42% distinte. Il quadro vero e'
un GRADIENTE di entropia di parola lungo min_ep (90,5% -> 42% -> 31% di distinte):
la fascia alta dell'orologio-record e' un regime a poche parole (discese
quasi-periodiche, il §99b visto dalle parole), e la "famiglia dei testimoni" e' il
suo estremo, non un oggetto nuovo alla soglia falsificata. Fatto strutturale che
resta (il piu' pulito): le stesse parole pesanti ricorrono FRA CATENE DISGIUNTE —
il regime e' portato da parole specifiche, riproducibili, con burden quantizzati
(23/34/36/31/44/53) e onset_germe 55 ricorrente: la fenomenologia coincide con
quella dei 2 violatori d'orizzonte (burden 36, onset_germe 55) — l'aria e' quella
degli INGRESSI MANCATI (quasi-onset). Da censire come regime, non come famiglia
(§100g).

## 100d. La lezione delle tre morti (§98 -> §99 -> §100)

max min_ep: 5 (n=1.174) -> 8 (n=6.980) -> 12 (n=34.928), senza saturazione; la
coda doppia si e' riempita appena arrivata la potenza (0/3 episodi -> 20/34); e lo
stesso record vale G=0 all'orizzonte corto e ep=19 alla V†. Una "costante giusta"
non puo' esistere per un osservabile la cui definizione dipende dall'orizzonte di
rilevazione. Sopravvivono tre soli tipi di enunciato: **deduttivi** (ep <= y_rel,
TIGHT), **condizionali a ipotesi dichiarate** (§98c A/B/C alla V†), **esistenziali**
(le falsificazioni). Regola operativa da qui in avanti: nessuna nuova soglia
numerica sull'orologio-record fuori da una preregistrazione completa (falsificatore
+ potenza + catena disgiunta + aspettativa di morte); i fronti ammessi sono
strutturali (il regime di parole, la geometria V†), non numerici.

## 100e. Pannello (2 lenti in sessione)

- **Lente 1 (verifica indipendente): VERDE.** 4/4 falsificatori e 2/2 autopsie
  bit-identici (macchinario a passata singola con storia per-cella, cammino di
  divergenza proprio); BASE2 ricalcolato, appartenenze alle catene e disgiunzione
  riverificate; criterio preregistrato riapplicato (esattamente 4, i tre min_ep=8
  correttamente esclusi dal > stretto).
- **Lente 2 (logica): GIALLO, 1 ROSSO riparato.** ROSSO: il confronto col "0/6"
  di §99 andava fatto a livello EPISODI (0/3 vs 20/34, p~7%), non record (p~0,3%,
  autoconfutante) — recepito (§100a). Medi recepiti: episodi dichiarati ovunque;
  ep<=y_rel TIGHT valorizzato; deviazioni di preregistrazione dichiarate; tensione
  0/1.223 vs 1/230 e caveat deep-only a verbale; baseline stratificata ESEGUITA e
  promozione negata (§100c); caveat autopsia (i)-(iv) integrati (§100b);
  formulazione (qq) adottata (§100d/f).

## 100f. Trappole nuove

- **(qq) le soglie dell'orologio-record sono quantili con data di scadenza — e
  min_ep e' un osservabile della coppia (orbita, orizzonte)** (§100d): tre
  costanti-candidate morte in tre sessioni (5, 8+coda-vuota, 12 gia' in scadenza),
  massimi che salgono con n senza saturare, e lo stesso record che vale G=0 a
  V(onset+P) e ep=19 a V†. Ogni costante-candidata sull'orologio-record nasce SOLO
  dentro una preregistrazione (falsificatore, potenza, catena disgiunta) e con
  l'aspettativa di morire; i sopravvissuti ammessi sono deduttivi,
  condizionali-dichiarati o esistenziali. Confrontare i tassi per EPISODI, non per
  record (i record consecutivi condividono le colpevoli). Parente di (i), (h),
  (bb), (nn).

## 100g. Domande aperte / prossimo (§101)

1. **Il regime a poche parole della fascia alta** (§100c): identificare le parole
   pesanti (la top-60 di min_ep=4, le 3 cross-catena), classi modulo shift,
   rapporto con gli ingressi mancati (burden quantizzati, onset_germe 55 come i
   violatori d'orizzonte) e con la porta/A1 (§78): i record ad alto min_ep sono
   tentativi di porta falliti visti dal lato-record? Censimento del regime
   (fascia min_ep>=4), non della coda.
2. **Censimento alla V†**: quotare il costo (eval_word con orizzonte 2600 per
   ~50k record) e decidere se rifare §98; nel frattempo ogni tasso di buchi
   dell'orizzonte corto va dichiarato (2 noti / ~29k + 0 / catena-2 profondi;
   misti di catena-2 MAI riscanditi — debito).
3. Ereditati: geometria dei rientri (§98g.2), scia quasi-universale teorema?
   (§98g.3), separatori §97, fuggenti vs nere-D>=400, retro-nota §91c.3,
   stress-2 bianche, h1=1.

## 100h. Inventario file

- `alpha1/record_minep_hunt.py` (esteso: --chain2, disgiunzione verificata,
  verdetto preregistrato in-tool, parole ripetute) + `record_minep_hunt_summary2.json`,
  `record_minep_hunt2.log`.
- `alpha1/v_dagger_autopsy.py` (+`v_dagger_autopsy_summary.json`, `.log`).
- Scratchpad di sessione: word_repeat_baseline.py, word_family_stratified.py
  (baseline ordinaria e stratificata), lente1_verifica.py, lens2_g100_checks.py.
- `docs/DOUBLE_TAIL_ADDENDUM.md` — questo addendum.
