# ADDENDUM §105b — IL MECCANISMO DEI BUCHI: read-set piccolo nel cuneo vergine del drift

**Riepilogo in una frase:** autopsia comparata dei 2 episodi-lock §101 contro
controlli same-seed (record vicini, parole lente), col macchinario indipendente
§101e: il lock ai record accade quando **(H3) la parola-porta ha un transiente a
read-set MINUSCOLO** (9 e 14 celle, contro 454 e 931 dei controlli) **e (H1) il
read-set giace nel CUNEO VERGINE aperto dal drift laterale della discesa**
(drift_x = −6 negli ultimi 10 record in ENTRAMBI gli episodi; read-set tutto a
x<=0; celle mai-visitate 9/9 e 13/14) — con **(H2) contributo del consumo a
catena**: l'unica cella visitata del read-set dell'episodio A era stata RIPULITA
102 passi prima (= il consumo del tentativo del record precedente, Lemma 3 §101:
i rigetti shallow sabotano lo scudo dei tentativi successivi); i controlli hanno
130/288 NERE nel read-set e la scalinata a distanza 0. FALSIFICATO invece il
"filo del rasoio" della scalinata: le colpevoli di divergenza dei rigetti shallow
sono pose-record vecchie solo nel **10%** dei casi (44% entro cheb 1, campione
120) — lo scudo e' alimentato dal detrito generale delle escursioni (q med 9,
§98), non solo dalla scalinata: e' SPESSO, ed e' per questo che i lock sono rari
(2 episodi / 82k record).

Strumento: `alpha1/lock_hole_autopsy.py` (+`_summary.json`, `.log`); sonda
scalinata-vs-colpevoli in sessione (120 record, numeri qui).

## 105b.1 Numeri (episodi vs controlli, macchinario lente §101e)

| | read-set (celle) | bbox x / y_rel | nere | mai-visitate | scalinata dmin | drift_x (10 rec) |
|---|---|---|---|---|---|---|
| LOCK A t=4588 (onset 55) | **14** | [−6,0] / [1,6] | 0 | 13 (+1 ripulita 102 passi prima) | 8 | **−6** |
| LOCK B t=18142 (onset 65) | **9** | [−7,−1] / [1,5] | 0 | 9 | 11 | **−6** |
| controllo t=4398 (onset 4512) | 454 | [−14,18] / [1,21] | 130 | 198 | **0** | 0 |
| controllo t=17908 (onset 18417) | 931 | [−22,22] / [1,30] | 288 | 321 | **0** | +6 |

Coerenza interna: read-set degli episodi interamente bianco ⟺ classe R (§101,
per definizione di divergenza); controlli sporchi ⟺ classe T.

## 105b.2 Il quadro per l'attacco §105.2 (endgame di Link 1)

- **Lock al record ⟺ congiunzione:** (parola con read-set del transiente piccolo
  — proprieta' word-intrinseca, la classe veloce/porta-0) ∧ (read-set dentro il
  cuneo vergine del drift laterale). La scalinata NON difende li': sta nel cono
  visitato, il cuneo vergine e' strutturalmente fuori dalla sua portata.
- **Lo scudo e' spesso** (negativo onesto): il rifornimento delle palle vicine e'
  detrito generale di escursione (90% delle colpevoli di divergenza NON e'
  scalinata), quindi niente ledger ±1 a filo di rasoio; il nemico shallow-forever
  ha risorse abbondanti nel cono visitato.
- **Ma il nemico ha due obblighi permanenti misurabili:** (1) ogni rigetto
  CONSUMA una colpevole (Lemma 3, deduttivo) e il consumo puo' incatenarsi
  (episodio A); (2) per evitare i lock deve evitare PER SEMPRE la congiunzione
  sopra — dove il primo congiunto e' un predicato di parola (enumerabile:
  read-set size del germe, gia' calcolabile con la Lingua §104c) e il secondo un
  predicato geometrico della propria discesa (drift). La forma finale del
  problema: **puo' un'orbita eterna scegliere per sempre le proprie svolte in
  modo che ogni parola veloce presentata ai record guardi nel cono visitato?**
  — un enunciato di evitamento su oggetti FINITI (read-set delle parole veloci),
  parente della vietanza del Muro ma in direzione duale.

## 105b.3 Onesta' e pannello

Verbale-sonda: misure fatte col macchinario gia' indipendente e validato
(run_real / germ_turns_from_real, 40/40+11/11 §101e, 30/30+20/20 §104h);
coerenza interna episodi/controlli come sopra; campione scalinata n=120 con
seed dichiarato (rng 1057). Nessuna soglia nuova enunciata (i conteggi 9/14/454/
931 sono descrittivi dei 4 casi; il 10%/44% e' una quota campionaria).
Debito residuo: nessuno sul blocco §101-105 (pannelli §101e, §104h; §105b usa
solo strumenti gia' pannellati).

## 105b.4 Prossimo (§106)

1. **Predicato read-set-size:** calcolare |read-set(w)| per le 1459 parole dei
   record canonici e per la classe veloce: la soglia dei buchi e' word-decidibile
   (niente quantili: distribuzione completa a verbale).
2. **Geometria del cuneo:** formalizzare "read-set ⊆ cuneo vergine" col cono di
   §87 (Lemma del Cono) — candidato lemma: a un record y-min stretto, le celle a
   y_rel>=1 mai-visitate stanno oltre il fronte del cono passato; il lock e'
   possibile sse il read-set attraversa il fronte.
3. L'enunciato di evitamento duale (105b.2) come nuovo bersaglio della scala a
   Link 1; ereditati §101g/§102f/§103d/§104f.

## 105b.5 Inventario file (alpha1/)

- `lock_hole_autopsy.py` (+`_summary.json`, `.log`) — autopsia episodi vs
  controlli: read-set, colori, scalinata, drift.
