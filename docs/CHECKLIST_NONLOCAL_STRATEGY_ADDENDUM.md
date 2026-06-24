# ADDENDUM CHECKLIST-NONLOCAL — Dicotomia locale/globale e ridirezione (§65)

Catena addenda: ... CHECKLIST-VECTOR §63, CHECKLIST-VECTOR-MODEL §64,
**CHECKLIST-NONLOCAL §65**.
Bersaglio di sessione: registrare la lettura strategica imposta da §61 e §64. Il ponte
`lock -> checklist` resta solido; il punto nuovo e' che la checklist che decide il verdetto
non si comporta come un oggetto locale a raggio corto sul campione lungo. Il sottoagente Pauli
ha corretto il punto logico: §65 e' diagnosi strategica, non teorema di non-localita' matematica.
Quindi la prossima domanda non e' comprimere ancora il vettore sullo stesso campione, ma rendere
esplicita la non-localita' di T3' e poi cercare un invariante globale del campo di detriti.

## 65. Riepilogo in una frase
§61 e §64 non vanno indeboliti: il ponte locale `lock -> checklist -> verdetto` e' esatto
nel campione lungo. Ma i numeri §64 mostrano che T3' legge informazione lontana nel vettore:
la massa delle prime morti e' negli offset **45-99** (**677/786**, non tutte), e i **12**
fallimenti non coperti dai due periodi sono tutte collisioni di frontiera a offset **268...1591**,
con distanza relativa L1 **16...69** e L∞ **10...36**. La compressione 37/66 riduce il numero
di componenti, non rende locali le celle. Per trasformare questa diagnosi in teorema serve un
lemma separato di non-localita' di T3'.

## 65.1 Che cosa e' confermato
Restano risultati veri:
- §61: **891/891** gate-lock pre-onset muoiono esattamente alla prima lettura esogena cattiva;
  **24/24** onset veri passano il controllo positivo.
- §64: full-vector diagonale sul campione deduplicato: **786/786** KO con mismatch,
  **24/24** OK senza mismatch.

Il nuovo punto non nega questi risultati: li interpreta. La checklist e' il verdetto giusto,
ma il suo dominio non e' una finestra locale attorno alla formica.

## 65.2 Verifica numerica della non-localita'
Dai CSV §64:

| classe | valore |
|---|---:|
| prime cattive totali | 786 |
| prime cattive con offset 45-99 | **677** |
| quota offset 45-99 | **0.861** |
| fallimenti coperti da offset <=207 | 774 |
| fallimenti mancati da due periodi | **12** |

I 12 mancati sono tutti `frontier_black_collision`:

| offset | fase | distanza L1 | distanza L∞ |
|---:|---:|---:|---:|
| 268 | 99 | 20 | 10 |
| 273 | 100 | 19 | 11 |
| 279 | 0 | 17 | 12 |
| 298 | 103 | 16 | 11 |
| 373 | 0 | 21 | 13 |
| 488 | 103 | 26 | 16 |
| 488 | 0 | 26 | 16 |
| 492 | 99 | 28 | 16 |
| 685 | 0 | 33 | 19 |
| 799 | 0 | 37 | 22 |
| 1533 | 99 | 69 | 36 |
| 1591 | 24 | 67 | 36 |

Quindi il dato non dice "tutte le prime morti stanno a 45-99"; dice una cosa piu' utile:
il core del verdetto sta a 45-99, ma la diagonale esatta richiede anche frontiera lontana.

## 65.3 Perche' la compressione non basta
La compressione §64 e' utile come descrizione empirica:
- 37 offset esatti mantengono la diagonale nel campione lungo;
- 66 componenti phase-conditioned mantengono la diagonale nel campione lungo.

Pero' questa e' compressione del **numero** di vincoli, non della loro geometria. Una componente
a offset 99, 799 o 1591 resta una lettura lontana lungo il canale della highway. In particolare,
una finestra locale di raggio fisso non puo' sapere se una cella lontana sara' bianca o nera
quando il canale la raggiunge, a meno di portarsi dietro memoria spaziale del campo di detriti.

Questa e' la stessa ostruzione vista in §56.4-§56.5: la memoria spaziale sufficiente esplode.
Il prodotto A(r;m,D) e' sound e ottimo come verificatore locale/campionario, ma non diventa un
certificatore globale della checklist se il dominio da ricordare cresce con il transiente.

## 65.4 Dicotomia locale/globale
La parte locale/finita resta sigillata:
- Teorema della Finestra r<=4 e tariffe certificate;
- γ sui periodi piccoli;
- T1, T2, α2, T3' come pacchetto finito;
- §61 lock -> checklist -> verdetto esatto;
- §64 full-vector diagonale sul campione lungo.

La parte non-locale e' il crux:

```
un'orbita eterna non-highway produce mai un campo di detriti che ammette una delle 22 porte?
```

Questa domanda e' α1/β nella sua forma corretta. Non e' un tasso locale, non e' un pavimento
di morso fresco, non e' un min-cycle-mean su memoria finita, e non e' una compressione di CSV.
Eredita le trappole gia' viste:
- controfattuale eterno (§57.7-c): nessun campione finito decide l'enunciato;
- non-localita': le celle decisive possono stare lontano dalla finestra della formica;
- timing-blindness degli invarianti topologici/discreti: un indice intero non vede un tasso
  o una sequenza di gate mobili se non incorpora il campo di detriti.

## 65.5 Unificazione dei fallimenti precedenti
La stessa barriera spiega perche' diversi fronti non hanno chiuso il crux:
- §57: il pavimento del morso fresco erode, perche' non e' l'informazione globale giusta.
- §59: `deep_black -> lock` e' anti-correlato localmente, perche' il debito e' substrato,
  non grilletto.
- §56.4: il min-cycle-mean del prodotto riespone rotori/fantasmi e poi urta l'esplosione di
  memoria spaziale.
- §64: il vettore si comprime ma resta geometricamente lontano.

La formulazione comune: l'ingresso richiede matching globale del detrito rispetto a una porta
mobile. Qualunque strumento a raggio fisso o a memoria spaziale piccola vede solo una proiezione
del problema.

## 65.6 Correzione del sottoagente: cosa non e' ancora provato
Pauli segnala un punto giusto e va registrato: i numeri §64/§65 non provano da soli una
non-localita' matematica di T3'. Provano che:
- il troncamento a due periodi fallisce nel campione lungo;
- alcune celle decisive stanno lontane dalla formica, fino a offset 1591 e L∞ 36;
- la compressione empirica non localizza geometricamente la checklist.

Per dire "T3' non e' determinata da un raggio finito" serve invece un lemma esplicito:

```
per ogni R esistono due campi C,C' che coincidono in B_R della porta,
ma hanno verdetto T3' diverso per una lettura esogena fuori da B_R.
```

Se il lemma viene dimostrato solo su configurazioni sintetiche, il risultato e' **non-localita'
sintattica** della checklist. Per diventare ostacolo dinamico completo deve essere rafforzato
su campi di detriti raggiungibili, o su un limite/chiusura naturale di tali campi. Questa
distinzione evita di vendere come prova cio' che §65 ha solo diagnosticato.

## 65.7 Ridirezione operativa §66
La priorita' non e' piu' "comprimere meglio sullo stesso campione". Il prossimo oggetto deve
avere la forma giusta, ma va costruito in due passi.

### 65.7-a Lemma di non-localita' T3'
Prima rendere formale il lemma sopra:
- fissare una porta/fase e il suo ordine di letture esogene;
- per ogni R scegliere una lettura a distanza >R;
- costruire due campi uguali in B_R e discordi solo sulla cella letta lontano;
- mostrare che il verdetto T3' cambia.

Questa prova sarebbe un lemma di interfaccia: non chiude α1, ma vieta di trattare T3' come
predicato di finestra locale.

### 65.7-b Profilo globale dei difetti di porta
Poi misurare l'oggetto della forma giusta:

**profilo dei difetti sulle 22 porte.**

Per ogni tentativo porta e per ogni fase/porta `g`, calcolare:
- `h_g(L)`: prima lettura cattiva entro l'orizzonte `L`, oppure `L+1` se non c'e';
- tipo della prima cattiva (`missing_black`, `frontier_black_collision`, ...);
- offset, cella relativa, distanze L1/L∞;
- `H_L = max_g h_g(L)`, cioe' la profondita' della porta migliore;
- orizzonti minimi: `L=208`, `512`, `1600`.

Il controllo deve includere leave-one-orbit-out e baseline non condizionata. Qui la baseline
torna utile non come prova, ma come filtro anti-overfitting: se il profilo e' idiosincratico
dei 24 onset lunghi, non e' ancora l'invariante giusto.

### 65.7-c Invariante globale del campo di detriti
Solo dopo il profilo ha senso cercare un:

**Invariante globale del campo di detriti.**

Domanda da rendere matematica:
*puo' un'orbita eterna mantenere il campo ostile a tutte e 22 le porte per sempre, mentre la
porta continua a muoversi e il detrito viene riscritto?*

Linee ammissibili:
- un potenziale globale sul campo, non a raggio fisso;
- un argomento ergodico/di misura sulla successione dei campi alle porte;
- un principio di rimescolamento globale che trasformi "porta mobile + vettore non-locale" in
  impossibilita' di evitamento eterno.

Linee declassate:
- altra compressione empirica del vettore sullo stesso campione;
- altra soglia scalare locale;
- altro min-cycle-mean senza memoria globale del detrito.

## 65.8 Caveat
- "Nessun automa a raggio finito" va letto nel senso uniforme/globale: un raggio abbastanza
  grande puo' coprire un campione finito, ma non T3' per configurazioni finite arbitrarie e
  transienti di scala non limitata.
- §65 e' una ridirezione strategica, non un nuovo teorema.
- Il lemma §65.7-a, se sintetico, prova non-localita' della checklist come predicato; non prova
  ancora che un'orbita eterna raggiungibile possa sfruttare o evitare quella non-localita'.
- Il campione §64 resta finito e selezionato per onset alto; qui viene usato per falsificare
  la speranza di localita', non per provare α1.

## 65.9 Frase di stato dell'arte
*Il locale e' chiuso, ma l'ingresso non e' locale. La checklist decide esattamente, pero' legge
un campo di detriti disteso lungo il canale futuro. Comprimerla riduce la lista, non il raggio.
Il prossimo passo e' prima formalizzare questa non-localita' per T3', poi misurare il profilo
dei difetti sulle 22 porte, e solo allora cercare l'invariante globale capace di dire se un
campo puo' evitare per sempre tutte le porte mobili.*
