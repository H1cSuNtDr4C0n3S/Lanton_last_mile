# CHAT_HANDOVER — Stato del programma Langton al 2026-06-25
**Da: sessione §73 (pass-rate classi co-moving T3') → A: prossima sessione (§74) in C:\Lanton_last_mile.**
**Leggere insieme a CLAUDE.md. Dettagli completi: docs/COMPAT_EVENT_COREACHABILITY_ADDENDUM.md §70-§73;
catena precedente: docs/COMPATIBILITY_POTENTIAL_ADDENDUM.md §69,
docs/ENDPOINT_MONOTONE_NOGO_ADDENDUM.md §68, docs/POTENTIAL_SEGMENT_SCANNER_ADDENDUM.md §67,
docs/DOOR_DEFECT_PROFILE_ADDENDUM.md §66, docs/CHECKLIST_NONLOCAL_STRATEGY_ADDENDUM.md §65,
docs/CHECKLIST_VECTOR_MODEL_ADDENDUM.md §64,
docs/CHECKLIST_VECTOR_GEOMETRY_ADDENDUM.md §63,
docs/CHECKLIST_MIXING_ADDENDUM.md §62, docs/LOCK_CHECKLIST_ADDENDUM.md §61,
docs/DEBT_LOCK_2D_ADDENDUM.md §60, docs/DEBT_LOCK_ADDENDUM.md §59,
docs/DELTA4_BETA_ADDENDUM.md §58, docs/ALPHA1_FABRY_ADDENDUM.md §57.**

## A. Stato del programma in dieci righe
La congettura resta ridotta a **α1 ∧ β ∧ γ**; il "locale" è sigillato (T1, T2, α2, T3′ + dogane).
Teorema della Finestra: r=4 chiuso (27,3M stati, rotori tutti B-T), tariffe δ₁=3/5, δ₂=1/7,
δ₃=1/64, δ₄^auto=2/313; automa-prodotto A(r;m,D) costruito, sound, verificatore dei 252 fantasmi
(§56). §57 ha declassato il pavimento del morso fresco; §58 ha mostrato che la non-localita'
`r=4` non erode. §59 ha falsificato il ponte diretto `deep_black -> lock`. §60 ha mostrato che
fresh-bite e' l'innesco locale. §61 ha mostrato che sui gate-lock lunghi il verdetto e'
esattamente la checklist T3'. §62 ha misurato il ricampionamento locale. §63 ha salvato
vettore e geometria. §64 ha misurato il modello/compressione vettoriale. §65 ha separato
diagnosi non-locale e teorema mancante. §66 ha mostrato che il profilo 22-porte lock-condizionato
seleziona sempre la fase reale. §67 ha falsificato i potenziali endpoint-monotoni semplici.
§68 ha ristretto il no-go alla forma lecita. §69 ha formulato `Φ_compat^L` come compatibilita'
prefissa con la migliore delle 22 porte e ha chiuso la versione endpoint (`best22_depth`).
**Novita' §71:** lo scanner di coppie co-raggiungibili trova un witness dinamico a `R=8`:
stesso patch locale `17x17`, stesso bit/fase T3', ma verdetto diverso per una cella relativa
`(15,13)` a offset 494, fuori da `B_8`. Questo prova non-vacuita' dinamica dello schema,
non un potenziale uniforme. A `R=16` zero collisioni esatte e' soprattutto baseline di
sparsita' del campione.
**Novita' §72:** il profilo dei 786 fallimenti T3' reali mostra che il discriminante cresce solo
nel frame grezzo: raw `max L∞` sale fino a **36**, ma nel frame co-moving W0 (sottratto
`floor(offset/104) * drift_phase`) collassa a **max L∞=9**. Quindi niente `door_debt_graph.py`
in coordinate grezze; il debt graph torna legittimo come test di Link 2 se usa classi intrinseche
co-moving. Link 1 resta il crux separato.
**Novita' §73:** sulle 131 classi co-moving di prima morte, la sonda pass/fail completa rigioca
tutti gli 810 tentativi e misura **101387** letture target: **91657 pass**, **9730 fail**,
pass-rate **0.9040**. **130/131** classi hanno almeno un pass e sono miste pass/fail; l'unica
zero-pass ha supporto debole (4 prime morti, 4 letture). La top class `(0,-5,-2,0)` non e'
un sabotaggio permanente: **4224 pass / 486 fail**. Link 3 resta vivo, ma va cercato come
vincolo GF(2) globale, non come riuso della stessa cella assoluta.
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
8. Dopo dedup `D>=80`, i tentativi porta unici sono **810**: **24 OK**, **786 KO**, hazard
   grezzo **0.0296**; fallimenti/orbita mediana **31.5**, max **50**, nessuna run maledetta.
9. La cella critica assoluta si riusa solo **1/762** coppie consecutive fallite e **1/12.945**
   coppie intra-orbita; L1 mediana tra celle critiche consecutive = **42**.
10. Il tipo di errore e' quasi senza memoria:
   `P(next frontier | prev frontier)=0.5227` vs `P(next frontier | prev missing)=0.5232`.
11. §63 salva **57.177** letture esogene su **810** tentativi porta; in **786/786** fallimenti
    la prima cella cattiva resta la morte esatta.
12. Nel vettore a due periodi i fallimenti hanno mismatch mediano **6** (q25 3, q75 10, max 29):
    la prima cella decide, ma il tentativo fallito spesso non e' quasi OK.
13. Geometria: stessa origine porta consecutiva **0/786**, L1 mediana origine **43**; stessa
    cella critica **1/762**. Il ricampionamento e' della porta, non solo dello sportello.
14. §64: il full-vector mantiene la diagonale: **786/786** fallimenti hanno mismatch, **24/24**
    OK no; il sotto-vettore a due periodi copre **774/786**, restano **12** collisioni di
    frontiera oltre offset 208.
15. La prima cella cattiva e' dominata da offset **45-77** (**598/786** prime morti);
    `98-99` resta necessario (**50** prime morti, e rimuoverlo perde **37** KO).
16. Mismatch totali: bucket `45-77` = **2797** celle, `104-207` = **1407**, `98-99` = **415**.
17. Compressione greedy: **37 offset esatti** o **66 componenti phase-conditioned** (su 542)
    mantengono la diagonale nel campione lungo.
18. §65 verifica la nota strategica: le prime morti sono dominate da offset **45-99**
    (**677/786**, non tutte); i **12** KO oltre due periodi sono tutti collisioni di frontiera
    a offset **268...1591**.
19. Le 12 celle tardive stanno a distanza relativa **L1 16...69** e **L∞ 10...36**:
    comprimere il numero di componenti non rende locale la checklist.
20. Dicotomia aggiornata: il locale/finito e' sigillato (Finestra, γ piccolo, T1/T2/α2/T3',
    §61, §64); il crux non-locale e' se il campo di detriti di un'orbita eterna puo' restare
    ostile a tutte le 22 porte mobili.
21. La baseline non condizionata resta utile come stress-test, ma **non** e' piu' la priorita'
    concettuale: nessun campione finito decide α1 (trappola controfattuale eterno).
22. **Correzione Pauli:** §65 e' diagnosi strategica/campionaria, non teorema. Per dire che T3'
    non e' determinata da un raggio finito serve il lemma: per ogni R esistono due campi uguali
    in B_R della porta ma con verdetto T3' diverso per una lettura esogena fuori B_R.
23. **Ridirezione concreta §66-a:** formalizzare quel lemma. Se usa campi sintetici, chiamarlo
    non-localita' sintattica; la versione dinamica richiede campi di detriti raggiungibili o una
    loro chiusura naturale.
24. **Ridirezione concreta §66-b:** costruire il `door-defect profile`: per ogni tentativo porta
    e per tutte le 22 fasi, misurare prima cattiva `h_g`, tipo, offset, distanza, `H=max_g h_g`
    agli orizzonti 208/512/1600, con leave-one-orbit-out e baseline anti-overfitting.
25. §66 implementa `alpha1/door_defect_profile.py`: **810** tentativi, **53.460** righe
    fase-orizzonte, orizzonti **208/512/1600**, runtime **69 s**, cross-check con §63:
    `compare_mismatches=0`.
26. Risultato §66: la fase reale e' **best unica in 810/810** per tutti gli orizzonti; a
    `L=1600` i **786** fallimenti hanno difetto entro orizzonte e i **24** ingressi sono clear.
27. Le fasi alternative compatibili col primo bit sono **11** per tentativo, ma muoiono tutte
    entro **5** letture esogene; le fasi incompatibili muoiono a `h=0`.
28. Interpretazione §66: il profilo 22-porte sui lock e' un controllo forte ma lock-condizionato,
    quasi tautologico. Ha aperto §67: lemma di non-localita' T3' + scanner non condizionato
    delle 22 porte sul campo di detriti.
29. Upgrade strategico prima di §67: §66 mostra un'asimmetria. Identificare la porta e' locale
    (off-phase compatibili muoiono entro 5); decidere se la porta vera entra e' globale
    (coda fino a offset 1591/L∞36).
30. La riformulazione globale e' qualitativa/di raggiungibilita', non un tasso: puo' riaprire
    strumenti combinatori/topologici ciechi alla versione-rate di α1.
31. Candidato §67, ora testato: cercare `Φ(detrito)` lower bounded, con decremento non sommabile a ogni
    rivisita nera profonda (ε uniforme oppure codominio discreto/ben fondato), `Φ=0` iff una
    porta entra, e non riducibile a prossimita' al lock (§59).
32. Caveat Pauli: il floor §58 e' evidenza empirica, non assioma dimostrativo; per provare serve
    una stima certificata o un ordine discreto. Lo scanner deve falsificare `Φ`, non provare α1.
33. Prima falsificazione pulita: segmenti tra gate-attempt consecutivi con eventi deep-black,
    nessun ingresso, ma `Φ(next) >= Φ(prev)`.
34. §67 implementa `alpha1/potential_segment_scanner.py`: ancore `gate` + `grid`, 24/24 orbite,
    **21.327** righe ancora, **21.183** segmenti, stride grid **1040**, runtime **~125 s**.
35. Gate, `L=1600`, segmenti deep/no-entry eleggibili **762**: `Φ_depth` viola **400/762**,
    `Φ_mass_104` **373/762**, `Φ_mass_208` **380/762**.
36. Grid, `L=1600`, segmenti eleggibili **6275**: `Φ_best22_depth` viola **3591/6275**,
    `Φ_best22_mass_104` **3150/6275**, `Φ_best22_mass_208` **3145/6275**.
37. Controlli §67: grid ha solo **2** clear finiti a `L=208/512` e **0** a `L=1600`; su gate
    `L=1600`, `best22_depth` coincide con la fase reale in **810/810**.
38. Lettura §67: i `Φ` naturali basati su prima morte e massa pesata dei mismatch non sono
    potenziali monotoni del campo di detriti. Deep-black e' driver/evento, non decremento di un
    potenziale endpoint-monotono finito.
39. §68 formalizza il no-go per questa classe di `Φ`, poi rimanda al lemma T3' con peso sulla
    realizzabilita'. Non riprovare `Φ_depth`/`Φ_mass` cambiando solo pesi.
40. Critic pass Pauli §68: dire "no-go empirico/testimoniale sul campione raggiunto", non
    "nessun potenziale finito funziona". Il test uccide solo proxy scalari endpoint-monotoni.
41. §68 implementa `alpha1/endpoint_monotone_audit.py`: nessuna nuova simulazione; legge i CSV
    §67, produce `endpoint_monotone_audit_summary.json` e `endpoint_monotone_audit_witnesses.csv`.
42. Gate `L=1600`, segmenti eleggibili **762**: `Φ_actual_depth` non-decrementi **400** e
    peggioramenti stretti **350**; `Φ_actual_mass_104` **373/371**; `Φ_actual_mass_208` **380/378**.
43. Grid `L=1600`, segmenti eleggibili **6275**: `Φ_best22_depth` **3591/2736** non-decrementi/
    peggioramenti stretti; `Φ_best22_mass_104` **3150/3149**; `Φ_best22_mass_208` **3145/3144**.
44. Nel quartile alto gate per deep-black (`>2609` eventi), `Φ_actual_mass_104` peggiora
    strettamente in **102/190** segmenti: il no-go non e' artefatto di segmenti poveri o pareggi.
45. Prossimo §69: schema T3'/realizzabilita'. Costruire coppie discriminanti con stesso dato
    locale intorno alla porta e verdetto T3' diverso per cella lontana; poi chiedere se sono
    raggiungibili da campi di detriti finiti.
46. Lettura strutturale post-§68: massa, area annerita, mismatch totali e deficit sommati non
    sono coordinate orientate. I flip locali depositano e ripuliscono, quindi i conteggi oscillano;
    non scrivere che la reversibilita' conserva massa, ma che rende i conteggi cattive coordinate
    Lyapunov.
47. Candidato §69: `Φ_compat^L`, non `Φ_mass`. Per ogni porta `g`, `h_g^L` = primo offset cattivo
    entro `L` (`L+1` se clear); `h_best^L=max_g h_g^L`; `Φ_compat^L=0` se `h_best^L=L+1`,
    altrimenti `exp(-h_best^L/104)`.
    Misura quanto avanti arriva la migliore porta, non quanti mismatch ci sono.
48. Caveat: la versione endpoint di `h_best` e' gia' ferita da §67/§68 (`Φ_best22_depth`).
    Quindi §69 deve cercare formulazione event-wise/amortizzata o di raggiungibilita', non
    ripetere lo scanner endpoint.
49. Le coppie discriminanti devono essere **co-raggiungibili**: due storie finite della formica,
    localmente indistinguibili alla porta, ma discordi nella cella lontana. Campi sintetici liberi
    provano solo non-localita' sintattica.
50. Gap aperto §69: `R(n)` e' censito a 40, mentre celle decisive osservate arrivano a offset
    1591 (anche se `L∞` relativo osservato arriva a 36). Il lemma dinamico deve portare questo
    caveat di scala.
51. §69 implementa `alpha1/compat_endpoint_audit.py`: nessuna simulazione; legge `best_h` dagli
    anchor §67 e produce `compat_endpoint_audit_summary.json` / `compat_endpoint_audit_witnesses.csv`.
52. `Φ_compat^L` endpoint: `h_g^L=first_bad_offset`, `h_best^L=max_g h_g^L`, `Φ=0` se clear
    fino a `L`, altrimenti `exp(-h_best^L/104)`. Equivalenza critica: e' `Φ_best22_depth`.
53. Gate `L=1600`: **762** segmenti deep/no-entry; `h_best` non migliora in **400/762**,
    peggiora strettamente in **350/762**.
54. Grid `L=1600`: **6275** segmenti deep/no-entry; `h_best` non migliora in **3591/6275**,
    peggiora strettamente in **2736/6275**.
55. Testimoni gate forti: orbita 2 `25->26`, deep **15099**, `h_best 45->45`; orbita 0
    `20->21`, deep **14244**, `47->45`; orbita 12 `15->16`, deep **13469**, `77->61`.
56. §70 non ha fatto un altro endpoint scanner: ha percorso entrambe le strade lecite, audit
    pre/post evento deep-black e schema T3'/co-raggiungibilita' formale.
57. `alpha1/compat_event_audit.py` misura `h_best^L` immediatamente prima/dopo singoli eventi
    deep-black (`pre=t`, `post=t+1`), con filtro `--min-event-t 1040` per evitare artefatti iniziali.
58. Run §70: 24/24 orbite, 25 eventi equispaziati per orbita, `L=1600`, **600** eventi,
    runtime **67.4 s**, nessun clear pre/post.
59. Risultato event-wise: `h_best` migliora in **243/600**, non migliora in **357/600**,
    peggiora strettamente in **259/600**, pari in **98/600**; mediana `delta_h_best=0`,
    min/max **-19/+16**, best phase cambiata in **492/600**.
60. Lettura §70: la monotonia immediata "ogni rivisita nera profonda avvicina una porta" e'
    falsa; restano solo credito/amortizzazione, ordine parziale/vettoriale, oppure prova senza
    potenziale scalare.
61. §71 implementa `alpha1/t3_coreachability_pair_scanner.py`: bucket esatto per patch locale
    normalizzato, bit osservato e fase T3' compatibile.
62. Witness dinamico §71: orbita 5, anchor grid `t=60320` e `t=60840`, `R=8`, fase 98,
    discriminante a offset **494**, cella rel **(15,13)** (`L∞=15>8`), `h_g^512=513 vs 494`,
    `h_g^1600=1014 vs 494`.
63. Correzione di lettura §71: `494 vs 513/1014` non rompe simmetria; la relazione richiede
    stesso dato locale e verdetto T3' diverso, non stesso futuro fuori finestra.
64. Controllo di sparsita' §71: sui gate/entry nessun bucket `h`-divergente; con griglia stride
    520 a `R=16` **0** collisioni esatte. Questo non e' un confine dinamico, solo il baseline
    atteso per patch `33x33`; implica solo che lo stesso anchor-set non puo' dare witness a
    `R=24/32/40`.

## B. Risultati delle ultime sessioni (§57-§71)

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

### B.8 Hazard/mixing della checklist (CHECKLIST-MIXING §62)
`alpha1/checklist_mixing.py` deduplica i lock `D>=80` gia' presenti come `D>=40` e analizza
le sequenze di gate-attempt da `lock_checklist_probe_rows.csv`. Runtime <1 s.

Risultato:
- tentativi porta unici: **810**;
- OK: **24**, KO: **786**, hazard grezzo **0.0296**;
- fallimenti prima dell'ingresso per orbita: min 24, mediana **31.5**, media **32.75**, max **50**,
  varianza **38.94** (molto sotto una geometrica iid col p globale, ma campione condizionato);
- fallimenti: `frontier_black_collision` 419, `missing_black` 367;
- transizioni: `frontier->frontier` 219, `frontier->missing` 190, `missing->frontier` 192,
  `missing->missing` 161, `frontier->OK` 10, `missing->OK` 14;
- riuso cella critica: **1/762** consecutivo, **1/12.945** intra-orbita; distanza L1 mediana 42.

Lettura: una cospirazione eterna non puo' essere locale-banale. Non basta tenere sbagliata
una cella, un tipo di dogana o una classe di parita'; dovrebbe essere un vincolo globale sul
campo di detriti che anticipa una sequenza di porte mobili.

### B.9 Vettore checklist + geometria porta (CHECKLIST-VECTOR §63)
`alpha1/checklist_vector_geometry.py` rigenera le 24 orbite, deduplica i gate-attempt come §62,
salva origine/heading della porta e ogni lettura esogena fino ad almeno due periodi
(`vector_horizon=208`) e comunque fino alla morte. Runtime completo: 68.6 s.

Risultato:
- tentativi porta unici: **810**; entry OK: **24**; fallimenti: **786**;
- letture esogene salvate: **57.177**; mismatch salvati: **5.806**;
- prima cella cattiva non coincidente con la morte: **0**;
- mismatch per fallimento nel vettore a due periodi: min 1, q25 3, mediana **6**, q75 10, max 29;
- stessa origine porta consecutiva: **0/786**; L1 origine mediana **43** (q25 17, q75 84.25);
- stessa cella critica: **1/762**; L1 critica mediana **42**;
- heading delta: `0:218`, `1:215`, `2:149`, `3:204`.

Lettura: non cambia solo la cella sbagliata, cambia la porta. Una protezione eterna deve
coordinare vettori su origini mobili, non solo preservare un bit locale.

### B.10 Modello vettoriale + compressione (CHECKLIST-VECTOR-MODEL §64)
`alpha1/checklist_vector_model.py` lavora solo sui CSV di §63, senza nuova simulazione. Misura
copertura dei mismatch per tipo, bucket, offset, fase, phase-offset e componente, poi fa una
compressione greedy tipo set-cover.

Risultato:
- full vector: diagonale perfetta (**786/786** KO coperti, **0/24** OK con mismatch);
- due periodi: **774/786** KO coperti, **12** KO mancati, tutti `frontier_black_collision`
  oltre offset 208 (offset 268 ... 1591);
- prime cattive per bucket: `45-77` = **598**, `98-99` = **50**, `00-44` = 77,
  `78-97` = 29, `100-103` = 14, `104-207` = 6, `208+` = 12;
- mismatch totali: `45-77` = **2797**, `104-207` = **1407**, `78-97` = 867,
  `98-99` = 415;
- set-cover: 37 offset esatti o 66 componenti phase-conditioned mantengono la diagonale
  sul campione lungo; `phase-offset` identifica gia' la cella relativa richiesta.

Lettura: la checklist si comprime ma non collassa a una singola dogana. Il blocco 45-77 e'
dominante, 98-99 resta necessario, e la coda frontier oltre due periodi impedisce di tagliare
rigidamente a 208 se si vuole la diagonale esatta.

### B.11 Non-localita' della checklist + ridirezione globale (CHECKLIST-NONLOCAL §65)
`docs/CHECKLIST_NONLOCAL_STRATEGY_ADDENDUM.md` registra la lettura strategica dei dati §61/§64.
La nota e' confermata con una correzione quantitativa: le prime morti non stanno tutte a 45-99,
ma quel blocco domina (**677/786**); i **12** KO mancati da due periodi sono frontiera lontana.
Il sottoagente Pauli aggiunge la correzione logica: questa e' evidenza di non-localita'
campionaria e fallimento del troncamento corto, non ancora un teorema di non-localita' dinamica.

Risultato:
- 45-99 = **677/786** prime cattive;
- due periodi = **774/786** KO coperti;
- 12 KO tardivi: offset **268, 273, 279, 298, 373, 488, 488, 492, 685, 799, 1533, 1591**;
- distanze relative dei 12 tardivi: L1 **16...69**, L∞ **10...36**;
- lettura: T3' decide esattamente, ma il dominio della decisione non e' catturato da un
  troncamento corto.

Conseguenza: il fallimento del pavimento del morso (§57), il ponte deep->lock falso (§59),
gli ostacoli del prodotto (§56.4) e la compressione non-localizzante (§64) sono manifestazioni
dello stesso punto: il matching d'ingresso e' globale. La domanda residua ha la forma:
un'orbita eterna puo' mantenere il campo di detriti ostile a tutte e 22 le porte mobili?
Prossimo passo operativo: lemma di non-localita' T3' + profilo globale dei difetti di porta.

### B.12 Door-defect profile lock-condizionato (DOOR-DEFECT-PROFILE §66)
`alpha1/door_defect_profile.py` valuta, per ogni tentativo porta deduplicato §63, tutte le 22
fasi/gate e misura `h_g(L)` per `L=208,512,1600`. Output: `door_defect_profile_rows.csv`,
`door_defect_profile_attempts.csv`, `door_defect_profile_orbits.csv`,
`door_defect_profile_summary.json`. Run completa: **24/24** orbite, **810** tentativi,
**53.460** righe fase-orizzonte, runtime **69 s**.

Controlli:
- self-test prima della run: `window_automaton.py --selftest` verde, `product_automaton.py --selftest`
  verde, `alpha1_engine.exe dump` vuota -> **9977**, `(7,-7)` -> **106258**;
- confronto con §63 sulla fase reale a `L=1600`: **0** mismatch.

Risultato:
- fase reale best unica: **810/810** a tutti gli orizzonti;
- `L=1600`: **786/786** fallimenti hanno difetto entro orizzonte, **24/24** ingressi clear;
- fasi compatibili alternative: **8100** righe per orizzonte, clear **0**, `h` mediana **2**,
  `h` massimo **5**;
- fasi incompatibili al primo bit: tutte `h=0`;
- coda oltre due periodi ritrovata: **12** fallimenti a offset 268...1591, tutti
  `frontier_black_collision`.

Lettura: il profilo 22-porte sui lock non e' ancora l'invariante globale. Condizionando su un
lock W0-like, la fase reale e' selezionata dal lock stesso; le altre fasi muoiono localmente.
Il crux globale sta prima: in un campo non condizionato, esiste qualche porta con `H_L` alto?
La forma piu' precisa e': identificare la porta e' locale; decidere il successo della porta
vera e' globale. L'invariante cercato vive nella seconda meta'.

### B.13 Potential segment scanner (POTENTIAL-SEGMENT-SCANNER §67)
`alpha1/potential_segment_scanner.py` testa, su ancore `gate` e `grid`, i candidati scelti con
Pauli: `Φ_depth=exp(-h/104)` e `Φ_mass(λ)=Σ_mismatch exp(-offset/λ)` per `λ=104,208`, piu'
le versioni `best22` sulle 22 porte. Output: `potential_segment_scanner_anchors.csv`,
`potential_segment_scanner_segments.csv`, `potential_segment_scanner_summary.json`. Run completa:
**24/24** orbite, **21.327** ancore, **21.183** segmenti, stride grid **1040**, runtime **~125 s**.

Test killer: segmento con eventi deep-black, nessun ingresso finale, ma `Φ(next) >= Φ(prev)`.
Risultato:
- gate `L=1600`: **762** segmenti deep/no-entry eleggibili; violazioni `Φ_actual_depth`
  **400/762**, `Φ_actual_mass_104` **373/762**, `Φ_actual_mass_208` **380/762**;
- grid `L=1600`: **6275** segmenti eleggibili; violazioni `Φ_best22_depth` **3591/6275**,
  `Φ_best22_mass_104` **3150/6275**, `Φ_best22_mass_208` **3145/6275**;
- su gate `L=1600`, `best22_depth` coincide con la fase reale in **810/810**; le masse differiscono
  poco (`mass104` 6/810, `mass208` 61/810), quindi il controllo best22 non salva la monotonia;
- grid ha **2** clear finiti a `L=208/512`, ma **0** a `L=1600`: erano artefatti di orizzonte.

Lettura: la famiglia naturale dei potenziali endpoint-monotoni finiti e' falsificata. Deep-black
resta un evento causale/ambientale, ma non induce un decremento endpoint-monotono di prima morte
o massa pesata dei difetti. Se un `Φ(detrito)` esiste, deve avere memoria/credito, un ordine
ben fondato non catturato da endpoint consecutivi, o una formulazione globale diversa.

### B.14 Endpoint-monotone no-go audit (ENDPOINT-MONOTONE-NOGO §68)
`alpha1/endpoint_monotone_audit.py` legge gli output §67 senza nuova simulazione e materializza
il no-go lecito: sui proxy scalari finiti testati, esistono segmenti raggiunti con deep-black,
nessun ingresso endpoint e `Φ(next) >= Φ(prev)`. Output:
`endpoint_monotone_audit_summary.json`, `endpoint_monotone_audit_witnesses.csv`.

Correzione Pauli integrata: questo e' un no-go empirico/testimoniale sul campione raggiunto,
non un teorema contro ogni potenziale globale. Uccide i proxy endpoint-monotoni e ogni
riparametrizzazione order-preserving di quei singoli scalari.

Risultato gate `L=1600`, **762** segmenti eleggibili:
- `Φ_actual_depth`: **400/762** non-decrementi, **350/762** peggioramenti stretti;
- `Φ_actual_mass_104`: **373/762** non-decrementi, **371/762** peggioramenti stretti;
- `Φ_actual_mass_208`: **380/762** non-decrementi, **378/762** peggioramenti stretti.

Risultato grid `L=1600`, **6275** segmenti eleggibili:
- `Φ_best22_depth`: **3591/6275** non-decrementi, **2736/6275** peggioramenti stretti;
- `Φ_best22_mass_104`: **3150/6275** non-decrementi, **3149/6275** peggioramenti stretti;
- `Φ_best22_mass_208`: **3145/6275** non-decrementi, **3144/6275** peggioramenti stretti.

Sanity: nel quartile gate piu' alto per deep-black (`>2609` eventi), `Φ_actual_mass_104`
peggiora strettamente in **102/190** segmenti. Il no-go non dipende da segmenti piccoli o da
pareggi.

Lettura strutturale: massa/area/mismatch non sono grandezze orientate. La formica deposita e
ripulisce tramite flip locali; quindi i conteggi oscillano e non sono buone coordinate Lyapunov.
La prossima coordinata sensata e' compatibilita', non quantita': per ogni porta `g`, misurare
`h_g^L`, il primo offset cattivo fino a orizzonte `L`, poi `h_best^L=max_g h_g^L`. Attenzione:
se si usa una somma/minimo di mismatch si ricade in `best22_mass`; se si usa endpoint
`h_best^L`, la famiglia e' gia' ferita da `Φ_best22_depth`. §69 deve quindi chiedere se esiste
una formulazione event-wise/amortizzata o di co-raggiungibilita' di `Φ_compat`.

Prossimo oggetto: `Φ_compat` + T3'/realizzabilita', non un nuovo `λ`.

### B.15 Compatibility potential endpoint audit (COMPATIBILITY-POTENTIAL §69)
`alpha1/compat_endpoint_audit.py` formalizza la versione endpoint di `Φ_compat^L` usando i CSV
gia' prodotti da §67. Nessuna nuova simulazione. Output: `compat_endpoint_audit_summary.json`,
`compat_endpoint_audit_witnesses.csv`.

Definizione:
- `h_g^L` = primo offset cattivo della porta `g` fino a orizzonte `L`;
- `h_best^L=max_g h_g^L`;
- `Φ_compat^L=0` se `h_best^L=L+1`, altrimenti `exp(-h_best^L/104)`.

Equivalenza critica: letto sugli endpoint, `Φ_compat^L` e' `Φ_best22_depth`. Non e' un nuovo
potenziale; §69 lo rende esplicito e lo chiude.

Risultati `L=1600`:
- gate: **762** segmenti deep/no-entry, `h_best` non migliora in **400/762**, peggiora strettamente
  in **350/762**;
- grid: **6275** segmenti deep/no-entry, `h_best` non migliora in **3591/6275**, peggiora
  strettamente in **2736/6275**;
- quartile gate alto per deep-black (`>2609`): **106/190** non-miglioramenti, **91/190**
  peggioramenti stretti.

Testimoni gate:
- orbita 2, gate `25 -> 26`, deep **15099**, `h_best 45 -> 45`;
- orbita 0, gate `20 -> 21`, deep **14244**, `h_best 47 -> 45`;
- orbita 12, gate `15 -> 16`, deep **13469**, `h_best 77 -> 61`.

Conclusione: compatibilita' endpoint morta come potenziale monotono netto. Resta aperta solo
una versione event-wise/amortizzata, oppure una prova via T3'/co-raggiungibilita' senza scalare
endpoint.

### B.16 Compat event + co-raggiungibilita' (COMPAT-EVENT/CO-RAGGIUNGIBILITA' §70)
`alpha1/compat_event_audit.py` e' il micro-audit non-endpoint: rigenera le 24 orbite lunghe,
campiona eventi deep-black, e valuta `h_best^L` subito prima/dopo il singolo passo.

Comando finale:
`C:\Python\Python310\python.exe alpha1\compat_event_audit.py --limit-orbits 0 --max-events-per-orbit 25 --min-event-t 1040 --max-seconds 300 --horizons 1600 --out-prefix alpha1\compat_event_audit`.

Risultati `L=1600`:
- **600** eventi, **24/24** orbite, 25 eventi per orbita;
- `h_best` migliora in **243/600**, non migliora in **357/600**, peggiora strettamente in
  **259/600**, pari in **98/600**;
- mediana `pre_h_best=5`, mediana `post_h_best=5`, mediana `delta_h_best=0`, media `+0.1517`;
- min/max `delta_h_best = -19/+16`;
- nessun clear pre/post;
- best phase cambiata in **492/600**.

Lettura: la monotonia event-wise ingenua e' falsificata. Una rivisita nera profonda non
avvicina sempre la migliore porta; puo' anche disallinearla. Questo non prova che nessun
potenziale globale esista: spinge verso credito/amortizzazione, ordine parziale/vettoriale o
schema T3'/co-raggiungibilita'.

Schema teorico §70: distinguere non-localita' sintattica da non-localita' su detriti
raggiungibili. La coppia utile e' `(H0,H1,g,n)`: due storie finite replayable, stessa porta
normalizzata e stesso dato locale su `B_R`, stessa fase/bit compatibile, letture precedenti non
distinguibili, e prima cella discriminante `e_n` fuori da `B_R`.

§71 ha implementato lo scanner e ha trovato un witness dinamico a `R=8`; vedi B.17.

### B.17 T3' co-raggiungibilita' pair scanner (§71)
`alpha1/t3_coreachability_pair_scanner.py` rigenera le 24 orbite, costruisce anchor gate/entry
e opzionalmente grid, normalizza il patch locale `D|B_R`, poi cerca bucket con stesso
`(R, L, observed_turn_bit, eval_phase, patch)` ma `h_g^L` diverso. Un witness viene accettato
solo se la prima cella discriminante e' fuori da `B_R`.

Run baseline gate/entry:
`C:\Python\Python310\python.exe alpha1\t3_coreachability_pair_scanner.py --limit-orbits 0 --max-seconds 300 --out-prefix alpha1\t3_coreachability_pair_scanner`.
Risultato: **810** anchor, **133650** eval, **133485** bucket, collisioni solo a `R=8`
(**22** per ogni `L`), ma **0** bucket `h`-divergenti.

Run positiva:
`C:\Python\Python310\python.exe alpha1\t3_coreachability_pair_scanner.py --limit-orbits 0 --max-seconds 300 --include-grid --grid-stride 520 --radii 8 --horizons 208,512,1600 --out-prefix alpha1\t3_coreachability_pair_scanner_grid520_r8`.
Risultato: **13394** anchor, **442002** eval, **441771** bucket, **44** bucket collidenti per
ogni `L`, **1** bucket `h`-divergente a `L=512` e `L=1600`.

Witness §71:
- orbita **5**, `rngstate=16489936061346709332`;
- anchor grid `5:grid:116` a `t=60320`, origine `(58,-26)`, heading `2`;
- anchor grid `5:grid:117` a `t=60840`, origine `(48,-36)`, heading `2`;
- stesso patch `R=8` (`17x17`), hash `1e838dafb7a51b780addaa3772ef0181`;
- fase valutata **98**, bit osservato **0**;
- discriminante T3' a offset **494**, cella relativa **(15,13)**, `L1=28`, `L∞=15`;
- requisito: bianca (`required_black=0`); caso cattivo: `frontier_black_collision`;
- `h_g^512`: **513 vs 494**; `h_g^1600`: **1014 vs 494**.

Controllo di sparsita' `R=16`:
`C:\Python\Python310\python.exe alpha1\t3_coreachability_pair_scanner.py --limit-orbits 0 --max-seconds 300 --include-grid --grid-stride 520 --radii 16 --horizons 208,512,1600 --out-prefix alpha1\t3_coreachability_pair_scanner_grid520_r16`.
Risultato: **13394** anchor, **442002** eval, **442002** bucket, **0** collisioni esatte.
Lettura: zero collisioni a `R=16` non ha peso strutturale forte; lo spazio dei patch `33x33`
e' enorme rispetto al campione. Dice solo che sugli stessi anchor non serve provare `R=24/32/40`.

Lettura: §71 trasforma la non-localita' da sintattica a dinamica osservata per `R=8`, perche'
le due configurazioni sono prefissi replayable della stessa orbita. E' una lettura di esistenza:
non prova una famiglia per ogni `R`, non muove α1, non sostiene da solo un potenziale uniforme,
e non sostituisce un argomento di closure/raggiungibilita' globale.

### B.18 Profilo `L∞` discriminante T3' vs profondita' lock (§72)

`alpha1/door_discriminant_linf_profile.py` profila il CSV §66 prima di costruire un grafo
dei debiti. Filtro: `kind=pre_onset_lock`, `is_actual_phase=1`, `clear=0`, `horizon=1600`.

Comando:
`C:\Python\Python310\python.exe alpha1\door_discriminant_linf_profile.py --horizon 1600 --out-prefix alpha1\door_discriminant_linf_profile`.

Risultato: **786** fallimenti T3' reali, **786** lock fisici unici, `depth == first_bad_offset`
in **786/786**. Tipi errore: **419** `frontier_black_collision`, **367** `missing_black`.
Massimi grezzi: `depth=1591`, raw `L∞=36`.

Rimisura co-moving W0:
- `40-77`: **675** casi, mediana `L∞=5`, max **9**;
- `78-103`: **93** casi, mediana `L∞=3`, max **7**;
- `104-207`: **6** casi, mediana `L∞=6`, max **7**;
- `208-511`: **8** casi, mediana `L∞=7.5`, max **8**;
- `512-1023`: **2** casi, mediana `L∞=7.5`, max **8**;
- `1024+`: **2** casi, mediana `L∞=7`, max **8**.

Casi estremi:
- orbita 21, attempt `21:26`, fase 24, depth **1591**, raw rel `(-36,-31)`,
  co-moving `(-6,-1)`, co-moving `L∞=6`;
- orbita 5, attempt `5:17`, fase 99, depth **1533**, raw rel `(-33,36)`,
  co-moving `(-5,8)`, co-moving `L∞=8`.

Lettura: la versione grezza del lemma della dogana ricorrente era nel frame sbagliato. Sottratto
il drift fase-dipendente della highway, il supporto resta piccolo: `comoving L∞<=9`, **131**
classi osservate `(phase, comoving_rel_x, comoving_rel_y, required_black, bad_kind)`. Quindi
`door_debt_graph.py` e' riaperto come test di Link 2 nel frame intrinseco, ma Link 1
("orbita eterna non-highway => lock W0-like profondi infinite volte") resta il crux.

### B.19 Pass-rate delle classi co-moving T3' (§73)

`alpha1/door_comoving_class_passrate.py` usa le 131 classi co-moving di prima morte §72 e
rigioca le 24 orbite per misurare tutte le letture T3' corrispondenti, passaggi inclusi.

Comando:
`C:\Python\Python310\python.exe alpha1\door_comoving_class_passrate.py --horizon 1600 --out-prefix alpha1\door_comoving_class_passrate`.

Risultato:
- **24/24** orbite, **810** tentativi porta;
- **131** classi target, **101387** letture evento;
- **91657** pass, **9730** fail, pass-rate **0.9040**;
- prime morti ritrovate: **786/786**;
- classi con almeno un pass: **130/131**;
- classi miste pass/fail: **130/131**;
- unica zero-pass: rank 46, `(phase=92, rel=(1,2), required=1)`, supporto **4** letture.

Top class:
`(phase=0, comoving=(-5,-2), required_black=0)` ha **78** prime morti su **78** celle
assolute diverse, ma sulle letture target complete fa **4224 pass / 486 fail** su **4710**.
Quindi non e' una dogana co-moving permanentemente sbagliata.

Lettura: Link 2 ha finitezza/ricorrenza; Link 3 non e' falsificato dal pass-rate. Pero' il
motore non puo' essere "stessa cella assoluta flippata due volte": il riuso assoluto resta
assente. La prossima macchina deve essere un grafo co-moving pass/fail e poi un vincolo GF(2)
globale sulle parita' di visita.

## C. Roadmap (priorita' prossima sessione §74)
1. **DECLASSATA: α1-come-pavimento-del-morso-fresco.** Misurata, erode (B.3). Non riaprire come
   liminf-che-decade da rincorrere via simulazione: stesso muro del controfattuale eterno (CLAUDE.md §1-i).
2. **FATTO §64: modello vettoriale.** Dominante 45-77, 98-99 necessario, due periodi quasi ma
   non totalmente sufficienti.
3. **FATTO §64 (prima passata): compressione del vettore.** 37 offset / 66 componenti mantengono
   la diagonale nel campione lungo, ma non localizzano geometricamente la checklist.
4. **FATTO §65: non-localita' campionaria della checklist.** T3' e' il verdetto esatto e legge
   celle lontane lungo il canale; questo falsifica il troncamento corto, ma non e' ancora un
   teorema dinamico.
5. **FATTO §70-a: schema T3'/co-raggiungibilita'.** Non sovra-investire sulla sola
   non-localita' sintattica: il peso vero e' la realizzabilita' delle coppie discriminanti da
   storie finite/campi raggiungibili.
6. **FATTO §66: `door-defect profile` sui lock.** La fase reale e' best unica 810/810; le
   fasi compatibili alternative muoiono entro 5 letture. Utile controllo, ma troppo condizionato
   per essere l'invariante globale.
7. **FATTO §67: candidati `Φ_depth`/`Φ_mass` e scanner segmentale.** I candidati naturali
   endpoint-monotoni sono falsificati: gate `L=1600` viola ~49-52%, grid ~50-57%.
8. **FATTO §68: no-go locale per `Φ` endpoint-monotoni finiti.** Prima morte, massa pesata,
   best22 e deficit finiti non forniscono decremento endpoint netto sotto deep-black. Non riaprire
   la stessa famiglia cambiando solo `λ` o troncamento.
9. **FATTO §69: formulare e chiudere `Φ_compat^L` endpoint.** Non massa del detrito:
   distanza-prefix dalla compatibilita' con una delle 22 porte. Endpoint = `best22_depth`, quindi
   falsificato come monotonia netta.
10. **FATTO §70-b: test pre/post evento `Φ_compat`.** `h_best` non migliora in **357/600**
   eventi deep-black e peggiora in **259/600**: la monotonia immediata ingenua e' chiusa.
11. **FATTO §71: scanner di coppie co-raggiungibili.** Witness empirico dinamico a `R=8`
   trovato. Interpretazione conservativa: solo non-vacuita' dello schema; `R=16` zero-collisioni
   e' sparsita' combinatoria, non confine strutturale.
12. **FATTO §72: profilo `L∞` raw + co-moving.** Sui 786 fallimenti reali, il raggio grezzo
   cresce fino a `L∞=36`, ma sottraendo il drift W0 fase-dipendente collassa a `L∞<=9`.
13. **FATTO §73: pass-rate classi co-moving.** Le classi top non sono sabotaggi deterministici:
   130/131 classi passano almeno una volta e sono miste pass/fail; la top class fa 4224/4710 pass.
14. **PRIORITA' §74: debt graph co-moving pass/fail + Link 1.** Computazionale: costruire
   `door_debt_graph.py` nel frame intrinseco W0 usando tutte le letture pass/fail, non solo
   prime morti. Teorica: formulare Link 1, cioe' perche' un'orbita eterna non-highway debba
   produrre lock W0-like profondi infinite volte. Solo dopo ha senso un sistema XOR/SAT globale GF(2).
15. **Se si cerca ancora un potenziale, deve cambiare forma.** Ammessi solo: compatibilita'
   event-wise/amortizzata, memoria/credito tra segmenti, codominio discreto/ben fondato con
   certificato, oppure potenziale globale del campo di detriti non leggibile da endpoint consecutivi.
16. **Invariante globale del campo di detriti.** La domanda precisa: puo' un'orbita
   eterna mantenere tutte le checklist sbagliate per sempre? Ora e' un problema qualitativo di
   raggiungibilita'/evitamento, non un tasso: riapre strumenti combinatori/topologici se formulati
   su questo livello.
17. **Campione baseline piu' ampio (secondario ma utile).** Usarlo come stress-test anti-overfitting
   della stabilita' delle componenti §64/§67, non come strada concettuale autonoma per decidere α1.
18. **Consolidamento (alternativa legittima).** Il locale sigillato, γ≤40, finestra r=4, prodotto sound
   sono teoremi: scrivibili come contributo a sé (riduzione a α1∧β∧γ + macchina) senza chiudere il crux.
19. **Coda PRODOTTO §56 (se si torna sul fronte certificazione):** rimozione cicli B-T nel prodotto
   (ostacolo A) e memoria temporale compatta (ostacolo B); poi r=4 ibrida δ^alt parziale.
20. **r=5 e γ esteso (42–52): SOLO dopo** — direttiva invariata.

## D. Domande aperte in coda (oltre la roadmap)
1. Checklist beta sui lock delle orbite lunghe: ponte locale confermato, mixing locale, geometria
   porta, compressione vettoriale, profilo 22-porte lock-condizionato, scanner §67, no-go §68,
   `Φ_compat` endpoint §69, pre/post event §70, witness co-raggiungibile `R=8` §71, profilo
   `L∞` discriminante §72 e pass-rate classi co-moving §73 misurati. Il crux resta prima del
   lock: Link 1 per orbite eterne, famiglia/closure co-raggiungibile robusta in raggio,
   debt graph co-moving pass/fail come Link 2/3, oppure potenziale con credito/amortizzazione.
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
  Sonda §62: `C:\Python\Python310\python.exe alpha1\checklist_mixing.py`.
  Sonda §63: `C:\Python\Python310\python.exe alpha1\checklist_vector_geometry.py`.
  Sonda §64: `C:\Python\Python310\python.exe alpha1\checklist_vector_model.py`.
  §65 e' un addendum strategico: `docs/CHECKLIST_NONLOCAL_STRATEGY_ADDENDUM.md`.
  Sonda §66: `C:\Python\Python310\python.exe alpha1\door_defect_profile.py`.
  Sonda §67: `C:\Python\Python310\python.exe alpha1\potential_segment_scanner.py`.
  Audit §68: `C:\Python\Python310\python.exe alpha1\endpoint_monotone_audit.py`.
  Audit §69: `C:\Python\Python310\python.exe alpha1\compat_endpoint_audit.py`.
  Audit §70: `C:\Python\Python310\python.exe alpha1\compat_event_audit.py --limit-orbits 0 --max-events-per-orbit 25 --min-event-t 1040 --max-seconds 300 --horizons 1600 --out-prefix alpha1\compat_event_audit`.
  Scanner §71: `C:\Python\Python310\python.exe alpha1\t3_coreachability_pair_scanner.py --limit-orbits 0 --max-seconds 300 --include-grid --grid-stride 520 --radii 8 --horizons 208,512,1600 --out-prefix alpha1\t3_coreachability_pair_scanner_grid520_r8`.
  Profilo §72: `C:\Python\Python310\python.exe alpha1\door_discriminant_linf_profile.py --horizon 1600 --out-prefix alpha1\door_discriminant_linf_profile`.
  Pass-rate §73: `C:\Python\Python310\python.exe alpha1\door_comoving_class_passrate.py --horizon 1600 --out-prefix alpha1\door_comoving_class_passrate`.
- **Builder C prodotto:** `product_build.exe <r> <m> <D> <outdir> [cap] [modo]` (0=full,1=black-only,
  2=ibrida); MAI il BFS Python del prodotto oltre poche migliaia di stati (esplode + swap, §56.6).
- **Niente Monitor con `tail -f`** (restano orfani "in esecuzione per ore"): seguire i run con Read
  sull'output o `until grep` che ESCE.
- Trappole cumulative: CLAUDE.md §1 (a–i) + RADIUS §50/§54.4/§55.2 + PRODOTTO §56.6 +
  **ALPHA1 §57.7** (reset-hash per-seme; survivorship temporale; controfattuale eterno; apofenia π·10⁵).
- Verbale prossima sessione: **§74**, stesso stile.
- Tempi tipici: build r4 20 s; A(2;4,5) prodotto 12,7 s; alpha1 search 31.7k semi/s; reseed 313k <1 s.
