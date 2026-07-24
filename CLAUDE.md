# CLAUDE.md — Progetto Langton Last Mile (C:\langton_last_mile)

Programma di dimostrazione della congettura dell'autostrada della formica di Langton.
Collaborazione con Michael Spina. **Lingua di lavoro: italiano.**

## 0. Prima di tutto
1. Leggi `CHAT_HANDOVER.md` (stato del programma, risultati, roadmap) — è la fonte di verità.
2. Se esiste `C:\Langton_research\claude.md` (l'altro progetto), leggilo e **fondi le sue
   convenzioni di parallelizzazione con la §4 qui sotto: in caso di conflitto vince quello**.
3. Non eseguire MAI run lunghe prima di aver passato i self-test (§5).

## 1. Metodologia (non negoziabile)
- Stile Faraday–Maxwell: falsificazionismo, onestà sopra validazione. Ogni ipotesi va
  attaccata, non difesa. Un risultato senza tentativo di falsificazione non è un risultato.
- Ogni numero importante va validato con almeno un check indipendente (identità interne,
  casi noti, conteggi incrociati). I valori certificati sono nei summary JSON e negli addenda.
- Verbali: si continua la numerazione dei paragrafi degli addenda (§108 CHIUSO con §108b — pannello eseguito, 17/17 decisioni applicate; prossimo: **§109**, che si apre SOLO davanti a un nuovo lemma o a un invariante d'ordine esplicito e preregistrabile, gate §107d.6).
  Ogni sessione produce un ADDENDUM nello stesso stile (riepilogo in una frase, risultati,
  trappole nuove, domande aperte, inventario file).
- Trappole note: lista cumulativa negli addenda (`docs/`). Le più letali:
  (a) **survivorship da bordo griglia** (run a onset precoce escono percorrendo la highway
      ⇒ campione distorto; antidoto: onset detection incrementale con stop anticipato);
  (b) DFS con stack condiviso: il ramo a svolta forzata DEVE fare pop come il ramo libero
      (sintomo: rapporti interi esatti tra conteggi indipendenti);
  (c) l'automa a finestra è una SOVRA-approssimazione: si trasferiscono alle orbite solo
      enunciati "ogni cammino infinito fa X", MAI "esiste un cammino che fa Y";
  (d) parole cicliche: confronti solo a meno di rotazione (funzione `canon`);
  (e) min cycle mean assumiB sul grafo pieno è banalmente 0: ha senso solo senza archi-rotore;
  (f) processi lunghi: chunking con budget temporale interno e checkpoint su disco;
  (g) **reset-hash per-seme = collo di banda di memoria** (ALPHA1 §57.7-a): in una ricerca
      parallela su molti semi, azzerare l'INTERA tabella hash a ogni seme satura la banda di
      memoria (non i thread) e fa crollare il throughput ~8×. Resettare SOLO le celle toccate
      (lista `touched`, reset O(celle) non O(tabella)). Vale per ogni sweep multi-seme;
  (h) **survivorship temporale** (ALPHA1 §57.7-b): selezionare orbite per onset alto = selezionare
      per starvation (densità bassa/stalli lunghi quasi per definizione). I tassi/pavimenti si
      leggono SOLO within-orbit, mai confrontando semi di T diverso. È la (a) nel tempo;
  (i) **controfattuale eterno** (ALPHA1 §57.6): ogni orbita simulata converge ⇒ NESSUNA soglia
      misurata sul finito prova un enunciato su orbite eterne (α1, pavimenti del tasso, ...).
      La simulazione può falsificare un meccanismo locale, non decidere α1.
  (j) **bordo-scarta nell'onset detection** (ENTRY-SEED §76.6): bocciare la rilevazione dell'onset
      quando la formica tocca il bordo della griglia scarta un ingresso GIA' avvenuto — la highway
      drifta all'infinito e spinge la formica fuori dal box ~22k passi dopo l'aggancio. Sintomo
      letale: 0% di ingressi per semi piccoli (falso). Antidoto: rilevare l'onset sui turni
      raccolti fino al bordo; il bordo limita la coda, non invalida l'aggancio.
  (k–m) vedi CHAT_HANDOVER §77/§78 (srotolare-germe, late-entry, spaziale-limitato != stato).
  (n) **deficit di consumo = pavimento-del-morso travestito** (CONSUMPTION-LEDGER §79): ogni
      lemma "consumo deep-black > rigenerazione da supporto finito" e' FALSO — le creazioni di
      nero (letture bianche, alimentate dalla frontiera B-T) sono >= distruzioni; il pool di nero
      CRESCE. Non riaprire bilancio/squilibrio di tasso del consumo (= pavimento-del-morso §57).
      La leva, se esiste, e' la coda lunga dei ritorni lontani (age >> periodo), non il bilancio.
  (o) **nessun classificatore finito-stato a raggio fisso sugli eventi deep-black** (DEEP-MOTIF
      §80, ESTESA §81): l'alfabeto dei motivi locali co-moving al detrito NON satura (r=3 ~99,4%
      unici; scoperta ultimo/primo 1,14; unione/somma tra orbite 0,979; intersezione 19/1,5M).
      §81: vale ANCHE potando il motivo alla parte causalmente attiva (celle visitate nei prossimi
      104/208 passi): scoperta 0,811, ~57% unici, unione cresce. Non riaprire checklist/
      footprint-finito/classe-co-moving SUL LATO-ALPHA, pieno o potato: finito-stato funziona
      solo sul lato-beta (porta, §78). Il lato-alpha e' irriducibilmente dinamico.
  (p) **il nucleo universale non e' un manico** (DEEP-MOTIF-PRUNED §81): esiste un vocabolario di
      1.572 motivi attivi condiviso da tutte le 24 orbite con massa eventi stazionaria ~35,6%
      (quintili piatti, ortogonale all'eta'), ma la coda aperiodica porta ~64% della massa ed e'
      la parte illimitata. Non costruire argomenti finito-stato sul nucleo sperando che la coda
      sia trascurabile: il nucleo e' un vincolo/impronta da rispettare, non una riduzione.
  (q) **il taglio nucleo/coda non segmenta la dinamica** (CORE-TAIL-PROFILE §82): la massa sul
      vocabolario universale e' invariante nel tempo (§81), per eta' e per alimentazione (§82:
      bucket eta' piatti 35–36% fino ad age>104000; morso-fed 36,9% vs recycle 35,4%). NON
      cercare la parte genuinamente aperiodica come sottopopolazione separabile di eventi (per
      eta', vc, o membership al vocabolario): la miscela e' omogenea, l'aperiodicita' abita la
      stessa popolazione che parla il dialetto universale.
  (r) **il nucleo non e' linguaggio di transito** (HIGHWAY-LANGUAGE §83): L_hw (linguaggio potato
      delle letture nere sulla highway pura) = 46 parole esatte, sature, identiche su 24/24
      orbite, ma sovrapposizione col nucleo 2/1.572 e massa deep-black pre-onset su L_hw 0,05%.
      A (r=3, H=104) caos profondo e transito sono linguisticamente disgiunti: NON costruire
      ponti alpha->beta su sovrapposizioni di vocabolario locale.
  (s) **il nucleo non ha antenati periodici noti — e (q) ha confini** (ROTOR-LANGUAGE §84):
      highway 0,05% (§83), rotori 4,5% degli eventi-nucleo con l'unica classe in eccesso (p15,
      x1,9) a massa-nucleo 0% esatto su 24/24 orbite; LRRRR evitato totalmente (0 su ~1,5M vs
      ~0,18% di caso); rotori r>=2 assenti dal caos anche alla baseline. La periodicita' di
      svolta E' il primo asse che segmenta la miscela nucleo/coda (delimita (q), che resta
      valida per eta'/vc), ma su classi minuscole: fatto strutturale, non leva quantitativa.
      Metodo obbligatorio per confronti simili: >=3 periodi pieni + baseline nulla condizionata.
  (t) **assW e' gratis** (LRRRR-HALO §85): nei certificati via automa finestra, sopravvissuti i
      cui archi di assunzione sono solo assW (bianco = default dello spazio vuoto) sono un
      campanello di REALIZZABILITA', non indizio di fantasma. Ispezionare i sopravvissuti e
      tentare il testimone diretto prima di scalare il raggio (qui: nero isolato ⇒ (LRRRR)^3,
      teorema-finestra falso ma ridotto al TEOREMA HALO ⟺ esatto: 9 celle bianche, r<=2).
  (u) **la scia d'arrivo e' gratis** (TRAIL-HALO §86): le posizioni t−1,t−2,t−3 di una lettura
      deep giacciono nell'halo posteriore e i loro colori sono funzione delle ultime 3 svolte.
      Prima di cercare un meccanismo "ambientale/termodinamico" per un enunciato di vicinato ai
      deep-event, RICOSTRUIRE ALL'INDIETRO la scia: la classe stessa (deep = fuori-finestra) puo'
      forzare l'enunciato per definizione (qui: Teorema della Scia ⟹ evitamento (LRRRR)^3 ai
      deep e' teorema per ogni orbita, incluse le eterne). Corollario pratico: ogni statistica
      di vicinato ai deep va prima scontata del contributo di scia.
  (v) **lo spoiler puo' essere la propria scia invecchiata** (CONE-LOCK §87): lo Spoiler Vecchio
      (eterna => nero d'eta'>=K entro raggio ~15-68 in ogni istante, K<=14) NON implica che il caos
      "muoia di solitudine": una cella dipinta K+1 passi fa e' gia' vecchia a scala K e il caos si
      sposta ~0 in 14 passi (rotore §77) — nessun K finito chiude per camping. Non riaprire
      argomenti "il caos resta senza neri vicini". La leva e' la geometria ai pose-record
      (burden1, Residuo dei Cinque) e il costo di pre-seminare il futuro contro B-T.
  (w) **fardello basso ≠ parola viva** (CONE-LOCK §87e-2): un teorema-parola ai record e' VACUO
      se la parola non ha estensioni all'indietro record-compatibili di profondita' arbitraria.
      I minimi senza filtro di vitalita' (2 a K=58-70, 4 a P(0)) sono tutti vacui (estinzione
      entro prof. 3-7). Certificare SEMPRE la vitalita' (catena/ciclo di prepend) prima di
      enunciare; il minimo che conta e' sul sottoinsieme vivo.
  (x) **il fondo del testimone DFS non e' il regime** (WEAPON-VITALITY §88): le lettere piu'
      profonde di un testimone early-exit sono le meno vincolate; uno scan di periodicita'
      eventuale che pretende il periodo fino all'ultima lettera boccia cicli REALI (§88: periodo
      8 con ~40 periodi osservati, invisibile a transiente 480). Antidoto: finestra periodica
      interna massima, poi ri-certificare σ,τ da zero (il testimone e' solo un suggeritore).
  (y) **collo di bottiglia ≠ forzatura eterna** (WEAPON-VITALITY §88): il muro dei prepend puo'
      essere a binario unico per un tratto finito (prof. 2..17 dietro w101) e riaprirsi
      esponenzialmente (×1.65). Dichiarare sempre fino a che profondita' l'unicita' e'
      esaustiva; non dedurre forzatura globale del passato.
  (aa) **la vitalita' all'indietro D e' una risorsa di seme travestita** (U2-POCKET §92):
      ogni parola con accesso al territorio vergine ha D=∞ (Lemma del Raggio Monotono,
      1 nero FRESCO = 1 cella di SEME ogni 2 passi; la rotaia σ di §88 paga 5/8 ⇒ anche
      D(w101)=∞ non certifica presentabilita' ai record lontani). Il tasso NON e'
      universale: la discesa in autostrada e' una rotaia infinita a costo totale O(1)
      (13 neri) ⇒ l'invariante e' il BILANCIO senza tasso (#prime-visite-della-vita-nere
      ≤ |seme_nero|). MAI credere a "D ≤ costante" senza aver attaccato con la fuga
      verso il vergine E con la discesa in autostrada. Ledger corretto: pending(c) ⟺
      prima-lettura-corrente-in-parola nera; OGNI L apre/riapre (anche su rivisitata),
      R su pending chiude — vietare solo L-su-fresco non uccide (2.918 passi, +226
      pending). Parente di (n)/(w) e del pavimento-del-morso §57.
  (bb) **i campioni best-first di estensioni sottostimano le code** (U2-POCKET §92):
      il censimento §90c vedeva 2 config di copertura e D≤4; il vero sup era ∞ (43
      config, jackpot al 20° tipo; caduta anche la "tasca 15 celle su 2 righe" §91b).
      Le cacce guidate dalla distanza trovano le porte piu' vicine, non le piu' ricche:
      per falsificare servono passeggiate casuali profonde + steering sulle
      configurazioni. E' la (h) sul piano delle estensioni. Corollario di metodo
      (G4-v1 vacuo, pannello §92): UN GATE DEVE POTER FALLIRE — asserire soglie
      minime di copertura del test, non solo il verde.
  (cc) **istanza striscia-stretta di (c)+(z)** (U2-POCKET §92): dell'astrazione OUT si
      trasferisce solo la morte; le config-FUGA vanno attaccate con la realizzazione
      concreta (qui erano REALI). Meccanismo quantificato: i round-trip rientro-flip-
      uscita scramblano le parita' del bordo (16 celle ⇒ 1,2M stati = ~37% del box;
      WIDE 37 celle ⇒ >30M stati = OOM Python su 16 GB, vedi (g)): una fase-1 cosi'
      non pota quasi nulla.
  (dd) **il residuo-al-minimo non e' IN GENERALE un insieme di celle bloccate**
      (U2-FAR §93): se una caccia si ferma sempre sulle stesse celle residue, NON
      dedurre blocco per-cella — l'ostruzione puo' essere CONGIUNTA (nucleo
      {(-1,1),(0,1)} chiudibile perfino in coppia, debito che sguscia in riga 2;
      ma sui jackpot (0,1) E' bloccata per enumerazione: i due casi coesistono).
      Antidoto: sonda mirata per-cella/per-coppia col goal esplicito
      (u2_far_core_block.py) PRIMA di enunciare blocchi.
  (ee) **"albero finito ⇒ seme vicino" richiede il min-pending su TUTTI i nodi**
      (U2-FAR §93): la nascita puo' essere in QUALSIASI nodo dell'enumerazione (il
      passato FINISCE, non muore) e il conteggio pend0-D>0 NON basta (jackpot:
      52-56<0 ma min vero 46-50). Parente di (w): quantificare su ogni troncamento.
  (ff) **la macchina-palla con OUT astratto non decide il ledger** (U2-FAR §93):
      l'astrazione che a §92 non potava la sopravvivenza non pota nemmeno la
      pulizia dei pending — stessa radice di (cc), nuovo sintomo (1.376 stati
      puliti fantasma vs reale mai sotto 2). Non riprovare strisce piccole esatte
      + OUT libero: servono i req fuori striscia (motore C, (g)) o un invariante
      che sopravviva allo scramble. [NB §94: "reale mai sotto 2" poi FALSIFICATO —
      il reale raggiunge pend2=0, ma (evidenza attuale) solo con posa in palla;
      i 1.376 clean-far restano fantasmi non realizzati.]
  (gg) **l'invariante campionato non e' un fatto — la chiusura induttiva e' il
      gate** (PARITY-FLUX §94): un funzionale GF(2) costante su 762k stati
      campionati e su 42/42 parole (phi_colonna0) puo' essere FALSO negli angoli
      che la politica di camminata non raggiunge. Se la chiusura alla Houdini non
      lo promuove, trattarlo come artefatto; il killer-step della chiusura indica
      l'angolo da campionare. Parente di (i) e (bb).
  (hh) **il floor di una caccia e' survivorship anche a 10^9 nodi se la famiglia
      di politiche e' una sola** (PANNELLO §94): la campagna §93 (1,29G nodi)
      dava pend2 floor 2; una DFS greedy MIRATA diversa trova pend2=0 in 7 s /
      660k nodi. Per un negativo servono politiche indipendenti multiple, e ogni
      floor "misurato" va etichettato con la politica che lo ha prodotto.
      Istanza quantificata di (bb).
  (ii) **enunciare la dicotomia, non la finitezza — e mai un rosso che maschera
      il testimone** (TRATTO-PULITO §95): un sottoalbero potato puo' essere
      infinito fuori dal dominio della pota; l'enunciato sano e' "confinato
      OPPURE il primo sconfinamento e' un testimone", e il checker deve
      riportare il testimone PRIMA di ogni assert di esaurimento (un
      `assert esaurito` che scatta prima trasforma una falsificazione in un
      rosso generico non diagnosticabile). Parente di (bb)/(cc).
  (jj) **la vitalita' dell'albero intero non e' l'invariante — guardare il
      sottoalbero potato dal vincolo** (TRATTO-PULITO §95): "pend2=0 ⇒ albero
      dei prepend finito" era FALSO (2/8 nodi puliti vivi oltre depth 400), ma
      era la domanda sbagliata: i rami che ri-sporcano la palla non producono
      controesempi. L'oggetto giusto e' il sottoalbero potato al vincolo
      violabile (pend2=0), dove la pota da' struttura gratis (in palla solo
      all-R ⇒ morte ≤3 per Bianchi che Curvano). Parente di (aa).
  (kk) **scambiare i dati senza scambiare la semantica non e' la simmetria**
      (TRIPWIRE-CP §96): l'immagine speculare di un'orbita ha bit scambiati E
      regola scambiata; interpretare i bit scambiati con la regola standard
      da' il mondo a COLORI INVERTITI (req tutte flippate, misurato 256/256).
      Ogni test di simmetria deve coniugare l'INTERPRETE, non solo l'input;
      un insieme derivato da un oggetto chirale (oracolo all-R) non e'
      M-chiuso e non deve esserlo (coniugarlo con l'oracolo specchio).
      Antidoto permanente: alpha1/mirror_tripwire.py (gate M0-M4) su ogni
      nuovo certificato. Parente di (d) e dei bug di frame §86.6/§89c.
  (ll) **il washout e' l'esca obbligatoria delle macchine a zona esatta /
      OUT libero** (COLLO-MACHINE §97): se gli esiti raggiungibili non
      cambiano corrompendo lo stato iniziale, l'astrazione ha buttato il
      vincolo portante e l'esito non dice nulla (ne' in positivo ne' in
      negativo). Testare il washout PRIMA di leggere il verdetto, con TUTTI
      i flip singoli + coppie e corse ESAUSTIVE (un flip solo e' un
      testimone di insensibilita', non di totalita'). Radice comune (ff)/(cc).
  (mm) **i confronti differenziali tra esplorazioni CAPPATE non sono
      definiti — e l'init sound "per caso fattuale" va assertato**
      (COLLO-MACHINE §97): due BFS al cap hanno frontiere diverse; K1/K2/
      coniugazioni tra prefissi troncati danno verdetti spuri — propagare i
      flag esaurita, etichettare NON-DEFINITO sotto cap, il ramo TEOREMA
      esige l'esaustivita' di tutte le corse. E ogni ipotesi di modello vera
      solo per i parametri correnti (init loc=OUT con posa w101 a cheb 4)
      va ASSERTATA, non presunta: a R=4 sarebbe stata unsound silenziosa.
      Parente di (hh).
  (nn) **l'eta' e' relativa all'orologio** (OCCURRENCE-SUPPLY §98): "detrito antico /
      quasi statico / pre-semina" cambiano segno cambiando unita' (passi vs
      epoche-evento). §89b leggeva staticita' (eta' med 2002 passi, 60%>=10P) dove la
      scala dei record vede rifornimento a mediana 3 epoche, max 31; nessuna colpevole
      profonda precede l'apertura della propria riga. Prima di dichiarare una risorsa
      "antica" (e attaccarla alla Blocco Antico), misurarla nell'orologio degli EVENTI
      che la consumano. Parente di (h) e della lezione §72 (frame co-moving).
  (oo) **le frazioni per-cella non decidono enunciati per-evento** (OCCURRENCE-SUPPLY
      §98, beccata dal pannello prima del verbale): un meccanismo che deve valere
      "almeno una volta per evento" va misurato sui MINIMI per-evento, non sulla massa
      per-cella — la massa e' dominata dagli eventi grossi (G~87) e nascondeva un
      minimo quasi-universale (91,5% dei record con colpevole di scia, min_ep<=5
      su 1174/1174). Parente di (hh) e (h).
  (pp) **il caso degenere escluso in silenzio dal denominatore e' il segnale**
      (MINEP-HUNT §99): un "if vuoto: continue" senza contatore ha nascosto 230
      record G=0, fra cui le 2 violazioni REALI dell'orizzonte V(onset+P) (residuo
      tutto bianco, onset a 2.372/14.757 passi >> onset_germe+P) = prima
      realizzazione del caveat V† di §98c. Ogni ramo degenere va CONTATO e
      riportato con semantica dichiarata; se un tripwire storico non e' replicato,
      la sua assenza va dichiarata a verbale. Parente di (bb) e (ii).
  (qq) **le soglie dell'orologio-record sono quantili con data di scadenza — e
      min_ep e' un osservabile della coppia (orbita, orizzonte)** (DOUBLE-TAIL
      §100): tre costanti-candidate morte in tre sessioni (min_ep<=5; coda doppia
      vuota; max 12 gia' in scadenza), massimi che salgono con n senza saturare,
      stesso record G=0 a V(onset+P) e ep=19 a V†, e il soffitto deduttivo
      ep<=y_rel realizzato CON UGUAGLIANZA (q=0) dai falsificatori: non c'e'
      spazio sotto. Nuove soglie SOLO dentro preregistrazioni complete
      (falsificatore + potenza + catena disgiunta + aspettativa di morte);
      enunciati ammessi: deduttivi, condizionali-dichiarati, esistenziali.
      Tassi confrontati per EPISODI, non per record (i consecutivi condividono
      le colpevoli). Parente di (i), (h), (bb), (nn).
  (rr) **le foglie di un albero potato non sono una misura** (SCUDO-ANTICO §107b):
      potando il sottoalbero alla prima decisione, il conteggio delle foglie pesa
      le classi per la POLITICA di potatura, non per la massa dei passati (una
      foglia a prof. 1 = ~meta' dell'albero al cap; il "binario unico" apparente
      era due binari paralleli). O si estende tutto al cap e si classifica al cap,
      o si pesa ogni foglia per le sue estensioni valide. Istanza enumerativa di
      (hh)/(oo). Corollario (istanza di pp): un criterio di gate calcolato su una
      distribuzione DEGENERE (moda >96%) spara spurio; controllare la
      degenerazione prima del verdetto.
  (ss) **l'irraggiungibilita' a cap e' un negativo con data di scadenza**
      (DANGER-REACH §107c): "cella irraggiungibile da ogni passato di
      profondita' <=D" non e' un fatto strutturale finche' il fenomeno non
      CHIUDE (tutti i d_hit finiti) o il cap non e' spinto alla chiusura —
      i 12/14 e 5/9 "bit antichi" di §107b a D=28 sono scesi a 0 a D=55/48.
      Fatti stabili: la TRIPLA (D_geo, d_hit, gap vs baseline matched) e la
      traduzione per-cella "deciso a >= d_hit+K passi". E' la (qq) sulle
      soglie di PROFONDITA', gemella di (h)/(bb) sui cap. Corollario
      (istanza di c): i d_hit dell'albero NON predicono la dinamica (il
      passato reale dei lock non tocca a 4k-18k passi cio' che l'albero
      tocca a 16-48): l'albero serve per i negativi e per i budget, mai
      per prevedere quando qualcosa succede davvero.
  (tt) **la quota sull'albero non e' una probabilita' dinamica** (SHIELD-MAP
      §107d): un funzionale contato sui passati ENUMERATI (sigma_D, quote di
      rami/foglie) non ha significato dinamico finche' non e' CALIBRATO
      contro la griglia reale — sigma_D (bimodale 0→1 sull'albero) ha
      associazione DEBOLE con la ricchezza-scudo reale (Spearman 0,0755;
      bande piatte ~0,32). In piu': sigma≈0 = ASSENZA di certificato nero
      (massa open/indecisa: 32/59 open=cap, 13 cap=1, 0/59 white_all), NON
      certificato bianco — nominare le classi per cio' che l'astrazione
      certifica davvero ("sigma-low", mai "lock-capable"). Gli enunciati
      d'albero restano deduzioni valide ("ogni passato valido..."); MAI
      leggerli come tipicita'/probabilita' di eventi reali senza gate di
      calibrazione. Sorella di (c), gemella di (ss).
  (uu) **il profilo marginale non localizza gli estremi congiunti**
      (SHIELD-MAP §107d, Simpson): un evento puo' stare al picco della
      marginale e in una valle della congiunta — "lock nel nucleo denso"
      (marginale-wx 0,42) era in realta' densita' 2D 0,19/0,12 sulle righe
      giovani cy=1,2. Dichiarare estremita'/tipicita' SOLO alle coordinate
      complete dell'evento; ogni collasso di coordinate va giustificato
      PRIMA del verdetto. Parente di (oo) e (h).

## 2. Convenzioni della dinamica (INVARIATE da HANDOVER §2)
- Bianco → svolta R (orario), nero → L; la cella si inverte dopo la lettura; poi mossa di 1.
- Heading: 0=su, 1=destra, 2=giù, 3=sinistra. Lettura→svolta→flip→mossa.
- W0 = parola della highway, periodo 104 (58 R, P(R)=0.558, rot=12), drift diagonale (±2,±2).
  File: `data/W0.npy` (0/1), `data/w0.txt` (L/R). Onset griglia vuota: N0=9977.
- morso = lettura **fresca-bianca** (`fresh & color==0`); definizione canonica in `morso_census.py`.
- Parola realizzabile = compatibile con QUALCHE configurazione finita: fresche libere,
  rivisite forzate dall'alternanza. R(n) censiti fino a 40 (`data/gamma_enum.pkl`).

## 3. Mappa del progetto
- `CHAT_HANDOVER.md` — stato completo del programma e roadmap.
- `docs/` — catena degli addenda: HANDOVER, HANDOVER2, ANATOMY, ALPHA (§1–28),
  GAMMA (§29–35), MORSO (§36–44), RADIUS (§45–55), PRODOTTO (§56), ALPHA1_FABRY (§57),
  DELTA4-BETA (§58), DEBT-LOCK (§59), DEBT-LOCK 2D (§60), LOCK-CHECKLIST (§61),
  CHECKLIST-MIXING (§62), CHECKLIST-VECTOR (§63), CHECKLIST-VECTOR-MODEL (§64),
  CHECKLIST-NONLOCAL (§65), DOOR-DEFECT-PROFILE (§66), POTENTIAL-SEGMENT-SCANNER (§67),
  ENDPOINT-MONOTONE-NOGO (§68), COMPATIBILITY-POTENTIAL (§69),
  **COMPAT-EVENT/CO-RAGGIUNGIBILITA' (§70-§74), GA-GATE-ZERO (§75), ENTRY-SEED-FRONTIER (§76), ROTOR-STALL (§77), GATE-ONE-COMOVING (§78), CONSUMPTION-LEDGER (§79), DEEP-MOTIF-SATURATION (§80), CONE-LOCK (§87), WEAPON-VITALITY (§88), U2-POCKET (§92), U2-FAR (§93), U2-FAR-PANEL (§94), U2-CLEAN-STRETCH (§95), U2-SIGNATURE (§96), U2-COLLO-MACHINE (§97), OCCURRENCE-SUPPLY (§98), MINEP-HUNT (§99), DOUBLE-TAIL (§100), RECORD-DIVERGENCE (§101), FASCIA-DOOR (§102), FRESH-PHASE (§103), DOOR-APPROACH (§104), LOCK-HOLE (§105b), SPEED-LIMIT (§106), DANGER-CLASS (§107a), SCUDO-ANTICO (§107b), DANGER-REACH (§107c), SHIELD-MAP (§107d), KERNEL-EXTENDED (§107e), CONSOLIDATION (§108/§108b: testa + volumi A/B, v2 con decisioni del pannello)**.
  La numerazione § è globale e continua.
- `alpha1/` — **sonde α1/β via distribuzione dei valori (§57), non-localita' r=4 (§58),
  hazard debito->lock (§59), modello 2D deep/bite (§60), lock->checklist T3' (§61),
  hazard/mixing checklist (§62), vettore/geometria checklist (§63), modello/compressione
  vettoriale checklist (§64), ridirezione non-locale/globale con correzione Pauli (§65),
  profilo 22-porte lock-condizionato (§66), scanner dei potenziali segmentali (§67),
  audit/no-go endpoint-monotono (§68), `Φ_compat` endpoint (§69), `Φ_compat` event-wise
  + schema T3'/co-raggiungibilita' (§70), scanner di coppie co-raggiungibili T3' (§71),
  profilo `L∞` discriminante-vs-profondita' (§72), pass-rate classi co-moving T3' (§73),
  e gate rango GF(2) sulle dogane (§74).**
  `alpha1_engine.c` (+ .exe): simulatore C self-contained, modi `search`/`reseed`/`dump`,
  **early-stop all'onset + reset-solo-celle-toccate** (31.7k semi/s su 14 shard), semi
  riproducibili dal solo stato RNG a 64 bit. Validato: vuota→9977, (7,−7)→106258, highway 22/104.
  `alpha1_within.py` (test within-orbit: max-stall, pavimento a finestra), `status.ps1` (monitor),
  `ALPHA1_RUN.md` (run), `onsets_shard*.txt` (88.521 hit≥100k), `dumps_all.txt` (24 orbite lunghe).
  `delta4_long_orbits.py` rigenera le 24 orbite da `rngstate` e misura `r=4` deep-black,
  minimi mobili e lock W0-like; risultato §58: il debito profondo tiene mentre il morso fresco
  affonda.
  `debt_lock_hazard.py` usa predictor causale `[t-L,t)` e lock futuro `[t,t+H)`; risultato §59:
  il ponte diretto deep-black -> lock e' anti-correlato, mentre fresh-bite predice positivamente.
  `debt_lock_2d.py` mostra che l'effetto fresh-bite resta positivo a deep quasi fissato, mentre
  deep resta negativo/debole a bite quasi fissato.
  `lock_checklist_probe.py` ricostruisce E(k) da `W0` e valuta T3' sui gate-lock: risultato §61,
  891/891 morti esatte alla prima lettura esogena cattiva e 24/24 onset veri OK.
  `checklist_mixing.py` deduplica i gate-attempt e misura hazard/mixing: risultato §62,
  810 tentativi porta unici, hazard OK 0.0296, riuso cella critica 1/762 consecutivo e
  1/12.945 intra-orbita.
  `checklist_vector_geometry.py` salva origine/heading porta e vettore esogeno: risultato §63,
  57.177 letture esogene, 5.806 mismatch, prima cattiva=morte in 786/786 fallimenti,
  origine porta consecutiva riusata 0/786.
  `checklist_vector_model.py` analizza i CSV di §63 senza nuova simulazione: risultato §64,
  full-vector diagonale (786/786 KO, 24/24 OK), due periodi coprono 774/786 KO, fascia 45-77
  domina le prime morti, 98-99 resta necessario, compressione greedy 37 offset / 66 componenti
  phase-conditioned sul campione lungo.
  `docs/CHECKLIST_NONLOCAL_STRATEGY_ADDENDUM.md` registra §65: T3' e' verdetto esatto ma
  il troncamento corto fallisce; 12 KO oltre due periodi arrivano a offset 1591 e L∞ 36.
  Correzione Pauli: §65 e' diagnosi strategica/campionaria, non teorema dinamico.
  `door_defect_profile.py` registra §66: su 810 tentativi la fase reale e' best unica 810/810,
  fasi compatibili alternative muoiono entro 5 letture. Upgrade strategico: identificare la
  porta e' locale, decidere se la porta vera entra e' globale.
  `potential_segment_scanner.py` registra §67: Pauli ha selezionato `Φ_depth` e `Φ_mass(λ)`;
  la run completa fa 24/24 orbite, 21.327 ancore, 21.183 segmenti. Gate `L=1600`: violazioni
  **400/762** per `Φ_depth`, **373/762** per `Φ_mass_104`, **380/762** per `Φ_mass_208`.
  Grid `L=1600`: `best22_depth` **3591/6275**, `best22_mass_104` **3150/6275**,
  `best22_mass_208` **3145/6275**. Conclusione: non riprovare potenziali endpoint-monotoni
  finiti cambiando solo pesi.
  `endpoint_monotone_audit.py` registra §68: no-go empirico/testimoniale, non teorema dinamico.
  Gate `L=1600`: `Φ_depth` **400/762** non-decrementi e **350/762** peggioramenti stretti;
  `Φ_mass_104` **373/762** e **371/762**; `Φ_mass_208` **380/762** e **378/762**.
  Grid `L=1600`: `best22_mass_104` **3150/6275** non-decrementi e **3149/6275** peggioramenti
  stretti. Addendum strategico §68: massa/area/mismatch non sono coordinate orientate; i flip
  locali depositano e ripuliscono, quindi i conteggi oscillano. §69 = `Φ_compat^L` + schema
  T3'/co-raggiungibilita', non nuovo `λ`.
  `compat_endpoint_audit.py` registra §69: endpoint `Φ_compat^L` coincide con `best22_depth` e
  quindi non e' nuovo. Gate `L=1600`: `h_best` non migliora in **400/762** e peggiora strettamente
  in **350/762**; grid: **3591/6275** e **2736/6275**.
  `compat_event_audit.py` registra §70: su **600** eventi deep-black (24 orbite, 25/orbita,
  `L=1600`, `--min-event-t 1040`), `h_best` non migliora in **357/600** e peggiora in
  **259/600**; la monotonia immediata ingenua di `Φ_compat` e' falsificata.
  `t3_coreachability_pair_scanner.py` registra §71: witness dinamico co-raggiungibile a
  `R=8` (orbita 5, fase 98, offset 494, rel `(15,13)`, `L∞=15`). Lettura conservativa:
  e' non-vacuita' dinamica dello schema, non sostegno diretto a un potenziale uniforme.
  A `R=16`, zero collisioni sulla griglia stride 520 e' soprattutto sparsita' combinatoria.
  `door_discriminant_linf_profile.py` registra §72: sui **786** fallimenti T3' reali
  (`horizon=1600`), `depth == first_bad_offset` in 786/786. Nel frame grezzo il discriminante
  cresce fino a `L∞=36`, ma nel frame co-moving W0, sottraendo
  `floor(offset/104) * drift_phase`, collassa a `L∞<=9` (131 classi osservate).
  Conclusione operativa a §72: non costruire `door_debt_graph.py` su classi grezze
  `(phase, rel_x, rel_y, required_color)`; se mai, solo nel frame intrinseco W0. §74 ha poi
  potato il debt graph come prossimo passo automatico. Link 1 resta separato e non risolto.
  `door_comoving_class_passrate.py` registra §73: sulle 131 classi co-moving di prima morte,
  rigioca **810** tentativi e **101387** letture target; **91657** pass, **9730** fail,
  pass-rate **0.9040**. **130/131** classi hanno almeno un pass e sono miste pass/fail;
  l'unica zero-pass ha supporto 4. La top class `(0,-5,-2,0)` fa **4224 pass / 486 fail**.
  Link 3 non e' falsificato; il motore deve essere GF(2) globale, non riuso assoluto cella.
  `door_gf2_rank_gate.py` registra §74: sulle matrici GF(2) delle letture target, fase 0
  pre-onset `offset<=1600` ha **304** tentativi, **187** colonne, rango **138** (nullita'
  **49**) con `C0=0` **0.9963** e senza colonne costanti/duplicate. Fase 0 depth `80+`,
  prefisso `offset<=103`, ha rango **4/19**. Lettura corretta: il deficit shallow e' reale ma
  troppo debole per forzare ingresso; i deficit profondi sono sample-limited o quasi-W0/circolari.
  §74 pota la via GF(2) shallow; prossimo passo = Link 1 non-simulativo o consolidamento.
- `GA_stress_agent/` — stress-test §75 del piano GA/no-entry. `ga_gate_zero_audit.py` mostra
  che il prototipo `A0(r,K,D0)` NON determina T3': due anchor replayabili della stessa orbita
  collassano nello stesso stato astratto per `r<=8`, `K=80`, `D0=80`, fase 98, ma hanno
  prefisso T3' diverso (`h_512=513` vs `494`; `h_1600=1014` vs `494`). A `r=9` il patch si
  distingue. Lo stress-test sintattico separa anche due campi con stesso `A0(8,80,80)` e
  discriminante T3' a offset 138, rel `(3,9)`. Lettura: non classificare SCC no-entry finche'
  T3' non e' funzione dello stato, oppure gli stati `unknown` restano tali.
- `code/window_automaton.py` — automa a finestra raggio r (lo strumento principale ora).
- `code/product_automaton.py` (+ `product_build.c`/.exe) — automa-prodotto A(r;m,D): finestra ×
  memoria di celle uscite (alternanza dentro gli stati). Builder C, 3 politiche; `--selftest`
  OBBLIGATORIO. Per istanze non minuscole usare SOLO il builder C (`--use-c`); MAI il BFS Python
  oltre poche migliaia di stati (esplode + swap). Diagnosi e ostacoli aperti: PRODOTTO §56.4–56.6.
- `code/ghost_block_analysis.py`, `code/check_witnesses.py` — copertura catalogo (m,D,politica) e
  check alternanza/realizzabilità/gamma dei testimoni del prodotto.
- `code/gamma_enum.c` — enumeratore/checker code periodiche eterne (`gcc -O3 -o gamma_enum gamma_enum.c`).
  Modi: `sweep pmin pmax`, `part p K idx`, `check file.txt`.
- `code/morso_census.py`, `code/morso_automaton.py` — censimento morsi e prototipo automa.
- `code/libant.c`, `code/antlib.py` — simulatore C della vecchia pipeline (compilare:
  `gcc -O3 -shared -fPIC -o libant.so libant.c`).
- `data/` — parole di test, pkl certificati; `results/` — summary e cicli raggio 1–3 già
  calcolati (valori di riferimento per i cross-check).
- `entry_seed/` — **mappatura della bocca (§76): mappa inversa + germi minimi + frontiere Q1/Q2.**
  `reverse.py` (mappa diretta/inversa sparsa, self-test round-trip 12000 passi -> griglia vuota),
  `clib.py` (loader autosufficiente di `code/libant.c`), `germ.py` (germe minimo per fase via
  troncamento raggio + greedy; out `germs_22.json`, min globale 13 celle fasi 0/103, onset 0),
  `brute.c` (ricerca forward semi minimi, reset-touched, fix bordo-scarta §76.6-j),
  `make_summary.py` (+ `seed_frontier.json`: Q1 b=1->onset 310 ... b=5->62, b=13->0; Q2 b=2->dist 0),
  `figura.py` (+ `frontiera_semi.png`).
  **§77 (rotor-stall):** `stall_geometry.py` (+ `stall_geometry.json`, `stall_footprint.png`) —
  geometria degli stalli del morso su `(7,-7)`: area-filling, molteplicita' ~1.57, bbox~len^0.767;
  la formica e' un rotor-router walk (cella = rotore a 2 stati), ma NON abeliano (uscita dipende
  dall'heading). `abelian_test.py` (escape 303/1109/1/1135 per heading) + `escape_scaling.py`
  (prova di viabilita': esponente di fuga deriva oltre 1.5, bite-stall limitato ~303 = quantita'
  diversa da #30 ⇒ strada non-abeliana NON priorita'). Livello morso, non α1. Dettaglio:
  `docs/ROTOR_STALL_ADDENDUM.md`.

## 4. Parallelizzazione (Ryzen 7 5800X, 8C/16T) — default se claude.md esterno non dice altro
- CPU-bound puro (C, sweep gamma_enum / alpha1 search): 14 processi shard con `start /low` o
  priorità BelowNormal (lasciare 2 thread liberi); shard disgiunti (per prefissi di scelte libere,
  o per offset RNG con semi riproducibili). I conteggi dei shard DEVONO sommare ai totali noti.
- **Collo di bottiglia = memoria, non thread** (lezione ALPHA1 §57.1): se ogni iterazione tocca/
  azzera una struttura grossa, 14 processi saturano la banda. Resettare solo lo stato sporcato
  (es. celle toccate) prima di scalare i thread. Misurato: 1.8k→31.7k semi/s solo con questo fix.
- Python memory-bound (BFS automa, dict grossi): 6–8 processi max (la RAM e la cache L3
  contano più dei thread); preferire un singolo processo ottimizzato + numpy vettoriale
  quando possibile. Niente hyperthreading per BFS con dict > 1 GB.
- Run > 10 min: SEMPRE log append-only con timestamp + (per i BFS) checkpoint su disco, così la
  run è riprendibile e monitorabile. Per le search a semi riproducibili basta loggare il rngstate.
- Ogni port C/numba di codice Python validato va rivalidato con i self-test PRIMA dell'uso.

## 5. Self-test (PRIMA di tutto, fermarsi al primo rosso)
1. `python code\window_automaton.py --selftest` (r=1: 15 stati, h=0.8114, 1 rotore; r=2: 403, 3 rotori).
2. `python code\product_automaton.py --selftest` (4/4 verde: m=0≡base; orbita reale costo invariante;
   frame canonico≡assoluto; 252/252 fantasmi bloccati; non richiede `build/r*_delta_cycle.txt`).
3. `alpha1\alpha1_engine.exe`: vuota→onset 9977; (7,−7)→106258; highway densità morso 22/104.
4. Cross-check r=3/r=4 coi `results/radius*_summary.json` prima di ogni nuova analisi a finestra.
5. (se si tocca la bocca/§76) `python entry_seed/reverse.py`: forward Python == motore C 12000 passi,
   round-trip esatto -> griglia vuota + (0,0,0). Verifica reversibilita' e convenzioni della dinamica.

## 6. Obiettivo strategico (perché questo task)
Teorema della Finestra (MORSO §40–40.1): ogni orbita eterna legge infinitamente spesso celle
nere fuori dalla finestra di memoria (2r+1)×(2r+1), con tasso ≥ δ_r (δ₁=3/5, δ₂=1/7), salvo
cavalcate finite (≤4 periodi) di rotori espliciti tutti uccisi da B–T/γ. La domanda a cui
r=4,5 rispondono: la stretta sui rotori resta monotona e B–T/γ-uccidibile a ogni raggio?
**AGGIORNAMENTO ALPHA1 §57:** la formulazione di α1 come *pavimento del tasso di morso fresco*
("modo DC del morso", #24) è stata **misurata ed erode** (densità→0, stalli ~lineari in T fino a
3·10⁵, anche nel caos puro). NON è l'invariante giusto. L'handle sano è il tasso di **non-località
δ_r** (lettura nera fuori-finestra), che NON è legato alla densità globale di morso ed è già un
teorema per r≤4. **AGGIORNAMENTO §58:** sulle 24 orbite lunghe il tasso nero fuori-finestra r=4
ha mediana 0.2334/passo e tail/core mediano 1.06; i minimi mobili sono ancora 9x/16x/27.4x
`delta4_auto` per L=313/1040/10400, mentre il morso fresco ha finestre a zero. **AGGIORNAMENTO
§59:** il ponte diretto debito profondo -> lock e' falso nel predittore locale: hazard `D>=40`
cala coi quantili deep-black e cresce coi quantili fresh-bite. **AGGIORNAMENTO §60:** la griglia
2D conferma che bite e' l'innesco: effetto `D>=40` mediano +0.1373 entro strisce deep, mentre
deep resta -0.0350 entro strisce bite. **AGGIORNAMENTO §61:** il ponte locale lock -> checklist
e' confermato: 891/891 gate-lock pre-onset muoiono esattamente alla prima lettura esogena cattiva
e 24/24 onset veri passano il controllo positivo. **AGGIORNAMENTO §62:** la checklist viene
quasi ricampionata localmente: 810 tentativi porta unici, 24 OK, 786 KO, riuso della cella
critica 1/762 consecutivo e tipo di errore quasi senza memoria. Prossimo fronte: vettore
checklist completo + geometria della porta. **AGGIORNAMENTO §63:** il vettore e la geometria
sono salvati: 57.177 letture esogene, mismatch mediano 6 nei fallimenti, stessa origine porta
consecutiva 0/786, L1 origine mediana 43. **AGGIORNAMENTO §64:** il modello vettoriale mantiene
la diagonale col full-vector, comprime a 37 offset / 66 componenti sul campione lungo, ma due
periodi mancano 12 KO. **AGGIORNAMENTO §65:** la lacuna non si chiude comprimendo ancora:
il troncamento corto fallisce e le celle decisive possono essere lontane. Correzione Pauli:
questo non e' ancora un teorema di non-localita' dinamica. **AGGIORNAMENTO §66:** il
`door-defect profile` sui lock e' fatto: fase reale best unica 810/810, off-phase compatibili
muoiono entro 5 letture, coda 268...1591 ritrovata. Quindi il profilo lock-condizionato non e'
l'invariante globale; §66 nomina l'asimmetria corretta: identificare la porta e' locale, decidere
il successo della porta vera e' globale. **AGGIORNAMENTO §67:** lo scanner segmentale ha falsificato
i candidati naturali `Φ_depth`/`Φ_mass`: su segmenti deep/no-entry, `Φ(next) >= Φ(prev)` avviene
in circa meta' dei casi sia su gate sia su grid. Quindi deep-black non e' decremento endpoint-monotono
di un potenziale finito basato su prima morte o massa pesata dei mismatch. **AGGIORNAMENTO §68:**
Pauli restringe il linguaggio: no-go empirico/testimoniale sui proxy scalari finiti testati, non
teorema dinamico. L'audit da CSV conferma peggioramenti stretti, non solo pareggi: gate `L=1600`
`Φ_mass_104` peggiora strettamente in **371/762** segmenti; grid `best22_mass_104` in **3149/6275**.
Addendum §68: non scrivere che la reversibilita' conserva massa; scrivere che massa/area/mismatch
sono conteggi non orientati, perche' i flip locali depositano e ripuliscono. Prossimo fronte (§69):
`Φ_compat^L`, dove `h_g^L` e' il primo offset cattivo della porta `g`, `h_best^L=max_g h_g^L`,
e `Φ_compat^L=0` se `h_best^L=L+1`, altrimenti `exp(-h_best^L/104)`. Se `Φ_compat` diventa somma di mismatch, ricade in
`best22_mass`; se resta solo endpoint `h_best`, e' gia' ferita da `Φ_best22_depth`. Questo ha
impostato §69: separare endpoint da forma event-wise/amortizzata e co-raggiungibilita' con due storie finite della formica,
localmente indistinguibili alla porta, discordi nella cella lontana. Caveat scala: `R(n)` arriva
a 40, celle decisive osservate a offset 1591. **AGGIORNAMENTO §69:** la versione endpoint e'
chiusa: `compat_endpoint_audit.py` mostra che `h_best` non migliora in **400/762** gate e
**3591/6275** grid, con peggioramenti stretti **350/762** e **2736/6275**.
**AGGIORNAMENTO §70:** il pre/post evento deep-black falsifica anche la monotonia immediata
ingenua: su **600** eventi, `h_best` non migliora in **357/600** e peggiora in **259/600**.
**AGGIORNAMENTO §71:** `alpha1/t3_coreachability_pair_scanner.py` trova un witness dinamico
co-raggiungibile a `R=8` (stesso patch locale, fase 98, discriminante rel `(15,13)` a offset
494). Questo chiude solo la lettura "esistenza/non-vacuita'"; non muove α1 e non supporta da
solo un potenziale. `R=16` zero-collisioni e' baseline di sparsita', non confine strutturale.
**AGGIORNAMENTO §72:** `alpha1/door_discriminant_linf_profile.py` misura i 786 fallimenti T3'
reali: nessuna duplicazione fisica, `depth=first_bad_offset` sempre. La crescita grezza
`L∞=36` era drift del tubo W0: nel frame co-moving fase-dipendente il supporto collassa a
`L∞<=9`, con 131 classi osservate.
**AGGIORNAMENTO §73:** `alpha1/door_comoving_class_passrate.py` misura i pass-rate delle stesse
classi: 810 tentativi, 101387 letture target, pass-rate 0.9040; 130/131 classi hanno almeno un
pass e sono miste pass/fail. La top class `(0,-5,-2,0)` fa 4224 pass / 486 fail.
**AGGIORNAMENTO §74:** `alpha1/door_gf2_rank_gate.py` misura il rango GF(2): fase 0 all
pre-onset `offset<=1600` ha rango 138/187 (nullita' 49), C0=0 0.9963, senza colonne banali;
fase 0 depth `80+`, prefisso `<=103`, ha rango 4/19. Interpretazione aggiornata: dipendenze
shallow reali ma troppo deboli per UNSAT, deficit profondi sample-limited o circolari. Questo
impostava il fronte §75: Link 1 non-simulativo/consolidamento, non `door_debt_graph.py`
automatico.
**AGGIORNAMENTO §75:** stress-test GA/no-entry gate-zero: `A0(r,K,D0)` e' sound come
sovra-approssimazione, ma cieco rispetto a T3'. Con `r<=8`, `K=80`, `D0=80`, fase 98, due
storie replayabili della stessa orbita collassano nello stesso stato astratto e hanno prefisso
T3' diverso (`h_512=513` vs `494`). Stop corretto: niente classificazione SCC su `A0`; prossimo
fronte (§76) = definire `A1` con T3' deterministico/proof object, oppure propagare `unknown`.
**AGGIORNAMENTO §78:** kernel co-moving della porta `A1`: il verdetto no-entry e' funzione di uno
stato finito co-moving (footprint 44 celle, raggio strutturale rho<=9) + budget temporale `P=15`;
unknown-free a `P>=15` su 2014 attempt, oltre = `unknown` (vuoto sul campione, NON
dimostrabile-vuoto = Link 1). `delta_r` (morsi) e `A1` (porta) sono due certificati beta
COMPLEMENTARI, non un singolo automa-finestra a raggio 9.
**AGGIORNAMENTO §79:** ledger di consumo (SCOUT; simulatore indipendente validato su onset 9977 +
W0 + alternanza 0/106000). Sul transiente (7,-7) la forma ingenua del lemma di consumo e' FALSA:
creazioni di nero (~0.556/passo) > distruzioni (~0.443/passo), pool che cresce, inflow di frontiera
(B-T) ~4:1 sul consumo deep, rigenerazione dominantemente locale (eta' mediana 8). Stessa morte del
pavimento-del-morso (§57). L'ostruzione vive nella coda lunga (age>1040, max 4068) = §77 rotore
non-abeliano. Deficit-di-consumo chiuso (trappola n); oggetto vero = grafo causale di rigenerazione
ristretto alla coda lunga. Dettaglio: docs/CONSUMPTION_LEDGER_ADDENDUM.md.
**AGGIORNAMENTO §80:** positive gate (§79.6) eseguito sul Ryzen (24 orbite reali, 16 core, 22s): MORTO.
**AGGIORNAMENTO §87:** calcolo dei lock esteso alle corse reali (`docs/CONE_LOCK_ADDENDUM.md`).
Lemma Replay-Lock (V_T coi colori iniziali = lock esatto <=> di ogni corsa finita, self-test 1000
junk + 200 flip); Lemma del Cono (gate onset 5/5: vuota 9977 blob 1376 r29, b1 310 blob 104 r9;
affitto periodico ESATTO 22 celle/periodo da p0=0, lock eterno finitamente descritto; le 3 celle
di scia stanno in ogni blob); Lemma Finestra-K (colori del footprint degli ultimi K passi =
funzione della parola, verificato su reale); CENSIMENTO germi finestra-K: ZERO buchi a K=6..14
(50/154/448/1300/3680 germi, tutti onset) => TEOREMA DELLO SPOILER VECCHIO (eterna => nero
d'eta'>=K entro raggio med 15 max 68, ogni istante, ogni K<=14); streak L/R cappate a 4.
FORENSE onset 24/24 == header Ryzen: germe reale = 13-17 neri (mediana 13 = minimo §76) r<=7,
interfaccia 1-2 periodi, fresh 100% da p2, f_bordo med 0.68, outward 23/24. KILL-GATE §79.1
SCARICATO: raggio decisivo (prime-letture, word-minimale) cresce 18/38/93.5/118 con Delta=2/10/100/
1000 periodi senza stabilizzare => niente programma a footprint limitato per deep->W0. Via dei
RECORD (B-T): a un record y-min davanti+riga-0 bianchi gratis, footprint in {y>=1}; burden1 min
record-compatibile 18/16/14/10 a K=12/14/16/18; caccia beam 300 (K<=40): plateau a 5 celle da
K=32 — POI FALSIFICATO come artefatto di beam dal run Ryzen certificato (beam 5000, kmax 60,
parallelo): discesa 5 -> 4 (K=35) -> 3 (K=40) -> **2 (K=58/60)**, ancora in discesa al cap;
residui {(-2,1),(0,2)} e {(-2,1),(1,1)}, con (-2,1) costante da K=26 (l'ultima sentinella).
POI (beam 8000, kmax 160): il 2 muore a K=71, il beam collassa in una STAFFETTA periodica a
fardello 4; DFS sui prepend: TUTTI i campioni a fardello 2 e perfino P(0) del ciclo si
estinguono all'indietro (prof. 3-7) => enunciati VACUI per orbite eterne (trappola w). Lezione:
coprire spoiler costringe il passato; criterio arma corretto = burden1=0 E D(w) illimitato;
cacciatore v3 con --viable-k e --per-class. Congettura §88: D illimitato => burden1 >= 1?
Link 1 riformulato esatto, NON caduto; trappola (v). Prossimo §88: caccia all'arma (kmax/beam
maggiori: burden1=0?); se trovata, forzatura ai record (l'arma da sola NON fa cadere Link 1);
parole reali ai record; record doppi/angoli. Certificazione Ryzen §86-§87e COMPLETATA (bit-identica).
L'alfabeto dei motivi locali co-moving agli eventi deep-black non satura (r=3 ~99,4% eventi unici;
scoperta nuovi-motivi ultimo20%/primo20%=1,14; pooled unione/somma=0,979; intersezione 19/1,5M). Il
lato-alpha (detrito) NON e' finito-stato — opposto al lato-beta/porta (§78, footprint 44 / P<=15). Tre
falsificazioni in fila (deep->W0 §59, deficit §79, alfabeto finito §80): il crux di Link1 e'
irriducibilmente dinamico (coerente §28.2). Trappola (o). Dettaglio: docs/DEEP_MOTIF_SATURATION_ADDENDUM.md.
**AGGIORNAMENTO §88 (Parola Viva / Residuo dell'Uno):** la caccia v3 CON vitalita' (beam 4000,
kmax 120, viable-k 8, per-class 200, Ryzen 19 min) scende a **burden1=1 a K=101..120, residuo
{(1,1)}**, weapon null; il collasso a staffetta-4 di §87e-bis era inquinamento da minimi vacui.
Il passato di w101: binario UNICO (esaustivo prof. 2..17, poi riapertura ×1.65, trappola y),
burden1=1 e residuo (1,1) COSTANTI fino a prof. 624; regime periodico interno periodo 8
(finestra [3,320) = 39.6 periodi) e ciclo di prepend **σ=LLRLLRLL certificato geometricamente**
(heading ritorno 0 ⇒ blocchi traslati, conflitti solo gap<=g_max=12, Δ_anchor=(-2,0) ⇒
record-compat eterna; M_cert=14) ⇒ **D(w101)=∞**, falsificazione 3/3 verde (diretta m=15..40,
catena K=565, traslazione footprint); clausola-onset CHIUSA via Replay-Lock+disgiunzione
(run(m)=run(40) ∀m≥40: onset 160, burden1=1, residuo (1,1) = TEOREMA senza parti empiriche). **TEOREMA DELLA PAROLA VIVA:** eterna non-highway ⇒ a
ogni record y-min con suffisso w101 la cella (1,1) e' nera — primo teorema-parola NON vacuo;
pigeonhole sul **RESIDUO DELL'UNO**. Corridoio burden<=1: albero esponenziale (486.676 rami
vivi a prof. 60 in 1.5M nodi, non esaustivo), arma MAI vista. Congettura pavimento-vivo:
D=∞ ⇒ burden1>=1 (il livello 1 e' ora OCCUPATO da una parola viva). Trappole (x),(y). Prossimo §89: parole vive ai record
reali delle 24 orbite; pigeonhole sull'Uno (riga y_rel=1 = riga-record precedente, scia §86);
arma = parola viva a burden1=0 (kmax>120, automa dei prepend per l'impossibilita').
Dettaglio: docs/WEAPON_VITALITY_ADDENDUM.md.
**AGGIORNAMENTO §89a (censimento parole reali ai record):** 1639 record y-min pre-onset
(24 orbite): burden1 reale min 12 / med ~317 a K=101, mai <=6, zero w101, zero burden-0;
TRIPWIRE del teorema 1620/1620 (>=1 colpevole nera a ogni record lontano dall'onset);
3 record a UNA sola colpevole. Anello di occorrenza riformulato sul conteggio delle
colpevoli. **§89b:** G = passeggiata quasi bilanciata (med 96), detrito quasi statico
(96% nere al record dopo, ~48% ancora colpevoli), eta' med ~18P (60%>=10P, 3722 di seme;
soglia >=K forzata per costruzione), cheb med 15/max 75 (=raggi §87). Autopsie G=1 3/3:
colpevole = PROPRIA SCIA a eta' K+1..K+13, cheb 3-6 (trappola v al bordo del pigeonhole).
**§89c:** forense 3/3 (colpevole = passo 0 dell'estensione K+j, svolta R, mai rivisitata;
frame: ruotare con k=(-h0)%4) + **TEOREMA DEL BLOCCO ANTICO**: (1,1) fuori dal footprint
di sigma^m·tau·w101 per OGNI m => eta' colpevole > 405+8m ai record della famiglia: la
scia recente non salva il pigeonhole lungo la famiglia certificata. **§89d:** Blocco Antico esaustivo sull'ALBERO INTERO dei passati di w101 (onset non
richiesto; conteggi == muro: il filtro-onset non pota mai): zero visite a (1,1) su 91.027
passati validi a prof. 40 => eta'((1,1)) > 141 a ogni record-w101 di qualsiasi orbita.
Dicotomia §90: evita-per-sempre (=> nero solo da seme, B-T esce dal seme => w101 VIETATA
ai record tardivi) vs visita (=> verdetto della parola estesa, ricorsione); decidere con
l'automa dei prepend. docs/RECORD_WORD_CENSUS_ADDENDUM.md.
**AGGIORNAMENTO §90 (dicotomia decisa / ARMA / Muro dietro l'Uno):** il corno (b) e'
reale (visita a prof. 57; sweep esaustivo a 46 = zero => eta'((1,1)) > 147). Coprente
che lascia (1,1) BIANCA = **PAROLA-ARMA (burden1=0, K=158)**, 30/30 nel campione, ma
morta all'indietro: K=158 ha D=0, le profonde muro esatto [1x12,0] (D=12 uniforme a
prof. 77/105/129); NERA => D<=4, burden 67..1976. Congettura raffinata: burden1=0 =>
D<=12. TEOREMA-BERSAGLIO §90d (Muro dietro l'Uno, enunciato corretto a §91): orbite
ETERNE, record y-min STRETTI fuori da un intorno finito del seme (coerente §89a: 0/1639).
Trappola (z): raggiungibilita' astratta non trasferisce (automa a scatola validato V1
ma non conclusivo; realizzazione concreta guidata > allargare scatole).
docs/WEAPON_DICHOTOMY_ADDENDUM.md.
**AGGIORNAMENTO §91 (U1 dimostrato, lacuna = U2-NERO):** U1 = TEOREMA DEL RIGIOCO
BIANCO (coprente-bianca => arma, burden1=0 onset 160), dimostrazione via Replay-Lock +
residuo certificato, RIPARATA dal pannello di scettici (buco d'orizzonte: la rilevazione
legge fino a T=2600 => usare V-DAGA, 576 celle; check G1b: V-DAGA INT {y>=1} SUB
F U {(1,1)}, zero extra — lezione: l'orizzonte giusto e' quello della RILEVAZIONE, non
dell'evento). Attacco: 1859 armi fresche, 0 controesempi. Ramo bianco chiuso per le
eterne senza bound di vitalita'; resta U2-NERO (coprente-nera => D<=4; tasca 15 celle
su 2 righe). Enunciato del Muro corretto: vietanza per ETERNE ai record y-min STRETTI
fuori da un intorno finito del seme ("storia lunga" NON basta; le convergenti possono
presentare = ingresso forzato). Prossimo §92: certificato U2-NERO alla-HALO
(esatta-in-striscia, uscita=sopravvivenza), poi famiglia inevitabile (scia minima §89b).
docs/WALL_BEHIND_ONE_ADDENDUM.md.
**AGGIORNAMENTO §92 (U2-NERO FALSIFICATA, D=∞ certificato, bilancio dei neri freschi):**
il certificato §91b e' stato costruito e validato (`alpha1/u2_pocket_certificate.py`,
6 gate: formula del passo, lemma del suffisso, replay bit-identico 60 muri §90c,
membership 60/60; G4 riparato dal pannello con camminate lunghe e SOGLIE asseribili:
264.854 stati, 4.427 rientri, 644 coperture; lemma di sovra-approssimazione promosso a
deduttivo) ma ha FALSIFICATO il bersaglio: "coprente-nera ⇒ D≤4" era survivorship
best-first (trappola bb; cade anche la "tasca 15 celle" §91b) — scala reale
D = 0/4/8/12/48/56 (43.726 nere, 43 config vs 2 del censimento), 34 coprenti-nere
fuggono nel vergine (riga 13–33) e una e' TEOREMA D=∞ (`u2_infinite_rail.py`, Lemma del
Raggio Monotono): cade la forma word-level, uniforme E per-parola. Il corno 3 del Muro
NON si chiude via vitalita' (riapre SOLO il corno 3: U1 intatto, ri-attaccato 12/12):
D e' l'invariante sbagliato (trappola aa) — il raggio paga 1 nero fresco = 1 cella di
seme ogni 2 passi, la σ di §88 5/8 (anche D(w101)=∞ non certifica presentabilita' ai
record lontani), ma la discesa in autostrada costa O(1) totale ⇒ l'invariante e' il
BILANCIO senza tasso; ledger corretto = pending per-cella (ogni L apre/riapre, R su
pending chiude). Restano certificati: T1 h1=2⇒D=0 (geometria), T2 zero cicli in-tasca,
T3 muro con celle tutte in S_CORE ⇒ D≤33, T4 corridoio h1=0 ⇒ req(2,1)=B. Fase-1 WIDE
>30M stati = OOM Python (trappola cc/g). Prossimo §93: U2-LONTANO (corsa inversa
forzata + contabilita' dei pending nella palla senza seme, usando la parte
w101-specifica — il Muro si richiude nella forma spaziale senza bound su D); lemma dei
bianchi che curvano (verificato: all-R muore entro il 5°); h1=1 mai realizzata
(0/43.726); "burden1=0 ⇒ D≤12": attacchi economici falliti (T1 blocca le sorelle-flip;
151 bianche max 12 ma classi nuove 4/8) — stress-2 bianche dedicata.
docs/U2_POCKET_ADDENDUM.md.
**AGGIORNAMENTO §94 (censimento famiglia, pannello, PAVIMENTO FALSIFICATO, parity-flux):**
censimento born-near sulla famiglia RIGENERATA (`u2_far_born_near_census.py`, gate
GC0-GC4): 273.493 coprenti-nere in 50 config `(h1, req|S_CORE)` — **273.459
CERTIFICATE (r_seed<=63), 34 fuggenti (31/34 in una config mista), 0 min-pend=0**;
nuove classi D 28/32/52/60/64. Pannello §93: **COMPLETATO 3/3** (nascita-vicina in
terza run: Lemma REGGE su tutti gli assi, 3/3 esche, enumeratore indipendente
solo-valid() bit-identico 12/12, controesempi pend2 fuori-ipotesi 10/10;
precisazioni: depth_cap>=D_true+1, ramo min-pend-0 = rinuncia con gamba-1 ancora
valida; corollario-bonus "eterne senza palla" RESPINTO in sintesi — a record
fissato il passato di un'eterna e' finito: l'eternita' vincola il futuro, non il
passato); numeri §93 tutti bit-identici; imprecisioni: 2.020 vicini veri
(non 3.396), controllo negativo caccia vacuo. **FALSIFICATO il PAVIMENTO DEL
LEDGER** (due lenti convergenti + verifica di terra): pend2=0 raggiungibile (posa
(-1,2) IN palla; 7s/660k nodi vs 1,29G ciechi = trappola hh), pend2=1={(0,2)} con
posa (0,3) FUORI; cadono residuo-nucleo §93e e "mai sotto 2" §93f; 10 controesempi
in `u2_far_pend2_counterexamples.json`. SOPRAVVIVE: **posa fuori palla => pend2>=1
mai violato** (~160M+1,29G nodi) = LEDGER SPORCO v2 (basta al Muro: l'ipotesi
esclude seme E origine); i puliti sono quasi-morti all'indietro (17-71 nodi) =>
via "chiusura per vitalita'". PARITY-FLUX: nullspace GF(2) su feature di stato +
chiusura Houdini (526 tipi-di-passo): phi_colonna0 (762k stati concordi, 42/42)
RIFIUTATO dalla chiusura e poi falsificato = trappola gg (il checker batte il
campione); per-pose PP0 rosso, da raffinare. Prossimo §95: chiusura per vitalita' (pend2=0
=> albero finito => Nascita Vicina => Muro senza pavimento); Ledger Sporco v2
deduttivo (per-pose raffinato / motore C striscia allargata / clean-far da
uccidere-realizzare); fuggenti nuove vs 34 nere-D>=400; retro-nota §91c.3.
docs/U2_FAR_PANEL_ADDENDUM.md.
**AGGIORNAMENTO §93 (U2-LONTANO: ledger, NASCITA VICINA, pavimento del ledger):**
il ledger dei pending e' meccanizzato e validato (`alpha1/u2_far_ledger.py`, gate
L0-L3 + pannello lente-ledger con macchinario indipendente e 3 mutazioni-esca
beccate; L2 riproduce bit-identico il controesempio §92e: 2918 passi, pending
60->286; scoperta: L su pending IRREALIZZABILE => ogni L e' apertura netta;
"pending finali = seme nero visitato" promosso a TEOREMA). **LEMMA DELLA NASCITA
VICINA** (`u2_far_born_near.py`, per-parola, due gambe origine/seme, min-pending su
TUTTI i nodi — trappola ee): 42/42 testimoni ad albero finito CERTIFICATI vietati
ai record lontani (r_seed<=16, senza bound su D), cross-validati con valid().
**PAVIMENTO DEL LEDGER pend2>=2**: TEOREMA per enumerazione sui 12 finiti
(`u2_far_pend2_floor.py`, min 2/3/3/4, jackpot residuo {(-1,1),(0,1)} = scia §86);
congettura misurata sulle 6 fuggenti (caccia DFS-milestone `u2_far_closure_hunt.py`:
nessuna chiusura, 37k nodi mirati R=2 + 1,29G campagna; corsa forzata fresco=>R
muore <=64 su tutte le 48 coprenti reali `u2_far_run.py`; ostruzione CONGIUNTA
whack-a-mole riga1<->riga2, trappola dd, sonda `u2_far_core_block.py`). Macchina
astratta palla-2 NON decide (`u2_far_ball2_machine.py`: 1.376 puliti fantasma,
trappola ff). Corno 3 del Muro SPEZZATO: (3a) alberi finiti chiusi via Nascita
Vicina; (3b) fuggenti = pavimento del ledger (aperto; se vero, Muro chiuso al
raggio 2+intorno). Pannello §93 PARZIALE: 2/5 lenti (3 uccise da limite sessione,
DEBITO §94). Prossimo §94: completare pannello; pavimento sulle fuggenti (motore C
striscia allargata / invariante parita'-flusso / automa prepend in-palla);
censimento born_near sulle 43 config; retro-nota §91c.3.
docs/U2_FAR_ADDENDUM.md.
**AGGIORNAMENTO §95 (TRATTO PULITO: riduzione di v2, dicotomia, oracolo):**
la via "chiusura per vitalita'" (§94c.2) e' FALSIFICATA in apertura (trappola
jj: nere400[0]/[2] hanno sottoalbero INTERO vivo oltre depth 400) e sostituita
da una riduzione: **LEMMA DEL PASSO DI PULIZIA** (deduttivo: pend2 decrementa
solo con R sulla cella pending chiusa, in palla-2, posa = quella cella) +
**TEOREMA DEL TRATTO PULITO** (ogni nodo pulito appartiene al sottoalbero-a-
pend2=0 del suo ultimo nodo di pulizia m*<=n, posa(m*) in palla; radicamento a
w101: pend2(w101)=6 => vale per OGNI passato che presenta w101) => Ledger
Sporco v2 <=> nessun tratto pulito esce dalla palla (i 1.376 clean-far
raggiungibili SOLO via tratto pulito). **DICOTOMIA** (deduttiva): in palla il
tratto pulito e' forzato all-R => muore <=3 (Bianchi che Curvano); o confinato
o il primo passo fuori E' il testimone (checker a foglia-testimone, trappola
ii). Certificati esaustivi: 31/31 stati di pulizia reali (8 §94 + 23 cacce
multi-politica G3, 17 nuovi) con sottoalbero pulito VUOTO e firma UNICA
((−1,2), heading sx) bloccata da req((0,2))=1 (whack-a-mole di colonna 0);
0 falsificatori. **ORACOLO PIGRO** (`u2_far_clean_oracle.py`): 25/40 firme
(posa,heading) confinate deduttivamente, **15 firme-exit astratte** mai
realizzate = fronte esatto: v2 teorema <=> le 15 irraggiungibili. Pannello
3/3 in sessione (bit-identico 10/10, esche 6/6; riparati non-sequitur
finitezza, assert-order, m*<=n; v2 dichiarata congettura empirica sui nodi
non raggiunti). Convenzione bit a verbale: bit 1 = R = lettura BIANCA, bit 0
= L = NERA. Prossimo §96: uccidere/realizzare le 15 firme-exit (vincoli di
raggiungibilita': pend-storia del genitore, scia §86, geometria del passo di
pulizia; o cacce per-firma); ereditati: fuggenti nuove vs nere-D>=400,
retro-nota §91c.3, stress-2 bianche, h1=1.
docs/U2_CLEAN_STRETCH_ADDENDUM.md.
**AGGIORNAMENTO §96 (FIRME-EXIT, COLLO DELLA PULIZIA, TRIPWIRE CP):**
oracolo v2 (`u2_far_clean_oracle_v2.py`) con vincoli deduttivi: C1 "muro
delle nove" (w101 visita 9/10 celle di palla, manca solo (1,1) => a ogni nodo
pulito req=1 sulle 9), C3 (c_par visitata), C4 (c_par con y>=1 => ((2,1),3)
senza genitore) => 7/15 firme-exit uccise, restano 8 (tutte exit-diretta);
Lemma dell'exit-step => **v2 <=> nessuna delle 8 firme (cella, heading) e'
realizzabile come nodo di pulizia** — fronte finito. Cacce per-firma
(`u2_far_signature_hunt.py`, 1242 job, 733M passi, PA/PB/PC/PD, controllo
positivo S0): 8 residue 0 hit; **603 pulizie censite TUTTE ((-1,2), h=3) e
TUTTE da PC** (PA/PB/PD zero: pulire da zero e' rarissimo; negativo
etichettato PC-only). **COLLO DELLA PULIZIA** (candidato-teorema §97): la
palla si pulisce da UNA porta sola; se teorema => v2 TEOREMA => Muro chiuso.
Lemma della Catena di Chiusura (run-R in palla <=3, pending che si
ACCUMULANO all'indietro, 4o passo = L su c*; pattern RRRRL 8/8 di terra).
Intuizione chirale (Michael): identita' R−L=ΔB deduttiva (W0: 58−46=12=rot,
winding=carica nera; heading≡ΔB mod 4; gia' implicita a §79; assioma Z/4
disponibile per PP0) + tripwire specchio (`mirror_tripwire.py`, M0-M4:
coniugazione CP esatta con interpreti a chiralita' parametrizzata) che ha
beccato in-run due confusioni P-vs-CP = trappola (kk). Pannello §96 3/3:
A/B/C/F reggono (indipendente 37/37, esche 4/4), E riscritto, B1-B4 chiuse.
Prossimo §97: TEOREMA DEL COLLO — enumerazione esaustiva degli approcci di
chiusura (catena <=3 R + aperture L) per uccidere le 8 firme; DAG delle
chiusure whack-a-mole. Ereditati: fuggenti nuove vs nere-D>=400, retro-nota
§91c.3, stress-2 bianche, h1=1.
docs/U2_SIGNATURE_ADDENDUM.md.
**AGGIORNAMENTO §97 (MACCHINA DEL COLLO: falsificazione della via a zona
piccola):** le due gambe §96g.1 fuse in una macchina finita esatta-in-zona /
OUT-libero (`u2_far_collo_machine.py`, stati int-packed, direzione di
soundness: intersezione vuota con le 8 firme = teorema). FALSIFICATA ai
raggi piccoli: radius 2 (esaustiva, 36.860 stati) 24 firme con
insensibilita' TOTALE ai flip dello stato iniziale (osservazione su tutti i
flip+coppie = washout, trappola ll); radius 3 (anello 11/11 tracciato, 60M
stati al cap, firme = lower bound) **tutte le 8 firme residue raggiungibili**
— INCONCLUDENTE cap-robusto: nessun teorema da zone raggio<=3 con ambiente
libero (rientro libero = direzioni d'approccio libere). Quale componente
scartata porti la rigidita' reale (req fuori zona / continuita'
uscita-rientro / mortalita' esterna) e' APERTO, esperimenti separatori
nominati. Pannello §97: semantica sound + verifica di terra forte (replay
proiettato del testimone reale, 1.270 passi, pend2 identico passo-passo);
riparati: GATE B1 (init loc=OUT era sound solo per cheb(posa_w101)=4>R — a
R=4 unsound silenziosa), K1/K2 NON-DEFINITI sotto cap (trappola mm),
washout retrocesso a osservazione. Z/4 non morde nell'OUT-libero (previsto).
Prossimo §98: esperimenti separatori (guscio req cheb R+1..R+k / rientro
vincolato al lato d'uscita); motore C striscia allargata con B1; vincoli-scia
sul rientro (§86 all'indietro); le cacce restano il falsificatore permanente.
Ereditati: fuggenti nuove vs nere-D>=400, retro-nota §91c.3, stress-2
bianche, h1=1.
docs/U2_COLLO_MACHINE_ADDENDUM.md.
**AGGIORNAMENTO §98 (ANELLO DI OCCORRENZA deciso in epoche-record):** il punto 4 della
scala §91c (famiglia di parole inevitabile ai record) e' stato deciso cambiando unita'.
LEMMA DELLA SCALA (deduttivo, T1-T4 zero violazioni su 188.234 colpevoli profonde,
gate §89a/§89b riprodotti): la riga -m apre al record m-1 ⇒ ai record profondi ogni
colpevole e' auto-dipinta dopo l'apertura della propria riga, entro y_rel<=k_max epoche
(identita' q = y_rel−ep); la pre-semina antica NON esiste come risorsa (il "detrito
antico" §89b = artefatto dell'orologio: eta' med 2002 passi ma 3 epoche, trappola nn).
Per-record (riparazione lente C, trappola oo): **min_ep<=5 su 1174/1174 record
profondi**; scia quasi-universale (91,5% con colpevole word-proximal, min_age med
107=K+6; 88,2% con colpevole di discesa, min_lag med 0) MA coda 8,5% senza colpevole
entro 2K (fino a 24.464 passi) ⇒ nessuna famiglia-parola a profondita' fissa e'
inevitabile; G=1 non-dimostrato-inevitabile (med 87); enumerazione §89c POTATA senza
esecuzione. TEOREMA DEL RIFORNIMENTO RECENTE (condizionale; ipotesi A germe-onset
semi-decidibile, B V† su residuo+k_max+classificazione, C k* esistenziale non
calcolato): eterna ⇒ evento pittura-e-preserva in ogni finestra di k* epoche, quota
<=k*. Punto 4 ⇒ (4'): il rifornimento perpetuo e' incompatibile con la non-entrata?
Pannello 3/3 (lente A 18/18 bit-identici con paint via traiettoria; lente B esche 4/4;
lente C 2 ROSSI riparati in sessione). Prossimo §99: min_ep<=5 struttura o campione
(orbite non selezionate per onset, sterilizzare trappola h); geometria dei RIENTRI
(segmenti co-moving al minimo, R−L=ΔB §96, rotore §77); scia quasi-universale =
teorema alla §86 esteso a K? Dettaglio: docs/OCCURRENCE_SUPPLY_ADDENDUM.md.
**AGGIORNAMENTO §99 (caccia preregistrata: min_ep<=5 FALSIFICATO, orizzonte
realizzato):** 5000 semi freschi non selezionati (gate canonici 24/24 bit-identici +
hist per-record + zero G=0): min_ep max = 8 (6 testimoni/6980 = 0,086%, verificati
6/6 da lente indipendente) ⇒ il "5" era un quantile (trappola h beccata dalla caccia
§98g.1; cade solo l'upgrade a finestra costante, ep<=y_rel e Rifornimento Recente
A/B/C intatti). Firma-W0 dei testimoni UCCISA dalla baseline (frag>=34 nel 23-29%
dei record ordinari); fatti superstiti: gradiente frag-vs-min_ep, parola identica in
3 testimoni di 3 orbite (coda word-mediated?), coppia lontana dall'onset. FATTO
NUOVO (trappola pp: 230 G=0 scartati in silenzio dal mio tool, riparato): 2
violazioni REALI del tripwire-orizzonte su 29.084 record freschi (residuo V(onset+P)
bianco, onset a 2.372/14.757 passi) = caveat V† di §98c realizzato; il meccanismo
G>=1 e' sano SOLO alla V†; 1620/1620 di §89a era (anche) fortuna del campione
(~7e-5). Coda doppia (ep>5 ⇒ age<=10P, 6/6) POST-HOC, preregistrata per §100
(min_ep>8 E min_age>1040, catena disgiunta, >=25k semi, potenza asserita). Prossimo
§100: caccia coda doppia; geometria V†\V sui 2 violatori; parole ripetute nella coda.
Dettaglio: docs/MINEP_HUNT_ADDENDUM.md.
**AGGIORNAMENTO §100 (coda doppia REALIZZATA, guarigione V†, fascia word-mediated):**
terza morte preregistrata: 25k semi catena-2 (disgiunzione verificata, verdetto
emesso dal tool) ⇒ 4 falsificatori min_ep>8 & min_age>10P (= 2 episodi, 4/4
bit-identici dalla lente), min_ep max 12 (5→8→12 = quantili); "0/6" §99 = 0/3
episodi vs 20/34, p~7% (contare EPISODI). I falsificatori realizzano ep=y_rel CON
UGUAGLIANZA (q=0): il soffitto della Scala e' TIGHT — niente costanti sotto.
Autopsia V† 2/2: divergenza a d=542/750 su cella NERA reale a y_rel 21/25 oltre
l'orizzonte corto; la † profonda rispetta ep<=y_rel (19<=21): Scala horizon-free;
min_ep† indeterminato (prima-divergenza != residuo † completo). Fascia
word-mediated: 45 testimoni → 14 parole (>20σ vs coupon-collector, 3 pesanti
cross-catena, burden quantizzati, onset_germe 55 == violatori: aria di ingressi
mancati) MA baseline stratificata nega la promozione (concentrazione gia' a
min_ep=4: top-60; gradiente 90,5%→42%→31%): REGIME della fascia alta, non
famiglia. Trappola qq. Pannello 2/2 (1 ROSSO episodi-vs-record riparato).
Prossimo §101: censire il regime min_ep>=4 (parola top-60, cross-catena, legame
porta/A1 §78), quotare censimento V†, riscandire i misti.
Dettaglio: docs/DOUBLE_TAIL_ADDENDUM.md.
**AGGIORNAMENTO §101 (RECORD-DIVERGENCE: dicotomia, primi lock ai record, fascia = porta):**
d(t) = profondita' di prima divergenza del rigioco del germe al record (mai censita).
DICOTOMIA DEL RECORD (deduttiva, Lemmi 0-5'): (T) rigetto nel transiente / (R) lock
W0-like di ride = d − onset_germe passi / (E) ingresso; Link 1 ⟸ "(R)/(E) i.o. ai
record" (unidirezionale). Censimento canonico (gate §89a/b/§98 riprodotti, T-DIV
due-derivazioni 1639/1639): T su 1639/1639, d med 17 (0,6% del transiente), colpevole
piu' vicina cheb med 3 max 8, min_ep† med 2 max 5 (flag §100 chiuso), G† med 142
zeri 0, drift-giu' 891/1639. Caccia preregistrata catena-3 (8000 semi, 82.243
record): F1 morto (min_cheb max 19: quarta soglia-quantile, qq), **F2 REALIZZATO —
primi 2 EPISODI di lock ai record (ride 269/384 = 2,6/3,7 periodi)**, P3 falsificata,
**V† 0 violazioni su 82.243** (Replay-Lock alla daga perfetto; 578 G†=0 fisiologici).
SALDATURA: le parole dei 2 lock = STESSA parola 101-bit cross-seme (+ shift-10) e
stanno nei 14 testimoni della fascia §100 ⇒ fascia = classe delle parole-porta
("alto min_ep = tentativi di porta" realizzato). Struttura drift: il ride muore solo
risalendo nel visitato (y_rel 16-19) ⇒ ai record drift-giu' l'eterna ha colpevole
FORZATA nel transiente. Pannello: lente A 40/40 + 11/11, esche 3/3 + terra-check
Lemma 0, lente logica (Lemma 5' indebolito, episodi contati). Prossimo §102:
occorrenza della fascia (enumerazione parole veloci realizzabili record-compatibili,
legame A1 §78); costo del transiente sporco drift-giu' (attacco alla-Muro per-parola);
min_cheb solo preregistrato. docs/RECORD_DIVERGENCE_ADDENDUM.md.
**AGGIORNAMENTO §105 (pannello §105a + BUCHI §105b):** pannello §102-104 SALDATO
(lente indipendente 30/30+20/20, ri-enumerazione 671, 25/25 realizzazioni
costruttive, saturazione Lingua a 1 periodo). §105b: meccanismo dei lock ai
record = read-set del transiente minuscolo (9/14 celle vs 454/931) nel cuneo
vergine del drift laterale (drift_x −6 in entrambi gli episodi), con consumo a
catena (Lemma 3); scalinata NON e' filo-di-rasoio (colpevoli=pose 10%, scudo =
detrito d'escursione, spesso). Bersaglio nuovo in scala: evitamento duale — puo'
un'eterna tenere per sempre i read-set delle parole veloci nel cono visitato?
Prossimo §106: |read-set(w)| word-decidibile sulle 1459 canoniche; cuneo
formalizzato col Cono §87. docs/LOCK_HOLE_ADDENDUM.md.
**AGGIORNAMENTO §106 (SPEED-LIMIT):** LEMMA DEL CUNEO + TEOREMA DEL LIMITE DI
VELOCITA' (deduttivi: L1+Scala+Lemmi §101): read-set tutto garantito-vergine ⇒
l'orbita cavalca; contrappositiva = vincolo di lentezza word-decidibile sulle
eterne ai record di classe T. Terra: T2 6055 garantite 0 nere; T1 1622/1622;
T3: i 2 lock reali = 0 garantite (fortuna, non velocita'): l'ipotesi non e'
ancora realizzata in natura. Nemico stretto fra lentezza forzata + buchi da
evitare (~1/40k). Prossimo §107: incompatibilita' dei due obblighi su discesa
B-T infinita, o falsificazione costruttiva (politica lenta perpetua ⇒ bersaglio
record-anchored falso, Link 1 fuori-record). docs/SPEED_LIMIT_ADDENDUM.md.
**AGGIORNAMENTO §107a (DANGER-CLASS):** |R_T| sui 1639 canonici min 4/med 302/max
3956; classe <=15 = 0,2% (contiene i 2 lock: 14 e 9); <=50 = 4% su 20/24 orbite.
PIEGA SU γ: falsificatore costruibile del bersaglio record-anchored = o
controesempio-γ (escluso <=40) o α1 stessa. Scala finale: Link 1 ⟸ (i)
occorrenza classe pericolosa i.o. ∧ (ii) fallimento scudo (vie deduttive note
tutte chiuse; serve argomento nuovo cuneo-vs-scudo; (ii) realizzato 2/82k).
docs/DANGER_CLASS_ADDENDUM.md.
**AGGIORNAMENTO §107b (SCUDO ANTICO):** attacco per-parola all'indietro (strada
scelta con confronto a 2 round vs secondo Fable). F0 `danger_geometry_census.py`:
theta_min DEGENERE (=2 quasi ovunque: il Cuneo non forza mai l'intero read-set
word-side), classe ≡ taglia ≡ direzionale ≡ transiente corto (coh 0.535→0.92;
lock 0.93/1.00): saldatura H1↔H3 = ri-descrizione; shift-10 cross-lock word-side.
F2 `danger_backward_autopsy.py` (classificazione AL CAP, trappola rr; GA naive
bit-identica, GB passato reale 2/2, lente esterna indipendente verde): a D=28
i lock hanno 12/14 e 5/9 celle di R_T irraggiungibili da ogni passato <=28 ⇒
bit dell'OR-kernel ANTICHI (>129 passi); WHITE_ALL=0; σ_D(w) = quota-shield dei
passati validi, BIMODALE sulla classe (q25 0.0002/med 0.10/q75 0.90; σ=1 esatto
= parole deduttivamente sicure a prof. dichiarata); lock σ_22 0.080/0.0012 NON
estremi (24/66 a σ<=0.01) ⇒ (ii) senza discriminante word-side: fallimento
scudo = proprieta' della pre-storia antica (deposito antico nel cono del
drift). Prossimo: raggiungibilita' minima per cella; σ_D sul vocabolario
intero; scudo antico vs Cono §87. docs/DANGER_BACKWARD_ADDENDUM.md.
**AGGIORNAMENTO §107c (RAGGIO DEL DEPOSITO):** P1a eseguita (2 round vs secondo
Fable; lente esterna a inizio sessione, gate sul GAP vs matched, tripla
anti-ri-descrizione). Motore C 10-11 ns/nodo (51G nodi/37 s), validazione
totale (R0/R0b/R1/RG + lente 17/17+15/15 + R2 completo + R2-profondo + somme
shard). **L'orizzonte CHIUDE**: tutte le celle di R_T raggiungibili entro
d_hit<=48 (A)/<=36 (B) ⇒ "bit antichi=irraggiungibili" di §107b in parte
artefatto del cap (trappola ss); fatti stabili: TRIPLA per cella + "colore
deciso da pittura >= d_hit+101 passi" (raggio esatto 137-149 A / 117-137 B);
GAP gate preregistrato REGGE (32 vs 24 A — ombra in gran parte della
regione-cuneo; 12 vs 4 B, zero censure); **il passato reale non legge MAI R_T
fino al seme** (13/14 e 9/9; = cuneo vergine §105b) ⇒ (ii) = verginita'
perpetua, oggetto = divario albero-48/dinamica-MAI. P2: 1459/1459 esatte a
D=22 (zero troncate, regressione 66/66): σ=1 esatto 71 (4,9%) ⇒ riduzione di
(i) per dominanza-sicura MORTA; σ<=0.01 = 59 (4%) concentrate |R_T| 16-50
(37% della banda). Prossimo §107d: Cono §87 vs cuneo (d_hit come budget), F3
calibrazione (join sigma_vocab_perword × griglia §106), reach sulle 59 σ≈0.
docs/DANGER_REACH_ADDENDUM.md.
**AGGIORNAMENTO §107d (SHIELD-MAP, v2 corretta dal pannello del titolare —
v1 in 718c9c1):** sessione di risultati NEGATIVI utili, macchinario griglia
validato (GF3 OR=1 1639/1639 = T⟺OR §101; GF2 lock OR=0 esatto; replay
bit-per-bit; GW0 entro tolleranza): (1) sigma_D non predice la ricchezza
nera reale (mediane 0,30-0,33 ovunque; Spearman 0,0755; condizionato
[−0,15,0,09]) = trappola (tt); sigma=1 resta deduttivo. (2) Classe sigma≤0.01
rinominata SIGMA-LOW ("lock-capable" ritirato): 32/59 open=cap, 13 cap=1,
0/59 white_all = assenza di certificato nero, non passati-bianchi. (3) Gap
d'albero dei lock non uniforme nella classe (48 confronti finiti: 16>/25=/7<).
(4) Mappa = P(nero|c∈R_T) condizionata; "lock nel nucleo denso" era artefatto
di Simpson (trappola uu): densita' 2D reale ai lock 0,19/0,12 (righe giovani);
§105b NON ribaltato, Cono non escluso; "antico/word-indipendente/deposito
correlato/zeri strutturali/quasi-estinti" RITIRATI (ERRATA 107d.0). (5)
**RIDUZIONE A LINK 1 CORRETTA (era lacunosa):** forma sufficiente = #{t:
classe-κ ∧ ride(t)=d(t)−og>=L_0} = ∞; l'OR-kernel attuale (transiente fino a
og) da' solo d>=og (ride anche 0) ⇒ serve KERNEL ESTESO R_{T,L} (letture
esogene fino a og+L; compatibile ⟺ ride>=L). Prossimo §107e (mossa unica):
R_{T,104} + forense last-paint + ipotesi last-paint cutset (ordine ben
fondato), test minimo 2 lock + controlli T, gate 1-6; se fallisce ⇒
consolidamento. docs/SHIELD_MAP_ADDENDUM.md.
**AGGIORNAMENTO §107e (KERNEL-EXTENDED, v2 con ERRATA 107e.0):** mossa
unica eseguita. Bicondizionale R_{T,104} compatibile ⟺ ride>=104 =
**teorema deduttivo sotto le ipotesi del record stretto (Lemmi 0-1 §101);
implementazione VERIFICATA su 1.641 record** (T-DIV esteso d_a==d_b,
mismatch assente a kernel bianco, zero unknown; regressioni bit-esatte
d-CSV §101 e d_full lock 324/449; gate 1(c) non indipendente; banda
0<=ride<104 vuota nel campione; supporto word-decidibile, VERDETTO
word+griglia). Forense bianco≠vergine esatta: kernel lock 66/67 vergini
(esatto sui 67, non generalizzabile) + 1 visitata-pari = cella consumata
§105b (terzo percorso di controllo parzialmente indipendente); first-bad
n_vis med 1, 50 da-seme, gap_ep med 2 max 8 (quantili). **H-NR =
iniettivita' pura degli eventi di pittura UCCISA** (morte attesa
dichiarata): 103.980 eventi unici non-seme, 55.359 a molteplicita'>=2,
37.116 condivisi da record non adiacenti — muore ogni prova dal non-riuso
stretto (parente trappola n); riuso controllato/nesting logicamente aperti
senza candidato definito (specifica di ricerca: rango su
t↦last_W2B(first_bad(t)), monotonia dedotta, PRIMA di ogni calcolo).
Regola preconcordata ⇒ **§108 = CONSOLIDAMENTO** con separazione rigida:
teoremi universali con ipotesi / certificazioni finite / osservazioni
campionarie / crux aperti e strade falsificate. Crux invariato:
#{t: classe-κ ∧ ride(t)>=L_0} = ∞ NON dimostrata.
docs/KERNEL_EXTENDED_ADDENDUM.md (v2).
**AGGIORNAMENTO §108-v1 (CONSOLIDAMENTO):** inventario completo a quattro
strati compilato da due lettori indipendenti (versioni post-ERRATA
obbligatorie, zero claim nuovi, ogni voce con § e file): volume A §40-§97
(28 [T] / 21 [C] / 13 [O] / 12 [X]) + volume B §57-§75+§78-§86+§98-§107e
(15 / 20 / 34 / 25) + documento-testa con architettura a 6 pilastri (locale
sigillato δ_r r<=4; γ periodo minimo <=41; β = δ_r + A1; Muro/U2 con corno
3b ⟺ 8 firme; lato-record meccanizzato col kernel esteso; crux unico
#{t: classe-κ ∧ ride>=L₀} = ∞ NON dimostrato) e **17 DA CHIARIRE** per il
pannello del titolare. Regola di riapertura: solo invariante preregistrato
coi 6 gate §107d.6. docs/CONSOLIDATION_108.md (+_A, _B).
**AGGIORNAMENTO §108b (PANNELLO §108 + STESURA FINALE):** le 17 DA CHIARIRE
DECISE dal titolare (verdetto 2026-07-24) e applicate ai tre documenti (v2;
zero nuove simulazioni, zero claim nuovi; v1 in 34ada36). Decisioni chiave:
"crux unico" RITIRATO ⇒ **crux operativo centrale della linea record-side**
= #{t: classe-κ ∧ ride>=L₀} = ∞ (restano formalmente aperti ANCHE corno 3b
del Muro, ipotesi (A) di onset finito per ogni parola presentabile, tratto
γ 42-102; "unico" solo dopo riduzione esplicita degli altri obblighi);
T17 spezzato (corni 1/2/3a [T] parziali, 3b [X]=X6; NESSUN raggio unico del
Muro — forma per-parola B_inf(z_t, r_seed(w)) disgiunta da origine+seme,
63 = max sulle 273.459 censite); T3-D<=33 in due strati ([T] condizionale
con S_CORE + lemma sound + enumerazione max 33; [C] = C14); convenzioni
canoniche: record stretto y_t < min_{s<t} y_s (heading/footprint =
conseguenze), V†_H per-verdetto (U1 H=2600; record-side t† = max(2600,
og_rec+2080)), og_rec/og_win ("asse assoluto og+101" ELIMINATO, sempre
ride = d − og_rec), γ dicitura unica "periodo minimo <=41" ("γ<=40"
eliminato), cavalcate per-raggio <=4 (r<=3) / <=2 (r=4), tre nozioni di
fase DISTINTE senza mappa; statuti: burden1 nel teorema solo >= m_K
(18/16/14/10 = censimento non filtrato, minimo vivo non dimostrato
raggiunto), D(w101) citabile solo =∞ (624 = early-exit storico; ∞ non
dimostra presentazione su singola eterna), 0,0455 [C] confermato non-bound,
impronta A1 = [C] senza P uniforme, §79 solo [O]/SCOUT, JSON §106d legacy,
Link 1 solo forma B4.19 (§104d = storia dell'errata), superstiti r=2,3 =
solo Teorema Halo + una classe realizzata, 0/1.223-vs-1/230 = [O] su
ensemble diversi + debito archiviato (misti mai riscanditi). Riconteggio:
A 28/21/13/12 INVARIATO; B 15/20/**35**/25 (+B3.35). **§108 CHIUSO come
consolidamento definitivo; §109 solo con nuovo lemma o invariante d'ordine
esplicito e preregistrabile.** docs/CONSOLIDATION_108.md (+_A, _B) v2.
Mandato post-§108b del titolare (2026-07-24): lavoro preliminare pre-§109
sul corno 3b (8 firme-exit) = **docs/PREREG_RIENTRO_SCIA.md v2** (ERRATA-1
del pannello: L∃ = ∃f: ¬R_f distinto da v2 = ∀f — testimone falsifica v2,
non L∃; F1-v2/F1-L separati; Fase 0 sola geometria locale; Fase 0b
lemma-ponte RC2 prima di ogni macchina; Fase 1 caccia al falsificatore di
v2, PE|PC condizionata / solo PF disgiunta, soglie per-firma; Fase 2 =
proxy diagnostico senza trasferimento deduttivo; §109 solo con vera
deduzione ¬R_f + gate verdi; esclusi γ forza-bruta, statistiche scudo,
ipotesi onset universale).
**AGGIORNAMENTO §102 (FASCIA-DOOR: fascia = porta-0, le porte reali sono due):**
la fascia NON ha suffisso-nucleo (comune globale 3 bit; troncare cambia l'onset:
proprieta' dell'intera finestra 101) — l'invariante e' la fase W0 d'ingresso del
germe: **12/14 a fase 0 esatta**, 2 a 99/102 (ext accidentale), 0 altrove. Onset
REALI delle 24 orbite: **porta-0 20/24** (10 esatte + 10 ext 1-7, coda 4-7
leggermente pesante dichiarata) + **porta-24/25 4/24**, zero fuori-cluster su 104
fasi. Molteplicita' reale delle porte ~2: l'occorrenza di Link 1 si concentra sulla
porta-0, decisa dal kernel A1 §78. Strumento: alpha1/fascia_door_probe.py (gate
24/24, fase univoca, esca beccata). Prossimo §103: fasi su ~10k semi freschi;
mappatura ↔ 22 porte §66 / fase-0 §74; evento "porta-0-completante" word-free e
tasso per-epoca ai record. docs/FASCIA_DOOR_ADDENDUM.md.
**AGGIORNAMENTO §103 (FRESH-PHASE):** 2500 semi freschi (preregistrato, verdetto dal
tool, gate 24/24): porta-0 95,4% (47,3% esatta + 48,1% ext), porta-24/25 4,1%,
12 fuori-cluster su fasi {16,30-31,91-92} = micro-porte (qq vale anche per le FASI);
istogramma ext uccide il modello a moneta §102: **picco a ext=5 (487 vs ~78) e buco
a ext=3 (1 vs ~156)** — l'approccio alla porta-0 e' strutturato (firma canonica di
~5 passi in fase 99, "3" quasi vietato). Prossimo §104: anatomia picco-5/buco-3 vs
E(k) §61 / 22 porte §66; micro-porte preregistrate; evento porta-0-completante ai
record = osservabile d'occorrenza di Link 1. docs/FRESH_PHASE_ADDENDUM.md.
**AGGIORNAMENTO §104 (DOOR-APPROACH):** vocabolario d'approccio canonico (ext5 = 1
parola 88%; fase-0 = famiglia suffisso `LRRRRLLL` 85%; top-10 68%); 11/14 germi
fascia = parola IDENTICA `RLRRLRRRRLLL` (#2 reale: la porta vive nel transiente del
germe); LEMMA LINGUA D'APPROCCIO (enumerazione esaustiva): 671/4096 approcci-12
realizzabili davanti a W0-fase-0 (saturo, osservate ⊆, 89 famiglie ⇒ concentrazione
dinamica); **spettro porte ai 1639 record = spettro ingressi freschi (95,4/4,5/0,2)
⇒ la meta' occorrenza di Link 1 collassa su B-T; Link 1 ai record = lim sup
[d − onset_germe] >= L0, nemico unico il rigetto-shallow perpetuo.** Pannello:
debito SALDATO in sessione (§104h: 30/30+20/20+25/25 costruttive, 671
ri-enumerato, 2 esche; correzione: saturazione gia' a 1 periodo). Prossimo §105: pannello blocco
§101-104; attacco per-parola al transiente porta-0 (~55 letture); selezione del
vocabolario (buco-3). docs/DOOR_APPROACH_ADDENDUM.md.
Roadmap completa:
CHAT_HANDOVER §C.
