# ADDENDUM DOOR-DEFECT-PROFILE — Profilo globale delle 22 porte (§66)

Catena addenda: ... CHECKLIST-VECTOR-MODEL §64, CHECKLIST-NONLOCAL §65,
**DOOR-DEFECT-PROFILE §66**.
Bersaglio di sessione: eseguire il passo operativo suggerito da Pauli in §65: per ogni
tentativo porta, leggere tutte le 22 fasi/gate e misurare la profondita' del primo difetto
`h_g(L)`. Il risultato chiarisce un punto importante: sul campione gia' condizionato da lock
W0-like, la fase reale e' sempre la migliore; quindi il profilo lock-condizionato non e'
ancora l'invariante globale cercato.

## 66. Riepilogo in una frase
`door_defect_profile.py` conferma e rafforza §63/§64: sui **810** tentativi porta la fase reale
e' la **migliore unica in 810/810** casi, mentre le fasi alternative compatibili col primo bit
muoiono entro **5** letture esogene. Questo e' un buon controllo di coerenza, ma declassa il
profilo "22 porte sul lock" a oggetto lock-condizionato: il prossimo passo deve essere uno
scanner non condizionato del campo di detriti.

## 66.1 Strumento
Nuovo file:

```
alpha1/door_defect_profile.py
```

Per ogni tentativo porta deduplicato come §63:
- ricostruisce lo stato della formica al tempo del lock;
- valuta tutte le **22** fasi in `GATE_PHASES`;
- misura `h_g(L)` per `L=208,512,1600`;
- separa fasi incompatibili al primo bit, fasi compatibili alternative e fase reale;
- salva righe fase-orizzonte, sintesi per tentativo e sintesi per orbita.

Output generati:

```
alpha1/door_defect_profile_rows.csv
alpha1/door_defect_profile_attempts.csv
alpha1/door_defect_profile_orbits.csv
alpha1/door_defect_profile_summary.json
```

Controllo indipendente: la riga della fase reale a `L=1600` coincide con §63 su tutti i
tentativi (`compare_mismatches = 0` contro `checklist_vector_geometry_attempts.csv`).

## 66.2 Run completa
Comando:

```
C:\Python\Python310\python.exe alpha1\door_defect_profile.py --max-seconds 290 --out-prefix alpha1\door_defect_profile
```

Risultato:
- orbite completate: **24/24**;
- tentativi porta: **810** = **786** fallimenti + **24** ingressi;
- righe tentativo-orizzonte: **2430**;
- righe fase-orizzonte: **53.460**;
- runtime: **69 s**.

Self-test prima della run:
- `window_automaton.py --selftest`: verde;
- `product_automaton.py --selftest`: verde;
- `alpha1_engine.exe dump`: vuota -> **9977**, seme `(7,-7)` -> **106258**.

## 66.3 Numeri principali
Per ogni orizzonte:

| L | actual_is_best | best unico | failure clear | entry clear | max h sui fallimenti |
|---:|---:|---:|---:|---:|---:|
| 208 | 810/810 | 810/810 | 12 | 24 | 209 |
| 512 | 810/810 | 810/810 | 4 | 24 | 513 |
| 1600 | 810/810 | 810/810 | 0 | 24 | 1591 |

Le fasi compatibili col primo bit sono sempre **11** per tentativo. Tra le fasi compatibili
alternative:
- righe per orizzonte: **8100**;
- clear: **0**;
- `h` mediana: **2**;
- `h` massimo: **5**.

Le fasi incompatibili al primo bit muoiono tutte a `h=0`, come previsto.

Alla scala `L=1600`:
- tutti i **786** fallimenti hanno difetto entro orizzonte;
- i **24** ingressi veri sono clear;
- tipi di errore sui fallimenti: **419** `frontier_black_collision`, **367** `missing_black`.

La coda oltre due periodi viene ritrovata esattamente:

```
268, 273, 279, 298, 373, 488, 488, 492, 685, 799, 1533, 1591
```

Sono tutti `frontier_black_collision`; quattro restano oltre `L=512`.

## 66.4 Interpretazione
Il profilo risponde a una domanda piu' debole di quella globale. Se si parte gia' da un lock
W0-like, la fase reale e' selezionata dal lock stesso: le altre fasi compatibili falliscono
quasi subito per mismatch locale della parola, e le incompatibili falliscono al primo bit.

Quindi:
- il risultato e' un forte controllo di coerenza della pipeline §61-§64;
- conferma che la coda non-locale appartiene alla fase reale, non a una scelta alternativa
  nascosta tra le 22 porte;
- ma **non** produce ancora un invariante globale del campo di detriti.

La frase corretta non e': "abbiamo trovato la porta globale migliore".
La frase corretta e': "sui lock gia' selezionati, la porta migliore e' tautologicamente la
fase del lock; il crux globale sta prima della selezione del lock".

## 66.5 Prossimo passo (§67)
La priorita' cambia forma:

1. **Lemma di non-localita' T3'**: ancora da scrivere. Per ogni R, costruire due campi uguali
   in `B_R` della porta ma con verdetto diverso per una lettura esogena fuori `B_R`. Se il
   lemma usa campi sintetici, chiamarlo non-localita' sintattica; la versione dinamica richiede
   campi raggiungibili o una loro chiusura naturale.
2. **Scanner non condizionato delle 22 porte**: campionare ancore non selezionate da lock profondi
   e misurare `H_L=max_g h_g(L)` sul campo di detriti. Stratificare almeno per tempo/orbita,
   morso fresco, deep-black e profondita' W0-like `D(t)`. Questo e' il baseline che manca.

Solo dopo questi due passi ha senso tornare al "potenziale globale": il profilo lock-condizionato
ha mostrato dove non cercarlo.

## 66.6 File prodotti
- `alpha1/door_defect_profile.py`
- `alpha1/door_defect_profile_rows.csv`
- `alpha1/door_defect_profile_attempts.csv`
- `alpha1/door_defect_profile_orbits.csv`
- `alpha1/door_defect_profile_summary.json`

I file `door_defect_profile_smoke_*` sono solo output temporanei della smoke test e non fanno
parte del risultato §66.
