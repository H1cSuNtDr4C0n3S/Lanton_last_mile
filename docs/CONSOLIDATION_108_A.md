# §108 — INVENTARIO METÀ A: fondamenta + linea del Muro/U2 (§40–§97) (v2 = §108b)

Perimetro: Teorema della Finestra e δ_r (MORSO §40–40.1, RADIUS §45–55), γ
(GAMMA §29–35), automa-prodotto (PRODOTTO §56), Scia (§86), Cono/Spoiler
Vecchio (§87), Parola Viva (§88), censimento record + Blocco Antico (§89),
dicotomia/ARMA/Muro (§90), U1 (§91), U2 (§92–§97). NON copre §98+.
Etichette per strato come da `docs/CONSOLIDATION_108.md`: [T]/[C]/[O]/[X].
Dove un risultato è stato poi corretto/ritirato, qui compare SOLO la versione
corretta, con nota della correzione. Nessun claim nuovo.
**§108b:** le 9 questioni DA CHIARIRE sono state DECISE dal pannello §108
(verdetto 2026-07-24) e le decisioni sono applicate in questo volume
(sezione DECISIONI in coda; v1 in 34ada36; nessuna nuova simulazione).

Convenzioni presupposte (CLAUDE.md §2): bianco→R, nero→L, flip dopo lettura,
poi mossa; W0 periodo 104, drift (±2,±2); onset griglia vuota 9977.
"Record y-min stretto" (definizione CANONICA, decisione §108b-A5):
all'istante subito prima della lettura, **y_t < min_{s<t} y_s**; ne segue
che il semipiano y ≤ y_t non è stato visitato dalla traiettoria precedente;
la BIANCHEZZA segue soltanto aggiungendo y_t < y_min(seme); heading-su e
footprint delle ultime K svolte in {y_rel ≥ 1} sono CONSEGUENZE nella
convenzione temporale scelta (§87.6, §91a), non parti della definizione.
Orizzonti dei tripwire (decisione §108b-A3): nessun V† numericamente
universale — V†_H(w) = prime letture fino all'orizzonte ESATTO del
verdetto; U1: H = 2600; record-side: H = t† = max(2600, og_rec+2080)
(og_rec: convenzione §108b-B4, testa §Convenzioni).
"Frame anchor" = posa finale in origine, heading-su. Convenzione bit dei
certificati U2 (fissata a verbale §95b): bit 1 = R = lettura BIANCA,
bit 0 = L = lettura NERA.

---

## 1. [T] TEOREMI UNIVERSALI

### 1.A Fondamenta (finestra, γ, prodotto)

**T1. Teorema della Finestra (r = 1..4).** Ipotesi: orbita eterna della
formica di Langton da configurazione iniziale finita. Tesi: l'orbita legge
infinitamente spesso celle nere fuori dalla propria finestra di memoria
(2r+1)×(2r+1) per r = 1,2,3,4 (fino a 9×9); poiché le prime-visite nere sono
finite, compie infinite rivisite nere a escursione ≥ r.
Dove: MORSO §40 (r=1,2), §40.1 (r=3), RADIUS §47 (r=4);
`docs/MORSO_ADDENDUM.md`, `docs/RADIUS_ADDENDUM.md`.
Metodo: enumerazione esaustiva CHIUSA del window-automaton (BFS completo:
15 / 403 / 45.971 / 27.297.183 stati); entropia del sottografo senza-assumiB
= 0 esatto a ogni raggio; parte ricorrente = unione di rotori deterministici
con parole cicliche esplicite (r=4: 3 parole, p=10/20/74), tutte uccise da
Bunimovich–Troubetzkoy (teorema esterno citato) — a r=4 senza bisogno del
γ-checker; a r≤3 alcune uccise dal γ-checker (drift=0).
Caveat: (i) l'automa è una SOVRA-approssimazione: si trasferiscono solo
enunciati "ogni cammino infinito fa X" (trappola c); (ii) C₄ ∩ C₃ = ∅ —
nessun annidamento dei rotori tra raggi (trappola §50); (iii) le cavalcate
dei rotori sono finite: ≤ 4 periodi a r≤3, ≤ 2 a r=4 (potenze massime
realizzabili, calcolate).

**T2. Tariffa esatta δ_r (quantificazione del Teorema della Finestra).**
Ipotesi: ogni comportamento eterno che non sia una cavalcata finita di un
rotore esplicito (costanti per-raggio, decisione §108b-A8: ≤ 4 periodi a
r ≤ 3, ≤ 2 a r = 4). Tesi: frequenza asintotica di letture
nere fuori-finestra ≥ δ_r, con δ₁ = 3/5, δ₂ = 1/7, δ₃ = 1/64, δ₄ = 2/313.
Dove: MORSO §40.1, RADIUS §48; `code/min_assumeB.c`,
`results/radius{1..4}_summary.json`, testimoni `build/r*_delta_cycle.txt`.
Metodo: doppio certificato — ciclo testimone esplicito (upper bound) +
fixpoint in aritmetica intera (lower bound); il fatto "sottografo noB privato
degli archi-rotore è un DAG" è VERIFICATO a runtime (Kahn, abort se non
copre), non assunto.
Caveat obbligatori: (a) il min cycle mean sul grafo pieno è banalmente 0 —
la quantificazione ha senso solo senza archi-rotore (trappola e); (b) il
minimo è raggiunto SOLO da cicli irrealizzabili: il testimone δ₄ ha potenza
massima realizzabile 0 (viola l'alternanza già alla prima ripetizione, §54.1)
⇒ δ₄ è lower bound sano ma il pavimento reale delle orbite è strettamente
più alto (δ₄^real, mai calcolato — [X]); (c) l'enunciato sano è "ogni cammino
paga ≥ δ", MAI "esiste orbita che paga δ" (§54.4).

**T3. Teorema γ (code periodiche, periodi piccoli).** Ipotesi: orbita da
configurazione iniziale finita. Tesi: il linguaggio di svolte NON è
definitivamente periodico di periodo minimo ≤ 41.
Dove: GAMMA §32; `code/gamma_enum.c`, `data/gamma_enum.pkl`.
Metodo: p dispari esclusi ANALITICAMENTE (rot(w) ≡ p mod 2 ⇒ mai ≡ 0 mod 4,
§30.2, con B–T per il caso limitato); p pari ≤ 40 per enumerazione esaustiva
CHIUSA (3,31 miliardi di foglie realizzabili, 1,65 G candidate al check
completo, ZERO superstiti; coerenza interna alternanza+fresca-L+superstiti =
candidate esatta a ogni p).
Caveat: il check è di sola NECESSITÀ (C1 rot/drift + C2 alternanza eterna +
C3 zero prime-visite-L stazionarie): un eventuale superstite NON sarebbe
automaticamente una coda eterna (punto vacuo qui, da ricordare se si estende
p, §33.1). W0 (p=104) resta l'unica coda eterna nota; il gap 42–102 è aperto.

**T4. Soundness dell'automa-prodotto A(r;m,D).** Ipotesi: nessuna (proprietà
della costruzione). Tesi: ogni orbita reale si solleva a un cammino del
prodotto coi colori ricordati veri; l'eviction è solo perdita d'informazione;
il costo assumiB lungo la proiezione è invariante in (m,D) ⇒ il min cycle
mean del prodotto è un lower bound sulla tariffa di OGNI cammino infinito
auto-consistente a orizzonte (m,D) (chiude in linea di principio il caveat
aperiodico di RADIUS §55.4).
Dove: PRODOTTO §56.1; `code/product_automaton.py`, `code/product_build.c`.
Metodo: dimostrazione + self-test (§56.2).
Caveat FONDAMENTALE: la soundness NON produce δ^alt — come certificatore il
prodotto ha due ostacoli aperti ([X]): (A) spezza i rotori B–T del base e li
riespone come cicli economici (min grezzo < δ^auto, privo di significato
senza rimozione preventiva dei cicli B–T — trappola §56.6); (B) la memoria
spaziale esplode prima di chiudere (m≈16–24 necessario, fuori portata).

### 1.B Scia, lock, cono, spoiler (§86–§87)

**T5. Teorema della Scia.** Ipotesi: t lettura nera deep_1 (cella visitata,
fuori dalla finestra viva 3×3) di QUALSIASI orbita (finita o eterna).
Tesi: nel frame heading-su almeno una delle tre celle di scia
{(0,1),(−1,1),(−1,0)} è nera al tempo t con età ≤ 3 (precisamente: la cella
d'ordine j della più recente svolta R tra t−1..t−3 è nera con età j; se le
tre svolte sono L,L,L, pos(t−4) = centro ⇒ la lettura non è deep:
contraddizione).
Dove: §86.1, `docs/TRAIL_HALO_ADDENDUM.md`.
Metodo: deduttivo (induzione all'indietro sulla geometria d'arrivo).
Corollari (tutti teoremi, per ogni orbita incluse le eterne): (1) nessuna
lettura deep inizia (LRRRR)³ — l'evitamento §84/§85 non è più statistica
(la trappola i cade per QUESTO enunciato); vale a fortiori per deep_2..4;
(2) lo 0% di motivi potati vuoti ai deep (§81) è teorema; (3) halo bianco a
t≥4 ⇒ svolte(t−4..t−1) = R,L,L,L e pos(t−4) = centro (firma di ogni
cavalcata: in-finestra, mai fresca, mai deep).
Caveat: copre l'INIZIO di (LRRRR)³ alla lettura, nulla su code parziali di
cavalcata (§86.5). Trappola (u): ogni statistica di vicinato ai deep va prima
scontata del contributo di scia.

**T6. Teorema-lock di prima-lettura (⟺) e impossibilità dei rotori r≥2.**
Enunciato: una parola di svolte W parte dalla lettura corrente ⟺ ogni cella
primo-letta durante W ha il colore richiesto (L=nera, R=bianca) al momento
iniziale (riletture forzate dall'alternanza); se una rilettura contraddice,
W è irrealizzabile da lettura singola in QUALSIASI ambiente.
Conseguenza esatta (calcolo diretto su tutte le rotazioni ×3 periodi):
LLRRRR (rotore r=2) 0/6 rotazioni realizzabili, LLRRLLRRRR (p10) 0/10 —
quelle parole sono IMPOSSIBILI come parole di lettura ancorate nel piano
(esistono solo nell'astrazione a finestra); p15 15/15 realizzabili col lock
canonico {centro + 3 celle di scia + (1,0)} neri.
Dove: §86.3, `alpha1/word_lock.py`. Metodo: deduttivo + calcolo esaustivo
delle rotazioni; verifica necessità (ogni flip rompe) + sufficienza (1000
ambienti junk).

**T7. Lemma del Replay-Lock.** Ipotesi: corsa finita di T passi da posa
(x,y,h) su ambiente E; V_T = celle lette con i colori iniziali.
Tesi: (sufficienza) ogni E' che coincide con E su V_T produce stessa parola
e traiettoria per T passi; (necessità per-cella) cambiare il colore iniziale
di una cella di V_T cambia la parola esattamente alla sua prima lettura.
V_T è il lock esatto word-minimale della corsa.
Dove: §87.1, `docs/CONE_LOCK_ADDENDUM.md`, `alpha1/onset_cone_lock.py`.
Metodo: deduttivo (induzione sui passi).

**T8. Lemma del Cono (+ affitto periodico esatto).** Ipotesi: le 5 corse
d'ingresso certificate (germi: vuota 9977, b1 310, b2 162, b3 142, (7,−7)
106258). Tesi: in QUALSIASI orbita, a QUALSIASI istante, se tutte le celle
del cono C(posa(t)) (lock ruotato/traslato) hanno i colori richiesti,
l'orbita replica la corsa ed entra in autostrada; il lock eterno è
finitamente descritto: blob pre-onset + striscia periodica di ESATTAMENTE 22
celle nuove/periodo (co-moving stabilizzato dal periodo 0). La parte
semi-infinita della striscia oltre il supporto nero corrente è bianca gratis
⇒ condizione finita.
Corollario (prima forma di Link 1 con denti): un'orbita eterna non-highway
deve avere, in ogni istante, almeno una cella nera dentro il Cono Bianco
C_0(posa(t)); le 3 celle di scia stanno nel blob in tutti i casi.
Dove: §87.2. Metodo: Replay-Lock (T7) + certificati finiti delle corse
(gate 5/5). Caveat: condizionale ai germi della libreria (per ciascun germe:
o un nero nella parte bianca-richiesta o pattern del germe sbagliato).

**T9. Lemma della Finestra-K.** Ipotesi: ogni orbita, ogni istante t ≥ K,
w = svolte(t−K..t−1). Tesi: (a) w è realizzabile; (b) il footprint F(w)
delle celle toccate negli ultimi K passi e i loro colori al tempo t sono
funzione di w sola. Dove: §87.3. Metodo: deduttivo (induzione; duale del
Replay-Lock), verificato su dati reali (150 sonde, 0 mismatch).

**T10. Teorema dello Spoiler Vecchio (scala K ≤ 14).** Ipotesi: orbita
eterna non-highway; K ∈ {6,8,10,12,14}. Tesi: in OGNI istante t ≥ K esiste
una cella nera in V(w(t)) \ F(w(t)): un nero NON toccato negli ultimi K passi
(età-di-tocco ≥ K), a distanza Chebyshev ≤ 68 (mediana 15) dalla formica.
Dove: §87.3, `alpha1/kwindow_spoiler_census.py`.
Metodo: condizionato SOLO al censimento esaustivo CHIUSO: tutte le parole
realizzabili a K = 6..14 (50/154/448/1300/3680) hanno germe di finestra-K
che fa onset (ZERO buchi) ⇒ per T8+T9 un'eterna deve avere uno spoiler.
Caveat (trappola v): lo spoiler può essere la propria scia invecchiata
(cella dipinta K+1 passi fa); NESSUN K finito chiude per camping — la leva è
la geometria ai record, non l'esistenza dello spoiler.

**T11. Lemma delle streak cappate.** In OGNI orbita le streak di L e di R
sono ≤ 4 (quattro svolte uguali chiudono un quadrato sulla cella di partenza
già riscritta; la quinta rileggerebbe il colore originario). Dove: §87.3.
Metodo: deduttivo elementare, certificato anche dal filtro di realizzabilità
(all-L/all-R scartate a ogni K ≥ 5).

**T12. Teorema della checklist ai record (K ≤ 18; forma decisa §108b-A1).**
Ipotesi: orbita eterna non-highway; pose-record y-min stretto; w = ultime K
svolte (necessariamente record-compatibili: footprint ⊆ {y_rel ≥ 1}).
Tesi: deve esserci un nero di età ≥ K in una checklist di burden1(w) celle
specifiche, con **burden1(w) ≥ m_K**, dove m_K = 18/16/14/10 a
K = 12/14/16/18 sono i minimi ESATTI del censimento esaustivo chiuso NON
filtrato per vitalità; nessuna parola-arma (burden1=0) esiste a K ≤ 18.
Dove: §87.6, `alpha1/spoiler_quadrant_profile.py`.
Metodo: condizionato al censimento (esaustivo per quei K) + T8/T9.
Caveat (trappola w; decisione §108b-A1): il bound burden1(w) ≥ m_K passa
AUTOMATICAMENTE al sottoinsieme vivo; NON è invece dimostrato che il minimo
vivo sia raggiunto né che valga esattamente 10 (i minimi vivi per K ≤ 18
non sono stati ricalcolati; il pannello ha deciso: nessun ricalcolo). Resta
la lezione §87e-2/§88: un teorema-parola ai record è VACUO se la parola non
ha passati record-compatibili di profondità arbitraria.

### 1.C Parola Viva e Blocco Antico (§88–§89)

**T13. Teorema della Parola Viva (Residuo dell'Uno).** Esiste w* = w101
(101 svolte, testo completo in §88.2), realizzabile e record-compatibile, con
**D(w101) = ∞** (passato periodico certificato σ^∞·τ, σ = LLRLLRLL, τ = 304
lettere) e **burden1(w101) = 1**, residuo {(1,1)} (diagonale dietro-destra
della posa record), onset del germe 160.
Conseguenza (per T8+T9): a ogni pose-record y-min stretto in cui le ultime
101 svolte sono w101, l'ingresso è deciso dalla SOLA cella (1,1): se bianca,
l'orbita entra. Contrappositiva: orbita eterna non-highway ⇒ a OGNI record
y-min stretto con suffisso w101, (1,1) è nera.
Dove: §88.4–88.5, `docs/WEAPON_VITALITY_ADDENDUM.md`,
`alpha1/record_weapon_cycle.py`, `record_weapon_onset_lock.py`.
Metodo: certificato geometrico finito (heading di ritorno 0 ⇒ blocchi
traslati; conflitti solo a gap ≤ g_max = 12 ⇒ check finito M_cert = 14;
Δ_anchor = (−2,0) ⇒ record-compatibilità eterna) + clausola-onset CHIUSA via
Replay-Lock (run(m) = run(40) ∀ m ≥ 40: onset 160, burden1 = 1, residuo
{(1,1)} = teorema senza parti empiriche; m < 40 verificati uno a uno).
Corollario (Famiglia Viva): σ^m·τ·w101 è una progressione infinita di parole
record-compatibili tutte a burden1 = 1 sulla stessa cella.
Caveat/correzione (retro-nota §92e, VINCOLANTE): D(w101) = ∞ NON certifica
la presentabilità di w101 ai record LONTANI DAL SEME (la rotaia σ paga 5
neri freschi = 5 celle di seme per blocco, lineare esatto misurato fino a
m=52); l'etichetta "non-vacuo" di §88 va riletta: la non-vacuità ai record
lontani è essa stessa parte della congettura del Muro. Il teorema
CONDIZIONALE (SE w101 al record ALLORA (1,1) nera) è intatto. Il teorema
inoltre NON dice che w101 occorra ai record delle eterne (occorrenza:
0/1639 nei record reali, §89a) né che 1 sia il pavimento vivo.
Decisione §108b-A9: il valore citabile di D è ESCLUSIVAMENTE il certificato
D(w101) = ∞ (il 624 del binario DFS è un early-exit storico, trappola x);
e D = ∞ NON dimostra la presentazione della parola lungo una SINGOLA
orbita eterna.

**T14. Teorema del Blocco Antico (famiglia certificata).** Ipotesi: le
ultime 405+8m svolte di un'orbita sono σ^m·τ·w101 (qualsiasi m ≥ 0).
Tesi: l'orbita non ha visitato (1,1) in quell'arco; per un'eterna
non-highway (che a quel record deve avere (1,1) nera, T13) la colpevole
(1,1) ha età > 405+8m — la scia recente non può mai salvare il pigeonhole
lungo la famiglia; la pre-semina richiesta diverge con m.
Dove: §89c, `docs/RECORD_WORD_CENSUS_ADDENDUM.md`,
`alpha1/record_trail_forensics.py`.
Metodo: residuo = {(1,1)} ⇒ fuori footprint; verificato m = 0..46 + per OGNI
m via l'induzione onset-lock di T13.

**T15. Blocco Antico sull'albero INTERO dei passati (a profondità
dichiarata 46).** Ipotesi: QUALSIASI orbita (eterna o no), record y-min
stretto con suffisso w101. Tesi: età((1,1)) > 147 (nessun passato
realizzabile e record-compatibile di w101 visita (1,1) entro 46 prepend).
Dove: §89d (prof. 40, età > 141) esteso a prof. 46 in §90b (5,5M nodi,
zero visite); `alpha1/record_ancient_block_tree.py`.
Metodo: enumerazione esaustiva CHIUSA dell'albero dei prepend (validità =
realizzabilità + footprint in {y≥1}; onset NON richiesto — nozione giusta
per i passati). Nota: il corno "visita" si attiva a profondità 57 (§90b),
coerente (57 > 46).

### 1.D U1 e il Muro dietro l'Uno (§90–§91)

**T16. U1 — Teorema del Rigioco Bianco (versione V†).** Ipotesi: estensione
all'indietro realizzabile e record-compatibile di w101 la cui ULTIMA visita
a (1,1) la lascia BIANCA. Tesi: la parola estesa ha burden1 = 0 e onset 160
— è una PAROLA-ARMA (ingresso incondizionato).
Corollario (ramo bianco chiuso): a un record y-min STRETTO il cui passato
lascia (1,1) bianca, l'ingresso in autostrada segue incondizionatamente ⇒
nessuna orbita eterna non-highway può trovarsi in questo ramo — SENZA alcun
bound di vitalità.
Dove: §91a, `docs/WALL_BEHIND_ONE_ADDENDUM.md`, `alpha1/u1_replay_theorem.py`.
Metodo: deduttivo su Replay-Lock (T7) + due certificati finiti: residuo(w101)
= {(1,1)} (T13) e G1b: V†_2600 ∩ {y≥1} ⊆ F ∪ {(1,1)}, dove V†_2600(w101) =
576 prime letture fino all'orizzonte ESATTO del verdetto U1, H = 2600
(convenzione V†_H, decisione §108b-A3; la prima stesura con V a orizzonte
onset+P era un non-sequitur d'orizzonte, riparata dal pannello — lezione:
l'orizzonte giusto è quello della rilevazione).
Robustezza: attacco con 1859 coprenti-bianche fresche (G4 §91) + 12
avversarie fresche (§92h): zero controesempi. U1 dichiarato INTATTO dopo la
falsificazione di U2-NERO (§92d: riapre SOLO il corno 3).

**T17. Muro dietro l'Uno — risultati parziali: corni 1, 2, 3a (SPEZZATO
dalla decisione §108b-A2: i corni 1/2/3a sono [T] parziali, il corno 3b è
[X] e vive per intero in X6; la versione §90d/§91c.3 con "D ≤ 4 ⇒ Cheb ≤
~5" è MORTA).** Bersaglio: per un'orbita ETERNA non-highway, a ogni record
y-min STRETTO con posa fuori da un intorno finito dell'origine/seme,
presentare w101 come suffisso è impossibile (B–T dà infiniti record fuori
da ogni intorno finito). NON esiste ancora un raggio unico del Muro
(decisione A2): la forma rigorosa è PER-PAROLA — se B_∞(z_t, r_seed(w))
non interseca né l'origine né il supporto del seme, la parola finita
certificata w non è presentabile al record z_t (via T21); il 63 è solo il
MASSIMO di r_seed sulle 273.459 parole finite censite, NON un bound
globale. Stato per corni:
- corno 1 (il passato non visita mai (1,1)): il nero su (1,1) viene dal seme
  iniziale ⇒ solo record vicini al seme — CHIUSO ai record tardivi
  (deduttivo, §90d.1);
- corno 2 (coprire-bianco): CHIUSO da U1 (T16);
- corno 3a (coprente-nera ad albero dei prepend FINITO): Lemma della
  Nascita Vicina (T21) ⇒ origine E cella nera di seme entro r_seed dal
  record — censimento §94a: 273.459/273.493 parole della famiglia
  CERTIFICATE, r_seed ≤ 63, zero alberi esauriti con min-pend = 0;
- corno 3b (coprente-nera FUGGENTE, 34 note): APERTO [X] — per intero in
  X6 (bersaglio = Ledger Sporco v2, ridotto a §95–§96 a "nessuna delle 8
  firme-exit realizzabile come nodo di pulizia", T24–T26).
NB (pannello §91 + §94b): le orbite CONVERGENTI possono presentare w101
(ingresso forzato, non violazione); "storia lunga" da sola NON basta e
nemmeno "eterna" da sola (a record fissato il passato di un'eterna è finito:
l'eternità vincola il futuro, non il passato) — l'ipotesi giusta è SPAZIALE.
Coerenza esterna: 0/1639 w101 nei record reali (§89a).

### 1.E U2: ledger, Nascita Vicina, Tratto Pulito, Collo (§92–§97)

**T18. Teorema (testimone): sup D = ∞ sulle coprenti-nere — U2-NERO
falsificata.** Esiste una coprente-nera (prof. 233) con D = ∞, via il
**Lemma del Raggio Monotono** (deduttivo + check finito): il raggio (L,R)^m
prepende una scala di celle tutte distinte a y ≥ 1; se ogni cella oltre la
coppia m0 supera y_max del footprint e la validità è verificata per
m ≤ m0+Δ, allora vale per OGNI m. ⇒ "coprente-nera ⇒ D ≤ D₀" è FALSA sia
uniforme sia per-parola (cade U2-NERO §90c/§91b; cade anche la "tasca 15
celle su 2 righe" §91b — RITRATTATA, era il campione best-first distorto).
Dove: §92c–d, `docs/U2_POCKET_ADDENDUM.md`, `alpha1/u2_infinite_rail.py`.
Trappole (aa) (D = risorsa di seme travestita) e (bb) (best-first sottostima
le code: §90c vedeva 2 config e D ≤ 4; scala reale D = 0/4/8/12/28/32/48/
52/56/60/64/∞).

**T19. Fatti certificati della macchina in-striscia (condizionali).**
T1: h1=2 ⇒ D=0 (geometria pura, nessuna ipotesi di campo). T2: zero cicli
in-tasca (nessuna delle 47.312 coperture astratte sopravvive DENTRO la
striscia: sopravvivere = uscirne). T3 (statuto deciso §108b-A6, DUE
strati): **[T] teorema computer-assistito CONDIZIONALE — ogni muro reale
interamente confinato in S_CORE ha D ≤ 33**, dove (i) S_CORE = la striscia
CORE della macchina §92a (le 15 celle della tasca §91b + (1,1));
(ii) il lemma di sovra-approssimazione è SOUND e deduttivo (§92a: ogni
transizione reale soddisfa in_succ/out_succ, la regola della cella-giovane
è necessaria, req|S congelato fuori striscia); (iii) l'enumerazione
esaustiva delle 28.910 coperture astratte morenti in-striscia ha massimo
D astratto = 33 (i testimoni confinati D=4/8/12 hanno verdetto astratto
esattamente 4/8/12). "Confinamento" = celle del muro in S_CORE, NON
"riga ≤ 2". Lo strato [C] (certificato della macchina) è C14.
T4: nel corridoio h1=0, req(2,1)=B forzato alla copertura.
Dove: §92b, `alpha1/u2_pocket_certificate.py`.

**T20. Bilancio senza tasso (teorema del ledger).** Ipotesi: parola-passato
COMPLETA (dalla nascita) di un'orbita reale. Tesi: pending finali = celle
NERE del SEME visitate (esatto: prima lettura di vita vede il colore del
seme); quindi #prime-visite-della-vita-che-leggono-nero ≤ |seme_nero|,
SENZA tasso. Fuori dal supporto del seme una prima-visita-della-vita legge
bianco ⇒ R forzato.
Dove: §92e (formulazione), §93a (promozione a teorema, lente ledger);
`alpha1/u2_far_ledger.py` (gate L1: uguaglianza esatta su griglia vuota,
(7,−7), 10 blob).
Semantica del ledger (deduttiva, §93a): pending(c) ⟺ req(c)=0; **L su cella
già pending è IRREALIZZABILE** ⇒ ogni L è apertura netta; R su pending
chiude. Caveat vincolante (trappola aa/n): il tasso NON è universale — la
discesa in autostrada (finestre cicliche di W0) è valida+record-compatibile
per ogni lunghezza testata con neri freschi TOTALI costanti (13/14/19):
costo O(1) ⇒ il bilancio generico NON dà la vietanza; serve la parte
w101-specifica.

**T21. Lemma della Nascita Vicina (per-parola, due gambe).** Ipotesi:
e2+w101 coprente-nera con albero dei prepend FINITO (enumerazione esaustiva
senza cap, profondità D_true, r_seed = max(r_foot, r_wall); serve
depth_cap ≥ D_true+1). Tesi, per ogni passato completo che la presenta a un
record y-min stretto: (gamba 1) la nascita è in QUALSIASI nodo dell'albero
⇒ ORIGINE entro r_seed dal record (nessuna ipotesi di pending); (gamba 2) se
min su TUTTI i nodi di #pending > 0, una cella NERA di SEME entro r_seed dal
record. ⇒ coprente VIETATA a ogni record y-min stretto con palla-(r_seed)
priva di seme e di origine; nessun bound su D; vale per ogni orbita.
Dove: §93c, `docs/U2_FAR_ADDENDUM.md`, `alpha1/u2_far_born_near.py`;
pannello 3/3 a §94b (enumeratore indipendente bit-identico 12/12, 3/3 esche).
Metodo: deduttivo dato l'albero esaustivo. Trappola (ee): il min-pending va
preso su TUTTI i nodi (il passato FINISCE, non muore; il conteggio
pend0−D>0 non basta). Certificati: 42/42 testimoni §93 (r_seed ≤ 16) +
273.459 parole del censimento §94 (r_seed ≤ 63).

**T22. Pavimento pend₂ sui 12 testimoni finiti (teorema per enumerazione;
NON generalizzabile).** Sui 12 testimoni ad albero finito, il minimo di
pend₂ su TUTTI i nodi è 2 (jackpot) / 3 / 3 / 4 ⇒ ogni loro passato completo
lascia ≥ 2 celle nere di seme a Cheb ≤ 2 dal record.
Dove: §93d, `alpha1/u2_far_pend2_floor.py`.
ATTENZIONE (correzione §94c): la CONGETTURA generale "pend₂ ≥ 2" (e anche
"≥ 1" incondizionata) è FALSIFICATA sulle fuggenti: pend₂ = 0 raggiungibile
(posa di nascita (−1,2), DENTRO la palla) e pend₂ = 1 con posa (0,3) FUORI
(10 controesempi di terra, `alpha1/u2_far_pend2_counterexamples.json`).
Cade anche "residuo al minimo sempre {(−1,1),(0,1)}" (§93e — artefatto di
politica) e "il reale mai sotto 2" (§93f). Sopravvive come CONGETTURA
EMPIRICA il Ledger Sporco v2: posa (nascita) fuori palla-2 ⇒ pend₂ ≥ 1 —
mai violato (~160M+37M+1,29G nodi), che BASTA al Muro (l'ipotesi del record
esclude seme E origine dalla palla). Trappole (gg), (hh).

**T23. Lemma dei Bianchi che Curvano.** Per ogni parola valida non vuota:
il cammino all'indietro all-R muore entro il 5° passo (i 4 versori sommano a
0 ⇒ il 4° R cade sulla coda; dicotomia su word[0]). Corollario: ogni cammino
all'indietro che sopravvive fa ≥ 1 L in ogni finestra di 5 passi, e ogni L
apre un pending. Dove: §93a (deduttivo; esaustivo su tutte le 2958 parole
valide di lunghezza 1–14, lente §93). Caveat: NON limita la crescita dei
pending (§92g.2).

**T24. Lemma del Passo di Pulizia + Teorema del Tratto Pulito (riduzione di
v2).** Lemma (deduttivo): pend₂ decrementa ⟺ passo R sulla cella pending
chiusa con Cheb ≤ 2; |Δpend₂| ≤ 1 per passo; la posa dopo il passo È quella
cella, dentro la palla-2. Teorema (deduttivo dato il lemma): ogni nodo
pulito (pend₂=0) in un albero con radice sporca appartiene al
sottoalbero-a-pend₂=0 del suo ULTIMO nodo di pulizia m* ≤ n, con posa(m*)
in palla. Radicamento a w101: pend₂(w101) = 6 ⇒ la riduzione vale per OGNI
passato completo che presenta w101 a un record, senza case-split sulle
coprenti. Corollario: Ledger Sporco v2 ⟺ nessun sottoalbero pulito sopra un
nodo di pulizia raggiungibile contiene una posa fuori palla-2 (i 1.376
clean-far astratti raggiungibili SOLO via tratto pulito).
Dove: §95b, `docs/U2_CLEAN_STRETCH_ADDENDUM.md`,
`alpha1/u2_far_clean_stretch.py`.

**T25. Dicotomia del Tratto Pulito.** (Deduttiva; sostituisce l'enunciato
ingenuo "sottoalbero pulito finito", smontato dal pannello — trappola ii.)
Dentro la palla il tratto pulito è forzato all-R (L aprirebbe pend₂,
L-su-pending e R-su-req=1 irrealizzabili) ⇒ muore entro 3 passi (T23);
quindi per ogni nodo di pulizia: O il sottoalbero pulito resta confinato
(profondità ≤ 3, l'enumerazione esaurisce SEMPRE) O il primo nodo con posa
fuori palla (profondità ≤ 4) è GIÀ un testimone clean-far = falsificazione
di v2. Dove: §95c. Certificati esaustivi (non survivorship): 31/31 stati di
pulizia reali noti hanno sottoalbero pulito VUOTO, firma unica ((−1,2),
heading sx), bloccata da req((0,2))=1.

**T26. Oracolo v2 e riduzione finale: v2 ⟺ 8 firme irrealizzabili.**
Vincoli deduttivi: C1 "muro delle nove" (exact_state(w101) visita 9/10 celle
di palla-2 — manca solo (1,1), coerente con T14/T15 ⇒ a ogni nodo pulito le
9 hanno req=1: l'unica cella di palla percorribile dal tratto è (1,1), al
più una volta); C3 (la cella del genitore è visitata); C4 (c_par ha y ≥ 1:
((2,1),3) irrealizzabile). ⇒ 7/15 firme-exit dell'oracolo §95d uccise
(inclusa la promozione a DEDUTTIVO del confinamento della firma reale
((−1,2),3)); restano 8 firme residue, tutte a exit-diretta. Lemma
dell'exit-step: da un nodo di pulizia con firma residua il passo d'uscita è
SEMPRE realizzabile ⇒ **Ledger Sporco v2 ⟺ nessuna delle 8 firme
(cella,heading) è realizzabile come nodo di pulizia di un passato valido**.
Lemma della Catena di Chiusura (versione corretta dal pannello; la prima con
"ingresso fresco dal bordo" era un BUCO): run-R in palla ≤ 3, pending che si
ACCUMULANO all'indietro, 4° passo forzatamente L su c* stessa — la catena
può proseguire in palla con aperture L (nessun enunciato di ingresso dal
bordo). Dove: §96a–b, `docs/U2_SIGNATURE_ADDENDUM.md`,
`alpha1/u2_far_clean_oracle_v2.py`.

**T27. Identità chirale R−L = ΔB.** Su ogni segmento di ogni orbita:
ΔB (variazione del numero di neri) = #R − #L, e Δheading ≡ ΔB (mod 4).
W0: 58−46 = 12 = rot esatto (il winding della highway È la carica nera per
periodo). Dove: §96d (deduttiva in una riga; già implicita a §79).
Caveat: non è entrata nei certificati §96 (ledger su GF(2), identità su
Z/4); nell'astrazione OUT-libero di §97 NON morde (§97d).

**T28. Coniugazione CP esatta.** L'involuzione M (x→−x, heading dx↔sx,
R↔L E scambio della regola d'interpretazione) coniuga esattamente la
dinamica; P da sola è violata. Dove: §96d, `alpha1/mirror_tripwire.py`
(M0–M4). Trappola (kk): scambiare i dati senza scambiare la semantica non è
la simmetria (bit-swap nudo = mondo a colori invertiti, 256/256 req
flippate); un insieme derivato da un oggetto chirale (oracolo all-R) non è
M-chiuso e non deve esserlo.

---

## 2. [C] CERTIFICAZIONI FINITE DELL'IMPLEMENTAZIONE

Formato: strumento — gate/regressioni — cosa NON prova.

**C1.** `code/window_build.c` + `code/analyze_radius.py` (RADIUS §46):
`--selftest` riproduce r=1,2,3 all'identico (stati, archi, conteggi per
tipo, entropie, SCC, parole, verdetti) contro i summary certificati;
r=4 = 27.297.183 stati in 20 s. NON prova: nulla su r ≥ 5; nulla
sull'esistenza di orbite (sovra-approssimazione, trappola c).

**C2.** `code/min_assumeB.c` (RADIUS §48): doppio certificato δ_r (ciclo +
fixpoint intero `verify p q`); DAG del sottografo noB-senza-rotori verificato
a runtime (abort se Kahn non copre); δ₁..δ₃ cross-validati con `--karp`
Python. NON prova: che δ_r sia raggiunto da orbite (il testimone δ₄ è un
fantasma, §54.1); la bisezione float da sola è solo un localizzatore
(trappola §50).

**C3.** `code/gamma_enum.c` (GAMMA §31): conteggi foglie ≡ censimento R(p)
(p=12..24 identici); W0 PASS, roll(W0,−37) PASS, W0 SPECCHIATA FAIL (offset
13 = prima raffica di frontiera — la chiralità ricade dal formalismo),
(RL)^∞ FAIL; i chunk `part` sommano esattamente ai totali. NON prova:
sufficienza (ammissibile ⇒ testimone costruibile) — solo necessità.

**C4.** `code/product_automaton.py` + `code/product_build.c` (PRODOTTO
§56.2): self-test 4/4 (m=0 ≡ base byte-per-byte; orbita reale mai bloccata
e costo invariante = 558 per ogni (m,D); frame canonico ≡ assoluto; 252/252
fantasmi bloccati da A(4;32,8)); builder C ≡ Python byte-per-byte in tutte e
3 le politiche. Come VERIFICATORE: copertura del catalogo a full m=32/D=8,
ibrida m=24/D=8. NON prova: δ^alt (ostacoli A/B, §56.4–56.5); il min grezzo
del prodotto è privo di significato senza rimozione dei cicli B–T.

**C5.** `code/altmin_driver.py` + catalogo `results/delta4_alt_catalog.jsonl`
(RADIUS §55.2): 252 fantasmi distinti, ognuno con conflitto esplicito
(distanza temporale ≤ 124; 72/252 NO-B-T uccisi SOLO da alternanza); tagli
append-only certificati per-fantasma. NON prova: che 0.0455 sia un lower
bound di δ₄^alt — è una barriera RELATIVA alla sequenza di taglio (un ciclo
consistente più economico potrebbe passare per un arco tagliato, §55.2);
la certificazione esaustiva è il contenuto del Lemma A ([X]).
Collocazione [C] CONFERMATA dal pannello (decisione §108b-A4): 0.0455 è
l'esito certificato della SPECIFICA sequenza append-only di 252 tagli;
l'inferenza a lower bound per δ₄^alt resta [X] (X1).

**C6.** `alpha1/halo_occupancy_profile.py` (§86): gate §85a esatti 24/24;
tripwire ⟺ halo 0 violazioni; tripwire T2 (scia) 0/2.323.679 deep_1;
T3 0/5.716 cavalcate; T4 0. Bug-story §86.6: la prima stesura (offset invece
di celle assolute) è stata beccata dal tripwire ⟺ sui dati reali — antidoto:
self-test con formica in posizione ≠ origine. NON prova: i valori medi di
occupazione (quelli sono [O] delle 24 orbite).

**C7.** `alpha1/word_lock.py` (§86b): necessità (ogni flip di cella-lock
rompe W) + sufficienza (1000 ambienti junk per parola); gate
lock((LRRRR)³) = {centro nero}+9 halo bianche (riproduzione §85c).

**C8.** `alpha1/onset_cone_lock.py` (§87.1–87.2): self-test 1000 junk fuori
V (parola identica) + 200 flip dentro V (cambia esattamente alla prima
lettura); gate onset 5/5 (vuota 9977, b1 310, b2 162, b3 142, (7,−7)
106258); bug del drift corretto in sessione (heading reale all'onset).

**C9.** `alpha1/kwindow_spoiler_census.py` (§87.3): censimento esaustivo
chiuso K=6..14, cap 2M, zero NO-onset. NON prova: K ≥ 16 (mai censito
esaustivamente); nulla sul camping (trappola v).

**C10.** `alpha1/onset_forensics.py` (§87.4–87.5): 24/24 onset identici agli
header di `dumps_all.txt`; tripwire di replay e sotto-corse 0 divergenze.
Kill-gate §79.1: il raggio decisivo (prime-letture, word-minimale) cresce
18/38/93.5/118 con Δ = 2/10/100/1000 periodi senza stabilizzare. NON prova:
verdetto-minimalità del footprint (dichiarato; i determinanti piccoli sono
già esclusi da §59/§78–80).

**C11.** Catena §88 (`record_weapon_vitality/rail/cycle/cycle_verify/
onset_lock.py`): riproduzione in-process bit-identica della run v3;
controllo negativo (campione vacuo K=60: D=2 come dichiarato);
falsificazione del certificato σ 3/3 verde (diretta m=15..40, catena
lettera-per-lettera K=565, traslazione footprint su 5 coppie); verifica
avversaria multi-agente 46 claim (43 ok, 3 riparati in sessione, incluso il
sigillo onset-lock). Il muro dei prepend è ESAUSTIVO solo a prof. 2..17
(binario unico), poi riapre ×1.65 (trappola y — dichiarare sempre fino a che
profondità l'unicità è esaustiva).

**C12.** Catena §89 (`record_word_census/guilty_dynamics/trail_forensics/
ancient_block_tree.py`): gate onset 24/24 == header; cross-check assert fra
§89a e §89b (stessi 1639 record); forense G=1 3/3 con fix di frame
documentato (rotazione k=(−h0)%4, §89c); albero §89d con conteggi IDENTICI
al muro §88 Test B (il filtro-onset non pota mai — coerente con §87b zero
buchi). NON prova: inevitabilità di alcuna famiglia di parole ai record.

**C13.** `alpha1/u1_replay_theorem.py` (§91a): G1 (residuo/inclusione su V,
|V|=81, onset 160), G1b (V†_2600, 576 prime letture all'orizzonte H=2600: zero celle extra —
il check portante della versione riparata; convenzione V†_H, §108b-A3), G2 (colori su F bit-identici
60/60), G3 (30/30 coprenti-bianche: onset e intera V identici), G4 (attacco:
1859 armi fresche, 0 controesempi) + 12/12 avversarie fresche (§92h).

**C14.** `alpha1/u2_pocket_certificate.py` + `u2_infinite_rail.py` (§92):
6 gate (G0 formula del passo 1500×2; G1 lemma del suffisso 42.697; G2 replay
bit-identico dei 60 muri §90c; G3 membership 60/60; G4 RIPARATO dal pannello
— camminate lunghe ≤320 passi con SOGLIE asseribili ≥500 rientri/≥50
coperture: la v1 era vacua, "un gate deve poter fallire"; G5 testimoni);
lemma di sovra-approssimazione promosso a deduttivo. Raggio monotono con
assert di monotonia stretto. NON prova: confinamento reale (la fase 1 non
pota quasi nulla, trappola cc); nulla sulle bianche oltre D=25 astratto.

**C15.** `alpha1/u2_far_ledger.py` + `u2_far_run.py` (§93a–b): gate L0
(identità incrementale, 800 estensioni), L1 (verità di terra forward:
pending = seme nero visitato, uguaglianza esatta 10/10 blob + vuota +
(7,−7)), L2 (riproduzione bit-identica del controesempio §92e: 2918 passi,
pending 60→286), L3 (all-R esaustivo 2958 parole). Lente indipendente §93i:
macchinario riscritto, 3 mutazioni-esca tutte beccate. Corsa forzata
fresco⇒R: muore ≤ 64 passi su TUTTE le 48 coprenti reali (deterministica
per-parola). NON prova: bound sulla crescita dei pending nei passati con L.

**C16.** `alpha1/u2_far_born_near.py` + `u2_far_born_near_census.py`
(§93c, §94a): 42/42 alberi finiti certificati con cross-validazione
solo-`valid()` (D, min_pend bit-identici); censimento famiglia RIGENERATA:
gate GC0 (60 §90c → esattamente 2 config), GC1 (42 testimoni bit-identici —
pairing per INDICE, il pairing per nome era un bug reale beccato), GC2, GC3
(soglie asseribili), GC4. Semantica dei cap: mai falsi certificati (errore
sempre conservativo; depth_cap ≥ D_true+1 dichiarato). NON prova: nulla
sulle 34 fuggenti (a cap 3M nodi/450 prof. — restano il campo di battaglia).

**C17.** Pannelli §93/§94 (3/3): lente ledger, lente enunciati, lente
caccia, lente macchina-palla2, lente nascita-vicina — riproduzioni
bit-identiche, 10+ esche beccate complessivamente; correzioni incorporate
(2.020 vicini veri, non 3.396; contabilità per-raggio; C4 vacuo chiuso per
enumerazione indipendente). I 10 controesempi pend₂ verificati di terra
(`u2_far_pend2_counterexamples.json`). Nota di metodo (memoria utente): le
lenti dei pannelli vanno lanciate a INIZIO sessione (due morti per limite di
sessione a §93/§94).

**C18.** `alpha1/u2_far_ball2_machine.py` (§93f): gate B0–B3 verdi (fase 1
riprodotta stato-per-stato; 8/8 testimoni reali in cov_n; ledger palla-2
astratto == reale). NON prova: il ledger — 1.376 stati puliti-lontani
astratti sono FANTASMI non realizzati (trappola ff: OUT libero dimentica i
req fuori striscia; solo la morte si trasferisce).

**C19.** `alpha1/u2_far_clean_stretch.py` + `u2_far_clean_oracle.py` (§95):
gate G0–G4 (G1b: pend₂(w101)=6; lemma di terra 0 violazioni su 310 cammini,
esca palla-1 beccata con 2682 violazioni); dicotomia nell'enumeratore a
foglia-testimone (ordine testimone-prima-di-assert — un assert d'esaurimento
prematuro avrebbe mascherato una falsificazione, trappola ii); pannello §95
3/3 IN SESSIONE (lente logica: non-sequitur riparato; lente macchinario
indipendente 10/10 bit-identici; esche 6/6). Oracolo: gate O0. NON prova:
v2 (certificazione per-nodo-RAGGIUNTO; v2 resta congettura empirica,
trappola hh).

**C20.** `alpha1/u2_far_clean_oracle_v2.py` + `u2_far_signature_hunt.py` +
`mirror_tripwire.py` (§96): gate W1 (footprint 9 celle — il gate portante),
O0, E1 (senza vincoli riproduce le 15 di §95d), E2 (C1 monco cambia le
residue); cacce con controllo positivo obbligatorio S0 (20 hit sulla firma
nota; esca M4: controllo corrotto ⇒ S0 rosso); tripwire CP M0–M4 (M1: P da
sola diverge — il checker vede la violazione di parità); lente macchinario
indipendente 37/37; esche 4/4 (inclusa: senza C4 risorge esattamente e solo
((2,1),3)). NON prova: l'irrealizzabilità delle 8 firme (il negativo è
PC-only, §96c).

**C21.** `alpha1/u2_far_collo_machine.py` (§97): soundness della
sovra-approssimazione validata dal pannello (rientri adiacenti, congelamento
req, morte, rilevazione firme su ogni arco); GATE B1 (assert
cheb(posa_w101) > R — l'init loc=OUT era sound solo "per caso fattuale" a
R ≤ 3: a R=4 sarebbe stata unsound silenziosa, trappola mm); verifica di
terra FORTE N4: replay proiettato del testimone reale §96, 1.270 passi,
pend₂ macchina == reale a ogni passo (raccomandazione R1: il controllo
positivo forte per le macchine astratte è il replay proiettato, non la
membership della firma); esche N1–N3 beccate; K1/K2 etichettati NON-DEFINITI
sotto cap. NON prova: nulla in positivo (radius ≤ 3 inconcludente
cap-robusto, §97c).

---

## 3. [O] OSSERVAZIONI CAMPIONARIE

Formato: dato — campione — unità — caveat/scadenza (ogni soglia è un
quantile, trappola qq).

**O1.** Entropia del window-automaton pieno ↘ 0.734 (0.8114 / 0.7594 /
0.7441 / 0.7367 a r=1..4) ≈ entropia esatta del realizzabile — RADIUS §47.
(Valori esatti calcolati; l'estrapolazione del limite è osservativa.)

**O2.** Debito sulle orbite reali con semantica di memoria esatta 9×9
(RADIUS §54.2): transiente griglia vuota 0,1775 nere profonde/passo (finestre
da 1000: 0,115–0,249); età del detrito mediana 684 passi (max 6848);
highway: esattamente 16 nere profonde/periodo = 0,1529/passo = 24× δ₄, età
40–116. Campione: orbita griglia vuota. Lettura: anche l'eternità "buona"
paga — la distingue il COME (età e regolarità). Caveat età: trappola (nn)
di §98 — "antico/statico" dipende dall'orologio (passi vs epoche-evento).

**O3.** Minimi reali su sliding window (RADIUS §55.3): min tasso nere
profonde per L=313/626/1000/5000 = 0.080–0.089 / 0.099–0.112 / 0.114–0.118 /
0.163 = 12,5–25,5× δ₄^auto; i minimi CRESCONO con L. Campione: griglia vuota
+ 3 IC random (16 nere). Coerente con la barriera dei fantasmi (C5), ma non
un bound.

**O4.** Occupazione dell'halo ai deep_1 (§86.2): k_r min 1 (su 24/24
orbite — il Teorema della Scia è STRETTO, nessun "≥2" da attaccare), moda
4–5, media 4,563; s=0 (halo interamente rifornito nell'intervallo) 24,37%;
neri-halo di seme 0,15%; k_r piatto per età (bucket 4,67/4,46/4,49/4,51/
4,47). Campione: 24 orbite lunghe, 2.323.679 eventi — selezionate per onset
alto (trappola h): i valori medi valgono per LORO.

**O5.** Forense degli onset reali (§87.4): il germe consumato dalla highway
neonata è 13–17 neri (mediana 13 = il minimo teorico §76), raggio ≤ 7;
interfaccia 1–2 periodi; f_bordo mediana ~0.68; drift outward 23/24.
Campione: 24 orbite. Lettura: il caos entra dalla porta più stretta.

**O6.** Burden1 e caccia all'arma (§87d–e, §88.1): minimo record-compatibile
censito 18/16/14/10 a K=12..18 (esaustivo); col filtro di vitalità
(viable-k 8) il minimo VIVO scende 19→…→1 (K=101..120, residuo {(1,1)});
weapon (burden1=0 viva): MAI vista — beam 4000/kmax 120, binario dei
prepend seguito fino a prof. 624 (early-exit storico del testimone DFS,
decisione §108b-A9: il valore di D citabile è SOLO il certificato
D(w101)=∞, T13), corridoio 1,5M nodi (486.676 rami vivi al cap 60,
NON esaustivo).
Scadenza/caveat: i minimi senza filtro di vitalità a K>18 (plateau 5
"Residuo dei Cinque", discese a 2) erano TUTTI artefatti di beam o minimi
VACUI (estinzione entro prof. 3–7) — versione corretta a §88 (trappole w, x).

**O7.** Parole reali ai record y-min stretti pre-onset (§89a): 1639 record
(24 orbite); burden1 a K=101 min 12 / mediana ~317 / max 3956 (mai ≤ 6);
zero match con w101; zero burden1=0; 3 record a UNA sola colpevole.
Tripwire del meccanismo Cono: 1620/1620 record lontani dall'onset con ≥ 1
cella-residuo nera. CORREZIONE (§99, MINEP-HUNT, trappola pp): su campioni
freschi esistono 2 violazioni REALI del tripwire-orizzonte a V(onset+P)
(caveat V† realizzato) — il meccanismo è sano SOLO all'orizzonte V†_H
(record-side: H = t† = max(2600, og_rec+2080), decisione §108b-A3);
il 1620/1620 era (anche) fortuna del campione (~7·10⁻⁵). Caveat: orbite
selezionate per onset alto (trappola h) — lettura within-orbit.

**O8.** Dinamica delle colpevoli (§89b): G mediana 96 (min 1, max 1700),
passeggiata quasi bilanciata; persistenza nera al record dopo ~96%;
Chebyshev colpevoli mediana 15 / max 75 (= raggi Spoiler Vecchio §87);
autopsie G=1 3/3: colpevole = PROPRIA SCIA a età K+1..K+13, Cheb 3–6
(trappola v misurata al bordo del pigeonhole). CORREZIONE d'orologio (§98,
trappola nn): "età mediana 1856 passi ≈ 18P, 60% ≥ 10P" NON significa
detrito antico — nell'orologio delle epoche-record il rifornimento ha
mediana 3 epoche; non attaccare risorse "antiche" al Blocco Antico su base
§89b.

**O9.** Scala dei muri delle coprenti-nere (versione corretta §92c + §94a,
sostituisce §90c): D = 0 / 4 / 8 / 12 / 28 / 32 / 48 / 52 / 56 / 60 / 64
/ ≥400(cap) / ∞ (T18); 50 config di copertura distinte; 273.493 coprenti
censite; 34 fuggenti (31/34 in una config: proprietà per-parola);
h1=1 mai realizzata (0/43.726). Il "D ≤ 4, 2 config" di §90c era
survivorship best-first (trappola bb).

**O10.** Ledger Sporco v2 (§94c): "posa di nascita fuori palla-2 ⇒
pend₂ ≥ 1" mai violato su ~160M passi (lente caccia) + ~37M nodi (lente
macchina) + 1,29G (campagna §93). ETICHETTA OBBLIGATORIA (trappola hh): il
floor di una caccia è survivorship anche a 10⁹ nodi se la famiglia di
politiche è una — il "pend₂ ≥ 2" della stessa campagna è morto in 7 s con
una politica diversa. I 1.376 clean-far astratti restano i falsificatori
candidati.

**O11.** Il Collo della Pulizia (§95e, §96c): 31 stati di pulizia reali
certificati (§95) + 603 pulizie censite (§96, run 733M passi, 1242 job):
TUTTE con firma ((−1,2), heading sx h=3), TUTTE prodotte dalla politica PC
(mutazione dei testimoni); PA/PB/PD: zero pulizie. 8 firme residue: 0 hit
(82,8M passi/firma), controllo positivo 20 hit. Negativo etichettato
PC-only (pulire la palla da zero è talmente raro che le cacce cieche non ci
riescono MAI). Candidato-teorema, NON teorema.

**O12.** Macchina del collo (§97b–c): radius 2 (esaustiva, 36.860 stati) 24
firme raggiungibili, insensibilità TOTALE ai flip iniziali (tutti i flip +
coppie — osservazione washout, trappola ll); radius 3 (cap 60M, NON
esaustiva) ≥ 23 firme, TUTTE le 8 residue incluse (lower bound cap-robusto:
la raggiungibilità è monotona). Nessun teorema da zone raggio ≤ 3 con OUT
libero.

**O13.** Grammatica dei fantasmi δ4 (§55.2): distanza temporale del primo
conflitto min 20 / mediana 64 / max 124 (sempre limitata, "appena oltre la
finestra"); 234/252 violano nel primo periodo. Base della via
automa-prodotto (memoria temporale k ≈ 128).

---

## 4. [X] CRUX APERTI E STRADE FALSIFICATE

Formato: oggetto — stato — trappola.

**X1. δ₄^alt / δ₄^real mai certificati.** La barriera 0.0455 è relativa
alla sequenza di taglio (C5); Lemma A ("ogni ciclo sotto ε è fantasma o
B–T") e Lemma B (memoria antica non eternamente economica) restano bersagli
formali (§55.4). Caveat aperiodico: il Lemma A sui CICLI non limita da solo
le orbite aperiodiche — serve l'automa-prodotto con alternanza interna agli
stati (§55.4), che esiste ed è sound (T4) ma non certifica (ostacoli A —
rimozione cicli B–T nel prodotto, mai implementata — e B — esplosione
spaziale; la memoria temporale compatta di §56.7.2 non è mai stata
costruita). Trappole (e), §56.6 prodotto-rotori.

**X2. r = 5.** Non tentato (≳10¹⁰ stati): serve potatura teorica, non
hardware (§49, §51.4). Congettura collaterale §51.5: ogni parola di rotore
ha rot ≢ 0 mod 4 oppure drift = 0 (renderebbe il Teorema della Finestra
autosufficiente senza γ-checker a ogni raggio) — mai attaccata.

**X3. γ: gap 42–102.** Forza bruta realistica fino a ~48–52; oltre serve
potatura teorica (§33.2). Il γ aperiodico è fuori portata del formalismo
attuale (si intreccia con α1).

**X4. Congettura del pavimento vivo:** per ogni w record-compatibile con
D(w) illimitato, burden1(w) ≥ 1 (§87e/§88.5). Il livello 1 è OCCUPATO da
w101; l'arma (parola VIVA a burden1 = 0) non è mai comparsa in tre campioni
ampi consecutivi (O6) ma resta logicamente possibile per K > 120 o su altri
rami. NB: il criterio corretto dell'arma esige la vitalità (trappola w) e —
dopo §92 — "viva" andrebbe a sua volta pesata col bilancio dei neri freschi
(trappola aa).

**X5. "burden1 = 0 ⇒ D ≤ 12" (§90c):** congettura INDEBOLITA, non decisa.
Gli attacchi economici del pannello §92 falliscono (sorelle-flip h1=2 ⇒ D=0;
151 bianche max D=12 ma con classi nuove 4/8 mai viste), l'astratto ammette
bianche fuggenti (16.388) e confinate fino a D=25: per la trappola (bb) la
coda 48/56/∞ è plausibile. Serve la campagna stress-2 bianche (ereditata
§92g.5, mai fatta).

**X6. Il Muro dietro l'Uno — corno 3b (IL crux della linea U2; qui per
intero per decisione §108b-A2, spezzato da T17).** Catena
attuale: Ledger Sporco v2 (O10) ⟺ nessun tratto pulito esce dalla palla
(T24–T25) ⟺ nessuna delle 8 firme-exit è realizzabile come nodo di pulizia
(T26). Vie tentate e FALSIFICATE, in ordine:
- pavimento pend₂ ≥ 2 (§93d) — FALSIFICATO §94c (trappole gg, hh);
- chiusura per vitalità "pend₂=0 ⇒ albero finito" (§94f.2) — FALSIFICATA in
  apertura §95a (2/8 vivi oltre depth 400; trappola jj: guardare il
  sottoalbero POTATO dal vincolo, non l'albero intero);
- invariante parity-flux phi_colonna0 (§94d) — rifiutato dalla chiusura
  Houdini e POI falsificato dai controesempi (trappola gg: il checker batte
  il campione); il per-pose PP0 è ROSSO al punto fisso, da raffinare prima
  di ogni riuso;
- macchina palla-2 con OUT astratto (§93f) — non decide (trappola ff);
- via a zona piccola raggio ≤ 3 / OUT-libero (§97) — FALSIFICATA
  (cap-robusto: le 8 firme restano raggiungibili; con rientro libero le
  direzioni d'approccio sono libere per costruzione; trappole ll, mm).
Aperto nominato (§97c): QUALE componente scartata dall'OUT-libero porta la
rigidità reale — (a) req fuori zona, (b) continuità uscita-rientro,
(c) mortalità esterna — con esperimenti separatori proposti (guscio di req
cheb R+1..R+k con rientro teletrasportato; rientro vincolato al lato
d'uscita). Vie costruttive §97g: motore C a striscia allargata (radius ≥ 4
esatto, trappola g); vincoli-scia sul rientro (Scia §86 all'indietro, dove
lo Z/4 di T27 potrebbe mordere); invariante flux OUT-resistente.
Il falsificatore permanente: realizzare UNA delle 8 firme ⇒ v2 falsa.

**X7. Collo della Pulizia come teorema.** "Ogni nodo di pulizia ha firma
((−1,2),3)" (O11): se dimostrato ⇒ v2 TEOREMA (la firma è confinata da C1)
⇒ corno 3b chiuso ⇒ Muro chiuso nella forma per-parola di T17 (decisione
§108b-A2: palla-2 per le fuggenti + r_seed per-parola sulla famiglia
certificata — nessun raggio unico). La via enumerativa diretta (§96g.1) è
stata falsificata nella forma a zona piccola (§97 = X6); il negativo
empirico resta PC-only.

**X8. Occorrenza (fuori perimetro A, puntatore).** Tutti i teoremi-parola
della linea (T13–T17) sono di VIETANZA, non di cattura: nessuna orbita reale
presenta w101 ai record (0/1639, O7). L'anello di occorrenza è stato
riformulato e portato avanti a §98–§107 (metà B): qui si registra solo che
la vietanza di una parola non muove Link 1 senza una famiglia INEVITABILE ai
record (§90d, §91c.4).

**X9. h1 = 1 mai realizzata** (0/43.726, §92c): candidato a ostruzione di
corridoio dimostrabile (§92g.4) — mai attaccata. Ereditata.

**X10. Fuggenti nuove vs nere-D≥400** (§94f.4): le 34 fuggenti del
censimento = 6 vecchie + 28 nuove; la classificazione dei corridoi di fuga
non è mai stata fatta. Ereditata.

**X11. Kill-gate deep→W0 (negativo definitivo).** Nessun programma a
footprint limitato co-moving decide "questo evento deep-black porterà a lock
W0": il raggio decisivo cresce senza stabilizzare (C10, §87.5). Direttrice
CHIUSA; con §80 (alfabeto non satura, trappola o) e §79 (deficit di consumo,
trappola n): il lato-alpha è irriducibilmente dinamico.

**X12. Strade falsificate storiche della linea record (promemoria con
trappola):** pavimento del morso fresco (§57, trappola i/n); Residuo dei
Cinque come ostruzione (§87e — artefatto di beam); minimi vacui a fardello
2/4 (§87e-2, trappola w); scan di periodicità ingenuo sul fondo del
testimone (trappola x); U2-NERO word-level (§90c/§91b, trappole aa/bb);
tasca 15-celle (§91b, ritrattata §92c); raggiungibilità astratta come
risultato (§90a, trappola z).

---

## DECISIONI DEL PANNELLO §108 (§108b — le 9 questioni del volume A, DECISE e applicate)

1. **burden1 vs vitalità (→ T12, O6):** conservati 18/16/14/10 come minimi
   esatti del censimento chiuso NON filtrato; nel teorema soltanto
   burden1(w) ≥ m_K; il bound passa automaticamente al sottoinsieme vivo;
   NON è dimostrato che il minimo vivo sia raggiunto e valga esattamente
   10. Nessun ricalcolo.
2. **Raggio del Muro (→ T17, X6):** non esiste ancora un raggio unico del
   Muro; T17 spezzato — corni 1, 2, 3a come risultati parziali [T], corno
   3b come [X] (= X6). Forma rigorosa per-parola: se B_∞(z_t, r_seed(w))
   non interseca origine né supporto del seme, la parola finita certificata
   non è presentabile. Il 63 è solo il massimo sulle 273.459 parole finite
   censite, non un bound globale.
3. **Tripwire d'orizzonte (→ T16, C13, O7):** nessun V† numericamente
   universale; V†_H(w) = prime letture fino all'orizzonte esatto del
   verdetto. Per U1: H = 2600. Per Dicotomia/tripwire record-side:
   H = t† = max(2600, og_rec+2080).
4. **0,0455 (→ C5, X1):** confermato [C], ma solo come esito certificato
   della specifica sequenza append-only di 252 tagli; non è un lower bound
   per δ₄^alt — tale inferenza resta [X].
5. **Record y-min stretto (→ convenzioni in testa e qui sopra):**
   definizione canonica, all'istante subito prima della lettura:
   y_t < min_{s<t} y_s ⇒ semipiano y ≤ y_t mai visitato dalla traiettoria
   precedente; bianchezza solo aggiungendo y_t < y_min(seme); heading e
   footprint sono conseguenze nella convenzione temporale scelta, non
   parti della definizione.
6. **T3-D≤33 (→ T19, C14):** scisso in due strati — [T] teorema
   computer-assistito condizionale "ogni muro reale interamente confinato
   in S_CORE ha D ≤ 33" (con definizione di S_CORE, lemma di
   sovra-approssimazione sound, enumerazione esaustiva con massimo 33);
   [C] certificato della macchina (C14).
7. **γ (→ T3):** dicitura unica "Nessuna orbita da configurazione iniziale
   finita ha linguaggio di svolte definitivamente periodico di periodo
   minimo ≤ 41" (dispari analitici; pari ≤ 40 per enumerazione chiusa);
   "γ ≤ 40" eliminato.
8. **Cavalcate (→ T1, T2):** costanti per-raggio dichiarate — massimo
   quattro periodi per r ≤ 3, massimo due per r = 4.
9. **D(w101) (→ T13, O6, C11):** citabile ESCLUSIVAMENTE D(w101) = ∞; il
   624 è un early-exit storico del testimone DFS; e D = ∞ non dimostra la
   presentazione della parola lungo una singola orbita eterna.

---

## Conteggio voci (§108b)

[T] 28 · [C] 21 · [O] 13 · [X] 12 — riconteggio §108b: INVARIATO (gli
split A2/A6 riallocano contenuto già contato: il corno 3b era già X6, il
certificato di T19-T3 era già C14). Le 9 DA CHIARIRE: DECISE (sopra).

## Fonti (file letti integralmente)

`CLAUDE.md`; `docs/MORSO_ADDENDUM.md`; `docs/RADIUS_ADDENDUM.md`;
`docs/GAMMA_ADDENDUM.md`; `docs/PRODOTTO_ADDENDUM.md`;
`docs/TRAIL_HALO_ADDENDUM.md`; `docs/CONE_LOCK_ADDENDUM.md`;
`docs/WEAPON_VITALITY_ADDENDUM.md`; `docs/RECORD_WORD_CENSUS_ADDENDUM.md`;
`docs/WEAPON_DICHOTOMY_ADDENDUM.md`; `docs/WALL_BEHIND_ONE_ADDENDUM.md`;
`docs/U2_POCKET_ADDENDUM.md`; `docs/U2_FAR_ADDENDUM.md`;
`docs/U2_FAR_PANEL_ADDENDUM.md`; `docs/U2_CLEAN_STRETCH_ADDENDUM.md`;
`docs/U2_SIGNATURE_ADDENDUM.md`; `docs/U2_COLLO_MACHINE_ADDENDUM.md`;
ERRATA: `docs/SHIELD_MAP_ADDENDUM.md` §107d.0,
`docs/KERNEL_EXTENDED_ADDENDUM.md` §107e.0 (nessuna delle due tocca
direttamente §40–§97; le correzioni interne al perimetro sono quelle dei
pannelli §91–§97 e §98/§99, incorporate sopra); scheletro:
`docs/CONSOLIDATION_108.md`.
