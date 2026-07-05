# ADDENDUM §97 — U2-LONTANO 5: la MACCHINA DEL COLLO (falsificazione della via a zona piccola)

**Riepilogo in una frase:** le due gambe del programma §96g.1 (enumerazione
degli approcci di chiusura + DAG whack-a-mole) sono state fuse in una sola
macchina finita ESATTA-IN-ZONA / OUT-LIBERO (`u2_far_collo_machine.py`,
stato = req per cella di zona + posizione/heading, direzione di soundness
giusta: l'astrazione allarga le traiettorie reali, quindi un'intersezione
vuota con le 8 firme residue sarebbe TEOREMA) — e la via e' stata
FALSIFICATA ai raggi piccoli: a radius 2 (esaustiva, 36.860 stati) la
macchina raggiunge 24 firme con insensibilita' totale ai flip dello stato
iniziale (osservazione B4, tutti i flip + coppie), a radius 3 (anello
cheb=3 esatto, 11/11 celle visitate da w101, 60M stati al CAP, firme =
lower bound) **tutte le 8 firme residue restano raggiungibili** — verdetto
INCONCLUDENTE ma **cap-robusto** (raggiungibilita' monotona) ⇒ nessun
teorema da zone a raggio ≤3 con ambiente libero: con rientro libero le
direzioni d'approccio sono libere per costruzione, e firme che differiscono
(anche) solo per heading non possono essere uccise. Quale delle tre cose
scartate dall'astrazione OUT porti la rigidita' reale del collo (req fuori
zona / continuita' uscita-rientro / mortalita' esterna) resta APERTO, con
esperimenti separatori nominati. Pannello §97 (2 lenti + sintetizzatore):
semantica della sovra-approssimazione SOUND (rientri adiacenti, congelamento
req, morte, rilevazione firme su ogni arco) e verifica di terra FORTE (il
testimone reale §96 proiettato passo-passo sulla macchina: 1.270 passi,
pend₂ identico a ogni passo); UN buco vero riparato (init loc=OUT sound
solo per cheb(posa_w101)=4 > R: a R=4 sarebbe stato UNSOUND — GATE B1) +
K1/K2 NON-DEFINITI sotto cap (trappola nuova mm) + washout retrocesso a
osservazione (trappola nuova ll, forma corretta). Il Z/4 dell'identita'
chirale NON morde in questa astrazione (come previsto: un'escursione
esterna libera assorbe qualsiasi Δheading).

Strumento nuovo: `alpha1/u2_far_collo_machine.py` (+ summary).

## 97a. La macchina (le due gambe fuse)

Modello: zona = {cheb ≤ R, y ∈ [1,R]} tracciata ESATTA (req per cella ∈
{FREE,0,1}; dinamica del camminatore all'indietro: cella letta cn = posa −
D[h] FORZATA da (posa, heading), lettura forzata da req(cn) — branch solo su
FREE —, il ledger flippa req(cn), la lettera fissa h′ = h−1 (R) / h+1 (L),
morte su y<1; su una cella visitata non-pending la lettura forzata e' L =
RIAPERTURA: il whack-a-mole e' nel modello per costruzione, non per
ipotesi); OUT = sovra-approssimazione (rientro da qualsiasi cella di zona E
con qualsiasi heading h purche' la posa di provenienza P = E + D[h] sia
fuori zona con y ≥ 1; req fuori zona dimenticate). Stato int-packed
(anti-OOM, trappola g — la prima corsa con tuple ha toccato 9,6 GB ed e'
stata uccisa). Stato iniziale = nodo-w101 (radicamento §95): req misurate da
`exact_state(w101)`, (1,1) FREE, loc OUT, pend₂ = 6.

Soundness (direzione del kill): ogni estensione reale induce una traiettoria
della macchina (i passi in zona sono esatti; i tratti esterni reali sono un
sottoinsieme delle escursioni libere) ⇒ una firma NON raggiungibile dalla
macchina non e' realizzabile da nessun passato reale. Il DAG delle chiusure
(gamba b) esce dalla stessa esplorazione (archi = (cella chiusa, posa
precedente in palla)).

## 97b. Radius 2: il WASHOUT (osservazione diagnostica — retrocessa dal pannello)

A radius 2 (sola palla esatta): 36.860 stati, esaurita, **24 firme**
raggiungibili — tutte le 8 residue incluse. E l'osservazione: corrompendo lo
stato iniziale le firme raggiungibili non cambiano (misura post-pannello,
azione B4: **9 flip singoli + 36 coppie, tutte corse esaustive, TUTTE
insensibili** — `washout_osservazione = True`, zero config sensibili). Il pannello ha RETROCESSO la prima formulazione: (i) la corsa
iniziale aveva UN solo flip come testimone di "totalita'"; (ii) il
meccanismo dichiarato ("il rientro becca le celle di palla direttamente") e'
letteralmente falso per 3 celle su 10 — (−1,1), (0,1), (1,1) non hanno pose
esterne adiacenti con y≥1 e sono riconfigurabili solo via cammino in-zona
forzato; (iii) l'esca N3 (vietare i 2 rientri di riga 1) fa cadere 4 firme
tra cui la residua ((2,2),3): le firme DIPENDONO dagli entry-points. Resta
il contenuto diagnostico: un'insensibilita' alle condizioni iniziali e' il
sintomo che l'astrazione ha buttato il vincolo portante — da testare SEMPRE
(trappola ll), con TUTTI i flip e corse esaustive, mai con un testimone
solo.

## 97c. Radius 3: washout spezzato, ma le 8 restano raggiungibili

w101 visita TUTTE le 11 celle dell'anello cheb=3 (GATE W1b) ⇒ req
dell'anello tracciate esatte; le celle di palla non sono piu' beccabili dal
rientro diretto (si entra dall'anello, lettura forzata, cammino esatto).
Esiti (60M stati, CAP raggiunto — esplorazione NON esaustiva, le firme sono
un lower bound; il verdetto pero' e' cap-indipendente perche' le 8 residue
sono GIA' state raggiunte):

- **23 firme raggiungibili** — un **LOWER BOUND** (esplorazione al cap, non
  esaustiva; radius 2 esaustivo ne dava 24), **tutte le 8 residue incluse**;
- il verdetto INCONCLUDENTE e' **cap-robusto**: la raggiungibilita' e'
  monotona, le 8 residue trovate restano trovate;
- K0 verde (firma reale raggiungibile — la macchina non e' unsound per
  difetto); K1/K2: **NON-DEFINITI sotto cap** (pannello B2, trappola mm:
  due BFS cappate hanno frontiere diverse, il confronto differenziale tra
  prefissi non dice nulla; i flag `esaurita` vengono propagati e il ramo
  TEOREMA esige l'esaustivita' di TUTTE le corse confrontate).

**Conclusione (falsificazione della gamba a cosi' com'era, enunciato
trasferibile):** l'esatto-in-zona a raggio ≤3 con ambiente OUT libero e
senza memoria NON esclude le firme residue — con rientro libero le
direzioni d'approccio sono libere, e firme che differiscono (anche) solo
per heading non possono essere uccise. Il DAG whack-a-mole (gamba b)
subisce la stessa sorte: sotto rientro libero non ha pozzo unico.
**Quale componente scartata dall'astrazione porti la rigidita' reale e'
APERTO** (pannello, punto 7): l'OUT-libero butta via TRE cose insieme —
(a) le req fuori zona, (b) la continuita' geometrica uscita→rientro,
(c) la mortalita' esterna — e i dati non discriminano. Esperimenti
separatori proposti: guscio di req ricordate a cheb R+1..R+k con rientro
teletrasportato (testa (a) senza (b)); rientro vincolato al quadrante/lato
d'uscita con req esterne libere (testa (b) senza (a)).

## 97d. Z/4: onesta' preventiva confermata

L'assioma chirale R−L=ΔB (heading ≡ ΔB mod 4, §96d) era candidato a vincolo
dell'enumeratore. Nell'astrazione OUT-libero NON morde: su un'escursione
esterna Δh ≡ ΔB_out (mod 4) con ΔB_out libero (il vagabondaggio esterno
assorbe qualsiasi classe) ⇒ nessuna pota. Resta candidato per modelli con
escursioni esterne vincolate (§98).

## 97e. Pannello §97 (2 lenti + sintetizzatore con verifica sul campo)

- **Lente logica (soundness, 7 attacchi):** rientri/adiacenza REGGE (ogni
  posa reale con y≥1 e' una cella letta ⇒ i rientri sono tutti adiacenti e
  coperti da entry_pts; nessun attraversamento di zona senza lettura);
  congelamento req a OUT REGGE (il segmento esterno non tocca req di zona
  per definizione); morte y<1 REGGE (ordine dei check necessario e
  corretto); rilevazione firme REGGE (su ogni arco, prima del filtro seen,
  rientri inclusi). **UN BUCO di soundness vero: l'init loc=OUT non era
  gated contro la posa di continuazione di w101** — (4,1) ha cheb 4 e a
  R≥4 cade IN zona: la macchina sarebbe stata UNSOUND esattamente al raggio
  del riuso previsto (riparato: GATE B1, assert cheb(posa)>R). **K1/K2
  sotto cap = confronto tra BFS troncate con frontiere diverse: NON
  DEFINITI** (riparato: flag esaurita propagati, trappola mm). Washout
  "totale" da 1 flip: retrocesso (riparato: tutti i flip + coppie). La
  lettura "rigidita' = continuita' del cammino esterno": coerente ma NON
  derivata — riformulata come questione aperta con esperimenti separatori.
- **Lente esche (4/4 beccate):** N1 (vietare riaperture: 36.860→9 stati,
  24→0 firme — il whack-a-mole e' il motore di quasi tutta la
  raggiungibilita'); N2 (heading-prima-del-passo: insieme = rotazione h+1
  della baseline — beccata dal confronto insiemistico, NON dal solo K0:
  **K0-membership e' un controllo positivo debole**, cieco alle rotazioni
  globali); N3 (vietare i rientri di riga 1: 24→20 firme, muore la residua
  ((2,2),3) — non vacua, le firme dipendono dagli entry-points); N4
  (verifica di terra FORTE: il testimone reale §96 rigenerato
  deterministicamente e PROIETTATO passo-passo sulla macchina radius 2 —
  1.270 passi: 10 rientri tutti in entry_pts, 17 passi in zona, 26 letture
  forzate coincidenti, pend₂ macchina == reale a ogni passo, firma finale
  coincidente: la sovra-approssimazione e' radicata a terra).
- Raccomandazione R1 (adottata a verbale): il controllo positivo forte per
  le macchine astratte e' il **replay proiettato di terra** (stile N4), non
  la membership della firma.

## 97f. Trappole nuove

- **(ll) il washout e' l'esca obbligatoria delle macchine a zona esatta /
  OUT libero** (COLLO-MACHINE §97): se l'insieme degli esiti raggiungibili
  NON cambia corrompendo lo stato iniziale, l'astrazione ha buttato il
  vincolo portante e l'esito non dice nulla sul sistema reale — ne' in
  positivo ne' in negativo. Testare SEMPRE il washout PRIMA di leggere il
  verdetto, con TUTTI i flip singoli (+ coppie) e corse ESAUSTIVE — un
  flip solo e' un testimone di insensibilita', non di totalita' (pannello
  B4). Un K1 rosso non e' un bug del gate, e' la diagnosi. Radice comune
  con (ff)/(cc); parente di (gg).
- **(mm) i confronti differenziali tra esplorazioni CAPPATE non sono
  definiti — e l'init "teletrasportato" va gated a ogni raggio**
  (COLLO-MACHINE §97, pannello B1/B2): due BFS al cap con semi/ordini
  diversi hanno frontiere diverse: confrontarne gli output (K1/K2, washout,
  coniugazioni) produce verdetti spuri in entrambe le direzioni — i flag
  `esaurita` vanno PROPAGATI e ogni gate differenziale etichettato
  NON-DEFINITO sotto cap; il ramo TEOREMA esige l'esaustivita' di TUTTE le
  corse confrontate. E ogni parametro di modello che oggi e' sound "per
  caso fattuale" (init loc=OUT con posa w101 a cheb 4 > R) diventa unsound
  cambiando UN parametro (R=4): assertare il fatto, non presumerlo.
  Parente di (hh) (il confronto dipende dalla politica di esplorazione).

## 97g. Domande aperte / programma §98

1. **La via esterna al Collo**: la rigidita' vive fuori zona. Tre attacchi
   nominati: (a) **motore C striscia allargata** (§93h.2-a, radius ≥ 4
   esatto — stime di stato severe: gia' radius 3 supera 60M in Python;
   servono C + rappresentazione compatta e/o esattezza parziale mirata);
   (b) **vincoli-scia sul rientro** (Teorema della Scia §86 all'indietro:
   le ultime k svolte del camminatore forzano le celle attorno al punto di
   uscita — accoppiare uscita e rientro con un budget finito di heading/
   parita', dove il Z/4 di §96d potrebbe finalmente mordere);
   (c) **invariante flux che sopravviva all'OUT** (per-pose §94d raffinato,
   gg-aware: la chiusura induttiva come gate, mai il campione).
2. Il negativo empirico sul Collo resta il piu' forte disponibile (603/603
   PC-only §96c): una realizzazione di una delle 8 firme ucciderebbe v2 —
   le cacce restano il falsificatore permanente.
3. Ereditati: fuggenti nuove vs nere-D≥400 (§94f.4); retro-nota §91c.3;
   stress-2 bianche; h1=1 (§92).

## 97h. Inventario file (alpha1/)

- `u2_far_collo_machine.py` (+`_summary.json`) — macchina del collo
  radius 2/3, gate W1b/R2/K0/K1/K2, DAG whack-a-mole, stati int-packed.
