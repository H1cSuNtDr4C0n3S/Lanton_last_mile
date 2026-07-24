# ADDENDUM §107d — SHIELD-MAP: calibrazione sigma/griglia, mappa del deposito antico, gap non-generalizzato

**Riepilogo in una frase:** i tre strumenti programmati a §107c (F3 calibrazione,
mappa del cuneo = meta' empirica di P1b, reach sulle 59 lock-capable) sono
stati eseguiti con gate bidirezionali deduttivi tutti verdi (GF3: OR-kernel=1
su 1639/1639 canonici — T ⟺ OR=1 dalla dicotomia §101; GF2: i 2 lock a
OR=0 esatto; replay bit-per-bit; istogrammi/somme bit-identici a §107a/F3) e
il quadro di (ii) e' cambiato tre volte: (1) **la calibrazione FALSIFICA
l'aspettativa preregistrata** — la ricchezza-scudo reale di griglia e' PIATTA
in sigma_D (mediane 0.30-0.33 su tutte le bande, da sigma=1 a sigma<0.01) ⇒
la misura uniforme sui passati enumerati non ha presa dinamica e il verdetto
"lock non estremi" §107b perde la base di misura, MA nella direzione che
rafforza la conclusione: lo scudo reale e' ANTICO e word-indipendente
(trappola nuova tt); (2) la **mappa spaziale** del deposito antico (frame
ancora, x normalizzata al drift) e' una campana asimmetrica centrata sulla
posa (picco 0.42 a wx∈[−2,2]; muore a wx≈47 lato drift, ≈−58 lato opposto =
settori strutturalmente vergini misurati) e **i lock NON stanno nel settore
vergine: le loro celle (wx 0..7) cadono nel NUCLEO PIU' DENSO** ⇒ (ii) =
BUCO locale raro nel nucleo denso, non escursione nel cuneo strutturale (il
fronte del Cono delimita i settori vergini ma non cattura i lock); (3) il
**gap R_T-vs-matched dei lock NON generalizza** alla sottoclasse sigma≤0.01
(59/59 misurate a D=45-48: mediane per-parola 4 vs 4, pareggi 31/59; banda
16-50: RT>matched 6/23) ⇒ l'ombra d'albero era dei due lock-episodi, non
della classe. Bonus: alberi all'indietro QUASI-ESTINTI per alcune sigma≈0
(692-8k nodi totali a D=48).

Strumenti: `alpha1/danger_shield_calibration.py` (F3),
`alpha1/danger_wedge_map.py` (mappa), `alpha1/danger_reach_vocab.py`
(reach-59, riusa il motore C §107c senza modifiche).

## 107d.1 F3 — calibrazione sigma_D vs scudo di griglia

Preregistrata a §107c.5 (aspettativa: correlano; unita' primaria = parola
unica; bande dichiarate; nessuna soglia). Osservabile: nb = #nere in R_T(w)
al tempo del record (colori reali, frame ancora = assoluto traslato,
heading 0 assertato).

Gate: **GF0** 1639 record, istogramma |R_T| bit-identico a §107a; **GF1**
replay bit-per-bit dei turns (validazione per-passo della griglia); **GF2**
(controllo positivo KILL) i 2 lock: nb = 0/14 e 0/9 esatti; **GF3**
(deduttivo, dalla dicotomia §101 + corollario OR §107a): un canonico con
OR=0 avrebbe ride garantito ⇒ non-T ⇒ contraddizione — violazioni
**0/1639**. Tutti verdi.

Risultato (ricchezza mediana nb/n_rt per banda sigma):
sigma=1: 0.3205 (71 parole) — [0.9,1): 0.3293 (1073) — [0.5,0.9): 0.3247
(83) — [0.1,0.5): 0.2963 (112) — [0.01,0.1): 0.3208 (61) — <0.01: 0.3077
(59). **PIATTA.** L'aspettativa preregistrata e' FALSIFICATA: sigma_D non
predice lo scudo reale. Lettura: sigma_D misura la scudatura FORZATA dal
passato recente (≤22 passi); lo scudo di natura e' pittura antica, la cui
densita' (~1/3) non dipende dalla parola. Conseguenze: (a) "lock non
estremi in sigma" §107b resta vero come enunciato d'albero ma non ha
significato dinamico; (b) la conclusione finale di §107b ("(ii) =
proprieta' della pre-storia antica") esce RAFFORZATA e con il metro giusto;
(c) il verso KILL di sigma=1 (rigetto garantito, deduttivo) resta intatto —
e' measure-free.

Nota descrittiva (non enunciata, qq): a densita' ~1/3 e indipendenza naive,
P(read-set tutto bianco) per n=9-14 sarebbe ~0.5-3% — i lock osservati
(2/82k ≈ 2,4e-5) sono molto piu' rari ⇒ il deposito antico e' spazialmente
CORRELATO (scudo "spesso", §105b): i buchi sono soppressi rispetto al caso.

## 107d.2 La mappa del deposito (meta' empirica di P1b)

`danger_wedge_map.py`: densita' di nero per cella ancora (wx, cy) con
wx = cx·sign(drift_x del germe), pooled sui 1639 canonici (219.112 nere ==
F3 esatto, GW0; zero record a drift_x=0; replay bit-per-bit GW1).

Profilo laterale: campana asimmetrica centrata sulla posa — picco 0.42-0.42
a wx∈[−2,2], spalla lato drift piu' ripida (0.30 a wx=8, 0.20 a wx=20,
<0.06 da wx≈37, **zeri esatti da wx=47**), spalla opposta piu' lenta (0.34
a wx=−8, 0.24 a wx=−20, ~0.18-0.21 fino a wx=−45, **zeri da wx≈−58**).
I settori a densita' 0 sono il Lemma del Cuneo §106 che morde in natura
(garantite-vergini): il fronte del cono passato e' ora un oggetto MISURATO.

**Il fatto che ribalta la lettura di §105b:** i lock hanno drift_x=−6 e
celle ancora cx∈[−7,0] ⇒ wx∈[0,7] = il NUCLEO piu' denso della mappa
(densita' attesa 0.34-0.42; i controlli §105b nelle stesse posizioni: 45%
nere). Il lock NON e' un read-set nel settore strutturalmente vergine — e'
un **buco locale raro nel nucleo denso**. La "verginita'" §105b e' vera
per-cella (mai visitate) ma le POSIZIONI sono normalmente coperte: cio' che
manca al record del lock e' la copertura LOCALE recente-di-escursione,
non la copertura strutturale. Corollario per P1b: la formalizzazione
cono-vs-R_T uccide solo i read-set nei settori vergini (rari: la classe
direzionale ci si avvicina) ma non decide i buchi del nucleo — il fronte
del Cono NON e' il meccanismo di (ii).

## 107d.3 Reach sulle 59 lock-capable

`danger_reach_vocab.py` (motore C §107c riusato tal quale; profondita'
per-parola dal budget: D=48 per 42 parole, 45-47 per le altre; zero
non-definite). Domanda preregistrata §107c.7: il gap R_T>matched e' dei
lock o della sottoclasse?

**Risposta: dei lock.** Mediane per-parola dei gap (d_hit − D_geo):
R_T med 4 vs matched med 4 (51/50 parole con mediana finita); per-parola
RT>matched 16, pareggi 31, RT<matched 7, censurate 8. Nella banda 16-50
(nucleo lock-capable, 23 parole): RT>matched 6, pareggi 14, RT<matched 2,
cens 4. L'ombra d'albero sopra-matched dei lock (32v24, 12v4 §107c) e'
una proprieta' dei due episodi (parole piccole E direzionali E wedge-side),
non della sottoclasse sigma≈0. Domanda aperta (non testata): il gap
correla con coh_traj/direzionalita'?

Bonus: 28/59 parole hanno celle irraggiungibili-esaustive anche a D=45-48 —
ma sono le parole GROSSE (celle a D_geo grande: geometria, non ombra) — e
alcune sigma≈0 hanno alberi all'indietro quasi-estinti (nodi_C totali a
D=48: 692, 2.703, 3.897, 8.089): la validita' all'indietro puo' quasi
morire pur con la parola realizzabile in avanti. Nota per il futuro: la
quasi-estinzione e' essa stessa un candidato certificato di rigetto
(pochi passati validi = verdetto quasi-deciso), non esplorato.

## 107d.4 Stato di (ii) dopo §107d

Il fallimento dello scudo e' un evento della PRE-STORIA con queste
proprieta' misurate: (a) nessuna presa word-side (sigma piatta in griglia,
gap non generalizzato; restano taglia piccola + direzionalita' come
impronte deboli); (b) spazialmente = buco locale nel nucleo denso della
campana (~1/3), non escursione nei settori vergini; (c) piu' raro
dell'indipendenza naive ⇒ deposito correlato/spesso. L'attacco per §107e:
**statistica dei BUCHI del nucleo** — dimensione/frequenza dei cluster
bianchi locali attorno alla posa ai record (osservabile di griglia,
word-free) e la domanda di evitamento duale §105b diventa: puo' un'eterna
tenere i buchi del proprio nucleo lontani dai read-set piccoli-direzionali
per sempre? (il rifornimento §98/§104 dipinge il nucleo da solo: i buchi
sono l'eccezione che la discesa stessa ripara — quantificare il tasso di
riparazione vs il tasso di presentazione della classe).

## 107d.5 Trappole nuove

- **(tt) la quota sull'albero non e' una probabilita' dinamica**
  (SHIELD-MAP §107d): un funzionale definito contando i passati ENUMERATI
  (sigma_D, quote di rami, frazioni di foglie) non ha significato dinamico
  finche' non e' CALIBRATO contro la griglia reale — qui sigma_D (bimodale
  0→1 sull'albero) e' risultato ORTOGONALE alla ricchezza-scudo reale
  (piatta ~1/3 ovunque). Enunciati d'albero restano validi come deduzioni
  ("ogni passato valido..."); MAI leggerli come tipicita'/probabilita'
  degli eventi reali senza il gate di calibrazione. Sorella di (c) (l'albero
  sovra-approssima) e figlia dell'angolo cieco del round-1 §107c; istanza
  gemella: i d_hit SOVRA vs il passato reale che non tocca MAI (§107c).

## 107d.6 Prossimo (§107e)

1. **Statistica dei buchi del nucleo** (osservabile word-free di griglia):
   cluster bianchi locali attorno alla posa ai record; tasso di riparazione
   del rifornimento vs tasso di presentazione della classe piccola.
2. Gap-vs-direzionalita' (coh_traj) sulle 59+2 (domanda aperta 107d.3).
3. Quasi-estinzione all'indietro come certificato di rigetto (107d.3).
4. Ereditati: §106c, §105b.4, §101g, §102f, §103d, §104f, F1 gamba-Cuneo.

## 107d.7 Inventario file

- `alpha1/danger_shield_calibration.py` + `danger_shield_calibration.json`
  (+log): F3, gate GF0-GF3, bande sigma, per_word griglia.
- `alpha1/danger_wedge_map.py` + `danger_wedge_map.json` (+log): mappa
  (wx, cy), profili laterale/verticale, GW0/GW1.
- `alpha1/danger_reach_vocab.py` + `reach_vocab_sigma0.jsonl` (+log):
  triple e gap per le 59 sigma≤0.01, D per-parola dichiarato.
