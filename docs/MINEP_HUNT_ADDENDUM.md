# ADDENDUM §99 — LA CACCIA PREREGISTRATA: min_ep<=5 FALSIFICATO, l'ORIZZONTE REALIZZATO

**Riepilogo in una frase:** la caccia preregistrata a §98g.1 (falsificatore di
"min_ep <= 5" su orbite NON selezionate per onset) ha funzionato al primo colpo — su
5000 semi freschi (catena xorshift dichiarata, onset med 3.964 vs 250-313k dei
canonici) il massimo sale a **min_ep = 8** (6 testimoni su 6.980 record profondi con
colpevoli, 0,086%, verificati BIT-IDENTICI da lente indipendente): il "5" era un
quantile del campione §98, non struttura (trappola h beccata dalla caccia costruita
apposta; nessun teorema di §98 ne dipendeva); la coda e' fatta di record in discese
rapide (l'orologio-record corre nei tratti quasi-periodici) e il pannello ha ucciso la
lettura "firma-W0" con la baseline (frammento >=34 nel 23-29% dei record ordinari);
FATTO NUOVO trovato dalla lente 2 dentro un buco della mia pipeline (230 record G=0
scartati in silenzio, trappola nuova pp): **2 violazioni REALI del tripwire-orizzonte
§89a su 29.084 record freschi** — residuo tutto bianco con onset a 2.372 e 14.757
passi di distanza (>> onset_germe+P) — la PRIMA REALIZZAZIONE del caveat
V(onset+P) != V† di §98c: il meccanismo G>=1 per le eterne DEVE usare V†, e
l'1620/1620 di §89a era fortuna del campione canonico. Resta in piedi: il bound
deduttivo ep <= y_rel (Scala §98b), la falsificazione, e una candidata "coda doppia
vuota" (ep>5 => age<=10P, 6/6) dichiarata POST-HOC e preregistrata per §100.

Strumento: `alpha1/record_minep_hunt.py` (+`_summary.json`, `.log`; 5000 semi, 8
worker, 60 s; gate canonici 24/24 bit-identici a §98 su 6 campi + istogramma
per-record min_ep + zero G=0). Pannello: 2 lenti in sessione (§99e).

## 99a. La caccia (design preregistrato a §98g.1) e i numeri

Semi freschi riproducibili: s0 = xs(xs(BASE)), s_{i+1} = xs(xs(s_i ^ GOLD)),
BASE=0x9E3779B97F4A7C15, GOLD=0xBF58476D1CE4E5B9, build_seed(s, 5, 25) (stessa
famiglia dei canonici: quadrati lato 5-25, densita' 0,25-0,60 — dichiarato: UNA
famiglia di semi, non "tutte le configurazioni"). Pipeline §98 identica (K=101,
record y-min stretti, censiti t<t_on / y<y_seed_min / t>=101, profondo =
ry+k_max(residuo) < y_seed_min), stessi tripwire di scala (T1/T2/T4 per-cella + T3
terra + scala consecutiva). Nessun filtro d'onset: no-onset entro cap 1,5M = 0/5000,
semi vuoti/sopra-origine = 0/5000 (filtri dichiarati e vacui in fatto).

| | canonici §98 | freschi §99 |
|---|---|---|
| orbite | 24 (onset 250-313k, SELEZIONATE) | 5.000 (onset med 3.964, range 188-69.366) |
| record censiti | 1.639 | 50.702 |
| profondi | 1.174 (G=0: 0) | 7.210 (G=0: 230 — §99c) |
| min_ep hist | 566/397/182/26/3, max 5 | 2965/2259/1409/297/44/**3/2/1**, max **8** |
| ha-giovane <=2K | 91,5% | 82,0% |
| min_lag med / <=P | 0 / 88,2% | 0 / 90,1% |

**Verdetto:** "min_ep <= 5" FALSIFICATO — era un quantile (6/6980 = 0,086% sopra 5;
compatibile con 0/1174 di §98, p ~ 36%: nessuna tensione, solo campione piu' largo e
non selezionato). Caveat di lettura (lente 2): la falsificazione (esistenziale) e'
immune al bias di composizione, ma l'ISTOGRAMMA no — i record profondi sono
meccanicamente onset-tilted (onset med pesato-per-profondo 14.441 = 3,6x la mediana
delle orbite; le orbite a onset <= 1000 sono il 12,7% delle orbite ma lo 0,8% dei
profondi). Non promuovere "max 8" a struttura: e' il quantile del prossimo campione.

## 99b. Autopsia dei 6 testimoni, e la firma-W0 uccisa dalla baseline

I 6 testimoni (4 orbite; verificati 6/6 bit-identici su 10 campi dalla lente 1 con
macchinario indipendente — log-eventi per cella in unica passata, niente replay):
coppie di record consecutivi con le STESSE colpevoli fisiche (es. {(18,-17),(19,-18),
(19,-17)} a ep 7 poi 8), eta' in passi 341-901 (nessuna antica), G in {1,2,3},
burden 23/34, dt locali 6-70. Il meccanismo e' definitorio, non causale: min_ep>5 con
min_age<=901 FORZA >=6 record in <=901 passi — la coda vive nei tratti di discesa
rapida, dove l'orologio-record corre rispetto all'orologio-passi.

**La lettura "firma quasi-W0" e' MORTA in sessione** (metodo §84: baseline nulla
obbligatoria): tutti e 6 condividono max-frammento-W0 = 34/101, MA la baseline sui
record profondi ordinari da' frammento >=34 nel 28,8% (300 semi, med 28, max 78) e la
lente 2, sull'intero campione: 23,1% fra i min_ep<=5, gradiente gia' presente sotto
soglia (16% -> 48% per min_ep 1 -> 4), e mediana ESATTAMENTE 34 fra i record
onset-prossimali (4/6 testimoni lo sono). Il 34 condiviso e' composizione, non firma.
Fatti sani che restano per §100: (a) il GRADIENTE frammento-vs-min_ep su migliaia di
record; (b) una parola IDENTICA compare in 3 testimoni di 3 orbite diverse — la coda
sembra word-mediated: predizione falsificabile (parole ripetute fra i nuovi testimoni
su catena disgiunta); (c) una coppia di testimoni e' LONTANA dall'onset (t_on-t ~31k):
la coda non e' solo onset-prossimale (n=1 orbita).

## 99c. FATTO NUOVO: le violazioni dell'orizzonte (caveat §98c.2 realizzato)

La mia pipeline scartava in silenzio i record profondi a G=0 (230/7210) — trappola
nuova (pp): il caso degenere escluso dal denominatore ERA il segnale. La lente 2 ha
rifatto il tripwire §89a (G>=1 se t_on-t > onset_germe+P) su TUTTI i 29.084 record
censiti lontani dall'onset: **2 VIOLAZIONI REALI** —

- rngstate 7589057972138690721, t=13.356 (profondo): burden 36, residuo V(onset+P)
  tutto bianco, onset_germe+P = 159, eppure t_on - t = **2.372**;
- rngstate 17133539851518799906, t=12.164 (misto): burden 36, idem, t_on - t = **14.757**.

Lettura esatta: se il residuo a orizzonte V(onset+P) e' tutto bianco, la corsa
rigioca il germe SOLO fino a dove il germe legge celle di V(onset+P); la prima
lettura oltre (le celle di V† \ V) puo' deviarla — e qui l'ha deviata, per 14.757
passi. E' la prima realizzazione del caveat 2 di §98c (lezione V† §91): il
**meccanismo G>=1 per le eterne e' sano SOLO alla V†**; il tripwire 1620/1620 di
§89a e i 1174/1174 di §98 erano anche fortuna del campione (tasso reale di buchi
dell'orizzonte corto: ~7·10⁻⁵ sul campione fresco). Gli altri 228/230 G=0 sono
fisiologici (entro onset_germe+P dall'onset: l'orbita sta entrando e il residuo
bianco e' l'ingresso stesso; margine mediano -104).

Conseguenze: (i) nessun enunciato di §98 cade — 98c esigeva gia' V† come ipotesi
(B); (ii) ogni FUTURO censimento di colpevoli deve o usare V† o dichiarare il tasso
di buchi; (iii) i 2 violatori sono i primi oggetti concreti per misurare la geometria
di V† \ V (dove vive la cella che salva la corsa?).

## 99d. Che cosa resta in piedi (stato dell'invariante di rifornimento)

- **Deduttivo (intatto):** Lemma della Scala §98b (T1-T4 ancora zero violazioni su
  ~195k colpevoli profonde fresche), bound ep <= y_rel <= k_max(w), identita'
  q = y_rel - ep, Teorema del Rifornimento Recente §98c nella forma condizionale
  (A/B/C) — che non usava il "5".
- **Falsificato:** l'upgrade "finestra costante 5" (§98g.1). L'evento inevitabile
  resta a finestra k* (esistenziale), non costante.
- **Osservazione post-hoc, NON promossa:** la coda doppia e' vuota — tutti i 6
  testimoni ep>5 hanno min_age <= 10P (2 sopra 5P), cioe' 0/6980 record con
  rifornimento vecchio in ENTRAMBI gli orologi. Soglie scelte dopo i dati (5P non
  funzionava: 2/6 sopra) e potenza nulla (0/6 si otterrebbe per caso ~18% anche con
  P(age>10P|ep>5)=25%). **PREREGISTRAZIONE per §100** (fissata ORA, trappola bb —
  un gate deve poter fallire): falsificatore = record profondo con G>=1, min_ep > 8
  E min_age > 10P = 1040; catena semi DISGIUNTA (BASE' = xs(BASE ^ 0xD1B54A32D192ED03),
  stessa ricorsione); >= 25.000 semi (attesi ~30 testimoni ep>5 al tasso osservato:
  se la coda doppia resta vuota LI', diventa candidata-struttura; se non arrivano
  ~30 testimoni ep>5, il test e' sottopotenziato e va dichiarato tale).

## 99e. Pannello (2 lenti in sessione)

- **Lente 1 (verifica testimoni, indipendente): VERDE.** 6/6 testimoni bit-identici
  su 10 campi (incluse le celle guilty con ep/age/lag), 4/4 orbite, t_on ricalcolati
  identici; tripwire di coerenza sui record adiacenti ai testimoni: 8/8 (o non-profondi
  o min_ep in {4,5} — il bordo del burst e' visibile anche nei vicini).
- **Lente 2 (logica + replica strumentata dell'intera catena): GIALLO, 2 ROSSI
  riparati in sessione.** (R1) firma-W0 = pattern-matching post-hoc su n effettivo
  3-4: uccisa con baseline propria (§99b) — recepito, F2 degradata a gradiente +
  parola-ripetuta; (R2) 230 G=0 scartati in silenzio + tripwire §89a droppato:
  riparato nel tool (G=0 censiti con flag oltre-orizzonte, gate rafforzato con
  istogramma per-record min_ep — le somme non bastavano — e T3 aggiunto), fatto
  nuovo a verbale (§99c). Gialli recepiti: istogramma non promuovibile (composizione
  onset-tilted 3,6x), coda doppia solo-preregistrata, F4 corretta (4/6 testimoni a
  G<=2, 3 episodi indipendenti, tutti onset-prossimali: al bordo G basso la scia
  giovane e' modalita' dominante nel canonico, non legge — il fresco realizza la
  modalita' complementare).

## 99f. Trappole nuove

- **(pp) il caso degenere escluso in silenzio dal denominatore e' il segnale**
  (§99c): la pipeline che salta "if not cell_vals: continue" senza contare ha
  nascosto i 230 G=0, tra cui le 2 violazioni d'orizzonte — l'unico fatto
  qualitativamente nuovo della sessione. Ogni ramo degenere (vuoto, zero, None) va
  CONTATO e riportato con la sua semantica dichiarata; se un tripwire storico
  (qui: G>=1 di §89a) non e' applicabile o non e' replicato, la sua assenza va
  dichiarata a verbale. Parente di (bb) (un gate deve poter fallire) e di (ii)
  (il rosso che maschera il testimone).

## 99g. Domande aperte / prossimo (§100)

1. **Caccia preregistrata alla coda doppia** (§99d: soglie e catena FISSATE) — se
   vuota con potenza dichiarata, "ep>8 => age<=10P" diventa candidata-struttura e
   l'evento inevitabile ha una forma a due orologi.
2. **Geometria di V† \ V sui 2 violatori** (§99c): dove vive la cella che devia la
   corsa? Quanto costa il censimento §98 rifatto alla V†? (I violatori sono il caso
   di studio concreto.)
3. **Parole ripetute nella coda** (§99b): la stessa parola in 3 orbite = la coda
   min_ep alta sembra un fenomeno di POCHE parole (word-mediated). Censire le parole
   dei testimoni su campione allargato; se la coda e' una famiglia finita di parole,
   il bordo alto di ep torna enumerabile — ironia: la via-parola risorge proprio
   dove l'orologio-record fallisce.
4. Ereditati: geometria dei rientri (§98g.2), scia quasi-universale teorema? (§98g.3),
   esperimenti separatori §97, fuggenti vs nere-D>=400, retro-nota §91c.3, stress-2
   bianche, h1=1.

## 99h. Inventario file

- `alpha1/record_minep_hunt.py` (+`record_minep_hunt_summary.json`, `.log`) — caccia
  su semi freschi: gate canonici (6 campi + hist per-record + zero G=0), tripwire
  scala, G=0 censiti con flag oltre-orizzonte, testimoni con dettaglio celle e
  dt_burst, coda doppia.
- `docs/MINEP_HUNT_ADDENDUM.md` — questo addendum.
- Pannello e baseline: scratchpad di sessione (lente1_verify_testimoni.py,
  lens2_f2_baseline.py, lens2_tripwire_full.py, w0_fragment_baseline.py); esiti
  integrali a verbale in §99b/c/e.
