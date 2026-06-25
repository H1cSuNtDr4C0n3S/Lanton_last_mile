# GA Gate-Zero Addendum (§75)

Riepilogo in una frase: il primo stress-test del programma GA/no-entry fallisce al gate-zero,
perche' il prototipo astratto `A0(r,K,D0)` non determina il verdetto T3' e quindi non puo'
certificare SCC no-entry senza cecita' strutturale.

## 75.1 Obiettivo

La sessione §75 non cercava una nuova prova della congettura. Doveva rendere falsificabile il
piano GA/no-entry prima della classificazione SCC:

1. costruire un prototipo finito `A0(r,K,D0)` come sovra-approssimazione sound;
2. chiedere se il verdetto/prefisso T3' e' funzione dello stato astratto;
3. fermarsi prima delle SCC se il gate-zero fallisce.

Questo segue la correzione strategica post-§74: non trattare `beta/GF(2)` come fase separata
post-`alpha1`, ma come eventuale certificato interno per SCC con lock profondi ricorrenti e
ingresso ancora evitato.

## 75.2 Stato astratto testato

Il prototipo testato e':

```text
A0-state = (
  P_r,                 # patch locale normalizzato del detrito in B_r
  b0,                  # bit letto all'anchor
  g,                   # fase gate T3' valutata
  min(d_g,K),          # prefisso W0 di fase g visibile, saturato a K
  min(d_g,D0),         # profondita' lock, saturata a D0
  [d_g >= D0]          # flag lock profondo
)
```

`P_r` e' espresso nel frame porta/anchor. `d_g` e' la lunghezza del prefisso futuro che coincide
con `W0` in fase `g`. La semantica e' volutamente una sovra-approssimazione: ogni storia concreta
della formica si proietta nello stato, ma il detrito fuori patch viene dimenticato.

## 75.3 Risultato gate-zero

Verdetto: **FAIL** per `A0(r,K,D0)` con `K=80`, `D0=80`, e per il witness dinamico finche'
`r<=8` e i cap restano `<=494`.

Comando registrato:

```powershell
C:\Python\Python310\python.exe GA_stress_agent\ga_gate_zero_audit.py --radii 2,3,4,8,9 --synthetic-radius 8 --K 80 --D0 80 --horizons 512,1600 --out GA_stress_agent\gate_zero_summary.json
```

Due anchor replayabili dalla stessa orbita lunga collassano nello stesso stato astratto:

```text
orbita: 5
rngstate: 16489936061346709332
fase T3': 98

A: t=60320, origin=(58,-26), heading=2
B: t=60840, origin=(48,-36), heading=2
```

Per `r=2,3,4,8` gli stati coincidono:

```text
patch_hash r=8 = 1e838dafb7a51b780addaa3772ef0181
observed_turn_bit = 0
tail_prefix_cap_K = 80
lock_depth_cap_D0 = 80
deep_lock_flag = 1
```

ma il prefisso T3' differisce:

```text
A: first_bad = 1014, h_512 = 513, h_1600 = 1014
B: first_bad =  494, h_512 = 494, h_1600 = 494
```

La prima differenza del patch locale compare a `r=9`.

Limite logico: questo e' un witness dinamico per non-determinacy di `h_g^L`/verdetto prefix
finito. Non e' un witness binario infinito entry-vs-no-entry: a `L=1600` entrambi falliscono,
ma con offset diverso.

## 75.4 Witness sintattico

Lo script costruisce anche due campi finiti con stesso `A0(8,80,80)` ma differenza su una
cella T3' fuori patch:

```text
fase: 98
discriminante: offset=138, rel=(3,9), Linf=9
required_black=0
```

Risultato:

```text
campo pass: h_1600 = 1601, clear_1600 = 1
campo fail: h_1600 = 138,  clear_1600 = 0
stesso stato A0: si
```

Limite logico: e' sintattico/prefix, non una co-raggiungibilita'. Serve a mostrare che un patch
finito non decide T3' senza memorizzare le celle interrogate dalla checklist o un proof object
equivalente sul fuori-patch.

## 75.5 Conseguenza sulle SCC

Le SCC non sono state classificate. Farlo dopo il gate-zero FAIL sarebbe una certificazione cieca:
una SCC "no-entry" potrebbe essere tale solo perche' lo stato non vede la cella T3' discriminante.

Il certificato mancante non e' altro compute. E' uno dei seguenti:

1. rendere T3' una funzione dello stato, includendo tutte le celle rilevanti o un proof object
   equivalente;
2. trattare il fuori-patch simbolicamente con stati `OK/KO/unknown`, senza classificare
   `unknown` come no-entry;
3. integrare il ramo beta come certificato defect-current SCC-level, non come post-processing
   di singoli cicli.

## 75.6 Lettura strategica

`A0` resta sound come sovra-approssimazione, ma e' cieco rispetto a T3' gia' a `r<=8` con cap
naturali `K,D0=80`. Il risultato non dimostra ne' falsifica la congettura; impedisce una prova
sbagliata.

Il prossimo fronte (§76) non e' aumentare `r` a caso. E':

1. definire una variante `A1` in cui T3' sia deterministico per costruzione o proof object;
2. oppure propagare esplicitamente `unknown` nelle SCC e dimostrare solo cio' che non dipende
   dal fuori-patch;
3. fissare prima un budget di refinement, per trattare la non-convergenza come risultato e non
   come richiesta indefinita di compute.

## 75.7 Inventario file

- `GA_stress_agent/GA_STRESS_REPORT.md` — report tecnico della sessione.
- `GA_stress_agent/ga_gate_zero_audit.py` — audit gate-zero.
- `GA_stress_agent/gate_zero_summary.json` — output macchina.
- Self-test riferiti dal report: `window_automaton.py --selftest`, `product_automaton.py --selftest`,
  e `alpha1_engine.exe` su vuota `9977` e difetto `(7,-7)` `106258`.
