# Gate-One Co-Moving Kernel Addendum (§78)

Riepilogo in una frase: il fallimento gate-zero di §75 era una scelta di **frame**, non un limite
di fondo — gli stati esogeni di `E(k)`, riletti nel frame **co-moving W0**, hanno un'impronta
**finita e fissa** di raggio strutturale `rho<=9` (uguale al `<=9` empirico di §72), e questa
impronta **separa** i due anchor che avevano collassato sotto `A0`; resta aperto solo il
**cap temporale** `P` (profondità in periodi), che è il residuo Link 1.

## 78.1 Obiettivo

§75 ha chiuso la via `A0(r,K,D0)`: nessun raggio in frame-ancora `r<=8` rende T3' funzione dello
stato, perché la cella discriminante **cavalca il tubo W0** ed esce dalla finestra col drift. La
roadmap (C.16) chiedeva: definire `A1` con T3' deterministico per costruzione, **oppure** propagare
`unknown`. Questa sessione fissa l'**intuizione del kernel** (la portante minima di `A1`) e la mette
alla prova senza nuovo simulatore — solo `make_exogenous_schedule`, `phase_drifts`, `replay_snapshots`,
`eval_first_bad` già validati.

## 78.2 Il kernel

Enunciato. T3' **non** è funzione di nessuna finestra in frame-ancora (ogni raggio fisso fallisce,
§75). È — strutturalmente — funzione dell'impronta di letture esogene nel **frame co-moving W0**,
ottenuta sottraendo `(offset // 104) * drift_phase[g]`. Il `drift_phase[g]` è calcolato esattamente
dalla rotazione W0 della fase `g` (`phase_drifts`).

Perché il frame co-moving è quello giusto: `E(k)` registra il colore richiesto di ogni **nuova cella
visitata dalla highway** a offset crescente; siccome la highway è periodica-con-drift, le nuove celle
del periodo `p` sono quelle del periodo 0 traslate di `p * drift`. In coordinate co-moving collassano
sulla stessa impronta del periodo 0.

## 78.3 Risultato strutturale (impronta fissa, raggio certificato)

`gate_one_comoving_audit.py`, parte `structural`, calcola l'impronta co-moving per le 22 fasi di porta
(`GATE_PHASES`) a `max_offset=20000`, verificando la stabilizzazione ai tagli 1040/5200/10400/20000.

Risultato fase 98:

| upto offset | letture grezze | celle impronta co-moving | `rho` |
|---:|---:|---:|---:|
| 1040 | 244 | **44** | 7 |
| 5200 | 1124 | **44** | 7 |
| 10400 | 2224 | **44** | 7 |
| 20000 | 4251 | **44** | 7 |

L'impronta è **identica** (44 celle) a tutti gli orizzonti mentre le letture grezze crescono
244 -> 4251: l'impronta co-moving è un **insieme finito fisso**, non cresce con l'orizzonte.

Su tutte le 22 fasi di porta: `all_footprints_stabilized = 1`, `|S_g|` tra 38 e 52,
e **`max_g rho_g = 9`**.

Confronto chiave: il `rho` strutturale (da W0 soltanto, check finito) = **9** = il
`comoving max L∞ = 9` **empirico** misurato in §72 sui 786 fallimenti reali. Quindi il
limite di raggio non è un artefatto di campione: è **strutturale**. Questo risponde alla
domanda di certificazione (b) per la metà **spaziale** del kernel: il raggio co-moving è
limitato dalla struttura di `E(k)/W0`.

## 78.4 Sufficienza sul testimone gate-zero

`gate_one_comoving_audit.py`, parte `sufficiency`, rigioca il testimone dinamico §75 (orbita 5,
`rngstate=16489936061346709332`, fase 98, anchor `t=60320` / `t=60840`) e confronta i due anchor
**sull'impronta co-moving fissa**, lette lungo le strisce per-periodo.

Risultato (riproduce §75: `first_bad` 1014 vs 494):
- entrambi i `first_bad` mappano alla **stessa cella co-moving (7,5)** (`anchors_same_comoving_decisive_cell=1`);
- l'impronta co-moving **separa** i due anchor: differiscono in **12/44** strisce
  (`comoving_footprint_separates_anchors=1`).

Cella decisiva co-moving **(7,5)**, colore richiesto **bianco**:
- A è nera a (7,5) ai periodi **9, 12** -> prima violazione periodo 9 (offset 1014);
- B è nera a (7,5) ai periodi **4, 7** -> prima violazione periodo 4 (offset 494).

Lettura: la **stessa dogana co-moving** (7,5) decide entrambi gli anchor, a periodi diversi. Quindi
`A1 =` "colori del detrito lungo le strisce dell'impronta co-moving" rende T3' funzione dello stato
**esattamente dove `A0` era cieco**. È un gate-one **pass** sul controesempio che ha rotto gate-zero.

## 78.5 Definizione di `A1`

```text
A1-state(g) = (
  per ogni cella s dell'impronta co-moving S_g (|S_g| ~40-52, rho<=9):
    la sequenza di colori del detrito lungo la striscia  s + p*drift_g,  p = 0..P,
  observed_turn_bit,
  fase g
)
```

- Parte **spaziale**: finita e certificata (`<=52` celle, `rho<=9`, da W0).
- Parte **temporale**: il cap `P` in periodi. T3' è determinato da `A1` **fino a `P`**; oltre `P`
  lo stato è `unknown`.

Questo sintetizza le due opzioni di §75.5: Opzione 1 (T3' funzione dello stato, includendo le celle
rilevanti) per lo **spazio**, Opzione 2 (`OK/KO/unknown` fuori budget) per il **tempo**.

## 78.6 Residuo onesto (il vero crux, isolato)

Trappola nuova **(m)**: impronta spaziale limitata **≠** stato finito. Le 44 celle co-moving non sono
44 celle assolute: ognuna è una **striscia** interrogata a ogni periodo su una cella assoluta diversa
(`s + p*drift`). Le letture grezze crescono senza limite (244 -> 4251 -> ∞). Su un campo
**raggiungibile** (finito) il detrito si esaurisce e la checklist termina, ma il **periodo `P`** in cui
termina dipende dall'estensione del detrito.

Il testimone §75 si decide entro `P<=9`. La domanda residua: esiste un cap `P` uniforme su **tutte**
le storie raggiungibili tale che T3' sia deciso entro `P` periodi dalla porta? Quel cap è dove vive
Link 1: un'orbita eterna non-highway potrebbe avere detrito arbitrariamente lontano lungo una striscia,
spingendo `P` all'infinito. Bound uniforme di `P` ~ Link 1 / α1-hard.

Rischio specifico da non nascondere: la profondità decisiva `P` è la versione **co-moving** della
lunghezza di stallo che **erode** in §30/§57 (cap di campione, non eterno; controfattuale eterno,
CLAUDE.md §1-i). Sul campione §72 i `first_bad` arrivano a offset 1591 = periodo **15**, con coda
sottile ma presente. Quindi è plausibile che `P` non sia limitato sui prefissi raggiungibili — il che
**favorisce la via `unknown`** rispetto al determinismo pieno.

## 78.7 Prossimo passo

1. **Sweep within-orbit della profondità decisiva** sulle 24 orbite lunghe: per ogni tentativo porta,
   il periodo `P` del `first_bad` (o il max periodo con striscia nera prima dell'ingresso) cresce con
   `T` o satura? È l'analogo §78 della misura within-orbit degli stalli (#30), ma sulla quantità
   **giusta** (profondità co-moving della dogana decisiva, non lunghezza di stallo grezza). Se cresce
   con `T` -> `P` illimitato sui prefissi -> `A1` ha bisogno di `unknown`, certificazione α1-hard. Se
   satura -> candidato `P` uniforme.
2. **Costruire `A1` con `unknown` esplicito** a un budget `P` fissato e certificare solo le SCC il cui
   verdetto no-entry è invariante alle strisce `unknown` (Opzione 2 di §75.5, ora ben fondata).
   Fissare il budget `P` *prima* (CLAUDE.md: trattare la non-convergenza come risultato).

Non riaprire: aumentare `r` in frame-ancora (§75 lo ha chiuso); door_debt_graph in coordinate grezze
(§72/§74 lo hanno potato).

## 78.8 Inventario file

- `GA_stress_agent/gate_one_comoving_audit.py` — audit gate-one (strutturale + sufficienza).
- `GA_stress_agent/gate_one_comoving_summary.json` — output macchina.
- Riusa: `alpha1/lock_checklist_probe.py` (`make_exogenous_schedule`, `rel_to_abs`, `GATE_PHASES`),
  `alpha1/door_discriminant_linf_profile.py` (`phase_drifts`),
  `GA_stress_agent/ga_gate_zero_audit.py` (`replay_snapshots`),
  `alpha1/t3_coreachability_pair_scanner.py` (`eval_first_bad`).
- Self-test propedeutici (invariati): `window_automaton.py --selftest`, `product_automaton.py --selftest`,
  `alpha1_engine.exe` su vuota `9977` e `(7,-7)` `106258`.

Comando:
`python GA_stress_agent/gate_one_comoving_audit.py --phase 98 --orbit-index 5 --anchor-a 60320 --anchor-b 60840 --periods 12 --horizon 1600`.

---

## 78.9 Risultato: sweep della profondità decisiva `P` (eseguito)

`decisive_depth_sweep.py` misura, per ogni attempt di gate-lock nelle 24 orbite lunghe, la
profondità co-moving decisiva `P = first_bad_offset // 104` alla **fase reale**, a orizzonte
**10400 (100 periodi)** — 6.5x il cap di §72/§66 (1600 = periodo 15) — per non censurare `P`.

Validazione: **786 attempt falliti**, identico alla popolazione §72. Pipeline confermata.

Risultati:
- **`P` concentrato a 0**: 768/786 = **97.7%** falliscono al periodo 0 (offset < 104). Mediana 0, p95 0.
- **Coda sottilissima**: istogramma periodi `{0:768, 1:6, 2:4, 3:1, 4:3, 6:1, 7:1, 14:1, 15:1}`, **max 15**.
- **Niente censura**: a orizzonte 10400, **0** fallimenti oltre il periodo 15 e **0** vicini al nuovo
  orizzonte. Quindi il max 1591 di §72 era una coda isolata reale, non il bordo di una distribuzione
  tagliata. `P` si ferma davvero ~15 su questi dati.
- **Niente salita within-orbit tardiva**: solo **2/24** orbite hanno l'ultimo 30% di attempt che fissa
  un nuovo running-max di `P` — l'**opposto** dell'erosione degli stalli di §30.
- **Niente crescita cross-orbit**: `corr(max P, onset) = 0.057`. Il `P=15` è nell'orbita **21**
  (onset 255k, tra le più corte); le **3 orbite più lunghe** (313k/308k/302k) hanno `max P = 1/2/1`.
  Se `P` crescesse con `T`, le orbite lunghe avrebbero `P` profondo: è il contrario.

Verdetto onesto. Sui dati raggiungibili più profondi disponibili (`T` fino a 3.1x10^5), la profondità
co-moving decisiva `P` è **limitata (≤15) e non cresce con `T`**. Questo **favorisce la via del
determinismo** per `A1`: un budget di periodi `P` esiste, e il **97.7%** degli attempt si decide già a
`P=0`. È un quadro nettamente migliore del rischio paventato in §78.6 (che `P` erodesse come lo stallo):
i dati dicono che **non** erode.

Limite invalicabile (Faraday-Maxwell). Restano dati di orbite **convergenti** (sub-onset): un'orbita
eterna non-highway è controfattuale (muro α1). E la coda non è banalmente 0 (esistono attempt a periodo
15), quindi l'inviluppo vero del budget su **tutti** i campi raggiungibili resta non dimostrato — solo
non smentito, e senza segno di crescita.

`A1` rigoroso aggiornato: finestra spaziale co-moving (`ρ≤9`, certificata §78.3-4) + **budget di periodi
`P`** con `unknown` oltre. Poiché l'insieme oltre-budget è **empiricamente vuoto già a `P=15`**,
l'`unknown` è piccolo e controllato: `A1` decide il 97.7% a `P=0`, decide la coda fino al budget, e
marca `unknown` solo oltre (insieme vuoto sul campione). La trappola (m) (spaziale-limitato ≠ stato
finito) è quindi **empiricamente mite**: la profondità temporale che farebbe esplodere lo stato è
concentrata a 0 e limitata ≤15 sul campione.

Prossimo passo aggiornato:
1. **Inviluppo della coda**: spingere più semi/orbite (oltre le 24 selezionate per onset alto, banda
   stretta 251k-313k) per vedere se `P>15` compare mai. È l'unico modo per stressare il budget; resta
   evidenza, non prova (controfattuale eterno).
2. **Costruire `A1` a budget `P` fissato** (es. 16) con `unknown` oltre, e certificare le SCC: con
   l'insieme oltre-budget vuoto sul campione, la certificazione è trattabile.

Inventario aggiornato: `GA_stress_agent/decisive_depth_sweep.py`,
`GA_stress_agent/decisive_depth_summary.json`, `GA_stress_agent/decisive_depth_rows.csv`.
Comando: `python GA_stress_agent/decisive_depth_sweep.py --horizon 10400`.

---

## 78.10 Certificato a budget di `A1` (eseguito — opzione 2)

`a1_budget_certificate.py` costruisce `A1` e verifica che il verdetto no-entry (T3'-fail) sia
**funzione dello stato finito co-moving**, ri-derivandolo dallo stato SOLO (read cappate al periodo `P`).

Risultati su tutti i **786** attempt falliti raggiungibili:
- **Costruzione sound (`construction_sound=1`)**: ogni cella di first-bad è co-moving **dentro** l'impronta
  fissa `S_phase` (786/786), e la ri-derivazione a budget `P` riproduce **esattamente** il verdetto
  ground-truth. Quindi `A1` immagazzina davvero la lettura decisiva — non è un'asserzione.
- **Curva di copertura |unknown| vs `P`**: `P=0` → 97.7% determinati (18 unknown), monotona crescente,
  **unknown-free a `P=15`** (0 unknown). Budget 15 copre TUTTI gli attempt falliti raggiungibili.
- **Posizione-sola insufficiente** (contrasto §73, ora sui nostri dati): delle 131 classi co-moving
  posizione-sola, **9 sono ambigue** (più di un periodo decisivo nello stesso punto), es. fase-0 cella
  `(-7,-2)` con periodi `{0,1,3,6}`. I **contenuti** delle strisce di `A1` le risolvono per costruzione
  (periodo diverso ⇒ read memorizzata diversa ⇒ stato diverso). Pass-rate posizione-sola 0.904 (§73) →
  `A1` rende deterministico.
- **Spazio degli stati finito**: max impronta 52 celle; bound `2^(|S_g|*(P+1))` (sovrastima grossolana);
  gli stati `A1` **raggiungibili** sono esattamente i 786 fallimenti campionati + contesto orbita.

Verdetto. Il blocco del gate-zero (A0 cieco, §75) è **scaricato**: su `A1` il verdetto no-entry è
funzione di uno stato finito co-moving, **unknown-free a `P≥15`** su tutti gli attempt raggiungibili.
Resta per la certificazione eterna: l'insieme oltre-budget `unknown` (vuoto sul campione, non
dimostrabile-vuoto in eterno = Link 1). La prossima costruzione separata NON è un automa-finestra a
raggio 9 (infattibile, 3^361; e comunque oggetto sbagliato): è il bridge con la linea δ_r — vedi §78.12.

Inventario: `GA_stress_agent/a1_budget_certificate.py`, `GA_stress_agent/a1_budget_certificate.json`.

---

## 78.11 Stress della coda con semi nuovi (eseguito — opzione 1)

Test dell'inviluppo del budget `P` fuori dalle 24 orbite selezionate per onset alto. `alpha1_engine.c`
ricompilato e validato (griglia vuota → onset **9977**; `(7,-7)` → onset **106258**). Harvest via
`search`: **312** semi nuovi convergenti con onset **≥80k** (range 80k-180k), nessuno coincidente con
i 24 rngstate esistenti (`new_high_onset_seeds.csv`). Sweep di profondità decisiva sui **70 a onset più
alto** (105k-180k) con `new_seed_depth_sweep.py`.

Risultato su **1228** attempt falliti indipendenti:
- `P`: mediana 0, p95 0, **MAX 14**. Istogramma `{0:1207, 1:10, 2:4, 3:2, 4:3, 10:1, 14:1}`.
- **0 attempt con `P>15`**. Il soffitto del budget regge su un campione indipendente.
- **98.3%** a `P=0` (1207/1228), stessa concentrazione dell'originale.
- Il `P` più profondo (14) è a onset **114k**, NON al massimo (180k → `P=4`). Nessuna crescita pulita
  con `T` (corr 0.245, rumore della coda sottile).

Quadro combinato (24 orbite 250k-313k + 70 semi 105k-180k = **2014** attempt falliti):
`P` concentrato a 0 (~97%), **mai oltre 15**, profondità massime ai onset MEDI non ai più alti.
La preoccupazione §78.6 (che `P` erodesse come il pavimento di stallo §30) è **doppiamente smentita**:
2014 attempt, nessuno oltre il periodo 15, nessun trend con `T`.

Limite invariato (Faraday-Maxwell): restano orbite convergenti, controfattuale eterno non t_toccato, e
la coda non è 0 (esistono `P=14,15`) ⇒ bound uniforme su TUTTI i campi raggiungibili non dimostrato,
ma ora molto solido e non-crescente su 2014 attempt onset-diversi. Corrobora la costruzione `A1` a
budget 15 di §78.10.

Inventario: `GA_stress_agent/new_high_onset_seeds.csv` (312 semi), `GA_stress_agent/new_seed_depth_sweep.py`,
`GA_stress_agent/new_seeds_depth_summary.json`. Comando: `python GA_stress_agent/new_seed_depth_sweep.py --top 70`.

---

## 78.12 Sintesi e relazione con δ_r (correzione + handoff)

Correzione di framing (Faraday-Maxwell, su mia svista nelle §§precedenti): §78 (porta/`A1`) e δ_r
(morsi) sono **due certificati β complementari**, NON un unico oggetto a "raggio 9". Un automa-finestra
a raggio 9 è infattibile (box 19×19 = 361 celle, 3^361) e comunque è l'oggetto sbagliato.

Cosa sono davvero i due lati, e dove stanno (numeri dalla repo):

- **Lato porta (§78, fatto).** `A1` è una macchina finita valutata agli eventi di lock: impronta
  co-moving di **44 celle** (box `ρ=9`, strutturale) + budget temporale **P=15** + `unknown` oltre
  (vuoto sul campione, 2014 attempt). Verdetto no-entry = funzione dello stato finito. È un check
  **one-shot** alla porta, non la dinamica continua.

- **Lato morsi (δ_r, in corso, indipendente da §78).** Automa-finestra a raggio `r` (continuo, ogni
  passo) + memoria prodotto `A(r;m,D)` di `m` celle fuori-finestra in box `D`. Stato nella repo:
  - finestra `r=3`: 45971 stati, 1 SCC ricorrente senza-assumiB (rotore), parola p=15 drift(0,1) → **B-T**;
  - finestra `r=4`: 27.3M stati, 66913 SCC ricorrenti senza-assumiB, **tutti rotori**;
  - prodotto `δ^alt` VERIFICATO > 0: `r1m8d8` → δ=1/8=0.125; `r2m4d8` → δ=2/71≈**0.028** (witness certificato).
  `δ^alt>0` = tariffa assumiB **positiva per passo** ⇒ nessun cammino auto-consistente evita
  "assumere nero" per sempre.

Perché NON si fondono in un automa solo: l'impronta porta (44 celle) eccede la memoria esplicita
trattabile del prodotto (`m≈4-8`; già `r2m4d5h` = 17.3M stati). Sono usi diversi (porta = one-shot ai
lock; prodotto = morsi continui). Tenerli separati è corretto, non una rinuncia.

**Link 1 (crux, aperto)** — "orbita eterna non-highway ⇒ lock W0-like profondi infinite volte" — è ciò
che **combinerebbe** i due: `δ^alt>0` (i morsi forzano struttura/tariffa) + `A1` (verdetto porta finito).
Va formulato come **lemma autonomo**, anche debole/condizionato.

Prossimi passi per la chat successiva (DUE linee indipendenti + il ponte):
1. **δ_r (lato morsi)**: spingere `A(r;m,D)` a `(m,D)` maggiori e finestra `r=3`; vedere se `δ^alt`
   resta staccato da 0 o caratterizzarne il limite. È la linea "Step 1" dei handover, **indipendente**
   da §78. Self-test `product_automaton.py --selftest` OBBLIGATORIO prima.
2. **§78 (lato porta)**: il certificato a budget è chiuso; resta solo l'inviluppo eterno della coda
   (controfattuale) — rendimenti decrescenti via simulazione; il gap rigoroso è Link 1.
3. **Link 1 come lemma autonomo** che salda δ^alt (morsi) e A1 (porta).

Stato self-test alla consegna: `window_automaton.py --selftest` VERDE (r1=15, r2=403). Eseguire anche
`product_automaton.py --selftest` prima di lavorare sul prodotto.
