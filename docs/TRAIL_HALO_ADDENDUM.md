# ADDENDUM TRAIL-HALO — Il Teorema della Scia: l'invariante ambientale di §85 e' un teorema, e con lui l'evitamento §84 e lo 0% motivi vuoti §81 (§86)

Catena addenda: ... HIGHWAY-LANGUAGE §83, ROTOR-LANGUAGE §84, LRRRR-HALO §85, **TRAIL-HALO §86**.

Bersaglio di sessione (roadmap §85.7.1–2): perche' il caos maturo non presenta MAI l'halo bianco
ai deep-black? Misurare la distribuzione dei neri-nell'halo, il bilancio scrittura→rilettura, il
legame con la frontiera B-T; estendere la riduzione-halo a p15.
Esito: la domanda e' **chiusa in modo esatto**. Il caos maturo non presenta mai l'halo bianco
perche' **non puo'**: la scia d'arrivo della formica interseca l'halo negli ultimi ≤3 passi e vi
deposita un nero — a meno che le tre svolte precedenti non siano L,L,L, nel qual caso la
ricostruzione all'indietro mostra che la formica era **sul centro 4 passi prima** e il centro non
e' mai uscito dalla finestra viva: la lettura non e' deep. L'evitamento di (LRRRR)^3 ai deep-event
diventa un **teorema** (la trappola (i) cade per questo enunciato), e il metodo dei lock di
prima-lettura spiega strutturalmente l'intera dicotomia di §84.

> **NOTA DI STATO: run REALI** (container Claude, 1 core): §86a profilo di occupazione halo sulle
> 24 orbite (59 s), self-test 4-heading + ⟺ randomizzato 20k + snapshot 1000 VERDI; gate §85a
> per orbita (nblack, deep_1, tot_all, mat_all) **esatti 24/24**; tripwire ⟺ halo 0 violazioni;
> tripwire T2 (scia) **0 violazioni su 2.323.679 deep_1**; T3 (RLLL+revisita-4) 0 violazioni su
> 5.716 cavalcate; T4 0. §86b lock di prima-lettura con verifica necessita'-tutte + sufficienza
> 1000 junk per parola, gate §85c (lock(LRRRR^3) = halo) VERDE. Strumenti:
> `alpha1/halo_occupancy_profile.py`, `alpha1/word_lock.py`; output
> `alpha1/halo_occupancy_summary.json`, `alpha1/word_lock_summary.json`,
> `alpha1/halo_occupancy_run.log`. Ri-run Ryzen: entrambi gli script (nessun flag necessario).
> NB: bug-story metodologica in §86.6 (offset vs celle assolute, catturato dal tripwire ⟺).

## 86. Riepilogo in una frase
A ogni deep_1 almeno una delle tre **celle di scia** {(0,1),(−1,1),(−1,0)} (frame heading-su) e'
nera con eta' ≤3 — dimostrato per induzione all'indietro e verificato per-evento su 2,3M deep_1
con 0 violazioni — quindi l'halo non e' mai tutto bianco, quindi **nessun deep-black inizia
(LRRRR)^3 in NESSUNA orbita, incluse le eterne**: l'invariante ambientale di §85 non e' una
proprieta' misteriosa del caos maturo ma una conseguenza della geometria d'arrivo piu' la
definizione stessa di deep.

## 86.1 TEOREMA DELLA SCIA (esatto, locale)
**Enunciato.** Sia t una lettura nera deep_1 (cella visitata, fuori dalla finestra viva 3×3).
Allora, nel frame heading-su della lettura, almeno una delle celle {(0,1),(−1,1),(−1,0)} ⊂ HALO
e' nera al tempo t, con ultimo tocco a eta' ≤3. Piu' precisamente, detto j∈{1,2,3} l'indice della
piu' recente svolta R tra t−1,t−2,t−3: la cella di scia d'ordine j e' nera con eta' esattamente j.

**Dimostrazione (induzione all'indietro).** pos(t−1)=(0,1) sempre (cella d'arrivo).
(i) svolta(t−1)=R ⟹ (0,1) letta bianca ⟹ nera ora, eta' 1. Altrimenti (0,1) bianca ora ⟺ letta
nera (L) a t−1 ⟹ heading pre-svolta = destra ⟹ pos(t−2)=(−1,1).
(ii) svolta(t−2)=R ⟹ (−1,1) nera, eta' 2 (non rivisitata a t−1). Altrimenti pos(t−3)=(−1,0).
(iii) svolta(t−3)=R ⟹ (−1,0) nera, eta' 3. Altrimenti heading pre-svolta = sinistra ⟹
**pos(t−4) = centro**: le posizioni t−4..t restano tutte a distanza Chebyshev ≤1 dal centro, che
quindi non attraversa mai l'anello di dimenticanza della finestra r=1 ⟹ centro visitato e in
finestra ⟹ la lettura non e' deep_1 (ne' fresca). Contraddizione. (t≥4 e' automatico: uscire e
rientrare dalla finestra richiede ≥4 passi.) ∎

**Verifica sperimentale (tripwire T2, per-evento):** 0 violazioni su 2.323.679 deep_1, 24 orbite.
Eta' minima dei neri-halo: 1 (49,25%), 2 (33,66%), 3 (17,10%), altro **0**.

**Corollari.**
1. deep_1 ⟹ halo non tutto bianco ⟹ (Teorema Halo §85c) **nessuna lettura deep inizia
   (LRRRR)^3**. L'evitamento totale di §84/§85a (0 su 2,3M) e' un TEOREMA valido per ogni orbita:
   il caveat trappola-(i) di §85.5 cade per questo enunciato. Vale a fortiori per deep_2..4 (⊆).
2. Via l'entailment §85.3 (motivo potato vuoto ⟹ halo bianco): lo **0% di motivi potati vuoti**
   ai deep (§81) e' teorema.
3. **Firma del passato di ogni cavalcata** (t≥4): halo bianco ⟹ svolte(t−4..t−1) = R,L,L,L e
   pos(t−4) = centro — la formica ha dipinto lei stessa il centro di nero esattamente 4 passi
   prima e vi e' tornata col ricciolo sinistro. Ogni cavalcata e' quindi in-finestra, mai fresca,
   mai deep. **Tripwire T3: 0 violazioni su 5.716 cavalcate reali; T4: 0.** (Le 0/3.332 letture
   fresche senza match di §85a sono spiegate: una lettura fresca a t≥4 non puo' cavalcare.)

## 86.2 Risultato §86a — occupazione dell'halo ai deep_1 (24 orbite, 2.323.679 eventi)
| misura | valore |
|---|---|
| k_r (neri nell'halo alla rilettura) | min **1** su 24/24 orbite; moda 4–5; media **4,563** |
| distribuzione k_r | 1: 1,44% · 2: 6,28% · 3: 15,86% · 4: 24,76% · 5: 25,44% · 6: 16,90% · 7: 7,63% · 8: 1,53% · 9: 0,16% |
| eventi k_r=1 (nero solitario) | SOLO sulle 3 celle di scia: (0,1) 21.473 · (−1,1) 6.604 · (−1,0) 5.305 |
| k_w (alla scrittura) medio | 4,259 (Δ medio +0,30: l'halo si arricchisce prima del ritorno) |
| s=0 (halo interamente rifornito nell'intervallo) | **24,37%** — nessun argomento statico alla scrittura poteva coprire i deep |
| neri-halo di seme mai visitato | 0,15% — il rifornimento e' quasi tutto frontiera B-T, non seme |
| per-cella | ~48–49% ovunque (densita' caotica) tranne (−1,0) 57,7% e (−1,1) 56,9% — le celle di scia arricchite dal teorema |
| omogeneita' (trappola q) | k_r medio per bucket eta' del nero profondo: 4,67 / 4,46 / 4,49 / 4,51 / 4,47 — piatto |

Lettura: (a) il minimo empirico e' **1**, quindi il teorema e' **stretto** e non esiste un
enunciato "≥2" da attaccare (risposta alla domanda §85.7.1); gli eventi k=1 realizzano
esattamente e soltanto i tre casi del teorema. (b) L'occupazione tipica (~4,6 su 9, densita'
caotica ~50%) e' molto sopra il minimo: l'evitamento e' doppiamente protetto — garantito dalla
scia, ridondato dall'ambiente. (c) Il 24,4% di eventi s=0 dimostra che la domanda di §85.7.1
("bilancio tra scrittura e rilettura") aveva risposta NEGATIVA sul lato statico: serviva un
argomento dinamico, ed e' la scia con eta' ≤3.

## 86.3 Risultato §86b — lock di prima-lettura (estensione del metodo halo, roadmap §85.7.2)
**Teorema-lock (⟺, per calcolo diretto):** una parola di svolte W parte dalla lettura corrente
⟺ ogni cella primo-letta durante W ha il colore richiesto (L=nera, R=bianca) al momento
iniziale; le riletture sono forzate dall'alternanza. Se una rilettura contraddice, W e'
irrealizzabile da lettura singola in QUALSIASI ambiente. Verifica per parola: necessita' (ogni
flip di cella-lock rompe W) + sufficienza (1000 ambienti junk). Gate: lock((LRRRR)^3) =
{centro nero} + 9 halo bianche — VERDE (riproduzione §85c).

| parola (×3 periodi, tutte le rotazioni) | esito |
|---|---|
| LRRRR (p5) | 2/5 rotazioni realizzabili (LRRRR: 1 nero + 9 bianchi; RRRRL: 0 neri + 10 bianchi) |
| LLRRRR (p6, rotore r2) | **0/6 realizzabili** — irrealizzabile da lettura singola in ogni ambiente |
| LLRRLLRRRR (p10) | **0/10 realizzabili** — idem |
| p15 (LLLLRLRRRRLRRRR) | **15/15 realizzabili**; lock canonico: 5 neri + 6 bianchi (1 periodo) |

Due conseguenze esatte:
1. **L'assenza dei rotori r≥2 dal caos (§84, "anche alla baseline") e' un teorema**: quelle
   parole non sono evitate — sono **impossibili** come parole di lettura ancorate nel piano, in
   qualunque rotazione e ambiente. Esistono solo come parole cicliche dell'astrazione B-T a
   finestra (`radius*_cycles.txt`): coerente con §77 (i teoremi abeliani non trasferiscono) e
   affilatura della trappola (s).
2. **La dicotomia §84 e' spiegata strutturalmente.** I neri richiesti dal lock di p15 sono
   {(0,0), **(0,1), (−1,1), (−1,0)**, (1,0)}: il centro piu' **esattamente le tre celle di scia
   del Teorema della Scia**, piu' (1,0). LRRRR esige solitudine (0 neri extra, 9 bianchi — e la
   scia gliela nega SEMPRE ai deep); p15 esige compagnia proprio dove la scia la deposita. Il
   caos maturo uccide le parole che esigono solitudine e favorisce quelle che esigono la scia:
   evitamento totale di LRRRR, eccesso ×1,9 di p15 — due facce dello stesso teorema.

## 86.4 Interpretazione
- La domanda di §85 ("perche' il detrito profondo non e' mai solo?") si e' rivelata avere una
  risposta **definizionale-geometrica**, non termodinamica: essere deep significa essere tornati
  da fuori-finestra, e tornare da fuori-finestra imprime nella parte posteriore dell'halo la
  propria scia recente. Nessuna proprieta' di "maturita'" del caos e' necessaria: l'enunciato
  vale al passo 4 come al passo 300.000, su orbite finite come eterne.
- Tre fatti empirici di §84/§85/§81 sono ora teoremi esatti (evitamento LRRRR ai deep, firma
  RLLL delle cavalcate, 0% motivi vuoti) e uno e' impossibilita' pura (rotori r≥2). Il
  lato-alpha ha adesso una tecnica esatta che "attraversa la dinamica" (§28.2): ricostruzione
  all'indietro della scia + lock di prima-lettura.
- Onesta' Faraday–Maxwell: **Link 1 non si muove.** Il teorema chiude la domanda locale di §85,
  non l'orbita eterna. Ma cambia l'inventario: le prossime domande dinamiche a diametro finito
  possono ora scontare la scia (vedi trappola (u)) e disporre dei lock come oggetti esatti.

## 86.5 Caveat
- Il teorema copre l'INIZIO di (LRRRR)^3 alla lettura (come il ⟺ di §85c); nulla dice su code
  parziali di cavalcata — irrilevante per gli usi §84/§81.
- k_r medio ~4,6 e la sua piattezza per eta' restano fatti empirici delle 24 orbite (trappola i
  vale per LORO, non piu' per l'evitamento).
- La spiegazione dell'eccesso p15 e' direzionale (il lock domanda scia, la scia c'e'); il valore
  ×1,9 e la massa-nucleo 0% esatta dei p15-rides restano da derivare.

## 86.6 Bug-story metodologica (a futura memoria)
Prima stesura: halo valutato con gli OFFSET del frame al posto delle celle assolute (mancava la
somma a (x,y)). I self-test passavano perche' testavano la formica all'origine, dove offset ≡
celle assolute; il **tripwire ⟺ sui dati reali** (273 violazioni su orbita 0) ha catturato il bug
al primo run. Antidoto permanente: nei self-test la formica va messa in posizione casuale ≠
origine; il ⟺ di un teorema esatto e' il miglior tripwire possibile su dati reali.

## 86.7 Trappola nuova
- **(u) la scia d'arrivo e' gratis.** Le posizioni t−1,t−2,t−3 di una lettura deep giacciono
  (condizionatamente alle svolte) nell'halo posteriore, e i loro colori sono funzione delle
  ultime 3 svolte. Prima di cercare un meccanismo "ambientale/termodinamico" per un enunciato di
  vicinato ai deep-event, RICOSTRUIRE ALL'INDIETRO la scia e verificare se la classe di eventi
  (deep = fuori-finestra) non forzi gia' l'enunciato per definizione. Corollario pratico: ogni
  statistica di vicinato ai deep va prima scontata del contributo di scia.

## 86.8 Roadmap (§87)
1. **Kill-gate §79.1** (deep-black-anchored decisive-depth sweep) — in coda da tre sezioni, ora
   e' il momento: il lato-alpha ha esaurito le domande locali a diametro finito nate dal
   vocabolario.
2. **Lock del linguaggio W0**: applicare il calcolatore di lock alle 46 parole esatte di L_hw
   (§83) — non come ponte di vocabolario (trappola r) ma come inventario esatto: quanti
   neri/bianchi e a che raggio esige il transito? Il confronto lock-caos vs lock-highway e' un
   confronto tra oggetti esatti, il primo possibile finora.
3. (Certificazione) ri-run Ryzen §85a/b/c e §86a/b.

## 86.9 Inventario file
- `alpha1/halo_occupancy_profile.py` + `alpha1/halo_occupancy_summary.json` +
  `alpha1/halo_occupancy_run.log` (§86a: profilo occupazione, tripwire ⟺/T2/T3/T4, gate §85a)
- `alpha1/word_lock.py` + `alpha1/word_lock_summary.json` (§86b: lock di prima-lettura,
  gate §85c, censimento rotazioni)
- `docs/TRAIL_HALO_ADDENDUM.md` (questo file)

## 86.10 Frase di stato dell'arte
*Chiedevamo al caos perche' non lascia mai le nove celle bianche, e la risposta era scritta nei
passi della formica stessa: chi torna da lontano porta con se' la propria scia, e la scia e' nera
almeno in un punto dell'halo — sempre, per ogni orbita, anche eterna. Lo zero su due milioni e
trecentomila non era una statistica: era un teorema che aspettava di essere letto all'indietro.
E la serratura delle parole ha fatto il resto: i rotori profondi non entrano nel piano, la
cavalcata solitaria muore di compagnia obbligata, e p15 prospera perche' chiede in dote proprio
le tre celle che la scia regala. Il lato-alpha ha i suoi primi teoremi.*
