"""data.json の問題データをざっと点検する。  python tools/check.py"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, "data.json"), encoding="utf-8"))
TB = {x["n"]: x for x in d if x.get("r") == "TB"}
ng = []
for q in (x for x in d if x.get("r") == "Q"):
    i, k = q["id"], q.get("k")
    for f in ("t", "e"):
        if not q.get(f): ng.append(f"{i}: {f} がない")
    if k == "one" and not (isinstance(q.get("a"), int) and 0 <= q["a"] < len(q["o"])): ng.append(f"{i}: a が不正")
    if k == "multi" and not (isinstance(q.get("a"), list) and len(q["a"]) >= 2 and all(0 <= a < len(q["o"]) for a in q["a"])): ng.append(f"{i}: multi の a が不正")
    if k == "sel" and any(r["a"] not in q["opts"] for r in q["rows"]): ng.append(f"{i}: sel の分類名が opts にない")
    if k == "match" and any(len(p) != 2 for p in q["o"]): ng.append(f"{i}: match の組が不正")
for n, b in TB.items():
    c = b.get("cls", {})
    if c.get("seg") and len(c["seg"]) != len(c["lines"]): ng.append(f"第{n}回: seg と lines の数が違う")
    if sum(1 for l in c.get("lines", []) if l.get("w")) != 1: ng.append(f"第{n}回: 小テストで止まる行(w)が1つでない")
print("\n".join(ng) or "問題なし"); sys.exit(1 if ng else 0)
