# §108 — CONSOLIDAMENTO: riduzione a α1 ∧ β ∧ γ + macchina (v1, in attesa di pannello)

**Statuto di questo documento:** testa del consolidamento deciso a §107e.4
(regola preconcordata §107d.6.5). I contenuti vivono nei due VOLUMI:
- `docs/CONSOLIDATION_108_A.md` — fondamenta + linea del Muro/U2 (§40-§97):
  28 [T] + 21 [C] + 13 [O] + 12 [X] + 9 DA CHIARIRE.
- `docs/CONSOLIDATION_108_B.md` — certificati α1/β + linea record-side
  (§57-§75, §78-§86, §98-§107e): 15 [T] + 20 [C] + 34 [O] + 25 [X] +
  8 DA CHIARIRE.
Compilati da due lettori indipendenti sull'intera catena degli addenda,
versioni post-ERRATA (§107d.0, §107e.0) OBBLIGATORIE; nessun claim nuovo;
ogni voce cita § e file. Le 17 questioni DA CHIARIRE (sotto) sono decisioni
editoriali del pannello §108, NON risolte unilateralmente.

## Disciplina (imposta a §107e, vincolante)

Ogni affermazione appartiene a UNO dei quattro strati, dichiarato:
- **[T] Teorema universale** — enunciato con TUTTE le ipotesi (tipicamente:
  orbita eterna / non-highway / record y-min stretto / a profondita'
  dichiarata), luogo della prova (§), metodo (deduzione / enumerazione
  esaustiva CHIUSA).
- **[C] Certificazione finita dell'implementazione** — gate verdi,
  regressioni, e la dichiarazione esplicita di cio' che NON prova.
- **[O] Osservazione campionaria** — dato, campione, unita', scadenza
  (ogni soglia e' un quantile: trappola qq).
- **[X] Crux aperto / strada falsificata** — con la lettera di trappola.
Regole: niente promozioni implicite [O]→[T]; predicati etichettati per
supporto/verdetto (es. kernel esteso: supporto word-decidibile, verdetto
word+griglia).

## 1. Architettura della riduzione (sintesi; dettagli nei volumi)

Bersaglio: nessuna orbita eterna non-highway (⇒ congettura dell'autostrada
per orbite da configurazione iniziale finita, dato γ sulla coda periodica).
Pilastri consolidati:
1. **Locale sigillato** [T]: Teorema della Finestra r=1..4 con tariffe
   esatte δ_r (A-T1/T2) — ogni eterna legge i.o. celle nere fuori-finestra
   9×9, tasso ≥ δ₄ = 2/313, salvo cavalcate finite di rotori espliciti
   (tutte uccise: B-T/γ; i rotori r≥2 sono impossibili come parole ancorate
   nel piano, B1.4).
2. **γ** [T]: nessuna coda eterna di periodo minimo ≤ 41 (dispari analitici,
   pari ≤ 40 per enumerazione chiusa; A-T3; dicitura da uniformare, DC-A7).
3. **β (dogana)** [C]: due certificati complementari — δ_r (morsi, continuo)
   e il kernel co-moving della porta A1 §78 (one-shot ai lock: footprint 44,
   ρ≤9, unknown-free a P=15 sul campione; il bound eterno di P e' Link 1
   visto dal lato porta, B4.21).
4. **Linea del Muro/U2** [T]+[X]: U1/Rigioco Bianco (A-T16), Parola Viva e
   Blocco Antico (A-T13-15), Nascita Vicina (A-T21), riduzione v2 ⟺ 8
   firme-exit (A-T24-26) — corno 3b aperto (A-X6).
5. **Linea record-side** [T]+[C]: Scala (B1.5), Dicotomia del Record (B1.7),
   Cuneo/Limite di Velocita' (B1.8-9), corollario OR (B1.10), kernel esteso
   R_{T,L} (B1.11: teorema deduttivo sotto le ipotesi del record stretto,
   implementazione verificata su 1.641 record; supporto word-decidibile,
   verdetto word+griglia).
6. **Il crux (unico)**: Link 1 — forma vigente record-side (post
   §107d.0.10): **#{t : presentazione di classe κ a t ∧ ride(t) = d(t) −
   onset_germe(w_t) ≥ L₀} = ∞** — NON dimostrata (B4.20); la meta'
   "occorrenza" e' collassata su B-T (§104d, spettro identico), il
   fallimento-scudo e' realizzato 2/82k coi meccanismi §105b/§107c; le vie
   deduttive note per (ii) sono tutte chiuse (elenco B4.20/A-X6); H-NR
   (iniettivita' pura) uccisa (B4.18); riapertura empirica solo con
   invariante d'ordine nuovo, esplicito e preregistrato (specifica di
   ricerca §107e.0, non promossa).

## 2. Questioni per il pannello §108 (17 DA CHIARIRE, decisioni editoriali)

Dal volume A (dettagli in coda ad A):
- A1. Minimi burden1 K≤18 senza filtro di vitalita' (citarli come censimento,
  o riderivarli vivi).
- A2. Raggio dell'intorno del Muro da citare (13+bbox vs r_seed≤63 vs
  2+intorno, fusione 3a/3b).
- A3. Fissare la versione V† come canonica del tripwire d'orizzonte
  (coordinare con B).
- A4. Collocazione della barriera 0.0455 (in [C] con caveat — confermare).
- A5. Definizione canonica unica di "record y-min stretto".
- A6. Statuto di T3-D≤33 ([T]-condizionale vs [C]).
- A7. Dicitura γ ("nessuna coda eterna di periodo minimo ≤ 41; enumerazione
  chiusa sui pari ≤ 40").
- A8. Costanti di cavalcata per-raggio (≤4 a r≤3, ≤2 a r=4).
- A9. D(w101): citabile SOLO il certificato (=∞), mai il 624 del testimone.
Dal volume B (dettagli in coda a B):
- B1. Statuto della stabilizzazione dell'impronta A1 §78.3 ([T] o [C]).
- B2. Le tre nozioni di "fase" (§61-66 / §74 / §102-104) NON identificate
  senza mappatura (mai eseguita).
- B3. Tensione 0/1223 vs 1/230 violazioni-orizzonte (§100) + misti mai
  riscanditi (debito dichiarato).
- B4. Convenzione onset_germe (dal record, asse assoluto og+101) da
  dichiarare in ogni strumento futuro.
- B5. §79 citabile solo con statuto "scout" (mai riprodotto con
  alpha1_engine).
- B6. Refuso d'etichetta nel JSON §106d (dichiarato, non corretto).
- B7. Citare SOLO la forma corretta della riduzione (B4.19); §104d =
  formulazione storica.
- B8. Non attribuire realizzabilita' a tutti i 4 sopravvissuti r=2,3
  (basta il ⟺ del Teorema Halo).

## 3. Stato finale e regola di riapertura

Il programma consegna: locale sigillato (r≤4, tariffe esatte), γ≤41-minimo,
due certificati β, una catena di teoremi di vietanza (U1, Blocco Antico,
Nascita Vicina) e la meccanizzazione esatta del lato-record (Dicotomia,
kernel esteso), piu' l'atlante delle strade falsificate con le trappole
(a-uu) — senza chiudere il crux. Riapertura del fronte empirico:
SOLO con un invariante preregistrato che soddisfi i 6 gate di §107d.6
(in particolare: ammettere il riuso dello scudo, rango esplicito, monotonia
dedotta, un controesempio uccide, unknown mai no-entry).
