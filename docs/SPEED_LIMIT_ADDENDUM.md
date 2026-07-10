# ADDENDUM §106 — TEOREMA DEL LIMITE DI VELOCITA': il primo dente deduttivo sull'evitamento duale

**Riepilogo in una frase:** composizione di tre pezzi gia' dimostrati (velocita'
L1 + Scala/T3 + Lemmi 0-1 §101) in un teorema nuovo: **LEMMA DEL CUNEO** — a un
record y-min stretto ogni cella (x, k) visitata a riga y_rel=k soddisfa
|x|+k <= Delta_k (eta' in passi della riga) ⇒ le celle con |x|+k > Delta_k sono
GARANTITE-VERGINI (sotto il seme: bianche) — e **TEOREMA DEL LIMITE DI
VELOCITA'** — se TUTTO il read-set del transiente di w e' garantito-vergine,
l'orbita cavalca (d >= onset_germe, classe R/E); contrappositiva: **a ogni record
di classe T (le eterne ai record profondi) almeno una cella del read-set ha
|x|+k <= Delta_k: un vincolo di LENTEZZA della discesa, per-parola e
word-decidibile — il primo vincolo deduttivo sull'evitamento duale §105b.**
Terra-check: **T2 = 6055 celle garantite-vergini, 0 nere** (Lemma del Cuneo
verificato); **T1 = 1622 record classe T, 0 violazioni**; **T3 (onesta'):
i 2 lock reali avevano 0 celle garantite (14/9 tutte fortunate)** — i buchi
osservati sono fortuna dello scudo sottile, non velocita' forzata: l'ipotesi
del teorema non si e' ancora realizzata in natura e il dente morde solo nel
regime estremo-veloce (discese rapide alla §99).

Strumento: `alpha1/speed_limit_theorem.py` (+`_summary.json`, `.log`; 18,5 s).

## 106a. Enunciati e dimostrazioni

**Lemma del Cuneo (deduttivo).** Record y-min stretto a t, posa (0,0) rel. Per
k >= 1 sia Delta_k = t − t_open(riga y_rel=k), dove t_open e' il record che ha
aperto la riga (Scala (i)/T3 §98: la riga assoluta −m apre esattamente al record
m−1; ogni visita alla riga e' >= t_open). Se (x, k) e' stata visitata a tempo
tau, allora tau >= t_open(k) e la formica va da (x,k) a (0,0) in t−tau passi
unitari ⇒ |x| + k <= t − tau <= Delta_k. QED. Corollario (con Lemma 0 §101):
sotto il seme, |x|+k > Delta_k ⇒ mai visitata ⇒ BIANCA a t.

**Teorema del Limite di Velocita'.** Ipotesi: record profondo t con parola w,
(A) onset_germe(w) finito; R_T(w) = read-set del transiente (prime-letture del
germe < onset_germe, non-footprint, y_rel >= 1), tutte le celle sotto il seme.
Se ogni (x,k) di R_T(w) ha |x|+k > Delta_k, allora ogni lettura del transiente
del rigioco combacia col germe (celle garantite-bianche = assunzione del germe;
footprint per Finestra-K; y_rel <= 0 per Lemma 0) ⇒ per il Lemma 1 §101,
d(t) >= onset_germe: **l'orbita cavalca W0** (classe R o E). QED.
**Contrappositiva (il dente):** un'orbita che a t NON cavalca (classe T — per le
eterne ai record profondi, (E) e' vietata dal Rifornimento §98c) soddisfa
    min su R_T(w) di [ Delta_k − (|x|+k) ] >= 0,
cioe' la discesa recente e' abbastanza LENTA da coprire il read-set. Il vincolo
e' word-decidibile (R_T(w) dal germe) e per-record (Delta_k dalla scala).

## 106b. Terra-check (24 orbite, 1622 record con read-set sotto-seme)

- **T2 (Lemma del Cuneo): 6055 celle garantite-vergini interrogate nel replay,
  0 nere.** (Deduttivo ⇒ il check e' contro i bug, non contro la natura.)
- **T1 (contrappositiva): 1622/1622 record di classe T hanno almeno una cella
  del read-set NON garantita — 0 violazioni.** Margine di lentezza
  min(Delta_k − (|x|+k)): minimo assoluto −48 (esistono celle singole garantite),
  mediana +79,5; **nessun record con read-set INTERAMENTE garantito** e' mai
  stato osservato (coerente: sarebbe stato classe R/E).
- **T3 (episodi §101): 0/14 e 0/9 celle garantite** — i lock reali sono nati da
  vergini FORTUNATE (lo scudo non le aveva coperte pur potendo), non dal cuneo
  forzato. Il teorema descrive un regime (estremo-veloce) piu' profondo di
  quello gia' realizzato.

## 106c. Che cosa dice per Link 1 (onesto)

1. Primo vincolo DEDUTTIVO sull'enunciato di evitamento duale (§105b.2): il
   nemico shallow-forever non e' libero — a ogni record con parola veloce deve
   pagare lentezza (Delta_k >= |x|+k su almeno una cella). Non chiude nulla da
   solo: il nemico puo' scendere lentamente.
2. La strategia-limite del nemico e' ora stretta fra DUE obblighi quantificati:
   lentezza al record (qui) + scudo non-garantito da mantenere (i buchi fortunati
   §105b restano possibili per lui in negativo: deve EVITARLI, e §103 mostra che
   in natura capitano ~1/40k record).
3. Direzione §107: quantificare l'incompatibilita' fra i due obblighi lungo una
   discesa B-T infinita — es. il vincolo di lentezza sommato su tutte le
   presentazioni veloci vs il tasso di record forzato; oppure falsificare:
   costruire (enumerativamente) una politica di discesa lenta che tiene sporchi
   tutti i read-set veloci per sempre (se esiste come oggetto periodico, il
   bersaglio record-anchored di Link 1 e' FALSO e Link 1 va vinto fuori-record).

## 106d. Onesta' e pannello

Teorema per composizione di lemmi gia' dimostrati/pannellati (§98 Scala, §101
Lemmi 0-1, Finestra-K §87); terra-check T1/T2 con replay canonico (query
deterministiche); T3 sugli episodi con la stessa pipeline. Etichetta corretta a
verbale: nel JSON il campo "neg (tutte garantite)" conta i record con ALMENO una
cella garantita (min margine < 0), non "tutte" — refuso d'etichetta, i check T1/
T2 sono indipendenti da esso. Nessuna soglia nuova (il margine e' distribuzione,
non costante).

## 106e. Inventario file (alpha1/)

- `speed_limit_theorem.py` (+`_summary.json`, `.log`) — terra-check T1/T2/T3 del
  Lemma del Cuneo e del Teorema del Limite di Velocita'.
