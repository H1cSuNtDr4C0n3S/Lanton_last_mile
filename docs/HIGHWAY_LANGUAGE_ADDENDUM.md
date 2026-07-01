# ADDENDUM HIGHWAY-LANGUAGE — Il nucleo NON e' linguaggio di transito: caos e highway sono linguisticamente disgiunti (§83)

Catena addenda: ... DEEP-MOTIF-SATURATION §80, DEEP-MOTIF-PRUNED §81, CORE-TAIL-PROFILE §82,
**HIGHWAY-LANGUAGE §83**.

Bersaglio di sessione (roadmap §82.5.1): i 1.572 motivi del vocabolario universale sono il linguaggio
quasi-periodico "di transito"? I motivi di testa (catene di 3 celle sul cammino imminente) lo
suggerivano a occhio. Ipotesi da attaccare: nucleo ≈ parole locali della highway.

**Decisione di design** (documentata): la highway in territorio vergine non rivisita territorio
dimenticato ⇒ (quasi certamente) niente eventi deep-black post-onset. L'analogo equo e'
**L_hw = linguaggio locale potato delle letture nere sulla highway pura**: post-onset (assestamento
2·104, raccolta 20 periodi), a OGNI lettura nera, motivo p104 r=3 con pipeline IDENTICA a §81/§82
(potatura alle celle visitate nei 104 passi successivi, normalizzazione C4, centro escluso).

> **NOTA DI STATO: run REALE** sulle 24 orbite (da `dumps_all.txt`), ambiente Claude-container
> (1 core, 125 s). Tre gate, tutti VERDI: (1) nev pre-onset esatti vs §80 24/24 (gli eventi
> pre-onset risolvono con tcap=onset, identico a §81/§82); (2) nucleo ricostruito = 1.572 con massa
> mediana identica a §81 a precisione macchina; (3) L_hw SATURA (taglia a 10 periodi == a 20).
> Strumento: `alpha1/highway_language_probe.py`; output `alpha1/highway_language_summary.json`.
> Ri-run Ryzen: `python alpha1\highway_language_probe.py --workers 16`.

## 83. Riepilogo in una frase
**Ipotesi falsificata, nettamente**: L_hw ha esattamente **46 parole** (= le 46 letture nere di W0,
104−58R), satura al periodo ed e' **identico su tutte le 24 orbite**, ma la sovrapposizione col
nucleo e' **2/1.572 motivi** (0,1%), la massa del traffico deep-black pre-onset su L_hw e'
**0,05%** [0,01–0,42] e **nessuno** dei top-20 motivi del nucleo e' linguaggio-highway: a raggio 3 e
orizzonte 104, il linguaggio del caos profondo e quello del transito sono **disgiunti**.

## 83.1 Risultato (24 orbite)
| metrica | valore |
|---|---:|
| \|L_hw\| per orbita | 46 = 46 [min=max], **= n. letture nere di W0** |
| saturazione (10 vs 20 periodi) | esatta, 24/24 (GATE 3) |
| L_hw tra orbite | unione 46 = intersezione 46 (**identico**, quoziente C4 perfetto) |
| \|L_hw ∩ nucleo-24\| | **2** (4,3% di L_hw; 0,1% del nucleo) |
| massa deep-black pre-onset su L_hw | **0,05%** med [0,01–0,42] |
| massa su L_hw ∩ nucleo | 0,02% [0,01–0,06] |
| massa su nucleo (riferimento §81) | 35,63% [34,40–36,33] |
| top-20 motivi del nucleo in L_hw | **0/20** |

Consistenza interna notevole: 46 motivi distinti = una parola per fase di lettura nera del periodo,
nessuna collisione, stabile su 20 periodi e su 24 istanze indipendenti della highway — L_hw e' un
oggetto esatto, non una stima.

## 83.2 Interpretazione
- **Il ponte vocabolario α→β e' morto.** L'idea (promossa in §82.5.1) che il 35,6% fosse "un terzo
  del traffico speso in modalita' quasi-highway" e' falsa: il caos profondo parla highway-language
  in 5 eventi su 10.000. Il vocabolario universale e' un invariante **genuinamente caotico**,
  intrinseco al regime pre-onset, non un'eco del transito.
- **Affilatura linguistica di §59.** Il ponte diretto deep-black→lock era gia' anti-correlato nel
  predittore; ora sappiamo che anche a livello di configurazione locale attiva i due regimi sono
  (quasi) disgiunti a (r=3, H=104). Coerente e piu' forte.
- **Le catene di §82 non sono parole W0.** L'occhio vedeva "segmenti quasi-periodici"; il numero
  dice che la geometria delle catene del nucleo e' diversa da quella delle 46 parole della highway.
  Candidato successivo naturale: i **rotori espliciti** della finestra (le parole cicliche B-T
  gia' censite: LLRRRR p6, LLRRRRLLRRRR p12, ecc. in `radius*_cycles.txt`) — il nucleo potrebbe
  essere il linguaggio delle *cavalcate di rotore* (§77 collega gli stalli al rotor-router walk).
- **Cosa NON dice.** Nulla sull'eterno (trappola i). E la disgiunzione e' misurata sul confronto
  deep-black(caos) vs tutte-le-nere(highway) a scala (r=3, H=104): non esclude parentele a raggio
  o orizzonte diversi.

## 83.3 Caveat
- Le popolazioni anchor differiscono per la condizione di finestra (deep vs tutte le letture nere):
  equo per l'ipotesi testata (il nucleo E' deep), ma un confronto "nere non-deep del caos vs L_hw"
  resta non misurato.
- La banda alta della massa su L_hw (0,42% su un'orbita) resta due ordini sotto il nucleo; nessuna
  orbita si avvicina a una parentela.
- L_hw dipende dalla potatura H=104 esattamente come il nucleo: il confronto e' alla stessa scala
  per costruzione.

## 83.4 Trappola nuova
- **(r) il nucleo non e' linguaggio di transito.** Non costruire ponti α→β su sovrapposizioni di
  vocabolario locale: a (r=3, H=104) il linguaggio deep-black e L_hw (46 parole esatte di W0) sono
  disgiunti (2/1.572 motivi, massa 0,05%). Il vocabolario universale e' un fatto del caos, non
  dell'autostrada.

## 83.5 Roadmap
1. **§84 (rotori)**: confrontare il nucleo con il linguaggio delle cavalcate di rotore (parole
   cicliche B-T di `radius1/2/3_cycles.txt`, es. LLRRRR p6): stessa pipeline di L_hw su orbite
   sintetiche di rotore, oppure proiezione dei motivi del nucleo sui pattern di svolta locali.
   E' l'ultima famiglia quasi-periodica esplicita disponibile; se anche questa e' disgiunta, il
   nucleo e' un oggetto nuovo senza antenati periodici noti.
2. Kill-gate §79.1 (deep-black-anchored decisive-depth sweep) resta in coda come gate negativo.
3. (Certificazione) ri-run Ryzen di §83.

## 83.6 Inventario file
- `alpha1/highway_language_probe.py` (sonda §83: L_hw post-onset + massa pre-onset, tre gate;
  `--orbits`, `--workers`, `--out`)
- `alpha1/highway_language_summary.json`

## 83.7 Frase di stato dell'arte
*Le millecinquecento parole universali del caos non sono l'eco dell'autostrada: la highway ha
esattamente quarantasei parole, sempre le stesse su ogni orbita, e il traffico profondo non ne
pronuncia quasi mai nessuna. Due linguaggi disgiunti sullo stesso reticolo — il transito parla la
sua liturgia periodica, il detrito parla per un terzo un dialetto fisso che non viene da lei.
L'invariante 35,6% e' del caos e soltanto del caos; se ha antenati, vanno cercati nei rotori.*
