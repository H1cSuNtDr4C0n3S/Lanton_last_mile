# ADDENDUM DEEP-MOTIF-SATURATION — Il lato-alpha (detrito) non e' finito-stato (§80)

Catena addenda: ... GA-GATE-ZERO §75, ENTRY-SEED-FRONTIER §76, ROTOR-STALL §77,
GATE-ONE-COMOVING §78, CONSUMPTION-LEDGER §79, **DEEP-MOTIF-SATURATION §80**.

Bersaglio di sessione: eseguire il *positive gate* di §79.6 — l'alfabeto dei motivi locali
co-moving agli eventi deep-black (il detrito delta4) e' finito (un manico) o cresce col territorio?

> **NOTA DI STATO: run REALE** su Ryzen 7 5800X (16 core), 24 orbite lunghe vere ricostruite da
> `dumps_all.txt`, 22 s. Dinamica + definizione deep-black riusate **identiche** da
> `delta4_long_orbits.py` (deep = nera fuori dalla finestra 9x9 viva, gia' letta). Il "motivo" e' il
> campo nero co-moving *pieno* entro raggio r, normalizzato in heading (C4). Strumento:
> `alpha1/deep_motif_saturation.py`; output `alpha1/deep_motif_saturation_summary.json`.

## 80. Riepilogo in una frase
Il positive gate e' **morto**: l'alfabeto dei motivi locali agli eventi deep-black **non satura**.
Quasi ogni evento e' localmente unico (r=3: ~99,4%, 73.959 motivi distinti / 74.416 eventi sull'orbita
piu' lunga), la scoperta di nuovi motivi **non cala** (ultimo20%/primo20% = 1,14 mediana), e non esiste
alcun alfabeto universale tra orbite (r=3 unione/somma = **0,979**, intersezione = **19** motivi su 1,5M).
Il detrito non ha un manico finito-stato.

## 80.1 Risultato (24 orbite, onset 251k–313k)
| metrica (r=3 salvo nota) | valore |
|---|---:|
| motivi distinti / eventi (orbita 0, r=3) | 73.959 / 74.416 (~99,4% unici) |
| idem r=4 / r=5 | ancora piu' vicino a 1 |
| scoperta nuovi-motivi ultimo20%/primo20% (mediana orbite) | **1,14** (non satura; semmai sale) |
| pooled r=3: somma-per-orbita / unione | 1.509.525 / 1.478.021 |
| pooled r=3: unione/somma | **0,979** (alfabeti quasi disgiunti) |
| pooled r=3: intersezione su 24 orbite | **19** motivi |
| eta' rivisita-nera profonda (mediana / max tipici) | ~3.000 / fino a ~246.000 |

## 80.2 Interpretazione
- **Contrasto con §78 (il punto vero).** Il **lato-beta** (porta/lock) *e'* finito-stato: il footprint
  co-moving della porta caratterizza il verdetto (44 celle, raggio<=9, P<=15, unknown-free, 786/786).
  Il **lato-alpha** (detrito deep-black) *non* lo e': nessun alfabeto finito di configurazioni locali.
- **Tre falsificazioni in fila, stessa direzione.** deep->W0 (§59, anti-correlato), deficit di consumo
  (§79, nessun deficit), alfabeto finito (§80, illimitato). Il detrito resiste a ogni manico
  finito-stato/strutturale. Coerente con §28.2: la prova deve attraversare la dinamica; nessuna
  scorciatoia statica/finito-stato funziona sul lato-alpha.
- Il footprint co-moving di §78 caratterizza solo l'angolo vincolato in cui vivono gli eventi-porta;
  gli eventi deep-black vivono nel bulk caotico non vincolato.

## 80.3 Caveat
- Il "motivo" e' il campo nero co-moving **pieno** entro raggio r, che include detrito morto accumulato
  (alta entropia) ⇒ l'unicita' per-evento e' in parte attesa. Il test piu' giusto pota il motivo alla
  parte causalmente attiva (celle lette nei prossimi ~104 passi, o la componente connessa attorno alla
  formica). **Ma** il pezzo robusto e' la **disgiunzione tra orbite** (unione/somma 0,979): non si spiega
  con l'entropia del detrito — se esistesse un alfabeto finito universale, le orbite lo condividerebbero
  comunque, e il footprint-porta di §78 include anch'esso detrito eppure satura. Non ci si aspetta che la
  versione potata ribalti; e' l'unico modo in cui potrebbe.
- Una sola passata, 24 orbite finite convergenti (§1-i): non decide l'eterno.

## 80.4 Trappola nuova
- **(o) nessun classificatore finito-stato a raggio fisso sugli eventi deep-black.** L'alfabeto dei
  motivi locali al detrito cresce col territorio (non satura, disgiunto tra orbite). Non riaprire
  approcci checklist / footprint-finito / classe-co-moving **sul lato-alpha** — funzionano solo sul
  lato-beta (porta/lock, §78). Il lato-alpha richiede un argomento dinamico, non un'astrazione finita.

## 80.5 Roadmap
1. (Solo per chiudere il caveat) motivo **potato** alla parte causalmente attiva; aspettativa: negativo,
   per la disgiunzione gia' osservata.
2. Preso atto che il lato-alpha non e' finito-stato: la macchina-beta (§78) **non** si estende al detrito.
   alpha1 / Link 1 richiede un argomento che gestisca complessita' aperiodica genuina (non statico,
   non finito-stato, non a tasso — tutti muri documentati). Il crux resta intatto; §80 ne delimita la
   natura: e' irriducibilmente dinamico.

## 80.6 Inventario file
- `alpha1/deep_motif_saturation.py` (positive gate, parallelo 16 core, ~22 s su 24 orbite)
- `alpha1/deep_motif_saturation_summary.json` (curve di saturazione + eta', per orbita)

## 80.7 Frase di stato dell'arte
*Il lato-porta e' una serratura finita: §78 la legge con 44 celle. Il lato-detrito non e' una serratura
ed e' nessun automa finito: quasi ogni morso profondo accade in una configurazione locale mai vista, e
orbite diverse non condividono quasi nulla. Le tre vie strutturali al detrito sono chiuse (porta, deficit,
alfabeto). Quel che resta di Link 1 e' esattamente cio' che e' irriducibilmente dinamico — e §28.2 lo
diceva: per quello bisogna attraversare la dinamica, non aggirarla con uno stato finito.*
