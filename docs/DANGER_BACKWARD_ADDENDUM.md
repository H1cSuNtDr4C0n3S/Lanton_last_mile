# ADDENDUM §107b — SCUDO ANTICO: autopsia all'indietro della classe pericolosa

**Riepilogo in una frase:** l'attacco per-parola all'indietro (strada E del
confronto a due round, round-2 accettato con riparazioni) e' stato eseguito su
F0 (geometria word-side) e F2 (albero dei prepend): la classe pericolosa e'
risultata una RI-DESCRIZIONE della taglia (classe ≡ |R_T| piccolo ≡ read-set
direzionale ≡ transiente corto; theta_min DEGENERE: il Cuneo non forza mai
l'intero read-set word-side), la macchina dei prepend con classificazione al
cap da' il funzionale word-decidibile **σ_D(w) = quota-shield dei passati
validi di profondita' D** che SPACCA la classe in due sottopopolazioni
(bimodale: q25 0.0002 / med 0.10 / q75 0.90 a D=22) — **σ≈1 = parole
"sicure-dal-recente"** (ogni passato valido scuda: rigetto garantito a
profondita' dichiarata) e **σ≈0 = parole "decise-dall'antico"** (celle di R_T
irraggiungibili da QUALSIASI passato ≤D: 12/14 e 5/9 per i 2 lock a D=28) —
e i 2 lock reali NON sono estremi dentro la classe (σ_22 = 0.080 e 0.0012;
24/66 parole a σ≤0.01): **il fallimento dello scudo non ha discriminante
word-side — e' proprieta' della pre-storia antica** (conferma "fortuna"
§106-T3 e cuneo §105b). Il residuo di Link 1 ai record si restringe:
(ii) vive sulla sottoclasse σ≈0, e i suoi bit dell'OR-kernel (§107c-bis) sono
**bit ANTICHI** — decisi a distanza > D+K ≈ 129 passi (unita' = passi,
trappola nn rispettata: in epoche-record possono essere recenti, §98).

Strumenti: `alpha1/danger_geometry_census.py` (F0),
`alpha1/danger_backward_autopsy.py` (F2). Numeri:
`alpha1/danger_geometry_census.json`, `alpha1/danger_backward_autopsy_summary.json`.

## 107b.1 Il confronto a due round (metodo di sessione)

Sessione impostata con un secondo cervello Fable indipendente (2 round):
ranking finale E > A > D > C > B — (B) ricorrenza-per-misura muore per
principio sulla trappola (i); (C) accoppiamento dei kernel e' notazionale
(pigeonhole da' la ricorrenza di QUALCHE stato, non del cattivo — lezione §75);
(A) com'era enunciata e' una doppia occorrenza. (E) = autopsia all'indietro
della parola-lock, con riparazioni imposte dal round-2: polarita' (deliverable
= RIDUZIONE del residuo, parente A1 §78, non chiusura alla-U1: i 2 lock
naturali sono white-pasts realizzati a record lontani, quindi "white ⇒
seme-vicino" era gia' pre-escluso), soundness a profondita' finita
(indeciso ≠ bianco), fase-0 word-side col gate che puo' fallire.

## 107b.2 F0 — geometria word-side (danger_geometry_census)

Gate: **G0** R_T ∩ footprint = ∅ verificata per-parola con footprint
INDIPENDENTE (virtual_walk, non germ_long_run); **G1** istogramma per-record
|R_T| bit-identico a `danger_class_sizes.json` §107a; **G2** cross-macchinario
sui 2 lock: (|R_T|, onset_germe) word-side = (14, 55) e (9, 65) == lente reale
§101e (germe da griglia vera). Tutti verdi.

Fatti:
1. **theta_min e' DEGENERE.** theta(cella) = |x|+k (eta' minima della riga k
   perche' la cella sia visitabile, Lemma del Cuneo §106); theta_min(w) = 2
   per quasi ogni parola (moda > 96%), pericolosa o no: OGNI parola tiene una
   cella scudabile a |x|+k <= 4 vicino alla posa. Il vincolo di lentezza T1
   §106 e' soddisfacibile da una sola cella vicina; il Cuneo non forza MAI
   l'intero read-set vergine a livello word-side. (Il criterio G3-v1 su
   theta_min ha SPARATO SPURIO sulla distribuzione degenere — rango 0.0 da
   bisect_left sui ties, P_iid=1.0 al minimo del supporto: istanza della
   trappola (pp), il caso degenere era il segnale; riparato in-sessione.)
2. **Classe ≡ taglia ≡ direzionale ≡ transiente corto.** La coerenza laterale
   coh_traj (quota di celle di R_T con sign(x) = segno dello spostamento netto
   word-forzato del transiente) decade monotona con n: med 0.92 (n<=15) →
   0.735 (16-50) → 0.593 (51-100) → 0.535 (801+). I 2 lock: **0.93 e 1.00**
   (9/9 celle sul lato del drift). Nessuna separazione oltre-taglia possibile
   word-side: la saldatura H1↔H3 e' una ri-descrizione, non un manico
   indipendente.
3. **Shift-scan (±12):** la realizzabilita' dei tagli e' SPARSA (a molti
   record il taglio s=0 e' l'unico realizzabile nel vicinato con |R_T|
   piccolo); coerenza shift-10 cross-lock confermata word-side: LOCKA a
   s=−10 da' |R_T|=9 e LOCKB a s=+10 da' 14 (le due finestre dello stesso
   flusso locale, §101).

## 107b.3 F2 — la macchina dei prepend (danger_backward_autopsy)

Semantica (deduttiva, dal flip): per una cella di R_T (∉ footprint(w)),
il colore al record e' deciso dall'ULTIMA visita del passato esteso —
lettura bianca ⇒ lasciata NERA (shield), lettura nera ⇒ lasciata BIANCA;
la decisione e' STABILE sotto prepend piu' profondi (i prepend aggiungono
solo visite piu' vecchie). Stato incrementale O(1)/passo: (posa, heading
d'arrivo, req: cella → colore a inizio-finestra); passo indietro con vincolo
di alternanza (fresche libere, rivisite forzate) + record-compat (y>=1 nel
frame ancora — record y-min stretto). Classi al cap D: SHIELD (>=1 nera),
WHITE_ALL (tutte bianche = certificato-lock), OPEN (>=1 indecisa).

**RIPARAZIONE v1→v2 (in-sessione, da mettere a verbale):** la v1 potava il
sottoalbero alla prima decisione e riportava conteggi di FOGLIE. Misura
DISTORTA: una shield-leaf a profondita' 1 pesa ~meta' dei passati di
profondita' D ma contava 1 (LOCKA ha esattamente questa biforcazione a d=1
sulla cella R_T (−1,5)). E' il parente enumerativo delle trappole (hh)/(oo):
il conteggio era politica-pesato. La v2 estende TUTTI i passati validi al cap
e classifica AL CAP; il "binario unico §88-like" della v1 era in realta' DUE
binari paralleli (ramo shield e ramo white della biforcazione d=1), forzati
fino a prof. ~12.

Gate: **GA** lente naive indipendente (virtual_walk sull'intera parola estesa,
nessuno stato incrementale): nodi per profondita' e classi al cap bit-identici
a prof. <= 12 (lock) e <= 8 (baseline); **GB** controllo positivo: il passato
REALE di ogni episodio percorre la macchina valido a ogni profondita' e mai
shield — LOCKA decide 1 cella BIANCA a prof. 1 = esattamente la cella
consumata a eta' 102 dell'autopsia §105b (combacia); **GC** disgiunzione
R_T/footprint assertata in codice. [Pannello: lente esterna indipendente
lanciata in-sessione su LOCKA D=16 e sul claim σ=1 — esito in 107b.6.]

## 107b.4 Fatti della macchina

A D=28 (esaustivo, dichiarato; oltre = INDECISO):

| episodio | passati validi | SHIELD | WHITE_ALL | OPEN | celle irragg. |
|---|---|---|---|---|---|
| LOCKA (|R_T|=14) | 7.023 | 550 (7,8%) | **0** | 6.473 | **12/14** |
| LOCKB (|R_T|=9) | 830.581 | 1.188 (0,14%) | **0** | 829.393 | **5/9** |

1. **I bit dell'OR-kernel dei lock sono ANTICHI:** 12/14 e 5/9 celle di R_T
   sono IRRAGGIUNGIBILI da qualunque passato record-compatibile di
   profondita' <= 28 (bit [nero,bianco,indeciso] = [0,0,tutti]) ⇒ il loro
   colore al record e' deciso dal passato a distanza > 129 passi. L'unica
   cella "recente" di LOCKA e' (−1,5), letta a prof. 1 da OGNI passato
   (biforcazione: 544 la lasciano nera / 6.479 bianca — il ramo shield
   sopravvive all'indietro ~12 volte meno del ramo white); il passato reale
   dell'episodio A prese il ramo bianco (la consumo' — eta' 102, §105b).
2. **WHITE_ALL = 0 ovunque:** nessun certificato-lock a profondita' finita
   <= 28 (per lockare servono TUTTE le celle decise bianche: mai realizzato
   nell'albero). Il lock resta un evento della coda antica.
3. **Baseline ordinarie appaiate** (og minimi disponibili fra n>50 — il
   confound di taglia e' DICHIARATO, non eliminato): σ_22 = 0.16, 0.37,
   0.994, **1.000**. Le ultime due sono parole con scudo FORZATO dal passato
   recente: ogni passato valido di prof. 22 scuda ⇒ **rigetto garantito a
   ogni record reale che le presenti** (il passato reale e' uno dei passati
   enumerati) — il verso KILL della riduzione funziona e produce una classe
   di parole deduttivamente sicure alla profondita' dichiarata.

## 107b.5 Lo scan σ_D e il verdetto sulla classe

σ_D(w) su tutte le 66 parole della classe <=50 (D=22, esaustivo per parola):
distribuzione BIMODALE — min 0 / q25 0.0002 / med 0.103 / q75 0.902 / max 1.0;
24/66 a σ <= 0.01, e all'altro estremo parole a σ = 1.0 esatto (cap 2.808 e
31.856 passati, tutti shield). I 2 lock a D=22: σ = 0.080 (A) e 0.0012 (B) —
**dentro la meta' bassa, NON estremi** (anche il cap varia selvaggiamente:
1..126k passati validi — alberi all'indietro da quasi-estinti a pieni).

**Verdetto:** (ii) non ha discriminante word-side dentro la classe: decine di
parole pericolose sono "lock-capable" quanto i lock (σ≈0, celle tutte
antiche) e vengono presentate ai record, ma lo scudo antico le copre quasi
sempre (64/66 nel canonico §107a, 2 lock su 82k nella caccia §101). Il
fallimento dello scudo e' interamente una proprieta' della PRE-STORIA
(cuneo del drift §105b) — coerente con §106-T3 (0 celle garantite-vergini:
"fortuna", non velocita' forzata).

**Riduzione realizzata (forma del round-2):** al record profondo che presenta
una parola pericolosa w con σ_D(w)≈0, il verdetto = OR di <= κ bit co-moving
TUTTI decisi dal passato piu' vecchio di D+K passi. La scala §107c si
raffina: (ii) = "quei bit antichi sono tutti 0 a una presentazione
pericolosa i.o." — l'oggetto dell'attacco e' ora il DEPOSITO ANTICO nel cono
del drift, non la parola ne' il passato recente. Ai falsificatori costruibili
dell'evento ridotto si applica la piega su γ (§107b-vecchio, ora §107a.b).

## 107b.6 Pannello

- GA (lente naive interna, macchinario separato nello stesso file): verde
  bit-identico su lock e baseline.
- GB (terra: passato reale nella macchina): verde 2/2, con la cella
  consumata di §105b ritrovata alla profondita' giusta.
- Riparazioni in-sessione beccate dall'auto-scetticismo: G3-v1 spurio su
  distribuzione degenere (pp); v1 foglie-potate = misura politica-pesata
  (hh/oo). Entrambe documentate nei file.
- Lente esterna indipendente (secondo agente, macchinario riscritto da zero,
  forza bruta 2^d senza stato incrementale ne' pota, 1,7 s): LOCKA D=16 —
  nodi per profondita' 0..16 bit-identici 17/17, classi al cap {shield 1,
  white_all 0, open 17} == richeck del titolare, bit per-cella con (−1,5) =
  [1,17,0] unica cella mai indecisa: **TUTTO VERDE**; claim σ=1 (parola
  n_rt=33 og=264): enumerazione esaustiva indipendente a D=22 — cap 2.808
  IDENTICO, **shield 2.808/2.808, zero passati non-scudanti: falsificazione
  fallita, claim CONFERMATO**; celle irraggiungibili 9 == json, e la lente
  osserva che sono esattamente le 9 a x<0 (il lato sinistro del record —
  coerente col cuneo laterale). Caveat onesto della lente, a verbale: la
  convenzione temporale di onset_germe e' AMBIGUA se non dichiarata —
  onset_germe e' misurato DAL RECORD (asse assoluto = og+101); la lente
  l'ha risolta con evidenza indipendente (offset +101 verificato su 3
  parole + uguaglianza insiemistica delle 14 celle R_T di LOCKA), non
  forzando il match. Dichiarazione da propagare nei prossimi strumenti.

## 107b.7 Trappole nuove

- **(rr) le foglie di un albero potato non sono una misura** (F2 v1): se si
  pota il sottoalbero alla prima decisione, il conteggio delle foglie pesa
  ogni classe per la POLITICA di potatura, non per la massa dei passati
  (una foglia a prof. 1 = meta' dell'albero). O si estende tutto al cap e si
  classifica al cap, o si pesa ogni foglia per le sue estensioni valide.
  Istanza enumerativa di (hh)/(oo).
- (istanza di pp, non lettera nuova): un criterio di gate calcolato su una
  distribuzione DEGENERE (moda > 96%) spara spurio in entrambe le direzioni
  (rango 0 sui ties, potenze di (1−F) al minimo del supporto). Controllare
  la degenerazione PRIMA di leggere il verdetto del gate.

## 107b.8 Prossimo (§107c o §108)

1. **Profondita' minima di raggiungibilita' per cella** (per le σ≈0): a che
   D le celle antiche diventano raggiungibili? (BFS per-cella; da' il raggio
   temporale esatto del "deposito antico" richiesto allo scudo.)
2. **σ_D sul vocabolario intero** (1459 parole, D=22, ~1-2 h o motore C):
   quota di parole deduttivamente sicure (σ=1) nel vocabolario reale dei
   record — se domina, l'occorrenza (i) si restringe alla sottoclasse σ≈0
   e il suo tasso e' gia' misurato (0,2-4%/record).
3. **Il deposito antico nel cuneo:** formalizzare "lo scudo dei bit antichi"
   con il Lemma del Cono §87 (il fronte del cono passato attraversa R_T?)
   — l'attacco (ii) al livello giusto (pre-storia, non parola).
4. F1 ereditata (gamba-Cuneo sui 1639 stratificata per dt) — non eseguita
   in sessione, dichiarata.
5. Ereditati: §106c, §105b.4, §101g, §102f, §103d, §104f.

## 107b.9 Inventario file

- `alpha1/danger_geometry_census.py` + `danger_geometry_census.json` (F0:
  gate G0-G3, per_word 1459+2, shift_scan 68 record, gradiente di taglia).
- `alpha1/danger_backward_autopsy.py` + `danger_backward_autopsy_summary.json`
  (F2 v2: macchina incrementale + lente naive GA + GB passato reale +
  baseline 4 + scan_danger 66 parole).
- `alpha1/locka_d16_check.json` (confronto D=16 per la lente esterna).
