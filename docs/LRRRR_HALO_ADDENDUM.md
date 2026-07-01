# ADDENDUM LRRRR-HALO — Il teorema-finestra e' falso, ma cade meglio: caratterizzazione esatta e invariante ambientale (§85)

Catena addenda: ... CORE-TAIL-PROFILE §82, HIGHWAY-LANGUAGE §83, ROTOR-LANGUAGE §84,
**LRRRR-HALO §85**.

Bersaglio di sessione (roadmap §84.5.1): trasformare l'evitamento totale di (LRRRR)^3 ai deep-black
in un teorema esatto via automa finestra (enunciato "ogni cammino", trappola-c compliant).
Esito: **il teorema-finestra universale e' FALSO** (testimone reale trovato), ma la falsificazione
consegna di piu' di quanto il teorema avrebbe dato: una **caratterizzazione locale esatta** (⟺)
dell'inizio-cavalcata, un **invariante ambientale** del caos maturo, e un'**entailment** tra §84 e §81.

> **NOTA DI STATO: run REALI** (container Claude, 1 core): §85a profilo in profondita' sulle 24
> orbite (153 s), tripwire catena deep_4⊆…⊆deep_1 = 0 violazioni, gate §84 (deep_4 → 0 match) OK.
> §85b certificatore automa r=1,2,3 (build 45.971 stati r3 in 1,3 s; conteggi r1=15/r2=403 stati
> coerenti coi selftest verdi di sessione). §85c testimone + teorema halo con assert (necessita'
> 9/9, sufficienza 1000 ambienti). Strumenti: `alpha1/lrrrr_depth_profile.py`,
> `alpha1/lrrrr_avoidance_certificate.py`, `alpha1/lrrrr_halo_witness.py`; output
> `alpha1/lrrrr_depth_summary.json`, `alpha1/lrrrr_certificate_summary.json`.
> Ri-run Ryzen: i tre script con `--workers 16` dove applicabile.

## 85. Riepilogo in una frase
L'evitamento e' gia' massimale a **r=1** (0 match su **2.323.679** eventi deep_1; i 5.716 match
reali, 0,18% delle letture nere, vivono TUTTI in-finestra), ma l'automa resta INCONCLUSIVO a
r=1,2,3 con **4 sopravvissuti stabili** — e i sopravvissuti sono **reali**: un nero isolato nel
bianco cavalca (LRRRR)^3 (poi muore in LLLLR al 4o periodo, coerente B-T). La lettura giusta e' un
**⟺ locale esatto**: una lettura nera inizia (LRRRR)^3 *se e solo se* le **9 celle-halo** (esplicite,
raggio ≤2, frame heading) sono tutte bianche — quindi l'evitamento empirico equivale a: *nel caos
maturo, un deep-black non e' mai isolato a scala 2 lungo il cammino imminente*.

## 85.1 Risultato §85a — profilo in profondita' (24 orbite, pooled)
| popolazione | match (LRRRR)^3 | totale | tasso |
|---|---:|---:|---:|
| tutte le letture nere | 5.716 | 3.181.317 | 0,1797% |
| mai visitate (seme) | 0 | 3.332 | 0 |
| in-finestra a ogni r | **5.716** | 854.306 | **0,6691%** |
| deep_1 | **0** | **2.323.679** | 0 |
| deep_2 / deep_3 / deep_4 | 0 / 0 / 0 | 1.778.349 / 1.613.844 / 1.523.283 | 0 |

**r\* = 1**: l'evitamento vale gia' per ogni lettura nera di cella uscita anche solo dalla finestra
3×3. Le 5.716 cavalcate reali sono tutte spirali della formica sulla propria scia immediata.

## 85.2 Risultato §85b — certificatore automa (r=1,2,3)
| r | stati | archi assumeB | sopravvissuti (LRRRR)^2 | sopravvissuti (LRRRR)^3 |
|---|---:|---:|---:|---:|
| 1 | 15 | 11 | 10 | 10 |
| 2 | 403 | 151 | 76 | **4** |
| 3 | 45.971 | 13.537 | 5.853 | **4** |

A r=3, 5.849 archi muoiono esattamente alla profondita' 10 — la L del terzo periodo, dove la
finestra ormai sa che la cella e' bianca. I 4 sopravvissuti sono stabili r2→r3; ispezione: le L dei
periodi 2-3 sono **forzate** (la cavalcata rilegge i propri neri: auto-alimentata come il rotore),
e le uniche assunzioni residue sono **assW** (bianchi = default dello spazio vuoto). Il primo
sopravvissuto parte dallo stato tutto-U.

## 85.3 Risultato §85c — testimone e teorema halo
- **Testimone**: nero isolato in spazio bianco, formica sopra ⇒ parola LRRRR·LRRRR·LRRRR·LLLLR…
  Il teorema-finestra universale e' **falso**; i 4 sopravvissuti non erano fantasmi.
- **Teorema halo (⟺, per calcolo diretto)**: una lettura nera inizia (LRRRR)^3 ⟺ le 9 celle
  HALO = {(−2,0),(−2,1),(−1,−1),(−1,0),(−1,1),(−1,2),(0,−1),(0,1),(0,2)} (frame heading-su,
  raggio max 2) sono tutte bianche alla lettura. Nei 15 passi vengono primo-lette esattamente
  {centro}∪HALO; la dinamica consulta solo celle lette ⇒ tutto il resto e' irrilevante.
  Verifica: necessita' 9/9 (ogni singolo flip rompe la parola), sufficienza per costruzione +
  1000 ambienti junk (assert verdi in `lrrrr_halo_witness.py`).
- **Entailment §84 ⇒ §81**: motivo potato vuoto ⇒ (HALO ⊆ visitate-104 ∩ r3) halo bianco ⇒
  cavalcata. Contrapposta: evitamento totale (§84) ⇒ **0% motivi vuoti** — esattamente il valore
  misurato indipendentemente in §81. Due fatti empirici, una implicazione.

## 85.4 Interpretazione
- La falsificazione e' produttiva: al posto di un teorema-finestra (impossibile: il testimone e'
  reale) abbiamo la **riduzione esatta** dell'evitamento a un enunciato ambientale finito:
  *"nessun deep-black presenta l'halo bianco di 9 celle"* — 0 su 2,3M a r=1. E' il primo enunciato
  del lato-alpha con **forma finita e bersaglio dinamico preciso** (9 celle, raggio 2): esattamente
  il tipo di domanda "attraversa la dinamica" che §28.2 prescriveva, ora con un oggetto concreto.
- L'automa ha fatto il suo lavoro da sovra-approssimazione onesta: ha ucciso 13.533/13.537 archi e
  indicato col dito i 4 realizzabili.
- I match reali (0,67% degli in-finestra) sono il residuo di auto-gioco della formica sulla scia
  fresca: coerente con l'arricchimento giovani-morso-fed di §82.C.

## 85.5 Caveat
- 0/2,3M e' empirico su 24 orbite convergenti (trappola i): l'invariante ambientale non e' deciso
  per orbite eterne — e' pero' adesso un bersaglio dimostrativo finito e ben posto.
- Il ⟺ vale per l'inizio-cavalcata alla lettura; non parla di code parziali di cavalcata (un
  evento a meta' giro non e' coperto — irrilevante per gli usi §84/§81).

## 85.6 Trappola nuova
- **(t) assW e' gratis.** Nei certificati via automa, sopravvissuti i cui archi di assunzione sono
  solo assW (bianco = default dello spazio vuoto/povero) sono un campanello di realizzabilita',
  NON indizio di fantasma: il bianco si realizza col nulla. Prima di scalare il raggio, ispezionare
  i sopravvissuti e tentare il testimone diretto (qui: nero isolato, trovato in un passo).

## 85.7 Roadmap
1. **§86 (il bersaglio nuovo)**: perche' il caos maturo non presenta mai l'halo bianco ai deep-black?
   Candidati: bilancio di occupazione dell'halo tra scrittura (ultima visita) e rilettura della
   cella profonda; legame con il Lemma del morso / frontiera B-T; misura della distribuzione del
   numero di neri nell'halo ai deep-event (se il minimo empirico e' ≥2, l'enunciato da attaccare
   e' piu' forte del necessario).
2. Estendere il metodo halo alle altre parole: (LRRRR)^2 ha 76→5.853 sopravvissuti (non e' una
   parola a halo unico); p15 (i rides puro-coda di §84) merita la stessa riduzione.
3. Kill-gate §79.1 resta in coda.
4. (Certificazione) ri-run Ryzen §85a/b/c.

## 85.8 Inventario file
- `alpha1/lrrrr_depth_profile.py` + `alpha1/lrrrr_depth_summary.json` (§85a, tripwire catena)
- `alpha1/lrrrr_avoidance_certificate.py` + `alpha1/lrrrr_certificate_summary.json` +
  `alpha1/lrrrr_certificate_run.log` (§85b, r=1,2,3)
- `alpha1/lrrrr_halo_witness.py` (§85c, teorema halo con assert)

## 85.9 Frase di stato dell'arte
*Cercavamo un teorema di finestra e abbiamo trovato di meglio: la cavalcata elementare ha una
serratura esatta — nove celle bianche in croce attorno al nero — e il caos maturo non lascia mai
quella serratura aperta: due milioni e trecentomila occasioni, zero volte. Il teorema universale e'
falso per colpa di un nero solitario nel deserto bianco, ma proprio quel testimone ci ha dato la
chiave: adesso la domanda del lato-alpha ha nove celle di diametro. Perche' il detrito profondo non
e' mai solo? Chi risponde a questo, attraversa la dinamica.*
