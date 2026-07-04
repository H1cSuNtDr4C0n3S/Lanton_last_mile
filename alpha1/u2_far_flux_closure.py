# u2_far_flux_closure.py — §94: PROMOZIONE DEDUTTIVA degli invarianti parity-flux.
#
# Input: i funzionali GF(2) di u2_far_parity_flux (37 uniformi tra le 8 fuggenti).
# Metodo (Houdini / invariante induttivo massimale):
#   - tipo-di-passo = (cn, h, req(cn), bit) con cn in W (c = cn + D[h], coordinate
#     note, dentro o fuori W), piu' i passi di uscita (c in W -> cn fuori W) e i
#     passi OUT->OUT (delta solo heading+parita', determinato da h);
#   - delta(t) = XOR dei bit di feature cambiati dal passo t (il passo tocca SOLO
#     la cella visitata cn = nuova posa: il req|W non e' MAI dimenticato — qui
#     l'astrazione OUT della trappola ff non puo' mordere: le visite sono pose);
#   - un tipo-di-passo e' AMMISSIBILE per l'insieme I se il sistema lineare
#     GF(2) {phi.v = c_phi (phi in I)} + {bit di posa/heading/req(cn)/parita'
#     fissati da t} e' risolubile (eliminazione di Gauss);
#   - CHIUSURA: per ogni t ammissibile e ogni phi in I, phi.delta(t) = 0.
#     Houdini: si eliminano i phi violati e si itera al punto fisso.
#   - I sopravvissuti sono INVARIANTI INDUTTIVI: veri a v0 (costante verificata
#     per-parola) => veri su OGNI nodo di OGNI albero dei prepend. TEOREMA.
#
# Bersaglio: phi_colonna0 = p(0,1) + p(0,2) + pose(0,2) ≡ 1 (sulle fuggenti).
#   Se sopravvive => a ogni nascita con posa != (0,2):
#   p(0,1) + p(0,2) = 1 => pend2 >= 1 => TEOREMA DEL LEDGER SPORCO (forma >=1):
#   ogni record y-min stretto con palla-2 priva di seme e' VIETATO alle coprenti
#   fuggenti con costante iniziale 1 (le finite sono gia' chiuse da Nascita
#   Vicina §93c/§94-censimento).
#
# SOUNDNESS del quantificatore: i tipi-di-passo enumerano TUTTE le transizioni
# localmente valide (y>=1 + realizzabilita' del req + alternanza forzata); la
# chiusura quantifica su OGNI stato che soddisfa I, non solo sui campionati.
# I passi con c fuori W usano solo informazione portata dalle feature: sound.
#
# GATE:
#   FC0 controllo positivo: l'invariante universale par(x+y)+par(h) (teorema
#       banale: ogni passo unitario toggla entrambi) DEVE sopravvivere;
#   FC1 esca: corrompendo delta (omettendo il toggle di parita') la chiusura
#       DEVE uccidere l'invariante universale (l'attacco puo' fallire);
#   FC2 le costanti iniziali phi.v0 sono ricontrollate con exact_state per le
#       8 fuggenti + le 34 del censimento.
#
# Uscita: alpha1/u2_far_flux_closure_summary.json (+ .log)
import sys, os, json, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from record_weapon_vitality import to_bits, SUMMARY
from u2_pocket_certificate import exact_state, FREE
from onset_cone_lock import DX, DY
from u2_far_parity_flux import (W_CELLS, W_IDX, NW, BALL2, F_P, F_V, F_POSE,
                                F_OUT, F_HEAD, F_PAR, F_BIAS, NFEAT,
                                feat_vector, dot)

HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "u2_far_parity_flux_summary.json")
WIT = os.path.join(HERE, "u2_cover_witnesses.json")
CEN = os.path.join(HERE, "u2_far_born_near_census_summary.json")
OUT_JSON = os.path.join(HERE, "u2_far_flux_closure_summary.json")
LOG = os.path.join(HERE, "u2_far_flux_closure.log")


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


# ---------------- algebra lineare GF(2) ----------------

def feasible(eqs):
    """eqs = lista (vettore int, rhs 0/1). True se il sistema e' risolubile."""
    rows = []                              # (vec, rhs) in forma echelon per msb
    piv = {}
    for vec, rhs in eqs:
        v, b = vec, rhs
        while v:
            m = v.bit_length() - 1
            if m in piv:
                pv, pb = piv[m]
                v ^= pv; b ^= pb
            else:
                piv[m] = (v, b)
                v = 0; b = 0
                break
        if v == 0 and b == 1:
            return False                   # 0 = 1: inconsistente
    return True


# ---------------- tipi di passo ----------------

def parity_bits(c):
    out = 0
    if c[0] & 1:
        out |= 1 << (F_PAR + 0)
    if c[1] & 1:
        out |= 1 << (F_PAR + 1)
    if (c[0] + c[1]) & 1:
        out |= 1 << (F_PAR + 2)
    return out


def pose_bit(c):
    return (1 << (F_POSE + W_IDX[c])) if c in W_IDX else (1 << F_OUT)


def step_types():
    """Enumera (nome, delta, vincoli) per ogni tipo di passo localmente valido.
    vincoli = lista (feature_idx, valore) da imporre nella feasibility
    (posa/heading/req(cn)); delta = XOR dei bit cambiati."""
    out = []
    # (i) cn in W (la visita tocca il req di cn)
    for cn in W_CELLS:
        i = W_IDX[cn]
        for h in range(4):
            c = (cn[0] + DX[h], cn[1] + DY[h])   # posa corrente: cn = c - D[h]
            if c[1] < 1:
                continue                          # posa impossibile
            base_fix = [(F_HEAD + hh, 1 if hh == h else 0) for hh in range(4)]
            # posa corrente: tutti i bit di posa fissati
            for cc in W_CELLS:
                base_fix.append((F_POSE + W_IDX[cc], 1 if cc == c else 0))
            base_fix.append((F_OUT, 0 if c in W_IDX else 1))
            # parita' della posa corrente: note (coordinate di c note)
            pb = parity_bits(c)
            for k in range(3):
                base_fix.append((F_PAR + k, (pb >> (F_PAR + k)) & 1))
            for req_cn, bits in ((FREE, (0, 1)), (0, (1,)), (1, (0,))):
                # req(cn): FREE -> p=0,v=0; 0 -> p=1,v=1; 1 -> p=0,v=1
                fix = list(base_fix)
                if req_cn == FREE:
                    fix += [(F_P + i, 0), (F_V + i, 0)]
                elif req_cn == 0:
                    fix += [(F_P + i, 1), (F_V + i, 1)]
                else:
                    fix += [(F_P + i, 0), (F_V + i, 1)]
                for bit in bits:
                    h2 = (h - 1) & 3 if bit == 1 else (h + 1) & 3
                    delta = 0
                    # req di cn: FREE+L -> p 0->1, v 0->1; FREE+R -> v 0->1;
                    # visitata -> p toggla
                    if req_cn == FREE:
                        delta ^= 1 << (F_V + i)
                        if bit == 0:
                            delta ^= 1 << (F_P + i)
                    else:
                        delta ^= 1 << (F_P + i)
                    # posa: c -> cn
                    delta ^= pose_bit(c) ^ pose_bit(cn)
                    # heading
                    delta ^= (1 << (F_HEAD + h)) ^ (1 << (F_HEAD + h2))
                    # parita': note entrambe
                    delta ^= parity_bits(c) ^ parity_bits(cn)
                    out.append((f"IN cn={cn} h={h} req={req_cn} bit={bit}",
                                delta, fix))
    # (ii) uscita: c in W, cn fuori W
    for c in W_CELLS:
        for h in range(4):
            cn = (c[0] - DX[h], c[1] - DY[h])
            if cn in W_IDX or cn[1] < 1:
                continue
            base_fix = [(F_HEAD + hh, 1 if hh == h else 0) for hh in range(4)]
            for cc in W_CELLS:
                base_fix.append((F_POSE + W_IDX[cc], 1 if cc == c else 0))
            base_fix.append((F_OUT, 0))
            pb = parity_bits(c)
            for k in range(3):
                base_fix.append((F_PAR + k, (pb >> (F_PAR + k)) & 1))
            for bit in (0, 1):                   # req(cn) fuori W: ignoto
                h2 = (h - 1) & 3 if bit == 1 else (h + 1) & 3
                delta = pose_bit(c) ^ (1 << F_OUT)
                delta ^= (1 << (F_HEAD + h)) ^ (1 << (F_HEAD + h2))
                delta ^= parity_bits(c) ^ parity_bits(cn)
                out.append((f"EXIT c={c} h={h} bit={bit}", delta, base_fix))
    # (iii) OUT -> OUT: posa resta OUT; parita' cambiano secondo h; le
    # coordinate sono ignote ma il DELTA di parita' dipende solo da D[h]
    for h in range(4):
        base_fix = [(F_HEAD + hh, 1 if hh == h else 0) for hh in range(4)]
        base_fix.append((F_OUT, 1))
        for cc in W_CELLS:
            base_fix.append((F_POSE + W_IDX[cc], 0))
        for bit in (0, 1):
            h2 = (h - 1) & 3 if bit == 1 else (h + 1) & 3
            delta = (1 << (F_HEAD + h)) ^ (1 << (F_HEAD + h2))
            if DX[h]:
                delta ^= 1 << (F_PAR + 0)
            if DY[h]:
                delta ^= 1 << (F_PAR + 1)
            delta ^= 1 << (F_PAR + 2)
            out.append((f"OUT h={h} bit={bit}", delta, base_fix))
    return out


def houdini(invs, steps, tag=""):
    """invs = lista (phi, const). Ritorna (sopravvissuti, uccisi, dettagli)."""
    alive = list(invs)
    killed = []
    rounds = 0
    while True:
        rounds += 1
        to_kill = {}
        for name, delta, fix in steps:
            # feasibility: I + vincoli del tipo di passo
            eqs = [(phi, c) for phi, c in alive]
            eqs += [(1 << idx, val) for idx, val in fix]
            eqs.append((1 << F_BIAS, 1))
            if not feasible(eqs):
                continue
            for j, (phi, cst) in enumerate(alive):
                if dot(phi, delta):
                    to_kill.setdefault(j, name)
        if not to_kill:
            break
        for j in sorted(to_kill, reverse=True):
            killed.append((alive[j][0], alive[j][1], to_kill[j]))
            del alive[j]
        log(f"  {tag}Houdini round {rounds}: uccisi {len(to_kill)}, "
            f"vivi {len(alive)}")
    return alive, killed, rounds


def readable(phi):
    supp = []
    for i in range(NFEAT):
        if (phi >> i) & 1:
            supp.append(
                f"p{W_CELLS[i-F_P]}" if i < F_V else
                f"v{W_CELLS[i-F_V]}" if i < F_POSE else
                f"pose{W_CELLS[i-F_POSE]}" if i < F_OUT else
                "OUT" if i == F_OUT else
                f"h{i-F_HEAD}" if i < F_PAR else
                ["x%2", "y%2", "(x+y)%2"][i - F_PAR] if i < F_BIAS else "1")
    return supp


def main():
    ap = argparse.ArgumentParser()
    args = ap.parse_args()
    t0 = time.time()

    pf = json.load(open(PF))
    invs = []
    for r in pf["invarianti"]:
        if not r["costante_uniforme"]:
            continue
        phi = 0
        for i in r["supporto_idx"]:
            phi |= 1 << i
        invs.append((phi, r["costante"]))
    log(f"chiusura §94: {len(invs)} invarianti uniformi in ingresso")

    # phi bersaglio: colonna-0
    phi_c0 = (1 << (F_P + W_IDX[(0, 1)])) | (1 << (F_P + W_IDX[(0, 2)])) \
        | (1 << (F_POSE + W_IDX[(0, 2)]))
    assert any(phi == phi_c0 for phi, _ in invs), \
        "phi_colonna0 non tra gli uniformi!"
    # controllo positivo FC0: par(x+y) + par(h) — cerca il rappresentante
    phi_univ = (1 << (F_PAR + 2)) | (1 << (F_HEAD + 1)) | (1 << (F_HEAD + 3))
    in_span_univ = any(phi == phi_univ for phi, _ in invs)
    log(f"phi_colonna0 presente; phi_universale presente come vettore: "
        f"{in_span_univ} (se no: e' nel coset, va aggiunto)")
    if not in_span_univ:
        # verifica che sia invariante sui dati: aggiungilo con costante dedotta
        # dalla prima parola (v0) e lascialo alla chiusura
        d = json.load(open(SUMMARY))
        w101 = to_bits(d["best_per_K"]["101"]["word"])
        wit = json.load(open(WIT))
        e2 = to_bits(wit["jackpot"][0]["word"])
        c0, h0, req0 = exact_state(tuple(e2) + tuple(w101))
        v0 = feat_vector(c0, h0, req0)
        invs.append((phi_univ, dot(phi_univ, v0)))

    steps = step_types()
    log(f"tipi di passo enumerati: {len(steps)}")

    alive, killed, rounds = houdini(invs, steps)
    surv_c0 = any(phi == phi_c0 for phi, _ in alive)
    surv_univ = any(phi == phi_univ for phi, _ in alive)
    log(f"CHIUSURA raggiunta in {rounds} round: vivi {len(alive)}/{len(invs)}")
    log(f"FC0 (controllo positivo, phi universale sopravvive): {surv_univ}")
    log(f"BERSAGLIO phi_colonna0 sopravvive: {surv_c0}")
    assert surv_univ, "FC0 FALLITO: l'invariante universale e' stato ucciso!"

    # FC1: esca — chiusura con delta corrotto (parita' (x+y) omessa nei passi
    # OUT): l'invariante universale DEVE morire
    steps_esca = []
    for name, delta, fix in steps:
        if name.startswith("OUT"):
            delta ^= 1 << (F_PAR + 2)
        steps_esca.append((name, delta, fix))
    alive_e, killed_e, _ = houdini([(phi_univ, invs[-1][1] if not in_span_univ
                                     else dict(invs)[phi_univ])],
                                   steps_esca, tag="esca ")
    fc1 = not any(phi == phi_univ for phi, _ in alive_e)
    log(f"FC1 (esca delta corrotto uccide phi universale): {fc1}")
    assert fc1, "FC1 FALLITO: la chiusura non becca il delta corrotto"

    # FC2: costanti iniziali per le fuggenti note (8 + 34 censimento)
    d = json.load(open(SUMMARY))
    w101 = to_bits(d["best_per_K"]["101"]["word"])
    wit = json.load(open(WIT))
    fugg = []
    for grp in ("jackpot", "nere400"):
        for k, w in enumerate(wit[grp]):
            fugg.append((f"{grp}[{k}]", to_bits(w["word"])))
    cen = json.load(open(CEN))
    for k, f in enumerate(cen["fuggenti_dettaglio"]):
        fugg.append((f"cens[{k}]", to_bits(f["word_ext"])))
    n_c1 = 0
    for name, e2 in fugg:
        c0, h0, req0 = exact_state(tuple(e2) + tuple(w101))
        v0 = feat_vector(c0, h0, req0)
        cst = dot(phi_c0, v0)
        if cst == 1:
            n_c1 += 1
        else:
            log(f"  FC2: {name} ha costante colonna-0 = 0 (non coperta dal "
                f"teorema-ledger; va chiusa via albero finito)")
    log(f"FC2: costante colonna-0 = 1 su {n_c1}/{len(fugg)} fuggenti note")

    out = {"invarianti_ingresso": len(invs),
           "tipi_di_passo": len(steps),
           "round_houdini": rounds,
           "sopravvissuti": [{"supporto": readable(phi), "costante": c}
                             for phi, c in alive],
           "uccisi": [{"supporto": readable(phi), "costante": c,
                       "passo_killer": nm} for phi, c, nm in killed],
           "phi_colonna0_sopravvive": surv_c0,
           "fc0_universale": surv_univ,
           "fc1_esca": fc1,
           "fc2_costante1_su_fuggenti": [n_c1, len(fugg)],
           "elapsed_s": round(time.time() - t0, 1)}
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=1)
    log(f"scritto {OUT_JSON} in {out['elapsed_s']} s")
    if surv_c0:
        log("*** TEOREMA CANDIDATO (chiusura induttiva verificata): a ogni "
            "nodo di ogni albero dei prepend di una coprente-nera con "
            "costante colonna-0 = 1, p(0,1)+p(0,2)+[posa=(0,2)] = 1; alla "
            "nascita fuori palla-2: pend2 >= 1. ***")
    else:
        killer = [k for k in killed if k[0] == phi_c0]
        log(f"phi_colonna0 UCCISO da: {killer[0][2] if killer else '?'} — "
            f"servono feature piu' ricche o realizzazione concreta")


if __name__ == "__main__":
    main()
