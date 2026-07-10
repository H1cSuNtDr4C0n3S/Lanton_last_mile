# ADDENDUM §107 (apertura) — LA CLASSE PERICOLOSA e la piega su γ

**Riepilogo in una frase:** il predicato dei due obblighi (§106c) e' ora
interamente quantificato: |R_T(w)| (taglia del read-set del transiente,
word-decidibile) ha sui 1639 record canonici **min 4 / med 302 / max 3956**, la
**classe pericolosa** |R_T| <= 15 occorre allo 0,2% dei record (4/24 orbite;
<= 50: 4%, 20/24 orbite) e contiene entrambi i lock reali (14 e 9) — quindi il
nemico shallow-forever affronta la classe pericolosa in modo ricorrente nei
campioni e la copre SEMPRE (anche un |R_T| = 4 e' stato coperto); e la via di
falsificazione §106c.3 ("politica di discesa lenta perpetua") SI PIEGA SU γ:
una politica periodica sarebbe una parola eterna non-W0 = controesempio-γ, gia'
escluso fino a periodo 40 (`gamma_enum`, R(n) censiti) — una politica
NON-periodica e' un'orbita eterna generica = la domanda α1 stessa. Il bersaglio
record-anchored di Link 1 eredita quindi il supporto di γ, e la sua parte
irriducibile resta la coppia: [presentazioni della classe pericolosa i.o.] ∧
[lo scudo fallisce su una di esse] — entrambe misurate (0,2%/record; 2/82k)
ed entrambe fuori portata della misura per l'eterno (trappola i).

Numeri: `alpha1/danger_class_sizes.json` (istogramma completo per-record).

## 107a. Distribuzione della classe pericolosa (1639 record canonici)

| soglia κ | record |R_T| <= κ | quota | orbite |
|---|---|---|---|
| 10 | 1 | 0,06% | 1/24 |
| 15 | 4 | 0,2% | 4/24 |
| 20 | 8 | 0,5% | 7/24 |
| 30 | 17 | 1,0% | 11/24 |
| 50 | 66 | 4,0% | 20/24 |

onset_germe dei record a |R_T|<=15: med 204, max 272 (coerente: read-set piccolo
⇔ transiente corto ⇔ classe veloce/porta-0). I 2 lock: |R_T| = 14 e 9 —
entrambi nella classe <= 15. Nessuna soglia enunciata (trappola qq): κ e' un
parametro del predicato, la distribuzione e' il dato.

## 107b. La piega su γ (osservazione strutturale)

La direzione di falsificazione di §106c.3 — costruire una discesa perpetua che
tiene sporchi i read-set veloci — ha due soli tipi possibili:
1. **periodica** (spazio-tempo): la parola di svolte eterna risultante avrebbe
   periodo != condizioni-W0 ⇒ e' esattamente un **controesempio-γ**, gia'
   escluso dall'enumerazione fino a periodo 40 (`data/gamma_enum.pkl`, §2);
2. **non-periodica**: un'orbita eterna caotica descendente = l'oggetto stesso
   della domanda α1 (nessuna costruzione finita puo' esibirla, trappola i).
⇒ il bersaglio record-anchored di Link 1 non ha falsificatori COSTRUIBILI a
buon mercato: la sua negazione o e' γ-falsa (<= 40) o e' α1-completa. Questo
salda il fronte §106/§107 ai pilastri esistenti del programma (α1 ∧ β ∧ γ) e
chiude la direzione (b) di §106c.3 come "gia' coperta da γ".

## 107c. Stato finale della scala a Link 1 (dopo §101–§107a)

Link 1 (record-anchored, sufficiente) ⟸ (i) ∧ (ii), con:
- **(i) occorrenza della classe pericolosa:** l'eterna presenta parole a
  |R_T| <= κ ai record i.o. — misurato 0,2-4%/record sui campioni; predicato
  word-decidibile; NON dimostrato per l'eterno;
- **(ii) fallimento dello scudo:** su una presentazione pericolosa, il read-set
  e' interamente bianco — realizzato 2/82k in natura (§101), meccanismo
  completo (§105b: cuneo del drift + consumo a catena), vincolo deduttivo di
  lentezza (§106) nel regime estremo.
Le vie deduttive note per (ii) — ledger (trappola n), scalinata a filo-di-rasoio
(falsificata §105b), solitudine (trappola v), zona piccola (§97) — sono tutte
chiuse: (ii) richiede un argomento nuovo sulla geometria del cuneo contro lo
scudo d'escursione. (i) e' il parente record-anchored delle domande d'occorrenza
storiche, ora su un predicato finito.

## 107c-bis. COROLLARIO DELL'OR (kernel co-moving del lato-record)

Dalla Dicotomia §101 (Lemmi 0-1): a un record profondo con parola w (ipotesi A),
    **rigetto (classe T) ⟺ OR dei colori reali delle celle di R_T(w)** —
le divergenze entro il transiente vivono SOLO sul read-set (footprint word-
determinato, celle basse bianche gratis), e read-set tutto bianco ⇒ co-evoluzione
fino all'onset (Teorema del Limite di Velocita' ne e' il caso garantito-vergine).
Quindi il verdetto del record e' funzione di |R_T(w)| bit co-moving: **il
lato-record ha il suo kernel finito, gemello del kernel-porta A1 §78 (44 celle,
P=15) — e sulla classe pericolosa il kernel e' un OR di <= κ bit.** La parte (ii)
della scala (107c) diventa: "a una presentazione pericolosa, quei <= κ bit sono
tutti 0" — l'intero residuo dinamico di Link 1 ai record e' lo stato di <= κ
celle co-moving in un istante ricorrente. (Definitionale-deduttivo: nessun
contenuto empirico nuovo; da' l'OGGETTO per l'attacco §107d.2.)

## 107d. Prossimo

1. (i) come domanda di ricorrenza del vocabolario: le parole a |R_T| piccolo
   sono legate alla firma d'approccio §104 — la loro presentazione ai record e'
   collegabile ai rientri della Scala (§98g.2)?
2. (ii): geometria del cuneo vs scudo — formalizzare "lo scudo copre il cuneo"
   come proprieta' di stato co-moving finito (parente A1 §78, lato-record).
3. Ereditati: §106c, §105b.4, §101g, §102f, §103d, §104f.
