# ADDENDUM DEBT-LOCK 2D — Memoria profonda + innesco locale (§60)

Catena addenda: ... DELTA4-BETA §58, DEBT-LOCK §59, **DEBT-LOCK 2D §60**.
Bersaglio di sessione: dopo la falsificazione del ponte diretto deep-black -> lock (§59), testare
il modello a due coordinate `(deep_black, fresh_bite) -> lock`.

## 60. Riepilogo in una frase
La griglia 2D conferma la correzione: **fresh-bite e' il predittore positivo dei lock anche a
deep quasi fissato**, mentre deep-black resta negativo/debole anche a bite quasi fissato. Il lock
non e' prodotto dal debito profondo da solo; nasce quando la memoria profonda e' disponibile ma
l'attivita' fresca locale e' ancora accesa. Il prossimo passo naturale non e' un altro predictor
scalare, ma `lock -> checklist T3'`.

## 60.1 Strumento: `alpha1/debt_lock_2d.py`
Script senza nuove dipendenze, stesso protocollo causale di §59:
- predictor in `[t-Lpred, t)`;
- evento lock in `[t, t+H)`;
- `Lpred in {313, 1040, 3120}`, `H in {312, 1040}`, `D in {40, 80}`;
- bin indipendenti per `deep_black` e `fresh_bite`;
- summary con effetto di deep entro strisce di bite e effetto di bite entro strisce di deep.

Output:
- `alpha1/debt_lock_2d_grid.csv`
- `alpha1/debt_lock_2d_summary.csv`
- `alpha1/debt_lock_2d_summary.json`

Runtime completo: **146.7 s**, 24 orbite in pass1 + 24 in pass2. Nessuna search di onset.

## 60.2 Risultato aggregato
Effetto medio pesato entro strisce:

| soglia | deep effect entro bite | bite effect entro deep |
|---|---:|---:|
| D>=40 | min -0.0911, mediana **-0.0350**, max -0.0208 | min +0.0697, mediana **+0.1373**, max +0.2640 |
| D>=80 | min -0.0046, mediana **-0.0022**, max +0.0018 | min +0.0024, mediana **+0.0121**, max +0.0181 |

Caso centrale (`Lpred=1040`, `H=1040`):

| D | best cell `(deep,bite)` | best hazard | worst cell `(deep,bite)` | worst hazard | deep effect | bite effect |
|---:|---|---:|---|---:|---:|---:|
| 40 | (0,4) | **0.5063** | (4,0) | 0.1601 | -0.0621 | +0.1645 |
| 80 | (0,4) | **0.0299** | (2,0) | 0.0054 | -0.0035 | +0.0130 |

Interpretazione operativa: il massimo hazard sta nella cella **deep basso / bite alto**, non in
deep alto. Il deep alto segnala starvation/memoria riciclata; il lock richiede ancora frontiera
attiva.

## 60.3 Lettura strategica
§58 resta valido: la non-localita' profonda non erode e quindi il Teorema della Finestra e' ancora
l'invariante robusto. §59-§60 chiariscono pero' che questa non-localita' non e' il grilletto
immediato dei lock. La decomposizione empirica aggiornata e':

```
non-localita' r=4 persistente = substrato di memoria
fresh-bite/freschezza locale = innesco dei lock simbolici
lock simbolico + checklist esogena = beta
```

Quindi il fronte utile si sposta alla checklist: tra i lock prodotti nelle finestre a bite alto,
quale stato delle celle esogene decide l'ingresso o la morte?

## 60.4 Caveat
- I bin 2D non sono indipendenti: anchor vicini condividono gran parte della finestra.
- `D(t)` resta match simbolico, non checklist T3'.
- Il risultato e' empirico su prefissi finiti selezionati per onset alto.
- La griglia 2D usa `--stride 4`; `--stride 1` e' disponibile ma piu' costoso.

## 60.5 Prossima roadmap
1. **Lock -> checklist T3'.** Sui lock `D>=40/80` gia' estraibili, valutare la checklist esogena
   completa o una proxy iniziale per porte/fasi principali.
2. **Stratificare per celle esogene.** Separare lock morti per dogana, frontiera, soglia sepolta,
   come in T3' ma sulle 24 orbite lunghe.
3. **Modello hazard a tre stadi.** `fresh-bite -> lock`, `lock -> checklist`, `checklist -> ingresso`.

## 60.6 Inventario file
- `alpha1/debt_lock_2d.py`
- `alpha1/debt_lock_2d_grid.csv`
- `alpha1/debt_lock_2d_summary.csv`
- `alpha1/debt_lock_2d_summary.json`

## 60.7 Frase di stato dell'arte
*La memoria profonda e' il terreno, non la scintilla. La scintilla e' la freschezza locale: quando
la formica torna a mordere, i fattori W0-like compaiono; poi decide la dogana.*
