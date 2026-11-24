"""tools/questions/lNN.json（オリジナル問題）から data.json の問題関連データを作り直す。
使い方:  python tools/build_questions.py
- Q（問題）, CP（各回の問題リスト）, QP（問題→教科書ページ）, O（出題順）, L（図解レッスンの確認問題）を更新する
- 教科書(TB)・用語集(G)などには触らない
"""
import json, glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data.json")
TAG = re.compile(r"</?(b|br|i|code|small|u|span)\b[^>]*>")
KEEP = ("tag", "k", "t", "o", "a", "rows", "opts", "x", "e", "m", "rd", "rg")

d = json.load(open(DATA, encoding="utf-8"))
qs = []
for f in sorted(glob.glob(os.path.join(ROOT, "tools", "questions", "l*.json"))):
    qs += json.load(open(f, encoding="utf-8"))
qs.sort(key=lambda q: q["id"])
ids = [q["id"] for q in qs]
assert len(ids) == len(set(ids)), "IDが重複しています"

CP = next(x for x in d if x.get("r") == "CP")
TB = {x["n"]: x for x in d if x.get("r") == "TB"}
LM = {x["id"]: x for x in d if x.get("r") == "L"}
cls = {c["n"]: c for c in CP["list"]}

newQ, byc, qp = [], {}, {}
for q in qs:
    n = int(q["id"][1:3]); c = cls[n]
    lt = next(l for l in c["lt"] if l in LM)
    r = {"r": "Q", "id": q["id"], "d": c["d"]}
    r.update({k: q[k] for k in KEEP if k in q})
    if TAG.search(json.dumps({k: q.get(k) for k in ("t", "e", "m", "o", "rows")}, ensure_ascii=False)):
        r["h"] = 1  # HTML（<b>など）をそのまま表示する
    r.update(src="orig", lt=lt, ci=0)
    newQ.append(r); byc.setdefault(n, []).append(q["id"])
    p = q.get("page")
    assert isinstance(p, int) and 0 <= p < len(TB[n]["pages"]), f"{q['id']} の page が教科書の範囲外: {p}"
    qp[q["id"]] = [n, p]

for c in CP["list"]:
    c["q"] = byc.get(c["n"], [])
alive = set(ids)
for l in LM.values():
    keep = [i for i in l.get("q", []) if i in alive]
    if not keep:
        keep = [i for c in CP["list"] if l["id"] in c["lt"] for i in byc.get(c["n"], [])][:6]
    l["q"] = keep

out = []
for x in d:
    r = x.get("r")
    if r == "Q": continue
    if r == "QP": x = {"r": "QP", "m": qp}
    if r == "O": x = {"r": "O", "ids": ids}
    out.append(x)
out += newQ
json.dump(out, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"問題 {len(newQ)} 問で data.json を更新しました")
