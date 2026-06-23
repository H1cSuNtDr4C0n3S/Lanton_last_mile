# catalog_stats.py — statistica del catalogo dei fantasmi (delta4_alt_catalog.jsonl)
import json, sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
recs = [json.loads(l) for l in open(r"C:\Lanton_last_mile\results\delta4_alt_catalog.jsonl")]
print("fantasmi catalogati:", len(recs))
cons = [r for r in recs if r["conflitto"] is None]
print("consistenti:", len(cons))
recs = [r for r in recs if r["conflitto"] is not None]
d = sorted(r["conflitto"]["distanza"] for r in recs)
print(f"distanza del primo conflitto: min {d[0]}, q1 {d[len(d)//4]}, mediana {d[len(d)//2]}, "
      f"q3 {d[3*len(d)//4]}, max {d[-1]}")
print("stesso periodo:", sum(r["conflitto"]["stesso_periodo"] for r in recs),
      "/ cross-periodo:", sum(not r["conflitto"]["stesso_periodo"] for r in recs))
print("periodo in cui scatta il conflitto:", Counter(r["conflitto"]["periodo"] for r in recs))
print("verdetti B-T dei fantasmi:", Counter(r["bt"] for r in recs))
print("p (assumiB per ciclo):", Counter(r["p"] for r in recs))
qs = sorted(r["q"] for r in recs)
print(f"q: min {qs[0]}, mediana {qs[len(qs)//2]}, max {qs[-1]}")
print(f"costo: min {min(r['mean'] for r in recs):.5f}, max {max(r['mean'] for r in recs):.5f}")
print("duplicati (stessa parola canonica):", sum(r["dup"] for r in recs))
print("celle di conflitto piu' frequenti:",
      Counter(tuple(r["conflitto"]["cella"]) for r in recs).most_common(6))
print("offset del conflitto: min", min(r["conflitto"]["offset"] for r in recs),
      "max", max(r["conflitto"]["offset"] for r in recs))
