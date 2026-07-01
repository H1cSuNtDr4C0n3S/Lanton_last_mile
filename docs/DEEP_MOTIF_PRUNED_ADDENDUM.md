# ADDENDUM DEEP-MOTIF-PRUNED — Il motivo potato: caveat §80.3 chiuso, e il vocabolario universale del detrito attivo (§81)

Catena addenda: ... GATE-ONE-COMOVING §78, CONSUMPTION-LEDGER §79, DEEP-MOTIF-SATURATION §80,
**DEEP-MOTIF-PRUNED §81**.

Bersaglio di sessione: chiudere il caveat §80.3 — il motivo co-moving pieno include detrito morto
(alta entropia), quindi l'unicita' per-evento era in parte attesa. Il test giusto pota il motivo alla
parte **causalmente attiva**: le sole celle nere (entro raggio r, normalizzazione C4 identica a §80)
che la formica visita/legge nei successivi H passi (H=104 e 208, cioe' 1 e 2 periodi W0).

> **NOTA DI STATO: run REALE** sulle 24 orbite lunghe vere (da `dumps_all.txt`), ambiente
> Claude-container (1 core, 381 s sequenziale). La catena di validazione e' pero' completa: self-test
> §5 tutti verdi (window r1/r2, prodotto 4/4, motore vuota→9977 e (7,−7)→106258), e la modalita' FULL
> calcolata nella stessa passata riproduce **esattamente** i numeri certificati Ryzen di §80 su
> **24/24 orbite** (nev, distinct r=3/4/5, pooled 1.509.525 / 1.478.021 / 19 / 0,979), con **zero**
> violazioni delle inclusioni pruned104 ⊆ pruned208 ⊆ full. Ri-esecuzione su Ryzen (1 comando,
> `--workers 16`, ~1 min) raccomandata solo per omogeneita' della catena di certificazione.
> Strumento: `alpha1/deep_motif_pruned.py`; output `alpha1/deep_motif_pruned_summary.json`.
> **CERTIFICATO Ryzen 2026-07-02**: ri-run 16 core, 37,0 s, output integralmente
> identico al run container (validazione 24/24, 0 violazioni, tutti i pooled e le masse).

## 81. Riepilogo in una frase
Il caveat e' **chiuso nella direzione attesa** — anche potato alla parte causalmente attiva l'alfabeto
**non satura** (scoperta ultimo20%/primo20% mediana 0,811; ~57% eventi con motivo unico; unione che
cresce con le orbite) e la trappola (o) si estende al motivo potato — **ma** la potatura rivela cio' che
l'entropia del detrito morto mascherava: un **vocabolario universale finito** di 1.572 motivi presenti
in *tutte* le 24 orbite che porta una **massa stazionaria di eventi ~35,6%** (banda tra orbite
[34,4–36,3], piatta nel tempo within-orbit, ortogonale all'eta' dell'evento). Il detrito attivo =
vocabolario finito a massa Θ(1) + coda aperiodica illimitata.

## 81.1 Risultato (24 orbite, onset 251k–313k, r=3 salvo nota)
| metrica | full (§80) | potato H=104 | potato H=208 |
|---|---:|---:|---:|
| motivi distinti / eventi (orbita 0) | 73.959 / 74.416 (~99,4%) | 42.722 (~57%) | 49.834 (~67%) |
| scoperta ultimo20%/primo20% (mediana) | 1,14 | **0,811** | — |
| pooled: union/sum | 0,979 | **0,650** | 0,732 |
| pooled: intersezione 24 orbite | 19 | **1.572** (~83×) | 1.242 |
| massa eventi su nucleo-24 (mediana orbite) | — | **35,63%** [34,40–36,33] | 27,22% [25,88–28,37] |
| massa su nucleo-maggioranza (≥12 orbite) | — | 49,15% (7.849 motivi) | 39,07% (6.695 motivi) |
| taglia motivo (med / p90 / max / vuoti) | — | 7 / 13–14 / ~30 / **0,00%** | — |
| stazionarieta' within-orbit (quintili Q1..Q5) | — | 35,26 / 35,69 / 35,68 / 35,41 / 35,95 % | — |
| eta' media evento nucleo vs fuori-nucleo | — | 14.014 vs 14.045 (indistinguibili) | — |

## 81.2 Interpretazione
- **Verdetto primario (il bersaglio): caveat §80.3 chiuso.** Nessuna saturazione nemmeno sulla parte
  causalmente attiva: la scoperta di nuovi motivi resta ~0,8 (lontana da 0), i distinti crescono con
  l'onset, l'unione cresce con le orbite. **Nessun classificatore finito-stato a raggio fisso cattura
  gli eventi deep-black neppure ristretto al motivo attivo.** §80 confermato; trappola (o) estesa.
- **I motivi potati non sono vacui**: mediana 7 celle, zero vuoti. (Nota a margine: ogni evento
  deep-black ha almeno una cella nera attiva entro r=3 visitata nei 104 passi successivi.)
- **Scoperta secondaria (non pianificata): il vocabolario universale.** La quasi-disgiunzione di §80
  (union/sum 0,979, intersezione 19) era in parte sostanziale artefatto entropico del detrito morto:
  potando alle celle attive, union/sum crolla a 0,650 e l'intersezione a 24 orbite sale ~83× (1.572
  motivi). Quei 1.572 motivi portano il **35,6% della massa di eventi**, con tre proprieta' forti:
  (i) banda strettissima tra 24 orbite indipendenti (±1%); (ii) **stazionaria nel tempo** within-orbit
  (quintili piatti ⇒ non e' survivorship (h) ne' transiente); (iii) **ortogonale all'eta'** (media
  14.014 vs 14.045 ⇒ il nucleo NON e' "gli eventi giovani del riciclo": permea tutte le eta').
- **Lettura strutturale.** Il lato-alpha attivo si decompone in: *vocabolario ricorrente universale*
  (finito, condiviso, massa Θ(1) stazionaria) + *coda aperiodica* (illimitata, ~64% della massa, quasi
  tutta localmente unica). E' la coda a rendere l'alfabeto illimitato; e' il nucleo a essere un
  invariante quantitativo nuovo della dinamica deep-black. Coerente col quadro §79 (rigenerazione
  dominantemente locale + coda lunga come ostruzione) e con la diluizione a orizzonte doppio
  (H=208: nucleo piu' piccolo e piu' leggero, 27,2% ⇒ l'universalita' vive sull'interazione a 1 periodo).
- **Cosa NON dice.** Nulla sull'eterno (trappola i). Il nucleo da solo non e' un manico per Link 1:
  la parte illimitata porta ~2/3 della massa. E l'ortogonalita' all'eta' uccide la lettura ingenua
  "nucleo = macchina del riciclo giovane".

## 81.3 Caveat
- L'eta' confrontata e' la **media**; la sotto-popolazione a coda lunga (age ≫ periodo, la leva §79)
  potrebbe ancora usare il nucleo in proporzione diversa. Test dedicato in roadmap (81.5.2).
- Il motivo potato vive per costruzione sul cammino futuro ∩ box 7×7: una parte di condivisione tra
  orbite e' combinatoriamente attesa. Ma la *concentrazione di massa* (35,6% su 1.572 motivi contro
  ~578k) e la sua strettezza/stazionarieta' non lo sono, e i ~40k distinti per orbita mostrano che lo
  spazio e' lontano dall'esaurimento.
- Una sola passata, 24 orbite finite convergenti (§1-i): non decide l'eterno.
- Ambiente container, non Ryzen; mitigato dalla riproduzione esatta 24/24 dei numeri §80 in full-mode.

## 81.4 Trappola nuova
- **(p) il nucleo universale non e' un manico.** Non costruire argomenti finito-stato sul nucleo-24
  sperando che la coda sia trascurabile: la coda porta ~64% della massa ed e' esattamente la parte
  illimitata (trappola o). Il nucleo e' un *vincolo/impronta* che ogni argomento dinamico deve
  rispettare (massa stazionaria Θ(1) su vocabolario finito), non una riduzione.

## 81.5 Roadmap
1. **Cross §79**: correlare membership nucleo/coda con recycle-fed vs morso-fed (vc del ledger §79):
   il vocabolario universale coincide con la meccanica del riciclo locale?
2. **Coda lunga**: restringere l'analisi eta' agli eventi age>1040 e age>10·104 — se la coda lunga
   vive sistematicamente FUORI dal nucleo, isola la parte genuinamente aperiodica dove deve vivere
   l'argomento dinamico di Link 1.
3. **Interpretabilita' del nucleo**: dump dei 1.572 motivi (taglie, geometrie, prossimita' a parole
   W0-like): sono segmenti di cammino quasi-periodici? Collegamento naturale all'impronta spettrale.
4. (Certificazione) ri-run su Ryzen `--workers 16` per omogeneita' della catena.

## 81.6 Inventario file
- `alpha1/deep_motif_pruned.py` (sonda §81: full+p104+p208 in una passata, validazione §80 integrata,
  massa nuclei, stazionarieta' per quintile, eta' core/coda; `--orbits`, `--workers`, `--out`)
- `alpha1/deep_motif_pruned_summary.json` (per-orbita + event_mass + flag validazione)

## 81.7 Frase di stato dell'arte
*Potato alla parte causalmente attiva, il detrito resta senza automa finito: il caveat di §80 e' chiuso
e la trappola (o) tiene anche sul motivo attivo. Ma sotto l'entropia c'era una firma: un vocabolario di
1.572 configurazioni attive condiviso da tutte le orbite, che porta un terzo esatto e stazionario della
massa degli eventi profondi, a ogni eta'. Il lato-alpha non e' riducibile a stati finiti — pero' adesso
sappiamo che ogni argomento dinamico per Link 1 deve attraversare una dinamica che parla per due terzi
una lingua sempre nuova e per un terzo un dialetto fisso e universale.*
