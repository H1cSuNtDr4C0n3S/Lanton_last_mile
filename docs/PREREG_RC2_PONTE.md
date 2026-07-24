# PREREG RC2 — IL PONTE SCIA forward→backward (Fase 0b, pre-§109)

**Statuto (vincolante):** preregistrazione dell'ENUNCIATO e dell'AUDIT
dell'antecedente per il lemma-ponte RC2 (mandato del titolare post-Fase 0,
verdetto 2026-07-25: "enunciato matematico RC2 con audit dell'antecedente;
macchina soltanto dopo"). NON asserisce il ponte, NON contiene risultati,
NON costruisce macchine, NON tocca la Fase 1 (chiusa: mancano ancora le 8
milestone quantitative per-firma). Requisiti operativi ereditati
dall'ERRATA classificatoria di Fase 0: ogni checker di Fase 0b usa
CONTROLLI ESPLICITI (niente assert nudi: fail-open sotto `python -O`) e
registra `sys.flags.optimize == 0` nel summary.

## 0. Oggetto e posta in gioco

RC2 (docs/PREREG_RIENTRO_SCIA.md §1) vuole usare il Teorema della Scia
(§86.1, A-T5) sul camminatore all'indietro ai punti di uscita/rientro.
§86.1 è certificato in dinamica FORWARD con antecedente ESATTO: "t lettura
NERA deep₁ (cella VISITATA, fuori dalla finestra viva 3×3)". Il verdetto
post-Fase 0 fissa il punto: le due firme a genitore esterno individuate
dalla Fase 0 ((−2,2) h=1 e (2,2) h=0, unica sorgente
`alpha1/prereg_fase0_geometry_summary.json`) sono bersagli SOLO
CONDIZIONATAMENTE — il vantaggio esiste se il bordo-genitore può essere
identificato con un evento cui si applica DAVVERO l'antecedente della
Scia; "essere un rientro" da solo non basta.

## 1. Lemma 0b.0 — corrispondenza temporale backward–forward (da certificare)

Enunciato da dimostrare (nessuna parte è asserita qui). Sia P un passato
completo che presenta w101 a un record y-min stretto (frame anchor: posa
finale in origine, heading-su; convenzione bit §95b: 1 = R = lettura
BIANCA, 0 = L = lettura NERA), di lunghezza totale T = 101 + N (N =
numero di prepend). Allora per ogni k ∈ [1, N]:
- (i) il k-esimo prepend del camminatore corrisponde al passo forward di
  indice j(k) = N − k + 1 (il prepend più profondo = il passo più
  antico dell'orbita);
- (ii) la cella letta dal prepend k (cn = posa − D[h], §97a) è, nel frame
  anchor, la cella letta dal passo forward j(k);
- (iii) posa e heading del camminatore al depth k determinano posizione e
  heading forward a j(k) tramite una mappa esplicita DA SCRIVERE nel
  lemma (inclusa la convenzione di verso backward vs forward);
- (iv) la lettera del prepend è la svolta del passo forward j(k), e il
  colore letto forward coincide col colore richiesto dal req backward.
Metodo: deduzione dalle definizioni del camminatore (§92a, §95b) + gate
di terra OBBLIGATORIO: replay forward dei 10 controesempi §94 e di ≥ 100
estensioni casuali, confronto passo-passo bit-identico (stile N4/§97e).
Una divergenza qualsiasi = lemma rosso.

## 2. Lemma 0b.1 — audit dell'antecedente (il cuore, falsificabile)

**Marcatura candidata M1 (fissata QUI, prima di ogni run; ogni modifica =
nuova preregistrazione):** un prepend k è RC2-marcato se, sul SOLO stato
backward dichiarato: (a) la lettera è L (lettura nera); (b) la cella
letta è fuori dalla finestra viva 3×3 del passo forward corrispondente,
ricostruita dalla geometria d'arrivo delle ultime ≤ 3 svolte del
camminatore (la stessa induzione all'indietro di §86.1, che è geometria
pura delle svolte); (c) la componente "VISITATA" è decisa come sotto —
o dedotta, o il punto è `unknown` e NON è marcato.

Decidibilità backward delle tre componenti dell'antecedente:
- **NERA:** decidibile (lettera L ⟺ lettura nera, semantica req §92a);
- **FUORI FINESTRA 3×3:** da dimostrare backward-decidibile dalla
  geometria delle ultime ≤ 4 posizioni del camminatore (candidato:
  ricostruzione d'arrivo §86.1); se la ricostruzione richiede
  informazione non dichiarata ⇒ `unknown`;
- **VISITATA (la componente INSIDIOSA, nominata dal verdetto):**
  "visitata al passo forward j(k)" = visitata da passi PIÙ ANTICHI =
  prepend PIÙ PROFONDI di k, che il camminatore al depth k NON ha ancora
  costruito. NON è backward-decidibile in generale. Vie ammesse: dedurla
  dal ledger (semantica pending §93a: L su pending irrealizzabile;
  pending finali = seme nero visitato, T20 §92e/§93a) sotto le ipotesi
  del record (palla senza seme e senza origine); se la deduzione non
  chiude ⇒ il punto è `unknown` e RC2 NON si applica lì. Questo è il
  punto dove il ponte può morire (esito UNKNOWN-DOMINATO, sotto).

**PONTE (enunciato da certificare):** ogni prepend RC2-marcato da M1
soddisfa, nel replay forward, l'antecedente esatto di §86.1: lettura
nera ∧ cella visitata ∧ fuori dalla finestra viva 3×3.
**FALSIFICATORE (F-0b.1):** UN SOLO stato backward ammesso dalla
marcatura il cui replay forward NON soddisfa l'antecedente ⇒ PONTE
FALSO (si riformula la marcatura con nuova preregistrazione, o si
abbandona RC2). Il testimone va riportato PRIMA di ogni assert
d'esaurimento (trappola ii).

Conseguenza dichiarata della marcatura (non un risultato): i rientri a
lettera R (lettura bianca) sono fuori marcatura per definizione — RC2,
se certificato, vincola SOLO i punti L. Se ai punti utili delle due
firme-bersaglio il traffico è R-dominato, il vantaggio condizionale
svanisce: va misurato, non presunto.

## 3. Lemma 0b.2 — località e completezza del dominio (da certificare)

Da dimostrare: il verdetto di marcatura (marcato / non-marcato /
`unknown`) è funzione di un INTORNO FINITO DICHIARATO dello stato
backward — raggio r_0b e profondità di storia d_0b ESPLICITI — cosicché
il dominio D_RC2 delle configurazioni locali ammesse ai punti candidati
è FINITO e la sua enumerazione è COMPLETA (non un campione: due
implementazioni concordi su un campione NON bastano, ERRATA-1.6). Ogni
parametro sound "per caso fattuale" va verificato con controllo
esplicito a ogni valore di raggio (trappola mm).

## 4. Gate 0b.3 — enumerazione + replay forward (solo dopo 0b.0–0b.2)

Enumerare D_RC2 per intero; per ogni elemento: replay forward e verifica
dell'antecedente con checker a CONTROLLI ESPLICITI; esca obbligatoria
(elemento corrotto ⇒ il checker DEVE fallire); tripwire CP M0–M4 sul
macchinario nuovo (trappola kk); `sys.flags.optimize == 0` registrato
nel summary. Esiti ammessi (tre, mutuamente esclusivi, emessi dal tool):
- **PONTE CERTIFICATO:** RC2 utilizzabile nelle macchine di Fase 2/3,
  RISTRETTO ai punti marcati;
- **PONTE FALSO (F-0b.1):** testimone esplicito a verbale;
- **UNKNOWN-DOMINATO:** la marcatura non copre nessun punto utile alle
  firme-bersaglio (in particolare se "VISITATA" non si deduce mai):
  RC2 inutilizzabile — esito negativo onesto, si archivia.

## 5. Cosa questo documento NON fa

Non asserisce il ponte né alcuna irrealizzabilità ¬R_f; non costruisce
macchine ("macchina soltanto dopo"); non apre la Fase 1 (servono le 8
milestone quantitative per-firma, verdetto sotto-soglia = solo
`unknown`); non modifica il Teorema della Scia (§86.1 resta forward, con
le sue ipotesi). Trappole di guardia per l'esecuzione: (c)/(z) l'astratto
non trasferisce; (ii) testimone-prima-di-assert; (kk) coniugare
l'interprete; (ll) washout; (mm) niente confronti sotto cap, parametri
assertati; (u) ogni statistica di vicinato va scontata della scia; (ee)
minimi su TUTTI i nodi quando servono.
