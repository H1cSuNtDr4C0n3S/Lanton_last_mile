# ADDENDUM §104 — DOOR-APPROACH: il vocabolario canonico, la Lingua d'Approccio (lemma), lo spettro dei tentativi ai record

**Riepilogo in una frase:** l'approccio alla porta-0 e' un **vocabolario canonico
piccolo** (le ultime 12 svolte pre-onset: il picco ext=5 di §103 e' UNA parola,
`RLLRRLRLRRRR`, 430/487 = 88%; il cluster fase-0 esatta e' la famiglia col suffisso-8
`LRRRRLLL`, 1011/1182 = 85%; top-10 = 68% di tutti gli ingressi), **unificato fra
reale e germi**: 11/14 germi della fascia approcciano la porta con la parola
IDENTICA `RLRRLRRRRLLL` (la #2 del vocabolario reale — la porta era invisibile ai
suffissi §102 perche' vive nel FUTURO della parola, nel transiente del germe);
il **LEMMA DELLA LINGUA D'APPROCCIO** (deduttivo, enumerazione esaustiva 2^12 via
realizzabilita' word-lock): **esattamente 671/4096 parole-approccio di larghezza 12
sono realizzabili** davanti a 2 periodi di W0-fase-0 (saturo: 671 anche a 3 periodi;
osservate ⊆ realizzabili; 89 famiglie di suffisso-8 realizzabili ⇒ la concentrazione
85% su UNA famiglia e' DINAMICA, non forzata dalla realizzabilita'); e lo **spettro
delle porte tentate AI RECORD** (fase del germe per tutti i 1639 record canonici):
**porta-0 95,4%** (695 esatta + 868 ext), porta-24/25 4,5%, micro-porte 3 (fasi
16, 31) — **identico allo spettro degli ingressi reali freschi** (95,4/4,1/0,5 §103)
⇒ la meta' "occorrenza" di Link 1 collassa su B-T: i tentativi di porta-0 sono lo
stato GENERICO dei record (i.o. gratis per un'eterna), e Link 1 ai record e' ridotto
a UNA quantita': lim sup [d(t) − onset_germe(w_t)] (il rigetto-shallow perpetuo e'
l'unico nemico rimasto).

Strumenti (alpha1/): `door_approach_census.py` (+`_summary.json`, `.log`),
`record_germ_phases.json`; sonde in-sessione per lingua d'approccio e fasi dei
germi (numeri a verbale qui).

## 104a. Censimento degli approcci (2499 onset freschi catena-3, gate §103 riprodotto)

Parole d'approccio = `turns[t_on−12 .. t_on)`. 234 distinte; top-10 = 68%:

| approccio | n | cluster dominante |
|---|---|---|
| RLLRRLRLRRRR | 430 | ext5 (430/487 = 88% del picco §103) |
| RLRRLRRRRLLL | 381 | fase0 |
| LRLRLRRRRLLL | 301 | fase0 |
| RRLRLRRRRLLL | 146 | fase0 |
| LRRRRLLRRRRL | 131 | ext (misto) |
| LRLLLLRRRRLR | 123 | ext4 (62) + porta24 (38) + ext2 (22) |

- Il cluster fase-0 esatta e' dominato dalla **famiglia di suffisso-8 `LRRRRLLL`**
  (1011/1182 = 85%): i primi 4 turni variano, gli ultimi 8 no.
- L'unico ext=3 osservato (`RRLRLLRRLRLL`) e' una parola isolata: il buco-3 di
  §103 e' l'assenza dinamica della sua classe, non un vincolo di realizzabilita'
  (la classe e' realizzabile, vedi 104c).
- **La stessa parola d'approccio puo' precedere porte diverse** (`LRLLLLRRRRLR`:
  ext4, porta-24/25 e ext2): il vocabolario e' trasversale alle porte — l'approccio
  non determina la fase da solo.

## 104b. Unificazione germi/reale

Approccio dei 14 germi della fascia (le ultime 12 svolte del germe prima del SUO
onset): **11/14 = `RLRRLRRRRLLL` identica** (la #2 reale), 1 = `LRLRLRRRRLLL`
(la #3 reale), 2 = parole con coda W0 gia' inclusa (le due fascia a fase 99/102,
coerenti). 12/14 nel vocabolario reale top-10/suffisso-8. **Perche' §102 non vedeva
un suffisso comune:** l'oggetto comune non e' nel suffisso della parola-record ma
a valle, nel transiente del germe (onset 55–261 passi dopo il record): la porta e'
un oggetto della CONTINUAZIONE.

## 104c. LEMMA DELLA LINGUA D'APPROCCIO (deduttivo)

Enumerazione esaustiva: per ognuna delle 2^12 = 4096 parole a di larghezza 12,
realizzabilita' (virtual_walk: nessuna rilettura contraddittoria = compatibile con
QUALCHE configurazione finita, convenzione §2) della parola `a + W0(fase 0) × 2`.
**Esattamente 671/4096 realizzabili; 671 anche con coda × 3 (saturo a 2 periodi).**
Le osservate (top-10 + canonica fascia) sono tutte dentro (gate). Fra le 671 ci
sono **89 famiglie di suffisso-8 distinte** ⇒ il dominio dinamico osservato
(1 famiglia all'85%) e' molto piu' stretto del cono di realizzabilita': la
concentrazione e' un fatto della DINAMICA d'ingresso, non del word-lock.
(Il lemma da' il bound esterno; l'inner bound osservato e' 234 parole.)

## 104d. Lo spettro delle porte AI RECORD — e il collasso dell'occorrenza

Fase W0 del germe per TUTTI i 1639 record canonici (1459 parole distinte,
germ run + estrattore §102 con esca):

| porta | n record | quota | (ingressi reali freschi §103) |
|---|---|---|---|
| porta-0 (esatta + ext 1-7) | 1563 (695+868) | **95,4%** | 95,4% |
| porta-24/25 | 73 | 4,5% | 4,1% |
| micro-porte (16, 31) | 3 | 0,2% | 0,5% |

**Lo spettro dei tentativi ai record e' lo spettro degli ingressi.** Conseguenza
per Link 1: la meta' "occorrenza" (quale parola/porta occorre ai record — il buco
storico, §98.0) NON richiede piu' un teorema di famiglia: **ogni record profondo
E' (al 95%) un tentativo di porta-0** (ipotesi A per-parola come §98c), e i record
sono i.o. per B-T. Link 1 ai record si riduce a una sola quantita':

>  **lim sup su t record di [d(t) − onset_germe(w_t)] >= L0**  (lock profondi i.o.)

con l'unico nemico = **rigetto-shallow perpetuo** (d < onset_germe definitivamente,
§101d), la cui geometria e' quantificata (§101: colpevole a cheb med 3, consumata a
ogni tentativo; §101d: per i germi drift-giu' la colpevole e' forzata nel
transiente).

## 104e. Gate, esche, onesta'

- Gate: cluster §103 riprodotti nel censimento approcci (fase0 1182, ext 1203,
  porta24 102, fuori 12; 0 skip extra); estrattore di fase univoco (104 rotazioni
  distinte) con esca bit-corrotto beccata (§102); osservate ⊆ realizzabili (104c);
  spettro record vs spettro reale = campioni indipendenti concordi (1639 canonici
  vs 2499 freschi).
- Onesta': verbale-sonda con pannello RIDOTTO (gate interni e conteggi; nessuna
  lente indipendente completa sui nuovi strumenti — DEBITO dichiarato per §105,
  in testa di sessione come da lezione §93/§94). I claim sono conteggi
  deterministici + un lemma per enumerazione esaustiva con self-test; il rischio
  residuo e' sulle convenzioni (fase, direzione della coda), gia' coperte
  dall'esca §102.
- Trappola (qq): nessuna nuova soglia; "671" e' un conteggio esatto di
  un'enumerazione completa, non un quantile; "95,4%" e' una quota di campione,
  non una costante.

## 104f. Domande aperte / programma §105

1. **Pannello sul blocco §101–104** (debito 104e): lente indipendente su
  approcci/fasi/lingua; esche su door_approach_census.
2. **Il nemico unico:** rigetto-shallow perpetuo. Ora che l'occorrenza e'
  collassata, l'attacco giusto e' per-parola sulla classe dominante: il transiente
  della porta-0 con approccio `RLRRLRRRRLLL` (onset 55: ~55 letture, oggetto
  FINITO) — che cosa deve pagare un'orbita per tenerlo sporco a ogni record?
  (Macchina del Muro/U1 sul germe-porta; attenzione a (v): niente argomenti di
  solitudine.)
3. **Anatomia del buco-3/picco-5:** ora e' un fatto di selezione dinamica del
  vocabolario (104a): perche' la dinamica sceglie ext5-class e evita ext3-class?
4. Ereditati: §101g, §102f, §103d, rientri §98g.2, scia-teorema §98g.3,
  separatori §97, fuggenti vs nere-D>=400, retro-nota §91c.3, stress-2 bianche,
  h1=1.

## 104g. Inventario file (alpha1/)

- `door_approach_census.py` (+`_summary.json`, `.log`) — censimento approcci-12
  per cluster di fase, gate §103.
- `record_germ_phases.json` — spettro delle porte dei 1639 record canonici.
