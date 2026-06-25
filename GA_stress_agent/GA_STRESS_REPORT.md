# GA/no-entry stress test - gate-zero audit

Data: 2026-06-25.
Scope: stress-test tecnico del piano GA/no-entry. Nessun file esistente e' stato modificato;
gli artefatti sono in `GA_stress_agent/`.

## 1. Stato prototipo `A0(r,K,D0)`

Il minimo prototipo sound testato qui e':

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

`P_r` e' nel frame della porta/anchor. `d_g` e' la lunghezza del prefisso futuro che coincide
con `W0` in fase `g`. La semantica e' una sovra-approssimazione: ogni storia concreta della
formica si proietta in uno stato, ma il detrito fuori patch e' dimenticato.

Target SCC previsto, non eseguito perche' gate-zero fallisce:

```text
SCC tipo I:  nessun lock profondo ricorrente
             -> ramo Link 1 / gate-avoiding

SCC tipo II: lock profondi ricorrenti, ma nessun ingresso T3'
             -> ramo beta / defect-current
```

Classificatori ammessi solo dopo gate-zero: drift zero via B-T/unboundedness, periodicita' via
gamma, fresh-L inevitabile, ranking ben fondato, defect-current SCC-level.

## 2. Gate-zero result

Verdetto: **FAIL** per `A0(r,K,D0)` con `K=80`, `D0=80`, e in generale per il witness dinamico
finche' `r <= 8` e i cap `K,D0 <= 494`.

Output macchina: `GA_stress_agent/gate_zero_summary.json`.

Comando:

```powershell
C:\Python\Python310\python.exe GA_stress_agent\ga_gate_zero_audit.py --radii 2,3,4,8,9 --synthetic-radius 8 --K 80 --D0 80 --horizons 512,1600 --out GA_stress_agent\gate_zero_summary.json
```

## 3. Witness dinamico raggiunto

Due anchor replayabili dalla stessa orbita lunga:

```text
orbita: 5
rngstate: 16489936061346709332
fase T3': 98

A: t=60320, origin=(58,-26), heading=2
B: t=60840, origin=(48,-36), heading=2
```

Per `r=2,3,4,8` gli stati astratti coincidono:

```text
patch_hash r=8 = 1e838dafb7a51b780addaa3772ef0181
observed_turn_bit = 0
tail_prefix_cap_K = 80
lock_depth_cap_D0 = 80
deep_lock_flag = 1
```

Ma il T3' prefix verdict differisce:

```text
A: first_bad = 1014, h_512 = 513 (clear fino a 512), h_1600 = 1014
B: first_bad =  494, h_512 = 494 (fail),              h_1600 = 494
```

La prima differenza del patch locale compare solo a `r=9`. Quindi un successo a `r=2/3/4`
sarebbe compatibile con cecita' dell'astrazione.

Limite logico: questo witness dinamico prova non-determinacy di `h_g^L`/verdetto prefix finito.
Non e' un witness binario infinito entry-vs-no-entry: a `L=1600` entrambi sono fail, con offset
diverso.

## 4. Witness sintattico prefix

Per separare la cecita' pura della rappresentazione dalla rarita' dei witness dinamici, lo
script costruisce anche due campi finiti con lo stesso `A0(8,80,80)` e differenza su una cella
T3' fuori patch:

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

Limite logico: questo e' sintattico/prefix, non co-raggiungibilita'. Serve solo a mostrare che
un patch finito non puo' decidere T3' senza memorizzare le celle interrogate dalla checklist o
un certificato equivalente sul fuori-patch.

## 5. SCC-level status

Non ho classificato SCC. Farlo dopo il FAIL gate-zero sarebbe sospetto: una SCC "no-entry"
potrebbe essere no-entry solo perche' lo stato non vede la cella T3' discriminante.

Lista SCC classificate/non classificate: **non applicabile**.

Witness della SCC dura: **non applicabile in questa sessione**. Il witness duro e' a monte:
due storie collassano nello stesso stato astratto ma hanno T3' prefix diverso.

## 6. Diagnosi del certificato mancante

Il certificato mancante non e' compute. E' uno dei seguenti:

1. rendere T3' una funzione dello stato, includendo nella componente astratta tutte le celle
   T3' rilevanti o un proof object equivalente;
2. trattare il fuori-patch simbolicamente, con stati `OK/KO/unknown` e non classificare
   `unknown` come no-entry;
3. spostare il ramo beta dentro le SCC come certificato defect-current su tutta la componente,
   non come post-processing di singoli cicli.

Se il refinement aggiunge celle T3' fino a decidere il witness, il prossimo bordo arriva da
altri discriminanti. Quindi il budget va fissato prima. Per questa sessione la stop rule e':
gate-zero FAIL -> stop prima di SCC.

## 7. Verdetto onesto

Non c'e' una prova della congettura e non c'e' emptiness certificata. Il risultato e':

```text
A0(r,K,D0) e' una riformulazione finita sound come sovra-approssimazione,
ma e' cieca rispetto a T3' gia' a r<=8 con cap naturali K,D0=80.
Qualunque classificazione SCC no-entry basata su A0 e' sospetta finche'
T3' non diventa funzione dello stato o finche' gli unknown non restano tali.
```

Il prossimo passo corretto non e' aumentare r a caso, ma definire una variante `A1` in cui
il gate-zero sia un teorema/proof object, oppure accettare che il deliverable sia una SCC/stato
avversario con T3' `unknown`.
