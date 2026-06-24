# ADDENDUM COMPATIBILITY-POTENTIAL — `Φ_compat` endpoint e oltre (§69)

Catena addenda: ... POTENTIAL-SEGMENT-SCANNER §67, ENDPOINT-MONOTONE-NOGO §68,
**COMPATIBILITY-POTENTIAL §69**.
Bersaglio di sessione: formulare `Φ_compat^L` senza ricadere nella massa dei difetti, verificare
che la versione endpoint e' gia' falsificata dai dati §67/§68, e isolare cio' che resta vivo:
event-wise/amortizzazione e co-raggiungibilita'.

## 69. Riepilogo in una frase
`Φ_compat^L` e' la distanza-prefix dalla compatibilita' con la migliore delle 22 porte; ma se la
si legge solo sugli endpoint dei segmenti, coincide con `best22_depth` e quindi e' gia'
falsificata. Nel micro-audit §69, sui segmenti deep/no-entry a `L=1600`, `h_best` non migliora
in **400/762** gate e in **3591/6275** grid; peggiora strettamente in **350/762** e **2736/6275**.

## 69.1 Definizione
Per ogni anchor, porta compatibile `g` e orizzonte `L`:

```
h_g^L = primo offset <= L in cui la porta g disaccorda con T3'
        (L+1 se nessun disaccordo e' visto fino a L)
h_best^L = max_g h_g^L
Phi_compat^L = 0 se h_best^L = L+1, altrimenti exp(-h_best^L / 104)
```

`h_best^L` misura quanto avanti arriva la migliore parola-porta prima del primo disaccordo.
Non misura quanti mismatch ci sono. Se `Φ_compat` viene definita come somma/minimo di mismatch,
ricade in `best22_mass` e appartiene gia' alla famiglia falsificata in §68.

## 69.2 Equivalenza critica
La versione endpoint di `Φ_compat^L` non e' un nuovo candidato: e' `Φ_best22_depth` riscritto.
Infatti `potential_segment_scanner.py` aveva gia' salvato:

- `best_h` = `h_best^L`;
- `phi_best22_depth = 0` se `best_h=L+1`, altrimenti `exp(-best_h/104)`.

Quindi un segmento deep/no-entry con `h_best(next) <= h_best(prev)` e' esattamente un
non-decremento di `Φ_compat` endpoint. Questo chiude la possibilita' di usarla come potenziale
scalare netto tra gate/grid consecutivi.

## 69.3 Micro-audit da CSV
Nuovo script:

```
C:\Python\Python310\python.exe alpha1\compat_endpoint_audit.py
```

Input:

```
alpha1/potential_segment_scanner_anchors.csv
alpha1/potential_segment_scanner_segments.csv
```

Output:

```
alpha1/compat_endpoint_audit_summary.json
alpha1/compat_endpoint_audit_witnesses.csv
```

La micro-audit non risimula nulla. Legge `best_h` dagli anchor §67, lo unisce ai segmenti, e
separa:

- **non-miglioramento:** `h_best(next) <= h_best(prev)`;
- **peggioramento stretto:** `h_best(next) < h_best(prev)`.

## 69.4 Risultati endpoint `L=1600`
Gate, **762** segmenti deep/no-entry:

| famiglia | eleggibili | non-migliora | peggiora stretto | pari | migliora |
|---|---:|---:|---:|---:|---:|
| gate | 762 | **400** | **350** | 50 | 362 |

Grid, **6275** segmenti deep/no-entry:

| famiglia | eleggibili | non-migliora | peggiora stretto | pari | migliora |
|---|---:|---:|---:|---:|---:|
| grid | 6275 | **3591** | **2736** | 855 | 2684 |

Nei quartili gate di `deep_black_count`, il quartile alto (`>2609`) ha **106/190** non-miglioramenti
e **91/190** peggioramenti stretti. Il fallimento endpoint non e' un effetto di segmenti poveri
di eventi deep-black.

Testimoni gate forti:
- orbita 2, gate `25 -> 26`, `t=225308..287361`: deep-black **15099**,
  `h_best=45 -> 45`;
- orbita 0, gate `20 -> 21`, `t=216215..273208`: deep-black **14244**,
  `h_best=47 -> 45`;
- orbita 12, gate `15 -> 16`, `t=115979..173215`: deep-black **13469**,
  `h_best=77 -> 61`;
- orbita 1, gate `21 -> 22`, `t=229701..272646`: deep-black **10893**,
  `h_best=76 -> 45`.

## 69.5 Conclusione endpoint
La compatibilita' endpoint e' falsificata come potenziale monotono netto. Questo non dice che
ogni evento deep-black sia inutile: dice solo che, tra due anchor consecutivi, il progresso
eventuale puo' essere cancellato o invertito da altri flip prima dell'endpoint successivo.

Quindi resta viva solo una delle forme seguenti:

- `Φ_compat` event-wise: misurare `h_best` immediatamente prima/dopo singoli eventi deep-black;
- `Φ_compat` amortizzata: tenere una banca/credito che accumula progresso deep e contabilizza
  le cancellazioni successive;
- ordine vettoriale/parziale, non scalare endpoint;
- argomento di co-raggiungibilita' T3' senza potenziale scalare.

## 69.6 Co-raggiungibilita'
La non-localita' sintattica di T3' non basta: due campi sintetici uguali localmente e diversi
in una cella lontana dimostrano solo che il predicato non e' locale. Per pesare sulla dinamica
servono coppie discriminanti **co-raggiungibili**:

1. due storie finite della formica;
2. stesso dato locale intorno alla porta fino a raggio `R`;
3. verdetto T3' diverso per una cella discriminante lontana;
4. entrambe le storie producono campi di detriti raggiungibili, non messi a mano.

Gap aperto: `R(n)` e' censito a 40, mentre gli offset decisivi osservati arrivano a 1591
(distanza relativa `L∞` fino a 36). Non e' chiaro se il gap si chiuda con concatenazioni locali
o richieda un nuovo certificato di raggiungibilita'.

## 69.7 Prossimo passo
Non fare un altro endpoint scanner. Due direzioni lecite:

1. **Empirica breve:** micro-script pre/post deep-black event, su campione limitato, per vedere se
   `h_best` aumenta localmente attorno agli eventi profondi oppure no.
2. **Teorica:** schema T3'/co-raggiungibilita' con definizione precisa di coppia discriminante
   raggiungibile e dei dati locali da eguagliare.

Entrambe devono tenere aperti due esiti: trovare una forma event-wise/amortizzata utile di
`Φ_compat`, oppure dimostrare che anche la famiglia compatibilita' cade e che α1 non e'
attaccabile per discesa di potenziale del detrito.

## 69.8 File prodotti
- `alpha1/compat_endpoint_audit.py`
- `alpha1/compat_endpoint_audit_summary.json`
- `alpha1/compat_endpoint_audit_witnesses.csv`
