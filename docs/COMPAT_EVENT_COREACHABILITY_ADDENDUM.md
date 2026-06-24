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

---

# §71. Scanner di coppie co-raggiungibili T3'

## 71. Riepilogo in una frase
Il witness dinamico cercato esiste gia' nel campione raggiunto a raggio locale **R=8**:
due storie finite replayable della stessa orbita hanno lo stesso patch normalizzato `17x17`,
stesso bit osservato e stessa fase T3' compatibile, ma divergono a offset **494** su una cella
relativa **(15,13)** fuori da `B_8`. Questa e' lettura **di esistenza/non-vacuita'** dello
schema co-raggiungibile, non un argomento di potenziale uniforme; a `R=16`, sulla stessa griglia
densa, l'assenza di collisioni esatte e' attesa per sparsita' del campione nello spazio dei
patch `33x33`.

## 71.1 Strumento
Nuovo script:

```
C:\Python\Python310\python.exe alpha1\t3_coreachability_pair_scanner.py `
  --limit-orbits 0 `
  --max-seconds 300 `
  --include-grid `
  --grid-stride 520 `
  --radii 8 `
  --horizons 208,512,1600 `
  --out-prefix alpha1\t3_coreachability_pair_scanner_grid520_r8
```

Definizione operativa:
- anchor raggiungibili = gate/entry deduplicati come §63 piu' eventuali anchor griglia da replay;
- patch locale = bitset completo di `D|B_R` nel frame normalizzato della porta/anchor;
- bucket = `(R, horizon, observed_turn_bit, eval_phase, patch_bytes)`;
- `eval_phase` default = ogni fase gate compatibile col primo bit osservato;
- `h_g^L = L+1` se nessun difetto entro `L`, altrimenti primo offset cattivo;
- witness accettato solo se due record nello stesso bucket hanno `h_g` diverso e la prima
  lettura discriminante del record precoce ha `L∞ > R`.

La verifica replay e' interna: stesso `patch_bytes`, stesso `observed_turn_bit`, stessa fase,
`late.h > n`, e `disc_linf > R`.

## 71.2 Run e risultati

### Gate/entry baseline, raggio piano §71
Comando:

```
C:\Python\Python310\python.exe alpha1\t3_coreachability_pair_scanner.py `
  --limit-orbits 0 `
  --max-seconds 300 `
  --out-prefix alpha1\t3_coreachability_pair_scanner
```

Risultato:
- **24/24** orbite;
- **810** anchor gate/entry;
- **133650** valutazioni;
- **133485** bucket;
- collisioni esatte solo a `R=8`: **22** bucket collidenti per ogni `L`;
- bucket `h`-divergenti: **0**.

Lettura: sui soli gate/entry il campione e' troppo sparso; nessuna coppia discriminante esatta.

### Griglia stride 1040, sanity a R=4
Comando:

```
C:\Python\Python310\python.exe alpha1\t3_coreachability_pair_scanner.py `
  --limit-orbits 0 --max-seconds 300 --include-grid `
  --radii 4 --horizons 208,512,1600 `
  --out-prefix alpha1\t3_coreachability_pair_scanner_grid_r4
```

Risultato:
- **7109** anchor, **234597** valutazioni;
- **253** bucket collidenti per ogni `L`;
- **5** bucket `h`-divergenti per ogni `L`;
- **15** witness registrati dopo deduplica a un witness per bucket/orizzonte.

Lettura: il metodo trova coppie dinamiche quando il raggio locale e' piccolo. Questo e' sanity
check, non il target §71 principale.

### Griglia stride 520, primo raggio target R=8
Comando finale positivo:

```
C:\Python\Python310\python.exe alpha1\t3_coreachability_pair_scanner.py `
  --limit-orbits 0 --max-seconds 300 --include-grid --grid-stride 520 `
  --radii 8 --horizons 208,512,1600 `
  --out-prefix alpha1\t3_coreachability_pair_scanner_grid520_r8
```

Risultato:
- **24/24** orbite;
- **13394** anchor;
- **442002** valutazioni;
- **441771** bucket;
- **44** bucket collidenti per ogni `L`;
- bucket `h`-divergenti: `L=208`: **0**, `L=512`: **1**, `L=1600`: **1**;
- witness registrati: **2** (stesso bucket, due orizzonti).

Witness:

| campo | valore |
|---|---:|
| `R` | **8** |
| `eval_phase` | **98** |
| `observed_turn_bit` | **0** |
| patch | `1e838dafb7a51b780addaa3772ef0181` |
| anchor tardi | orbita **5**, grid **117**, `t=60840`, origine `(48,-36)`, heading `2` |
| anchor presto | orbita **5**, grid **116**, `t=60320`, origine `(58,-26)`, heading `2` |
| discriminante | offset **494**, rel **(15,13)**, `L1=28`, `L∞=15` |
| requisito T3' | bianca (`required_black=0`) |
| caso cattivo | `frontier_black_collision` (`actual_black=1`) |
| `h_g^512` | **494 vs 513** |
| `h_g^1600` | **494 vs 1014** |

Questa e' una coppia co-raggiungibile empirica: le due storie finite sono due prefissi della
stessa orbita, replayabili da `rngstate=16489936061346709332`; sono localmente indistinguibili
su `B_8`, ma T3' legge una cella fuori raggio che cambia il verdetto.

L'asimmetria `494 vs 513/1014` e' attesa: la relazione di co-raggiungibilita' richiede stesso
dato locale e diverso verdetto T3', non simmetria del futuro fuori finestra. A `L=512`, `513`
e' solo il sentinel `L+1` ("nessun difetto entro l'orizzonte") per il secondo anchor.

### Griglia stride 520, R=16: controllo di sparsita'
Comando:

```
C:\Python\Python310\python.exe alpha1\t3_coreachability_pair_scanner.py `
  --limit-orbits 0 --max-seconds 300 --include-grid --grid-stride 520 `
  --radii 16 --horizons 208,512,1600 `
  --out-prefix alpha1\t3_coreachability_pair_scanner_grid520_r16
```

Risultato:
- **13394** anchor;
- **442002** valutazioni;
- **442002** bucket;
- collisioni esatte: **0**.

Lettura: sulla stessa griglia, non c'e' nessuna coppia con patch `33x33` identico. Questo **non**
ha peso dinamico forte: lo spazio dei patch a `R=16` e' enorme rispetto a 442002 valutazioni, quindi
zero collisioni e' il baseline combinatorio naturale. L'unica conclusione lecita e' operativa:
non serve rilanciare `R=24,32,40` sugli stessi anchor, perche' una collisione a raggio piu' grande
implicherebbe gia' collisione a `R=16`.

## 71.3 Interpretazione
Claim lecito:
- esiste almeno un witness dinamico co-raggiungibile a `R=8` nel campione lungo;
- la non-localita' non e' solo sintattica: le due configurazioni sono detriti raggiunti da
  storie finite della formica;
- il discriminante non e' vicino: `L∞=15 > 8`, offset temporale `494`.

Claim non lecito:
- non prova che T3' sia non-locale su ogni raggio;
- non prova α1;
- non esclude potenziali con credito/amortizzazione;
- non dice che la griglia stride 520 sia esaustiva.
- non legge l'assenza di collisioni a `R=16` come confine strutturale: e' principalmente
  effetto della collisione esatta in uno spazio di patch enorme.

Punto tecnico importante: l'equivalenza per patch completo e' radius-fragile per costruzione.
Piu' bit locali si richiedono, meno collisioni esatte sopravvivono. Se si vuole usare
co-raggiungibilita' per sostenere un potenziale/amortizzazione, l'equivalenza giusta probabilmente
non e' la collisione esatta grezza ma una nozione approssimata/quoziente, oppure una closure
locale generativa/SAT che costruisca estensioni esterne diverse di uno stesso dato locale.

## 71.4 Prossimi passi
1. Validare il witness `R=8` con un piccolo replay mirato che ristampi patch, bit e letture T3'
   fino a offset 494.
2. Esplicitare il bivio: lettura "esistenza" (gia' soddisfatta a `R=8`) vs lettura "potenziale"
   (non supportata dal witness radius-fragile).
3. Cercare famiglie aumentando la densita' degli anchor intorno ai bucket promettenti, non
   uniformemente su tutta l'orbita.
4. Formulare una closure/SAT locale: stesso dato locale raggiungibile a raggio `R`, estensioni
   esterne diverse, vincoli di alternanza/replay finito.
5. Separare in modo netto tre livelli nel testo finale: witness empirico `R=8`, schema per
   famiglia parametrica, e implicazioni eventuali per α1.

## 71.5 File prodotti
- `alpha1/t3_coreachability_pair_scanner.py`
- `alpha1/t3_coreachability_pair_scanner_summary.json`
- `alpha1/t3_coreachability_pair_scanner_buckets.csv`
- `alpha1/t3_coreachability_pair_scanner_orbits.csv`
- `alpha1/t3_coreachability_pair_scanner_witnesses.csv`
- `alpha1/t3_coreachability_pair_scanner_grid_r4_summary.json`
- `alpha1/t3_coreachability_pair_scanner_grid_r4_buckets.csv`
- `alpha1/t3_coreachability_pair_scanner_grid_r4_orbits.csv`
- `alpha1/t3_coreachability_pair_scanner_grid_r4_witnesses.csv`
- `alpha1/t3_coreachability_pair_scanner_grid520_r8_summary.json`
- `alpha1/t3_coreachability_pair_scanner_grid520_r8_buckets.csv`
- `alpha1/t3_coreachability_pair_scanner_grid520_r8_orbits.csv`
- `alpha1/t3_coreachability_pair_scanner_grid520_r8_witnesses.csv`
- `alpha1/t3_coreachability_pair_scanner_grid520_r16_summary.json`
- `alpha1/t3_coreachability_pair_scanner_grid520_r16_buckets.csv`
- `alpha1/t3_coreachability_pair_scanner_grid520_r16_orbits.csv`
- `alpha1/t3_coreachability_pair_scanner_grid520_r16_witnesses.csv`

# §72. Profilo `L∞` del discriminante T3' vs profondita' lock

## 72.1 Motivazione

Prima di costruire un grafo dei debiti (`door_debt_graph.py`) bisogna verificare il presupposto
del "lemma della dogana ricorrente": servono **finitamente** molte classi di debito. La prima
misura grezza sembrava far crescere il discriminante T3' con la profondita' del lock. Il controllo
corretto e' pero' nel frame co-moving della highway: se la crescita grezza e' solo drift del tubo
W0, il pigeonhole sulle dogane intrinseche puo' ancora partire.

Correzione concettuale registrata:
- "caos eterno non-highway impossibile" e' ancora α1 riscritto; la novita' eventuale deve stare
  nel meccanismo, non nella forma per assurdo;
- il Link 1, "orbita eterna non-highway => lock W0-like profondi infinite volte", e' il crux,
  non la parte facile;
- la contraddizione paritaria non puo' basarsi sulla stessa cella assoluta, perche' §63 ha gia'
  mostrato quasi nessun riuso della cella critica assoluta. Se esiste, vive in dipendenze
  lineari globali GF(2) tra conteggi di visita, non nel flip per-cella isolato.

## 72.2 Script

Nuova sonda:

```
C:\Python\Python310\python.exe alpha1\door_discriminant_linf_profile.py `
  --horizon 1600 `
  --out-prefix alpha1\door_discriminant_linf_profile
```

Input: `alpha1/door_defect_profile_rows.csv` da §66.

Filtro:
- `kind=pre_onset_lock`;
- `is_actual_phase=1`;
- `clear=0`;
- `horizon=1600`.

Output:
- `alpha1/door_discriminant_linf_profile_rows.csv`;
- `alpha1/door_discriminant_linf_profile_unique_rows.csv`;
- `alpha1/door_discriminant_linf_profile_bins.csv`;
- `alpha1/door_discriminant_linf_profile_depths.csv`;
- `alpha1/door_discriminant_linf_profile_summary.json`.

La sonda esporta due frame:
- `raw`: coordinate relative originali `rel_x,rel_y`;
- `comoving`: coordinate intrinseche W0, ottenute sottraendo `floor(offset/104) * drift_phase`,
  dove `drift_phase` e' calcolato esattamente dalla rotazione W0 della fase valutata.

## 72.3 Risultati

Il campione selezionato contiene **786** fallimenti T3' reali. La deduplica per lock fisico non
rimuove nulla: **786/786** righe uniche. Inoltre `depth == first_bad_offset` per **786/786**,
quindi la profondita' del lock coincide con l'offset del primo discriminante T3' sul campione.

Conteggi globali nel frame grezzo:
- `frontier_black_collision`: **419**;
- `missing_black`: **367**;
- `max depth`: **1591**;
- `max L∞`: **36**;
- correlazione lineare `depth` vs `L∞`: Pearson **0.727**.

Non leggere Pearson come monotonia liscia: il grosso del campione e' a bassa profondita' e lo
Spearman globale e' **-0.098**. Il dato importante per il lemma delle classi finite e' l'envelope
di coda, non un fit monotono su tutti i 786 punti.

| depth bin | count | median depth | max depth | median `L∞` | q75 `L∞` | max `L∞` | missing | frontier |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 40-77 | 675 | 48 | 77 | 5.0 | 6.0 | 9 | 282 | 393 |
| 78-103 | 93 | 98 | 103 | 3.0 | 4.0 | 7 | 85 | 8 |
| 104-207 | 6 | 162.0 | 169 | 8.0 | 8.75 | 9 | 0 | 6 |
| 208-511 | 8 | 335.5 | 492 | 12.5 | 16.0 | 16 | 0 | 8 |
| 512-1023 | 2 | 742.0 | 799 | 20.5 | 21.25 | 22 | 0 | 2 |
| 1024+ | 2 | 1562.0 | 1591 | 36.0 | 36.0 | 36 | 0 | 2 |

Casi di coda:

| orbit | attempt | phase | depth | rel | `L1` | `L∞` | kind |
|---:|---|---:|---:|---|---:|---:|---|
| 21 | `21:26` | 24 | 1591 | `(-36,-31)` | 67 | 36 | `frontier_black_collision` |
| 5 | `5:17` | 99 | 1533 | `(-33,36)` | 69 | 36 | `frontier_black_collision` |
| 10 | `10:44` | 0 | 799 | `(-22,-15)` | 37 | 22 | `frontier_black_collision` |
| 4 | `4:4` | 0 | 685 | `(-19,-14)` | 33 | 19 | `frontier_black_collision` |
| 9 | `9:7` | 99 | 492 | `(-12,16)` | 28 | 16 | `frontier_black_collision` |

## 72.4 Lettura grezza

La strategia delle classi di debito **non respira in coordinate grezze**. Il raggio relativo del
primo discriminante non resta in un insieme piccolo e fisso: nella coda cresce da `L∞<=9` sotto
due periodi, a `16` intorno a 500 passi, a `22` intorno a 800, fino a `36` sopra 1500.

Questa lettura era troppo forte: confondeva non-localita' intrinseca con drift della highway.
La pendenza grezza `L∞/depth` e' dello stesso ordine di `2/104`, cioe' il drift del tubo W0.

## 72.5 Reframe co-moving W0

Rimisura nello stesso campione, ma nel frame intrinseco:

```
period_index = first_bad_offset // 104
offset_mod_period = first_bad_offset % 104
comoving_rel = rel - period_index * drift_phase
```

Il `drift_phase` e' fase-dipendente nel frame locale della porta. Esempi: fase 0 `(-2,-2)`,
fase 99 `(-2,+2)`, fase 103 `(+2,-2)`.

Risultato globale:
- `raw max L∞`: **36**;
- `comoving max L∞`: **9**;
- Pearson `depth` vs raw `L∞`: **0.727**;
- Pearson `depth` vs co-moving `L∞`: **0.100**;
- Spearman `depth` vs co-moving `L∞`: **-0.115**;
- classi osservate `(phase, comoving_rel_x, comoving_rel_y, required_black, bad_kind)`: **131**.

| depth bin | count | raw max `L∞` | co-moving median `L∞` | co-moving q75 `L∞` | co-moving max `L∞` |
|---|---:|---:|---:|---:|---:|
| 40-77 | 675 | 9 | 5.0 | 6.0 | 9 |
| 78-103 | 93 | 7 | 3.0 | 4.0 | 7 |
| 104-207 | 6 | 9 | 6.0 | 6.75 | 7 |
| 208-511 | 8 | 16 | 7.5 | 8.0 | 8 |
| 512-1023 | 2 | 22 | 7.5 | 7.75 | 8 |
| 1024+ | 2 | 36 | 7.0 | 7.5 | 8 |

Casi di coda dopo reframe:

| orbit | attempt | phase | depth | raw rel | raw `L∞` | drift phase | co-moving rel | co-moving `L∞` |
|---:|---|---:|---:|---|---:|---|---|---:|
| 21 | `21:26` | 24 | 1591 | `(-36,-31)` | 36 | `(-2,-2)` | `(-6,-1)` | 6 |
| 5 | `5:17` | 99 | 1533 | `(-33,36)` | 36 | `(-2,+2)` | `(-5,8)` | 8 |
| 10 | `10:44` | 0 | 799 | `(-22,-15)` | 22 | `(-2,-2)` | `(-8,-1)` | 8 |
| 4 | `4:4` | 0 | 685 | `(-19,-14)` | 19 | `(-2,-2)` | `(-7,-2)` | 7 |
| 9 | `9:7` | 99 | 492 | `(-12,16)` | 16 | `(-2,+2)` | `(-4,8)` | 8 |

## 72.6 Lettura corretta

Se si vuole salvare la direzione paritaria, il vincolo giusto deve cambiare forma:
- **frame co-moving W0**, non coordinate relative grezze;
- vincoli globali GF(2) sulla mappa "parola di svolte -> parita' di visita", non flip
  indipendenti per singola cella;
- oppure prima un argomento soft su Link 1: perche' un'orbita eterna non-highway debba
  produrre lock W0-like profondi infinite volte.

La misura co-moving riapre il Lemma della dogana ricorrente: sul campione lungo le classi esatte
nel frame intrinseco sono finite e piccole (`L∞<=9`). Questo non prova boundedness eterna e non
tocca Link 1. Pero' corregge la conclusione pratica: il `door_debt_graph.py` e' legittimo se,
e solo se, usa classi co-moving `(phase, offset_mod_period, comoving_rel_x, comoving_rel_y,
required_color/bad_kind)` e non celle relative grezze.

## 72.7 Roadmap aggiornata

Non costruire `door_debt_graph.py` in coordinate grezze. Costruirlo nel frame co-moving e tenerlo
separato da Link 1.

Prossimo progresso reale:
1. formulare Link 1 come lemma autonomo, anche debole o condizionato;
2. costruire il debt graph co-moving come test di Link 2, con classi finite osservate e senza
   riscalamenti tarabili;
3. solo dopo, costruire un sistema XOR/SAT sulle dipendenze globali GF(2), non su celle assolute
   riusate.

# §73. Pass-rate delle classi co-moving T3'

## 73.1 Motivazione

§72 ha mostrato finitezza e ricorrenza delle classi co-moving di prima morte. Ma il CSV §72 e'
condizionato sui soli fallimenti: non puo' dire se una classe ricorrente e' una dogana
intrinsecamente sempre sabotata, oppure se la stessa classe a volte passa e a volte fallisce.

Il gate per Link 3 e':

> per le classi co-moving ricorrenti, la parita' al momento della lettura e' forzata o resta
> variabile?

Se le classi top fossero zero-pass, il motore paritario sarebbe morto o dovrebbe cercare altre
porte. Se invece le stesse classi passano spesso, Link 3 ha un bersaglio reale.

## 73.2 Script

Nuova sonda:

```
C:\Python\Python310\python.exe alpha1\door_comoving_class_passrate.py `
  --horizon 1600 `
  --out-prefix alpha1\door_comoving_class_passrate
```

Input:
- `alpha1/door_discriminant_linf_profile_rows.csv` per le 131 classi di prima morte §72;
- `alpha1/dumps_all.txt` per rigiocare le 24 orbite e recuperare il campo al lock.

Metodo:
- considera solo la fase reale del lock;
- prende le classi `(phase, comoving_rel_x, comoving_rel_y, required_black)` osservate come
  prima morte in §72;
- rigioca tutti gli **810** tentativi porta (786 pre-onset falliti + 24 entry);
- per ogni lettura T3' entro `L=1600` che cade in una classe target, registra `pass/fail`,
  cella assoluta, offset, periodo e se l'evento e' la prima morte.

## 73.3 Risultati

Run completa:
- orbite completate: **24/24**;
- tentativi porta: **810**;
- classi target: **131**;
- righe evento lette: **101387**;
- pass: **91657**;
- fail: **9730**;
- pass-rate evento: **0.9040**;
- prime morti ritrovate: **786/786**.

Classi:
- classi con almeno un evento: **131/131**;
- classi con almeno un pass: **130/131**;
- classi miste pass/fail: **130/131**;
- classi zero-pass: **1/131**;
- classi zero-pass con supporto `first_bad_count >= 10`: **0**.

La sola zero-pass e' debole:

| rank | phase | co-moving rel | required | first bad | read events | pass | fail |
|---:|---:|---|---:|---:|---:|---:|---:|
| 46 | 92 | `(1,2)` | 1 | 4 | 4 | 0 | 4 |

Top classi:

| rank | class | first bad | reads | pass | fail | pass-rate | first-bad abs cells |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `(0,-5,-2,0)` | 78 | 4710 | 4224 | 486 | 0.8968 | 78 |
| 2 | `(103,3,-5,0)` | 49 | 1920 | 1751 | 169 | 0.9120 | 49 |
| 3 | `(0,-5,0,1)` | 39 | 314 | 150 | 164 | 0.4777 | 39 |
| 4 | `(103,3,-4,1)` | 35 | 128 | 88 | 40 | 0.6875 | 35 |
| 5 | `(0,-8,-1,0)` | 30 | 4710 | 4182 | 528 | 0.8879 | 30 |
| 6 | `(30,0,-3,1)` | 28 | 83 | 20 | 63 | 0.2410 | 28 |

Per le classi con almeno 10 prime morti, il pass-rate medio e' **0.7169**, minimo **0.2410**,
massimo **0.9742**. Quindi le classi dominanti non sono sabotaggi deterministici: passano
spesso, inclusa la top class.

## 73.4 Lettura

La premessa di Link 3 resta viva. Le classi co-moving ricorrono, ma non sono rigidamente bloccate
al colore cattivo. La classe top, che in §72 appariva come 78 prime morti su 78 celle assolute
diverse, qui produce **4224 pass** e **486 fail** su **4710** letture target. La stessa equazione
traslata a volte e' soddisfatta e a volte no.

Questo non accende ancora il motore paritario: le celle assolute restano quasi sempre diverse e
la collisione per flip della stessa cella non arriva da sola. Pero' chiude il falso negativo piu'
pericoloso: non siamo davanti a dogane co-moving permanentemente sbagliate. Se esiste una
contraddizione, deve vivere nelle dipendenze GF(2) globali fra queste letture variabili.

## 73.5 Roadmap aggiornata

Prossimi passi leciti:
1. costruire `door_debt_graph.py` nel frame co-moving, ma farlo come grafo di pass/fail e non
   come grafo delle sole prime morti;
2. includere nei nodi almeno `(phase, offset_mod_period, comoving_rel_x, comoving_rel_y,
   required_black)` e nei bordi la relazione temporale/assoluta fra letture;
3. cercare vincoli GF(2) globali sul vettore di parita' di visita, non riuso della stessa cella
   assoluta;
4. tenere separato Link 1: anche un Link 2+3 forte prova solo "lock profondi => pressione verso
   ingresso", non "orbita eterna => lock profondi".

## 73.6 File prodotti

- `alpha1/door_comoving_class_passrate.py`
- `alpha1/door_comoving_class_passrate_events.csv`
- `alpha1/door_comoving_class_passrate_classes.csv`
- `alpha1/door_comoving_class_passrate_orbits.csv`
- `alpha1/door_comoving_class_passrate_summary.json`
