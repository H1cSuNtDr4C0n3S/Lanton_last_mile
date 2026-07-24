# CONSOLIDAMENTO §108 — INVENTARIO, METÀ B (v2 = §108b)
## Certificati alpha1/beta + linea record-side (§57–§75, §78–§86, §98–§107e)

Perimetro: catena alpha1 §57–§75, kernel della porta §78, ledger/motivi §79–§86,
linea record-side §98–§107e. **Esclusi** (metà A): §36–§56 e §87–§97.
Per §107b/c/d/e si usa SEMPRE la versione post-ERRATA (§107d.0, §107e.0; "lock-capable"
RITIRATO a §107d.0.5). Nessun claim nuovo: ogni voce cita il § e il file sorgente.
**§108b:** le 8 questioni DA CHIARIRE sono state DECISE dal pannello §108 (verdetto
2026-07-24) e le decisioni sono applicate in questo volume (sezione DECISE in coda;
v1 in 34ada36; nessuna nuova simulazione).
Convenzioni canoniche (fissate in testa, `docs/CONSOLIDATION_108.md`): record y-min
stretto = y_t < min_{s<t} y_s (A5); V†_H per-verdetto, record-side t† = max(2600,
og_rec+2080) (A3); **og_rec** = onset del germe misurato DAL RECORD (≡ l'onset_germe
di questo volume), **og_win** = K + og_rec (asse della parola concatenata), tempo
assoluto = t_record + og_rec, sempre **ride = d − og_rec** — la dicitura "asse
assoluto og+101" è ELIMINATA (B4); le tre nozioni di "fase" (checklist §61–66 /
GF(2) §74 / porta §102–104) restano DISTINTE, nessuna identificazione senza mappa
esplicita (B2).
Convenzione etichette: **[TEOREMA]** = deduttivo con ipotesi complete; **[CONDIZIONALE]** =
teorema sotto ipotesi dichiarate aperte; **[ENUMERAZIONE]** = esatto per enumerazione
esaustiva finita; **[NO-GO-EMPIRICO]** = falsificazione sul campione raggiunto, non teorema
dinamico; **[QUANTILE]** = soglia campionaria con data di scadenza (trappola qq).

---

## STRATO 1 — TEOREMI UNIVERSALI

### B1.1 [TEOREMA] Teorema della Scia (§86.1, docs/TRAIL_HALO_ADDENDUM.md)
**Enunciato.** Sia t una lettura nera deep_1 (cella già visitata, fuori dalla finestra viva
3×3). Nel frame heading-su della lettura, almeno una delle tre celle di scia
{(0,1),(−1,1),(−1,0)} è nera al tempo t con ultimo tocco a età ≤3; detto j∈{1,2,3} l'indice
della più recente svolta R tra t−1,t−2,t−3, la cella di scia d'ordine j è nera con età
esattamente j.
**Ipotesi.** Dinamica canonica (CLAUDE.md §2); definizione deep_1 = cella visitata uscita
dalla finestra r=1; t≥4 è automatico (uscire e rientrare dalla finestra richiede ≥4 passi).
**Metodo.** Induzione all'indietro sulle ultime 3 svolte (§86.1); vale per OGNI orbita,
finita o eterna.
**Verifica di terra.** Tripwire T2 per-evento: 0 violazioni su 2.323.679 deep_1, 24 orbite
(`alpha1/halo_occupancy_profile.py`).
**Caveat.** Copre l'INIZIO della finestra alla lettura; nulla dice su code parziali di
cavalcata (§86.5).

### B1.2 [TEOREMA] Corollari della Scia: evitamento (LRRRR)^3 ai deep, 0% motivi vuoti, firma RLLL (§86.1, docs/TRAIL_HALO_ADDENDUM.md)
1. deep_1 ⟹ halo non tutto bianco ⟹ (Teorema Halo B1.3) **nessuna lettura deep inizia
   (LRRRR)^3 — in NESSUNA orbita, incluse le eterne** (la trappola (i) cade per questo
   enunciato; vale a fortiori per deep_2..4 per inclusione).
2. Via l'entailment §85.3: lo 0% di motivi potati vuoti ai deep (misurato in §81) è teorema.
3. Firma del passato di ogni cavalcata (t≥4): halo bianco ⟹ svolte(t−4..t−1)=R,L,L,L e
   pos(t−4)=centro (la cavalcata è in-finestra, mai fresca, mai deep). Tripwire T3:
   0 violazioni su 5.716 cavalcate reali; T4: 0.

### B1.3 [TEOREMA] Teorema Halo (⟺ locale esatto) (§85c, docs/LRRRR_HALO_ADDENDUM.md)
**Enunciato.** Una lettura nera inizia (LRRRR)^3 ⟺ le 9 celle HALO =
{(−2,0),(−2,1),(−1,−1),(−1,0),(−1,1),(−1,2),(0,−1),(0,1),(0,2)} (frame heading-su, raggio
max 2) sono tutte bianche alla lettura.
**Metodo.** Calcolo diretto: nei 15 passi vengono primo-lette esattamente {centro}∪HALO;
la dinamica consulta solo celle lette. Necessità verificata 9/9 (ogni singolo flip rompe la
parola), sufficienza per costruzione + 1000 ambienti junk (`alpha1/lrrrr_halo_witness.py`).
**Caveat.** Vale per l'inizio-cavalcata alla lettura (§85.5). NB: il teorema-FINESTRA
universale è FALSO (testimone reale: nero isolato — vedi B4.9).

### B1.4 [TEOREMA] Teorema-lock di prima-lettura + impossibilità dei rotori r≥2 nel piano (§86b, docs/TRAIL_HALO_ADDENDUM.md)
**Enunciato.** Una parola di svolte W parte dalla lettura corrente ⟺ ogni cella primo-letta
durante W ha il colore richiesto (L=nera, R=bianca) al momento iniziale; le riletture sono
forzate dall'alternanza; se una rilettura contraddice, W è irrealizzabile da lettura singola
in QUALSIASI ambiente. Applicazione (×3 periodi, tutte le rotazioni): LLRRRR (p6) 0/6
realizzabili, LLRRLLRRRR (p10) 0/10 — **i rotori r≥2 sono impossibili come parole di lettura
ancorate nel piano** (esistono solo come cicli dell'astrazione B-T a finestra); LRRRR 2/5;
p15 15/15 realizzabili, con lock canonico = centro + le 3 celle di scia + (1,0) neri.
**Metodo.** Calcolo diretto per parola; verifica: necessità (flip) + sufficienza (1000
ambienti junk) per parola (`alpha1/word_lock.py`).
**Conseguenza dichiarata.** L'assenza dei rotori r≥2 dal caos (§84) è teorema; la dicotomia
evitamento-LRRRR / eccesso-p15 è spiegata strutturalmente (§86.3).

### B1.5 [TEOREMA] Lemma della Scala (§98b, docs/OCCURRENCE_SUPPLY_ADDENDUM.md)
**Enunciato.** Ipotesi: partenza alla riga 0, mosse unitarie, record y-min STRETTI. Allora:
(i) la riga assoluta −m è visitata per la prima volta esattamente al record m−1;
(ii) a un record censito, ogni cella-residuo con riga < y_seed_min non è di seme; se è nera,
la sua ultima visita è stata una svolta R dell'orbita (autofornitura) con
paint_t ≥ t_record(riga); (iii) ep := #record in (paint_t, t] soddisfa **ep ≤ y_rel**.
Identità esatta di contorno: q = y_rel − ep (quota di rientro).
**Metodo.** Deduttivo (aritmetica della scala). Terra: T1–T4 zero violazioni su 188.234
colpevoli profonde canoniche (§98a) e su ~254k record freschi (§100a).
**Tightness.** Il bound è TIGHT: i falsificatori §100 realizzano ep = y_rel con uguaglianza
(q=0) — nessuna costante intermedia possibile (§100a.1). La Scala è **horizon-free** perché
deduttiva (§100b.iv).

### B1.6 [CONDIZIONALE] Teorema del Rifornimento Recente (§98c, docs/OCCURRENCE_SUPPLY_ADDENDUM.md)
**Enunciato.** Sia O eterna non-highway, t un record y-min stretto con posa sotto il seme e
residuo interamente profondo, w = ultime K=101 svolte. Ipotesi per-parola: **(A)** il germe
di w ha onset finito; **(B)** certificato d'orizzonte alla V†_H (prime letture fino
all'orizzonte ESATTO del verdetto, record-side H = t† = max(2600, og_rec+2080) —
decisione §108b-A3 — investendo residuo, k_max(w) e la classificazione "record
profondo"). Allora almeno una cella del residuo è nera a t, dipinta da O nelle ultime
y_rel ≤ k_max(w) epoche-record. **Corollario** (con **(C)** k* = sup di k_max† sulle
K-parole valide, costante ESISTENZIALE non calcolata): ogni eterna non-highway esegue in
ogni finestra scorrevole di k* epoche l'evento "pittura-e-preserva" (svolta R a quota di
rientro ≤ k*, mai più riletta fino all'uso).
**Caveat dichiarati (§98c).** (A) è semi-decidibile e resta ipotesi APERTA (circolarità
dichiarata: una K-parola con germe senza onset sarebbe un controesempio in forma di
configurazione finita); il 75/31 campionari NON sono k*; il teorema forza l'esistenza
dell'evento, non un tasso. Non usava il "5" poi falsificato (§99) né alcuna costante
misurata (§100a.2).

### B1.7 [TEOREMA] Dicotomia del Record (§101a, docs/RECORD_DIVERGENCE_ADDENDUM.md)
**Setup.** Record y-min stretto a t con posa sotto il seme (ry < y_seed_min), t ≥ K=101,
w = svolte[t−K..t); heading al record = 0 (frame = pura traslazione); germe di w =
footprint word-determinato (Finestra-K §87) + bianco altrove; ipotesi **(A)** onset_germe(w)
finito (onset_germe ≡ og_rec: misurato dal record, convenzione §108b-B4); orizzonte
t† = max(2600, og_rec+2080) (= V†_H record-side, §108b-A3); d(t) = primo indice di svolta
divergente tra corsa reale e germe.
**Lemmi (deduttivi).** L0 celle a y_rel ≤ 0 bianche gratis; L1 co-evoluzione fino a d, prima
differenza su una prima-lettura del residuo-daga R†(w), colore reale NERO; L2
d ≥ Cheb(cella di divergenza); L3 la corsa reale CONSUMA la colpevole a t+d; L4 se
d ≥ onset_germe, le svolte in [t+onset_germe, t+d) sono la coda periodica-104 del germe ⇒
**lock W0-like di ride = d − onset_germe passi**; L5' (Replay-Lock alla daga, forma
INDEBOLITA dal pannello §101e) G†=0 ⇒ criterio operativo di onset soddisfatto alla
finestra t† e lock ≥ 2080.
**Dicotomia.** A ogni record vale esattamente una: (T) d < onset_germe (rigetto nel
transiente); (R) onset_germe ≤ d < t† (lock W0-like di ride passi); (E) d ≥ t†.
**Riduzione (unidirezionale, dichiarata):** Link 1 ⟸ "(R)/(E) infinite volte ai record";
(T)-definitivo NON nega Link 1 (lock fuori-record possibili). [Cross-ref §108b-B7:
questa è la riduzione storica dichiarata di §101a; la forma sufficiente VIGENTE per il
consolidamento è quella di B4.19/B4.20: #{t: classe-κ(t) ∧ ride(t) ≥ L₀} = ∞.]
**Struttura per drift (corollario).** Un ride muore solo risalendo nel visitato (y_rel ≥ 1);
per germi drift-giù con transiente pulito la classe (E) = ingresso ⇒ vietata alle eterne
(sotto (A)+(B) di §98c) ⇒ ai record drift-giù l'eterna ha colpevole FORZATA nel transiente.
**Terra.** T-DIV (d per-svolte == d per-celle, due derivazioni indipendenti) 1639/1639;
T-SCALA 1567/1567 (§101b).

### B1.8 [TEOREMA] Lemma del Cuneo (§106a, docs/SPEED_LIMIT_ADDENDUM.md)
**Enunciato.** Record y-min stretto a t, posa (0,0) rel. Per k ≥ 1 sia
Delta_k = t − t_open(riga y_rel=k) (la riga −m apre al record m−1, Scala/T3 §98). Se (x,k)
è stata visitata, allora |x| + k ≤ Delta_k. Corollario (con Lemma 0 §101): sotto il seme,
|x|+k > Delta_k ⇒ mai visitata ⇒ BIANCA a t (**garantita-vergine**).
**Metodo.** Deduttivo (velocità L1 + Scala). Terra-check T2: 6055 celle garantite-vergini
interrogate nel replay, 0 nere (il check è contro i bug, non contro la natura).

### B1.9 [TEOREMA] Teorema del Limite di Velocità (§106a, docs/SPEED_LIMIT_ADDENDUM.md)
**Enunciato.** Ipotesi: record profondo t con parola w, (A) onset_germe(w) finito;
R_T(w) = read-set del transiente (prime-letture del germe < onset_germe, non-footprint,
y_rel ≥ 1), tutte le celle sotto il seme. Se ogni (x,k) ∈ R_T(w) ha |x|+k > Delta_k,
allora d(t) ≥ onset_germe: l'orbita cavalca W0 (classe R o E).
**Contrappositiva (il dente).** Un'orbita che a t NON cavalca (classe T — per le eterne ai
record profondi (E) è vietata dal Rifornimento §98c) soddisfa min su R_T(w) di
[Delta_k − (|x|+k)] ≥ 0 su almeno una cella: vincolo di LENTEZZA per-record, con supporto
word-decidibile (R_T dal germe).
**Terra.** T1: 1622/1622 record di classe T con almeno una cella non garantita, 0 violazioni.
**Caveat (T3, onestà).** I 2 lock reali avevano 0 celle garantite (14/9 tutte "fortunate"):
l'ipotesi del teorema non si è ancora realizzata in natura; il dente morde solo nel regime
estremo-veloce (§106b).

### B1.10 [TEOREMA] Corollario dell'OR — kernel co-moving del lato-record (§107c-bis, docs/DANGER_CLASS_ADDENDUM.md)
**Enunciato.** A un record profondo con parola w (ipotesi A), rigetto (classe T) ⟺ OR dei
colori reali delle celle di R_T(w): il verdetto del record è funzione di |R_T(w)| bit
co-moving; sulla classe pericolosa |R_T| ≤ κ è un OR di ≤ κ bit.
**Metodo/statuto.** Definizionale-deduttivo dai Lemmi 0-1 §101 (nessun contenuto empirico
nuovo; dà l'oggetto per l'attacco). Verificato di terra a §107d (GF3: OR=1 su 1639/1639
canonici; OR=0 esatto sui 2 lock).

### B1.11 [TEOREMA + CERT.] Kernel esteso R_{T,L}: gate fondante (§107e, docs/KERNEL_EXTENDED_ADDENDUM.md, v2 post-ERRATA 107e.0)
**Enunciato (formula adottata dall'ERRATA 107e.0.2).** La bicondizionale
[R_{T,L}(w_t) interamente compatibile ⟺ d(t) ≥ onset_germe+L ⟺ ride ≥ L] è un **corollario
deduttivo dei Lemmi 0-1 §101 sotto le ipotesi del record stretto**; l'implementazione è
VERIFICATA su 1.641 record (i 1.641 casi verificano l'implementazione finita, NON dimostrano
per enumerazione il teorema universale). R_{T,104}(w) = prime-letture esogene del germe a
y_rel ≥ 1 con tf < onset_germe+104, fuori footprint.
**Predicato corretto (ERRATA 107e.0.1):** SUPPORTO word-decidibile, VERDETTO word+griglia
(la compatibilità richiede i colori reali della griglia al record).
**Copertura dichiarata:** la direzione ⟸ ha 2 soli positivi nei dati (i lock); la banda
0 ≤ ride < 104 è VUOTA nel campione; la deduzione copre ciò che il campione non popola.
Gate 1(c) NON indipendente (censura a H ⇒ ride=L per costruzione); i gate probanti sono
d_a==d_b, l'assenza di mismatch a kernel bianco e le regressioni esterne.

### B1.12 [ENUMERAZIONE] Lemma della Lingua d'Approccio (§104c + correzione §104h, docs/DOOR_APPROACH_ADDENDUM.md)
**Enunciato.** Esattamente **671/4096** parole-approccio di larghezza 12 sono realizzabili
(virtual_walk: nessuna rilettura contraddittoria = compatibile con QUALCHE configurazione
finita, convenzione §2) davanti a W0-fase-0; **saturazione GIÀ a 1 periodo di coda**
(correzione dal pannello §105a: il vincolo è interamente nel primo periodo; 671 anche a
×2 e ×3). Le parole osservate ⊆ realizzabili; fra le 671 ci sono 89 famiglie di suffisso-8
⇒ la concentrazione dinamica osservata (85% su UNA famiglia) NON è forzata dalla
realizzabilità.
**Metodo.** Enumerazione esaustiva 2^12; ri-enumerazione indipendente 671/4096 esatto;
witness-backed: 25/25 realizzazioni costruttive corse su simulatore indipendente (§104h).

### B1.13 [TEOREMA] Traduzione deduttiva per-cella del raggio del deposito (§107c.3.2, docs/DANGER_REACH_ADDENDUM.md)
**Enunciato.** Nessun passato valido di NESSUNA profondità legge la cella c ∈ R_T a
distanza-indietro < d_hit(c) (chiusura per troncamento della macchina dei prepend) ⇒ a ogni
record reale che presenta w, il colore di c è deciso da pittura a ≥ d_hit(c)+101 passi dal
record. Raggio esatto del deposito antico: 137–149 passi (LOCKA, 12 celle), 117–137 (LOCKB),
salvo le eccezioni recenti note ((−1,5)@102, (−3,6)@127 di A; (−4,5)@117 di B).
**Caveat (trappola c / §107c.6).** I d_hit sono minimi SOVRA dell'albero: servono per i
negativi e per i budget, MAI per predire quando qualcosa succede davvero (il passato reale
non tocca a 4k–18k passi ciò che l'albero tocca a 16–48).

### B1.14 [TEOREMA] Verso KILL di σ=1: parole deduttivamente sicure a profondità dichiarata (§107b.4.3/§107b.5, docs/DANGER_BACKWARD_ADDENDUM.md; conteggio esatto §107c.4)
**Enunciato.** Se σ_D(w) = 1 esatto (OGNI passato record-compatibile valido di profondità D
contiene uno scudo nero su R_T(w)), allora ogni record reale che presenta w è un rigetto
garantito alla profondità dichiarata D (il passato reale è uno dei passati enumerati).
**Statuto.** Deduttivo per-parola, a profondità dichiarata. Conteggio esatto (P2, §107c.4):
71/1459 parole canoniche (4,9%) a σ=1 esatto con D=22. L'unico estremo deduttivo robusto è
σ=1 (ERRATA §107d.0.5): i valori intermedi dipendono dalla misura uniforme sull'albero e
dalla massa open (trappola tt); σ≈0 = ASSENZA di certificato nero, non certificato bianco.

### B1.15 [TEOREMA descrittivo-strutturale] Semantica della macchina dei prepend (§107b.3, docs/DANGER_BACKWARD_ADDENDUM.md)
**Enunciato.** Per una cella di R_T (∉ footprint(w)), il colore al record è deciso
dall'ULTIMA visita del passato esteso (lettura bianca ⇒ lasciata nera; lettura nera ⇒
lasciata bianca); la decisione è STABILE sotto prepend più profondi (i prepend aggiungono
solo visite più vecchie). Classi al cap D: SHIELD / WHITE_ALL / OPEN, con "indeciso ≠ bianco"
(soundness a profondità finita, imposta dal round-2 §107b.1).

---

## STRATO 2 — CERTIFICAZIONI FINITE DELL'IMPLEMENTAZIONE

### B2.1 `alpha1/alpha1_engine.c` (§57.1, docs/ALPHA1_FABRY_ADDENDUM.md)
Simulatore C self-contained (search/reseed/dump), convenzione identica a libant.c, morso =
lettura fresca-bianca byte-compatibile con morso_census.py. **Gate:** griglia vuota → onset
9977 esatto; (7,−7) → 106258; highway densità morso 22/104; Berlekamp–Massey su highway
L≈102 vs Bernoulli ≈n/2. Fix reset-solo-celle-toccate (1.8k → 31.7k semi/s su 14 shard;
trappola g/§57.7-a). Semi riproducibili dal solo rngstate a 64 bit.
**Non prova:** nulla sulle orbite eterne; è il motore, non un risultato.

### B2.2 Sonda δ4 e catena hazard/checklist (§58–§60, docs/DELTA4_BETA_ADDENDUM.md, DEBT_LOCK_ADDENDUM.md, DEBT_LOCK_2D_ADDENDUM.md)
`delta4_long_orbits.py`: rigenera le 24 orbite da rngstate, valida i morsi byte-per-byte
contro dumps_all.txt (24/24); `debt_lock_hazard.py`/`debt_lock_2d.py`: protocollo causale
[t−L,t) → [t,t+H), deterministico. **Non provano:** D(t) è match simbolico W0-like, non
checklist T3'; anchor correlati; campione onset-alto.

### B2.3 Pipeline checklist T3' (§61–§64, docs/LOCK_CHECKLIST_ADDENDUM.md → CHECKLIST_VECTOR_MODEL_ADDENDUM.md)
`lock_checklist_probe.py` ricostruisce E(k) da W0 (indipendente dai vecchi pickle), lock
per-allineamento left-maximal; controllo positivo onset veri 24/24 (entry_horizon=1248 —
check di frame e colori, NON nuova dimostrazione di T3'). `checklist_mixing.py` (dedup),
`checklist_vector_geometry.py` (vettore completo), `checklist_vector_model.py` (set-cover
sui CSV, senza nuova simulazione). Coerenza §66: riga fase reale a L=1600 coincide con §63
su tutti i tentativi (compare_mismatches=0). **Non provano:** β; il set-cover è descrittivo,
non un classificatore out-of-sample; compressione campione-specifica (§64.9).

### B2.4 `alpha1/door_defect_profile.py` (§66) e `potential_segment_scanner.py` + audit (§67–§69)
Profilo 22 fasi × orizzonti 208/512/1600 su 810 tentativi (53.460 righe fase-orizzonte);
audit §68/§69 da CSV senza risimulare (`endpoint_monotone_audit.py`,
`compat_endpoint_audit.py`). Self-test §5 verdi prima di ogni run. **Non provano:**
l'inesistenza di ogni potenziale (solo i proxy testati e le riparametrizzazioni
order-preserving, §68.7).

### B2.5 Scanner co-raggiungibilità e sonde §70–§74 (docs/COMPAT_EVENT_COREACHABILITY_ADDENDUM.md)
`compat_event_audit.py` (600 eventi, pre/post singolo passo deep-black, compare_bites
validato); `t3_coreachability_pair_scanner.py` (bucket per patch normalizzato completo,
witness con verifica replay interna; sanity R=4: 15 witness); `door_discriminant_linf_profile.py`
(dedup 786/786, depth==first_bad_offset 786/786, drift_phase esatto da W0);
`door_comoving_class_passrate.py` (prime morti ritrovate 786/786);
`door_gf2_rank_gate.py` (rank/affine rank GF(2), quota C0=0 da seed ricostruito).
**Non provano:** α1; il witness R=8 è esistenza/non-vacuità, radius-fragile (§71.3);
zero collisioni a R=16 = sparsità combinatoria, non confine strutturale.

### B2.6 Gate-zero GA: `GA_stress_agent/ga_gate_zero_audit.py` (§75, docs/GA_GATE_ZERO_ADDENDUM.md)
Verdetto FAIL certificato: due anchor replayabili (orbita 5, rngstate
16489936061346709332, fase 98, t=60320/60840) collassano nello stesso stato A0(r≤8,K=80,D0=80)
con prefisso T3' diverso (h_1600 = 1014 vs 494); prima differenza del patch a r=9; witness
sintattico a offset 138, rel (3,9). **Cosa certifica:** A0 sound come sovra-approssimazione ma
CIECO su T3' ⇒ niente classificazione SCC; `unknown` mai promosso a no-entry (§75.5).
**Non prova/nega la congettura:** impedisce una prova sbagliata (§75.6).

### B2.7 Kernel A1 della porta (§78.3–78.11, docs/GATE_ONE_COMOVING_ADDENDUM.md)
`gate_one_comoving_audit.py`: impronta co-moving delle 22 fasi porta stabilizzata ai tagli
1040/5200/10400/20000 (fase 98: 44 celle identiche mentre le letture grezze crescono
244→4251); |S_g| ∈ [38,52], **max_g rho_g = 9** = il L∞≤9 empirico §72 (metà spaziale
certificata da W0); sufficienza sul testimone §75 (stessa cella co-moving decisiva (7,5),
12/44 strisce separano). `a1_budget_certificate.py`: **construction_sound=1** — ogni
first-bad è dentro S_phase (786/786) e la ri-derivazione a budget P riproduce esattamente il
verdetto ground-truth; curva |unknown| vs P monotona, **unknown-free a P=15** sui 786
attempt; 9/131 classi posizione-sola ambigue, risolte dai contenuti delle strisce.
`decisive_depth_sweep.py` + `new_seed_depth_sweep.py`: 2014 attempt (24 orbite + 70 semi
freschi indipendenti onset 105k–180k), P mai > 15, ~97–98% a P=0, nessun trend con T.
**Non prova:** il bound uniforme di P su TUTTE le storie raggiungibili (l'oltre-budget è
vuoto sul campione, NON dimostrabile-vuoto = Link 1; §78.10). NB §78.12: A1 (porta,
one-shot ai lock) e δ_r (morsi, continuo) sono DUE certificati β complementari, non un
automa-finestra a raggio 9 (infattibile e oggetto sbagliato).
**Statuto DECISO (§108b-B1):** la stabilizzazione dell'impronta è [C], NON [T] — i
quattro tagli verificano una stabilizzazione FINITA; la promozione a teorema
richiederebbe un lemma formale di periodicità-con-drift valido per ogni offset e per
tutte le 22 fasi (mai formalizzato). E non implica comunque un budget temporale P
uniforme.

### B2.8 `alpha1/consumption_ledger_probe.py` (§79, docs/CONSUMPTION_LEDGER_ADDENDUM.md)
Simulatore SET-BASED INDIPENDENTE (non alpha1_engine.c), validato su: vuota → 9977 esatto;
W0 periodo 104/58R/drift; 0 violazioni di alternanza su 106.000 passi su (7,−7).
**Statuto dichiarato: SCOUT, non risultato certificato** — "deep" = proxy d'età (>104/>1040),
NON la delta_r outside-window 9×9; conteggi mai riprodotti con alpha1_engine.c.
**Decisione §108b-B5:** §79 citabile SOLO come [O]/SCOUT; nessuna promozione e
NESSUNA riproduzione ora (il debito DC.5 resta archiviato come tale).

### B2.9 Catena motivi §80–§84 (docs/DEEP_MOTIF_SATURATION_ADDENDUM.md → ROTOR_LANGUAGE_ADDENDUM.md)
`deep_motif_saturation.py` (run Ryzen reale, dinamica e definizione deep riusate identiche
da delta4_long_orbits.py); `deep_motif_pruned.py` (§81: full-mode riproduce ESATTAMENTE i
numeri §80 su 24/24; inclusioni pruned104 ⊆ pruned208 ⊆ full 0 violazioni; CERTIFICATO
Ryzen 2026-07-02 bit-identico); `core_tail_profile.py` (§82: doppio gate — nev esatti §80
24/24, nucleo 1.572 con massa identica §81; CERTIFICATO Ryzen); `highway_language_probe.py`
(§83: tre gate, incluso L_hw saturo 10 vs 20 periodi; CERTIFICATO Ryzen);
`rotor_language_profile.py` (§84: match a meno di rotazione — trappola d; ≥3 periodi pieni;
baseline nulla condizionata a lettura nera — metodo reso OBBLIGATORIO dalla trappola s).
**Non provano:** nulla sull'eterno (trappola i); §84 con QMAX=15 non esclude periodi lunghi
non-censimento.

### B2.10 Certificatore automa (LRRRR)^3 (§85b, docs/LRRRR_HALO_ADDENDUM.md)
`lrrrr_avoidance_certificate.py` r=1,2,3 (conteggi stati 15/403/45.971 coerenti coi
selftest): sopravvissuti stabili 4 a r=2,3 — **INCONCLUSIVO come teorema-finestra**;
decisione §108b-B8: si afferma soltanto il Teorema Halo (B1.3) e l'esistenza di ALMENO
una classe di sopravvissuti realizzata dal testimone (B4.9); NESSUNA realizzabilità
attribuita separatamente a tutti e quattro (censimento mai fatto, DC.8). `lrrrr_depth_profile.py` con tripwire catena
deep_4⊆…⊆deep_1 = 0 violazioni. **Lezione certificata:** archi di assunzione solo-assW =
campanello di realizzabilità (trappola t).

### B2.11 Strumenti §86 + bug-story (docs/TRAIL_HALO_ADDENDUM.md §86.6)
`halo_occupancy_profile.py`: self-test 4-heading + ⟺ randomizzato 20k + snapshot 1000;
gate §85a per orbita esatti 24/24; tripwire ⟺ halo 0 violazioni. Bug-story a verbale: halo
valutato con offset invece di celle assolute, catturato dal tripwire ⟺ sui dati reali (273
violazioni su orbita 0) — antidoto permanente: self-test con formica in posizione ≠ origine.

### B2.12 `alpha1/record_supply_census.py` (§98, docs/OCCURRENCE_SUPPLY_ADDENDUM.md)
Gate esterni tutti assert-verdi (n record 1639 == §89a; tripwire 1620 == §89a; colpevoli
225.012 == §89b; da_seme 3.722; istogrammi == §89b; onset == header 24/24); tripwire T1–T4
zero violazioni. Pannello §98e: lente A indipendente (colori dalla traiettoria, non dal
replay) 18/18 campi bit-identici su 3 orbite; lente B 4/4 esche beccate con baseline
positiva; lente C 1 ROSSO logico riparato IN SESSIONE (minimi per-record aggiunti).

### B2.13 `alpha1/record_minep_hunt.py` (§99–§100, docs/MINEP_HUNT_ADDENDUM.md, DOUBLE_TAIL_ADDENDUM.md)
Cacce PREREGISTRATE (falsificatore + potenza + catena disgiunta verificata + verdetto
EMESSO DAL TOOL): catena-1 5000 semi, catena-2 25.000 (BASE2 disgiunzione riverificata da
lente). Gate canonici 24/24 bit-identici a §98 (6 campi + istogramma per-record + zero-G0).
Lenti: §99 6/6 testimoni bit-identici su 10 campi; §100 4/4 falsificatori + 2/2 autopsie
bit-identici. Riparazioni a verbale: 230 G=0 scartati in silenzio (trappola pp) riparato
in-tool; confronto per EPISODI non per record (ROSSO §100e riparato).
`v_dagger_autopsy.py`: 2/2 violatori, prima cella di divergenza (NON il residuo V†
completo — caveat §100b.i). **Non provano:** nessuna costante dell'orologio-record
(tutte quantili, trappola qq).

### B2.14 `alpha1/record_divergence_census.py` + `record_divergence_hunt.py` (§101, docs/RECORD_DIVERGENCE_ADDENDUM.md)
Gate esterni verdi (1639, 1620, 225.012, 3.722, hist == §89/§98); tripwire T-DIV 1639/1639
(due derivazioni indipendenti di d), T-VDAGGER, T-SCALA 1567/1567. Caccia catena-3 (8000
semi) preregistrata IN TESTA AL FILE, disgiunzione verificata, potenza realizzata 81.665.
Pannello §101e: lente A footprint dalla GRIGLIA REALE 40/40 bit-identici + 3/3 F2 + 8/8 F1
(`record_divergence_lens.py`, `record_lock_autopsy.py`); lente B 3/3 esche beccate + baseline
pulita + terra-check Lemma 0 (E4-v1 riconosciuta incapace di scattare e sostituita —
corollario cc). **Non prova:** occorrenza per l'eterno; riduzione dichiarata unidirezionale.

### B2.15 Sonde porte §102–§104 (docs/FASCIA_DOOR_ADDENDUM.md, FRESH_PHASE_ADDENDUM.md, DOOR_APPROACH_ADDENDUM.md)
`fascia_door_probe.py`: gate onset==header 24/24, coda per==per2, fase univoca (104
rotazioni W0 tutte distinte), esca bit-corrotto beccata. `fresh_onset_phase_census.py`
(§103): preregistrata (falsificatore F, potenza ≥1000, verdetto dal tool), gate 24/24
canoniche bit-identiche a §102. `door_approach_census.py` (§104) + pannello §104h TUTTO
VERDE: A1 30/30 (simulatore proprio + rilevatore onset RISCRITTO + riferimento W0.npy —
cross-valida la coppia di file canonici §2); A2a ri-enumerazione 671/4096 con checker
riscritto; A2b 25/25 testimoni di realizzazione; A3 20/20 fasi germi ai record; esche E1/E3-v2
beccate, E3-v1 promossa a misura (saturazione a 1 periodo). **Non provano:** teorema
d'occorrenza; quote = campione.

### B2.16 `alpha1/lock_hole_autopsy.py` (§105b) e `speed_limit_theorem.py` (§106)
§105b usa SOLO strumenti già pannellati (run_real/germ_turns_from_real: 40/40+11/11 §101e,
30/30+20/20 §104h); coerenza interna episodi/controlli (read-set bianco ⟺ classe R).
§106: terra-check T1/T2/T3 con replay canonico; refuso d'etichetta dichiarato nel JSON
("neg (tutte garantite)" conta i record con ALMENO una cella garantita — i check T1/T2 sono
indipendenti da esso, §106d). **Decisione §108b-B6:** il campo storico resta LEGACY con
etichetta errata; la semantica canonica è "almeno una cella garantita"; non usare il nome
storico come evidenza semantica e non alterare retroattivamente il dato.

### B2.17 F0/F2 dello Scudo Antico (§107b, docs/DANGER_BACKWARD_ADDENDUM.md)
`danger_geometry_census.py`: G0 R_T ∩ footprint = ∅ con footprint INDIPENDENTE; G1
istogramma bit-identico a danger_class_sizes.json §107a; G2 cross-macchinario sui 2 lock
== lente reale §101e. `danger_backward_autopsy.py` v2 (classificazione AL CAP — la v1 a
foglie potate era misura politica-pesata, trappola rr): GA lente naive bit-identica; GB
passato reale 2/2 nella macchina (cella consumata @102 ritrovata); lente ESTERNA
indipendente (forza bruta 2^d riscritta da zero): LOCKA D=16 17/17 livelli bit-identici,
claim σ=1 confermato con enumerazione esaustiva indipendente (2.808/2.808 shield).
Convenzione dichiarata dalla lente: onset_germe misurato DAL RECORD = **og_rec**
(decisione §108b-B4: la dicitura storica "asse assoluto og+101" è ELIMINATA; si usano
og_rec, og_win = K + og_rec, tempo assoluto t_record + og_rec; sempre ride = d − og_rec —
convenzione propagata dalla testa a ogni strumento futuro, chiude §107b.6). **Non prova:** i conteggi a D=28 sono a profondità dichiarata
(la lettura "bit antichi = irraggiungibili" è poi caduta col cap, trappola ss).

### B2.18 Motore reach C + P2 (§107c, docs/DANGER_REACH_ADDENDUM.md)
`danger_reach.c` (10-11 ns/nodo/core; 51G nodi/37 s): validazione totale — R0 regressione
bit-identica al summary §107b (18.161 / 2.138.444 nodi); R0b; R1 LOCKA (−1,5) d_hit=1; RG
D_geo ≤ d_hit su 677/725 celle; lente esterna indipendente (brute-force per livelli MAI
letto lo strumento del titolare): 17/17 e 15/15 livelli bit-identici; R2 port C vs Python
bit-identico (382 e 571 first_hit); R2-profondo: prefissi indipendenti dal cap; somme shard
== Python. `danger_sigma_vocab.py`: 1459/1459 parole ESATTE a D=22, zero troncate,
regressione 66/66 su §107b. `danger_reach_real.py`: passato reale, riproduzione del cuneo
vergine §105b con macchinario nuovo. **Non prova:** i d_hit sono SOVRA (etichetta
obbligatoria); n=1 per episodio sul reale (descrittivo).

### B2.19 Strumenti §107d (v2 — declassati a DIAGNOSTICA DESCRITTIVA, docs/SHIELD_MAP_ADDENDUM.md)
`danger_shield_calibration.py` (F3): gate meccanici verdi — GF0 istogramma bit-identico
§107a, GF1 replay bit-per-bit, GF2 lock nb=0/14 e 0/9 (controllo KILL), GF3 deduttivo OR
bidirezionale ⇒ **macchinario di lettura-griglia VALIDATO**. `danger_wedge_map.py`: GW0
solo "coerente entro tolleranza 0,1%" (NON bit-identico: totale ricostruito da ricchezza
arrotondata — ERRATA 107d.0.7; GW2 bianca≠vergine dichiarato ma NON implementato, 107d.0.6).
`danger_reach_vocab.py`: 59/59 misurate, profondità per-parola 45–48 dichiarate.
**Non provano:** nessuna conclusione interpretativa (tutte ritirate in 107d.0, vedi B4.19).

### B2.20 `alpha1/kernel_extended.py` (§107e, docs/KERNEL_EXTENDED_ADDENDUM.md v2)
Gate preregistrati nell'header: GATE 1 verde su 1641/1641 (d_a == d_b; kernel bianco ⇒
nessuna divergenza in [0,H); unknown 0); GATE 2 determinacy (verdetto = funzione di
(parola, colori di R_{T,104})); GATE 3 forense su storia visite (bianco/vergine esatto);
GATE 4 cut preregistrato prima dei verdetti; regressioni bit-esatte (d CSV §101 1639/1639;
d_full lock 324/449); regressione interna: restrizione tf < og == transient_readset §106.
Il "terzo macchinario indipendente" della v1 è corretto in "terzo percorso di controllo
PARZIALMENTE indipendente" (riusa funzioni e artefatti comuni — ERRATA 107e.0.4).
**Non prova:** la quantità di Link 1 (#{t: classe-κ ∧ ride ≥ L_0} = ∞) resta NON dimostrata.

---

## STRATO 3 — OSSERVAZIONI CAMPIONARIE

Nota generale di scadenza: TUTTE le voci di questo strato sono misure su orbite finite
convergenti (trappola i: il controfattuale eterno non si decide col finito); i campioni
"24 orbite lunghe" sono selezionati per onset alto (trappola h; lettura within-orbit);
ogni soglia/massimo è un QUANTILE con data di scadenza (trappola qq).

### B3.1 Erosione del pavimento del morso (§57.4, docs/ALPHA1_FABRY_ADDENDUM.md)
24 orbite 252k–313k (da 9,8·10⁸ semi, 88.521 hit ≥100k): max-stall 90–104 periodi, cresce
~linearmente con T; densità di morso ~0,05; floor a finestra L=1040 = 0 su tutte, L=10400
mediana 0,006 con uno zero esatto; kill-shot pre-lock: tail/core 1,13, gli stalli grossi
vivono nel caos genuino. **Unità:** passi/periodi; within-orbit. **Caveat:** evidenza forte,
NON prova (§57.6); best onset 313.358 = massimo campionario (trappola 57.7-d).

### B3.2 La non-località r=4 non erode (§58.3, docs/DELTA4_BETA_ADDENDUM.md)
Stesse 24 orbite: tasso nero fuori-finestra r=4 mediano 0,2334/passo (morso fresco 0,0537);
tail/core 1,058 vs 0,614; minimi mobili 9,0×/16,0×/27,4× delta4_auto=2/313 per L=313/1040/
10400 (il minimo CRESCE con la finestra mentre il morso fresco tocca 0). Lock simbolici
D≥40 in tutte le 24 (run min 113/med 130/max 167). **Caveat:** lock solo simbolico, senza
dogana (§58.5).

### B3.3 Hazard deep→lock anti-correlato; bite è l'innesco (§59.2/§60.2)
Protocollo causale [t−L,t)→[t,t+H): hazard di D≥40/80 decresce monotono coi quantili
deep-black (ratio top/bottom 0,13–0,48) e cresce con fresh-bite (2,17–10,23). Griglia 2D:
effetto bite entro strisce deep mediano +0,1373 (D≥40), effetto deep entro strisce bite
−0,0350; best cell = (deep basso, bite alto). **Caveat:** falsifica il ponte semplice, non
il ruolo teorico del debito (§59.4).

### B3.4 Lock → checklist: verdetto esatto sul campione (§61.2, docs/LOCK_CHECKLIST_ADDENDUM.md)
3303 lock pre-onset, 891 gate-lock: **891/891** morti esattamente alla prima lettura
esogena cattiva; 24/24 onset veri passano il controllo positivo. Morte bilanciata:
missing_black 447 / frontier_black_collision 444. A D≥80, 105/112 sono gate-lock.
**Caveat:** conteggio esatto sul campione delle 24 orbite; non prova β (§61.5).

### B3.5 Ricampionamento della checklist (§62, docs/CHECKLIST_MIXING_ADDENDUM.md)
810 tentativi porta unici (24 OK, 786 KO), hazard grezzo 0,0296; riuso cella critica
1/762 consecutivo, 1/12.945 intra-orbita; tipo di errore quasi senza memoria
(P(frontier|frontier)=0,5227 vs P(frontier|missing)=0,5232); parità: nessuna classe
semplice. **Caveat:** un solo successo per orbita per costruzione; non test iid (§62.2).

### B3.6 Porta mobile e vettore (§63, docs/CHECKLIST_VECTOR_GEOMETRY_ADDENDUM.md)
57.177 letture esogene; 786/786 prima cattiva == morte; mismatch nel vettore (2 periodi):
mediana 6, max 29; stessa origine porta consecutiva 0/786, L1 origine mediana 43 (max 222);
heading delta tutti popolati.

### B3.7 Compressione del vettore (§64, docs/CHECKLIST_VECTOR_MODEL_ADDENDUM.md)
Full-vector diagonale: 786/786 KO con mismatch, 24/24 OK senza. Due periodi coprono
774/786 (12 mancati, tutti frontier oltre 208, offset 268…1591). Prime morti: bucket 45-77
= 598/786; 98-99 necessario (rimuoverlo lascia 37 scoperti). Greedy: 37 offset / 66
componenti phase-conditioned mantengono la diagonale. **Caveat:** campione-specifica,
descrittiva (§64.9).

### B3.8 Diagnosi di non-località della checklist (§65.2, docs/CHECKLIST_NONLOCAL_STRATEGY_ADDENDUM.md)
Prime cattive a offset 45-99: 677/786 (0,861); i 12 oltre due periodi hanno L1 16…69,
L∞ 10…36. **Statuto (correzione Pauli §65.6):** diagnosi strategica/campionaria, NON
teorema di non-località matematica di T3'.

### B3.9 Profilo 22 porte lock-condizionato (§66.3, docs/DOOR_DEFECT_PROFILE_ADDENDUM.md)
Fase reale best unica 810/810 a ogni orizzonte; fasi compatibili alternative: 0 clear,
h mediana 2, max 5; incompatibili muoiono a h=0. Asimmetria nominata (§66.0-a):
identificare la porta = locale; decidere se la porta vera entra = globale.

### B3.10 Witness co-raggiungibile a R=8 (§71.2, docs/COMPAT_EVENT_COREACHABILITY_ADDENDUM.md)
Orbita 5, fase 98, patch 17×17 identico, bit identico: h_g divergenti (494 vs 513/1014),
discriminante offset 494, rel (15,13), L∞=15 > 8, frontier_black_collision. R=16 sugli
stessi anchor: 0 collisioni = baseline di sparsità (spazio patch 33×33 enorme).
**Statuto:** esistenza/non-vacuità dello schema; non supporta da solo un potenziale (§71.3).

### B3.11 Discriminante co-moving L∞ ≤ 9 (§72.5, docs/COMPAT_EVENT_COREACHABILITY_ADDENDUM.md)
786 fallimenti reali: raw max L∞ 36 → co-moving max L∞ **9** (sottraendo
floor(offset/104)·drift_phase); 131 classi osservate; Pearson depth vs L∞: 0,727 raw →
0,100 co-moving. La crescita grezza era drift del tubo W0.

### B3.12 Pass-rate delle classi co-moving (§73.3)
810 tentativi, 101.387 letture target: 91.657 pass / 9.730 fail (0,9040); 130/131 classi
miste pass/fail; unica zero-pass a supporto 4; top class (0,−5,−2,0): 4224/486.
Chiude il falso negativo "dogane co-moving sempre sbagliate".

### B3.13 Rango GF(2) delle dogane (§74.3)
Fase 0 all pre-onset offset≤1600: 304 attempt × 187 colonne, rango 138 (nullità 49),
C0=0 0,9963, zero colonne costanti/duplicate. Fase 0 depth 80+ prefisso ≤103: rango 4/19
(prefisso quasi-W0). **Lettura §74.4:** dipendenze shallow reali ma troppo deboli per
UNSAT; deficit profondi sample-limited o circolari.

### B3.14 Profondità decisiva P della porta (§78.9/78.11) [QUANTILE]
2014 attempt falliti (24 orbite + 70 semi freschi): P concentrato a 0 (~97-98%), max 15
(mai superato), nessun trend con T (corr 0,057 e 0,245); a orizzonte 10400 zero censure.
**Caveat:** orbite convergenti; l'inviluppo eterno resta non dimostrato (§78.11).

### B3.15 Ledger di consumo su (7,−7) (§79.2) [SCOUT]
106.000 passi pre-onset: creazioni nero 58.984 (~0,556/passo) > distruzioni 47.016
(~0,443/passo), pool +11.968; recycle-fed 61,7% (deep+ 69,3%); inflow B-T ~4:1 sul consumo
deep; età rivisita-nera med 8 / p90 108 / max 4068 (coda age>1040 = 0,6%, coincide con lo
stallo rotore §77). **Caveat:** una sola orbita, proxy d'età, non cross-validato con
alpha1_engine (§79.4). [Decisione §108b-B5: statuto definitivo [O]/SCOUT — nessuna
promozione, nessuna riproduzione ora.]

### B3.16 Saturazione dei motivi: NO (§80.1) [NO-GO-EMPIRICO]
24 orbite: r=3 ~99,4% eventi unici (73.959/74.416 su orbita 0); scoperta ultimo20%/primo20%
mediana 1,14; pooled unione/somma 0,979; intersezione 24 orbite = 19 motivi su ~1,5M.

### B3.17 Motivo potato + vocabolario universale (§81.1)
Potato H=104: ~57% unici, scoperta 0,811 (non satura — trappola o estesa); MA intersezione
24 orbite = **1.572 motivi** (~83×), massa eventi 35,63% [34,40–36,33], stazionaria per
quintili, ortogonale all'età; taglie med 7, zero vuoti. H=208: 1.242 / 27,2%.

### B3.18 Omogeneità del nucleo (§82.1)
Massa-nucleo 35–36% su OGNI bucket d'età (≤104 … >104000) e per alimentazione (morso-fed
36,9% vs recycle 35,4%; recycle-fed = 89,9% degli eventi sulle orbite mature); unica cella
non piatta: giovani morso-fed 42,95% con decadimento monotono. Nucleo in chiaro: top-10 =
12,4% del nucleo, catene lineari/diagonali di 3 celle sul cammino imminente.

### B3.19 Disgiunzione caos/highway (§83.1)
L_hw = 46 parole ESATTE (= letture nere di W0), saturo, identico su 24/24; sovrapposizione
col nucleo 2/1.572; massa deep-black pre-onset su L_hw 0,05% [0,01–0,42]; top-20 del nucleo
in L_hw: 0/20. (Scala del confronto: r=3, H=104 — §83.2.)

### B3.20 Rotori e periodicità di svolta (§84.1)
Eventi-nucleo su una qualunque cavalcata: 4,55%; LRRRR: 0 su ~1,5M vs baseline 0,18%
(poi TEOREMA via §86); rotori r≥2 assenti anche alla baseline (poi impossibilità B1.4);
p15: quota 0,0194% vs baseline 0,0103% (eccesso ×1,9) con massa-nucleo 0,00% esatto su
24/24 — prima crepa nell'omogeneità (delimita la trappola q); periodica generica q≤15:
3,47% con massa-nucleo 47,11%.

### B3.21 Occupazione dell'halo ai deep (§85.1/§86.2)
r* = 1 (evitamento già a deep_1: 0/2.323.679; i 5.716 match reali tutti in-finestra,
0,67%); k_r (neri nell'halo): min 1 su 24/24 (il teorema della Scia è STRETTO — nessun
enunciato "≥2" da attaccare), moda 4–5, media 4,563; eventi k_r=1 SOLO sulle 3 celle di
scia; s=0 (halo interamente rifornito nell'intervallo) 24,37% — nessun argomento statico
alla scrittura poteva coprire i deep.

### B3.22 Censimento della Scala in epoche (§98a)
1639 record canonici; 188.234 colpevoli profonde: età med 3 EPOCHE (vs 2002 passi — stesso
oggetto, due orologi: trappola nn), max 31; q = y_rel − ep med 9. Per-record (1174
interamente profondi): min_ep med 2 max 5 [QUANTILE, morto a §99]; scia quasi-universale
91,5% (min_age med 107 = K+6); min_lag med 0 (88,2% entro P); coda 8,5% senza colpevole
entro 2K (fino a 24.464 passi).

### B3.23 Caccia catena-1 (§99) [QUANTILE + FATTO NUOVO]
5000 semi freschi non selezionati (onset med 3.964): min_ep max 8 (6/6980 = 0,086%) —
"5" era quantile; firma-W0 dei testimoni UCCISA dalla baseline (frammento ≥34 nel 23-29%
dei record ordinari); FATTO NUOVO (trappola pp): **2 violazioni REALI del
tripwire-orizzonte** su 29.084 record (residuo V(onset+P) bianco, onset a 2.372/14.757
passi) = prima realizzazione del caveat V† di §98c — il meccanismo G≥1 è sano SOLO alla V†.

### B3.24 Caccia catena-2 e coda doppia (§100) [QUANTILE]
25.000 semi: min_ep max 12 (5→8→12 senza saturazione); 4 falsificatori doppia-coda =
2 EPISODI (min_ep 9-12 E min_age 3063-5050 > 10P); i falsificatori realizzano ep=y_rel con
q=0 (soffitto TIGHT); guarigione V† 2/2 (divergenza a d=542/750 su cella NERA reale a
y_rel 21/25; la † profonda rispetta ep≤y_rel: 19≤21); fascia word-mediated: 45 testimoni →
14 parole (>20σ vs coupon-collector; 3 pesanti cross-catena) MA promozione NEGATA dalla
baseline stratificata (concentrazione già a min_ep=4: top-60; gradiente distinte
90,5%→42%→31%): REGIME, non famiglia.

### B3.25 Censimento divergenza + caccia catena-3 (§101b/c)
Canonici: classe T 1639/1639 (R 0, E 0); d med 17 (0,6% del transiente); min_cheb† med 3
max 8 [QUANTILE: →19 su catena-3 con 112 falsificatori]; min_ep† med 2 max 5; G† med 142,
zeri 0; drift-giù 891/1639. Catena-3 (8000 semi, 82.243 record): **F2 REALIZZATO — primi
2 EPISODI di lock ai record** (ride 269 e 384 passi = 2,6/3,7 periodi); P3 FALSIFICATA
(103/112); **V† 0 violazioni su 82.243** (578 G†=0 tutti fisiologici); d max 2711 in classe
T. SALDATURA: le parole dei 2 lock = STESSA parola 101-bit cross-seme (+ shift-10), dentro
i 14 testimoni della fascia §100 ⇒ fascia = classe delle parole-porta.

### B3.26 Fascia = porta-0; due porte reali (§102b/c)
Fascia: 12/14 a fase W0 = 0 esatta, 2 a 99/102, 0 altrove; niente suffisso-nucleo (comune
globale 3 bit; troncare cambia l'onset del germe). Onset reali 24 orbite: porta-0 20/24
(10 esatte + 10 ext 1–7), porta-24/25 4/24, zero fuori-cluster [n=24 — superato da §103].

### B3.27 Spettro porte su semi freschi (§103a) [QUANTILE sui cluster]
2500 semi catena-3: porta-0 95,4% (47,3% esatta + 48,1% ext), porta-24/25 4,1%,
12 fuori-cluster (0,48%) su fasi {16,30-31,91-92} = micro-porte (falsificatore F
realizzato: lo "zero fuori" di §102 era artefatto di n=24). Istogramma ext UCCIDE il
modello a moneta: **picco a ext=5 (487 vs ~78 attesi) e buco a ext=3 (1 vs ~156)** —
approccio strutturato di ~5 passi in fase 99.

### B3.28 Vocabolario d'approccio e spettro ai record (§104a/b/d)
Top-10 approcci-12 = 68% degli ingressi; ext5 = 1 parola (`RLLRRLRLRRRR`, 88% del picco);
fase-0 = famiglia suffisso-8 `LRRRRLLL` 85%; 11/14 germi fascia = parola IDENTICA
`RLRRLRRRRLLL` (#2 reale). Spettro dei germi ai 1639 record canonici: porta-0 95,4%,
porta-24/25 4,5%, micro 0,2% — **identico allo spettro degli ingressi freschi** ⇒ la metà
"occorrenza" collassa su B-T (i tentativi di porta-0 sono lo stato generico dei record);
riduzione §104d: Link 1 ai record = lim sup [d − onset_germe] ≥ L0 [FORMULAZIONE STORICA:
i quantificatori sono stati corretti da §107d.0.10; per decisione §108b-B7 nel
consolidamento si cita SOLO la forma B4.19/B4.20 — §104d resta esclusivamente storia
dell'errata].

### B3.29 Meccanismo dei lock ai record (§105b.1)
Episodi vs controlli same-seed: read-set 14 e 9 celle (vs 454 e 931), tutto bianco, celle
mai-visitate 13/14 e 9/9, nel cuneo vergine del drift laterale (drift_x = −6 in entrambi);
consumo a catena: la cella visitata di A ripulita 102 passi prima (= consumo del tentativo
precedente, Lemma 3). FALSIFICATO il "filo del rasoio": colpevoli = pose-record solo 10%
(44% entro cheb 1, n=120) — lo scudo è detrito d'escursione, SPESSO.

### B3.30 Distribuzione della classe pericolosa (§107a)
|R_T| sui 1639 canonici: min 4 / med 302 / max 3956; ≤15 = 4 record (0,2%, 4/24 orbite,
contiene i 2 lock: 14 e 9); ≤50 = 66 (4,0%, 20/24). onset_germe della classe ≤15: med 204.
107c-ter: accoppiamento (i)∧(ii) DEBOLE nel campione (dt_burst: classe ≤50 med 4798 vs
8146; ≤15 med 3218, n=4). κ = parametro, nessuna soglia (qq).

### B3.31 Geometria word-side e σ_D (§107b.2/107b.5, post-NB)
theta_min DEGENERE (=2, moda >96%: il Cuneo non forza mai l'intero read-set word-side);
classe ≡ taglia ≡ direzionale ≡ transiente corto (coh 0.92→0.535 con n; lock 0.93/1.00);
σ_22 sulla classe ≤50 BIMODALE (q25 0.0002 / med 0.103 / q75 0.902); i 2 lock σ_22 = 0.080
e 0.0012, NON estremi (24/66 a σ≤0.01) ⇒ (ii) senza discriminante word-side. A D=28:
12/14 e 5/9 celle irraggiungibili [SUPERATO da §107c: chiude a 48/36 — trappola ss];
WHITE_ALL = 0 ovunque. ["lock-capable" RITIRATO — §107d.0.5.]

### B3.32 Reach: chiusura dell'orizzonte e cuneo vergine (§107c.3)
Tutte le celle di R_T raggiungibili: d_hit ≤ 48 (A, D_exh=55) / ≤ 36 (B, D_exh=48), zero
irraggiungibili-esaustive; GAP gate preregistrato REGGE (R_T med 32 vs matched 24 su A —
ombra in gran parte della REGIONE-cuneo, pool n=31 dichiarato sottile; 12 vs 4 su B, 3×
netto); **il passato reale non legge MAI R_T fino al seme** (13/14 a 4.487 passi; 9/9 a
18.041) — il divario albero-48/dinamica-MAI è l'oggetto di (ii). P2: σ=1 esatto 71/1459
(4,9%); σ≤0.01 = 59 (4,0%) concentrate in |R_T| 16-50 (37,1% della banda, NON nella
minima); celle irraggiungibili a D=22 quasi universali (1.452/1.459) — mai usarle nude
come discriminante.

### B3.33 Diagnostica §107d (v2 — solo enunciati sopravvissuti all'ERRATA)
σ_D NON è predittore marginale utile della ricchezza nera reale (mediane nb/|R_T|
0,30-0,33 su tutte le bande; Spearman 0,0755 su 1459; condizionato per taglia [−0,15,0,09])
— trappola tt. Il gap d'albero R_T-vs-matched NON è uniforme nella classe sigma-low
(48 confronti finiti: 16 > / 25 = / 7 <): è DEI LOCK. Struttura sigma-low: 32/59 open=cap,
13/59 cap=1, 0/59 white_all. Mappa condizionata P(nero | c ∈ R_T): baseline descrittiva;
alle coordinate 2D dei lock (righe giovani cy=1,2) densità 0,19/0,12 (NON il picco
marginale — Simpson, trappola uu). Ricchezza nera mediana sui read-set ~1/3.

### B3.34 Forense last-paint e H-NR (§107e.2/107e.3, post-ERRATA)
Kernel estesi dei lock: 66/67 celle VERGINI + 1 visitata-pari (la cella consumata di §105b,
terza conferma cross-percorso) — esatto sui 67 elementi, NON generalizzabile. First-bad dei
1639 canonici: 50 da-seme; età ultima pittura med 451 passi / max 138.199; gap_ep med 2 /
max 8 [QUANTILE]; n_visite med 1. H-NR: 103.980 eventi di pittura unici non-seme, 55.359
con molteplicità ≥2 (53% degli EVENTI, non degli usi), 37.116 condivisi da record NON
adiacenti nella sequenza canonica (non una distanza geometrica/asintotica) — il riuso è
la norma.

### B3.35 Violazioni-orizzonte profonde fra catene (§99c/§100a) [O — ensemble differenti; voce aggiunta per decisione §108b-B3]
1/230 in catena-1 vs 0/1.223 in catena-2 (p ~ 0,5%): osservazioni su ENSEMBLE
DIFFERENTI — né una contraddizione né una stima di frequenza. I record MISTI di
catena-2 non sono mai stati riscanditi: debito ARCHIVIATO (v. B4.24); la campagna
NON viene riaperta ora (§108b-B3).

---

## STRATO 4 — CRUX APERTI E STRADE FALSIFICATE

### Strade falsificate / no-go (con lettera di trappola)

**B4.1** α1 come pavimento del tasso di morso fresco: ERODE (densità→0, stalli ~lineari)
— non è l'invariante; declassata (§57.8.1). Trappole: survivorship temporale (h/§57.7-b),
controfattuale eterno (i/§57.7-c), reset-hash (g/§57.7-a), apofenia del massimo (§57.7-d).
Corollario: la simulazione non può decidere α1; NON riformulare come liminf-che-decade
(§57.8.4).

**B4.2** Ponte diretto "più debito profondo → più lock": FALSO (§59, anti-correlato);
il modello corretto è a due coordinate (deep = substrato, bite = innesco, §60). Non
riaprire predictor scalari.

**B4.3** [NO-GO-EMPIRICO] Potenziali endpoint-monotoni finiti (Φ_depth, Φ_mass_104/208,
Φ_best22, deficit best/top-3/somma): falsificati con peggioramenti stretti, non solo
pareggi (§67/§68; enunciato lecito in §68.7 — vale per quei proxy e ogni
riparametrizzazione order-preserving; NON dice che nessun potenziale esiste). Lettura
strutturale §68.8: massa/mismatch sono conteggi non orientati (i flip depositano e
ripuliscono). Non morti: Φ con credito/memoria, ordini ben fondati, raggiungibilità.

**B4.4** Φ_compat endpoint = best22_depth riscritto ⇒ già falsificata (§69); monotonia
event-wise ingenua falsificata (§70: 357/600 non-migliora, 259/600 peggiora). Restano:
event-wise amortizzata, ordine parziale, co-raggiungibilità (§70.4, mai promosse).

**B4.5** Via GF(2) shallow: no-go (§74.4) — dipendenze reali (nullità 49) ma troppo deboli
per tagliare i sabotaggi; deficit profondi sample-limited/circolari. door_debt_graph potato
(§72.6/§74.5) sia in coordinate grezze sia come raffinamento automatico.

**B4.6** A0(r,K,D0): FAIL al gate-zero (§75) — non determina T3' a r≤8; niente
classificazione SCC; `unknown` MAI classificato no-entry. Risolto in positivo dal frame
co-moving (§78), che però lascia il cap temporale P = residuo Link 1.

**B4.7** Deficit di consumo: FALSO (§79) — trappola **(n)**: creazioni ≥ distruzioni, pool
cresce, inflow B-T ~4:1; non riaprire bilanci/squilibri di tasso. La leva, se esiste, è la
coda lunga dei ritorni lontani.

**B4.8** Lato-alpha finito-stato: MORTO tre volte — alfabeto pieno (§80, trappola **(o)**),
alfabeto potato (§81, (o) estesa), nucleo-come-manico (§81, trappola **(p)**: la coda porta
~64% della massa). Il taglio nucleo/coda non segmenta per età/vc (§82, trappola **(q)**);
la periodicità di svolta segmenta ma su classi minuscole (§84, trappola **(s)**: delimita
(q), fatto strutturale non leva). Il nucleo non è linguaggio di transito (§83, trappola
**(r)**) né ha antenati periodici noti (§84).

**B4.9** Teorema-finestra universale per (LRRRR)^3: FALSO (§85c — testimone reale: nero
isolato nel bianco cavalca, poi muore in LLLLR al 4° periodo, coerente B-T). Trappola
**(t)**: sopravvissuti solo-assW = campanello di realizzabilità. La falsificazione ha
prodotto il Teorema Halo (B1.3) e poi il Teorema della Scia (B1.1). Trappola **(u)**:
ogni statistica di vicinato ai deep va prima scontata del contributo di scia.

**B4.10** Costanti dell'orologio-record: TRE morte preregistrate — min_ep≤5 (§99),
coda-doppia-vuota / ep>8⇒age≤10P (§100), min_cheb†≤8 (§101, →19); quarta: cluster di fase
"solo 2 porte" (§103, 12 fuori-cluster). Trappola **(qq)**: soglie = quantili con data di
scadenza; min_ep è osservabile della coppia (orbita, orizzonte); enunciati ammessi solo
deduttivi / condizionali-dichiarati / esistenziali; tassi per EPISODI. Trappola **(pp)**
(§99c): il caso degenere escluso in silenzio era il segnale (230 G=0 → 2 violazioni
d'orizzonte reali).

**B4.11** Firma-W0 dei testimoni min_ep alti: UCCISA dalla baseline (§99b); promozione
della fascia a "famiglia della soglia" NEGATA dalla baseline stratificata (§100c: regime a
gradiente, non famiglia). P3 (§101c): FALSIFICATA e riportata come tale.

**B4.12** Modello a moneta delle estensioni d'onset (§102c): UCCISO da §103 (picco-5/
buco-3): l'approccio alla porta è strutturato, non accidentale.

**B4.13** "Filo di rasoio" della scalinata: FALSIFICATO (§105b — colpevoli = pose-record
solo 10%; lo scudo è detrito d'escursione, spesso).

**B4.14** Riduzione di (i) per dominanza-sicura: MORTA (§107c.4.1 — σ=1 esatto è il 4,9%,
non la maggioranza).

**B4.15** "Bit antichi = celle irraggiungibili": in parte ARTEFATTO DEL CAP (§107c.3.1 —
i 12/14 e 5/9 a D=28 scendono a 0 a D=55/48). Trappola **(ss)**: l'irraggiungibilità a cap
è un negativo con data di scadenza; fatti stabili = la TRIPLA (D_geo, d_hit, gap vs
matched) e la traduzione per-cella (B1.13). Trappola **(rr)** (§107b): le foglie di un
albero potato non sono una misura.

**B4.16** σ_D come predittore dinamico: NO (§107d.1) — trappola **(tt)**: la quota
sull'albero non è una probabilità dinamica; gli enunciati d'albero restano deduzioni
("ogni passato valido…"), mai tipicità. "Lock-capable" RITIRATO (§107d.0.5): σ≈0 = assenza
di certificato nero (massa open), nome corretto **sigma-low**.

**B4.17** Conclusioni interpretative v1 di §107d: TUTTE RITIRATE (ERRATA 107d.0) — "lock
nel nucleo denso" (Simpson, trappola **(uu)**), "scudo antico/word-indipendente",
"deposito spazialmente correlato", "zeri strutturali", "alberi quasi-estinti = certificato".
Valore della sessione = i negativi (B3.33); il MECCANISMO dello scudo resta NON
identificato (§107d.4).

**B4.18** H-NR (iniettività pura degli eventi di pittura): UCCISA al primo contatto
(§107e.3, aspettativa di morte preregistrata) — il riuso dello scudo è la norma; muore
ogni prova fondata sul non-riuso STRETTO. Portata (ERRATA 107e.0.3): NON uccide ordini con
riuso controllato/nesting/molteplicità limitata (logicamente aperti, senza candidato
definito); il riuso sui canonici non decide da solo la sottosequenza pericolosa.
**Specifica di ricerca NON promossa** (107e.0): rango sul grafo causale
t ↦ last_W2B(first_bad(t)) con funzione di rango esplicita, monotonia dedotta e
molteplicità controllata PRIMA di ogni calcolo — oggi nessun candidato giustifica una
campagna.

**B4.19** Riduzione a Link 1 in forma "(i) ∧ (ii) su UNA presentazione": LACUNA LOGICA
(ERRATA §107d.0.10) — un fallimento = un episodio, non lock i.o.; e l'OR-kernel corto copre
solo il transiente (OR=0 ⇒ d ≥ onset_germe, che può dare ride ZERO). **Forma sufficiente
corretta (vigente):** #{t : presentazione di classe κ a t ∧ ride(t) = d(t) − onset_germe ≥
L_0} = ∞ (o versione con ingresso permanente) — da cui il kernel esteso §107e (B1.11).

### Crux aperti

**B4.20** **Link 1** (il crux operativo centrale della linea record-side, §108b):
"orbita eterna non-highway ⇒ lock W0-like profondi infinite volte". Stato dopo la metà B: (a) la metà "occorrenza" ai record è collassata su
B-T (§104d: spettro dei tentativi = spettro degli ingressi; ipotesi A per-parola); (b) la
quantità record-side vigente è #{t: classe-κ ∧ ride ≥ L_0} = ∞ (B4.19), con supporto
word-decidibile e verdetto word+griglia (§107e); (c) scala §107a: (i) occorrenza della
classe pericolosa i.o. [misurata 0,2–4%/record; NON dimostrata per l'eterno] ∧ (ii)
fallimento dello scudo [= verginità perpetua delle celle del cuneo, §107c.5; realizzato
2/82k; il divario albero-48/dinamica-MAI è l'oggetto]; (d) piega su γ (§107a.b,
osservazione strutturale): un falsificatore costruibile del bersaglio record-anchored o è
periodico (= controesempio-γ, escluso ≤40) o è α1 stessa. Vie deduttive note per (ii)
tutte chiuse: ledger (n), scalinata (B4.13), solitudine (v, metà A), zona piccola (§97,
metà A). Nessuna misura sul finito decide l'eterno (i).

**B4.21** Bound uniforme del budget P di A1 (§78.6/78.10): l'insieme oltre-budget è vuoto
sul campione (2014 attempt) ma NON dimostrabile-vuoto in eterno — è Link 1 visto dal lato
porta. Trappola (m) dichiarata: impronta spaziale limitata ≠ stato finito (le 44 celle sono
STRISCE, una cella assoluta nuova per periodo).

**B4.22** Ipotesi (A) del Rifornimento/Dicotomia (onset del germe finito per ogni K-parola
presentabile): semi-decidibile, APERTA, con circolarità dichiarata (§98c.1); k* costante
esistenziale non calcolata (C).

**B4.23** Lato-alpha irriducibilmente dinamico (§80.5/§28.2): tre falsificazioni in fila
(deep→W0 §59, deficit §79, alfabeto §80) ⇒ il crux richiede un argomento che attraversi la
dinamica; il vocabolario universale (35,6%, §81-§82) è un vincolo/impronta da rispettare,
non una riduzione. Derivare ×1,9 e massa-nucleo 0% dei p15-rides: aperto (§86.5).

**B4.24** Fronti §106/§107 ereditati e non chiusi: incompatibilità dei due obblighi
(lentezza al record §106 + scudo non-garantito da mantenere) lungo una discesa B-T
infinita (§106c.3); formalizzazione "scudo antico vs Cono §87" (§107c.7.1); F3
calibrazione dinamica preregistrata (§107c.5, join sigma_vocab × griglia — eseguita in
§107d come diagnostica, meccanismo NON identificato); F1 gamba-Cuneo stratificata
(ereditata §107b.8.4, dichiarata non eseguita); debito ARCHIVIATO per decisione
§108b-B3: riscansione dei record MISTI di catena-2 (§100g.2) — registrato, non
riaperto.

**B4.25** Decisione vigente (§107e.4, regola preconcordata §107d.6.5): gate fondante
certificato + ipotesi meccanicistica morta ⇒ **CONSOLIDAMENTO** (questa sessione §108),
nessuna nuova campagna empirica salvo un invariante d'ordine di natura diversa.

---

## DA CHIARIRE → DECISE dal pannello §108 (§108b)

**DC.1** §78.3: statuto della stabilizzazione dell'impronta co-moving. L'addendum la
chiama "certificata (da W0, check finito)" ma la verifica è ai tagli 1040/5200/10400/20000
+ argomento di periodicità-con-drift (§78.2) non formalizzato come lemma per ogni offset.
**DECISO (§108b-B1):** [C], non [T] — i quattro tagli verificano una stabilizzazione
finita; la promozione richiederebbe un lemma formale di periodicità-con-drift valido
per ogni offset e per tutte le 22 fasi; non implica comunque un budget temporale P
uniforme. Applicato in B2.7.

**DC.2** §102f.2/§103d: la mappatura porta-0/porta-24-25 ↔ le 22 porte di §66 (GATE_PHASES
/ E(k)) e la fase-0 di §74 NON è mai stata eseguita ("convenzioni di fase diverse",
dichiarato). **DECISO (§108b-B2):** tre simboli distinti per fase-checklist §61–66,
fase-GF(2) §74 e indice porta/record §102–104; NESSUNA identificazione senza una mappa
esplicita. Applicato nelle convenzioni di testa e nell'header di questo volume.

**DC.3** §100a (tensione a verbale): violazioni-orizzonte profonde 0/1.223 in
catena-2 vs 1/230 in catena-1 (p ~ 0,5%) — fortuna o clusterizzazione word-mediated; i
record MISTI di catena-2 non sono mai stati riscanditi (debito dichiarato §100g.2).
**DECISO (§108b-B3):** [O]+[X] — osservazioni su ensemble differenti, non una
contraddizione né una stima di frequenza (nuova voce B3.35); il mancato rescan dei
misti = debito ARCHIVIATO (B4.24); la campagna non si riapre ora.

**DC.4** §107b.6 (caveat della lente): la convenzione temporale di onset_germe è
AMBIGUA se non dichiarata. **DECISO (§108b-B4):** eliminato "asse assoluto og+101";
convenzione canonica: og_rec (misurato dal record), og_win = K + og_rec (asse della
parola concatenata), tempo assoluto dell'orbita = t_record + og_rec; sempre
ride = d − og_rec. Applicato in B2.17, B1.7 e nelle convenzioni di testa; ogni
strumento futuro la dichiara.

**DC.5** §79.6.3 (debito aperto): i conteggi del ledger scout non risultano mai riprodotti
con alpha1_engine.c e con la delta_r outside-window vera sull'ensemble delle 24 orbite
(il §82 ne riusa la classificazione vc, ma sul proprio simulatore). **DECISO
(§108b-B5):** §79 solo [O]/SCOUT; nessuna promozione e nessuna riproduzione ora.
Applicato in B2.8 e B3.15.

**DC.6** §106d: refuso d'etichetta nel JSON di speed_limit_theorem ("neg (tutte garantite)"
conta record con ALMENO una cella garantita) — dichiarato, non corretto nel file dati.
**DECISO (§108b-B6):** il campo storico resta legacy con etichetta errata; semantica
canonica = "almeno una cella garantita"; non usare il nome storico come evidenza
semantica e non alterare retroattivamente il dato. Applicato in B2.16.

**DC.7** §104d vs §107d.0.10: la riduzione "Link 1 ai record = lim sup [d − onset_germe] ≥
L0" (§104) è stata corretta nei quantificatori dall'ERRATA §107d.0.10 (forma vigente in
B4.19). **DECISO (§108b-B7):** nel consolidamento compare soltanto
#{t: classe-κ(t) ∧ ride(t) ≥ L₀} = ∞; §104d rimane esclusivamente storia dell'errata.
Applicato in B3.28 e nella testa (pilastro 6).

**DC.8** §85.2/§85.3: i "4 sopravvissuti stabili" dell'automa a r=2,3 sono realizzati dal
testimone (nero isolato), ma non è a verbale un censimento che dichiari se TUTTI e 4 i
sopravvissuti sono realizzabili o solo la classe del testimone. **DECISO (§108b-B8):**
affermare soltanto il Teorema Halo e l'esistenza di almeno una classe realizzata dal
testimone; nessuna realizzabilità attribuita separatamente a tutti e quattro.
Applicato in B2.10.

---

## Conteggio voci (§108b)

[T] 15 · [C] 20 · [O] **35** (riconteggio §108b: +1 = B3.35, decisione B3) · [X] 25.
Le 8 DA CHIARIRE: DECISE (sopra).
