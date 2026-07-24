# ADDENDUM §107e — KERNEL ESTESO: R_{T,104} certificato, H-NR uccisa, verso il consolidamento

**Riepilogo in una frase:** la mossa unica §107d.6 e' stata eseguita per
intero — (1) il KERNEL ESTESO R_{T,L}(w) (prime-letture esogene del germe a
y_rel>=1 con tf < onset_germe+L) e' meccanizzato a L=104 e il suo gate
fondante e' CERTIFICATO: `R_{T,104} interamente compatibile ⟺ ride = d −
onset_germe >= 104`, per-record su 1639 canonici + 2 lock (T-DIV §101 esteso
all'orizzonte H: d per-svolte == min-tf-nera per-celle su OGNI record con
scudo; zero unknown; regressioni bit-esatte: d CSV §101 1639/1639, d_full
lock 324/449) — l'oggetto record-side di Link 1 nella forma corretta dei
quantificatori (§107d.0.10) e' ora word-decidibile e agganciato alla
profondita' giusta; (2) la forense last-paint con distinzione esatta
bianco/vergine (gate 3, storia delle visite) da': kernel estesi dei lock
**66/67 celle VERGINI** (mai visitate, non seme) **+ 1 visitata-pari**
(LOCKA — la cella consumata di §105b, ritrovata dal terzo macchinario
indipendente), first-bad dei canonici a n_vis med 1, 50 da-seme; (3)
**l'ipotesi H-NR (last-paint cutset per non-riusabilita' stretta) e' UCCISA
al primo contatto** (gate 5, aspettativa di morte dichiarata in
preregistrazione): 103.980 eventi-scudo, 55.359 riusati da >=2 record,
37.116 da record NON consecutivi — il riuso degli attraversamenti e' la
NORMA; con il riuso maggioritario e non-locale, anche un ordine ben fondato
basato sul non-riuso e' senza appiglio. **Per la regola decisionale
preconcordata (§107d.6.5): prossima mossa = CONSOLIDAMENTO (roadmap §C.4),
nessuna nuova campagna empirica** salvo un invariante d'ordine di natura
diversa.

Strumento: `alpha1/kernel_extended.py` (+ `kernel_extended_summary.json`,
log). Convenzioni: og dal record (asse assoluto og+101, §107b.6);
profondita' in passi germe-tempo (i=0 ↔ t); epoche = indici nella lista
completa dei record y-min dell'orbita.

## 107e.1 Definizione e gate (preregistrati nell'header dello strumento)

R_{T,L}(w) = { (c, tf) : prima-lettura del germe (fr di `germ_long_run`),
tf < H = onset_germe+L, c fuori footprint(w), c_y >= 1 }. Le esogene a
c_y <= 0 sono auto-valide per record y-min stretto sotto il seme (deduzione
§101); il footprint e' word-determinato. Regressione interna: la
restrizione tf < og coincide col `transient_readset_from_germ` §106 su ogni
parola (assert).

GATE 1 (equivalenza, per-record): d_a = primo indice di svolta divergente
(gturns vs turns[t:]); d_b = min tf delle celle di R_{T,104} NERE al record.
Certificato: (a) kernel tutto bianco ⇒ nessuna divergenza in [0,H);
(b) altrimenti d_a == d_b; (c) compatibile ⟺ ride >= 104. Esito: **verde su
1641/1641**, unknown 0 (gate 6 mai attivato: svolte sempre disponibili).
GATE 2 (determinacy): verdetto = funzione di (parola, colori di R_{T,104}
al record); nessun altro input. GATE 3: forense su storia visite, non
colori. GATE 4: cut preregistrato prima dei verdetti (107e.3). GATE 5: un
controesempio uccide. Copertura DICHIARATA della biconditionale: la
direzione ⟸ (compat ⇒ ride>=104) ha 2 soli positivi nei dati (i lock); la
banda 0 <= ride < 104 e' VUOTA nel campione (1639/1639 canonici hanno
d < og, coerente con §101); la deduzione (Lemma 0 §101 + auto-validita'
c_y<=0) copre cio' che il campione non popola.

## 107e.2 Forense last-paint (gate 3)

- **Kernel estesi dei lock** (36 celle A, 31 B — il kernel esteso aggiunge
  al transiente le esogene del ride fino a og+104): LOCKA 35 vergini +
  **1 visitata-pari** (bianca per consumo, non per verginita' — e' la cella
  consumata a eta' 102 di §105b: terza conferma cross-macchinario dopo
  §105b e GB §107b); LOCKB 31/31 vergini; zero celle di seme. La
  distinzione bianco/vergine e' operativa e NON vuota (1/67).
- **First-bad dei 1639 canonici**: 50 da-seme-mai-dipinte; eta' dell'ultima
  pittura med 451 passi / max 138.199; in epoche-record: gap_ep med 2 /
  max 8 (due orologi riportati, trappola nn; il max 8 e' un QUANTILE del
  campione, non una costante — qq); n_visite med 1 (dipinte una volta, mai
  consumate).

## 107e.3 H-NR: morte al primo contatto (gate 5)

Preregistrazione (gate 4, nell'header prima di ogni verdetto): CUT = fronti
delle epoche-record; attraversamento = evento di ultima pittura (cella,
last_W2B) di una cella-scudo del kernel esteso; H-NR = nessun evento scuda
i kernel di due record distinti; aspettativa dichiarata di morte (colpevoli
condivise §98/§100). Esito: **103.980 eventi, 55.359 riusati (53%), di cui
37.116 da record non consecutivi** — H-NR falsificata in massa, non al
margine. Lettura: lo scudo e' un bene RIUSABILE e non-localmente riusabile;
qualunque argomento "ogni record pericoloso consuma una risorsa di scudo
fresca" e' contraddetto dai dati al livello del kernel esteso (parente
della trappola n: il consumo non e' il collo). Un ordine ben fondato
dovrebbe poggiare su una quantita' DIVERSA dal non-riuso degli
attraversamenti; nessun candidato naturale sopravvive a questo dato.

## 107e.4 Decisione (regola preconcordata §107d.6.5)

Il test minimo ha dato: gate fondante CERTIFICATO (il macchinario e
l'oggetto logico sono sani), ipotesi meccanicistica MORTA (H-NR). Come
concordato: **niente nuova campagna empirica; la prossima sessione e' il
CONSOLIDAMENTO** (roadmap §C.4) — scrittura organica dei teoremi locali
(locale sigillato, γ<=40, finestra r<=4, prodotto sound, U1/Muro, Scala,
Cuneo/Limite di Velocita', Dicotomia del Record §101, kernel esteso §107e)
come riduzione a α1∧β∧γ + macchina, senza chiudere il crux. Il kernel
esteso certificato e' il punto d'arrivo giusto del filone record-side: la
quantita' di Link 1 e' #{t: classe-κ ∧ ride(t)>=L_0} = ∞, e ride>=L e' ora
un predicato word+griglia esatto. Riapertura del fronte empirico solo con
un invariante d'ordine nuovo (proposta esplicita, preregistrata).

## 107e.5 Trappole

Nessuna lettera nuova: la sessione ha applicato (qq)/(nn)/(tt)/(uu) e le
regole §107d.6 senza incidenti; il bug di regressione (d del lock oltre H
censurato dal gate) e' stato un errore d'assert riparato in-sessione e
documentato nel log, non una trappola concettuale.

## 107e.6 Inventario file

- `alpha1/kernel_extended.py` + `kernel_extended_summary.json` (+log):
  kernel esteso L=104, gate 1-6, forense per-record, dettaglio pieno per i
  2 lock, eventi H-NR con esempi.
- v. anche: docs/SHIELD_MAP_ADDENDUM.md (v2, ERRATA §107d.0) per il
  contesto della correzione che ha imposto questa sessione.
