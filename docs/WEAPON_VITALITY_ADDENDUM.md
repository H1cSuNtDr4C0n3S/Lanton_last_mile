# ADDENDUM §88 — RECORD-WEAPON VITALITY: la Parola Viva e il Residuo dell'Uno

**Riepilogo in una frase:** la caccia v3 con filtro di vitalita' scende a burden1 = 1
(K = 101, residuo la sola cella (1,1)) e il passato di quella parola, dietro un collo di
bottiglia a binario unico, si stabilizza su un ciclo di prepend `σ = LLRLLRLL` con
CERTIFICATO GEOMETRICO finito ⇒ **D(w101) = ∞**: primo teorema-parola ai record **NON
vacuo** (trappola (w) scaricata su questo campione), e il pigeonhole di Link 1 si sposta
dal Residuo dei Cinque al **RESIDUO DELL'UNO**.

Macchina: Ryzen 7 5800X (macchina canonica) — nessuna certificazione pendente.
Sessione: 2026-07-02/03. Prerequisiti: CONE-LOCK §87 (Lemma del Cono, Lemma della
Finestra-K, burden1, record-compatibilita', trappola (w)).

## 88.1 La run v3 (caccia con vitalita' incorporata)

`record_weapon_hunt.py --beam 4000 --kmax 120 --viable-k 8 --per-class 200
--budget-s 21600` (15 worker, 1165 s — a fermarla e' stato kmax, non il budget).
Log: `alpha1/record_weapon_ryzen3.log`; summary: `alpha1/record_weapon_summary.json`.

Discesa del minimo (solo candidati con catena di prepend ≥ 8):

| K | 10 | 12 | 14 | 15 | 16 | 17 | 18 | 19 | 24 | 25 | 26 | 33 | 34 | 45 | 100 | **101–120** |
|---|----|----|----|----|----|----|----|----|----|----|----|----|----|----|-----|---------|
| burden1 | 19 | 18 | 16 | 15 | 14 | 11 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | **1** |

- Residui: a 3 celle {(-2,1),(0,2),(1,1)} per K=45–71, poi cambio famiglia a K=72 verso
  {(1,1),(4,1),(4,2)}; a 2 celle {(1,1),(4,1)} (K=100); a **1 cella {(1,1)}** da K=101,
  stabile fino al cap 120. Onset del germe 160 per tutta la famiglia finale.
- `weapon: null` — nessun burden1 = 0 fino a K = 120.
- Rilettura di §87e-bis: nella run senza filtro (beam 8000, kmax 160) il 2 moriva a K=71 e
  il beam collassava nella staffetta vacua a fardello 4. Col filtro di vitalita' il minimo
  VIVO continua a scendere: il collasso era inquinamento da minimi vacui, non un pavimento.
- La sentinella e' cambiata: non piu' (-2,1) (§87e) ma **(1,1)** — la diagonale
  dietro-destra della posa record.

**Struttura delle parole (figura `alpha1/record_weapon_words.png`,
script `record_weapon_words_fig.py`):** (i) le parole best-per-K crescono per prepend
(10 tratti di catena a suffisso); (ii) la parola K=120 contiene un motivo interno di 21
lettere (`RLRRRRLLLLRLLLLRLRRLR`, posizioni 6 e 78) ripetuto: p = 0.004 su 500 shuffle
anche con nulla condizionata alle streak ≤ 4 (accettazione 0.9%); (iii) il motivo NON e'
un frammento di W0: LCS con W0 ciclica = 15, p ≈ 0.15 (caso); (iv) nessuna periodicita'
globale (autocorrelazione max 0.70 su sovrapposizione 30). Nota onesta: il motivo-21 vive
nel transiente τ e dentro w101 (posizioni 6 e 78 di w120), NON nel regime σ del §88.4 —
stesso genere di fenomeno (il passato quasi-forzato ricicla mattoni), oggetto diverso.

## 88.2 Vitalita' di w101 (`record_weapon_vitality.py`)

`w101 = LLRLRRLRLRRLLRLLLLRLRRRRLLLLRLRLLLLRLLRLLRRLLRLLRLRLRLLRLRLRLRRRRLLLLRLLLLRLRRLRRLRRRRLRRLRLRLLLLRLRL`
(101 svolte, burden1 = 1, residuo {(1,1)}, onset 160).

**Gate (tutti verdi, fermarsi al primo rosso):** riproduzione in-process di w101, w120 e
di TUTTA la catena best K=102..120 (burden1/onset bit-identici al summary della run);
controllo negativo = il campione vacuo K=60 di §87e-2
(`LRLLRLRRLLLLRRLLLLRRLRRLRRLRRRRLLLLRLLRLRRLRLRLLRLLRLLRLRLRL`): burden1 = 2, onset 156,
residuo {(-2,1),(1,1)} riprodotti, e **D = 2** (estinzione entro prof. 3, come dichiarato
in §87e-2).

- **Test A (profondita'):** D(w101) ≥ 104 in 256 nodi/0.3 s, e il burden1 lungo TUTTA la
  catena testimone resta 1 (min = max = 1).
- **Test B (muro esaustivo):** conteggio dei prefissi di prepend validi per profondita'
  1..14: `[2,1,1,1,1,1,1,1,1,1,1,1,1,1]` — dietro w101 c'e' (quasi) un BINARIO UNICO.
  I 15 candidati-ciclo con σ = prefissi del binario (p ≤ 14) NON certificano: il taglio
  cade nel transiente, non nel regime (vedi §88.3 e trappola (x)).
- **Test C (corridoio a fardello ≤ 1):** DFS esaustiva con pota burden1 > 1 sopra w101:
  vedi §88.6 (risultato riportato li' per via del costo: la coda del muro contiene germi a
  onset lento).

## 88.3 Il binario forzato e il suo regime (`record_weapon_rail.py`)

DFS early-exit a bersaglio 624 (1952 nodi, 5 s): **D(w101) ≥ 624 con burden1 = 1 e residuo
{(1,1)} COSTANTI lungo tutta la discesa**. L'unicita' esaustiva vale per prof. 2..17; da
prof. 18 il muro si riapre (2,3,5,8,13,20,33,55,90,147,243,406,656 a prof. 30, crescita
~×1.65/livello): il binario unico e' un collo di bottiglia finito, non una forzatura
eterna (trappola (y)).

Cross-check indipendente della strettoia: i 19 prepend del beam (w120 = best della run v3)
e le 19 lettere recenti del binario DFS coincidono bit-identici (`LLLRLRRLRRRRLLLLRLL`) —
due ricerche indipendenti forzate sullo stesso binario, come l'unicita' esige.

Il testimone profondo mostra un regime periodico interno: finestra massima di periodicita'
= periodo **8**, intervallo [3,320) del binario = 317 lettere = **39.6 periodi** del blocco
`LLRLLLLR`. Lo scan di "periodicita' eventuale" ingenuo (periodo valido fino alla lettera
piu' vecchia) FALLISCE anche a transiente 480: le lettere piu' profonde del testimone
early-exit sono le meno vincolate e deviano dal regime (trappola (x)).

## 88.4 Il ciclo certificato: D(w101) = ∞ (`record_weapon_cycle.py`)

Dalla finestra interna: `σ = LLRLLRLL` (rotazione del blocco `LLRLLLLR`; 2 R, 6 L ⇒
heading di ritorno 0, ordine q = 1), `τ` = le 304 lettere recenti del binario,
`base2 = τ + w101` (405 svolte). **Certificato geometrico** (stile Teorema HALO §85):

1. il cammino virtuale di σ e' realizzabile, heading di ritorno 0 e drift
   Δ_walk = (0,2) ≠ 0 ⇒ ogni blocco σ successivo e' la COPIA TRASLATA del precedente
   (la dinamica della camminata virtuale e' invariante per traslazione);
2. i conflitti di rilettura tra blocchi (e tra blocco e base2) dipendono solo dal gap g e
   sono impossibili per g > g_max = ⌊diam/|Δ|∞⌋ + 1 = 12 ⇒ la validita' di
   `σ^m + base2` per OGNI m segue dal check finito m ≤ M_cert = 14 (catena
   lettera-per-lettera verificata);
3. record-compatibilita' eterna: Δ_anchor = (-2,0) ha componente y = 0 ≤ 0 ⇒ i blocchi
   vecchi traslano in orizzontale nel frame anchor e il footprint resta in {y ≥ 1}.

⇒ **realizzabilita' + record-compatibilita' di `σ^m·τ·w101` per OGNI m: D(w101) = ∞.**
La parola ha un passato record-compatibile esplicito, periodico, illimitato.

**Chiusura della clausola-onset (`record_weapon_onset_lock.py` — il sigillo).** L'onset
del germe (che definisce burden1) non e' coperto dall'induzione di traslazione; era
empirico (m ≤ 40 diretto; lo scettico della verifica multi-agente l'ha esteso a
m = 50/100/200: onset SEMPRE 160). Chiuso col Lemma Replay-Lock (§87a): la corsa fino a
onset+P dipende solo dai colori delle celle visitate V. A m0 = 40: |V| = 81, bbox x ∈
[-8,4]; i blocchi nuovi del germe sono copie traslate esatte a passo (2,0) che partono da
x ∈ [95,98] e si ALLONTANANO — disgiunti da V per ogni m (check finito + monotonia del
bbox). Per induzione: run(m) = run(40) per OGNI m ≥ 40 (controprova diretta m = 41..46:
onset, V, burden, residuo identici). ⇒ **per ogni m ≥ 40: onset = 160, burden1 = 1,
residuo {(1,1)} — TEOREMA. Nessuna clausola empirica residua** (m < 40 verificati uno a
uno). Il censimento §87b, coerentemente, non ha mai visto germi senza onset.

**Falsificazione del certificato (`record_weapon_cycle_verify.py`, tutto verde):**
(1) verifica diretta in simulazione per m = 15..40 (ben oltre M_cert): tutte valide,
burden1 = 1 e residuo {(1,1)} costanti; (2) catena lettera-per-lettera fino a m = 20
(K = 565); (3) traslazione esplicita del footprint anchor su 5 coppie consecutive
(m = 2,5,9,14,20): celle nuove = blocco precedente traslato di (2,0), colori identici.

## 88.5 TEOREMA DELLA PAROLA VIVA (Residuo dell'Uno)

**Teorema.** Esiste una parola w* di 101 svolte (w* = w101), realizzabile e
record-compatibile, con **D(w*) = ∞** (passato periodico certificato `σ^∞·τ`) e
**burden1(w*) = 1**, residuo {(1,1)}. Per il Lemma del Cono e il Lemma della Finestra-K
(§87): a ogni pose-record y-min in cui le ultime 101 svolte sono w*, l'ingresso in
autostrada e' deciso dalla SOLA cella (1,1) del frame anchor (la diagonale dietro-destra):
se e' bianca, l'orbita entra (onset 160 del germe).

**Contrappositiva (per orbite eterne non-highway):** a OGNI record y-min con suffisso w*,
la cella (1,1) DEVE essere lo spoiler (nera). E l'enunciato NON e' vacuo: w* ammette
passati record-compatibili di profondita' arbitraria (a differenza di tutti i minimi
§87e-2, estinti entro prof. 3–7).

**Cosa il teorema NON dice:** che w* occorra davvero ai record delle orbite eterne (quella
e' la dinamica dei record, §88.8-1), ne' che 1 sia il pavimento vivo (l'arma resta
logicamente possibile per K > 120 o su altri rami). Congettura §88 aggiornata: per ogni w
record-compatibile con D(w) illimitato vale burden1(w) ≥ 1 — ora sappiamo che il livello 1
e' OCCUPATO da una parola viva; l'arma, se esiste, deve battere un livello gia' realizzato.

**Corollario (Famiglia Viva):** con la chiusura della clausola-onset, la famiglia
`σ^m·τ·w101` e' una linea INFINITA di parole record-compatibili tutte con burden1 = 1 e
residuo {(1,1)} (teorema per ogni m ≥ 40, verifica diretta per m < 40): non una parola
viva, una progressione aritmetica di parole vive alla stessa cella.

## 88.6 Test C — il corridoio a fardello ≤ 1 (largo, senza arma)

DFS con pota burden1 > 1 sopra w101, cap di profondita' 60, budget 1.5M nodi (2073 s —
la coda del muro contiene germi a onset lento): **NON esaustivo**, e proprio per questo
il risultato e' notevole: **486.676 rami VIVI al cap 60**, morti quasi assenti
(1 a prof. 1 — il fratello della strettoia —, 81 a prof. 53, 851 a prof. 57),
**arma: nessuna** (nessun burden1 = 0 in 1.5M valutazioni).

Lettura: il livello fardello-1 non e' una linea sottile ma un ALBERO ESPONENZIALE di
parole (il corridoio resta a burden 1 quasi ovunque oltre la strettoia 2..17): w101 non e'
un'eccezione, e' il rappresentante certificato di una famiglia larga. Onesta': la
non-esaustivita' implica che l'assenza dell'arma nel corridoio esplorato NON e' una prova
di impossibilita' — e' pero' il terzo campione ampio consecutivo (beam v3 K<=120, binario
624, corridoio 1.5M) in cui burden1 = 0 non compare mai.

## 88.7 Trappole nuove

- **(x) il fondo del testimone DFS non e' il regime.** Le lettere piu' profonde di un
  testimone early-exit sono le meno vincolate (qualsiasi continuazione valida chiude il
  target): uno scan di periodicita' eventuale che pretende il periodo fino in fondo boccia
  cicli REALI (qui: periodo 8 con 39.6 periodi osservati, invisibile a transiente 480).
  Antidoto: cercare la finestra periodica interna massima e certificare con σ, τ estratti
  da li' — il certificato ri-testa tutto da zero, il testimone serve solo da suggeritore.
- **(y) collo di bottiglia ≠ forzatura eterna.** Il muro dei prepend puo' essere a binario
  unico per un tratto finito (qui prof. 2..17) e riaprirsi esponenzialmente (×1.65). Non
  dedurre unicita'/forzatura globale del passato da un tratto esaustivo corto; dichiarare
  sempre fino a che profondita' l'unicita' e' esaustiva.

## 88.8 Domande aperte / roadmap §89

1. **Dinamica dei record (ora l'attacco principale):** w* (o la famiglia `σ^m·τ·w*`)
   OCCORRE ai record reali delle 24 orbite? Piu' in generale: quali parole vive a burden1
   basso occorrono, e con che frequenza? Se parole a fardello 1 sono inevitabili ai
   record, il pigeonhole si gioca su UNA cella.
2. **Pigeonhole sull'Uno:** cosa vieta a un'eterna di tenere (1,1) sempre nera ai record
   con suffisso w*? La riga y_rel = 1 del record corrente era la riga-record del passaggio
   precedente (§87.9-1); la cella (1,1) e' inoltre a distanza 1 dalla scia d'arrivo
   (§86): c'e' spazio per un argomento di scia/eta'.
3. **L'arma:** proseguire la caccia (kmax > 120, altri rami del muro riaperto) con la
   lente nuova: l'arma deve essere una parola VIVA a burden1 = 0. Decidere la congettura
   del pavimento vivo ≥ 1 — l'automa dei prepend (stato = bordo della camminata virtuale)
   e' lo strumento candidato per un argomento di impossibilita'.
4. **Record doppi / angoli** (§87.9-3, invariato).

## 88.9 Inventario file (tutti in `alpha1/`)

- `record_weapon_summary.json` + `record_weapon_ryzen3.log` — run v3 (beam 4000, kmax 120,
  viable-k 8, per-class 200): burden1 = 1 a K = 101..120, weapon null.
- `record_weapon_words_fig.py` + `record_weapon_words.png` — figura struttura parole +
  LRS/LCS con baseline nulla (anche condizionata streak ≤ 4).
- `record_weapon_vitality.py` (+`_summary.json`, `.log`) — gate, D ≥ 104, muro esaustivo
  prof. 14, corridoio fardello ≤ 1, controllo negativo K=60.
- `record_weapon_rail.py` (+`_summary.json`, `.log`) — binario a prof. 624, burden1 = 1
  costante, unicita' 2..17, riapertura esponenziale, scan periodicita'.
- `record_weapon_cycle.py` (+`_summary.json`, `.log`) — finestra periodica massima e
  CERTIFICATO del ciclo σ = LLRLLRLL (D(w101) = ∞).
- `record_weapon_cycle_verify.py` (+`_summary.json`, `.log`) — falsificazione del
  certificato: verifica diretta m = 15..40, catena K = 565, traslazione esplicita.
- `record_weapon_onset_lock.py` (+`_summary.json`, `.log`) — il sigillo: chiusura della
  clausola-onset via Replay-Lock (run(m) = run(40) per ogni m ≥ 40).

**Verifica avversaria multi-agente (chiusura sessione):** 4 verificatori indipendenti
(numeri run v3, numeri vitalita'/binario/ciclo, scettico sulla logica del certificato,
coerenza documentale): 46 claim controllati, 43 ok; i 3 non-ok erano (i) tabella §88.1
senza i gradini K=15/16 (corretta), (ii) residuo del controllo K=60 non stampato nel log
(verificato dall'assert in-process del gate), (iii) la clausola-onset dichiarata empirica
— poi CHIUSA da `record_weapon_onset_lock.py` (sopra). Lo scettico non ha trovato buchi
nella logica del certificato e ha esteso la frontiera empirica a m = 200 prima della
chiusura teorica.
