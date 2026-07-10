# ADDENDUM §102 — FASCIA = PORTA-0: la fase d'ingresso e' l'invariante della fascia; le porte reali sono DUE

**Riepilogo in una frase:** la fascia word-mediated (14 parole: testimoni §100 + i 2
episodi-lock §101) NON ha un suffisso-nucleo (suffisso comune globale 3; il
troncamento cambia l'onset del germe: dipendenza dall'INTERA finestra K=101) — il suo
invariante e' la **FASE W0 D'INGRESSO: 12/14 entrano esattamente a fase 0** (le altre
2 a fase 99/102 = estensione all'indietro accidentale di 2/5 passi) e **0/14
altrove**; gli **onset REALI delle 24 orbite canoniche** si concentrano su **due
porte**: porta-0 (20/24: 10 esatte + 10 a fase 97–103 = estensioni all'indietro 1–7)
e **porta-24/25 (4/24)**, **zero orbite fuori dai tre cluster** su 104 fasi possibili
— la molteplicita' delle porte alla scala reale e' ~2, non 22 ne' 104, e la domanda
d'occorrenza di Link 1 si concentra su UNA porta dominante.

Strumento: `alpha1/fascia_door_probe.py` (+`_summary.json`, `.log`; 2,7 s).

## 102a. Che cosa NON e' la fascia (due negativi utili)

1. **Niente suffisso-nucleo:** suffisso comune globale delle 14 parole = 3 bit; un
   solo gruppo da 3 parole condivide 51 bit di suffisso; le altre sono a coppie
   sotto 40. La fascia non e' "tutte le parole che finiscono in σ*" (nessun
   parallelo diretto col w101 del Muro).
2. **Niente nucleo a K piccolo:** ogni suffisso troncato e' realizzabile gia' a
   K'=20, ma l'onset del germe CAMBIA (es. 55 → 2760): il germe veloce e' una
   proprieta' dell'intera finestra 101 (il footprint all'indietro cambia i colori
   del germe — coerente con §87e: onset e burden vanno ri-simulati a ogni prepend).
   Le parole troncate collassano su pochi onset comuni (2760, 838, 11177): i
   suffissi corti condivisi hanno il loro germe lento comune.

## 102b. Che cosa E' la fascia: porta-0

Per ognuna delle 14 parole: corsa lunga del germe, fase W0 della coda all'onset
(fase = rotazione k di `data/w0.txt` con combaciamento esatto dei 104 bit; le 104
rotazioni di W0 sono tutte distinte ⇒ fase univoca; esca: bit corrotto ⇒ fase None,
beccata):

| fase W0 | n |
|---|---|
| 0 (esatta) | **12** |
| 99, 102 (= ext 5, 2) | 2 |
| altre 101 fasi | **0** |

Drift del germe: (−2,2)×5, (−2,−2)×8, (2,−2)×1 — la DIREZIONE varia, la fase no:
l'invariante della fascia e' la porta, non la geometria assoluta. Burden 23–53,
onset_germe 55–261.

## 102c. Gli onset reali: due porte, zero altrove

Fase W0 di `turns[t_on : t_on+104]` per le 24 orbite canoniche (gate: onset ==
header 24/24; coda periodica verificata per==per2):

| cluster | n | lettura |
|---|---|---|
| fase 0 esatta | 10 | porta-0 |
| fasi 97–103 (ext 1–7) | 10 | porta-0 + estensione all'indietro accidentale |
| fasi 24–25 | 4 | **porta-24/25 (seconda porta genuina)** |
| altre 97 fasi | **0** | — |

Lettura dell'estensione: onset_verified estende l'onset all'indietro finche' le
svolte pre-porta coincidono per caso con W0; sotto un modello a moneta P(ext>=k) ~
2^-k gli attesi su 24 sono ~12/6/3/1,5/... e gli osservati 10/7/5/5/3/2/1 — coda
leggermente PESANTE a ext 4–7 (dichiarato: le svolte pre-porta sono correlate al
transiente della porta, non monete; nessun claim). L'estensione di 24–25 passi
(~2^-24) NON e' accidentale: porta-24/25 e' una seconda porta strutturale.

## 102d. Che cosa cambia per Link 1

1. La domanda d'occorrenza (§101g.1) si CONCENTRA: non "quale delle 2^101 parole",
   ma "la finestra che completa la **porta-0** (o la 24/25) occorre i.o. ai record
   delle eterne?". La molteplicita' dell'oggetto e' crollata: 14 parole → 1 porta
   dominante + 1 minore.
2. Il ponte con A1 (§78) e' ora nominabile: il kernel co-moving della porta decide
   ESATTAMENTE questi tentativi; i lock §101 sono attempt di porta-0 ai record.
3. Il quadro d'insieme: entrata reale = porta-0 (20/24) o porta-24/25 (4/24);
   fascia ai record = porta-0; violatori d'orizzonte §99 = parole onset 55 =
   porta-0. Tutta l'evidenza d'ingresso passa da due oggetti finiti.
4. Aperto (onesto): nessun teorema d'occorrenza; la corrispondenza porta-0/24-25 ↔
   le 22 porte di §66 e la fase-0 di §74 va mappata (convenzioni di fase diverse);
   il campione reale e' 24 (selezionate per onset alto, trappola h) — le fasi su
   semi freschi non sono ancora censite.

## 102e. Gate ed esche

- Gate: onset == header 24/24; coda periodica per==per2 24/24; fase trovata
  (not-None) 38/38 (14 germi + 24 reali); 104 rotazioni di W0 distinte (fase
  univoca).
- Esca estrattore: bit corrotto nella coda ⇒ fase None (beccata); controllo
  positivo fase 13 ritrovata.
- Onesta' di campione: fascia = 14 parole da catene 2-3 (selezione: testimoni
  min_ep>5 e lock — non un campione di parole "qualunque"); reali = 24 orbite
  selezionate per onset alto.

## 102f. Domande aperte / programma §103

1. **Fasi su semi freschi:** censire la fase d'onset di ~10k semi catena-3 (gia'
   simulati in §101b: basta la coda) — la bimodalita' 0/24-25 regge senza la
   selezione onset-alto? Quote relative delle due porte?
2. **Mappatura porte:** porta-0 e porta-24/25 nelle convenzioni §66 (22 porte
   E(k)) e §74 (fase 0 GF(2)); il germe minimo di porta-0 vs il germe-13 di §76.
3. **Occorrenza della porta-0 ai record:** definire l'evento "finestra
   porta-0-completante" come predicato word-free (fase del tentativo A1) e
   censirlo per epoca sulle 24 orbite — il tasso per-epoca e' l'osservabile
   d'occorrenza di Link 1.
4. Ereditati: §101g (costo del transiente sporco drift-giu'; min_cheb solo
   preregistrato), rientri §98g.2, scia-teorema §98g.3, separatori §97, fuggenti
   vs nere-D>=400, retro-nota §91c.3, stress-2 bianche, h1=1.

## 102g. Inventario file (alpha1/)

- `fascia_door_probe.py` (+`_summary.json`, `.log`) — fasi W0 della fascia e dei
  24 onset reali, troncamento, cluster, esche.
