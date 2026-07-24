# §108 — CONSOLIDAMENTO: riduzione a α1 ∧ β ∧ γ + macchina (v2 = §108b, decisioni del pannello applicate)

**Statuto di questo documento:** testa del consolidamento deciso a §107e.4
(regola preconcordata §107d.6.5). Il pannello §108 del titolare ha deciso
TUTTE e 17 le questioni DA CHIARIRE (verdetto 2026-07-24); §108b applica le
decisioni SENZA nuove simulazioni e senza claim nuovi (v1 in 34ada36).
I contenuti vivono nei due VOLUMI (entrambi v2 §108b):
- `docs/CONSOLIDATION_108_A.md` — fondamenta + linea del Muro/U2 (§40-§97):
  28 [T] + 21 [C] + 13 [O] + 12 [X]. Riconteggio §108b: INVARIATO — gli
  split A2/A6 riallocano contenuto già contato (il corno 3b era già A-X6;
  il certificato di T19-T3 era già A-C14). Le 9 questioni: DECISE.
- `docs/CONSOLIDATION_108_B.md` — certificati α1/β + linea record-side
  (§57-§75, §78-§86, §98-§107e): 15 [T] + 20 [C] + **35** [O] + 25 [X].
  Riconteggio §108b: +1 [O] (B3.35, violazioni-orizzonte fra catene,
  decisione B3). Le 8 questioni: DECISE.
Compilati da due lettori indipendenti sull'intera catena degli addenda,
versioni post-ERRATA (§107d.0, §107e.0) OBBLIGATORIE; nessun claim nuovo;
ogni voce cita § e file.

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

## Convenzioni canoniche (fissate dal pannello §108, vincolanti per ogni documento e strumento futuro)

- **Record y-min stretto (decisione A5).** Definizione canonica,
  all'istante subito prima della lettura: **y_t < min_{s<t} y_s**. Ne
  segue che il semipiano y ≤ y_t non è stato visitato dalla traiettoria
  precedente. La BIANCHEZZA segue soltanto aggiungendo y_t < y_min(seme).
  Heading-su e footprint in {y_rel ≥ 1} sono CONSEGUENZE nella convenzione
  temporale scelta, non parti della definizione.
- **Orizzonte del tripwire: V†_H(w) (decisione A3).** Nessun V†
  numericamente universale: V†_H(w) = prime letture fino all'orizzonte
  ESATTO del verdetto H. Per U1: H = 2600. Per Dicotomia / tripwire
  record-side: H = t† = max(2600, og_rec + 2080).
- **Convenzione og (decisione B4).** Eliminato "asse assoluto og+101".
  Si usano: **og_rec** = onset del germe misurato DAL RECORD; **og_win**
  = K + og_rec (indice nell'asse della parola concatenata); tempo assoluto
  dell'orbita = t_record + og_rec. Sempre **ride = d − og_rec**.
- **Tre nozioni di "fase" distinte (decisione B2).** Fase-checklist
  (§61–§66, E(k)), fase-GF(2) (§74), fase-porta / indice d'ingresso
  (§102–§104): tre simboli distinti, NESSUNA identificazione senza una
  mappa esplicita (mai eseguita, B-DC.2).
- **γ: dicitura unica (decisione A7).** "Nessuna orbita da configurazione
  iniziale finita ha linguaggio di svolte definitivamente periodico di
  periodo minimo ≤ 41." Dispari esclusi analiticamente; pari ≤ 40 per
  enumerazione chiusa. La dicitura "γ ≤ 40" è eliminata.
- **Cavalcate per-raggio (decisione A8).** Massimo 4 periodi per r ≤ 3,
  massimo 2 per r = 4 (potenze massime realizzabili, calcolate).

## 1. Architettura della riduzione (sintesi; dettagli nei volumi)

Bersaglio: nessuna orbita eterna non-highway (⇒ congettura dell'autostrada
per orbite da configurazione iniziale finita, dato γ sulla coda periodica).
Pilastri consolidati:
1. **Locale sigillato** [T]: Teorema della Finestra r=1..4 con tariffe
   esatte δ_r (A-T1/T2) — ogni eterna legge i.o. celle nere fuori-finestra
   9×9, tasso ≥ δ₄ = 2/313, salvo cavalcate finite di rotori espliciti
   (≤ 4 periodi a r ≤ 3, ≤ 2 a r = 4; tutte uccise: B-T/γ; i rotori r≥2
   sono impossibili come parole ancorate nel piano, B1.4).
2. **γ** [T]: nessuna orbita da configurazione iniziale finita ha
   linguaggio di svolte definitivamente periodico di periodo minimo ≤ 41
   (dispari analitici, pari ≤ 40 per enumerazione chiusa; A-T3). Il tratto
   42–102 resta aperto (A-X3).
3. **β (dogana)** [C]: due certificati complementari — δ_r (morsi,
   continuo) e il kernel co-moving della porta A1 §78 (one-shot ai lock:
   footprint 44, ρ≤9, unknown-free a P=15 sul campione). La
   stabilizzazione dell'impronta è [C], NON [T] (decisione B1), e NON
   implica un budget temporale P uniforme: il bound eterno di P e' Link 1
   visto dal lato porta (B4.21).
4. **Linea del Muro/U2** [T]+[X]: U1/Rigioco Bianco (A-T16), Parola Viva e
   Blocco Antico (A-T13-15), Nascita Vicina (A-T21), riduzione v2 ⟺ 8
   firme-exit (A-T24-26). T17 SPEZZATO (decisione A2): corni 1, 2, 3a =
   risultati parziali [T]; corno 3b = [X] (A-X6). Non esiste ancora un
   raggio unico del Muro: la forma rigorosa è per-parola (se
   B_∞(z_t, r_seed(w)) non interseca né l'origine né il supporto del
   seme, la parola finita certificata non è presentabile); il 63 è solo il
   massimo sulle 273.459 parole finite censite, non un bound globale.
5. **Linea record-side** [T]+[C]: Scala (B1.5), Dicotomia del Record (B1.7),
   Cuneo/Limite di Velocita' (B1.8-9), corollario OR (B1.10), kernel esteso
   R_{T,L} (B1.11: teorema deduttivo sotto le ipotesi del record stretto,
   implementazione verificata su 1.641 record; supporto word-decidibile,
   verdetto word+griglia).
6. **Crux operativo centrale della linea record-side** (correzione del
   pannello: "crux unico" era troppo forte): dimostrare
   **#{t : presentazione di classe κ a t ∧ ride(t) = d(t) − og_rec ≥ L₀}
   = ∞** — NON dimostrata (B4.20). Nel consolidamento compare SOLO questa
   forma (decisione B7; §104d = esclusivamente storia dell'errata).
   Restano formalmente aperti ANCHE: il corno 3b del Muro (A-X6),
   l'ipotesi (A) di onset finito per ogni parola presentabile (B4.22),
   e il tratto γ 42–102 (A-X3) — il crux può diventare "unico" soltanto
   dopo una riduzione esplicita di questi obblighi a quell'enunciato.
   Contesto fermo: la meta' "occorrenza" e' collassata su B-T (spettro
   identico); il fallimento-scudo e' realizzato 2/82k coi meccanismi
   §105b/§107c; le vie deduttive note per (ii) sono tutte chiuse (elenco
   B4.20/A-X6); H-NR (iniettivita' pura) uccisa (B4.18); riapertura
   empirica solo con invariante d'ordine nuovo, esplicito e preregistrato
   (specifica di ricerca §107e.0, non promossa).

## 2. §108b — le 17 decisioni del pannello (vincolanti, applicate)

Dal volume A (applicazione puntuale nella sezione DECISIONI in coda ad A):
- **A1 (burden1 K≤18 → A-T12, A-O6):** 18/16/14/10 conservati come minimi
  esatti del censimento chiuso NON filtrato; nel teorema soltanto
  burden1(w) ≥ m_K; il bound passa automaticamente al sottoinsieme vivo,
  ma NON è dimostrato che il minimo vivo sia raggiunto e valga esattamente
  10. Nessun ricalcolo.
- **A2 (Muro → A-T17, A-X6):** non esiste ancora un raggio unico del Muro;
  T17 spezzato (corni 1/2/3a [T] parziali, corno 3b [X]); forma rigorosa
  per-parola con B_∞(z_t, r_seed(w)); 63 = max censito su 273.459 parole,
  non bound globale.
- **A3 (V† → A-T16, A-C13, A-O7):** V†_H(w) per-verdetto (v. Convenzioni);
  U1: H=2600; Dicotomia/tripwire record-side: H = t† = max(2600, og_rec+2080).
- **A4 (0,0455 → A-C5, A-X1):** confermato [C] come esito certificato
  della specifica sequenza append-only di 252 tagli; l'inferenza a lower
  bound per δ₄^alt resta [X].
- **A5 (record stretto → Convenzioni):** definizione canonica
  y_t < min_{s<t} y_s; heading e footprint = conseguenze, non definizione.
- **A6 (D≤33 → A-T19, A-C14):** due strati — [T] teorema computer-assistito
  condizionale (con definizione di S_CORE, lemma di sovra-approssimazione
  sound, enumerazione esaustiva con massimo 33) + [C] certificato della
  macchina.
- **A7 (γ → A-T3, Convenzioni):** dicitura unica; "γ ≤ 40" eliminato.
- **A8 (cavalcate → A-T1/T2, Convenzioni):** costanti per-raggio
  dichiarate: ≤ 4 periodi a r ≤ 3, ≤ 2 a r = 4.
- **A9 (D(w101) → A-T13, A-O6):** citabile SOLO D(w101) = ∞; il 624 è un
  early-exit storico del testimone DFS; e D = ∞ NON dimostra la
  presentazione della parola lungo una singola orbita eterna.

Dal volume B (applicazione puntuale nella sezione DECISE in coda a B):
- **B1 (impronta A1 → B2.7):** [C], non [T]; i quattro tagli verificano
  una stabilizzazione finita; la promozione richiederebbe un lemma formale
  di periodicità-con-drift valido per ogni offset e tutte le 22 fasi; non
  implica comunque un budget temporale P uniforme.
- **B2 (fasi → Convenzioni):** tre simboli distinti per fase-checklist
  §61-66, fase-GF(2) §74 e indice porta/record §102-104; nessuna
  identificazione senza mappa esplicita.
- **B3 (0/1.223 vs 1/230 → B3.35, B4.24):** [O]+[X] — osservazioni su
  ensemble differenti, non una contraddizione né una stima di frequenza;
  il mancato rescan dei misti = debito ARCHIVIATO; campagna non riaperta.
- **B4 (og → Convenzioni, B2.17):** og_rec / og_win = K+og_rec / tempo
  assoluto t_record+og_rec; "asse assoluto og+101" eliminato; sempre
  ride = d − og_rec.
- **B5 (§79 → B2.8, B3.15):** solo [O]/SCOUT; nessuna promozione e nessuna
  riproduzione ora.
- **B6 (JSON §106d → B2.16):** il campo storico resta legacy con etichetta
  errata; semantica canonica "almeno una cella garantita"; il nome storico
  non è evidenza semantica; il dato non si altera retroattivamente.
- **B7 (Link 1 → pilastro 6, B4.19):** nel consolidamento compare soltanto
  #{t: classe-κ(t) ∧ ride(t) ≥ L₀} = ∞; §104d resta esclusivamente storia
  dell'errata.
- **B8 (quattro superstiti r=2,3 → B2.10):** si afferma soltanto il
  Teorema Halo e l'esistenza di ALMENO una classe realizzata dal
  testimone; nessuna realizzabilità attribuita separatamente a tutti e
  quattro.

## 3. Stato finale e regola di riapertura

Il programma consegna: locale sigillato (r≤4, tariffe esatte, cavalcate
≤4/≤2 per-raggio), γ (periodo minimo ≤ 41 escluso: dispari analitici,
pari ≤ 40 enumerati), due certificati β, una catena di teoremi di
vietanza (U1, Blocco Antico, Nascita Vicina) e la meccanizzazione esatta
del lato-record (Dicotomia, kernel esteso), piu' l'atlante delle strade
falsificate con le trappole (a-uu) — senza chiudere il crux operativo
centrale ne' gli altri obblighi formalmente aperti (corno 3b, ipotesi (A),
γ 42–102). Con §108b il consolidamento §108 e' CHIUSO come definitivo.
Riapertura del fronte empirico: SOLO con un invariante preregistrato che
soddisfi i 6 gate di §107d.6 (in particolare: ammettere il riuso dello
scudo, rango esplicito, monotonia dedotta, un controesempio uccide,
unknown mai no-entry). **§109 si apre soltanto davanti a un nuovo lemma o
a un invariante d'ordine esplicito e preregistrabile.**
