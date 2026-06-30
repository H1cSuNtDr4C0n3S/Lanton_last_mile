# ADDENDUM CONSUMPTION-LEDGER — Il deficit di consumo e' il pavimento-del-morso travestito (§79)

Catena addenda: ... POTENTIAL-SEGMENT-SCANNER §67, ENDPOINT-MONOTONE-NOGO §68,
COMPATIBILITY-POTENTIAL §69, COMPAT-EVENT/CO-RAGGIUNGIBILITA' §70-§74, GA-GATE-ZERO §75,
ENTRY-SEED-FRONTIER §76, ROTOR-STALL §77, GATE-ONE-COMOVING §78, **CONSUMPTION-LEDGER §79**.

Bersaglio di sessione: prototipare il *positive gate* del ledger di consumo (grafo causale
read-black -> write-black -> read-black) proposto dopo §78, su un'orbita reale, e decidere se
l'economia auto-sostenuta dei deep-black ha un **deficit** attaccabile oppure no.

> **NOTA DI STATO (Pauli): SCOUT, non risultato certificato.** Lo strumento e' un simulatore
> **indipendente**, NON `alpha1_engine.c`. Validato sulla dinamica: onset griglia vuota = **9977**
> esatto; highway W0 periodo 104 / 58 R / drift (-2,-2); **0 violazioni di alternanza su 106000**
> passi su (7,-7). La nozione di "deep" usata qui e' un **proxy d'eta'** (age>104 ~ 1 periodo,
> age>1040 ~ 10 periodi), **NON** la `delta_r` outside-window 9x9. I conteggi vanno ri-prodotti
> con `alpha1_engine.c` e con la definizione outside-window vera prima di promuoverli da scout a dato.

## 79. Riepilogo in una frase
Falsificazione utile (gemella di §59): la **forma ingenua del lemma di consumo** — "il deep-black
eterno consuma piu' struttura di quanta una configurazione finita possa rigenerare" — e' **falsa**
sul transiente di (7,-7). Le creazioni di nero (~0.556/passo) superano le distruzioni (~0.443/passo):
il pool di nero **cresce**; l'inflow di frontiera (morsi, B-T) supera il consumo profondo **~4:1**;
e la rigenerazione e' **dominantemente locale** (eta' mediana 8 passi). L'ostruzione non e' un deficit:
vive nella **coda lunga sottile** (age>1040, 0.6%, max 4068), che coincide con lo stallo rotore
**non-abeliano** di §77.

## 79.1 Strumento: `alpha1/consumption_ledger_probe.py` (prototipo)
Simulatore set-based autosufficiente (convenzione dinamica = CLAUDE.md §2: lettura -> svolta
[bianco=R orario, nero=L] -> flip -> mossa 1). Per ogni visita registra `(t, cella, colore, fresh,
visit_count, age)`. Metriche derivate: morsi (fresh-white), black-read, classificazione deep per
soglia d'eta', bilancio creazioni/distruzioni, e **split sorgente** del nero consumato (vc=1 =
morso-fed; vc>=3 = recycle-fed). Validazione inline (vuota->9977, W0, alternanza 0/106000).
Runtime: secondi (106000 passi, dict puro).

## 79.2 Risultato (difetto (7,-7), 106000 passi, pre-onset)

| quantita' | valore |
|---|---:|
| celle distinte visitate | 21982 |
| passi / cella distinta | 4.822 |
| max visite su una cella | 30 |
| celle visitate >=4 volte | 14065 (63.98%) |
| morsi (fresh-white) | 21981  (= distinte - 1; il difetto e' fresh-black) |
| black-read totali | 47016 |
| black-read age>104 (deep) | 5614 (11.9%) |
| black-read age>1040 (deep+) | 261 (0.6%) |
| eta' rivisita-nera: mediana / p90 / p99 / max | 8 / 108 / 476 / 4068 |
| **bilancio nero**: creazioni (letture bianche) / distruzioni (letture nere) / netto | 58984 / 47016 / **+11968** |
| **sorgente**: morso-fed (vc=1) / recycle-fed (vc>=3) | 38.3% / **61.7%** |
| tra i DEEP (age>1040): morso-fed / recycle-fed | 30.7% / **69.3%** |
| ratio consumo_deep104_cum / morsi_cum | 0.255 |

Consistenza interna: morsi 21981 = celle distinte 21982 - 1 (l'unica cella fresh-black e' il difetto);
creazioni 58984 = totale letture bianche = 106000 - 47016; netto +11968 = pool di nero che cresce.

## 79.3 Interpretazione
1. **Riciclo interno reale** (61.7% recycle-fed): il reframe alpha1/consumo (il Teorema della
   Finestra appartiene al lato-alpha, non al lato-beta/lock) ha **base fattuale**, non solo intuitiva.
2. **Nessun deficit.** Creazioni > distruzioni: il pool di nero accumula; l'inflow di frontiera
   (B-T) versa nero ~4:1 sul consumo deep. La sotto-forma "consumo > rigenerazione da supporto finito"
   muore con lo **stesso meccanismo** del pavimento-del-morso (§57): il supporto NON e' finito (B-T lo
   fa crescere) e la rigenerazione e' in parte interna. E' il pavimento-del-morso travestito.
3. **La difficolta' si concentra nella coda lunga.** La rigenerazione e' dominantemente locale
   (mediana 8, p90 = 1 periodo); il riciclo a lungo raggio e' una coda sottile (age>1040, 261 eventi),
   che coincide con lo stallo rotore non-abeliano di §77 (cross-check: §77 misurava eta'-detrito
   max 3756 sulla stessa orbita; qui max 4068). Il bulk locale e' uno steady-state rotore-strutturato:
   non c'e' teorema da cavare li'.

Decomposizione empirica aggiornata (estende §59.3):
```
Teorema della Finestra        -> deep-black a densita' positiva (detrito AUTO-prodotto)
riciclo locale (mediana 8)    -> steady-state rotore-strutturato (NON attaccabile)
coda lunga (age >> periodo)   -> §77 rotore non-abeliano = l'ostruzione vera
```

## 79.4 Caveat
- **§1-i controfattuale**: una sola orbita finita convergente; misure within-orbit; survivorship
  (singolo onset alto). Non decide nulla sull'eterno.
- **"deep" = proxy d'eta'**, non `delta_r` outside-window 9x9; (7,-7) non e' rappresentativo.
- **Non cross-validato con `alpha1_engine.c`**: solo la dinamica e' validata (onset 9977 esatto +
  W0 + 0 violazioni di alternanza). La definizione di deep-black va allineata alla `delta4` reale.
- Il **meccanismo** (inflow B-T + riciclo interno) e' strutturale ⇒ NON e' un artefatto del finito.

## 79.5 Trappola nuova (cumulativa; le trappole k–m sono in CHAT_HANDOVER §77/§78)
- **(n) deficit di consumo = pavimento-del-morso travestito.** Qualunque lemma "consumo deep-black >
  rigenerazione da supporto finito" fallisce: le creazioni di nero (letture bianche, alimentate dalla
  frontiera B-T) sono >= distruzioni; il pool di nero cresce. **Non riaprire** argomenti di bilancio /
  squilibrio di tasso del consumo. La leva, se esiste, e' sulla **coda lunga** dei ritorni lontani.

## 79.6 Roadmap
1. **Gate negativo (kill-gate, prioritario):** deep-black-anchored decisive-depth sweep (stile §78.7):
   il verdetto "questo evento deep-black portera' a lock W0" e' funzione di un footprint finito
   co-moving con `P` bounded? §59 e' gia' un pre-run negativo ⇒ aspettativa: `P` esplode / non
   stabilizza ⇒ chiudere definitivamente il path deep->W0. Eseguire SOLO come gate, non come direttrice.
2. **Gate positivo (l'oggetto vero):** costruire il grafo causale read-black -> write-black ->
   read-black **ristretto ai ~261 eventi age>1040** (NON sull'orbita intera): cercare un **alfabeto
   finito di motivi** di rigenerazione a lungo raggio. E' strutturale (sopravvive ai no-go §68) e
   vicino al Teorema della Finestra (usa davvero `delta_r`). Il candidato non e' uno scalare: e' un
   grafo di rigenerazione alternante del detrito, ristretto alla coda.
3. **Ri-eseguire 79.2 con `alpha1_engine.c`** + la `delta_r` outside-window vera, sull'ensemble delle
   24 orbite lunghe (within-orbit), per confermare/correggere i conteggi dello scout.

## 79.7 Inventario file
- `alpha1/consumption_ledger_probe.py` (prototipo, autosufficiente, validato su dinamica)
- `ledger_7m7.png` (figura Okabe-Ito: inflow di frontiera vs consumo profondo; istogramma eta' di
  rigenerazione)

## 79.8 Frase di stato dell'arte
*Il caos non muore di fame: si nutre. La frontiera (B-T) versa nero piu' in fretta di quanto il consumo
profondo lo bruci, e il riciclo e' quasi tutto a corto raggio. Non c'e' un deficit da sfruttare. Se c'e'
un teorema, e' nella coda sottile dei ritorni lontani — la stessa che §77 ha trovato rotore e non-abeliana.
Il last mile non e' "il deep-black diventa porta" (ponte sbagliato, §59), e non e' "il consumo si
esaurisce" (deficit falso, §79): e' che la rigenerazione a lungo raggio non puo' sostenersi in eterno
senza degenerare in una struttura gia' esclusa.*
