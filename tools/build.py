"""src/ から data.json を作り、続けて check.py で点検する。  python tools/build.py
- src/lessons/lNN.json    … 各回の教科書（pages）と授業（cls）＝ TB
- src/questions/lNN.json  … 各回の問題（形式は src/questions/INSTRUCTIONS.md）。問題IDは旧50回の番号のままで、どの回かはファイルで決まる
- src/base/*.json         … 用語集・図解レッスン・コマンド練習など
問題からは Q（問題）, CP の各回の問題リスト, QP（問題→教科書ページ）, O（出題順）, L の確認問題 を作る。
src/ のファイルは書き換えない（data.json だけを書く）。
"""
import glob, json, os, re, subprocess, sys
import srcio
import qfigs   # 問題の構成図（tools/qfigs.py）
import extra_pages   # 教科書に足す「もっとくわしく」のページ（tools/extra_pages.py）

sys.stdout.reconfigure(encoding="utf-8")

TAG = re.compile(r"</?(b|br|i|code|small|u|span)\b[^>]*>")
KEEP = ("tag", "k", "lv", "t", "o", "a", "rows", "opts", "x", "e", "m", "rd", "rg")

base = {r: srcio.load(srcio.base_path(r)) for r in srcio.BASE}
TB = {}
for f in sorted(glob.glob(os.path.join(srcio.SRC, "lessons", "l*.json"))):
    x = srcio.load(f); TB[x["n"]] = x
assert sorted(TB) == list(range(1, 82)), f"src/lessons の回がそろっていません: {sorted(TB)}"


def fit_svg(svg):
    """図の部品（円・四角）が 0〜360 の外にはみ出していたら、viewBox を横に広げて全部見えるようにする"""
    m = re.search(r'viewBox="0 0 360 ([\d.]+)"', svg or "")
    if not m:
        return svg
    xs = [(float(a) - float(r), float(a) + float(r)) for a, r in re.findall(r'<circle cx="([\d.\-]+)" cy="[\d.\-]+" r="([\d.]+)"', svg)]
    xs += [(float(a), float(a) + float(w)) for a, w in re.findall(r'<rect x="([\d.\-]+)" y="[\d.\-]+" width="([\d.]+)"', svg)]
    lo = min([0.0] + [a for a, _ in xs]); hi = max([360.0] + [b for _, b in xs])
    if lo >= 0 and hi <= 360:
        return svg
    lo, hi = lo - 4 if lo < 0 else 0, hi + 4 if hi > 360 else 360
    return svg.replace(m.group(0), f'viewBox="{lo:g} 0 {hi - lo:g} {m.group(1)}"', 1)


# ページの並べかえ：授業の「今日のまとめ」を最後にし、その前に付録（JSONでまとめの後ろにあるもの）と
# extra_pages の「もっとくわしく」を入れる。授業の場面（sc）と問題の page は、新しい並びに付け替える。
PMAP, XSTART = {}, {}   # PMAP[n][元の番号] = 新しい番号、XSTART[n] = 「もっとくわしく」の始まりの番号
for n in TB:
    pg = TB[n]["pages"]
    s = max((i for i, p in enumerate(pg) if "quiz" not in p and "まとめ" in p.get("t", "")), default=len(pg) - 1)
    tail, xs = pg[s + 1:], extra_pages.EXTRA.get(n, [])
    TB[n]["pages"] = pg[:s] + tail + xs + [pg[s]]
    PMAP[n] = {i: (i if i < s else i - 1 if i > s else len(TB[n]["pages"]) - 1) for i in range(len(pg))}
    XSTART[n] = s + len(tail)
    for l in TB[n].get("cls", {}).get("lines", []):
        l["sc"] = PMAP[n][l["sc"] - 1] + 1
    for p in TB[n]["pages"]:
        if p.get("svg"):
            p["svg"] = fit_svg(p["svg"])

# ---- 問題 ----
qs, qn = [], {}   # qn：問題ID → 回（ファイルの番号。IDの番号は旧50回のもので、回とは一致しない）
for f in sorted(glob.glob(os.path.join(srcio.SRC, "questions", "l*.json"))):
    n = int(re.search(r"l(\d+)\.json$", f).group(1))
    for q in srcio.load(f):
        qs.append(q); qn[q["id"]] = n
qs.sort(key=lambda q: q["id"])
ids = [q["id"] for q in qs]
dup = sorted({i for i in ids if ids.count(i) > 1})
assert not dup, f"IDが重複しています: {dup}"
assert not set(qfigs.FIG) - set(ids), f"qfigs.py に、ない問題の図がある: {sorted(set(qfigs.FIG) - set(ids))}"

CP = base["CP"][0]
LM = {x["id"]: x for x in base["L"]}
cls = {c["n"]: c for c in CP["list"]}

newQ, byc, qp = [], {}, {}
for q in qs:
    n = qn[q["id"]]; c = cls[n]
    lt = next(l for l in c["lt"] if l in LM)
    r = {"r": "Q", "id": q["id"], "d": c["d"]}
    r.update({k: q[k] for k in KEEP if k in q})
    if TAG.search(json.dumps({k: q.get(k) for k in ("t", "e", "m", "o", "rows")}, ensure_ascii=False)):
        r["h"] = 1  # HTML（<b>など）をそのまま表示する
    r.update(src="orig", lt=lt, ci=0)
    if q["id"] in qfigs.FIG:
        r["fig"] = fit_svg(qfigs.FIG[q["id"]])   # 構成図（SVG）
    newQ.append(r); byc.setdefault(n, []).append(q["id"])
    p = q.get("page")
    if q["id"] in extra_pages.QPAGE:   # 足したページを参照させる
        xn, k = extra_pages.QPAGE[q["id"]]
        assert xn == n, f"{q['id']} は第{n}回の問題なのに、extra_pages では第{xn}回になっている"
        p = XSTART[n] + k
    else:
        p = PMAP[n].get(p, p)
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

# ---- data.json（並び順はサイトが前提にしている元の順のまま）----
out = (base["D"] + base["L"] + base["G"] + base["C"] + base["B"] + base["CP"]
       + [TB[n] for n in sorted(TB)]
       + [{"r": "O", "ids": ids}, {"r": "QP", "m": qp}]
       + base["RG"] + newQ)
with open(srcio.DATA, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
print(f"data.json を作りました（教科書・授業 {len(TB)} 回、問題 {len(newQ)} 問）", flush=True)

sys.exit(subprocess.call([sys.executable, "-X", "utf8", os.path.join(srcio.ROOT, "tools", "check.py")]))
