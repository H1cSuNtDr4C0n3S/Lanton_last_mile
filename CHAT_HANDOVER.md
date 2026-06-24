# CHAT_HANDOVER — Stato del programma Langton al 2026-06-24
**Da: sessione §61 (lock -> checklist T3') → A: prossima sessione (§62) in C:\Lanton_last_mile.**
**Leggere insieme a CLAUDE.md. Dettagli completi: docs/LOCK_CHECKLIST_ADDENDUM.md §61;
catena precedente: docs/DEBT_LOCK_2D_ADDENDUM.md §60, docs/DEBT_LOCK_ADDENDUM.md §59,
docs/DELTA4_BETA_ADDENDUM.md §58, docs/ALPHA1_FABRY_ADDENDUM.md §57.**

## A. Stato del programma in dieci righe
La congettura resta ridotta a **α1 ∧ β ∧ γ**; il "locale" è sigillato (T1, T2, α2, T3′ + dogane).
Teorema della Finestra: r=4 chiuso (27,3M stati, rotori tutti B-T), tariffe δ₁=3/5, δ₂=1/7,
δ₃=1/64, δ₄^auto=2/313; automa-prodotto A(r;m,D) costruito, sound, verificatore dei 252 fantasmi
(§56). §57 ha declassato il pavimento del morso fresco; §58 ha mostrato che la non-localita'
`r=4` non erode. §59 ha falsificato il ponte diretto `deep_black -> lock`. §60 ha mostrato che
fresh-bite e' l'innesco locale. **Novita' §61:** sui gate-lock lunghi il verdetto e' esattamente
la checklist T3':
1. La formulazione di α1 come **pavimento del tasso di morso fresco** ("modo DC", #24) **erode**:
   su orbite fino a 3·10⁵, stalli ~lineari in T (90–104 periodi vs 8 a T≲25k), densità→~0.05,
   pavimento a finestra L=10400 sceso a mediana 0.006 con uno **zero esatto** — e tutto nel caos
   puro, non pre-lock (kill-shot tail/core=1.13). NON è l'invariante giusto.
2. Il tasso di letture nere fuori-finestra `r=4` **non erode** sulle stesse orbite: mediana
   **0.2334/passo**, tail/core mediano **1.06**; minimi mobili ancora **9x, 16x, 27.4x**
   sopra `delta4_auto=2/313` per L=313/1040/10400.
3. I lock simbolici W0-like persistono, ma **non** sono predetti positivamente da deep-black:
   `D>=40` cala con i quantili deep (delta top-bottom -0.2641...-0.1406), mentre cresce coi
   quantili fresh-bite (+0.1460...+0.3256).
4. Nel 2D, a deep quasi fissato l'effetto bite resta positivo (`D>=40` mediana +0.1373);
   a bite quasi fissato l'effetto deep resta negativo (`D>=40` mediana -0.0350).
5. `D>=40` e' comunque presente in tutte le 24 orbite (113-167 run/orbita), `maxD` min/med/max =
   78/167/1591; `D>=80` e' piu' raro ma presente in mediana 4 run/orbita.
6. **Caveat fondamentale:** ogni orbita converge ⇒ l'orbita eterna non-highway è controfattuale ⇒
   **evidenza forte, NON prova**. La simulazione NON può decidere α1; va dimostrata su orbite eterne.
7. `lock_checklist_probe.py` valuta T3' sui lock left-maximal per-allineamento: **891/891**
   gate-lock pre-onset muoiono alla prima lettura esogena cattiva; **24/24** onset veri
   passano il controllo positivo.
8. **Ridirezione aggiornata:** il ponte locale `lock -> checklist -> verdetto` e' sano. Il
   prossimo fronte e' la **hazard/mixing della checklist**: capire se gli stati-checklist ai lock
   possono restare eternamente sbagliati.

## B. Risultati delle ultime sessioni (§57-§61)

### B.1 Strumento alpha1_engine.c (ALPHA1 §57.1) — validato e veloce
Simulatore C self-contained (convenzione = libant.c). Modi `search` (early-stop all'onset, semi
riproducibili dal solo rngstate 64-bit), `reseed`, `dump`. morso = fresca-bianca. Validato:
vuota→**9977**, (7,−7)→**106258**, highway **22/104**; Berlekamp–Massey highway→L≈102, rumore→n/2.
**Fix di efficienza decisivo:** reset solo celle toccate invece di azzerare la hash 16 MB/seme →
da 1.8k a **31.7k semi/s** su 14 shard (collo = banda di memoria, non thread; CLAUDE.md §1-g/§4).

### B.2 I due test (ALPHA1 §57.2)
- **Carlson/Berlekamp–Massey:** ogni transiente caotico ha complessità lineare **n/2** ⇒ F(z)=Σz^{τₙ}
  ha frontiera naturale sul cerchio unitario (highway razionale). Dicotomia confermata ma = la
  convergenza riscritta, non α1.
- **gap/Fabry:** stalli e densità sui transienti lunghi (il bersaglio vero).

### B.3 Run Ryzen + test within-orbit (ALPHA1 §57.3–57.4) — il risultato
Run: 8.44 h, 14 shard, **9.8·10⁸ semi**, **88.521 orbite** onset≥100k, **BEST onset 313.358**
(≈3× sandbox; ricerca casuale plateau ~log: niente 10⁶ senza semi strutturati). Test within-orbit
(NON distorto, su 24 orbite 252k–313k, `dumps_all.txt`): max-stall **90–104 periodi** (~lineare in T,
core ~T^1.09), sale ancora nell'ultimo 30% in **16/24**, densità ~0.05, **L=1040 floor=0 su tutte**,
**L=10400 floor mediana 0.006 con uno zero** (orbita 268891). **Kill-shot pre-lock:** caos puro vs
pre-lock → tail/core **1.13**, e il core L=10400 floor tocca 0 ⇒ gli stalli grossi vivono nel caos.

### B.4 Sonda delta4 -> beta (DELTA4-BETA §58) — il risultato nuovo
`alpha1/delta4_long_orbits.py` rigenera le 24 orbite da `rngstate`, valida i morsi contro
`dumps_all.txt`, misura `r=4` deep-black e lock simbolici. Runtime completo: 72.6 s.

| quantita' | min | mediana | max |
|---|---:|---:|---:|
| tasso nero fuori-finestra `r=4` | 0.2277 | **0.2334** | 0.2378 |
| tasso morso fresco | 0.0466 | **0.0537** | 0.0627 |
| tail/core nero fuori-finestra | 1.031 | **1.058** | 1.093 |
| tail/core morso fresco | 0.439 | **0.614** | 0.795 |

Minimi mobili deep-black: L=313 -> 0.0575 (**9.0x** `delta4_auto`), L=1040 -> 0.1019
(**16.0x**), L=10400 -> 0.1750 (**27.4x**). I minimi del morso fresco sono zero a L=313 e
1040 su tutte le orbite, e zero globale anche a L=10400.

### B.5 Debito profondo -> lock (DEBT-LOCK §59) — falsificazione utile
`alpha1/debt_lock_hazard.py` usa predictor causale `[t-Lpred,t)` e lock futuro `[t,t+H)`,
con `Lpred={313,1040,3120}`, `H={312,1040}`, `D={40,80}`. Runtime completo: 164.3 s.

Per bin crescenti di `deep_black`, l'hazard futuro cala in tutti i casi:
- `D>=40`: delta top-bottom da **-0.2641** a **-0.1406**, ratio 0.28-0.48.
- `D>=80`: delta top-bottom da **-0.0236** a **-0.0107**, ratio 0.13-0.42.

Il controllo `fresh_bite` predice invece positivamente:
- `D>=40`: delta +0.1460 ... +0.3256.
- `D>=80`: delta +0.0117 ... +0.0271.

Esempio `Lpred=1040`, `H=1040`, `D>=40`: deep rate 0.1852->0.2742, bite rate
0.1255->0.0075, hazard 0.4867->0.2226. Interpretazione: il debito profondo e' substrato
di memoria, non grilletto; il lock richiede anche attivita' fresca.

### B.6 Modello 2D deep/bite -> lock (DEBT-LOCK 2D §60)
`alpha1/debt_lock_2d.py` binnerizza gli anchor per entrambe le coordinate. Runtime: 146.7 s.

Effetto medio pesato entro strisce:
- `D>=40`: deep effect entro bite mediano **-0.0350**; bite effect entro deep mediano **+0.1373**.
- `D>=80`: deep effect entro bite mediano **-0.0022**; bite effect entro deep mediano **+0.0121**.

Caso centrale `Lpred=1040`, `H=1040`: best cell `(deep=0,bite=4)` con hazard `0.5063`
per `D>=40`; worst `(deep=4,bite=0)` con hazard `0.1601`. Quindi la cella produttiva e'
deep basso / bite alto: il debito profondo e' substrato, non scintilla.

### B.7 Lock -> checklist T3' (LOCK-CHECKLIST §61)
`alpha1/lock_checklist_probe.py` ricostruisce E(k) direttamente da `W0`, estrae lock
per-allineamento left-maximal, separa porte/fasi mute con la tabella α2, e legge la checklist
read-only nello stato al tempo del lock. Runtime completo: 68.1 s.

Risultato:
- lock pre-onset valutati: **3303**;
- gate-lock pre-onset: **891**;
- gate-lock con morte esattamente alla prima lettura esogena cattiva: **891/891**;
- onset veri come controlli positivi: **24/24**.

Per soglia: `D>=40` = 3191 lock, 786 gate; `D>=80` = 112 lock, 105 gate. Sui gate-lock i
fallimenti sono bilanciati: `missing_black` 447, `frontier_black_collision` 444. Top offset:
45, 46, 71, 77, 99, 98. Lettura: il lock bussa, la checklist decide; il problema residuo e'
la non-cospirazione della checklist, non un altro proxy di `D(t)`.

## C. Roadmap (priorita' prossima sessione §62)
1. **DECLASSATA: α1-come-pavimento-del-morso-fresco.** Misurata, erode (B.3). Non riaprire come
   liminf-che-decade da rincorrere via simulazione: stesso muro del controfattuale eterno (CLAUDE.md §1-i).
2. **Checklist hazard.** Modellare `P(checklist OK | lock)` per fase porta, offset di morte,
   deep/bite pre-lock, tempo assoluto e indice del lock.
3. **Mixing della checklist.** Transizioni fra lock consecutivi: stato congiunto delle celle
   critiche, parita' `t mod 8/16`, posizione porta, riuso della cella assoluta critica.
4. **Consolidamento (alternativa legittima).** Il locale sigillato, γ≤40, finestra r=4, prodotto sound
   sono teoremi: scrivibili come contributo a sé (riduzione a α1∧β∧γ + macchina) senza chiudere il crux.
5. **Coda PRODOTTO §56 (se si torna sul fronte certificazione):** rimozione cicli B-T nel prodotto
   (ostacolo A) e memoria temporale compatta (ostacolo B); poi r=4 ibrida δ^alt parziale.
6. **r=5 e γ esteso (42–52): SOLO dopo** — direttiva invariata.

## D. Domande aperte in coda (oltre la roadmap)
1. Checklist beta sui lock delle orbite lunghe: ora il ponte locale e' confermato; resta
   quantificare hazard e mixing (vedi C.2-C.3).
2. Lemma A (alternanza taglia i fantasmi) / Lemma B (memoria antica non eternamente economica) —
   RADIUS §55.4: il prodotto È la via del Lemma A, una volta tolto l'ostacolo A (PRODOTTO §56).
3. Congettura B–T-autosufficienza (RADIUS §51.5): ogni parola di rotore ha rot≢0 mod4 o drift=0?
4. L_∞ NUMERABILE (§28.2) e **scala del diavolo falsificata** (sessione devil's-staircase): NON
   riaprire percorsi entropici/spettrali/quasi-periodici per α1 — il regime irrazionale è vuoto.

## E. Igiene operativa
- **Self-test PRIMA di tutto:** `window_automaton.py --selftest`, `product_automaton.py --selftest`,
  e `alpha1\alpha1_engine.exe` (vuota→9977; (7,−7)→106258; highway 22/104). MAI rossi.
- **Macchina:** Ryzen 5800X, **16 GB RAM (limite vero)**, 8C/16T; Python numpy/scipy SOLO
  `C:\Python\Python310\python.exe`; gcc = `C:\Strawberry\c\bin\gcc.exe`; stdout cp1252 ⇒
  `sys.stdout.reconfigure(encoding="utf-8")`.
- **alpha1 (sessioni §57-§59):** `alpha1_engine.exe search <shard> <nsh> <nseed> <cap> <smin> <smax> [minOnset]`
  (early-stop, reset-touched); `reseed <cap> <rngstate> <smin> <smax>` per ridumpare un'orbita dal
  rngstate; `dump <cap>` con seme su stdin. Monitor: `powershell -File alpha1\status.ps1`.
  Sonda §58: `C:\Python\Python310\python.exe alpha1\delta4_long_orbits.py`.
  Sonda §59: `C:\Python\Python310\python.exe alpha1\debt_lock_hazard.py`.
  Sonda §60: `C:\Python\Python310\python.exe alpha1\debt_lock_2d.py`.
  Sonda §61: `C:\Python\Python310\python.exe alpha1\lock_checklist_probe.py`.
- **Builder C prodotto:** `product_build.exe <r> <m> <D> <outdir> [cap] [modo]` (0=full,1=black-only,
  2=ibrida); MAI il BFS Python del prodotto oltre poche migliaia di stati (esplode + swap, §56.6).
- **Niente Monitor con `tail -f`** (restano orfani "in esecuzione per ore"): seguire i run con Read
  sull'output o `until grep` che ESCE.
- Trappole cumulative: CLAUDE.md §1 (a–i) + RADIUS §50/§54.4/§55.2 + PRODOTTO §56.6 +
  **ALPHA1 §57.7** (reset-hash per-seme; survivorship temporale; controfattuale eterno; apofenia π·10⁵).
- Verbale prossima sessione: **§62**, stesso stile.
- Tempi tipici: build r4 20 s; A(2;4,5) prodotto 12,7 s; alpha1 search 31.7k semi/s; reseed 313k <1 s.
