# ADDENDUM ENDPOINT-MONOTONE-NOGO — No-go controllato dei proxy Φ (§68)

Catena addenda: ... DOOR-DEFECT-PROFILE §66, POTENTIAL-SEGMENT-SCANNER §67,
**ENDPOINT-MONOTONE-NOGO §68**.
Bersaglio di sessione: chiudere correttamente il passo §67, senza trasformare una falsificazione
campionaria in teorema dinamico, e fissare il prossimo oggetto: T3'/realizzabilita'.

## 68. Riepilogo in una frase
Sul campione raggiunto §67, la strategia "deep-black forza decremento netto di un proxy scalare
endpoint-monotono finito" e' falsificata per i proxy testati: a `L=1600`, su gate deep/no-entry,
`Φ_depth` ha **400/762** non-decrementi e **350/762** peggioramenti stretti; `Φ_mass_104` ha
**373/762** non-decrementi e **371/762** peggioramenti stretti. La conclusione lecita non e'
"nessun potenziale esiste", ma "questi proxy e ogni loro riparametrizzazione order-preserving
non possono sostenere una prova via decremento endpoint".

## 68.1 Problema riformulato
Dato §67, vogliamo sapere quale no-go e' onesto:

- input: segmenti consecutivi tra anchor `gate` o `grid`, gia' raggiunti da orbite finite lunghe;
- evento richiesto: `deep_black_count > 0`;
- esclusione: nessun ingresso/clear all'endpoint del segmento;
- candidato: uno scalare `Φ` letto sugli endpoint, da ridurre a ogni segmento con deep-black;
- violazione: `Φ(next) >= Φ(prev)`.

Questo e' un test di falsificazione di un meccanismo, non una prova di α1. Uccide solo candidati
che pretendono decremento netto tra endpoint consecutivi.

## 68.2 Definizioni operative
Per questa sessione:

- **segmento eleggibile:** due anchor consecutivi della stessa famiglia e dello stesso orizzonte,
  con `deep_black_count>0` e `has_entry_endpoint=false`;
- **proxy endpoint-monotono:** funzione scalare `Φ(anchor)` che una prova vorrebbe far scendere
  sugli endpoint dei segmenti eleggibili;
- **non-decremento:** `ΔΦ = Φ(next)-Φ(prev) >= 0`;
- **peggioramento stretto:** `ΔΦ > 0`.

Se la prova richiede decremento non sommabile causato da deep-black, un non-decremento e' gia'
controesempio. I peggioramenti stretti sono registrati separatamente per evitare che il no-go
dipenda solo da pareggi.

## 68.3 Critic pass Pauli: correzioni accettate
Pauli ha imposto tre qualifiche, tutte integrate:

1. dire **no-go empirico/testimoniale sul campione raggiunto**, non teorema dinamico universale;
2. evitare frasi come "nessun potenziale finito funziona" o "deep-black non decrementa"; la forma
   corretta e': deep-black non forza decremento netto endpoint **di questi proxy**;
3. aggiungere una mini-audit da CSV, con testimoni e quantili, per escludere che la diagnosi sia
   un artefatto di segmenti piccoli o soli pareggi.

Obiezione non risolta: un `Φ` con memoria interna, credito/amortizzazione, ordine parziale o
codominio ben fondato non viene toccato da questo test.

## 68.4 Mini-audit da CSV
Nuovo script:

```
C:\Python\Python310\python.exe alpha1\endpoint_monotone_audit.py
```

Input:

```
alpha1/potential_segment_scanner_anchors.csv
alpha1/potential_segment_scanner_segments.csv
```

Output:

```
alpha1/endpoint_monotone_audit_summary.json
alpha1/endpoint_monotone_audit_witnesses.csv
```

La mini-audit non risimula nulla: legge i CSV §67, unisce segmenti e anchor, separa non-decrementi
e peggioramenti stretti, estrae witness top e stratifica per quantili di `deep_black_count` e
`gap_steps`.

## 68.5 Risultati audit: gate `L=1600`
Segmenti gate eleggibili: **762**.

| proxy | non-decrementi | peggioramenti stretti | pareggi | miglioramenti |
|---|---:|---:|---:|---:|
| `Φ_actual_depth` | **400/762** | **350/762** | 50 | 362 |
| `Φ_actual_mass_104` | **373/762** | **371/762** | 2 | 389 |
| `Φ_actual_mass_208` | **380/762** | **378/762** | 2 | 382 |
| `Φ_best22_depth` | **400/762** | **350/762** | 50 | 362 |

La falsificazione non vive solo nei pareggi. Per le masse, quasi tutti i non-decrementi sono
peggioramenti stretti.

Nei quartili di `deep_black_count`, `Φ_actual_mass_104` viola:

| deep-black bin | n | non-decrementi | peggioramenti stretti |
|---|---:|---:|---:|
| `<=263` | 191 | 95 | 95 |
| `263..949` | 190 | 97 | 96 |
| `949..2609` | 191 | 79 | 78 |
| `>2609` | 190 | 102 | 102 |

Quindi il no-go non e' prodotto da segmenti poveri di deep-black. Anche nel quartile alto
(`>2609` eventi deep-black) `Φ_mass_104` peggiora strettamente in **102/190** casi.

Testimoni top `L=1600`:
- orbita 2, gate `25 -> 26`, `t=225308..287361`: deep-black **15099**,
  `Φ_depth` pari (`h=45 -> 45`), nessun ingresso;
- orbita 0, gate `20 -> 21`, `t=216215..273208`: deep-black **14244**,
  `Φ_depth +0.0124`, `Φ_mass_104 +6.1825`, `Φ_mass_208 +15.1235`;
- orbita 12, gate `15 -> 16`, `t=115979..173215`: deep-black **13469**,
  `Φ_depth +0.0793`, `Φ_mass_104 +3.4276`, `h=77 -> 61`.

## 68.6 Risultati audit: grid `L=1600`
Segmenti grid eleggibili: **6275**.

| proxy | non-decrementi | peggioramenti stretti | pareggi | miglioramenti |
|---|---:|---:|---:|---:|
| `Φ_best22_depth` | **3591/6275** | **2736/6275** | 855 | 2684 |
| `Φ_best22_mass_104` | **3150/6275** | **3149/6275** | 1 | 3125 |
| `Φ_best22_mass_208` | **3145/6275** | **3144/6275** | 1 | 3130 |
| `phi_best_deficit` | **3591/6275** | **2736/6275** | 855 | 2684 |
| `phi_top3_deficit` | **3570/6275** | **2795/6275** | 775 | 2705 |
| `phi_sum_deficit` | **3371/6275** | **2927/6275** | 444 | 2904 |

Nel baseline non-condizionato il risultato e' ancora piu' meccanico: le masse oscillano quasi
perfettamente a meta'. Anche qui il problema non e' l'uguaglianza: `Φ_best22_mass_104` ha
**3149** peggioramenti stretti.

## 68.7 No-go lecito
Enunciato corretto:

> Nel campione raggiunto §67, per ciascuno dei proxy scalari finiti testati da
> `potential_segment_scanner.py`, esistono segmenti eleggibili con molti eventi deep-black,
> nessun ingresso endpoint e `Φ(next) >= Φ(prev)`. Dunque quei proxy, e ogni loro
> riparametrizzazione order-preserving, non possono sostenere una prova basata su decremento
> netto endpoint da deep-black.

Questo non dice:

- che α1 sia falso o vero;
- che non esista alcun potenziale globale;
- che deep-black sia irrilevante;
- che una funzione con memoria/credito sia esclusa;
- che la non-localita' dinamica sia dimostrata.

Dice solo che il leverage "deep-black floor -> scalare endpoint finito che scende" e' sbagliato.

## 68.8 Prossimo passo vero
Non aprire un nuovo scanner lungo e non riprovare `λ` diversi.

Il prossimo oggetto e' T3'/realizzabilita':

1. costruire lo schema di coppie discriminanti: stessi dati locali intorno alla porta fino a
   raggio `R`, verdetto T3' diverso per una cella lontana;
2. separare due livelli: non-localita' sintattica della checklist vs realizzabilita' dinamica
   da campi di detriti prodotti da orbite finite;
3. cercare testimoni raggiunti o una chiusura naturale dei campi raggiungibili.

Se si vuole ancora un `Φ`, la forma deve cambiare: memoria/credito, ordine parziale/discreto
ben fondato, o invariante globale del campo di detriti. Non uno scalare endpoint-based.

## 68.9 File prodotti
- `alpha1/endpoint_monotone_audit.py`
- `alpha1/endpoint_monotone_audit_summary.json`
- `alpha1/endpoint_monotone_audit_witnesses.csv`
