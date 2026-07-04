# ADDENDUM §93 — U2-LONTANO: il ledger dei pending, la Nascita Vicina, il pavimento del ledger

**Riepilogo in una frase:** il ledger dei pending progettato a §92e e' stato costruito e
validato (gate L0–L3 + attacco indipendente del pannello con 3 mutazioni-esca tutte
beccate; riproduzione bit-identica del controesempio §92: 2918 passi, 1326
L-su-rivisitata, pending 60→286) e ha prodotto tre risultati: (1) il **LEMMA DELLA
NASCITA VICINA** — coprente-nera con albero dei prepend FINITO ⇒ ORIGINE entro r_seed
dal record, e con min-pending>0 su tutti i nodi ⇒ anche una cella NERA di SEME entro
r_seed — che certifica **42/42 testimoni noti ad albero finito** (r_seed ≤ 16, classi
D = 0/4/8/12/48/56 di §92) vietati ai record lontani, SENZA alcun bound su D (e' il
sostituto sano del ramo finito della defunta U2-NERO; lemma PER-PAROLA, non di
famiglia); (2) il **PAVIMENTO DEL LEDGER pend₂ ≥ 2**: TEOREMA per enumerazione sui 12
testimoni ad albero finito (min esatto 2/3/3/4, residui espliciti) e congettura
misurata sulle 6 fuggenti (nessuna chiusura della palla-2 trovata: 37k nodi mirati a
R=2, 16,5M a R=3, 12M di sonde sul nucleo, 1,29G totali di campagna; ricerca greedy
NON esaustiva, trappola bb dichiarata), col residuo minimo che NON e' un insieme di
celle bloccate ma un'ostruzione CONGIUNTA (il nucleo {(−1,1),(0,1)} della scia si
chiude anche in coppia, ma il debito riappare in riga 2: whack-a-mole); (3) la macchina
astratta palla-2 (BFS post-copertura da tutte le 47.312 coperture-nere, 3,44M stati,
27 s) NON decide: 1.376 stati puliti-lontani astratti (+3.396 pend₂=0 vicini) —
l'astrazione OUT dimentica i req del footprint fuori striscia (trappola cc) — quindi
sui fuggenti il **TEOREMA DEL LEDGER SPORCO** (pend₂ ≥ 2 ⇒ ≥ 2 celle di seme in
palla-2 ⇒ vietanza) resta il bersaglio di §94: motore C a striscia allargata o
invariante di parita'/flusso.

Strumenti: `alpha1/u2_far_ledger.py`, `u2_far_run.py`, `u2_far_born_near.py`,
`u2_far_closure_hunt.py`, `u2_far_core_block.py`, `u2_far_ball2_machine.py`,
`u2_far_pend2_floor.py` (+ summary JSON e log).

## 93a. Il ledger dei pending: macchinario e gate

Semantica (dal pannello §92, ora meccanizzata e RAFFINATA dal pannello §93): nel
camminatore all'indietro (frame anchor, `exact_step` §92) **pending(c) ⟺ req(c) = 0**
(la prossima visita piu' antica deve leggere bianco ⟺ la prima-lettura-corrente-
nella-parola e' nera). **Ogni L apre il pending di una cella non-pending** (fresca o
rivisitata con req=1); **L su cella gia' pending e' irrealizzabile** (pending ⇒
lettura forzata bianca) — quindi ogni L e' un'apertura NETTA, mai una "riapertura
nello stesso istante" (lente ledger, 65 tentativi forzati, 0 realizzabili). Ogni R su
cella pending chiude; fresh-R neutra. Per una parola-passato **COMPLETA (dalla
nascita)**: pending finali = celle NERE del SEME visitate — e questo e' un TEOREMA,
non solo empiria: i flip avvengono solo alla lettura, quindi la prima lettura di vita
vede il colore del seme (lente ledger).

Gate (tutti verdi, `u2_far_ledger.py`, ~8 s):
- **L0** identita' incrementale req/pending vs ricalcolo da zero (800 estensioni);
- **L1** verita' di terra forward: griglia vuota (onset 9977) ⇒ **0 pending**;
  seme {(7,−7)} (onset 106258) ⇒ pending = **{(7,−7)} esatto**; 10 blob ⇒ pending ==
  seme nero visitato, **uguaglianza esatta 10/10** (bilancio §92e; il qualificatore
  "visitato" e' portante: blob con 44 nere, 35 visitate ⇒ 35 pending);
- **L2** riproduzione **bit-identica** del controesempio §92e: corsa fresco⇒R sul
  testimone infinite-rail: 2918 passi, 1326 L-su-rivisitata, pending 60→286, morte
  y<1;
- **L3** lemma all-R su 4000 parole: morte entro il 5°, morti al 4° tutte sulla coda
  + dicotomia (morte al 4° ⟺ prima lettura della coda bianca).

Attacco del pannello (lente ledger, macchinario riscritto da zero, semi diversi):
L0 su 360 passeggiate fino a 300 prepend, L1 con 29 semi avversari (anelli, linee,
isole, formica che parte su nero), L2 rifatta ex novo + 40 prefissi validati con
`valid()`, L3 ESAUSTIVO su tutte le 2958 parole valide di lunghezza 1–14 + 6000
lunghe. **Tre mutazioni-esca (heading invertito, ledger solo-L-su-fresco, req
invertito) tutte beccate ⇒ gli attacchi possono fallire.** Tutto REGGE.

**LEMMA DEI BIANCHI CHE CURVANO (deduttivo, per ogni parola valida NON vuota):**
i 4 prepend R consecutivi sommano D[h]+D[h−1]+D[h−2]+D[h−3] = 0, quindi il 4° cade
sulla CODA c0 (c1,c2,c3 ≠ c0: somme parziali di versori non nulle). Se la prima
lettura di c0 era bianca (word[0]=R), il 4° R e' irrealizzabile: morte al 4°, sulla
coda. Se era nera (word[0]=L), il 4° R chiude e il 5° cade su c1 = c0−D[h0], gia'
letta bianca al 1° (req=1): morte al 5°. Ai passi 1–3 la corsa puo' morire anche
prima (y<1 O irrealizzabile su cella di parola: 1202/2958 nell'esaustivo del
pannello). **All-R muore entro il 5° sempre.** Corollario: ogni cammino all'indietro
che sopravvive fa ≥ 1 L in ogni finestra di 5 passi, e ogni L apre un pending.
(Caveat §92g.2 intatto: questo NON limita la crescita dei pending.)

## 93b. La corsa inversa forzata sulle coprenti reali

`u2_far_run.py` su **48** coprenti-nere reali (2 jackpot + 5 D12 + 3 D8 + 2 D4 +
6 nere400 + 30 censimento §90c): la corsa deterministica fresco⇒R (zero debiti
nuovi; muore SOLO per y<1 = mai per irrealizzabilita', lente ledger) **muore entro
≤ 64 passi su TUTTE** (0 passi sulle D=0, 4–12 sulle confinate, 48–64 su
jackpot/nere400), non esce mai nemmeno dalla palla R=8, e chiude quasi nulla
(pend_fine ≈ pend0 = 37–74). Contrasto: la stessa corsa sopra fuga+coprente del
testimone §92 durava 2918 passi — la fuga era comprata con L-su-fresco.
**Corollario:** ogni passato reale sopra una coprente-nera devia dalla corsa a costo
zero con una L-su-fresco (= +1 pending) entro ≤ 64 passi dalla copertura.

## 93c. LEMMA DELLA NASCITA VICINA

**Lemma (per-parola, due gambe).** Sia e2+w101 una coprente-nera il cui albero dei
prepend e' FINITO (enumerazione esaustiva senza cap: profondita' D_true, celle del
muro cheb ≤ r_wall; r_seed = max(r_foot(parola), r_wall)). Allora per ogni passato
completo che la presenta a un record y-min stretto:
- **gamba 1 (origine):** la nascita e' entro D_true passi sopra la copertura — in
  QUALSIASI nodo dell'albero, non solo alle foglie — e la posa di nascita e' una
  cella del muro o della parola ⇒ **ORIGINE entro r_seed dal record** (nessuna
  ipotesi di pending);
- **gamba 2 (seme):** se in piu' min su TUTTI I NODI di #pending > 0, i pending
  finali sono ≠ ∅ e tutti dentro footprint(parola) ∪ celle-del-muro ⇒ **una cella
  NERA di SEME entro r_seed dal record**.
⇒ coprente VIETATA a ogni record y-min stretto con palla-(r_seed) priva di seme e
di origine. Nessun bound su D richiesto; vale per ogni orbita (eterna o no).

`u2_far_born_near.py`: **42/42 testimoni noti ad albero finito CERTIFICATI**
(r_seed ≤ 16, la maggior parte ≤ 9; min_pend sui nodi 35–74; D_true riproduce
esattamente la scala §92: 0/4/8/12/48/56; il codice BOCCIA il certificato se
min_pend = 0). Cross-validazione di terra (`--cross-validate`): TUTTI gli alberi
rienumerati con solo `valid()`, D e min_pend bit-identici (la lente enunciati ha
rienumerato indipendentemente i 12 testimoni: nodi bit-identici).
**Scope onesto:** il lemma e' PER-PAROLA; i "42" sono i testimoni noti (48 −
6 fuggenti), non le 43.726 nere / 43 config del censimento §92 — il censimento
born_near sulla famiglia intera e' lavoro §94 (alberi 10–116 nodi, costo minuscolo).
Le 6 nere400 sono "fuggenti" (albero oltre i cap: corridoi sottili, ~1100 nodi
tentati a prof. 300) e restano il campo di battaglia.

Due buchi trovati e riparati DURANTE la costruzione (trappola ee): la v1 usava il
conteggio (pend0 − D > 0) e le sole foglie — FALSO in generale (jackpot: pend0 = 52,
D = 56, ma min vero sui nodi 50/46 per enumerazione) — e r_pend al posto di r_foot
(l'estensione puo' riaprire pending su celle di parola fuori da pend0).

## 93d. Il pavimento del ledger: teorema sui finiti, congettura sui fuggenti

Bersaglio dell'attacco (falsificazione): un'estensione che chiuda TUTTI i pending
della palla-R e nasca fuori (= testimone che uccide la forma-palla al raggio R:
troncando li' la storia, seme = prime-letture-nere tutte fuori palla, nascita fuori,
record y-min stretto garantito da `valid()`). **Monotonia: successo a R' ≥ R ⇒
successo a R** ⇒ falsificare a R piccolo e' l'attacco piu' forte, e l'impossibilita'
a R = 2 si eredita a ogni R ≥ 2.

**TEOREMA (per enumerazione, `u2_far_pend2_floor.py`):** sui 12 testimoni ad albero
finito, il minimo di pend₂ su TUTTI i nodi (= ogni possibile nascita) e' **2**
(jackpot, residuo {(−1,1),(0,1)}), **3** (D12, residuo {(−2,1),(1,2),(2,2)}; D8,
{(−2,1),(−2,2),(2,2)}), **4** (D4) ⇒ ogni loro passato completo lascia ≥ 2 celle
nere di seme a cheb ≤ 2 dal record: vietate ai record con palla-2 senza seme (caso
finito del Teorema del Ledger Sporco; gli alberi sono corridoi quasi unici:
nodi validi = D+1).

**Congettura misurata (le 6 fuggenti):** `u2_far_closure_hunt.py` (DFS-milestone con
riparazione, steering, politiche randomizzate, 12 worker BelowNormal): **nessun
testimone di chiusura, a nessun raggio**. Contabilita' onesta per raggio (lente
enunciati): R=2 → floor **2** con 37.151 nodi mirati; R=3 → floor 2 con 16,5M;
R=4 → floor 7 con 19,4M; R=8 → floor 33 con 388M; R=12/16 → floor 43 con 432M+432M
(ai raggi grandi il floor misura pend_R, non pend₂); sonde sul nucleo ~12M; totale
campagna 1,29G nodi. **La ricerca e' greedy NON esaustiva (survivorship possibile,
trappola bb auto-applicata): il gate puo' fallire (witness-slot vuoto) e i 1.376
stati puliti astratti della macchina (93f) sono i falsificatori candidati.**
CONGETTURA DEL PAVIMENTO DEL LEDGER: per ogni estensione all'indietro valida di ogni
coprente-nera+w101, pend₂ ≥ 2. Se vera ⇒ TEOREMA DEL LEDGER SPORCO: ≥ 2 celle di
seme in palla-2 ⇒ il Muro si richiude al raggio 2 + intorno, senza alcun bound su D.

## 93e. Il nucleo {(−1,1),(0,1)} e l'ostruzione congiunta

A R=2 il residuo al minimo e' SEMPRE la coppia {(−1,1),(0,1)} (la scia d'arrivo di
w101, §86: prima lettura nera su entrambe) per tutti gli 8 fuggenti+jackpot. Sonda
mirata (`u2_far_core_block.py`):
- **(−1,1) si rivisita facile** (prof. 48–64, dentro il box B=6);
- **(0,1) si rivisita** ma solo con escursioni lunghe (prof. 215–5731, quasi tutte
  oltre il box B=8); **sui jackpot MAI: alberi finiti esauriti ⇒ (0,1) e' bloccata
  PER ENUMERAZIONE** su quelle due parole;
- la **chiusura CONGIUNTA della coppia esiste su 6/6 nere400** (prof. 240–4036) —
  ma negli stati a nucleo-chiuso il debito e' RIAPPARSO in riga 2: pend₂ al goal =
  {(−2,2),(0,2)} (+ (2,2) in 4 casi su 6); a R=3 il residuo minimo tocca anche la
  riga 3 ({(−1,2),(2,3)} su nere400[5]). Pavimento realizzato da sottoinsiemi
  DIVERSI: whack-a-mole tra le righe;
- box-esaustivi: a B=6/8 il sottoalbero in-box e' ESAURITO ma con uscite (2–5439):
  NESSUN certificato alla-Blocco-Antico ne segue; a B=10 esplode (cap 50M, ~1,3–2,1M
  uscite: trappola cc viva).

⇒ sulle fuggenti l'ostruzione NON e' il blocco di una cella (trappola dd): e'
CONGIUNTA — chiudere il nucleo costringe a riaprire la riga 2. Firma da invariante
di parita'/flusso sul bordo della palla, non da irraggiungibilita'.

## 93f. La macchina palla-2: sound ma cieca

La palla-2 (10 celle) sta tutta in S_CORE ⇒ i pending sono leggibili dallo stato
astratto §92. `u2_far_ball2_machine.py`: BFS post-copertura da TUTTE le 47.312
coperture-nere astratte (transizioni esatte-in-S + OUT col vincolo cella-giovane; il
lemma di sovra-approssimazione §92a si applica anche post-copertura, e la
decomposizione del corno 3 e' esaustiva: copertura = ULTIMA visita forward a (1,1),
pre-copertura = fase 1, (1,1) mai visitata = seme = corno 1). Gate B0–B3 verdi
(fase 1 riprodotta stato-per-stato; 8/8 testimoni reali in cov_n; ledger palla-2
astratto == reale; pend₂ = 0 raggiunto astrattamente ⇒ il non-teorema non e'
poverta' di raggiungibilita'). Esito: 3.436.966 stati; **1.376 stati puliti-LONTANI
(pend₂ = 0 e posa fuori palla) + 3.396 pend₂ = 0 vicini** ⇒ **nessun teorema**
(trappola c: solo la morte si trasferisce; i puliti-lontani sono i FANTASMI
candidati da uccidere o realizzare). L'astrazione OUT (rientro libero) dimentica i
req del footprint di w101 FUORI da S_CORE — gli stessi round-trip che a §92
scramblavano le parita' qui fabbricano pulizie che il reale (mai < 2) non sa fare.
Il contrasto astratto-pulisce-subito / reale-mai-sotto-2 LOCALIZZA l'ostruzione nel
campo fuori striscia.

## 93g. Trappole nuove

- **(dd) il residuo-al-minimo non e' IN GENERALE un insieme di celle bloccate:** se
  una caccia si ferma sempre sulle stesse celle residue, NON dedurre che siano
  irraggiungibili — l'ostruzione puo' essere congiunta (qui: sulle fuggenti il
  nucleo di riga 1 si chiude perfino in coppia e il debito sguscia in riga 2; ma sui
  jackpot (0,1) E' bloccata per enumerazione: i due casi coesistono nella stessa
  famiglia). Antidoto (ESEGUITO, `u2_far_core_block.py`): sonda mirata per-cella e
  per-coppia col goal esplicito, PRIMA di enunciare blocchi.
- **(ee) "albero finito ⇒ seme vicino" richiede il minimo su TUTTI i nodi:** la
  nascita e' in QUALSIASI nodo dell'enumerazione (il passato FINISCE, non muore), e
  il conteggio pend0 − D > 0 NON basta (jackpot: 52 − 56 < 0, ma min vero 46–50).
  Parente di (w): il quantificatore giusto e' "per ogni troncamento".
- **(ff) la macchina-palla con OUT astratto non decide il ledger:** l'astrazione che
  a §92 non potava la sopravvivenza qui non pota la pulizia — stessa radice
  (trappola cc), nuovo sintomo (stati puliti fantasma). Non riprovare con strisce
  piccole esatte + OUT libero: servono i req fuori striscia (motore C, trappola g) o
  un invariante che sopravviva allo scramble.

## 93h. Domande aperte / programma §94

1. **Completare il pannello:** 3 lenti su 5 (nascita-vicina, caccia, macchina)
   uccise dal limite di sessione — da rieseguire; le riparazioni delle 2 complete
   sono gia' incorporate; la lente nascita-vicina era stata pre-empita in parte
   (cross-validazione `valid()`, fix any-node, r_foot).
2. **Pavimento del ledger sulle fuggenti (il bersaglio):** dimostrare pend₂ ≥ 2 (o
   anche solo ≥ 1). Vie: (a) motore C con striscia allargata (S_CORE ∪ righe 3–4,
   hash a dimensione fissa, trappola g); (b) invariante di parita'/flusso sul bordo
   della palla (il whack-a-mole riga1↔riga2↔riga3 e' la firma); (c) automa dei
   prepend (§88) ristretto alla palla.
3. **Censimento born_near sulla famiglia:** dalle 48 parole-testimone alle 43 config
   / 43.726 nere di §92 (alberi minuscoli, costo basso); e rigenerare le 34
   nere-D≥400 (6 salvate) per classificare i corridoi di fuga.
4. **Retro-nota su §91c.3:** l'incollaggio del corno 3 via "D ≤ 4 ⇒ Cheb ≤ ~5" e'
   morto (§92); dopo §93 il corno 3 si SPEZZA in: (3a) alberi finiti ⇒ Nascita
   Vicina (l'intorno del Muro cresce da ~5 a r_seed ≤ 16 + bbox seme); (3b)
   fuggenti ⇒ Teorema del Ledger Sporco al raggio 2 (aperto, congettura misurata).
5. Ereditati da §92: stress-2 bianche ("burden1=0 ⇒ D≤12" contro il vergine);
   h1=1 mai realizzata (0/43.726).

## 93i. Pannello di scettici (parziale: 2 lenti su 5)

Pannello multi-agente a 5 lenti; **2 complete** (ledger, enunciati — 60+ tool call,
attacchi meccanici con macchinario indipendente), **3 uccise dal limite di sessione**
(nascita-vicina, caccia, macchina-palla2) — DEBITO dichiarato, punto 1 di §93h.
Esiti delle complete:
- **lente ledger:** L0/L1/L2 REGGONO (reimplementazione indipendente, 360
  passeggiate prof. 300, 29 semi avversari, L2 bit-identico); L1 promosso a
  TEOREMA (prima lettura di vita = colore del seme); L3 IMPRECISIONE riparata
  (casistica passi 1–3 completata con l'irrealizzabilita': 1202/2958; dominio
  ristretto a parole non vuote; dicotomia word[0] aggiunta al gate). Scoperta:
  **L su pending e' irrealizzabile** ⇒ ogni L e' apertura netta. 3 mutazioni-esca
  beccate ⇒ attacchi non vacui.
- **lente enunciati:** E1/E2 REGGONO; E3 IMPRECISIONE (per-parola, non di classe;
  due gambe origine/seme esplicitate) — riparata in 93c; E4 BUCO contabile
  (l'evidenza pend₂ diretta era 37k nodi a R=2 + 12M di sonde, non "430M") —
  riparato in 93d con la contabilita' per-raggio, lo split teorema-sui-finiti /
  congettura-sui-fuggenti, e la promozione del calcolo esaustivo a script
  (`u2_far_pend2_floor.py`, verdetti 2/3/3/4 bit-identici al calcolo della lente);
  E5/E6 IMPRECISIONI di precisione (3.396 vicini citati; dd scopata coi jackpot) —
  riparate in 93f/93g.

## 93j. Inventario file (alpha1/)

- `u2_far_ledger.py` (+`_summary.json`) — ledger dei pending, gate L0–L3, corsa
  forzata (`forced_run`), lemma all-R (`allr_run`, deduttivo + dicotomia). Run ~8 s.
- `u2_far_run.py` (+`_summary.json`) — corsa forzata sulle 48 coprenti-nere reali,
  palle R=8..32. Run < 1 s.
- `u2_far_born_near.py` (+`_summary.json`) — Lemma della Nascita Vicina: 42/42
  alberi finiti certificati, cross-validazione `valid()` (`--cross-validate`).
- `u2_far_pend2_floor.py` (+`_summary.json`) — TEOREMA del pavimento pend₂ sui 12
  testimoni finiti (min 2/3/3/4, residui espliciti), gate su D vs born_near.
- `u2_far_closure_hunt.py` (+`_summary.json`, `_summary_smallR.json`, `.log`) —
  caccia DFS-milestone alla chiusura del ledger, multi-processo, `--tag` per run
  parallele. Campagne: 610 s (R=8/12/16) + 86 s (R=2/3/4). Nessun testimone.
- `u2_far_core_block.py` (+`_summary.json`) — sonda mirata sul nucleo
  {(−1,1),(0,1)}: rivisite, chiusura congiunta, box-esaustivi. Run 533 s.
- `u2_far_ball2_machine.py` (+`_summary.json`) — macchina astratta del ledger in
  palla-2, BFS post-copertura, gate B0–B3. Run 27 s.
