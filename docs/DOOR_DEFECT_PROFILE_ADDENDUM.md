# ADDENDUM DOOR-DEFECT-PROFILE — Profilo globale delle 22 porte (§66)

Catena addenda: ... CHECKLIST-VECTOR-MODEL §64, CHECKLIST-NONLOCAL §65,
**DOOR-DEFECT-PROFILE §66**.
Bersaglio di sessione: eseguire il passo operativo suggerito da Pauli in §65: per ogni
tentativo porta, leggere tutte le 22 fasi/gate e misurare la profondita' del primo difetto
`h_g(L)`. Il risultato chiarisce un punto importante: sul campione gia' condizionato da lock
W0-like, la fase reale e' sempre la migliore; quindi il profilo lock-condizionato non e'
ancora l'invariante globale cercato.
Nota strategica aggiunta prima di §67: il vero contenuto di §66 e' un'asimmetria. Identificare
la porta e' locale; decidere se la porta vera entra e' globale.

## 66. Riepilogo in una frase
`door_defect_profile.py` conferma e rafforza §63/§64: sui **810** tentativi porta la fase reale
e' la **migliore unica in 810/810** casi, mentre le fasi alternative compatibili col primo bit
muoiono entro **5** letture esogene. Questo e' un buon controllo di coerenza, ma declassa il
profilo "22 porte sul lock" a oggetto lock-condizionato: il prossimo passo deve essere uno
scanner non condizionato del campo di detriti.

## 66.0-a Asimmetria locale/globale
§66 va nominato per quello che e':

```
identificare quale porta si sta provando = locale;
decidere se quella porta entra = globale.
```

Le fasi alternative compatibili col primo bit muoiono entro **5** letture esogene. La fase reale
e' best unica in **810/810** casi. Quindi la meta' "quale porta?" e' localmente sigillata dal lock.

La meta' "la porta entra?" resta invece non-locale: la fase reale puo' morire a offset **1591**
e distanza L∞ **36**. L'invariante globale, se esiste, non vive nell'identificazione della porta;
vive nel successo d'ingresso della porta gia' identificata.

Questa e' la ragione per cui il profilo lock-condizionato non e' una delusione: chiude la meta'
locale dell'asimmetria e lascia esposta l'unica meta' ancora utile.

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

1. **Lemma di non-localita' T3'**: non sovra-investire. La non-localita' sintattica e' quasi
   a priori: la checklist legge la cavalcata futura infinita della highway, quindi per ogni
   raggio R si puo' spostare la cella discriminante oltre `B_R`. Il peso vero non e'
   l'esistenza combinatoria della coppia di colorazioni, ma la **realizzabilita'**: le coppie
   discriminanti devono appartenere a campi raggiungibili da semi finiti, o a una chiusura
   naturale di tali campi. `L∞=36` e' solo il floor empirico che mostra che il lemma non e'
   vacuo nel campione.
2. **Candidato Φ globale**: formulare prima dello scanner un funzionale del detrito
   `Φ(detrito)` con quattro condizioni:
   - `Φ` limitato dal basso;
   - ogni rivisita nera profonda lo decrementa con massa non sommabile: decremento uniforme
     `ε>0`, oppure valori discreti/ordine ben fondato;
   - `Φ=0` se e solo se qualche porta entra;
   - `Φ` non e' prossimita' al lock, perche' §59 ha falsificato proprio quel proxy.
3. **Scanner non condizionato delle 22 porte**: campionare ancore non selezionate da lock profondi
   e misurare `H_L=max_g h_g(L)` sul campo di detriti. Stratificare almeno per tempo/orbita,
   morso fresco, deep-black e profondita' W0-like `D(t)`. Ma lo scanner non deve restare una
   caratterizzazione aperta: deve falsificare o sostenere la proprieta' floor-decrement di `Φ`.

Solo dopo questi passi ha senso tornare al "potenziale globale": il profilo lock-condizionato
ha mostrato dove non cercarlo, e il candidato `Φ` dice invece cosa lo scanner deve provare a
uccidere.

## 66.6 Cambio di categoria: da tasso a raggiungibilita'
La domanda globale

```
puo' il detrito restare ostile a tutte e 22 le porte per sempre?
```

non e' un tasso: e' un enunciato qualitativo di raggiungibilita'/evitamento. Questo e' il
cambio di categoria che riapre strumenti che la versione-tasso di α1 aveva reso ciechi:
combinatorics on words, coloring-avoidance e anche strumenti topologici di tipo indice, se
formulati su un problema si/no di raggiungibilita' invece che su un valore medio.

Il caveat resta duro: uno scanner su orbite finite eredita la trappola del controfattuale eterno.
Non puo' provare α1. Serve per falsificare candidati `Φ` o per produrre l'oggetto empirico che
un invariante globale dovra' spiegare.

## 66.7 Candidato di prova: potenziale Φ
Il candidato operativo per §67 e':

```
Φ(campo di detriti)
```

con:
- **(a) lower bound:** `Φ` e' limitato inferiormente;
- **(b) decremento forzato:** ogni lettura nera profonda fuori-finestra decrementa `Φ` in modo
  non sommabile: o con `ε` uniforme, o in un codominio discreto/ben fondato;
- **(c) assorbimento:** `Φ=0` equivale all'esistenza di una porta che entra;
- **(d) non-lock-proxy:** `Φ` non misura "vicinanza al lock", perche' §59 mostra che deep-black
  e lock sono anti-correlati nel predittore locale.

Se un tale `Φ` esiste, la logica sarebbe:

```
Teorema della Finestra + floor §58  =>  eventi deep-black ricorrenti
decremento uniforme/discreto        =>  massa di decremento non sommabile
Φ lower bounded                    =>  impossibile evitare il livello 0 per sempre
Φ=0                                =>  ingresso
β/Dogana                           =>  ingresso assorbente
```

Nel lato provato, il Teorema della Finestra forza ricorrenza di letture nere fuori finestra.
Il floor §58 e' evidenza empirica robusta sul campione lungo, non un assioma dimostrativo da
usare senza prova. Per una dimostrazione, il floor deve essere sostituito da una stima certificata
o da un ordine discreto che renda impossibile una discesa infinita.

Il crux onesto e' l'urto fra (b) e (d): esiste un funzionale del detrito decrementato dalle
rivisite nere profonde, ma diverso dalla prossimita' al lock? La scelta ovvia e' morta in §59.
Trovare un `Φ` cosi', o dimostrare che non esiste in una classe naturale, e' il bersaglio ben
posto di §67.

### 66.7-a Prima falsificazione empirica di Φ
§67 non deve cercare subito un `Φ` astratto. Deve proporre 2-3 candidati rozzi e provare a
ucciderli su segmenti tra gate-attempt consecutivi:

```
deep-black forced events > 0,
nessun ingresso nel segmento,
ma Φ(next) >= Φ(prev).
```

Questo e' il test killer minimale. Una versione piu' forte cerca ricorrenze empiriche del
profilo globale: due stati con profilo porta/vettore T3' simile o migliore, molte rivisite nere
profonde in mezzo e nessun ingresso. Se il deficit verso ingresso non scende monotonicamente,
quel candidato `Φ` e' morto.

## 66.8 File prodotti
- `alpha1/door_defect_profile.py`
- `alpha1/door_defect_profile_rows.csv`
- `alpha1/door_defect_profile_attempts.csv`
- `alpha1/door_defect_profile_orbits.csv`
- `alpha1/door_defect_profile_summary.json`

I file `door_defect_profile_smoke_*` sono solo output temporanei della smoke test e non fanno
parte del risultato §66.
