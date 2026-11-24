"""作り直し版の回（src/lessons_v2/lNN.json）を、読んで確かめるためのHTMLにする。
  python tools/preview_v2.py 1 19 50   → preview/v2_l01.html などを作る（preview/ は git に入れない）
ページごとに、左に教科書、右にそのページで話す授業のセリフを並べる。最後に台本の数字（行の長さ・生徒の割合など）を出す。
"""
import html, json, os, sys
import srcio

sys.stdout.reconfigure(encoding="utf-8")
OUT = os.path.join(srcio.ROOT, "preview")
CSS = """
:root{--ink:#14181f;--sub:#5b6472;--card:#fff;--bg:#f3f5f8;--line:#d9dee6}
@media (prefers-color-scheme:dark){:root{--ink:#e8ecf3;--sub:#9aa4b2;--card:#171b22;--bg:#0e1116;--line:#2a313c}}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.7 'Hiragino Sans','Noto Sans JP',sans-serif}
main{max-width:1180px;margin:0 auto;padding:16px}
h1{font-size:22px;margin:8px 0}.meta{color:var(--sub);font-size:14px}
.pg{display:grid;grid-template-columns:minmax(0,420px) minmax(0,1fr);gap:16px;margin:18px 0;padding-top:14px;border-top:1px solid var(--line)}
@media (max-width:820px){.pg{grid-template-columns:1fr}}
.tb{background:var(--card);border-radius:14px;padding:14px}.tb h3{margin:0 0 8px;font-size:17px}
.tb svg{width:100%;height:auto;display:block}.b{margin:10px 0 0}.p{margin:8px 0 0;padding:8px 10px;border-radius:8px;background:rgba(10,92,255,.1);font-weight:700}
.qz{margin-top:8px}.qz li{margin:2px 0}.ok{color:#00a05a;font-weight:800}
.ln{display:grid;grid-template-columns:3.2em 1fr;gap:8px;margin:0 0 8px}.who{font-weight:800;font-size:13px;padding-top:2px}
.t .who{color:#0a5cff}.s .who{color:#e6261f}.w{background:rgba(255,180,0,.15);border-radius:8px;padding:2px 6px}
.long{text-decoration:underline wavy #e6261f}.stats{background:var(--card);border-radius:14px;padding:12px 16px;margin-top:20px}
"""


def page_html(i, P):
    h = f'<div class="tb"><div class="meta">{i + 1}ページ目</div><h3>{html.escape(P["t"])}</h3>'
    if P.get("quiz"):
        Z = P["quiz"]
        h += f'<b>{Z["q"]}</b><ol class="qz" type="A">' + "".join(
            f'<li class="{"ok" if k == Z["a"] else ""}">{html.escape(o[0])}</li>' for k, o in enumerate(Z["o"])) + f'</ol><div class="b">{Z["e"]}</div>'
    else:
        h += P.get("svg", "") + (f'<div class="b">{P["b"]}</div>' if P.get("b") else "") + (f'<div class="p">{P["p"]}</div>' if P.get("p") else "")
    return h + "</div>"


def build(n):
    L = srcio.load(os.path.join(srcio.SRC, "lessons_v2", f"l{n:02d}.json"))
    lines = L["cls"]["lines"]
    out = [f'<main><h1>第{n}回 {html.escape(L["t"])}</h1>',
           f'<div class="meta">形：{L.get("form", "")}　前提：{"・".join("第%d回" % x for x in L.get("need", [])) or "なし"}<br>',
           f'今日のゴール：{" ／ ".join(L.get("goal", []))}<br>新しい用語：{"・".join(L.get("terms", []))}</div>']
    for i, P in enumerate(L["pages"]):
        ls = [l for l in lines if l["sc"] == i + 1]
        sc = "".join(
            f'<div class="ln {"t" if l["sp"] == "先生" else "s"}"><span class="who">{l["sp"]}</span>'
            f'<span class="{"w" if l.get("w") else ""} {"long" if len(l["t"]) > 60 else ""}">{html.escape(l["t"])}</span></div>' for l in ls)
        out.append(f'<section class="pg">{page_html(i, P)}<div>{sc}</div></section>')
    t = [l for l in lines if l["sp"] == "先生"]
    s = [l for l in lines if l["sp"] == "生徒"]
    chars = sum(len(l["t"]) for l in lines)
    out.append(f'<div class="stats"><b>台本の数字</b>　全{len(lines)}行（先生{len(t)}・生徒{len(s)}、生徒の割合 {len(s) / len(lines) * 100:.0f}%）'
               f'／先生の1行の平均 {sum(len(l["t"]) for l in t) / max(1, len(t)):.0f}字・60字超え {sum(len(l["t"]) > 60 for l in t)}行'
               f'／確認の問題 {sum(1 for l in lines if l.get("w"))}回／教科書 {len(L["pages"])}ページ'
               f'／読み上げの長さの目安 約{chars / 330:.0f}分</div></main>')
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"v2_l{n:02d}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<title>第{n}回 試作</title><style>{CSS}</style></head><body>{"".join(out)}</body></html>')
    print(path)


if __name__ == "__main__":
    for a in sys.argv[1:]:
        build(int(a))
