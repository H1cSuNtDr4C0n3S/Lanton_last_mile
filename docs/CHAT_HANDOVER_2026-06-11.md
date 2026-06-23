# CHAT_HANDOVER — Stato del programma Langton al 2026-06-11
**Da: sessione Claude.ai (fronti γ e morsi) → A: Claude Code in C:\langton_last_mile.**
**Leggere insieme a CLAUDE.md. Dettagli completi negli addenda in docs/ (numerazione § globale).**

## A. Stato del programma in dieci righe
La congettura è ridotta a: **α1 (ricorrenza dei lock) ∧ β (non-cospirazione della checklist) ∧ γ (esclusione delle asintotiche alternative)**. Il "locale" è SIGILLATO con quattro teoremi Lean-abili:
- **T1 (highway):** certificato finito 104·K + induzione di shift.
- **T2 (soglia):** Φ_ent = 22 porte esatte; fase k enterable ⟺ r(k)=∞; Jmax ≤ 7.
- **α2 (localizzazione):** L ≤ r(k), R* = 115, costante universale 116: ogni lock ≥ 116 passi è una porta.
- **T3′ (equivalenza):** ingresso ⟺ checklist esogena E(k) (celle ritardate + frontiera bianca), 0 FP / 0 FN su 8 famiglie avverse (diagonale perfetta).
Le dogane: P(ingresso | 5 dogane giuste al lock) = 0.918, P(| dogane 98/99 sbagliate) = 0.000 esatto (teorema: determinismo + lookback). I lock ricorrenti rimescolano la checklist ~iid (4 null puliti contro l'anti-teorema).

## B. Risultati delle ultime due sessioni (2026-06-11)

### B.1 Teorema γ sui periodi piccoli (GAMMA_ADDENDUM §29–35)
**Nessuna orbita da configurazione finita ha linguaggio di svolte definitivamente periodico di periodo minimo ≤ 41.** Dispari: esclusi analiticamente (rot(w) ≡ p mod 2 ⇒ mai ≡ 0 mod 4 ⇒ cammino limitato ⇒ Bunimovich–Troubetzkoy). Pari ≤ 40: enumerazione esaustiva con `gamma_enum.c` — 3,31 miliardi di parole realizzabili, 1,65 miliardi di candidate (rot≡0 mod 4 ∧ drift≠0), **zero superstiti** (morte: ~68% alternanza al wrap, ~32% fresca-L). Tre condizioni necessarie finite: (C1) rot/drift, (C2) alternanza eterna, (C3) zero prime-visite L nel regime stazionario (stabilizzazione tubi, induzione di shift). Bonus: censimento R(p) esteso a 40 (entropia code 0.729–0.735, terza misura concorde); chiralità riderivata gratis (W0 specchiata muore alla prima raffica di frontiera, offset 13). Il check è di **sola necessità** — un eventuale superstite a p>41 richiederebbe il secondo stadio (testimone T2-style). Gap 42–102: forza bruta fattibile fino a ~48–52 (×2,75 per passo di 2), oltre serve potatura teorica. **Direttiva di Michael: NON spingere γ ora; γ esteso è lo Step 4, dopo l'automa.**

### B.2 Fronte morsi (MORSO_ADDENDUM §36–44) — la sessione che consegna questo pacchetto
Morso = run massimale di letture fresche-bianche (≤ 4 esatto, riconfermato).
1. **Censimento a tre misure:** linguaggio esatto uniforme su R(20): tasso 0.455, morsi corti; transiente dinamico (150 run non distorti): tasso pooled 0.131 / per-run 0.178, **63% morsi tripli**, P(3|3)=0.727, gap dominanti 2 e 7 = i gap della highway; highway: 0.2115, 6 triple + 4 singole. La misura dinamica è highway-adiacente a livello blocchi.
2. **Legge del territorio:** A(t) ~ t^0.756 (R²=0.984) ⇒ tasso di morso ~ t^(−0.244), **nessun pavimento**; digiuni osservati fino a ~3.000 passi (13.9% dei passi in digiuni ≥312). corr(log n₀, tasso) = −0.941. Nota: α ≈ 3/4 ⇒ crescita compatta subdiffusiva r ~ t^(3/8) (da verificare universalità).
3. **TEOREMA DELLA FINESTRA (+ quantificazione §40.1):** automa a finestra (2r+1)×(2r+1) (sovra-approssimazione sana; stato = celle {ignota,bianca,nera} in frame canonico; leak = celle uscite dimenticate). Fatti calcolati: r=1: 15 stati, h=0.8114, esatto fino a n=8; r=2: 403 stati, h=0.7594; r=3: 45.971 stati, h=0.7441 (→ 0.734). **In tutti: entropia del sottografo senza-assumiB = 0 e parte ricorrente = rotori deterministici.** Cicli espliciti (canonici): C₁={LRRRR}, C₂={LLRRRR, (LLRRRR)², LLLLRLRRRRLRRRR}, C₃={LLLLRLRRRRLRRRR} — **stretta monotona, tutti uccisi** (rot ≢ 0 mod 4 o drift=0 ⇒ limitato ⇒ B–T; il p=12 verificato col γ-checker). TEOREMA: ogni orbita eterna legge infinitamente spesso celle nere fuori dalla finestra 7×7 ⇒ infinite rivisite nere profonde. Quantificazione: potenze massime realizzabili dei rotori = 3, 2, 1, 4; min tasso assumiB senza archi-rotore: δ₁ = 3/5, δ₂ = 1/7 (δ₃, δ₄ da calcolare — è il vostro task).

## C. Roadmap strategica (parole di Michael, vincolante)
"Non inseguire subito il periodo 104. Insegui la struttura che renderebbe necessario inseguirlo."
Tricotomia obiettivo per ogni orbita eterna non-highway: (1) lock profondi W0-like ricorrenti, (2) periodicità rivale (→ γ la uccide), (3) violazione di finitezza/alternanza/B–T.
- **Step 1 (IN CORSO — vostro task):** automa dei morsi a raggio crescente; SCC che evitano W0; rafforzamento del Teorema della Finestra a r=4,5; δ_r.
- **Step 2:** classificazione degli avoider — parole realizzabili che evitano fattori W0 di lunghezza ≥116: tendono a periodicità piccola / bassa rotazione / cammino limitato / infinite prime-visite nere / chiralità impossibile?
- **Step 3:** lemma ponte α1/γ: "se una parola in L_∞ evita lock W0 arbitrariamente profondi, allora è definitivamente periodica o contiene infiniti freschi neri" — il caso periodico va a γ, gli infiniti freschi neri violano la configurazione finita, la highway resta l'unica uscita.
- **Step 4 (solo dopo):** estendere γ a p=42–52 per uccidere i cicli falsi dell'automa.

## D. Domande aperte in coda (oltre il task immediato)
1. Ponte morsi→dogane: formalizzare le rivisite nere profonde come finestre di vincolo tipo-dogana anche fuori dalle cavalcate (§42.4).
2. α universale? Stimare l'esponente del territorio su famiglie diverse (§42.3).
3. Rafforzamento "∀r": se i rotori restano B–T/γ-uccidibili a ogni raggio, formulare il limite (non-località pura).
4. k=2 esaustivo (controllo, §28.5.2); sufficienza + Lean del pacchetto γ (§33.2.2); confronto proj_lat (AUC 0.33, vecchia pipeline) vs riga y=1 della checklist — richiede i file in C:\Langton_research.
5. L_∞ è NUMERABILE (§28.2): nessun argomento entropico/spettrale può chiudere α1 — non riaprire quel percorso (testimone: (RL)^∞, costo 0.004 bit).

## E. Igiene operativa
- I valori certificati per i self-test sono dentro `code/window_automaton.py` (--selftest) e nei summary in `results/`. MAI procedere con self-test rossi.
- Le trappole cumulative sono indicizzate negli addenda; le sei letali sono in CLAUDE.md §1.
- Convenzioni dinamica: CLAUDE.md §2 (INVARIATE — qualunque codice nuovo le rispetta o muore).
- Verbale di questa nuova fase: `docs/RADIUS_ADDENDUM.md`, numerazione da **§45**.
- Hardware: Ryzen 7 5800X (8C/16T); convenzioni di parallelizzazione: CLAUDE.md §4 + (se esiste) C:\Langton_research\claude.md che ha precedenza.
