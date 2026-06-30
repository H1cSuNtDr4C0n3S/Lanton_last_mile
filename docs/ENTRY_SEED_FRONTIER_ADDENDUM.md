# Entry Seed Frontier Addendum (§76)

Riepilogo in una frase: la mappa inversa della formica e' deterministica e verificata (round-trip
esatto su 12000 passi), e su questa base la doppia frontiera del seme minimo d'ingresso e'
calcolata e certificata; il risultato falsifica l'intuizione "ingresso rapido => seme complesso"
(una sola cella entra in 310 passi) e fissa il germe minimo globale a 13 celle (onset 0), ma tutto
resta interno al bacino e non muove Link 1 / alpha1.

## 76.1 Obiettivo

Riformulazione proposta da Michael (cambio di punto di vista rispetto alla catena §57-§75). Due
domande sul *seme*, non sul controfattuale eterno:

- **Q1** — il seme minimo che fa entrare la formica in autostrada nel **minor numero di passi**
  (ingresso piu' rapido);
- **Q2** — il seme minimo che fa agganciare la formica all'autostrada **piu' vicina al punto di
  partenza**, indipendentemente dal numero di passi.

Scopo dichiarato: caratterizzare geometricamente la **bocca** del bacino (i germi d'ingresso),
non produrre una nuova prova di alpha1. La sessione e' di mappatura, non di chiusura del crux.

Nota su Q1 come posta letteralmente: per reversibilita' (§76.2) la sola minimizzazione dei passi
e' degenere (onset 0 ottenuto da una qualsiasi fase d'autostrada, seme grande). L'oggetto vero e'
la **frontiera di Pareto** supporto-vs-onset; il "seme minimo" e' il regolarizzatore che la rende
non banale.

## 76.2 Mappa inversa e reversibilita' (verificata)

La mappa di update e' una biiezione; l'inversa e' deterministica, UNA sola preimmagine, nessun
albero. Ricostruzione esatta dallo stato (x,y,h):

```text
p_prev = (x,y) - dir(h)
colore ATTUALE di p_prev:
  nero   => svolta R fu fatta => h_prev = h-1 ; p_prev torna BIANCO
  bianco => svolta L fu fatta => h_prev = h+1 ; p_prev torna NERO
```

Verifica (`entry_seed/reverse.py`, self-test):

```text
ENGINE AGREEMENT (Python fwd vs C, 12000 passi): True
ROUND-TRIP: griglia vuota=True  stato(0,0,0)=True
ROUND-TRIP: turni invertiti == forward[::-1]: True
Supporto a t=12000: 952 celle nere
```

Conseguenza strutturale (gia' nota a ANATOMY §14 come "alberi backward", qui resa operativa e
certificata): reverse-iterare dalle autostrade traccia SOLO orbite del bacino. Le orbite sono
classi di equivalenza disgiunte; un'eventuale orbita eterna non-highway non viene mai toccata da
nessun seme costruito per inversione. Non esiste Lyapunov contrattivo (volume conservato, Liouville):
la cattura non e' discesa di potenziale (Z e N crescono entrambi), e' combinatoria. Questo
ricolloca, in forma piu' precisa, il muro del controfattuale eterno (CLAUDE.md §1-i): non e' solo
"i dati finiti non bastano", e' la reversibilita' stessa.

## 76.3 Germe minimo per fase (le 22 porte)

Per ciascuna delle 22 fasi enterable Phi_ent = {0,16,21,24,25,26,30,31,72,83,90,91,92,93,94,97,98,
99,100,101,102,103} (Teorema della Soglia, ANATOMY §12) si costruisce il germe minimo:

1. formica in autostrada profonda da griglia vuota, snapshot a fase phi (formica + griglia piena,
   supporto ~1080 celle di traccia);
2. troncamento a raggio Chebyshev R: si tengono solo le nere entro R dalla formica, si sbianca il
   resto; R minimo per cui forward resta su W0/Wbar con onset<=2;
3. minimizzazione greedy: si toglie ogni cella finche' l'autostrada regge (onset<=2, classe W/Wbar).

Risultato (`entry_seed/germs_22.json`, ogni germe verificato 80 periodi):

```text
supporto germi per fase (celle, tutti onset 0, classe W):
  fase  0:13  16:14  21:14  24:15  25:14  26:14  30:15  31:15  72:19  83:18
  fase 90:18  91:18  92:17  93:17  94:16  97:17  98:17  99:16 100:15 101:15
  fase102:14 103:13
MIN GLOBALE: 13 celle (fasi 0 e 103)
```

Coerenza col testimone di ANATOMY §12 (fase 72: 20 celle, onset 1): qui il greedy trova 19 celle,
onset 0 — leggermente piu' stretto e nello stesso ordine di grandezza. Il germe e' l'oggetto
co-moving intrinseco gia' nominato a §72: e' la finestra auto-spazzata, non la traccia.

Trappola (§76, conferma operativa): srotolare il germe ALL'INDIETRO fa **crescere** il supporto
(ogni passo nel bianco fresco aggiunge una cella via undo-L): 13 -> 237 a k=2000. L'orbita-indietro
del germe NON contiene semi piccoli; i semi piccoli e rapidi sono orbite diverse, raggiungibili
solo in avanti. Non aspettarsi che l'inversione minimizzi il supporto.

## 76.4 Q1 — frontiera supporto vs ingresso piu' rapido

Ricerca forward a forza bruta (`entry_seed/brute.c`): semi = b celle nere nel box, formica a
(0,0,0); reset solo celle toccate; onset = match esatto a W0/Wbar con coda >=6 periodi. Minimi
ri-certificati con il motore C (`entry_seed/seed_frontier.json`):

```text
b (celle)   onset minimo   seme campione
   0          9977         (griglia vuota)
   1           310         (0,-2)
   2           162         (-1,3)(1,3)
   3           142         (1,-3)(-2,-1)(-1,-1)
   4            71         (-2,-1)(-1,0)(-1,3)(2,3)
   5            62         (1,-3)(-1,-1)(-2,0)(-3,1)(-1,1)
  13             0         germe minimo (fasi 0/103)
```

(b=1 verificato anche su box [-12,12]: 310 resta il minimo globale a una cella.)

**Falsificazione dell'intuizione "veloce => complesso".** Non c'e' dilemma severo. Una sola cella
ben piazzata entra in 310 passi (vs 9977 della griglia vuota), due celle in 162, tre in 142. La
frontiera crolla immediatamente e si appiattisce avvicinandosi al germe (142 -> 71 -> 62): il
"ginocchio" e' intorno a b=4-5 (onset ~60-70), oltre il quale aggiungere celle rende poco. Il
costo del supporto piccolo non e' migliaia di passi, sono poche centinaia.

## 76.5 Q2 — frontiera supporto vs distanza lock-start

Stesso brute, metrica = distanza Manhattan |lock - start| (start = origine). Risultato:

```text
b (celle)   dist minima   onset    seme campione
   1            3          313      (1,3)
   2            0          276      (0,-1)(1,-1)
   3            0          268      (-2,-3)(0,-1)(1,-1)
   4            0          108      (-3,-2)(-1,-1)(1,0)(3,0)
   5            0          100      (-3,-2)(-1,-1)(-2,0)(1,0)(3,0)
```

Una singola cella non si aggancia mai piu' vicino di **distanza 3**. Con **2 celle**
{(0,-1),(1,-1)} la formica torna ad agganciarsi **esattamente** sul punto di partenza (distanza 0,
onset 276). Quindi il seme minimo che chiude il cerchio sulla casa di partenza ha supporto 2, e per
Q2 batte il germe da 13 celle proprio perche' Q2 ignora il tempo: il germe e' ottimale per Q1
(onset 0) ma non per Q2 (qualunque distanza, l'importante e' il supporto minimo a distanza 0).

Q1 e Q2 sono frontiere distinte per un motivo elementare: |lock - start| <= onset (la formica si
muove di 1/passo), quindi Q2 sta sotto Q1 ma ottimizza un altro punto. Q1 premia "marcia dritta,
blocca lontano ma presto"; Q2 premia "gira stretto, blocca anche tardi ma vicino".

## 76.6 Trappole nuove

- **(j) bordo-scarta nell'onset detection.** Bocciare la rilevazione dell'onset quando la formica
  tocca il bordo della griglia scarta un ingresso GIA' avvenuto: la highway drifta all'infinito e
  spinge la formica fuori dal box ~22000 passi dopo l'aggancio. Sintomo letale: 0% di ingressi per
  semi piccoli (falso). Antidoto: rilevare l'onset sui turni raccolti fino al bordo; il bordo
  limita la coda, non invalida l'aggancio.
- **(k) late-entry vs uscita-dal-box.** Un seme che NON entra entro il cap, e un seme che entra ma
  poi esce dal box, vanno distinti onestamente. Per i minimi di onset/distanza e' irrilevante (i
  minimi sono < cap e dentro il box), ma la percentuale "% entrati" dipende dal cap: a MAXSTEPS
  piccolo molti semi lenti (es. cella singola lontana, (7,-7)->106258) risultano "non entrati".
- **(l) inversione non minimizza il supporto.** Vedi §76.3: l'orbita-indietro di un germe cresce
  in supporto. Per trovare semi piccoli serve la ricerca forward, non l'inversione.

## 76.7 Limite logico (Faraday-Maxwell)

Tutto §76 vive nel bacino. Per reversibilita' (§76.2) l'eventuale orbita eterna non-highway sta in
una classe disgiunta che nessuno di questi semi tocca. Quello che §76 fa e' **raffinare la bocca**:
il germe critico e' ora un oggetto concreto e misurato (~13 celle, la finestra auto-spazzata
minima), non la formula vaga "lock W0-like arbitrariamente profondi". Questo precisa l'**enunciato**
di Link 1 — "ogni orbita eterna deve prima o poi contenere QUESTO germe" — ma non lo dimostra:
l'inevitabilita' "infinite volte" resta la parte dura, e i dati finiti non la danno. E' progresso
sulla formulazione, non sul lato gia' fatto. Coerente con §66 (identificare la porta e' locale,
decidere se la porta vera entra e' globale) e §72 (l'oggetto giusto e' nel frame co-moving).

## 76.8 Lettura strategica / prossimo fronte

Questa sessione non sostituisce la priorita' §76-da-roadmap (A1 con T3' deterministico / propagare
unknown). E' un ramo di mappatura della bocca, con tre agganci utili al fronte principale:

1. **Riformulazione "germe critico" di Link 1.** Caratterizzare la finestra minima la cui comparsa
   *forza* l'ingresso (non solo lo consente): l'inevitabilita' di quel germe e' esattamente alpha1
   nella forma linguaggio-teorica di ANATOMY §14, ora con bersaglio concreto.
2. **Il pavimento dell'onset.** Domanda aperta netta: esiste un onset minimo non-nullo per ogni
   supporto b? La frontiera ha un inviluppo inferiore duro (b celle non possono entrare prima di
   f(b) passi)? Se si', f(b) e' un invariante combinatorio della bocca.
3. **Connessione al canale T3'/dogane.** Il germe e' l'oggetto co-moving (§72); la macchina
   door-defect/checklist (§61-§74) e' la domanda "la porta vera entra". Unire i due livelli e' la
   forma sana del Link 1, non un tasso.

Non riaprire come strada per decidere alpha1 via simulazione: stesso muro del controfattuale eterno.

## 76.9 Inventario file

- `docs/ENTRY_SEED_FRONTIER_ADDENDUM.md` — questo addendum (§76).
- `entry_seed/reverse.py` — mappa diretta/inversa sparsa + self-test round-trip (12000 passi).
- `entry_seed/clib.py` — loader autosufficiente di `code/libant.c` + onset/classify/lock.
- `entry_seed/germ.py` — costruzione germe minimo per fase (troncamento raggio + greedy).
- `entry_seed/germs_22.json` — i 22 germi minimi certificati (min globale 13 celle, fasi 0/103).
- `entry_seed/brute.c` (+ `brute`) — ricerca forward dei semi minimi; reset-touched; fix bordo-scarta.
- `entry_seed/make_summary.py` — ri-certifica i campioni col motore C e scrive il riepilogo.
- `entry_seed/seed_frontier.json` — frontiere Q1/Q2 ri-certificate (output macchina).
- `entry_seed/figura.py` (+ `frontiera_semi.png`) — figura: frontiera Pareto + griglie dei campioni.
- Self-test richiamato: `entry_seed/reverse.py` (round-trip); riferimenti motore C vuota->9977,
  (7,-7)->106258.
