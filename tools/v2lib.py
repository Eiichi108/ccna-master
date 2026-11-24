"""作り直し版（src/lessons_v2）の回を書き出すための共通の部品。
台本は (場面番号, "T"=先生/"S"=生徒, セリフ, [1=確認の問題で止まる]) のリストで書き、save() で保存する。
save() は、場面番号とページ数・確認の問題のページと止まる行が合っているかを点検してから保存する。
読み上げ用の読み（y）は tools/rd.py の auto() で自動で付ける。
使い方：python から  sys.path.insert(0, "tools"); from v2lib import *
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import srcio, rd
from figs import *

def lines(spec):
    out = []
    for sc, who, t, *w in spec:
        o = {"sc": sc, "sp": "先生" if who == "T" else "生徒", "t": t}
        y = rd.auto(t)
        if y != t: o["y"] = y
        if w: o["w"] = 1
        out.append(o)
    return out

def save(n, title, d, form, need, goal, terms, pages, spec):
    L = {"r": "TB", "n": n, "t": title, "d": d, "form": form, "need": need, "goal": goal, "terms": terms,
         "pages": pages, "cls": {"lines": lines(spec)}}
    # 授業の場面番号がページの数をこえていないか、確認の問題のページと w の数が合うか
    assert max(l["sc"] for l in L["cls"]["lines"]) == len(pages), (n, "sc とページ数が合わない")
    qp = {i + 1 for i, p in enumerate(pages) if "quiz" in p}
    wp = {l["sc"] for l in L["cls"]["lines"] if l.get("w")}
    assert qp == wp, (n, "確認の問題のページと w の行が合わない", qp, wp)
    os.makedirs(os.path.join(srcio.SRC, "lessons_v2"), exist_ok=True)
    srcio.save(os.path.join(srcio.SRC, "lessons_v2", f"l{n:02d}.json"), L)
    st = [l for l in L["cls"]["lines"] if l["sp"] == "生徒"]
    print(f"第{n}回 {title}: {len(pages)}ページ・{len(L['cls']['lines'])}行・生徒{len(st) / len(L['cls']['lines']) * 100:.0f}%")
