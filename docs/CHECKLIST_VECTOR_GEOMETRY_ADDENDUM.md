# ADDENDUM CHECKLIST-VECTOR — Vettore esogeno e geometria della porta (§63)

Catena addenda: ... LOCK-CHECKLIST §61, CHECKLIST-MIXING §62,
**CHECKLIST-VECTOR §63**.
Bersaglio di sessione: salvare origine/heading della porta e non solo la prima cella cattiva,
ma il vettore delle letture esogene principali al momento del lock.

## 63. Riepilogo in una frase
Il vettore checklist conferma e rafforza §62: su **810 tentativi porta unici** abbiamo
**57.177 letture esogene** registrate; in **786/786** fallimenti la prima cella cattiva e'
ancora esattamente la morte, ma gia' entro due periodi il vettore contiene una mediana di
**6 mismatch** per tentativo fallito. Geometricamente, due porte consecutive non riusano mai
la stessa origine (**0/786**) e distano L1 mediana **43**: il ricampionamento non e' solo
della cella critica, e' della porta stessa.

## 63.1 Strumento: `alpha1/checklist_vector_geometry.py`
Lo script:
- rigenera le 24 orbite da `rngstate`;
- estrae lock W0-like per-allineamento come §61;
- deduplica i duplicati `D>=80`/`D>=40` come §62;
- salva per ogni gate-attempt: origine assoluta, heading, fase, profondita', prima cella
  cattiva, conteggi del vettore;
- salva ogni lettura esogena fino ad almeno `vector_horizon=208` e comunque fino alla morte
  del lock; per gli onset veri usa `entry_horizon=1248`;
- salva la geometria fra tentativi consecutivi.

Output:
- `alpha1/checklist_vector_geometry_attempts.csv`
- `alpha1/checklist_vector_geometry_cells.csv`
- `alpha1/checklist_vector_geometry_geometry.csv`
- `alpha1/checklist_vector_geometry_summary.json`

Runtime completo: **68.6 s**. Nessuna search di onset.

## 63.2 Risultato aggregato

| quantita' | valore |
|---|---:|
| tentativi porta unici | 810 |
| entry/onset OK | 24 |
| fallimenti | 786 |
| letture esogene salvate | 57.177 |
| mismatch esogeni salvati | 5.806 |
| fallimenti con prima cattiva != morte | **0** |

La diagonale locale di §61 resta intatta anche dopo aver salvato il vettore completo.

## 63.3 Densita' del vettore checklist
Sui tentativi falliti, contando le letture fino ad almeno due periodi:

| mismatch nel vettore | valore |
|---|---:|
| min | 1 |
| q25 | 3 |
| mediana | **6** |
| q75 | 10 |
| max | 29 |
| media | 7.39 |

Interpretazione: il primo errore decide il verdetto, ma il lock fallito non e' "quasi OK"
in senso globale. Nella finestra di due periodi ci sono spesso diversi vincoli gia' sbagliati.
Questo suggerisce che per modellare `P(checklist OK | lock)` serve davvero il vettore, non solo
la prima cella cattiva.

## 63.4 Geometria della porta

| misura fra tentativi consecutivi | valore |
|---|---:|
| stessa origine porta | **0/786** |
| L1 origine: min | 1 |
| L1 origine: q25 | 17 |
| L1 origine: mediana | **43** |
| L1 origine: q75 | 84.25 |
| L1 origine: max | 222 |

La cella critica replica §62:

| misura celle critiche consecutive | valore |
|---|---:|
| stessa cella critica | **1/762** |
| L1 critica mediana | **42** |
| q25 / q75 | 18 / 83 |
| max | 215 |

Heading delta fra porte consecutive:
`0:218`, `1:215`, `2:149`, `3:204`.
Non c'e' un heading bloccato; i quattro casi sono tutti popolati.

## 63.5 Lettura strategica
La porta mobile ora e' misurata direttamente, non inferita dalla cella critica:

```
gate-attempt n     = origine A, heading h, vettore E_A
gate-attempt n + 1 = origine B, heading h', vettore E_B
```

Con `A != B` sempre nel campione e distanza mediana 43, una protezione eterna della checklist
non puo' essere una memoria locale riusata. Deve coordinare un campo di detriti su una sequenza
di porte distinte e su vettori con piu' celle sbagliate.

Questo e' buono per β in senso falsificazionista: le scappatoie locali semplici continuano a
morire. Non e' ancora una prova: manca un argomento che trasformi "porta mobile + vettore
ricampionato" in impossibilita' di evitamento eterno.

## 63.6 Caveat
- Il vettore e' tagliato a `max(208, death_offset)` per i fallimenti; non e' l'intero schedule
  infinito T3'. Per gli onset il controllo resta a `1248`.
- Il campione e' sempre selezionato per onset alto.
- Le celle del vettore oltre la prima morte sono lette read-only nello stato al lock: sono una
  firma della checklist, non una traiettoria reale dopo il deragliamento.

## 63.7 Prossima roadmap
1. **Modello vettoriale (§64).** Stimare quali componenti del vettore spiegano `OK`:
   conteggi missing/frontier, prime dogane, offset 45-77 vs 98-99, phase-conditioned.
2. **Campione baseline.** Replicare §61-§63 su molte orbite non condizionate a onset alto,
   con cap piu' basso ma molti tentativi.
3. **Compressione del vettore.** Identificare un sotto-vettore minimo che predice il verdetto
   con la stessa diagonale nel campione lungo.

## 63.8 Inventario file
- `alpha1/checklist_vector_geometry.py`
- `alpha1/checklist_vector_geometry_attempts.csv`
- `alpha1/checklist_vector_geometry_cells.csv`
- `alpha1/checklist_vector_geometry_geometry.csv`
- `alpha1/checklist_vector_geometry_summary.json`

## 63.9 Frase di stato dell'arte
*Non cambia solo la cella sbagliata: cambia la porta. Il fallimento e' locale nel verdetto,
ma la sua ripetizione richiede una cospirazione spaziale su porte distinte.*
