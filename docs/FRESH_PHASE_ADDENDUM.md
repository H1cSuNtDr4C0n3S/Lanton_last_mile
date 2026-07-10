# ADDENDUM §103 — FRESH-PHASE: lo spettro delle porte a n=2500, l'approccio strutturato (picco-5/buco-3), le micro-porte

**Riepilogo in una frase:** il censimento preregistrato delle fasi d'onset su 2500
semi freschi catena-3 (gate: 24/24 canoniche bit-identiche a §102; verdetto dal
tool) da': **porta-0 = 95,4%** (47,3% esatta + 48,1% a fase 97–103), **porta-24/25
= 4,1%**, **12 fuori-cluster (0,48%)** su fasi {16, 30–31, 91–92} = micro-porte
nuove (falsificatore F realizzato: lo "zero fuori-cluster" di §102 era un artefatto
di n=24, trappola qq anche sulle fasi) — e l'istogramma delle estensioni
all'indietro **UCCIDE il modello a moneta di §102**: ext ha un **PICCO a 5 (487)**
e un **BUCO a 3 (1)** (attesi ~78/156 sotto 2^-k): l'approccio alla porta-0 e'
STRUTTURATO — in un quinto degli ingressi le ultime 5 svolte pre-onset coincidono
con W0 (fase 99), e la coincidenza di esattamente 3 e' quasi vietata. La porta
dominante non e' un punto: e' un oggetto con una firma d'approccio canonica.

Strumento: `alpha1/fresh_onset_phase_census.py` (+`_summary.json`, `.log`; 6 s,
14 worker).

## 103a. Numeri (2500 semi, 2499 onset, 1 skip, 0 no-onset)

| cluster | n | quota |
|---|---|---|
| fase 0 esatta | 1182 | 47,3% |
| fasi 97–103 (ext 1–7) | 1203 | 48,1% |
| porta-24/25 | 102 | 4,1% |
| **fuori-cluster** | **12** | **0,48%** |

Istogramma ext (1..7): 1→280, 2→188, **3→1**, 4→175, **5→487**, 6→32, 7→40.
Sotto il modello a moneta (P(ext=k) ~ 2^-k · n) gli attesi sarebbero ~625/312/156/
78/39/20/10: osservato picco netto a 5 (x12 l'atteso) e buco a 3 (1 vs 156).
**Correzione a §102 (onesta' falsificazionista):** la lettura "estensione
all'indietro accidentale" e' morta; le svolte pre-porta sono parte della porta
(un approccio canonico di ~5 passi in fase 99, mai di 3). La "coda leggermente
pesante" vista a n=24 era il primo sintomo.

Fuori-cluster (12): fasi 31×4, 16×3, 91×2, 92×1, 30×1 (+1). Micro-porte genuine o
approcci strutturati di porte note: da decidere (nessuna estensione all'indietro
di porta-0/24 produce quelle fasi).

## 103b. Che cosa cambia

1. **Per Link 1:** l'evento d'ingresso reale e' dominato (95%+4%) da DUE oggetti;
   l'osservabile d'occorrenza ai record (§102f.3) va definito sulla porta-0 CON la
   sua firma d'approccio (fase 99→0), non sulla sola fase 0.
2. **Per la porta/A1 §78:** il kernel decide i tentativi; la firma picco-5/buco-3
   e' una proprieta' della checklist d'approccio che il kernel deve gia'
   contenere — predizione verificabile sulla struttura di E(k) §61/§66.
3. **Trappola (qq) estesa:** anche i CLUSTER DI FASE sono quantili con data di
   scadenza (24→2500 ha aperto 5 fasi nuove); ogni enunciato "solo N porte" va
   preregistrato con potenza.

## 103c. Preregistrazione e gate (disciplina §100)

Falsificatore F (fase fuori {0}∪{97..103}∪{24,25}), potenza >=1000 onset
(realizzata: 2499), aspettativa dichiarata APERTA; verdetto emesso dal tool:
"F REALIZZATO: 12 onset fuori-cluster". Gate: 24/24 canoniche bit-identiche a
§102 (fase e onset per orbita); coda periodica per==per2 assert su ogni seme;
fase univoca (104 rotazioni distinte, esca bit-corrotto beccata a §102).
Riuso dichiarato della catena-3 §101 (disgiunzione da catene 1–2 verificata li');
le fasi sono un osservabile nuovo sugli stessi semi.

## 103d. Domande aperte / programma §104

1. Anatomia del picco-5/buco-3: le 5 svolte d'approccio sono un pezzo del
   transiente della porta? Confronto con la checklist E(k) §61 e le 22 porte §66
   (mappatura convenzioni di fase, ereditata da §102f.2).
2. Micro-porte {16, 30-31, 91-92}: germi minimi e stabilita' del loro tasso con n
   (solo preregistrato).
3. Evento "porta-0-completante" word-free ai record (§102f.3) con la firma
   d'approccio; tasso per-epoca = osservabile d'occorrenza di Link 1.
4. Ereditati: §101g, §102f, rientri §98g.2, scia-teorema §98g.3, separatori §97,
   fuggenti vs nere-D>=400, retro-nota §91c.3, stress-2 bianche, h1=1.

## 103e. Inventario file (alpha1/)

- `fresh_onset_phase_census.py` (+`_summary.json`, `.log`) — censimento
  preregistrato delle fasi d'onset su semi freschi, gate canonici, verdetto dal
  tool, istogramma ext.
