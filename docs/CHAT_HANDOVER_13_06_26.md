# CHAT_HANDOVER — Stato del programma Langton al 2026-06-13
**Da: sessione §56 (automa-prodotto temporale A(r;m,D)) → A: prossima sessione in C:\Lanton_last_mile.**
**Leggere insieme a CLAUDE.md. Dettagli completi: docs/PRODOTTO_ADDENDUM.md §56 (questa sessione);
catena precedente: docs/RADIUS_ADDENDUM.md §45–55; handover 06-11 archiviato in docs/CHAT_HANDOVER_2026-06-11.md.**

## A. Stato del programma in dieci righe
La congettura resta ridotta a **α1 ∧ β ∧ γ**; il "locale" è sigillato (T1, T2, α2, T3′ + dogane).
Stato del Teorema della Finestra (RADIUS): r=4 chiuso (27,3M stati, rotori tutti B-T), tariffe
certificate δ₁=3/5, δ₂=1/7, δ₃=1/64, δ₄^auto=2/313; il minimo del sovra-automa è un **fantasma**
(potenza realizzabile 0); 252 fantasmi tagliati, barriera empirica a 0.0455 ma **non** un lower
bound certificato (serve il Lemma A). Novità §56:
1. **Automa-prodotto A(r;m,D)** (finestra × memoria di celle uscite) **costruito, validato
   byte-per-byte (Python≡C), e dimostrato SOUND**: ogni orbita reale si solleva a costo invariante.
2. Come **verificatore** funziona: uccide **tutti i 252 fantasmi** del catalogo r=4 con memoria
   modesta (politica **ibrida nere-prima**, m=24, D=8 → 0 superstiti).
3. Come **certificatore di δ^alt** NON è ancora pronto: due ostacoli (vedi B.3) — il min cycle
   mean grezzo del prodotto scende **sotto** δ^auto perché spezza i rotori B-T.
4. Prima conferma diretta, dentro il prodotto, della tricotomia **δ^auto < δ^alt < δ^real**
   (r=1: minimo 1/8 alternanza-consistente ma gamma-REJECT per "fresca-L").

## B. Risultati di questa sessione (2026-06-13, §56)

### B.1 Infrastruttura (PRODOTTO §56.1–56.2)
`code/product_automaton.py` (prototipo+analisi+selftest+delta) e `code/product_build.c` (BFS C,
3 politiche memoria: full/black-only/ibrida, modo 0/1/2). Stato = finestra canonica {U,W,B,B*} ×
M (≤m celle uscite, box ‖·‖∞≤D, eviction deterministica). B* = nera nota solo da memoria: lettura
forzata che **paga** come assumiB. **Soundness provata e testata** (self-test 4/4 verde: m=0≡base
byte-identico; orbita reale mai bloccata a costo invariante; frame canonico≡assoluto; 252/252
fantasmi bloccati). Builder C ≡ Python byte-per-byte in tutte e 3 le politiche. **C ~3000× più
veloce**: A(2;4,5) 17,3M stati in 12,7 s.

### B.2 Verificatore del catalogo (PRODOTTO §56.3) — SUCCESSO
Copertura 252 fantasmi r=4: ibrida nere-prima **m=24,D=8 → 0 superstiti** (full nearest serve
m=32; black-only non arriva a 0 a D=8). I fantasmi mentono a corto raggio: memoria modesta + nere
prioritarie li copre tutti. Conferma quantitativa della firma RADIUS §55.2.

### B.3 Certificatore di δ^alt (PRODOTTO §56.4–56.5) — DUE OSTACOLI
Testimoni (doppio certificato ciclo+fixpoint intero, `code/check_witnesses.py`):
- A(1;2,8): δ=**1/8**, NO-B-T, **alternanza-OK**, gamma-REJECT (fresca-L) — δ^alt<δ^real confermato.
- A(2;2,8): δ=**2/70**, NO-B-T, **FANTASMA d=52** (m=2 insufficiente); A(2;4,8): 2/71, B-T, fant. d=64.

Il minimo del prodotto è **sotto** δ^auto (0.125<0.6; 0.029<0.143). Cause:
- **Ostacolo A (trappola nuova):** il prodotto **spezza i rotori B-T** del base (r=1: p5 sparisce;
  r=2: restano solo p15) e li riespone come cicli paganti-poco. Sono B-T ⇒ cavalcabili finitamente
  ⇒ non contano nel liminf. **Va rimosso ogni ciclo B-T PRIMA del min-cycle-mean** (oggi si tolgono
  solo i rotori-prodotto). Istanza al prodotto della trappola (e) CLAUDE.md §1.
- **Ostacolo B:** i fantasmi NO-B-T profondi (conflitto a d=52) richiedono m≥16, ma la **memoria
  spaziale (m,D) esplode**: r=1 m=16 e r=2 m=8 superano 40M stati; black-only peggio. Sufficiente
  ⇒ non computabile come automa completo.

## C. Roadmap (priorità prossima sessione)
1. **Rimozione dei cicli B-T nel prodotto** (ostacolo A): estendere `gen_rotor_edges.py`/
   `min_assumeB.c` al prodotto eliminando ogni ciclo con rot≢0 mod4 o drift=0. Verificare a r=1,2
   che il min-cycle-mean RISALGA sopra δ^auto: solo allora è un candidato δ^alt sano.
2. **Memoria temporale compatta** (ostacolo B): codificare l'ultimo colore visto solo per le celle
   toccate negli ultimi k passi, indicizzate per *tempo* d'uscita non per posizione (intuizione di
   Michael, RADIUS §55.4). Misurare la crescita stati vs (m,D); k(ε) limitato al crescere di ε?
3. **Prodotto r=4 con memoria minima + ibrida** (l'ibrida copre il catalogo a m=24), δ^alt parziale;
   stimare gli stati col cap prima di lanciare.
4. Solo dopo 1–3: confronto coi minimi reali su sliding window (RADIUS §55.3).
5. **r=5 e γ esteso (42–52): SOLO dopo** — direttiva invariata.

## D. Domande aperte in coda (oltre la roadmap)
1. Lemma A (alternanza taglia i fantasmi) e Lemma B (memoria antica non eternamente economica) —
   RADIUS §55.4: il prodotto È la via di certificazione del Lemma A, una volta tolto l'ostacolo A.
2. Congettura B–T-autosufficienza (RADIUS §51.5): ogni parola di rotore ha rot≢0 mod4 o drift=0?
3. Ponte morsi→dogane (§42.4) con tasso 2/313 a escursione ≥4; α universale (§42.3); Lean γ (§33.2.2).
4. L_∞ NUMERABILE (§28.2): non riaprire percorsi entropici/spettrali per α1.

## E. Igiene operativa
- **Self-test PRIMA di tutto:** `python code\window_automaton.py --selftest`,
  `python code\analyze_radius.py --selftest`, `python code\product_automaton.py --selftest`. MAI rossi.
- **Macchina:** Ryzen 5800X, **16 GB RAM (limite vero)**; Python numpy/scipy SOLO
  `C:\Python\Python310\python.exe`; gcc = `C:\Strawberry\c\bin\gcc.exe`; stdout cp1252 ⇒
  `sys.stdout.reconfigure(encoding="utf-8")`.
- **Builder C (sempre, per istanze non minuscole):** `product_build.exe <r> <m> <D> <outdir> [cap] [modo]`
  (modo 0=full,1=black-only,2=ibrida); `window_build.exe`, `min_assumeB.exe`, `gamma_enum.exe check`.
  **MAI il BFS Python del prodotto oltre poche migliaia di stati** (esplode + swap: incidente §56.6).
- **Niente Monitor con `tail -f`** (restano orfani "in esecuzione per ore"): seguire i run con Read
  sull'output o `until grep` che ESCE.
- Binari riusabili: `build/` (r1–r4 base ~2 GB; p* del prodotto), `build_pyval/` (validazione hash).
  Catalogo fantasmi `results/delta4_alt_catalog.jsonl`; testimoni `build/*_delta_cycle*.txt`.
- Trappole cumulative: CLAUDE.md §1 + RADIUS §50/§54.4/§55.2 + **PRODOTTO §56.6** (rotori spezzati;
  black-only esplode; BFS Python del prodotto; Monitor tail -f).
- Verbale prossima sessione: **§57**, stesso stile.
- Tempi tipici: build r4 20 s; analisi r4 70 s; A(2;4,5) prodotto 12,7 s; self-test prodotto <30 s.
