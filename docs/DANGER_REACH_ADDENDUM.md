# ADDENDUM §107c — RAGGIO DEL DEPOSITO: reach per-cella, chiusura dell'orizzonte, sigma sul vocabolario

**Riepilogo in una frase:** la strada P1a (profondita' minima di raggiungibilita'
per cella, scelta col confronto a due round contro un secondo Fable e riparata
in-round: gate sul GAP vs baseline matched, tripla anti-ri-descrizione, scala di
fallback sui costi) e' stata eseguita fino in fondo con motore C validato
(R0/R0b/R1/RG/R2 + lente esterna, tutto bit-identico): l'orizzonte di
raggiungibilita' dell'albero dei prepend CHIUDE — ogni cella di R_T dei 2 lock
e' raggiungibile da qualche passato valido entro d_hit ≤ 48 (A) / ≤ 36 (B),
quindi il "deposito antico" NON e' irraggiungibilita' d'albero (la lettura
forte di §107b era in parte artefatto del cap, esito-B del falsificatore
preregistrato R3, meta' realizzata) — MA (i) il GAP dinamico-vs-geometrico
preregistrato REGGE senza censure (R_T med 32 vs matched 24 su A; 12 vs 4 su
B), (ii) la traduzione deduttiva per-cella da' il raggio temporale ESATTO del
deposito (colore al record deciso da pittura a ≥ d_hit+101 passi: 137-149 su
A, 117-137 su B, salvo le 2 celle recenti note), e (iii) il passato REALE non
legge MAI quelle celle fino al seme (13/14 a 4.487 passi, 9/9 a 18.041 —
riproduce il cuneo vergine §105b con macchinario nuovo): il divario
albero-raggiunge-48 / dinamica-mai e' ora la quantita' esatta che l'attacco a
(ii) deve spiegare. P2 (sigma_D sul vocabolario intero, 1459/1459 esatte a
D=22, zero troncate, regressione 66/66 su §107b): sigma=1 esatto = 71 parole
(4,9%) ⇒ la riduzione di (i) per dominanza-sicura MUORE; la sottopopolazione
lock-capable (sigma ≤ 0.01) = 59 parole (4,0%) concentrata nella banda
|R_T| 16-50 (23/62 = 37%), non nella minima.

Strumenti: `alpha1/danger_reach_depth.py` (Python + gate),
`alpha1/danger_reach.c` (+exe, 10-11 ns/nodo/core),
`alpha1/danger_reach_c_driver.py` (sharding per prefissi, gate R2),
`alpha1/reach_lens_external.py` (lente esterna indipendente),
`alpha1/danger_sigma_vocab.py` + `danger_sigma_vocab_agg.py` (P2),
`alpha1/danger_reach_real.py` (passato reale).

## 107c.1 Metodo di sessione

Confronto a due round con secondo Fable (come §107b.1). Round 1 indipendente:
ranking P1a > P2 (parallelo) > P1b > P3 > P4, con angolo cieco dichiarato (la
misura uniforme sui passati enumerati non e' la misura dinamica — "lock non
estremi" §107b e' measure-dependent). Round 2 (attacchi del titolare, tutti
accettati/riparati): (1) misura dinamica semplificata all'osservabile di
griglia e DICHIARATA sottopotenziata per-parola (n=1-2 per parola: ritirata
come test di §107b, declassata a preregistrazione F3 per la sessione dopo,
join col P2); (2) tripla (D_geo, D_exh, d_hit-SOVRA) + gate sul GAP con
baseline nulla matched per lato e D_geo (metodo §84), morte dichiarata:
indistinguibile ⇒ Cuneo riscritto ⇒ consolidamento; (3) modello di costo
misurato in calibrazione, scala di fallback (minimo informativo D_exh=40,
floor Python 34), dedup esatto escluso (chiave troncata = unsound silenziosa);
(4) lente esterna lanciata come PRIMA azione (lezione panel-lens-timing),
P2 fire-and-forget, un solo fronte attivo.

## 107c.2 Validazione (tutto verde, tutto falsificabile)

- Self-test §5: finestra r1/r2 OK, prodotto 4/4 OK, motore vuota→9977 e
  (7,−7)→106258 OK (highway 22/104 coperta transitivamente da R0).
- **R0** regressione: dfs_census D=28 sui 2 lock bit-identico al summary
  §107b (18.161 / 2.138.444 nodi, cap, nodi_per_depth, cell_bits).
- **R0b** coerenza census↔reach a D=28; **R1** LOCKA (−1,5) d_hit=1;
  **RG** D_geo ≤ d_hit su ogni cella colpita (677/725 celle).
- **Lente esterna indipendente** (secondo agente, brute-force per livelli
  riscritto da zero, MAI letto lo strumento del titolare): LOCKA D=16 e
  LOCKB D=14 — nodes_per_depth bit-identici (17/17 e 15/15 livelli),
  first_hit coerenti; ambiguita' di convenzione risolte con evidenza e
  dichiarate (rotazione ancora verificata su due binari GV0/GV1; onset_germe
  dal record, asse assoluto og+101 — caveat §107b.6 propagato).
- **R2** port C vs Python puro: LOCKA D=36 e LOCKB D=32 bit-identici
  (nodi_per_depth completi + first_hit di TUTTE le celle, 382 e 571).
- **R2-profondo**: i run C a D=55/48 riproducono bit-identici i prefissi
  Python 0..44 (A) e 0..36 (B) — i conteggi per profondita' non dipendono
  dal cap. Somma shard a L=24 == Python (998 e 116.987 prefissi, §4).
- Motore C: griglia densa int8 + undo per-passo, 10-11 ns/nodo/core;
  10,6G nodi (A, D=55) in 8 s e 40,7G (B, D=48) in 28 s su 14 shard.

## 107c.3 Fatti — reach

TRIPLA finale (D_geo = BFS geometrica con solo y≥1; d_hit = minimo SOVRA
dell'albero; D_exh = 55/48, esaustivo, zero censure):

LOCKA (D_exh=55): (−1,5): 1/1; (−3,6): 6/26; poi cluster 36-43 con D_geo
6-12 — (−6,3):12/36, (−5,3):9/37, (−5,2):10/38, (−6,2):11/39, (−4,2):7/39,
(−4,1):8/40, (−4,3):8/40, (−5,1):9/41, (−3,1):9/41, (−3,2):6/42, (0,2):7/43 —
e ultima **(−2,1): 8/48**. Irraggiungibili-esaustive a 55: **0/14**.
LOCKB (D_exh=48): (−4,5):12/16; (−7,2):18/26; (−6,2):15/27; (−6,1):16/28;
(−7,1):17/29; (−5,1):13/29; (−5,2):14/30; (−1,1):9/33; (−4,1):12/36.
Irraggiungibili-esaustive a 48: **0/9**.

1. **L'orizzonte CHIUDE (esito-B parziale del falsificatore R3).** R3
   preregistrato (round 1): "per ciascun lock almeno una cella resta
   esaustivamente irraggiungibile a D=44". Realizzato su LOCKA ((−2,1),
   caduta solo a 48); FALSIFICATO su LOCKB (tutte entro 36). La lettura
   forte di §107b ("bit antichi" come irraggiungibilita') era in parte
   artefatto del cap: le "irraggiungibili a 28" evaporano a 36-48.
   L'enunciato §107b resta vero com'era scritto (a profondita' dichiarata).
2. **Traduzione deduttiva per-cella (sound per le orbite reali, direzione
   trappola c rispettata):** nessun passato valido di NESSUNA profondita'
   legge la cella c a distanza-indietro < d_hit(c) (chiusura per troncamento)
   ⇒ a ogni record reale che presenta w, il colore di c e' deciso da pittura
   a ≥ d_hit(c)+101 passi dal record. Raggio esatto del deposito antico:
   **137-149 passi (A, 12 celle), 117-137 (B)**; le eccezioni "recenti" sono
   le note (−1,5) (102) e (−3,6) (127) di A, (−4,5) (117) di B.
3. **GAP gate preregistrato: REGGE** (non e' la morte "Cuneo riscritto").
   R_T mediana 32 vs matched 24 (A; pool n=31, DICHIARATO sottile) e 12 vs 4
   (B; n=48). Zero censure al cap finale. Onesta': su A anche il matched e'
   alto (24) — l'ombra dinamica e' in gran parte proprieta' della REGIONE
   (il cuneo del drift §105b), con R_T estrema dentro; su B il contrasto e'
   3x netto. Le due finestre dello stesso flusso (shift-10) mostrano regimi
   diversi: A geo-vicina ma dinamicamente tardiva (gap 26-40), B geo-lontana
   e colpita presto dopo il bound (gap 8-16 tranne (−1,1): 24).
4. **Il passato reale non arriva MAI** (`danger_reach_real.py`, n=1 per
   episodio, descrittivo): fino al seme (4.487 e 18.041 passi) il passato
   vero legge solo (−1,5)@1 su A e NESSUNA cella su B — riproduzione esatta
   del cuneo vergine §105b con macchinario indipendente. Il confronto e'
   la forma quantificata della sovra-approssimazione: l'albero tocca tutto
   entro 48, la dinamica reale MAI. I d_hit non sono fatti dinamici
   (etichetta SOVRA obbligatoria); il divario 48-vs-MAI e' l'oggetto che la
   misura dinamica (F3) deve spiegare.

## 107c.4 Fatti — P2 (sigma_D sul vocabolario intero)

1459/1459 parole canoniche misurate ESATTE a D=22 (14 shard, ~10 min, zero
troncate, zero errori; regressione 66/66 bit-compatibile con lo scan §107b;
i 2 lock sono fuori-censimento, "+2"). Per bande di |R_T|
(n / sigma=1 esatto / sigma≤0.01 / sigma mediana):
≤15: 4 / 0 / 1 / 0.902 — 16-50: 62 / 4 (6,5%) / **23 (37,1%)** / 0.066 —
51-100: 158 / 6 / 17 / 0.806 — 101-300: 513 / 26 / 13 / 0.9997 —
301+: 722 / 35 / 5 / 1.0000. Totale: sigma=1 esatto **71 (4,9%)**,
sigma≤0.01 **59 (4,0%)**, sigma med 0.9999.

1. **La riduzione di (i) per dominanza-sicura MUORE:** le parole
   deduttivamente sicure (sigma=1 esatto a D=22) sono il 4,9%, non la
   maggioranza. (i) non si restringe gratis.
2. **La sottopopolazione lock-capable si concentra in |R_T| 16-50** (37,1%
   della banda a sigma≤0.01), NON nella banda minima: sigma≈0 e taglia
   minima sono assi DIVERSI dentro la classe pericolosa allargata.
3. Le parole grosse (n>100) hanno sigma med ≈ 1.0000 ma sigma=1 esatto raro
   (~5%): lo scudo diventa quasi-certo ma quasi mai certificato — il
   certificato esatto resta un oggetto raro a ogni taglia.
4. Celle irraggiungibili a D=22 quasi universali (1.452/1.459 parole con
   ≥1): a cap basso l'"antichita'" e' generica (coerente con la chiusura
   dell'orizzonte, 107c.3.1) — mai piu' usarla nuda come discriminante.

## 107c.5 Riduzione per la scala (stato §107d)

(ii) e' definitivamente al livello PRE-STORIA e ora ha la forma esatta:
fallimento dello scudo = **verginita' perpetua** delle celle del cuneo (il
rifornimento della Scala §98/§104 non arriva mai li', pur potendo l'albero
arrivarci entro 48 passi). L'attacco deve misurare/vincolare la PITTURA
dinamica del cuneo, non l'albero: F3 preregistrata (sessione dopo, richiede
il join ora disponibile `sigma_vocab_perword.jsonl` × colori di griglia alla
§106): calibrazione pooled sigma_D ↔ ricchezza-scudo di griglia sul canonico
(1639 record), per bande di sigma, contando EPISODI, nessuna soglia;
aspettativa: correlano; se non correlano, "lock non estremi" §107b perde la
base di misura. (i) resta con tasso misurato 0,2-4%/record sulla classe
piccola; la mappa sigma≈0 (59+2 parole) e' il bersaglio della ricorrenza.

## 107c.6 Trappole nuove

- **(ss) l'irraggiungibilita' a cap e' un negativo con data di scadenza:**
  un certificato "cella/oggetto irraggiungibile a profondita' D" non e' un
  fatto strutturale finche' il fenomeno non CHIUDE (tutti i d_hit finiti,
  qui a 36-48) o il cap non e' spinto alla chiusura; costruire teoria
  sull'assenza a cap basso eredita la scadenza (12/14 e 5/9 "antichi" a
  D=28 → 0 a D=55/48). I fatti stabili sono la tripla (D_geo, d_hit, gap
  vs matched) e la traduzione per-cella "deciso a ≥ d_hit+K". E' la (qq)
  sulle soglie di PROFONDITA', gemella di (h)/(bb) sul piano dei cap.
- (istanza di c, da tenere a mente qui): i d_hit dell'albero NON predicono
  la dinamica — il passato reale non tocca a 4k-18k cio' che l'albero tocca
  a 16-48. L'albero serve SOLO per i negativi (irraggiungibilita', che
  trasferisce) e per i budget; mai leggere d_hit come "quando succede".

## 107c.7 Prossimo (§107d o §108)

1. **P1b col raggio in mano:** "scudo antico copre il cuneo" formalizzato
   col Lemma del Cono §87 al livello pre-storia — il fronte del cono passato
   vs R_T, con i d_hit come budget per-cella (le celle del cuneo hanno
   pittura possibile solo da rami che il cono reale non percorre: perche'?).
2. **F3 calibrazione** (preregistrata a 107c.5): join sigma_vocab_perword ×
   colori di griglia §106 sul canonico; episodi, nessuna soglia.
3. **Reach sulle 59 parole sigma≤0.01** (ora economico: motore C, ~30 min):
   le triple e i gap della sottopopolazione lock-capable — il gap R_T>matched
   e' proprieta' dei lock o di tutta la sottoclasse?
4. F1 gamba-Cuneo stratificata (ereditata, dichiarata).
5. Ereditati: §106c, §105b.4, §101g, §102f, §103d, §104f.

## 107c.8 Inventario file

- `alpha1/danger_reach_depth.py` + `danger_reach_depth_summary.json` +
  `danger_reach_depth_run1.log`, `run2.log` (Python: gate R0/R0b/R1/RG,
  run D=36/32 e D=44/36).
- `alpha1/danger_reach.c` + `danger_reach.exe` (motore C, job per prefissi).
- `alpha1/danger_reach_c_driver.py` + `danger_reach_c_LOCKA_d36.json`,
  `danger_reach_c_LOCKB_d32.json` (gate R2), `danger_reach_c_LOCKA_d55.json`,
  `danger_reach_c_LOCKB_d48.json` (run finali) + `reach_c_*.log`.
- `alpha1/reach_lens_external.py` + `reach_lens_external.json` (lente).
- `alpha1/danger_sigma_vocab.py`, `danger_sigma_vocab_agg.py`,
  `sigma_vocab_perword.jsonl`, `sigma_vocab_summary.json` (P2; i log/shard
  jsonl restano fuori repo, rigenerabili).
- `alpha1/danger_reach_real.py` + `danger_reach_real.json` (passato reale).
