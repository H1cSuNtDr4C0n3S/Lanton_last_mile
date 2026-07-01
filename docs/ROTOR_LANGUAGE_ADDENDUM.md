# ADDENDUM ROTOR-LANGUAGE — Nemmeno i rotori: il nucleo non ha antenati periodici noti, e le prime crepe nell'omogeneita' (§84)

Catena addenda: ... DEEP-MOTIF-PRUNED §81, CORE-TAIL-PROFILE §82, HIGHWAY-LANGUAGE §83,
**ROTOR-LANGUAGE §84**.

Bersaglio di sessione (roadmap §83.5.1): dopo la disgiunzione dalla highway, i rotori espliciti B-T
del censimento finestra (`radius1..4_cycles.txt`) sono l'ultima famiglia quasi-periodica nota.
Ipotesi da attaccare: il nucleo-24 e' il linguaggio delle cavalcate di rotore.

**Metodo** (con due correzioni metodologiche imposte dallo smoke test, documentate):
per ogni evento deep-black, la parola di svolta futura viene confrontata con le parole PRIMITIVE
del censimento — LRRRR(p5, r1), LLRRRR(p6, r2), LLRRLLRRRR(p10, r4), LLLLRLRRRRLRRRR(p15, r2/r3),
P74(r4); le doppie si riducono — su **3 periodi pieni** (2 periodi sono statisticamente banali per
p piccole: q=2 matcha per caso 1/4), match a meno di rotazione (trappola d); controllo periodicita'
generica q≤15; e **baseline nulla empirica condizionata**: stesso classificatore su ancore
pseudo-casuali del flusso reale ristrette alle letture nere (gli eventi leggono sempre nero: senza
condizionamento la baseline di parole sbilanciate come LRRRR e' distorta). L'eccesso sopra il caso
e' misurato, non presunto. Incrocio col nucleo in streaming binario (§82).

> **NOTA DI STATO: run REALE** sulle 24 orbite (da `dumps_all.txt`), ambiente Claude-container
> (1 core, 132 s). Gate VERDI: (1) nev esatti vs §80 24/24; (2) nucleo ricostruito = 1.572, massa
> mediana identica a §81 a precisione macchina. Strumento: `alpha1/rotor_language_profile.py`;
> output `alpha1/rotor_language_summary.json`.
> Ri-run Ryzen: `python alpha1\rotor_language_profile.py --workers 16`.

## 84. Riepilogo in una frase
**Ipotesi falsificata** — terza famiglia periodica consecutiva: solo il **4,5%** degli eventi-nucleo
siede su una qualunque cavalcata, i rotori r≥2 sono **assenti dal caos persino alla baseline**,
LRRRR (r=1) e' **evitato totalmente** (0 eventi su 24 orbite vs ~0,18% di caso), e l'unica cavalcata
sopra il caso (p15, ×1,9) ha **massa-nucleo 0,00%** su tutte le orbite — la prima sottopopolazione
che rompe l'omogeneita' (q): le cavalcate p15 vivono interamente nella coda aperiodica.

## 84.1 Risultato (24 orbite, 3 periodi, baseline nulla condizionata a lettura nera)
| classe | quota eventi | baseline nulla | eccesso | massa-nucleo |
|---|---:|---:|---:|---:|
| nessuna | 96,50% | 95,52% | ×1,0 | 35,19% [33,97–35,86] |
| LRRRR (p5, r1) | **0,0000%** | 0,1808% | **0 (evitamento totale)** | — |
| LLRRRR (p6, r2) | 0,0000% | 0,0000% | assente dal caos | — |
| LLRRLLRRRR (p10, r4) | 0,0000% | 0,0000% | assente dal caos | — |
| LLLLRLRRRRLRRRR (p15) | 0,0194% | 0,0103% | **×1,9** | **0,00% [0,00–0,00]** |
| P74 (r4) | 0,0000% | 0,0000% | assente dal caos | — |
| periodica generica q≤15 | 3,47% | 4,30% | ×0,8 (deficit) | **47,11%** [43,80–50,66] |
| TUTTE (rif. §81) | 100% | — | — | 35,63% [34,40–36,33] |

Quota degli eventi-nucleo su una qualunque cavalcata: **4,55%** [4,22–5,06].

## 84.2 Interpretazione
- **Il nucleo non ha antenati periodici noti.** Highway (§83, 46 parole, massa 0,05%), rotori (§84,
  4,5% degli eventi-nucleo, e la sola classe in eccesso a massa-nucleo nulla): il vocabolario
  universale corrisponde a parole di svolta **non periodiche**. E' un oggetto del caos, punto.
- **Prime crepe nell'omogeneita' (q).** Eta' e alimentazione non segmentavano (§82); la
  periodicita' di svolta SI', debolmente ma nettamente: p15-rides = massa-nucleo 0% esatto
  (24/24 orbite), generica-periodica = 47,1% (sopra il 35,6%). La trappola (q) va quindi
  DELIMITATA: vale per eta'/vc, non per gli assi di periodicita' della svolta. Le classi sono
  pero' minuscole (0,02% e 3,5%): segmentano concettualmente, non quantitativamente.
- **Evitamento totale di LRRRR.** Non ridotto: zero su ~1,5M eventi, contro ~110/orbita attesi.
  Enunciato in forma "ogni evento deep-black NON inizia una cavalcata LRRRR di 3 periodi" — e'
  un enunciato universale, quindi **candidato a teorema via automa prodotto** (trappola-c
  compliant: i "per ogni cammino" trasferiscono). Se dimostrato, sarebbe il primo teorema
  esatto sul lato-alpha ottenuto DAL vocabolario.
- **Assenza dei rotori r≥2 dal caos.** Le lingue LLRRRR/LLRRLLRRRR/P74 non compaiono nemmeno ad
  ancore casuali: nel regime caotico maturo quelle cavalcate non esistono proprio (coerente con
  B-T/γ che le uccide; qui e' un fatto empirico di misura, non solo di eternita').
- **Cosa NON dice.** Nulla sull'eterno (trappola i). E p15 ×1,9 e' un eccesso modesto su classe
  minuscola: il fatto forte e' il suo 0% di nucleo, non l'eccesso.

## 84.3 Caveat
- Con 3 periodi richiesti, un evento a meta' o fine cavalcata non matcha (la finestra guarda solo
  avanti): l'incidenza misura "inizi di cavalcata all'evento", una sottostima dell'esposizione
  totale alle cavalcate. Non tocca il verdetto (il nucleo resta al 95%+ su svolte non periodiche).
- La baseline nulla condivide il flusso di svolte ma non la condizione deep (ancora = lettura nera
  qualunque): e' il null corretto per "il deep-black seleziona la periodicita'?", non per altri
  confronti.
- QMAX=15 limita il controllo generico ai periodi corti; periodi lunghi non-censimento non sono
  esclusi (ma p74 mostra che gia' al censimento le lingue lunghe sono assenti).

## 84.4 Trappola nuova
- **(s) il nucleo non ha antenati periodici noti — e (q) ha confini.** Non cercare parentele del
  vocabolario universale con famiglie quasi-periodiche esplicite: highway 0,05% (§83), rotori
  4,5% con l'unica classe in eccesso (p15) a massa-nucleo 0% (§84). La periodicita' di svolta E'
  il primo asse che segmenta la miscela nucleo/coda (delimita la trappola q, che resta valida per
  eta'/vc), ma le classi sono minuscole: non e' una leva quantitativa, e' un fatto strutturale.

## 84.5 Roadmap
1. **§85 (candidato teorema)**: verificare via automa prodotto (`code/product_automaton.py`,
   trappola-c compliant) l'enunciato universale "nessuna lettura nera fuori-finestra inizia una
   cavalcata LRRRR^3": se l'automa lo certifica, primo teorema esatto del lato-alpha nato dal
   vocabolario. Analogo per l'assenza dei rotori r≥2 dal regime caotico.
2. I p15-rides puro-coda (0,02%, ma 0% nucleo esatto): ispezione diretta dei ~12 eventi/orbita —
   cosa sono geometricamente?
3. Kill-gate §79.1 (deep-black-anchored decisive-depth sweep) resta in coda.
4. (Certificazione) ri-run Ryzen di §84.

## 84.6 Inventario file
- `alpha1/rotor_language_profile.py` (sonda §84: classi censimento a 3 periodi, baseline nulla
  condizionata, incrocio nucleo in streaming; `--orbits`, `--workers`, `--out`)
- `alpha1/rotor_language_summary.json`

## 84.7 Frase di stato dell'arte
*Il vocabolario del caos non discende da nessuna liturgia conosciuta: non dalla highway, non dai
rotori. Anzi: dove il ritmo si fa periodico il dialetto universale tace — zero parole del nucleo
sulle cavalcate p15, e la cavalcata elementare LRRRR il detrito profondo non la inizia mai, una
volta su un milione e mezzo dove il caso ne prometteva migliaia. L'omogeneita' ha mostrato la sua
prima crepa, ed e' una crepa che parla: il nucleo e' fatto di svolte che non si ripetono. Se
l'evitamento di LRRRR regge all'automa, il vocabolario avra' partorito il suo primo teorema.*
