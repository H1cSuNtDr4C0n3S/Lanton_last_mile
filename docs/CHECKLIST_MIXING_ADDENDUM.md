# ADDENDUM CHECKLIST-MIXING — Hazard e ricampionamento della checklist (§62)

Catena addenda: ... DEBT-LOCK 2D §60, LOCK-CHECKLIST §61,
**CHECKLIST-MIXING §62**.
Bersaglio di sessione: dopo aver verificato che T3' decide esattamente il verdetto locale,
misurare se i tentativi porta mostrano una protezione banale della checklist: riuso della
cella critica, memoria del tipo di errore, parita' o fasi bloccate.

## 62. Riepilogo in una frase
Deduplicando i lock `D>=80` gia' presenti come `D>=40`, le 24 orbite lunghe danno **810
tentativi porta unici**, con **24 checklist OK** e **786 fallimenti**. La cella critica assoluta
si riusa solo **1 volta su 762 coppie consecutive fallite** e **1 volta su 12.945 coppie
intra-orbita**. Il tipo di fallimento e' quasi senza memoria. Questo rafforza il quadro
"porta migrante = ricampionamento locale", senza trasformarlo ancora in un lemma β.

## 62.1 Strumento: `alpha1/checklist_mixing.py`
Lo script lavora solo sui CSV di §61:
- legge `alpha1/lock_checklist_probe_rows.csv`;
- tiene un solo tentativo per `(idx,start,phase,kind)`, preferendo la riga `D>=80` quando e'
  duplicata da `D>=40`;
- costruisce sequenze ordinate di gate-attempt per orbita, includendo l'onset vero come
  checklist OK;
- misura hazard per fase, streak di fallimenti, transizioni fra errori consecutivi, parita'
  `t mod 2/4/8/16`, e riuso della cella critica assoluta.

Output:
- `alpha1/checklist_mixing_attempts.csv`
- `alpha1/checklist_mixing_transitions.csv`
- `alpha1/checklist_mixing_phase.csv`
- `alpha1/checklist_mixing_summary.json`

Runtime: sotto 1 s. Nessuna simulazione.

## 62.2 Hazard grezzo della checklist

| quantita' | valore |
|---|---:|
| tentativi porta unici | 810 |
| checklist OK | 24 |
| checklist KO | 786 |
| hazard grezzo OK | **0.0296** |

Per soglia dopo dedup:

| soglia massima | tentativi |
|---:|---:|
| entry/onset | 24 |
| D>=40 | 681 |
| D>=80 | 105 |

Fallimenti prima dell'ingresso per orbita:
- min 24, q25 28, mediana **31.5**, media **32.75**, q75 35.75, max **50**;
- varianza popolazione **38.94**.

Se si prendesse il tasso globale `p=24/810`, una geometrica iid avrebbe stessa media circa
32.75 ma varianza ~1105. Qui la dispersione e' molto piu' stretta. Lettura prudente: non ci
sono "run maledette" nel campione, ma il campione e' condizionato a onset alto e contiene
esattamente un successo finale per orbita, quindi non e' un test iid puro.

## 62.3 Fasi porta

| fase | tentativi | OK | OK rate |
|---:|---:|---:|---:|
| 0 | 314 | 10 | 0.0318 |
| 103 | 128 | 3 | 0.0234 |
| 30 | 83 | 0 | 0.0000 |
| 24 | 75 | 2 | 0.0267 |
| 102 | 49 | 2 | 0.0408 |
| 31 | 45 | 0 | 0.0000 |
| 25 | 27 | 2 | 0.0741 |
| 100 | 26 | 2 | 0.0769 |
| 99 | 22 | 1 | 0.0455 |

Le fasi rare 97/98 hanno rate apparente alto, ma con n piccolo. La cosa robusta e' che il
ranking si fattorizza: alcune fasi producono molti lock (0, 103, 30, 24), ma il successo dipende
ancora dalla checklist locale.

## 62.4 Tipo di errore e transizioni
Fallimenti deduplicati:

| tipo | conteggio |
|---|---:|
| frontier_black_collision | 419 |
| missing_black | 367 |

Transizioni fra tentativi consecutivi:

| transizione | conteggio |
|---|---:|
| frontier -> frontier | 219 |
| frontier -> missing | 190 |
| frontier -> OK | 10 |
| missing -> frontier | 192 |
| missing -> missing | 161 |
| missing -> OK | 14 |

Il dato piu' pulito: `P(next frontier | prev frontier)=0.5227` e
`P(next frontier | prev missing)=0.5232`. Il tipo di errore precedente quasi non predice il
tipo di errore successivo. Anche `P(next OK)` resta nello stesso ordine: 0.0239 dopo frontier,
0.0381 dopo missing.

## 62.5 Riuso della cella critica

| misura | valore |
|---|---:|
| coppie consecutive fallite | 762 |
| stessa cella critica consecutiva | **1** |
| coppie fallite intra-orbita | 12.945 |
| stessa cella critica intra-orbita | **1** |
| distanza L1 mediana fra celle critiche consecutive | **42** |
| q25 / q75 L1 | 18 / 83 |
| max L1 | 215 |

Questo e' il segnale strutturale piu' importante di §62: il tentativo successivo non torna
sullo stesso interruttore. Ogni gate-lock legge una zona critica quasi sempre nuova del campo
di detriti. Una protezione eterna dovrebbe quindi avvelenare molte posizioni future diverse,
non conservare una singola cella o una singola dogana.

## 62.6 Parita'
Screening leggero:
- `t mod 2`: OK bilanciati 12/12;
- `t mod 4`: OK 7/7/5/5;
- `t mod 16`: OK in 13 residui su 16.

Con 24 successi totali non e' un test potente; pero' non compare una classe di parita' semplice
che contenga tutti i successi o tutti i fallimenti. Questo e' coerente con la caccia
all'anti-teorema precedente.

## 62.7 Lettura strategica
La catena aggiornata:

```
fresh-bite -> lock
lock -> porta profonda
porta -> checklist T3'
checklist -> verdetto esatto
tentativi successivi -> quasi nuova cella critica
```

§62 non chiude β. Sposta pero' l'anti-teorema in una forma piu' netta: una cospirazione eterna
non puo' essere locale-banale. Non basta tenere sbagliata una cella, un tipo di dogana o una
classe di parita'. Deve essere un vincolo globale sul campo di detriti che anticipa una sequenza
di porte mobili.

## 62.8 Caveat
- Il campione e' quello delle 24 orbite a onset alto: utile per stressare i transienti lunghi,
  non rappresentativo della misura baseline.
- Ogni orbita contiene per costruzione un solo successo finale; il tasso 0.0296 e' una hazard
  empirica sui tentativi osservati, non una stima universale.
- La sonda usa solo la prima cella cattiva, non l'intero vettore checklist.
- Mancano origine/heading del lock nel CSV §61; per un test geometrico piu' fine serve salvare
  anche porta assoluta, heading e vettore completo delle celle esogene.

## 62.9 Prossima roadmap
1. **Checklist vector (§63).** Estendere il valutatore per salvare il vettore completo delle
   celle esogene principali, non solo la prima cattiva.
2. **Geometria porta.** Salvare origine/heading dei lock e misurare distanza fra porte,
   non solo fra celle critiche.
3. **Campione piu' ampio non condizionato.** Ripetere su molte orbite baseline, senza filtro
   onset alto, con cap basso ma molti tentativi.

## 62.10 Inventario file
- `alpha1/checklist_mixing.py`
- `alpha1/checklist_mixing_attempts.csv`
- `alpha1/checklist_mixing_transitions.csv`
- `alpha1/checklist_mixing_phase.csv`
- `alpha1/checklist_mixing_summary.json`

## 62.11 Frase di stato dell'arte
*La checklist non resta chiusa appoggiandosi a una cella o a una parita'. La porta si sposta,
la cella critica cambia, e il tipo di errore viene quasi ricampionato.*
