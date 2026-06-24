# ADDENDUM DELTA4-BETA — Sonda breve: la non-localita' r=4 non erode (§58)

Catena addenda: ... RADIUS §45-55, PRODOTTO §56, ALPHA1_FABRY §57, **DELTA4-BETA §58**.
Bersaglio di sessione: dopo il fallimento del pavimento del morso fresco (§57), misurare sulle
stesse 24 orbite lunghe se il tasso di letture nere fuori dalla finestra 9x9 (`r=4`) tiene un
pavimento mentre il morso fresco affonda, e se i lock W0-like restano ricorrenti.

## 58. Riepilogo in una frase
Sulle 24 orbite lunghe gia' costose (onset 251k-313k), il morso fresco e' affamato ma la
non-localita' `r=4` resta massiccia: tasso nero fuori-finestra mediano **0.2334/passo**,
tail/core mediano **1.06**, minimi mobili ancora **9x, 16x, 27.4x** sopra `delta4_auto=2/313`
per finestre `313, 1040, 10400`; quindi l'invariante giusto non e' il morso fresco ma il debito
di memoria profonda. Questo non dimostra beta, pero' sposta il prossimo bersaglio su
"debito profondo -> lock/checklist".

## 58.1 Strumento: `alpha1/delta4_long_orbits.py`
Script self-contained, senza nuove dipendenze:
- legge le 24 intestazioni di `alpha1/dumps_all.txt`;
- rigenera ogni orbita da `rngstate` con lo stesso xorshift e la stessa convenzione di
  `alpha1_engine.c` (`DY=(-1,0,1,0)`);
- valida byte-per-byte i tempi di morso fresco contro `dumps_all.txt`;
- misura le letture nere fuori dalla memoria 9x9 (`r=4`) nel transiente;
- calcola minimi mobili su finestre `313, 1040, 10400`;
- calcola un lock simbolico semplice `D(t)` contro fattori di `W0` per soglie `40` e `80`.

Output:
- `alpha1/delta4_long_orbits_summary.csv`
- `alpha1/delta4_long_orbits_windows.csv`
- `alpha1/delta4_long_orbits_summary.json`

Runtime completo: **72.6 s** sulle 24 orbite. Nessuna search di nuovi onset.

## 58.2 Self-test e validazioni
Prima della sonda:
- `window_automaton.py --selftest`: verde.
- `product_automaton.py --selftest`: verde.
- `alpha1_engine`: griglia vuota -> `9977`; difetto `(7,-7)` -> `106258`.

Validazioni interne della sonda:
- `onset` header = `onset` dump per tutti i blocchi.
- i morsi freschi simulati coincidono con `dumps_all.txt` per tutte le orbite.
- prova `--limit 1`: orbita top ricostruita in 3.46 s con gli stessi valori principali.

## 58.3 Risultati quantitativi
Sulle 24 orbite:

| quantita' | min | mediana | max |
|---|---:|---:|---:|
| tasso nero fuori-finestra `r=4` | 0.2277 | **0.2334** | 0.2378 |
| tasso morso fresco | 0.0466 | **0.0537** | 0.0627 |
| tail/core nero fuori-finestra | 1.031 | **1.058** | 1.093 |
| tail/core morso fresco | 0.439 | **0.614** | 0.795 |

Minimi mobili:

| finestra L | min nero profondo | multiplo di `2/313` | min morso fresco |
|---:|---:|---:|---:|
| 313 | 0.0575 | **9.0x** | 0.0000 |
| 1040 | 0.1019 | **16.0x** | 0.0000 |
| 10400 | 0.1750 | **27.4x** | 0.0000 |

Per il morso fresco, il minimo a `L=313` e `L=1040` e' zero su tutte le orbite; a `L=10400`
il minimo globale e' ancora zero e la mediana e' `0.00606`. Il debito profondo fa l'opposto:
il minimo cresce con la finestra, e il tail non peggiora.

## 58.4 Lock simbolici W0-like
Il contatore `D(t)` e' volutamente leggero: match simbolico con fattori di `W0`, non checklist.

- `D>=40`: presente in tutte le 24 orbite; run per orbita min **113**, mediana **130**, max **167**.
- `maxD` letto dalla colonna `D40`: min **78**, mediana **167**, max **1591**.
- `D>=80`: variabile; run per orbita min **0**, mediana **4**, max **12**.

Lettura: i lock profondi non scompaiono nelle orbite affamate. Pero' `D(t)` da solo non e'
beta: manca lo stato della checklist esogena.

## 58.5 Verdetto
La sonda risponde alla domanda timeboxed: **si', `delta_r` tiene mentre il morso fresco affonda**.
Il fallimento del "modo DC del morso" non tocca il Teorema della Finestra; anzi, sulle orbite
selezionate per starvation, il debito nero profondo resta alto e leggermente piu' forte nel tail.

Questo non chiude alpha1/beta, per tre ragioni:
- campione finito e selezionato per onset alto;
- tutte le orbite osservate convergono, quindi resta il caveat del controfattuale eterno;
- il lock misurato e' solo simbolico: non include dogane/checklist.

## 58.6 Nuova roadmap
1. **Debito profondo -> lock.** Misurare hazard di `D>=40/80` condizionato al debito nero
   fuori-finestra in finestre precedenti, invece che al morso fresco.
2. **Debito profondo -> checklist.** Integrare un valutatore checklist T3' sui lock profondi
   delle 24 orbite: il passo beta vero e' capire se il debito rimescola le celle esogene.
3. **Lemma B.** Tradurre empiricamente il fatto chiave: la memoria antica non puo' essere
   eternamente economica senza produrre lock o prime-visite nere.
4. **Non riaprire la caccia al record onset.** I massimi campionari non sono struttura.

## 58.7 Trappole nuove
- `dumps_all.txt` contiene solo i tempi di morso, non le svolte o il campo: per `delta4` bisogna
  rigenerare da `rngstate`.
- Non confondere `D>=40` con beta: e' solo un lock simbolico, senza dogana.
- Il massimo `D` minimo va letto dalla statistica `D40`; `D80` puo' essere assente in alcune orbite.
- La convenzione `DY` deve seguire `alpha1_engine.c`; `orbit_debt.py` usa una convenzione verticale
  diversa ma simmetrica per la griglia vuota. Per i `rngstate` lunghi, usare sempre l'engine.

## 58.8 Inventario file
- `alpha1/delta4_long_orbits.py` — sonda principale.
- `alpha1/delta4_long_orbits_summary.csv` — una riga per orbita.
- `alpha1/delta4_long_orbits_windows.csv` — righe per orbita/finestra/tipo evento.
- `alpha1/delta4_long_orbits_summary.json` — summary completo con parametri e righe.

## 58.9 Frase di stato dell'arte
*Il morso fresco si spegne, ma la memoria profonda no. Le orbite piu' affamate continuano a
pagare nero fuori dalla finestra 9x9 a un tasso trenta volte sopra il pavimento automatico,
e continuano a produrre lock simbolici. Il prossimo ponte non e' piu' frontiera -> highway,
ma debito profondo -> dogane.*
