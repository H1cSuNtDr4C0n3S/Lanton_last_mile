# ADDENDUM §95 — U2-LONTANO 3: il TRATTO PULITO (chiusura per vitalita' riformulata, riduzione di v2, oracolo pigro)

**Riepilogo in una frase:** il programma §95.2 ("chiusura per vitalita': pend₂=0 ⇒
albero dei prepend finito") e' stato FALSIFICATO in apertura (i nodi puliti di
nere400[0]/[2] hanno sottoalbero INTERO vivo oltre depth 400) ma la sessione ha
trovato l'oggetto giusto al suo posto: il **LEMMA DEL PASSO DI PULIZIA** (ogni
decremento di pend₂ avviene con posa sulla cella chiusa, dentro la palla-2 —
deduttivo, una riga di ledger) e il **TEOREMA DEL TRATTO PULITO** (ogni nodo
pulito appartiene al sottoalbero-a-pend₂=0 del suo ultimo nodo di pulizia m*≤n,
che ha posa in palla; radicabile a w101: pend₂(w101)=6), che RIDUCONO il Ledger
Sporco v2 a un enunciato esaustivamente verificabile per-nodo ("nessun tratto
pulito esce dalla palla") con una **DICOTOMIA deduttiva**: dentro la palla il
tratto pulito e' forzato all-R (⇒ muore ≤3 passi per il Lemma dei Bianchi che
Curvano) — o resta confinato o il primo passo fuori E' GIA' il testimone
clean-far; sugli 8 nodi di pulizia reali noti il tratto e' il SINGOLO nodo
(sottoalbero pulito VUOTO, enumerazione esaustiva, non survivorship) e le cacce
multi-politica non hanno prodotto alcuna uscita; l'**ORACOLO PIGRO** (sovra-
approssimazione di TUTTI i nodi di pulizia possibili) confina deduttivamente
25/40 firme (posa,heading) e lascia **15 firme-exit astratte** = l'inventario
esatto del fronte per §96 (v2 diventa teorema ⟺ le 15 sono irraggiungibili).
Pannello di scettici 3/3 IN SESSIONE (lezione §93/§94 applicata): fatti
riprodotti bit-identici 10/10, esche 6/6 beccate, 1 non-sequitur d'enunciato
riparato (dicotomia al posto della finitezza), assert-order che avrebbe
mascherato una falsificazione corretto, quantificatori di v2 dichiarati.

Strumenti nuovi: `alpha1/u2_far_clean_stretch.py` (+ summary/log),
`alpha1/u2_far_clean_oracle.py` (+ summary).

## 95a. Il programma originale muore in apertura (e muore bene)

La via §94c.2 era: "ogni nodo pend₂=0 ha albero dei prepend sopra di se' FINITO
(evidenza: sottoalberi 17–71 nodi) ⇒ Nascita Vicina ⇒ Muro senza pavimento".
Prima sonda della sessione: FALSA. Sugli 8 nodi puliti dei controesempi §94,
6/8 sottoalberi interi esauriscono a 40 nodi (D=19, r_wall=3), ma
**nere400[0] e nere400[2] sono VIVI oltre depth 400** (r_wall ≥45/≥13, cap
500k). L'evidenza "17–71 nodi" della lente §94 valeva per i testimoni della
macchina, non per tutti. La vitalita' dell'albero INTERO e' l'invariante
sbagliato — come D a §92 (trappola aa): il ramo vivo sopra un nodo pulito puo'
ri-sporcare la palla e vagare, e non danneggia nessuno, perche' una nascita
sporca ha seme in palla ed e' gia' esclusa dall'ipotesi del record.

## 95b. Lemma del Passo di Pulizia e Teorema del Tratto Pulito

**Convenzione bit (fissata a verbale, pannello):** `to_bits` mappa 'R'→1,
'L'→0; bit 1 = R = lettura BIANCA (read=0, svolta forward h+1), bit 0 = L =
lettura NERA. (Una nota di contesto errata "1=L" e' circolata in sessione ed
e' stata sbugiardata da due lenti indipendenti.)

**LEMMA DEL PASSO DI PULIZIA (deduttivo).** Nel camminatore all'indietro il
pending di una cella cambia solo alla cella `cn` del passo (exact_step scrive
solo `req[cn]`, e muore prima di ogni mutazione parziale; il frame anchor non
deriva sotto prepend). pend₂ (pending con cheb≤2) decrementa ⟺ il passo e' R
(read=0) su `cn` pending con cheb(cn)≤2; il decremento e' esattamente 1
(|Δpend₂|≤1 per passo: L-su-pending e' irrealizzabile, §93); la posa dopo il
passo E' `cn`, dentro la palla-2. Di terra: 0 violazioni su 310 cammini (10
controesempi §94 + 300 estensioni casuali; esca palla-1: 2682 violazioni
trovate — il checker sa fallire).

**TEOREMA DEL TRATTO PULITO (riduzione, deduttivo dato il lemma).** Sia n un
nodo con pend₂(n)=0 in un albero dei prepend con radice sporca (pend₂(root)≥1).
pend₂ e' intera, ≥0, si muove di al piu' 1 per passo ⇒ esiste **m\* ≤ n**,
ultimo nodo della catena root→n in cui pend₂ transisce 1→0 (eventualmente
m\*=n), con **posa(m\*) in palla-2** (Lemma del Passo), e pend₂≡0 su tutto il
tratto [m\*, n]: n appartiene al **sottoalbero pulito** di m\* (prepend con
pend₂=0 a ogni nodo intermedio).

**Radicamento a w101 (regalo del pannello, attacco 5):** pend₂(w101) = 6
(celle {(-2,1),(-1,1),(0,1),(0,2),(1,2),(2,1)}, GATE G1b) ⇒ la riduzione vale
per **OGNI passato completo che presenta w101 a un record**, a qualunque
profondita' avvenga la nascita — dentro o sopra qualsiasi coprente, senza
case-split sulla famiglia delle coprenti. (In piu', G1: le 36 fuggenti
distinte — 42 nominali, 6 dup, coerente §94a "34 = 6 vecchie + 28 nuove" —
hanno pend₂(root) ≥ 4.)

**COROLLARIO (riduzione di v2).** Ledger Sporco v2 ("nascita con posa fuori
palla-2 ⇒ pend₂≥1, cioe' ≥1 cella di seme nero in palla") ⟺ **nessun
sottoalbero pulito sopra un nodo di pulizia raggiungibile contiene una posa
fuori palla-2**. Le nascite si dividono cosi': sporca ⇒ seme in palla-2
(esclusa dall'ipotesi del record); pulita ⇒ nel tratto pulito di un m\* con
posa in palla ⇒ (se i tratti sono confinati) origine in palla-2 (esclusa
dall'ipotesi del record: gamba-origine). I 1.376 clean-far astratti di §93f
sono raggiungibili SOLO attraverso un tratto pulito: da fantasmi generici
diventano bersagli con un collo di bottiglia esatto.

## 95c. Dicotomia del Tratto Pulito e certificati esaustivi

**DICOTOMIA (deduttiva; sostituisce l'enunciato ingenuo "sottoalbero pulito
finito", che il pannello ha smontato — fuori palla il tratto potrebbe vagare a
pend₂=0).** Dentro un tratto pulito nessuna cella di palla e' pending, quindi
sulle 10 celle di palla visitabili ({|x|≤2, y∈{1,2}}: valid() esige y≥1 e
(0,0) e' la posa finale mai letta) sono possibili solo **R-su-fresca** — L
aprirebbe pend₂ (esce dal tratto), L-su-pending irrealizzabile, R-su-req=1
irrealizzabile. Quindi il tratto pulito confinato in palla e' un **all-R** e
muore entro 3 passi (Lemma dei Bianchi che Curvano §93: il 4° R tornerebbe
sulla cella di pulizia c\*, che ha req=1). Per ogni nodo di pulizia m\*: **O**
il sottoalbero pulito resta confinato (profondita' ≤3, enumerazione esaurisce
SEMPRE) **O** il primo nodo con posa fuori palla (profondita' ≤4) e' GIA' un
testimone clean-far = falsificazione di v2. L'enumeratore tronca i rami alla
prima posa fuori (foglia-testimone): ogni non-confinamento produce un
TESTIMONE esplicito, mai un rosso generico.

**Certificati (G2, esaustivi — non survivorship):** sugli 8 nodi puliti dei
controesempi §94 (uno per cammino, tutti posa (−1,2); macchina[4]/[5] non
hanno nodi puliti) il sottoalbero pulito e' **VUOTO**: la cella successiva
forzata e' sempre (0,2) con req=1 ⇒ R irrealizzabile, L riaprirebbe pend₂
esattamente su (0,2) — la firma whack-a-mole di colonna 0 (§93d/§94d) vista
dall'altra parte: chi pulisce la palla muore contro la stessa cella che i
fuggitivi lasciano pendente. Il tratto pulito reale osservato e' il singolo
nodo di pulizia: **ogni nascita pulita nota E' un nodo di pulizia, con posa
in palla per il Lemma**. Dettaglio nuovo (lente indipendente): i nodi puliti
di macchina[1]/[3] sono i suffissi lunghi quanto macchina[0]/[2] (2 prepend
sotto la cima); nessun nodo dei 10 cammini e' mai pulito a palla-3 (la scelta
palla-2 non e' vacua).

## 95d. L'oracolo pigro: 25/40 confinate, 15 firme-exit

`u2_far_clean_oracle.py` sovra-approssima **tutti** i nodi di pulizia
possibili con la sola conoscenza necessaria per definizione: posa c\* in palla
(10 celle), heading libero (4), req(c\*)=1 (la pulizia e' R su pending),
pend₂=0 (celle di palla mai req=0), ogni altra cella risolta pigramente
(unknown ≡ FREE per il futuro del tratto: risolvere 0/1 restringe soltanto).
Esito:

- **25/40 firme (posa, heading) CONFINATE deduttivamente** (lo spiral all-R
  muore in palla entro 3 nodi, come da Dicotomia);
- **15 firme-exit astratte** (pose di bordo il cui spiral sbuca fuori palla al
  1°-2° passo prima di morire), inventario esatto nel summary JSON;
- GATE O0: la firma reale (−1,2) h=3 (sx) con la conoscenza reale req((0,2))=1
  muore immediatamente — coerente con gli 8 certificati.

Lettura onesta (trappole z/ff): l'exit astratto NON e' una falsificazione —
la raggiungibilita' astratta non trasferisce. Ma il fronte e' ora FINITO ed
esplicito: **v2 e' teorema ⟺ nessuna delle 15 firme-exit e' realizzabile come
nodo di pulizia di un passato valido**. Le cacce (95e) non ne hanno realizzata
nessuna (tutti i nodi di pulizia reali cadono sulla firma confinata (−1,2)
h=3). Per §96: o vincoli di raggiungibilita' deduttivi per firma (pend-storia
del genitore, scia d'arrivo §86, geometria del passo di pulizia), o cacce di
realizzazione mirate per firma.

## 95e. Cacce multi-politica (G3) e soglie (G4)

Quattro famiglie di politiche sulle 36 fuggenti distinte (P1 milestone-greedy
con cap per-milestone 40k e riparazione; P2 DFS greedy mirata; P3 passeggiate
profonde randomizzate con steering; P4 mutazione dei testimoni: tronca 10–320
bit dai controesempi e ri-esplora), 276 job, 86,3M passi, run 682 s (12 worker
BelowNormal). Esito:

- **23 stati di pulizia distinti certificati** (17 mai visti prima), dedupe
  per stato esatto, ognuno ri-verificato di terra (valid() + exact_state +
  pend₂=[]) e col **sottoalbero pulito enumerato esaustivamente: 23/23 VUOTI,
  0 pose fuori palla**;
- politiche produttive: P1 (3 stati, dai fuggenti del censimento
  census[0]/[2]/[6] — territorio indipendente dai testimoni §94) e P4 (20);
  P2/P3 zero (la pulizia e' un evento raro per cacce cieche: la stessa lente
  §94 servi' 660k nodi mirati per un hit). Nota di metodo: nelle prime due run
  piene P1 aveva prodotto 0 (2 hit negli smoke) — sfortuna dei semi a
  probabilita' ~2%/job; il G4 rosso e' stato trattato alzando i restart P1
  (24) e cambiando seme, MAI la soglia;
- caccia diretta al falsificatore (goal pend₂=0 con posa fuori): **0 hit**;
- **G4 verde**: 23 ≥ 10 stati, 17 ≥ 2 nuovi, 2 politiche produttive.

**Il fatto saliente:** TUTTI i 31 stati di pulizia reali noti (8 §94 + 23
nuovi, origini indipendenti: lente-caccia §94, lente-macchina §94, P1 su
censimento, P4 mutazioni) hanno la **STESSA firma ((−1,2), heading sx)** —
proprio l'unica firma che l'oracolo confina E che il req((0,2))=1 concreto
uccide sul nascere. Nessuna delle 15 firme-exit e' mai stata realizzata.
Verdetto della run: `TRATTO-PULITO-IN-PALLA (sui nodi di pulizia raggiunti —
v2 resta congettura empirica, trappola hh)`.

## 95f. Pannello di scettici (3 lenti, IN SESSIONE — lezione §93/§94 applicata)

Lanciato in parallelo alle run primarie (non a fine sessione: la lente
nascita-vicina era morta due volte per limite di sessione):

- **Lente logica** (attacchi 1–6): Lemma REGGE (exact_step tocca solo cn,
  frame anchor prepend-invariante — il candidato "buco d'orizzonte" alla §91
  non c'e'); Teorema REGGE con correzione m\*≤n; **BUCO d'enunciato trovato e
  riparato**: "cella di palla una volta ⇒ enumerabile esaustivamente" era un
  non-sequitur (fuori palla il tratto potrebbe vagare) — sostituito dalla
  Dicotomia; **assert-order corretto**: l'esaurimento era verificato PRIMA
  delle pose-fuori, una falsificazione reale sarebbe uscita come rosso
  generico nascondendo il testimone; quantificatori di v2 dichiarati
  (certificazione per-nodo-raggiunto, v2 resta congettura empirica);
  case-split del Muro esplicitato e SEMPLIFICATO dal radicamento a w101
  (pend₂(w101)=6, misurato dalla lente); confini palla/y<1/(0,0) REGGONO.
- **Lente macchinario indipendente**: reimplementazione da zero (solo valid()
  + anchor_trace come secondo riscontro): 10/10 cammini bit-identici (nodi
  puliti, pose, pend₂ finali), livello-1 sopra gli 8 puliti: unico prepend
  valido = L che riapre pend₂={(0,2)}, R sempre irrealizzabile — 8/8; esche
  E1/E2/E3 beccate (E3 non vacua: zero puliti a palla-3).
- **Lente esche sul checker principale**: M1 (pota rimossa) beccata su due
  strati (assert interno; poi numeri esplosi: pose_fuori 1749 su nere400[0]);
  M2 (palla a cheb≤4) beccata dai guard di vacuita' (G0/G2 rossi), lemma resta
  verde a ogni raggio (843 decrementi pend₄, 0 violazioni); M3 (bit-flip su
  fuggente) beccata da valid(). Nessuna esca vacua. Nota: 19-vs-40 nodi tra
  enumeratori = convenzione di conteggio (legal_bits filtra a monte,
  wall_exhaustive conta i tentativi morti), non disaccordo dinamico.

Correzioni applicate al codice/enunciati in sessione: dicotomia
nell'enumeratore (foglia-testimone), ordine testimone-prima-di-assert in
G2/G3, m\*≤n, G1b (pend₂(w101)=6), controllo pose dei nodi puliti nei cammini
casuali di G0 (falsificazione gratis), variabile morta rimossa, `== FREE` al
posto di `is FREE`, verdetto con qualificatore esplicito.

## 95g. Trappole nuove

- **(ii) enunciare la dicotomia, non la finitezza — e mai un rosso che
  maschera il testimone** (TRATTO-PULITO §95): un sottoalbero potato puo'
  essere infinito fuori dal dominio della pota; l'enunciato sano e' la
  dicotomia "confinato oppure il primo sconfinamento e' un testimone", e il
  checker deve trattare OGNI non-esaurimento come testimone esplicito di
  falsificazione (riportarlo PRIMA di ogni assert). Un `assert esaurito` che
  scatta prima del check dei testimoni e' fail-safe sul verde ma trasforma
  una falsificazione in un rosso generico non diagnosticabile. Parente di
  (bb)/(cc): il gate deve poter fallire NEL MODO GIUSTO.
- **(jj) la vitalita' dell'albero intero non e' l'invariante — guardare il
  sottoalbero potato dal vincolo** (TRATTO-PULITO §95): "pend₂=0 ⇒ albero
  finito" era falso (2/8 vivi oltre 400), ma era anche la domanda sbagliata:
  i rami che ri-sporcano la palla non producono controesempi. L'oggetto
  giusto e' il sottoalbero POTATO al vincolo violabile (qui pend₂=0), dove la
  pota stessa fornisce la struttura (all-R ⇒ morte ≤3). Parente di (aa)
  (invariante sbagliato) e istanza del metodo: prima di misurare la vitalita'
  di un albero, chiedersi quale sottoalbero conta per l'enunciato.

## 95h. Domande aperte / programma §96

1. **Le 15 firme-exit dell'oracolo** (il fronte esatto di v2): per ciascuna,
   o un vincolo di raggiungibilita' deduttivo (il genitore di m\* ha
   pend₂={c\*}; la scia d'arrivo §86 vincola le celle dietro la posa; la
   geometria del passo di pulizia lega h\* a h_par=(h\*+1)&3 e
   c_par=c\*+D[h_par]) o una caccia di realizzazione mirata per-firma.
   v2 teorema ⟺ 15/15 uccise. Una realizzata ⟺ v2 falsa (e Muro da
   riformulare di nuovo).
2. **Muro senza pavimento (stato)**: con Tratto Pulito + certificati, il
   corno 3b regge su: (sporca ⇒ seme in palla) + (pulita ⇒ m\* in palla +
   confinamento CERTIFICATO sui nodi raggiunti). Il gap residuo e' SOLO la
   quantificazione universale del confinamento = punto 1.
3. Ereditati: censimento 34 fuggenti nuove vs 34 nere-D≥400 (§94f.4);
   retro-nota §91c.3; stress-2 bianche e h1=1 (§92).

## 95i. Inventario file (alpha1/)

- `u2_far_clean_stretch.py` (+`_summary.json`, `.log`) — lemma, teorema,
  dicotomia, gate G0–G4 (G1b radicamento w101), cacce multi-politica P1–P4.
- `u2_far_clean_oracle.py` (+`_summary.json`) — oracolo pigro sulle 40 firme
  (posa,heading), gate O0; inventario delle 15 firme-exit.
