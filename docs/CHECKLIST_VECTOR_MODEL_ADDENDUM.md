# ADDENDUM CHECKLIST-VECTOR-MODEL — Modello e compressione del vettore (§64)

Catena addenda: ... LOCK-CHECKLIST §61, CHECKLIST-MIXING §62,
CHECKLIST-VECTOR §63, **CHECKLIST-VECTOR-MODEL §64**.
Bersaglio di sessione: stimare quali componenti del vettore esogeno spiegano il verdetto
`OK/KO` e quanto si puo' comprimere la checklist senza perdere la diagonale osservata sul
campione lungo.

## 64. Riepilogo in una frase
Il vettore completo salva ancora una diagonale perfetta: **786/786 fallimenti** hanno almeno
un mismatch e **24/24 OK** non ne hanno. La prima morte e' dominata dagli offset **45-77**
(598/786 prime cattive), ma il sotto-vettore a due periodi copre **774/786** fallimenti:
restano **12** collisioni di frontiera oltre offset 208. Una compressione greedy per offset
mantiene la diagonale con **37 offset**; una compressione phase-conditioned/cella la mantiene
con **66 componenti** su 542 componenti osservate.

## 64.1 Strumento: `alpha1/checklist_vector_model.py`
Lo script non simula nuove orbite. Legge solo i CSV di §63:
- `alpha1/checklist_vector_geometry_attempts.csv`
- `alpha1/checklist_vector_geometry_cells.csv`

Produce:
- `alpha1/checklist_vector_model_summary.json`
- `alpha1/checklist_vector_model_features.csv`
- `alpha1/checklist_vector_model_cover.csv`

Metodo: ogni mismatch del vettore e' un certificato locale di KO. Per una base di feature
(`bad_kind`, bucket di offset, offset esatto, fase, phase-offset, componente
phase-offset-cella) lo script misura copertura dei fallimenti e poi fa un set-cover greedy:
si selezionano componenti che coprono quanti piu' fallimenti ancora scoperti. La predizione e':
`KO` se almeno una componente selezionata e' in mismatch, altrimenti `OK`.

## 64.2 Validazione operativa
Prima dell'analisi sono stati rilanciati i self-test obbligatori:
- `C:\Python\Python310\python.exe code\window_automaton.py --selftest`: verde.
- `C:\Python\Python310\python.exe code\product_automaton.py --selftest`: verde.
- `alpha1\alpha1_engine.exe dump 200000`: griglia vuota -> **9977**.
- `alpha1\alpha1_engine.exe dump 200000` con `alpha1\seed_7_-7.txt`: **106258**.
- simulazione diretta della coda highway della griglia vuota: fresh-white **22/104**.

Check dello script:
- `C:\Python\Python310\python.exe alpha1\checklist_vector_model.py`
- `C:\Python\Python310\python.exe -m py_compile alpha1\checklist_vector_model.py`

## 64.3 Diagonale del vettore

| quantita' | valore |
|---|---:|
| tentativi porta | 810 |
| OK | 24 |
| fallimenti | 786 |
| mismatch cells | 5806 |
| fallimenti senza mismatch nel vettore esteso | **0** |
| OK con mismatch | **0** |

Quindi il vettore salvato in §63 non perde il segnale del verdetto: il full-vector e'
diagonale sul campione lungo.

Il sotto-vettore entro due periodi non e' esattamente sufficiente:

| vettore fino a offset 207 | valore |
|---|---:|
| fallimenti coperti | 774 |
| fallimenti mancati | **12** |
| copertura | **0.9847** |

I 12 mancati sono tutti `frontier_black_collision` oltre due periodi, con offset:
268, 273, 279, 298, 373, 488, 488, 492, 685, 799, 1533, 1591.
Lettura: due periodi quasi chiudono il campione, ma non bastano per la diagonale esatta.

## 64.4 Dove cade la prima cattiva

Prime celle cattive per bucket:

| bucket offset | prime cattive |
|---|---:|
| 00-44 early | 77 |
| **45-77 mid-gate** | **598** |
| 78-97 late-body | 29 |
| **98-99 deep-gate** | **50** |
| 100-103 tail | 14 |
| 104-207 period2 | 6 |
| 208+ | 12 |

Top offset di prima morte:
45:137, 46:78, 71:58, 77:56, 47:45, 76:32, 99:26, 44:26, 98:24, 43:22.

Quindi il collo dominante non e' piu' solo 98/99: la fascia 45-77 decide la maggioranza delle
morti. Gli offset 98/99 restano pero' necessari: rimuovere quel bucket lascia **37** fallimenti
non coperti.

## 64.5 Mismatch complessivi del vettore

Mismatch cells per bucket:

| bucket offset | mismatch cells |
|---|---:|
| 00-44 early | 91 |
| **45-77 mid-gate** | **2797** |
| 78-97 late-body | 867 |
| 98-99 deep-gate | 415 |
| 100-103 tail | 217 |
| **104-207 period2** | **1407** |
| 208+ | 12 |

Top offset per numero totale di mismatch:
77:300, 99:290, 71:222, 76:196, 45:179, 80:165, 61:157, 46:134, 50:132, 98:125.

La seconda osservazione e' importante: la prima cella decide la morte, ma il vettore fallito
contiene spesso altri mismatch tardivi, soprattutto nel secondo periodo. Questo rafforza §63:
non stiamo guardando near-OK microscopici, ma tentativi gia' incompatibili in piu' coordinate.

## 64.6 Compressione greedy

| base feature | universo osservato | componenti selezionate | diagonale preservata |
|---|---:|---:|---:|
| bad_kind | 2 | 2 | si |
| bucket offset | 7 | 6 | si |
| offset esatto | 163 | **37** | si |
| fase | 17 | 17 | si |
| phase-offset | 542 | **66** | si |
| phase-offset-kind | 542 | **66** | si |
| componente phase-offset-cella | 542 | **66** | si |

La riga `bad_kind` e' solo un sanity check tautologico: entrambi i tipi di errore coprono tutto.
Le righe utili sono:
- **offset esatto:** 37 offset bastano sul campione lungo;
- **phase-offset / componente:** 66 componenti phase-conditioned bastano, e in questo dataset
  `phase-offset` identifica gia' la cella relativa e il colore richiesto.

Primi passi della copertura per offset:
77 copre 300 fallimenti, 71 altri 143, 99 altri 92, 74 altri 60, 101 altri 36, 76 altri 29.

Primi componenti phase-conditioned:
`0|99|-2|1|1` copre 183 fallimenti, `0|77|-5|0|1` 164,
`0|80|-4|0|1` 149, `0|98|-3|1|1` 125, `103|99|0|-3|1` 107.

## 64.7 Ablazione per bucket

Rimuovendo un bucket alla volta e lasciando tutti gli altri:

| bucket rimosso | fallimenti persi |
|---|---:|
| 00-44 early | 0 |
| 100-103 tail | 13 |
| 104-207 period2 | 6 |
| 208+ | 12 |
| **45-77 mid-gate** | **130** |
| 78-97 late-body | 13 |
| **98-99 deep-gate** | **37** |

La fascia 45-77 e' il blocco piu' informativo e non ridondante. Il bucket 98-99 e'
piu' piccolo ma ancora non eliminabile. Il bucket 00-44 e' assorbito dagli altri mismatch:
come prima morte esiste, ma non serve alla diagnosi KO se si guarda il vettore piu' largo.

## 64.8 Lettura strategica
Il modello vettoriale comprime T3' in modo empiricamente forte ma non ancora teorico.
Il quadro aggiornato e':

```
full vector -> diagonale esatta sul campione lungo
due periodi -> 98.5% dei KO, ma non tutti
45-77 -> massa dominante della prima morte
98-99 -> collo profondo ancora necessario
phase-conditioned 66 componenti -> prima compressione concreta del vettore
```

Questo sposta la domanda beta in una forma piu' precisa: non basta dimostrare che una singola
dogana critica viene ricampionata. Serve controllare un sotto-vettore di decine di componenti,
con massa dominante nelle prime dogane 45-77 e una coda profonda/frontier oltre due periodi.

## 64.9 Caveat
- Campione sempre selezionato per onset alto: evidenza su transienti lunghi, non misura baseline.
- Il set-cover e' descrittivo, non un classificatore validato out-of-sample; con 24 OK non ha
  senso vendere AUC o regressioni.
- Le componenti oltre offset 208 entrano perche' §63 salva fino alla morte. Se si impone un
  vettore rigidamente a due periodi, la diagonale si perde su 12 fallimenti.
- La compressione `phase-offset` e' campione-specifica: va ritestata sul campione baseline
  prima di trattarla come oggetto universale.

## 64.10 Prossima roadmap
1. **Campione baseline non condizionato.** Replicare §61-§64 su molte orbite senza filtro onset
   alto, con cap piu' basso, per testare se i 66 componenti restano diagonali.
2. **Compressione stabile.** Intersecare i sotto-vettori greedy fra campione lungo e baseline:
   cercare componenti invarianti per fase/offset, non idiosincrasie dei 24 transienti.
3. **Modello hazard a tre stadi.** Collegare `fresh-bite -> lock`, `lock -> sub-vettore KO/OK`,
   `sub-vettore -> ingresso`, senza riaprire predictor scalari gia' falsificati.

## 64.11 Inventario file
- `alpha1/checklist_vector_model.py`
- `alpha1/checklist_vector_model_summary.json`
- `alpha1/checklist_vector_model_features.csv`
- `alpha1/checklist_vector_model_cover.csv`

## 64.12 Frase di stato dell'arte
*La checklist si comprime, ma non collassa a una dogana sola. Le prime porte 45-77 fanno la
maggior parte del lavoro, 98-99 restano il collo profondo, e dodici fallimenti ricordano che
la frontiera puo' mordere oltre due periodi. Il vettore non e' enorme, ma e' davvero vettoriale.*
