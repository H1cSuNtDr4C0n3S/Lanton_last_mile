# ADDENDUM POTENTIAL-SEGMENT-SCANNER — Falsificazione dei Φ monotoni semplici (§67)

Catena addenda: ... CHECKLIST-NONLOCAL §65, DOOR-DEFECT-PROFILE §66,
**POTENTIAL-SEGMENT-SCANNER §67**.
Bersaglio di sessione: subordinare a Pauli la scelta dei candidati `Φ(detrito)` piu' rozzi,
implementarli come falsificatori segmentali, e verificare se gli eventi deep-black forzati
spingono monotonicamente il campo verso una porta.

## 67. Riepilogo in una frase
La famiglia naturale dei potenziali monotoni per segmento e' falsificata. Sui segmenti tra
gate-attempt consecutivi con deep-black e senza ingresso, `Φ_depth` viola la monotonia in
**400/762** casi; `Φ_mass_104` in **373/762**. Sullo scanner non-condizionato a passo 1040,
`Φ_best22_depth` viola in **3591/6275** segmenti. Quindi deep-black e' ricorrente, ma non e'
un decremento monotono di questi deficit T3' finiti.

## 67.1 Scelta dei candidati, da Pauli
Pauli ha imposto la lettura giusta: testare prima i candidati piu' esposti, non cercare subito
un `Φ` astratto.

Candidati implementati:
- `Φ_depth = exp(-h/104)`, dove `h` e' la prima cattiva della porta reale; `Φ=0` se il vettore
  e' clear all'orizzonte.
- `Φ_mass_104 = Σ exp(-offset/104)` sui mismatch T3' della porta reale.
- `Φ_mass_208 = Σ exp(-offset/208)` sui mismatch T3' della porta reale.
- `Φ_best22_*`: analoghi best/min su tutte le porte compatibili col primo bit, per lo scanner
  non condizionato.
- proxy di controllo: deficit del best, top-3 e somma dei deficit sulle fasi compatibili.

Test killer:

```
deep_black_count > 0,
nessun ingresso nel segmento,
ma Phi(next) >= Phi(prev).
```

Questo uccide solo i `Φ` che pretendono monotonia netta tra anchor consecutivi; non uccide un
potenziale con credito interno, memoria o compensazioni lungo il segmento.

## 67.2 Strumento
Nuovo file:

```
alpha1/potential_segment_scanner.py
```

Lo scanner ricostruisce le 24 orbite lunghe e valuta due famiglie di anchor:
- **gate:** i tentativi porta deduplicati §63/§66;
- **grid:** anchor a passo fisso `1040`, esclusi i tempi gate.

Per ogni anchor e orizzonte `L=208,512,1600` valuta le 22 fasi porta compatibili/incompatibili,
calcola i proxy `Φ`, poi costruisce segmenti consecutivi per famiglia e orizzonte. Output:

```
alpha1/potential_segment_scanner_anchors.csv
alpha1/potential_segment_scanner_segments.csv
alpha1/potential_segment_scanner_summary.json
```

## 67.3 Run e controlli
Comando:

```
C:\Python\Python310\python.exe alpha1\potential_segment_scanner.py --max-seconds 290 --grid-stride 1040 --out-prefix alpha1\potential_segment_scanner
```

Self-test prima della run:
- `window_automaton.py --selftest`: verde;
- `product_automaton.py --selftest`: verde;
- `alpha1_engine.exe dump`: vuota -> **9977**, seme `(7,-7)` -> **106258**.

Risultato run:
- orbite completate: **24/24**;
- anchor-horizon rows: **21.327**;
- segment rows: **21.183**;
- grid stride: **1040**;
- runtime: **125 s**.

## 67.4 Risultati gate: porta reale
Segmenti gate a `L=1600`:
- segmenti totali: **786**;
- segmenti eleggibili (`deep_black_count>0` e nessun ingresso): **762**;
- deep-black per segmento: mediana **964**, max **15099**.

Violazioni:

| proxy | violazioni | rate | mediana ΔΦ |
|---|---:|---:|---:|
| `Φ_depth` | **400/762** | **0.5249** | 0.0 |
| `Φ_mass_104` | **373/762** | **0.4895** | -0.0531 |
| `Φ_mass_208` | **380/762** | **0.4987** | -0.0101 |

La falsificazione non e' marginale: circa meta' dei segmenti con molte letture deep-black non
migliora il potenziale della porta reale.

Esempi top:
- orbita 2, gate `25 -> 26`, `t=225308..287361`: deep-black **15099**, `ΔΦ_depth=0`.
- orbita 0, gate `20 -> 21`, `t=216215..273208`: deep-black **14244**,
  `ΔΦ_depth=+0.0124`, `ΔΦ_mass_104=+6.1825`.
- orbita 12, gate `15 -> 16`, `t=115979..173215`: deep-black **13469**,
  `ΔΦ_depth=+0.0793`, `ΔΦ_mass_104=+3.4276`.

Questi sono controesempi diretti alla speranza "deep-black event => porta reale piu' vicina".

## 67.5 Risultati grid: non-condizionato best-22
Anchor grid:
- anchor per orizzonte: **6299**;
- a `L=208/512` ci sono **2** clear finiti non-entry;
- a `L=1600` clear grid: **0**;
- best-h grid a `L=1600`: mediana **5**, max **1014**.

Segmenti grid a `L=1600`:
- segmenti/eleggibili: **6275/6275**;
- deep-black per segmento: mediana **247**, max **423**.

Violazioni:

| proxy | violazioni | rate | mediana ΔΦ |
|---|---:|---:|---:|
| `Φ_best22_depth` | **3591/6275** | **0.5723** | 0.0 |
| `Φ_best22_mass_104` | **3150/6275** | **0.5020** | +0.0181 |
| `Φ_best22_mass_208` | **3145/6275** | **0.5012** | +0.0115 |
| `phi_best_deficit` | **3591/6275** | **0.5723** | 0.0 |
| `phi_top3_deficit` | **3570/6275** | **0.5689** | 0.0 |
| `phi_sum_deficit` | **3371/6275** | **0.5372** | 0.0 |

Nel baseline non-condizionato la situazione e' ancora piu' chiara: i proxy oscillano, non
scendono. I due clear a `L=208/512` spariscono a `L=1600`, quindi sono falsi positivi finiti,
non ingressi.

## 67.6 Controllo best-22 sui gate
A `L=1600`, sui **810** gate-anchor:
- `Φ_depth` della porta reale e `Φ_best22_depth` differiscono in **0/810** casi;
- `Φ_mass_104` differisce in **6/810**;
- `Φ_mass_208` differisce in **61/810**.

Quindi §66 resta coerente: la profondita' best-22 collassa sulla fase reale. Le masse possono
preferire un'altra fase per mismatch tardivi, ma non cambiano la diagnosi segmentale.

## 67.7 Interpretazione
Questa sessione falsifica una classe, non α1.

Morta:
- `Φ_depth` come potenziale monotono;
- `Φ_mass_104/208` come potenziale monotono;
- `Φ_best22` finito come potenziale monotono;
- deficit best/top-3/somma sulle fasi compatibili.

Non morta:
- un `Φ` con credito interno;
- un `Φ` con memoria del segmento, non solo endpoint;
- un ordine ben fondato/discreto che tolleri oscillazioni locali ma vieti cicli globali;
- un argomento di raggiungibilita'/avoidance non espresso come decremento segmentale.

Il punto tecnico nuovo: il floor deep-black e' driver/evento, non potenziale. Anche quando gli
eventi deep-black sono molti, il deficit T3' della porta puo' peggiorare o restare uguale.

## 67.8 Caveat
- Campione ancora onset-high e finito: stress-test, non prova.
- La segmentazione tra gate-attempt e grid-anchor testa monotonia netta tra endpoint; non vede
  potenziali con oscillazioni compensate internamente.
- `D(t)` e proximity-to-lock non vanno riaperti come `Φ`: §59 li ha gia' falsificati come proxy.
- AUC/regressioni restano fuori bersaglio: qui si testa monotonia/falsificazione, non predizione.

## 67.9 Prossimo passo (§68)
Non rilanciare varianti di `Φ_depth` o `Φ_mass` con altri pesi: la classe e' gia' morta.

Priorita' §68:
1. scrivere un piccolo no-go lemma empirico/formale per i potenziali endpoint-monotoni finiti
   basati sul primo difetto o sulla massa pesata T3';
2. tornare al lemma di non-localita' T3' con focus sulla realizzabilita' delle coppie
   discriminanti;
3. se si cerca ancora un potenziale, deve avere memoria/credito o codominio ben fondato, non
   essere un numero reale endpoint-based.

## 67.10 File prodotti
- `alpha1/potential_segment_scanner.py`
- `alpha1/potential_segment_scanner_anchors.csv`
- `alpha1/potential_segment_scanner_segments.csv`
- `alpha1/potential_segment_scanner_summary.json`
