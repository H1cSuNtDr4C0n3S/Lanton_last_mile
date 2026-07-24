# ADDENDUM §107d — SHIELD-MAP: diagnostica sigma/griglia, mappa condizionata, gap non-generalizzato
# [v2 CORRETTA dal pannello del titolare — v1 nel commit 718c9c1; ERRATA in 107d.0]

**Riepilogo in una frase (corretto):** sessione di buoni RISULTATI NEGATIVI —
(1) sigma_D (misura uniforme sui rami astratti a D=22) NON e' un predittore
marginale utile della ricchezza nera reale (mediane nb/|R_T| 0,30-0,33 su
tutte le bande; Spearman 0,0755 su 1459; condizionato per taglia resta in
[−0,15, 0,09]) — trappola nuova (tt); (2) il gap d'albero R_T-vs-matched dei
due lock NON e' uniforme nella classe sigma-low (48 confronti finiti: 16 >,
25 =, 7 <); (3) replay bit-per-bit + controlli OR deduttivi bidirezionali
verdi (OR=1 su 1639/1639 canonici, OR=0 esatto sui 2 lock) = macchinario di
lettura-griglia validato. Le CONCLUSIONI interpretative della v1 ("scudo
antico word-indipendente", "deposito correlato", "lock nel nucleo piu'
denso", "fronte del Cono escluso", "zeri strutturali", classe "lock-capable")
sono RITIRATE (107d.0): il valore della sessione e' aver potato sigma e il
gap, non aver identificato il meccanismo dello scudo. La riduzione a Link 1
in roadmap era inoltre logicamente LACUNOSA (quantificatori + orizzonte del
kernel): corretta in CHAT_HANDOVER §C; prossima mossa unica = kernel esteso
R_{T,104} + last-paint cutset + gate-zero (107d.6).

Strumenti (DIAGNOSTICA DESCRITTIVA, non certificati):
`alpha1/danger_shield_calibration.py` (F3), `alpha1/danger_wedge_map.py`
(mappa condizionata), `alpha1/danger_reach_vocab.py` (reach sigma-low).

## 107d.0 ERRATA (pannello del titolare, accolto; claim verificati in sessione)

1. **"Lock nel nucleo piu' denso" = artefatto di marginalizzazione
   (Simpson).** Il profilo laterale marginalizza su cy; i lock concentrano
   le celle sulle righe giovani cy=1,2 a densita' bassa. Alle coordinate 2D
   effettive (verificato dalla mappa): LOCKA media 0,192 / med 0,191 /
   range 0,036-0,394; LOCKB media 0,120 / med 0,087 / range 0,027-0,295 —
   NON il picco marginale 0,34-0,42. Enunciato lecito: ascisse normalizzate
   centrali, coordinate 2D spesso in regioni a bassa densita'. §105b NON e'
   ribaltato; il fronte del Cono NON e' escluso. Trappola nuova (uu).
2. **"Scudo antico / word-indipendente" NON dimostrati.** F3 registra solo
   il colore al record: per "antico" servono ultima visita e ultimo
   bianco→nero; per "word-indipendente" servono repliche della stessa parola
   in episodi indipendenti (1393/1459 parole hanno UNA presentazione).
   Ritirati.
3. **"Deposito spazialmente correlato" NON dimostrato.** Il confronto
   2/82k ≪ (2/3)^n usa il denominatore sbagliato (82k = tutti i record, non
   le presentazioni eleggibili a pari n; p=1/3 uniforme non e' la marginale
   per-coordinata; niente unita'-episodio ne' incertezze). Possibilita',
   non risultato. Ritirato.
4. **"Falsificazione completa del test preregistrato" → "aspettativa
   qualitativa non supportata".** La preregistrazione parlava di
   correlazione ordinale ed episodi; il tool ha riportato mediane per bande
   con collasso per parola. Il dato (associazione debole: Spearman 0,0755;
   condizionata ~[−0,15, 0,09]) supporta la versione debole dell'enunciato.
5. **"Lock-capable" eliminato.** Nei dati delle 59 parole sigma<=0.01:
   32 hanno open=cap, 13 hanno cap=1, 0/59 hanno white_all>0 (verificato).
   sigma≈0 = ASSENZA DI CERTIFICATO NERO entro D=22 (massa indecisa), non
   certificato bianco ne' vicinanza al lock. Nome corretto: **sigma-low**
   ("bassa scudatura recente certificata"). L'unico estremo deduttivo
   robusto resta sigma=1 ⇒ ogni passato valido al cap contiene uno scudo
   nero; i valori intermedi dipendono dalla misura uniforme e dalla massa
   open (trappola tt).
6. **"Zeri strutturali" ritirato.** La mappa registra colori, non storie di
   visita: bianca ≠ vergine (mai visitata O visitata un numero pari di
   volte); GW2 era dichiarato ma non implementato. Inoltre la mappa misura
   P(nero | c ∈ R_T(w)) — condizionata dalla geometria dei read-set e
   pesata dalle parole grosse — non la densita' del campo attorno alla posa.
7. **GW0 non e' bit-identico**: il totale F3 e' ricostruito da `ricchezza`
   ARROTONDATA e confrontato con tolleranza 0,1% (nel run: coincidenza
   esatta 219.112, ma il check e' "coerente entro tolleranza"). Per
   identita' esatta va salvato nb_sum intero in F3.
8. **Conteggi reach-59 corretti**: 31/59 con tutte le celle raggiunte al
   cap; 28/59 con >=1 non raggiunta; confronti con ENTRAMBE le mediane
   finite: 48 → R_T>matched 16, uguali 25, R_T<matched 7; piu' 6 cens==cens
   (non sono pareggi numerici), 3 matched-cens, 2 rt-cens. Profondita'
   variabili 45-48 dichiarate. La conclusione qualitativa (nessun gap
   uniforme di classe) resta.
9. **"Alberi quasi-estinti = candidato certificato di rigetto" ritirato.**
   692 nodi a D=48 = poche estensioni dell'astrazione a quel cap; la parola
   e' osservata in una storia reale, quindi almeno una pre-storia esiste.
   Nessun contenuto deduttivo senza un enunciato booleano (estinzione
   completa con prova di chiusura / scudo universale / certificato
   induttivo). Pista chiusa senza quello.
10. **Riduzione a Link 1 in roadmap: LACUNA LOGICA (prioritaria).** La forma
   "(i) classe i.o. ∧ (ii) fallimento scudo su UNA presentazione ⇒ Link 1"
   e' falsa nei quantificatori: un fallimento = un episodio, non lock
   profondi i.o. E l'OR-kernel attuale copre solo il transiente fino a
   onset_germe: OR=0 ⇒ d(t) >= onset_germe(w), che puo' dare ride ZERO —
   nemmeno OR=0 i.o. implica Link 1. Forma sufficiente corretta:
   **#{t : presentazione di classe κ a t ∧ ride(t) = d(t) − onset_germe(w_t)
   >= L_0} = ∞** (o la versione con ingresso permanente). Serve il KERNEL
   ESTESO R_{T,L}(w) = tutte le letture esogene necessarie fino a
   onset_germe(w) + L, col gate: R_{T,L} interamente compatibile ⟺
   d(t) − onset_germe >= L. Corretta in roadmap; precede ogni §107e.
11. Semantica del segno in `danger_wedge_map.py` uniformata (il commento
   descriveva il cuneo a wx<0; con drift_x<0 e cx<=0 i lock hanno wx>=0).

## 107d.1 F3 — diagnostica sigma_D vs griglia (declassata a descrittiva)

Osservabile: nb = #nere in R_T(w) al record (colori reali, frame ancora).
Gate meccanici: GF0 istogramma bit-identico §107a; GF1 replay bit-per-bit;
GF2 lock nb=0/14 e 0/9 (controllo KILL); GF3 deduttivo OR=1 su 1639/1639
(T ⟺ OR=1 da §101). Tutti verdi — il MACCHINARIO è validato.

Dato: mediane nb/|R_T| per banda sigma: 0,3205 / 0,3293 / 0,3247 / 0,2963 /
0,3208 / 0,3077 (da sigma=1 a <0,01); Spearman 0,0755 (n=1459),
condizionato per taglia ~[−0,15, 0,09]. Enunciato supportato: **sigma_D non
e' un predittore marginale utile della ricchezza nera reale** (trappola tt).
Il verso KILL di sigma=1 (rigetto garantito, deduttivo) resta intatto.
Che cosa NON segue: antichita', word-indipendenza, universalita' della
pre-storia (vedi 107d.0.2-3). Per "antico" servono ultima-visita e ultimo
bianco→nero per cella (strumento del kernel esteso, 107d.6).

## 107d.2 Mappa condizionata del nero ai read-set (declassata a descrittiva)

`danger_wedge_map.py`: P(nero | c ∈ R_T(w)) per cella ancora (wx, cy),
wx = cx·sign(drift_x), pooled 1639 record; GW0 coerente entro tolleranza
(219.112 == ricostruzione F3 nel run), GW1 replay bit-per-bit. Profilo
laterale: campana asimmetrica (picco ~0,42 a wx∈[−2,2]; densita' <0,06 da
wx≈37 lato drift, code a zero osservate oltre wx≈47 / −58 — ZERO CAMPIONARI
di una misura condizionata, non certificati di verginita'). Alle coordinate
2D dei lock (righe giovani cy=1,2): densita' medie 0,19 (A) / 0,12 (B) —
regioni a bassa densita' (107d.0.1). Uso legittimo della mappa: baseline
condizionata per futuri confronti per-riga/per-parola; nessun enunciato
strutturale.

## 107d.3 Reach sigma-low (conteggi corretti in 107d.0.8)

59/59 misurate (D per-parola 45-48 dichiarato, zero non-definite; motore C
§107c riusato tal quale). Domanda §107c.7: il gap R_T>matched e' dei lock o
della classe? **Dei lock** (16>/25=/7< sui 48 confronti finiti; banda 16-50:
6>/…). Struttura della classe sigma-low: 32/59 open=cap, 13/59 cap=1,
0/59 white_all — sigma≈0 = massa indecisa, non passati-bianchi (107d.0.5).
Domanda aperta (non testata): gap vs coh_traj/direzionalita'.

## 107d.4 Stato di (ii) dopo la correzione

Fatti sopravvissuti: lo scudo ai record e' fenomeno reale con ricchezza
mediana ~1/3 sui read-set canonici, poco predetto da sigma_D; i due lock
sono episodi con read-set piccoli, direzionali, su righe giovani a bassa
densita' condizionata, con celle mai lette dal passato reale fino al seme
(§107c) e gap d'albero sopra-matched NON condiviso dalla classe. Il
MECCANISMO dello scudo (e del suo fallimento) resta NON identificato:
antichita', correlazione spaziale e word-indipendenza sono ipotesi da
certificare col kernel esteso (107d.6), non fatti.

## 107d.5 Trappole nuove

- **(tt) la quota sull'albero non e' una probabilita' dinamica** (§107d):
  un funzionale contato sui passati ENUMERATI (sigma_D, quote di rami)
  non ha significato dinamico finche' non e' calibrato contro la griglia
  reale — sigma_D (bimodale sull'albero) ha associazione DEBOLE con la
  ricchezza nera reale (Spearman 0,0755; bande piatte ~0,32). Gli enunciati
  d'albero restano deduzioni ("ogni passato valido..."); mai leggerli come
  tipicita'/probabilita' di eventi reali. In piu': sigma≈0 = assenza di
  certificato nero (massa open), NON certificato bianco — nominare le
  classi per cio' che l'astrazione certifica davvero. Sorella di (c),
  gemella di (ss).
- **(uu) il profilo marginale non localizza gli estremi congiunti**
  (§107d, Simpson): un evento puo' stare al picco della marginale e in una
  valle della congiunta ("lock nel nucleo denso": marginale-wx 0,42, densita'
  2D reale 0,19/0,12 sulle righe giovani). Dichiarare estremita'/tipicita'
  SOLO alle coordinate complete dell'evento; ogni collasso di coordinate va
  giustificato PRIMA del verdetto. Parente di (oo) (per-cella vs per-evento)
  e di (h).

## 107d.6 Prossima mossa unica (vincolante per §107e)

NIENTE altre statistiche marginali. Prima si ripara l'oggetto logico:

1. **Kernel esteso R_{T,L}(w)**: tutte le letture esogene necessarie fino a
   onset_germe(w) + L. Gate fondante (deduttivo, da certificare):
   R_{T,L}(w_t) interamente compatibile ⟺ d(t) − onset_germe(w_t) >= L.
   Solo questo kernel e' agganciato alla profondita' richiesta da Link 1.
2. **Forense per-mismatch**: mai visitata / ultima visita / ultimo
   bianco→nero / colore letto e lasciato / epoca-record dell'ultima pittura.
3. **Ipotesi da attaccare: last-paint cutset** — ogni nero che scuda il
   kernel esteso proviene da un evento causale che attraversa un cut
   spazio-temporale; l'ordine (ben fondato) o la non-riusabilita' degli
   attraversamenti deve impedire di scudare tutti i record pericolosi
   tardivi. Si cerca un ORDINE, non un'altra densita'.
4. **Test minimo prima di ogni campagna** (L=104, i 2 lock + controlli T
   appaiati, nessuna soglia appresa dai risultati). Gate: (1) equivalenza
   esatta kernel-compatibile ⟺ ride>=104; (2) determinacy/gate-zero dello
   stato usato (lezione §75); (3) distinzione esatta bianco/vergine;
   (4) cut definito PRIMA di guardare il verdetto; (5) un controesempio a
   monotonia/non-riusabilita' uccide l'ipotesi; (6) informazione fuori
   astrazione ⇒ unknown, mai no-entry.
5. **Se il gate fallisce**: consolidamento dei teoremi locali (roadmap
   §C.4), non un'altra campagna empirica.

## 107d.7 Inventario file

- `alpha1/danger_shield_calibration.py` + `.json` (+log): F3 descrittiva,
  gate GF0-GF3 (macchinario validato).
- `alpha1/danger_wedge_map.py` + `.json` (+log): mappa condizionata
  P(nero | c ∈ R_T), GW0 entro tolleranza, GW1.
- `alpha1/danger_reach_vocab.py` + `reach_vocab_sigma0.jsonl` (+log):
  triple/gap sigma-low, D 45-48 per-parola.
- v1 di questo addendum: commit 718c9c1 (conservato per riproducibilita').
