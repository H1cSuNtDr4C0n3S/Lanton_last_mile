# ADDENDUM §89 — RECORD-WORD CENSUS (sessione in corso)

## 89a. Le parole reali ai record y-min delle 24 orbite

**Riepilogo in una frase:** le parole che le orbite reali presentano davvero ai record
sono LONTANE dal minimo vivo (burden1 mediano ~317 a K=101, minimo 12; mai <= 6; zero
match con w101), MA il meccanismo del Cono e' verificato in natura senza eccezioni
(1620/1620 record lontani dall'onset hanno almeno una cella-residuo nera) e in tre casi
l'orbita e' passata a UNA sola cella nera dall'ingresso: l'osservabile giusto per l'anello
di occorrenza non e' la parola a fardello basso, e' il CONTEGGIO DELLE COLPEVOLI.

Strumento: `alpha1/record_word_census.py` (+`_summary.json`, `.log`; Ryzen, 14 s).
Metodo: per ciascuna delle 24 orbite lunghe (semi da `dumps_all.txt`), corsa fino
all'onset con rilevazione dei record y-min STRETTI pre-onset (assert heading=su
all'arrivo, 24/24 gate onset == header dumps); censiti solo i record sotto il bbox del
seme (semipiano davanti bianco garantito); per ogni record la parola delle ultime K
svolte (K = 18, 101), burden1/residuo via `eval_word`, e replay con lettura dei colori
REALI delle celle-residuo al tempo del record.

**Numeri (1639 record censiti, 52-99 per orbita, early scartati 5-348):**

- burden1 a K=101: min 12, mediana 317, max 3956; nessun record <= 6; a K=18: min 20,
  mediana 273 (il minimo astratto record-compatibile a K=18 e' 10, §87d: le parole REALI
  restano sopra anche il pavimento astratto).
- match esatti con w101 (copre tutta la famiglia sigma^m*tau*w101): **0** su 1639.
- parole a burden1=0 ai record: **0** (come il Teorema §88 esige per record lontani
  dall'onset); eval senza onset: 0.
- **TRIPWIRE DEL TEOREMA, 1620/1620:** per ogni record con t_on - t > onset_germe + P,
  almeno una cella del residuo e' risultata NERA nei colori reali. Zero violazioni: il
  meccanismo Cono+Finestra-K+Replay tiene su dati reali, non solo in astratto.
- Colpevoli (celle-residuo nere) ai record: scalano col burden, ma la coda bassa esiste:
  **3 record con UNA sola colpevole** (2 a burden 13, 1 a burden 31) — orbite passate a
  una cella dall'ingresso, l'evento-pigeonhole osservato in natura.

**Lettura onesta (anello 1 della chiusura):** l'ipotesi "parole vive a fardello basso
inevitabili ai record" NON e' supportata a questa scala: le parole reali ai record del
caos hanno fardello di centinaia. Caveat di survivorship (trappola h): queste 24 orbite
sono selezionate per onset alto (~250-313k) — proprio le orbite i cui record NON
convertono; la lettura e' within-orbit. Riformulazione produttiva per §89b: studiare la
DINAMICA del conteggio delle colpevoli fra record consecutivi (quanto spesso scende a 1?
cosa succede alla cella colpevole superstite fra un record e il successivo? eta' delle
colpevoli vs lag K della pre-semina §87.7c).

Inventario: `alpha1/record_word_census.py`, `record_word_census_summary.json`,
`record_word_census.log`.
