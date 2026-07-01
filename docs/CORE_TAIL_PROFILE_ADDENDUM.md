# ADDENDUM CORE-TAIL-PROFILE — La coda lunga NON vive fuori dal vocabolario: l'invariante 35,6% e' omogeneo (§82)

Catena addenda: ... CONSUMPTION-LEDGER §79, DEEP-MOTIF-SATURATION §80, DEEP-MOTIF-PRUNED §81,
**CORE-TAIL-PROFILE §82**.

Bersaglio di sessione (roadmap §81.5.1–2): dove vive la coda lunga delle eta' (la leva di §79)?
Profilo della massa sul nucleo-24 (i 1.572 motivi universali di §81) incrociato con ETA' dell'evento
(t − ultima visita) e ALIMENTAZIONE (vc==1 morso-fed / resto recycle-fed, definizione §79 riusata
verbatim da `consumption_ledger_probe.py`). Ipotesi da attaccare: la coda lunga e' sistematicamente
fuori dal vocabolario, e il nucleo coincide con la meccanica del riciclo.

> **NOTA DI STATO: run REALE** sulle 24 orbite (da `dumps_all.txt`), ambiente Claude-container
> (1 core, 103 s). Doppio gate di validazione, entrambi VERDI: (1) nev per orbita esatti vs §80
> 24/24; (2) nucleo ricostruito = **1.572** motivi con massa mediana **identica a §81** (uguaglianza
> alla precisione macchina, pipeline deterministica). Strumento: `alpha1/core_tail_profile.py`
> (streaming su file eventi binari per contenere la memoria); output
> `alpha1/core_tail_profile_summary.json` + `alpha1/core24_motifs.json`.

## 82. Riepilogo in una frase
**Entrambe le ipotesi sono falsificate**: la massa sul nucleo e' **35–36% a ogni eta'** (36,2 / 35,2 /
35,6 / 35,7 / 35,2% sui bucket ≤104 / ≤1040 / ≤10400 / ≤104000 / oltre) — la coda lunga parla il
dialetto universale esattamente quanto gli eventi giovani — ed e' **trasversale all'alimentazione**
(morso-fed 36,9% vs recycle 35,4%). L'invariante 35,6% di §81 e' **omogeneo**: costante tra orbite,
nel tempo, per eta' e per alimentazione. La parte aperiodica NON e' una sottopopolazione separabile.

## 82.1 Risultato (24 orbite, p104 r=3, mediane tra orbite [min, max])
**A. Massa nucleo per bucket di eta'** (quota eventi del bucket):
| bucket eta' | quota eventi | massa-nucleo |
|---|---:|---:|
| ≤104 | 12,00% | 36,17% [34,29–37,89] |
| 105–1040 | 25,41% | 35,24% [33,50–36,89] |
| 1041–10400 | 27,44% | 35,63% [34,47–37,27] |
| 10401–104000 | 33,95% | 35,71% [34,08–37,19] |
| >104000 | 1,03% | 35,16% [29,84–41,89] |

**B. Massa nucleo per alimentazione (§79)**:
| classe | quota eventi | massa-nucleo |
|---|---:|---:|
| vc==1 (morso-fed) | 9,97% | 36,92% [34,97–39,24] |
| vc==2 | 0,09% | 34,40% (popolazione esigua) |
| vc≥3 (recycle-fed) | 89,89% | 35,40% [34,21–36,06] |

**C. Interazione**: unica cella non piatta = giovani (≤104) morso-fed a **42,95%**, con decadimento
monotono 42,95 → 37,71 → 35,58 → 35,71 → 35,28 lungo l'eta'; tutto il resto e' 33–36%.

**Contesto**: sulle orbite convergenti il recycle-fed domina all'**89,9%** (vs 61,7% sul transiente
(7,−7) di §79): l'economia deep-black matura e' ancora piu' auto-alimentata.

**Il nucleo in chiaro** (`core24_motifs.json`, 1.572 motivi ordinati per massa): eventi coperti pooled
541.797 (35,89% del totale); massa interna concentrata (top-10 = 12,4%, top-100 = 41,3%, top-500 =
74,2% del nucleo); taglie med 6, min 1, max 12 (piu' piccoli e semplici della popolazione generale,
med 7 max ~30). I motivi di testa sono **catene lineari/diagonali di 3 celle** giacenti sul cammino
imminente nel frame normalizzato (es. {(−3,−3),(−2,−2),(−1,−1)} anti-diagonale perfetta;
{(−3,0),(−2,0),(−1,0)} retta): firma "segmento di cammino quasi-periodico", come congetturato in
§81.5.3 — da verificare contro le parole W0-like in §83.

## 82.2 Interpretazione
- **La leva sperata e' morta.** L'idea "isolare la regione genuinamente aperiodica separando la coda
  lunga dal vocabolario" non funziona: la miscela nucleo/coda e' **invariante di scala** rispetto al
  tempo di ritorno. Qualunque argomento dinamico per Link 1 non puo' segmentare gli eventi deep-black
  per eta', alimentazione o membership al vocabolario: in questa decomposizione la dinamica e' omogenea.
- **L'omogeneita' e' essa stessa il fatto nuovo.** Un terzo (35,6%) della massa degli eventi profondi
  cade su un vocabolario finito FISSO, in ogni orbita, in ogni epoca, a ogni eta', per ogni sorgente.
  Ha il sapore di una proprieta' ergodica/di misura della dinamica deep-black — un'impronta
  quantitativa stabile del "linguaggio attivo" del detrito — non di un meccanismo locale isolabile.
- **Il nucleo e' geometricamente strutturato** (catene corte sul cammino): coerente con
  rigenerazione dominantemente locale (§79) e con la diluizione a orizzonte doppio (§81, H=208).
- **Cosa NON dice.** Nulla sull'eterno (trappola i). L'omogeneita' e' misurata su 24 orbite
  convergenti; su orbite eterne ipotetiche resta controfattuale.

## 82.3 Caveat
- Il bucket >104000 ha popolazione esigua (~1%): la banda [29,8–41,9] e' larga per taglia campione,
  la mediana resta al 35%.
- vc==2 e' quasi vuoto (0,09%): coerente con la parita' colore/visita (cella d'origine bianca ⇒ nero
  letto a visite dispari); il residuo viene dalle celle-seme nere.
- L'arricchimento giovani-morso-fed (42,9%) e' reale ma piccolo e monotono-decadente: non un manico,
  una nota di colore compatibile con "il morso fresco innesca vicino al vocabolario" (§60: bite e'
  l'innesco).

## 82.4 Trappola nuova
- **(q) il taglio nucleo/coda non segmenta la dinamica.** La massa sul vocabolario universale e'
  invariante nel tempo (§81), per eta' e per alimentazione (§82): NON cercare la parte genuinamente
  aperiodica come sottopopolazione separabile di eventi (per eta', vc, o membership). La miscela e'
  omogenea; l'aperiodicita' vive dentro la stessa popolazione che parla il dialetto universale.

## 82.5 Roadmap
1. **§83 (interpretabilita' del nucleo)**: confrontare i 1.572 motivi (gia' in chiaro in
   `core24_motifs.json`) con le parole locali della highway/W0: il vocabolario universale e' il
   linguaggio quasi-periodico "di transito"? Se si', l'invariante 35,6% direbbe: *ogni* orbita
   convergente spende un terzo del suo traffico profondo in modalita' quasi-highway — un ponte
   quantitativo naturale (e finito!) verso il lato-beta.
2. Kill-gate §79.1 (deep-black-anchored decisive-depth sweep) resta in coda come gate negativo.
3. (Certificazione) ri-run Ryzen `--workers 16` di §81+§82 per omogeneita' della catena.

## 82.6 Inventario file
- `alpha1/core_tail_profile.py` (sonda §82: profilo eta'×alimentazione×nucleo, doppio gate §80/§81,
  streaming binario anti-OOM; `--orbits`, `--workers`, `--out`, `--motifs-out`)
- `alpha1/core_tail_profile_summary.json` (profili A/B/C + gate)
- `alpha1/core24_motifs.json` (i 1.572 motivi del nucleo in chiaro, ordinati per massa)

## 82.7 Frase di stato dell'arte
*Cercavamo la regione dove il detrito e' davvero aperiodico e abbiamo trovato che non e' una regione:
a ogni eta', a ogni epoca, da ogni sorgente, il traffico profondo parla per un terzo esatto un
dialetto fisso di millecinquecento parole — catene corte stese sul cammino che verra' — e per due
terzi una lingua sempre nuova. L'aperiodicita' non si lascia isolare; abita la stessa popolazione.
Resta in mano l'invariante piu' pulito visto finora sul lato-alpha: se quelle parole sono, come
sembrano, i segmenti quasi-periodici del transito, il 35,6% e' il primo ponte quantitativo finito
tra il caos del detrito e la porta.*
