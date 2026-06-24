# ADDENDUM COMPAT-EVENT/CO-RAGGIUNGIBILITA' — `Φ_compat` event-wise e T3' (§70)

Catena addenda: ... ENDPOINT-MONOTONE-NOGO §68, COMPATIBILITY-POTENTIAL §69,
**COMPAT-EVENT/CO-RAGGIUNGIBILITA' §70**.
Bersaglio di sessione: testare la forma event-wise di `Φ_compat` sui singoli eventi
deep-black e fissare, separatamente, lo schema T3'/co-raggiungibilita' che deve guidare §71.

## 70. Riepilogo in una frase
La monotonia event-wise ingenua di `Φ_compat` e' falsificata: su **600** eventi deep-black
campionati in **24/24** orbite, `h_best` non migliora in **357/600** casi e peggiora
strettamente in **259/600**. Questo uccide "ogni rivisita nera profonda avvicina subito una
porta"; non uccide potenziali con credito/amortizzazione ne' lo schema co-raggiungibile.

## 70.1 Convenzione dell'audit event-wise
Nuovo script:

```
C:\Python\Python310\python.exe alpha1\compat_event_audit.py `
  --limit-orbits 0 `
  --max-events-per-orbit 25 `
  --min-event-t 1040 `
  --max-seconds 300 `
  --horizons 1600 `
  --out-prefix alpha1\compat_event_audit
```

Convenzione:
- evento deep-black a tempo `t` = stato pre-step di `delta4_long_orbits.py`: cella corrente
  nera e fuori dalla memoria viva `r=4`;
- `pre` = stato a `t`, prima di read/turn/flip/move;
- `post` = stato a `t+1`, dopo quel singolo passo;
- `delta_h_best = h_post - h_pre`; positivo = progresso;
- `Φ_compat = 0` se `h_best=L+1`, altrimenti `exp(-h_best/104)`;
- `--min-event-t 1040` evita che il campione dipenda da celle nere iniziali del seed.

Lo script usa le stesse orbite lunghe di §58, rigenera i semi da `rngstate`, valida i morsi con
`compare_bites`, campiona eventi deep-black in modo deterministico/equispaziato, e valuta le 22
porte compatibili tramite la schedule T3' gia' usata in §61/§66/§69.

## 70.2 Numeri
Run definitiva:

- orbite completate: **24/24**;
- eventi deep-black selezionati: **600** (= 25 per orbita);
- orizzonte: `L=1600`;
- runtime: **67.4 s**;
- `pre_clear = 0`, `post_clear = 0`;
- best phase cambiata in **492/600** eventi.

Tabella principale:

| metrica | valore |
|---|---:|
| improve (`delta_h_best>0`) | **243/600** |
| non-improve (`delta_h_best<=0`) | **357/600** |
| decline (`delta_h_best<0`) | **259/600** |
| tie | **98/600** |
| mediana `pre_h_best` | **5** |
| mediana `post_h_best` | **5** |
| media `delta_h_best` | **+0.1517** |
| mediana `delta_h_best` | **0** |
| min/max `delta_h_best` | **-19 / +16** |
| media `delta_phi_compat` | **-0.001406** |

Testimoni forti:

- orbita 12, `t=37070`, `h_best 25 -> 6`, `delta=-19`;
- orbita 16, `t=92515`, `h_best 19 -> 3`, `delta=-16`;
- orbita 7, `t=50188`, `h_best 16 -> 3`, `delta=-13`;
- orbita 20, `t=25113`, `h_best 14 -> 3`, `delta=-11`.

## 70.3 Lettura
Risposta alla domanda affilata di §69: **no**, una rivisita nera profonda non fa sempre scendere
la distanza-prefix dalla compatibilita' con almeno una delle 22 porte, se la distanza e' letta
come `h_best` immediatamente pre/post evento.

La falsificazione e' pulita ma stretta:
- pulita, perche' misura il singolo passo deep-black, non un endpoint gate-to-gate;
- stretta, perche' il campione e' ancora empirico/testimoniale e gli eventi deep-black generici
  non sono gate-lock endpoint;
- informativa, perche' `h_best` resta molto basso (mediana 5) e la best phase cambia in 82% dei
  casi: l'atto locale di ripulire una cella nera puo' riallineare o disallineare la migliore porta.

Quindi la famiglia "scalare immediato" cade. Rimangono solo forme piu' strutturate: credito
amortizzato, ordine parziale/vettoriale, o prova senza potenziale scalare tramite
co-raggiungibilita'.

## 70.4 Schema T3'/co-raggiungibilita'
La parte teorica deve separare tre livelli:

1. non-localita' sintattica di T3';
2. non-localita' su campi raggiungibili da storie finite;
3. conseguenze dinamiche per α1/`Φ_compat`.

Definizioni operative:
- una **porta normalizzata** porta origine e heading nel frame relativo della porta; la fase `g`
  e' parte del certificato;
- `E_g=(e_j)` e' la schedule delle letture esogene T3' per fase `g`, con
  `e_j=(offset_j, rel_j, required_j)`;
- `h_g^L(D)` e' il primo offset `<=L` in cui `D(rel_j) != required_j`, oppure `L+1`;
- il **dato locale** a raggio `R` e' `D|B_R` nel frame della porta, piu' `observed_turn_bit` e
  fase/compatibilita' dichiarata;
- una **storia finita** e' una simulazione finita della formica da configurazione finita, con
  stato letto a un tempo-anchor; il suo detrito `D_H` e' raggiungibile.

Lemma sintattico:
se per ogni `R` esiste in `E_g` una lettura esogena fuori da `B_R`, allora T3' non e' determinato
da nessun raggio locale finito. Si costruiscono due campi sintetici uguali su `B_R`, uguali e
buoni sulle letture prima di `n`, e discordi sulla cella `e_n`. Limite: questo non dice che i due
campi siano detriti raggiungibili.

Coppia discriminante co-raggiungibile a raggio `R`:
una tupla `(H0,H1,g,n)` tale che:
- `H0` e `H1` siano storie finite replayable;
- le due porte normalizzate abbiano lo stesso dato locale su `B_R`;
- si valuti la stessa fase `g` o una fase compatibile dichiarata in entrambi i casi;
- le letture precedenti `e_j`, `j<n`, non distinguano i due campi;
- la cella `e_n` sia fuori da `B_R` e distingua il verdetto;
- `h_g(D_H0)>n` e `h_g(D_H1)=n`, o viceversa.

Claim ammessi:
- un singolo witness empirico prova non-localita' dinamica osservata a quel raggio nel campione;
- una famiglia parametrica per ogni `R` prova che T3' non e' determinata da alcun raggio locale
  sul dominio dei detriti raggiungibili.

Claim non ammessi ora:
- "questo prova α1";
- "nessun `Φ_compat` esiste";
- "la checklist e' dinamicamente non-locale per ogni raggio".

Caveat scala: `R(n)` e' censito a 40; le morti decisive osservate arrivano a offset 1591, anche
se la distanza relativa `L∞` osservata arriva solo a 36. Offset temporale e distanza geometrica
non sono intercambiabili.

## 70.5 Prossimo passo §71
Implementare `alpha1/t3_coreachability_pair_scanner.py`.

Schema minimo:
- input: anchor gia' prodotti da §63/§66/§67 o replay delle 24 orbite;
- per `R in {8,16,24,32,40}` e `L in {208,512,1600}`, hash del patch locale normalizzato;
- bucket per `(R, observed_turn_bit, eval_phase, patch_hash)`;
- cercare collisioni con `h_g` diverso e prima cella discriminante fuori da `B_R`;
- output witness CSV con storie, fase, `R`, `n`, cella relativa, tipo errore, `h0/h1` e verifica replay.

Esito positivo: witness dinamico di non-localita' a raggio `R`.
Esito negativo: nessuna coppia esatta nel campione a `R<=40`; non falsifica il lemma, ma misura
quanto il witness co-raggiungibile e' raro e se serve passare a closure/SAT locale.

## 70.6 File prodotti
- `alpha1/compat_event_audit.py`
- `alpha1/compat_event_audit_summary.json`
- `alpha1/compat_event_audit_summary.csv`
- `alpha1/compat_event_audit_witnesses.csv`
- `alpha1/compat_event_audit_events.csv`
