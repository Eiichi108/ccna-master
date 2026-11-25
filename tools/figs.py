"""教科書の図（SVG）を作る部品。作り直し版（src/lessons_v2）で使う。
どの図も横幅360の viewBox で、色はサイトのテーマ変数（--ink・--sub・--card）を使うので、明るい表示でも暗い表示でも読める。
文字が図からはみ出しそうなときは AssertionError で止まる（長い文は分けて渡す）。
"""
F = "Figtree,'Hiragino Sans',sans-serif"
M = "ui-monospace,Menlo,monospace"
ST = "paint-order:stroke;stroke:var(--card);stroke-width:4px;stroke-linejoin:round"
BL, GR, YE, RD, GY, PU, CY = "#0a5cff", "#00a05a", "#ffb400", "#e6261f", "#3d4450", "#8a3ffc", "#00a3b4"
INK, SUB, CARD = "var(--ink)", "var(--sub)", "var(--card)"
TERM_FG = "#e8ecf3"


def _w(s, size, mono=False):
    return sum((0.6 if mono else 0.58) * size if ord(c) < 128 else size for c in s)


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


import os
WARN = bool(os.environ.get("FIGS_WARN"))  # 1 にすると、止めずに長すぎる文を全部表示する


def T(x, y, s, size=13, weight=700, fill=INK, anchor="start", mono=False, halo=True):
    lim = 340 if anchor == "middle" else (350 if mono else 340) - x
    if anchor == "middle":  # 図の端からはみ出さないように内側へずらす
        half = _w(s, size, mono) / 2
        x = round(min(max(x, 6 + half), 354 - half), 1)
    if _w(s, size, mono) > lim:
        msg = f"図の文字が長すぎます（{_w(s, size, mono):.0f}>{lim}）：{s}"
        if WARN: print(msg)
        else: raise AssertionError(msg)
    if mono:
        return f'<text x="{x}" y="{y}" text-anchor="{anchor}" xml:space="preserve" style="font:700 {size}px {M};fill:{fill};white-space:pre">{_esc(s)}</text>'
    st = ";" + ST if halo else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="font:{weight} {size}px {F};fill:{fill}{st}">{_esc(s)}</text>'


def _fit(s, size, smallest, room=316):
    """囲みの中の文字が入りきらないときだけ、smallest まで少しずつ小さくする。"""
    while _w(s, size) > room and size > smallest:
        size = round(size - 0.5, 1)
    return size


def svg(h, label, body):
    return f'<svg class="tbfig" viewBox="0 0 360 {h:.1f}" role="img" aria-label="{_esc(label)}">{body}</svg>'


def boxes(label, items):
    """色つきの囲みを縦に並べる。items = [(見出し, [小さい文, ...], 色), ...]"""
    y, out = 6.0, []
    for title, subs, col in items:
        h = 40.5 + 17 * len(subs)
        out.append(f'<rect x="10" y="{y}" width="340" height="{h}" rx="12" fill="{col}" opacity=".1"/>')
        out.append(T(24, y + 25.5, title, _fit(title, 14.5, 12), 800))
        for i, s in enumerate(subs):
            out.append(T(24, y + 44.5 + 17 * i, s, _fit(s, 12.5, 11), 600, SUB))
        y += h + 6
    return svg(y + 4, label, "".join(out))


def card(label, emoji_line, lines, col=BL):
    """つかみ用の大きなカード。emoji_line は大きく出す1行、lines は下に続く文。"""
    h = 70 + 20 * len(lines)
    size = 20
    while _w(emoji_line, size) > 330 and size > 13: size -= 0.5
    out = [f'<rect x="10" y="6" width="340" height="{h}" rx="16" fill="{col}" opacity=".12"/>',
           T(180, 44, emoji_line, size, 800, INK, "middle")]
    for i, s in enumerate(lines):
        out.append(T(180, 74 + 20 * i, s, 13.5, 600, SUB, "middle"))
    return svg(h + 14, label, "".join(out))


def goals(label, items):
    """今日のゴール（番号つき）。"""
    return boxes(label, [(f"{i + 1}. {t}", subs, c) for i, (t, subs, c) in enumerate(items)])


def term(label, lines, caps=()):
    """端末の画面。lines = [(文字列, 色), ...]。英数字だけにする（等幅でそろえるため）。"""
    n = len(lines)
    h = 22 * n + 34
    out = [f'<rect x="10" y="10" width="340" height="{h}" rx="10" fill="#1d2330"/>',
           '<circle cx="24" cy="23" r="4" fill="#ff5f57"/><circle cx="38" cy="23" r="4" fill="#febc2e"/><circle cx="52" cy="23" r="4" fill="#28c840"/>']
    for i, (s, col) in enumerate(lines):
        assert all(ord(c) < 128 for c in s), f"端末の中は英数字だけにしてください：{s}"
        out.append(T(22, 52 + 22 * i, s, 10.5, 700, col, mono=True))
    y = 10 + h
    for i, s in enumerate(caps):
        y += 24 if i else 22
        out.append(T(180, y, s, 13 if i == 0 else 11.5, 800 if i == 0 else 700, INK if i == 0 else SUB, "middle"))
    return svg(y + (28 if caps else 10), label, "".join(out))


# ---- 構成図 ----
def _icon(kind, x, y, col):
    if kind == "router":
        return (f'<circle cx="{x}" cy="{y}" r="18" fill="{col}"/>'
                f'<path d="M{x-9} {y-4}h12l-4-4M{x+9} {y+4}h-12l4 4" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "switch":
        return (f'<rect x="{x-22}" y="{y-13}" width="44" height="26" rx="5" fill="{col}"/>'
                f'<path d="M{x-12} {y-4}h22l-4-3M{x+12} {y+4}h-22l4 3" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    if kind == "pc":
        return (f'<rect x="{x-16}" y="{y-14}" width="32" height="21" rx="3" fill="none" stroke="{col}" stroke-width="3"/>'
                f'<path d="M{x-9} {y+14}h18M{x} {y+7}v7" stroke="{col}" stroke-width="3" stroke-linecap="round"/>')
    if kind == "phone":
        return (f'<rect x="{x-10}" y="{y-17}" width="20" height="34" rx="4" fill="none" stroke="{col}" stroke-width="3"/>'
                f'<circle cx="{x}" cy="{y+11}" r="2" fill="{col}"/>')
    if kind == "server":
        return (f'<rect x="{x-13}" y="{y-18}" width="26" height="36" rx="3" fill="{col}"/>'
                f'<path d="M{x-7} {y-9}h14M{x-7} {y-1}h14M{x-7} {y+7}h14" stroke="#fff" stroke-width="2"/>')
    if kind == "cloud":
        return (f'<path d="M{x-26} {y+10}a12 12 0 0 1 4-22a16 16 0 0 1 30-4a12 12 0 0 1 18 14a10 10 0 0 1-4 12z" fill="{col}" opacity=".85"/>')
    if kind == "ap":
        return (f'<circle cx="{x}" cy="{y+6}" r="5" fill="{col}"/>'
                f'<path d="M{x-10} {y-2}a14 14 0 0 1 20 0M{x-16} {y-8}a22 22 0 0 1 32 0" stroke="{col}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    if kind == "fw":
        return (f'<rect x="{x-18}" y="{y-15}" width="36" height="30" rx="4" fill="{col}"/>'
                f'<path d="M{x-18} {y-5}h36M{x-18} {y+5}h36M{x-6} {y-15}v10M{x+6} {y-5}v10M{x-6} {y+5}v10" stroke="#fff" stroke-width="1.8"/>')
    raise ValueError(kind)


def topo(label, nodes, links, height=170, notes=()):
    """構成図。nodes = {名前: (種類, x, y, 色, 上の文字, 下の文字)}、links = [(a, b, 線の上の文字, 色)]。
    種類：router・switch・pc・phone・server・cloud・ap・fw。notes は図の下に出す文。"""
    out = []
    for a, b, txt, col in links:
        _, x1, y1, *_ = nodes[a]
        _, x2, y2, *_ = nodes[b]
        out.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{col or GY}" stroke-width="3" opacity=".7"/>')
        if txt:
            out.append(T((x1 + x2) / 2, (y1 + y2) / 2 - 7, txt, 10.5, 700, SUB, "middle"))
    for name, (kind, x, y, col, top, bottom) in nodes.items():
        out.append(_icon(kind, x, y, col))
        if top:
            out.append(T(x, y - 26, top, 12, 800, INK, "middle"))
        if bottom:
            for i, s in enumerate(bottom if isinstance(bottom, (list, tuple)) else [bottom]):
                out.append(T(x, y + 34 + 14 * i, s, 10.5, 700, SUB, "middle"))
    y = height
    for i, s in enumerate(notes):
        out.append(T(180, y + 20 * i, s, 13 if i == 0 else 12, 800 if i == 0 else 600, INK if i == 0 else SUB, "middle"))
    return svg(height + 20 * len(notes) + (8 if notes else 0), label, "".join(out))


def band(label, title, total, segs, ticks, rows=(), foot=None):
    """アドレスの帯。segs = [(始まり, 長さ, 中の文字, 色, 濃い=True)]、ticks = 目盛りに出す数、rows = 下の説明 [(文, 色)]。"""
    k = 340 / total
    out = [T(180, 22, title, 13.5, 800, INK, "middle")]
    for s, n, txt, col, strong in segs:
        x = 10 + s * k
        out.append(f'<rect x="{x:.1f}" y="34" width="{n * k:.1f}" height="30" fill="{col}" opacity="{".85" if strong else ".15"}" stroke="var(--card)" stroke-width="1"/>')
        if txt:
            out.append(f'<text x="{x + n * k / 2:.1f}" y="54" text-anchor="middle" style="font:800 12px {F};fill:{"#fff" if strong and col not in (YE,) else INK}">{_esc(txt)}</text>')
    for t in ticks:
        out.append(f'<text x="{10 + t * k:.1f}" y="78" text-anchor="{"start" if t == 0 else "end" if t == total else "middle"}" style="font:700 10.5px {M};fill:var(--sub)">{t}</text>')
    y = 100
    for txt, col in rows:
        out.append(f'<rect x="10" y="{y - 13}" width="5" height="17" rx="2" fill="{col}"/>')
        out.append(T(22, y, txt, 12.5, 700))
        y += 22
    if foot:
        out.append(T(180, y + 6, foot, 12.5, 700, SUB, "middle"))
        y += 20
    return svg(y + 4, label, "".join(out))


def bits(label, title, rows, foot=None, weights=(128, 64, 32, 16, 8, 4, 2, 1)):
    """8けたの2進数の表。rows = [(左の見出し, "01000000" のようなビット列, 下に出す説明 or None)]。
    ビット列に "-" を入れたマスは薄く表示する（使わないけた）。"""
    out = [T(180, 22, title, 13.5, 800, INK, "middle")]
    x0, cw = 72, 34
    for i, w in enumerate(weights):
        out.append(T(x0 + cw * i + cw / 2, 46, str(w), 11, 700, SUB, "middle"))
    y = 56
    for name, b, right in rows:
        out.append(T(8, y + 21, name, 10.5, 800))
        for i, c in enumerate(b):
            on = c == "1"
            out.append(f'<rect x="{x0 + cw * i + 2}" y="{y}" width="{cw - 4}" height="30" rx="5" fill="{BL if on else "none"}" stroke="{BL}" stroke-width="1.5" opacity="{1 if on else .5}"/>')
            out.append(f'<text x="{x0 + cw * i + cw / 2}" y="{y + 21}" text-anchor="middle" style="font:800 15px {F};fill:{"#fff" if on else "var(--sub)"}">{c}</text>')
        y += 38
        if right:
            out.append(T(x0, y + 8, right, 12, 700, GR))
            y += 22
    if foot:
        out.append(T(180, y + 14, foot, 12.5, 700, SUB, "middle")); y += 24
    return svg(y + 6, label, "".join(out))


def qopt(letter, col):
    """教科書の小テストの選択肢に付ける小さな印（A・B・C）。"""
    return (f'<g><rect x="-20" y="-20" width="40" height="40" rx="10" fill="var(--card)" stroke="{col}" stroke-width="3"/>'
            f'<text y="7" text-anchor="middle" style="font:800 20px {F};fill:{col}">{letter}</text></g>')


def quiz(q, opts, a, e):
    """教科書の確認の問題。opts は文字列のリスト（3つ程度）、a は正解の番号。"""
    cols = [BL, GR, YE, PU]
    return {"q": q, "o": [[o, qopt("ABCD"[i], cols[i])] for i, o in enumerate(opts)], "a": a, "e": e}
