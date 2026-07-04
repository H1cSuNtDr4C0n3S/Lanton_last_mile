# ADDENDUM §92 — U2-NERO FALSIFICATA (D = ∞ certificato), il bilancio dei neri freschi

**Riepilogo in una frase:** il certificato esatto-in-striscia progettato a §91b è stato
costruito e validato (6 gate meccanici, replay bit-identico dei 60 muri §90c), ma ha
FALSIFICATO il suo bersaglio invece di dimostrarlo: "coprente-nera ⇒ D ≤ 4" era un
artefatto di campionamento (scala reale D = 0/4/8/12/48/56, e 34 coprenti-nere fuggono
in territorio vergine con **D = ∞ certificato** via Lemma del Raggio Monotono — cade la
forma word-level "ogni coprente muore entro D limitato", uniforme E per-parola); la
lezione strutturale è che la vitalità all'indietro D è **l'invariante sbagliato** per la
vietanza — il raggio LR paga 1 **nero fresco = cella di seme** ogni 2 passi (ma il tasso
non è universale: la discesa in autostrada è una rotaia infinita a costo totale O(1)),
quindi l'invariante esatto è il **bilancio**: #prime-visite-della-vita-che-leggono-nero
≤ |seme_nero|, senza tasso; fuori dal supporto del seme una prima-visita-della-VITA
legge bianco (R forzato) e il muro diventa una **corsa inversa quasi-deterministica con
contabilità dei pending**: il Muro dietro l'Uno va richiuso su questo oggetto (§93,
"U2-LONTANO"), non su D. Riapre SOLO il corno 3: U1/ramo bianco (§91a, replay senza
vitalità) e corno 1 restano intatti. Addendum RIPARATO dal pannello di scettici (4
lenti: G4 vacuo rifatto con soglie, ledger dei pending, controesempio
discesa-in-autostrada, retro-nota su §88, enunciati precisati).

Strumenti: `alpha1/u2_pocket_certificate.py` (macchina + 6 gate + profilo + testimoni),
`alpha1/u2_infinite_rail.py` (teorema D = ∞), `alpha1/u2_cover_witnesses.json`
(testimoni riproducibili), + summary JSON e log.

## 92a. La macchina esatta-in-striscia (costruita come da progetto §91b)

Camminatore all'indietro in frame anchor; parole = ext+w101. Fatti meccanici, tutti
verificati contro `valid()`/`tail_cell` su migliaia di parole casuali (GATE 0):

- prepend del bit b: nuova cella `c' = c − D[h]`, **indipendente dal bit**; il bit
  determina solo colore letto (R=bianco, L=nero) e heading (`R → h−1, L → h+1`);
- requisiti a 3 stati per cella (libera / prossima-lettura-W / prossima-lettura-B),
  `req(c) = flip(prima-lettura corrente)`, aggiornato a `flip(letto)` dopo la visita;
- validità = realizzabilità (req) + record-compat (ogni cella a y ≥ 1) — la nozione
  DEBOLE giusta per i muri (nessun onset richiesto).

FASE 1: fixpoint di raggiungibilità dalla coda di w101, esatto dentro la striscia
CORE (le 15 celle della tasca §91b + (1,1)), astrazione OUT fuori (rientro libero con
regola della cella-giovane). Prima visita a (1,1) = copertura (bit R = NERA).
FASE 2: muro post-copertura esatto-in-striscia; uscita = sopravvivenza concessa.

**Gate (tutti verdi, `u2_pocket_certificate.py`):** G0 formula del passo (1500 parole
× 2 bit); G1 lemma del suffisso (42.697 suffissi: ogni suffisso di parola valida è
valido — serve alla colla del Muro); G2 replay dei 60 coprenti §90c con muri
bit-identici (simulatore esatto == `valid()` == JSON §91); G3 membership 60/60 delle
coperture reali nel raggiungibile; G4 estensioni casuali LUNGHE (≤320 passi, steering
sul bordo): 264.854 stati ammessi, 4.427 rientri OUT→IN, 644 coperture nei cover-set,
con SOGLIE minime asserite (≥500 rientri, ≥50 coperture) — **riparato dal pannello**:
la v1 (≤39 passi) non toccava mai la striscia ed era vacua (BUCO); lo stress del
pannello (10.000 camminate ×400 passi: ~979k prefissi, 6.615 rientri, 1.499 coperture,
0 respinte) e il G4 rifatto la sostengono ora davvero; G5 testimoni (sotto) riprodotti
esattamente, con flag di confinamento esplicito.

**Lemma di sovra-approssimazione (promosso a deduttivo dal pannello):** ogni transizione
reale soddisfa le condizioni di `in_succ`/`out_succ` — la regola della cella-giovane è
NECESSARIA (la cella del passo più recente è un passo del cammino: fuori S e a y≥1) —
e `req|S` è congelato durante il vagabondaggio fuori striscia (le visite esterne non
toccano celle di S). Quindi la fase 1 ammette OGNI estensione valida, per costruzione
e non solo empiricamente.

Numeri della macchina: 1.198.136 stati raggiungibili; 47.312 coperture-nere astratte
(h1 ∈ {0,1,2}); 28.910 muoiono in-striscia (D astratto max **33**, scala a passi ~4 =
giri della tasca che bruciano parità), **18.402 fuggono** (riga 3 e fianchi).

## 92b. Fatti certificati che restano in piedi

- **T1 (h1=2 ⇒ D=0), geometria pura:** il primo prepend sopra la copertura cade su
  (1,0), y=0, per entrambi i bit. Nessuna ipotesi di campo.
- **T2 (zero cicli in-tasca):** nessuna delle 47.312 coperture astratte sopravvive
  DENTRO la striscia (0 cicli su tutto il memo di fase 2): sopravvivere = uscirne.
- **T3 (bound condizionale):** ogni muro reale le cui CELLE restano tutte in S_CORE
  ha D ≤ 33 (max tra le 28.910 coperture astratte morenti; poggia sul lemma di
  sovra-approssimazione deduttivo di 92a; i testimoni confinati D=4/8/12 hanno
  verdetto astratto ESATTAMENTE 4/8/12). NB pannello: confinamento = celle del muro
  in S_CORE, NON "riga ≤ 2" — (3,2) e (−5,2) hanno y=2 ma stanno fuori striscia;
  il flag esplicito è nei testimoni di G5.
- **T4 (corridoio, h1=0):** req(2,1)=B alla copertura è FORZATO (il bit L del passo di
  corridoio manderebbe la cella-giovane a (2,0), y=0) — e il passo successivo del
  corridoio sta su (2,2).

## 92c. La FALSIFICAZIONE: la scala dei muri e la fuga reale

Campagna parallela (12 worker bf/steer/deep + 8 worker stress-2 jackseed/deepscr,
Ryzen, BelowNormal): 87.453 coprenti raccolte, 43.726 nere, 74.447 parole distinte,
43 configurazioni di copertura distinte (il censimento §90c ne aveva viste **2**).

- **Scala reale dei muri nere:** D = 0 (×23.406) / 4 (×11.340) / 8 (×2.358) /
  12 (×117) / 48 / 56 — il "D ≤ 4" di §90c era survivorship della porta più vicina
  (best-first puro = coprenti corte = configurazioni minime; parente di (h) e del
  plateau-beam §87e-bis). D cresce con quante parità della tasca la e′ rimescola.
- **Una configurazione-FUGA è realizzata** (verdetto astratto: esce a (2,3)): i due
  testimoni D=48/56 serpeggiano nel footprint di w101 fino alla **riga 6 (su 7)**,
  vengono instradati dal campo e muoiono sul muro dei record a (−5,1) — catene
  forzate quasi pure (una sola biforcazione).
- **Stress-2:** 34 coprenti-nere con muro a **D ≥ 400** (cap) e riga massima 13–33:
  ben oltre il tetto del footprint, in territorio vergine. h1=1 mai realizzata
  (0/43.726) pur essendo astrattamente ammissibile — candidato a ostruzione di
  corridoio dimostrabile (§93, punto 4).
- **Ritrattazione (pannello):** cade anche la GEOMETRIA DELLA TASCA di §91b ("15
  celle su due sole righe... un vicolo, non un territorio") e il framing §91c.2
  ("finito-flavored, tasca minuscola"): descrivevano solo i 60 muri best-first
  §90c, lo stesso campione distorto. La continuazione reale sale a riga 6–33 e
  oltre (raggio illimitato). La striscia CORE resta utile solo come dominio esatto
  della macchina, non come confinamento.

## 92d. TEOREMA (testimone): esiste una coprente-nera con D = ∞

**Lemma del Raggio Monotono.** Sia W valida con coda in posa (c0, h=0). Il raggio
(L,R)^m prepende la scala c0+(0,1), poi (−1,0), … : a coppie y cresce di 1 e x cala
di 1 ⇒ celle tutte distinte, y ≥ 1 sempre. Se ogni cella del raggio oltre la coppia
m0 ha y > y_max(footprint(W) ∪ raggio≤m0) e `valid(r_m + W)` per ogni m ≤ m0+Δ
(check finito), allora `valid(r_m + W)` per OGNI m: ogni passo ulteriore visita una
cella mai vista (prima lettura libera) e resta a y ≥ 1. QED.

`u2_infinite_rail.py`: testimone = coprente-nera prof. 233 (una delle 34); fuga di 66
prepend fino a posa (−18,12) h=0 (validità lettera-per-lettera); raggio interamente
fresco, m0=1, verificato per 41 coppie + monotonia meccanica su 500 coppie oltre m0.
**⇒ sup D = ∞ sulle coprenti-nere: U2-NERO è FALSA nella forma word-level di
§90c/§91b ("ogni coprente muore all'indietro entro D limitato"), sia uniforme sia
per-parola.** Precisazione del pannello: sopravvivono le forme condizionali T1/T3
(che sono ipotesi diverse), e sopravvive — APERTA — la lettura quantificata sui
passati REALI di orbite eterne ai record lontani dal seme, che il testimone NON
falsifica (ogni L del raggio è fresca-nella-parola: in un passato reale lontano dal
seme andrebbe onorata come debito o cella di seme): quella lettura È U2-LONTANO (92e).

Il corno 3 del Muro dietro l'Uno NON si chiude via vitalità (§90d/§91c da rivedere
su questo punto). **Riapre SOLO il corno 3:** U1/ramo bianco (§91a) è puro replay
V†, dichiara esplicitamente di non usare alcun bound di vitalità, e il pannello lo
ha ri-attaccato con 12 coprenti-bianche avversarie fresche mai viste dai gate §91
(8 sorelle-flip delle nere-fuggenti + 4 da scramble profondo, prof. fino a 537):
12/12 burden1=0, onset 160 — U1 regge; il corno 1 (seme) è intatto per definizione.
Dato astratto da registrare (era solo nel JSON): fase-2 BIANCA = 16.388 fuggenti,
30.924 morenti con D confinato max 25.

## 92e. La lezione strutturale: il bilancio dei neri freschi

Il raggio LR consuma **esattamente 1 nero fresco ogni 2 passi** (misurato: min=max=1
per coppia su 50 coppie); nel testimone i 52 neri freschi sono 41 dal raggio + 11
dalla fuga (66 passi), e coprente+w101 ne portano altri 46 INTERNI alla tasca (come
passato completo il testimone non è mai un record lontano dal seme, già prima del
raggio). Per una parola-passato di un'orbita REALE, una cella fresca-nel-passato-INTERO
è la prima visita della VITA: il suo colore è quello del **seme**. Quindi:

- ogni prolungamento all'indietro eterno o lunghissimo che passa dal vergine paga
  neri freschi = celle di seme: per un seme finito, il numero di prime-visite-della-vita
  che leggono nero lungo l'INTERO passato è ≤ |seme_nero|;
- **fuori dal supporto del seme (basta questo: non serve "lontano"), una
  prima-visita-della-vita legge bianco ⇒ R.** Nella ricostruzione all'indietro pero'
  "fresco-nella-parola" ≠ "fresco-nella-vita": una L su cella fresca-nella-parola
  resta lecita come **DEBITO** — impegna una visita ancora piu' antica (o un nero di
  seme, escluso nella palla lontana). **Ledger corretto (BUCO del pannello): il
  debito e' uno stato della cella, non un evento** — `pending(c)` ⟺ la
  prima-lettura-corrente-nella-parola di c e' nera (req(c)=W); OGNI L (fresca o
  rivisitata) apre/riapre il pending, ogni R su cella pending lo chiude; bilancio =
  #pending a fine corsa. Controesempio che uccide il ledger ingenuo "solo
  L-su-fresco": sopra fuga+coprente+w101 del testimone, la corsa con zero L-su-fresco
  e' deterministica (0 biforcazioni), sopravvive 2.918 passi (y fino a 25) con 1.326
  L-su-rivisitata e porta i pending da 60 a 286 (+226 celle di seme richieste, 1 ogni
  ~13 passi);
- **il tasso NON e' universale (BUCO del pannello):** il raggio LR paga 1/2, la corsa
  senza-L-su-fresco ~1/13, e la **DISCESA IN AUTOSTRADA** (finestre cicliche di W0,
  fasi finali 14/28/61/71) e' valida+record-compatibile per OGNI lunghezza testata
  (1..831 lettere, 2..32 periodi) con neri freschi TOTALI COSTANTI (13/14/19), tutti
  all'estremo antico: e' il glider eterno dalla nascita, |seme|=13, con record y-min
  stretti arbitrariamente lontani dal seme. **L'invariante esatto e' il bilancio
  senza tasso** (#prime-letture-vita-nere ≤ |seme_nero|, verificato con uguaglianza
  su 12 orbite simulate): da solo NON da' la vietanza — la vietanza dovra' poggiare
  sulla parte w101-specifica (i pending in-palla di coprente+w101 e della corsa);
- la vacuita' del testimone D=∞ ai record lontani vale nella lettura passato-completo
  (banalmente: 46 neri freschi in-tasca) ed e' APERTA nella lettura a suffisso (i
  neri del raggio potrebbero essere debiti pagati da un passato ancora piu' antico):
  questa apertura COINCIDE con U2-LONTANO. D resta comunque l'invariante sbagliato —
  stessa struttura della trappola (w): un'altra risorsa-non-limitata travestita
  (parente del pavimento-del-morso §57 e del deficit §79: la risorsa e' il vergine);
- **retro-nota su §88 (pannello):** la rotaia certificata σ^m·τ·w101 paga 5 neri
  freschi per blocco σ (misurato, lineare esatto fino a m=52: 93→353) — PIU' del
  raggio LR. Quindi D(w101)=∞ resta teorema ma NON e' piu' un certificato di
  presentabilita' di w101 ai record lontani dal seme; il Teorema della Parola Viva
  (condizionale: SE w101 al record allora (1,1) nera) e' intatto, ma l'etichetta
  "non-vacuo" di §88 va riletta: la non-vacuita' ai record lontani e' ora essa
  stessa parte della congettura del Muro (e va bene cosi': il Muro vuole proprio
  dimostrare che w101 NON si presenta ai record lontani).

**Riformulazione del Muro (bersaglio §93 — "U2-LONTANO"):** a un record y-min stretto
con suffisso w101 e palla-R priva di seme, il passato COMPLETO sopra la coprente deve
(i) chiudere TUTTI i pending in-palla (ledger corretto: ogni cella con prima-lettura-
corrente nera va coperta da una visita ancora piu' antica che legga bianco, o esce
dalla palla), e (ii) terminare alla nascita. Se si certifica che nessuna corsa con
contabilita' dei pending chiude i conti restando in-palla (la palla e' finita e ogni
pagamento allunga il passato in-palla e apre nuovi vincoli), la copertura di (1,1)
avviene vicino al seme/nascita ⇒ vietanza ai record lontani, SENZA alcun bound su D.
Attenzione (pannello): la discesa-in-autostrada mostra che il bilancio GENERICO non
basta — il certificato deve usare la parte w101-specifica (i pending che coprente+w101
lasciano in-palla e come la corsa li muove). Branching residuo: i debiti/pending e i
rivisitati-di-e′ fuori striscia; resta da vincolare la fase 1.

## 92f. Trappole nuove

- **(aa) la vitalità all'indietro D è una risorsa di seme travestita** (parente di
  (n)/(w) e del pavimento-del-morso §57): ogni parola con accesso al territorio
  vergine ha D = ∞ (raggio monotono, 1 nero fresco/2 passi; la rotaia σ di §88 paga
  5/8; la discesa in autostrada paga O(1) TOTALE). Enunciati "D ≤ costante" su
  famiglie di parole vanno attaccati con la fuga verso il vergine E con la discesa
  in autostrada prima di essere creduti; D = ∞ a sua volta NON certifica
  presentabilità ai record lontani. L'invariante sano per orbite reali è il bilancio
  dei pending/neri freschi (senza tasso!): prima-visita-della-vita fuori dal seme =
  bianca = R forzato.
- **(bb) i campioni best-first di estensioni sottostimano le code** (è la (h) sul
  piano delle estensioni): §90c vedeva 2 configurazioni e D ≤ 4; il vero sup era ∞.
  Le cacce guidate dalla distanza trovano le porte più vicine, non le più ricche;
  per falsificare servono passeggiate casuali profonde e steering sulle
  configurazioni (qui: 43 config, jackpot al 20° tipo).
- **(cc) istanza striscia-stretta di (c)+(z), col meccanismo quantificato:**
  dell'astrazione OUT si trasferisce solo la morte (come (c)); le config-FUGA vanno
  attaccate con la realizzazione concreta (antidoto di (z) — qui la fuga era REALE).
  Il contenuto nuovo è il meccanismo: i round-trip rientro-flip-uscita scramblano
  quasi liberamente le parità del bordo (1,2M stati = ~37% del box su 16 celle), e
  la memoria esplode con la striscia (WIDE >30M stati = OOM Python su 16 GB, vedi
  (g)): una fase-1 così non pota quasi nulla.

## 92g. Domande aperte / programma §93

1. **U2-LONTANO (corsa inversa forzata):** enumerare le coperture-nere ammissibili
   (fase 1) e per ciascuna correre la corsa deterministica fresco⇒R fino a y<1 /
   uscita dalla palla-R: se tutte muoiono ≤ B, il Muro si richiude nella forma
   spaziale corretta (§91: l'ipotesi giusta era già spaziale). Gestire le parità
   ignote fuori striscia (branching solo sui rivisitati-di-e′, o fase 1 più larga
   in C con tabella hash a dimensione fissa).
2. **Il lemma dei bianchi che curvano** (verificato dal pannello su 4000 parole:
   morti 1°..5° = 2628/504/258/273/337, ZERO oltre; i 337 al 4° cadono TUTTI sulla
   cella di coda): un cammino all'indietro di soli R torna sulla coda al 4° passo
   (somma dei 4 vettori = 0) e muore entro il 5° (rileggerebbe bianca una cella
   appena dipinta nera); al più 3 freschi consecutivi senza L (stretto, raggiunto).
   Attenzione (pannello, e2): vietare solo le L-SU-FRESCO non uccide — quella corsa
   è deterministica al 100% ma può durare a lungo (2.918 passi sopra la fuga del
   testimone) ACCUMULANDO pending: il mattone giusto è il lemma all-R + il ledger
   dei pending, con bound B certificato caso per caso.
3. **Bilancio globale dei neri freschi lungo il passato intero:** #L-freschi ≤ |seme|
   vale per OGNI passato reale — è un vincolo nuovo, ortogonale a burden/D, che
   collega direttamente la vietanza al germe (§76) e a B-T.
4. **h1=1 mai realizzata** (0/43.726): dimostrare l'ostruzione di corridoio (entrambe
   le celle-giovani di un ingresso su (1,2) con h=2 stanno in striscia ⇒ servono
   corridoi in-tasca lunghi; la fase 1 li ammette, la realtà pare di no).
5. **La congettura §88/§90 va riscritta:** "burden1=0 ⇒ D ≤ 12" è da ritestare contro
   la fuga verso il vergine. Il pannello ha già provato i due attacchi economici, ed
   entrambi FALLISCONO: le sorelle-flip delle nere-fuggenti hanno h1=2 ⇒ D=0 (per
   T1), e 151 coprenti-bianche fresche danno max D=12 — MA con classi NUOVE D=4/8
   mai viste a §90c (che vedeva solo 0 e 12): per la trappola (bb) la coda
   48/56/∞ è plausibile. L'astratto ammette bianche fuggenti (16.388) e confinate
   fino a D=25 > 12: serve una campagna stress-2 dedicata alle bianche.

## 92h. Pannello di scettici (verifica avversaria, 4 lenti)

Pannello multi-agente su raggio/macchina/bilancio/corpus (85 tool call, tutti gli
attacchi meccanici in-repo). Esito: il teorema D=∞, T1/T4, il lemma del suffisso, il
lemma all-R e la coerenza col corpus (§88 σ-rail stessa `valid()`; Blocco Antico;
"D illimitato ⇒ burden1 ≥ 1" con burden 67..1976) REGGONO. Tre BUCHI riparati:
G4 vacuo (rifatto con camminate lunghe e soglie asseribili), ledger dei debiti
(pending per-cella, non solo L-su-fresco), tasso non-universale (controesempio
discesa-in-autostrada a costo O(1) ⇒ l'invariante è il bilancio senza tasso).
Imprecisioni corrette: enunciato 92d ristretto alla forma word-level; T3 col
confinamento sulle celle (non riga_max) e lemma di sovra-approssimazione promosso a
deduttivo; assert di monotonia reso stretto nel codice del raggio; ritrattazione
esplicita della tasca §91b; U1 dichiarato intatto (ri-attaccato: 12/12 bianche
avversarie fresche burden1=0 onset 160); retro-nota su §88 (D(w101)=∞ non certifica
presentabilità ai record lontani); (cc) declassata a istanza di (c)+(z).
Lezione di metodo (gemella del buco-orizzonte §91): **un gate deve poter fallire** —
G4-v1 verificava 31.610 volte lo stesso stato OUT iniziale.

## 92i. Inventario file (alpha1/)

- `u2_pocket_certificate.py` (+`_summary.json`, `.log`) — macchina esatta-in-striscia,
  6 gate, profilo fase-2 (morenti/fuggenti/cicli), verifica testimoni. Run canonica 9 s.
- `u2_infinite_rail.py` (+`_summary.json`, `.log`) — teorema D = ∞ (fuga a posa alta +
  raggio monotono + bilancio dei neri freschi).
- `u2_cover_witnesses.json` — testimoni riproducibili: scala D (0/4/8/12/48/56),
  2 jackpot config-FUGA, 6 nere-D≥400 (riga max 13–33), provenienza delle campagne.
- Nota memoria (trappola g): fase 1 su striscia WIDE = >30M stati = OOM in Python su
  16 GB; MAI rieseguirla in Python (motore C con hash a dimensione fissa, se servirà).
