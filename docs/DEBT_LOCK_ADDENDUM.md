# ADDENDUM DEBT-LOCK — Il debito profondo non predice direttamente i lock (§59)

Catena addenda: ... ALPHA1_FABRY §57, DELTA4-BETA §58, **DEBT-LOCK §59**.
Bersaglio di sessione: testare il ponte empirico piu' semplice suggerito da §58:
finestre con piu' letture nere fuori dalla memoria 9x9 (`r=4`) producono piu' lock W0-like
subito dopo?

## 59. Riepilogo in una frase
Falsificazione utile: il ponte semplice **"piu' debito profondo -> piu' lock" e' falso** sulle
24 orbite lunghe. A parita' di protocollo causale `[t-L,t) -> [t,t+H)`, l'hazard futuro di
`D>=40/80` decresce monotonamente coi quantili di deep-black; il controllo `fresh_bite`, invece,
predice positivamente i lock. Lettura: il debito profondo e' un invariante di non-localita',
ma il lock nasce nelle finestre in cui il consumo fresco/ricostruzione locale e' vivo, non nelle
finestre piu' indebitate e affamate.

## 59.1 Strumento: `alpha1/debt_lock_hazard.py`
Script senza nuove dipendenze, basato su `alpha1/delta4_long_orbits.py`:
- rigenera le 24 orbite lunghe da `rngstate`;
- valida i morsi freschi contro `dumps_all.txt`;
- usa predictor causale nel passato `[t-Lpred, t)`;
- evento futuro: esiste lock W0-like in `[t, t+H)`;
- `Lpred in {313, 1040, 3120}`, `H in {312, 1040}`, `D in {40, 80}`;
- predictor: `deep_black` r=4 e controllo `fresh_bite`;
- default `--stride 4`, deterministico, per stare sotto 5 minuti.

Output:
- `alpha1/debt_lock_hazard_summary.csv`
- `alpha1/debt_lock_hazard_bins.csv`
- `alpha1/debt_lock_hazard_summary.json`

Runtime completo: **164.3 s**, 24 orbite in pass1 + 24 in pass2. Nessuna search di onset.

## 59.2 Risultato aggregato
Per bin crescenti del predictor `deep_black`, l'hazard futuro cala in tutti i casi:

| predictor | soglia | delta top-bottom | ratio top/bottom |
|---|---:|---:|---:|
| deep_black | D>=40 | -0.2641 ... -0.1406 | 0.28 ... 0.48 |
| deep_black | D>=80 | -0.0236 ... -0.0107 | 0.13 ... 0.42 |
| fresh_bite | D>=40 | +0.1460 ... +0.3256 | 2.17 ... 6.58 |
| fresh_bite | D>=80 | +0.0117 ... +0.0271 | 3.38 ... 10.23 |

Esempio centrale (`Lpred=1040`, `H=1040`, `D>=40`):

| bin deep | mean deep | mean bite | hazard |
|---:|---:|---:|---:|
| 0 | 0.1852 | 0.1255 | 0.4867 |
| 1 | 0.2185 | 0.0716 | 0.4064 |
| 2 | 0.2383 | 0.0385 | 0.3249 |
| 3 | 0.2543 | 0.0182 | 0.2701 |
| 4 | 0.2742 | 0.0075 | 0.2226 |

Il controllo fresh-bite, nello stesso caso, va nella direzione opposta:

| bin bite | mean deep | mean bite | hazard D>=40 |
|---:|---:|---:|---:|
| 0 | 0.2627 | 0.0001 | 0.1686 |
| 1 | 0.2562 | 0.0134 | 0.2979 |
| 2 | 0.2391 | 0.0429 | 0.3677 |
| 3 | 0.2201 | 0.0775 | 0.4043 |
| 4 | 0.1888 | 0.1333 | 0.4942 |

## 59.3 Interpretazione
La non-localita' `r=4` di §58 resta il fatto strutturale: non erode, anche nelle orbite affamate.
Ma come predittore locale immediato dei lock e' anti-correlata, perche' il deep-debt alto coincide
con finestre a morso fresco quasi spento. I lock W0-like richiedono ancora attivita' di frontiera
e ricostruzione locale: il debito profondo e' il substrato di memoria, non il grilletto.

Nuova decomposizione empirica:

```
Teorema della Finestra -> non-localita' persistente
morso/freschezza locale -> lock simbolici W0-like
lock + checklist esogena -> beta
```

Quindi il ponte diretto "Finestra -> lock" va sostituito con un modello a due coordinate:
debito profondo (memoria disponibile) + freschezza/attivita' locale (innesco).

## 59.4 Caveat
- `D(t)` e' ancora solo match simbolico W0-like, non checklist T3'.
- Gli anchor sono correlati; `--stride 4` riduce costo ma non rende indipendenti i campioni.
- Il campione resta selezionato per onset alto e consiste in prefissi finiti convergenti.
- Il risultato falsifica il ponte semplice, non il ruolo teorico del debito profondo.
- I bin `fresh_bite` a finestre corte possono avere bin vuoti per massa enorme a zero: il summary
  usa bottom/top non vuoti.

## 59.5 Prossima roadmap
1. **Modello a due coordinate.** Hazard `D>=40/80` su griglia 2D `(deep_black, fresh_bite)`,
   non su predictor singolo.
2. **Lock -> checklist.** Valutare T3' sui lock profondi gia' estratti: beta vive nello stato
   delle celle esogene, non nel solo `D(t)`.
3. **Separare regimi.** Core/tail e finestre pre-onset lontane vs vicine: capire se l'anti-correlazione
   deep->lock e' solo starvation o anche geometria della memoria.

## 59.6 Inventario file
- `alpha1/debt_lock_hazard.py`
- `alpha1/debt_lock_hazard_summary.csv`
- `alpha1/debt_lock_hazard_bins.csv`
- `alpha1/debt_lock_hazard_summary.json`

## 59.7 Frase di stato dell'arte
*La memoria profonda non si spegne, ma non basta a far bussare. Quando il debito e' massimo,
la frontiera e' spesso muta; quando la frontiera torna a masticare, compaiono i lock. La prossima
variabile non e' una soglia singola ma una coppia: memoria profonda piu' innesco locale.*
