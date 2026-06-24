# ADDENDUM LOCK-CHECKLIST — T3' morde sui lock lunghi (§61)

Catena addenda: ... DELTA4-BETA §58, DEBT-LOCK §59, DEBT-LOCK 2D §60,
**LOCK-CHECKLIST §61**.
Bersaglio di sessione: spostare il test dal predittore di lock al verdetto locale T3':
dato un lock W0-like profondo, la morte/entrata e' gia' scritta nello stato delle letture
esogene?

## 61. Riepilogo in una frase
Sulle 24 orbite lunghe, **ogni gate-lock pre-onset muore esattamente alla prima lettura
esogena cattiva della checklist T3'**: 891/891 esatti. I 24 onset veri passano la checklist
nel controllo positivo. Quindi il passaggio `lock -> checklist -> verdetto` e' confermato
sul campione lungo; il problema residuo non e' piu' "un lock simbolico decide?", ma
"la successione delle checklist puo' restare sbagliata per sempre?".

## 61.1 Strumento: `alpha1/lock_checklist_probe.py`
Lo script:
- rigenera le 24 orbite da `rngstate` in `alpha1/dumps_all.txt`;
- estrae lock W0-like **per-allineamento** e left-maximal, evitando il tie-breaking pooled
  gia' segnato come trappola in ALPHA §23;
- usa soglie `D>=40` e `D>=80`;
- separa fasi porta `Phi_ent` dalle fasi mute usando la tabella `r(k)` di α2;
- ricostruisce la checklist T3' direttamente da `W0`: ogni prima visita della cavalcata e'
  esogena e deve avere al lock il colore richiesto dalla svolta corrispondente;
- valuta lo stato read-only al tempo del lock e confronta la prima lettura esogena cattiva
  con la morte reale del lock.

Output:
- `alpha1/lock_checklist_probe_rows.csv`
- `alpha1/lock_checklist_probe_summary.json`

Runtime completo: **68.1 s**, nessuna search di onset.

## 61.2 Risultato aggregato

| criterio | valore |
|---|---:|
| lock pre-onset valutati | 3303 |
| gate-lock pre-onset | 891 |
| gate-lock con morte = prima checklist cattiva | **891/891** |
| onset veri come controlli positivi | **24/24** |

Per soglia:

| soglia | lock totali | gate-lock |
|---:|---:|---:|
| D>=40 | 3191 | 786 |
| D>=80 | 112 | 105 |

I lock profondi sono quasi tutti alle porte: a `D>=80`, 105/112 sono gate-lock.

## 61.3 Stratificazione della morte
Sui gate-lock, la prima lettura cattiva e' bilanciata:

| tipo di fallimento | gate-lock |
|---|---:|
| missing_black | 447 |
| frontier_black_collision | 444 |

Lettura: ci sono due modi quasi simmetrici di fallire la checklist:
1. manca una cella nera richiesta da una dogana/cella di corpo;
2. una cella che doveva essere bianca e' gia' nera, cioe' collisione con detrito/frontiera.

Top fasi porta sui gate-lock:
`0:356`, `103:138`, `30:86`, `24:76`, `102:55`, `31:45`, `100:32`, `99:32`,
`25:25`, poi code piu' rare.

Top offset di morte/checklist:
`45:137`, `46:78`, `71:58`, `77:56`, `99:52`, `98:48`, `47:45`, `76:32`.
Gli offset 98/99 restano sportelli profondi, ma il collo di bottiglia non e' solo quello:
molte morti arrivano gia' nella fascia 45-77.

## 61.4 Non-gate lock
I lock non-porta sono 2412:
- `mute_early_death`: 2393;
- `mute_threshold_death`: 19.

Questo e' coerente con α2: fuori dalle porte il lock simbolico non e' un candidato beta; e'
un fattore W0 che muore prima o al rientro della soglia. La checklist T3' e' il discrimine
solo una volta localizzati alla porta.

## 61.5 Lettura strategica
La catena empirica aggiornata diventa:

```
fresh-bite alto -> piu' lock simbolici
lock profondo -> localizzazione sempre piu' porta
gate-lock -> verdetto T3' read-only
checklist OK -> ingresso
checklist KO -> morte esatta alla prima cella cattiva
```

§61 non prova β: tutte queste orbite sono finite e convergono. Pero' chiude il dubbio operativo
sul ponte locale. Non serve cercare un altro proxy di `D(t)`: sui lock porta il verdetto e'
gia' la checklist.

La domanda rimasta e' quindi la β vera: la successione degli stati-checklist ai tempi di lock
puo' evitare in eterno l'evento OK, oppure viene ricampionata abbastanza da rendere impossibile
una cospirazione globale?

## 61.6 Caveat
- Il valutatore ricostruisce E(k) da `W0` invece di riusare i vecchi `gate_checklists.pkl`,
  non presenti in questo workspace. Questo e' intenzionale e indipendente dai vecchi pickle.
- Il controllo positivo degli onset veri e' finito (`entry_horizon=1248`), non una verifica
  infinita; serve come check di frame e colori, non come nuova dimostrazione di T3'.
- I lock sono estratti per-allineamento left-maximal, ma il campione resta quello delle 24
  orbite selezionate per onset alto.

## 61.7 Prossima roadmap
1. **Checklist hazard (§62).** Modellare `P(checklist OK | lock)` in funzione di fase, offset,
   deep/bite pre-lock, tempo e indice di lock.
2. **Mixing della checklist.** Guardare transizioni fra lock consecutivi: stato congiunto,
   parita' `t mod 8/16`, posizione porta, riuso della cella assoluta critica.
3. **Porte rare/fantasma.** Misurare per fase il ranking `P(lock porta)` e `P(checklist OK | lock)`.

## 61.8 Inventario file
- `alpha1/lock_checklist_probe.py`
- `alpha1/lock_checklist_probe_rows.csv`
- `alpha1/lock_checklist_probe_summary.json`

## 61.9 Frase di stato dell'arte
*Il lock bussa, la checklist decide. Sulle orbite lunghe non c'e' rumore in mezzo: quando una
porta fallisce, fallisce esattamente alla prima cella esogena sbagliata.*
