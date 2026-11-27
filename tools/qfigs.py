"""問題の構成図（topology）。build.py が読み込んで、問題の fig（SVG）にする。
FIG = {問題ID: SVG}。図の中の機器名・ポート・アドレスは、問題文と合わせる。
答えそのもの（例：ネイティブVLANの番号、OSPFの役割）は図に書かない。
描き方は tools/figs.py の topo()。links は (a, b, 線の上の文字, 色, a側のポート, b側のポート)。
"""
from figs import topo, BL, GR, GY, PU, YE, RD, CY

COL = {"router": BL, "switch": GR, "pc": GY, "phone": GY, "server": PU, "cloud": GY, "ap": CY, "fw": RD}


def N(kind, x, y, top="", bottom="", col=None):
    return (kind, x, y, col or COL[kind], top, bottom)


def L(a, b, txt="", pa="", pb="", col=None):
    return (a, b, txt, col, pa, pb)


def F(nodes, links, h=150, notes=()):
    return topo("構成図", nodes, links, height=h, notes=notes)


def pair(a, b, pa, pb, txt="", ba="", bb="", kind="switch", notes=()):
    """2台を横につないだ図"""
    return F({"a": N(kind, 80, 60, a, ba), "b": N(kind, 280, 60, b, bb)}, [L("a", "b", txt, pa, pb)], 130, notes)


def ros(vlans, txt=""):
    """ルーターオンアスティック：R1 G0/0 — SW1 と、VLANごとのPC"""
    n = {"r": N("router", 180, 45, "R1"), "s": N("switch", 180, 160, "SW1")}
    ls = [L("r", "s", txt, "G0/0", "G0/24")]
    xs = {1: [180], 2: [90, 270], 3: [60, 180, 300]}[len(vlans)]
    for i, (v, x) in enumerate(zip(vlans, xs)):
        n[f"p{i}"] = N("pc", x, 235, "", f"VLAN {v}")
        ls.append(L("s", f"p{i}"))
    return F(n, ls, 290)


def hub(center, nbrs, h=240, notes=()):
    """1台のルーターと、まわりのネクストホップ。nbrs = [(ポート, 相手の文字, 下の文字), ...]"""
    pos = [(55, 55), (305, 55), (180, 185), (55, 170)]
    n = {"c": N("router", 180, 95, center)}
    ls = []
    for i, (port, top, bot) in enumerate(nbrs):
        x, y = pos[i]
        n[f"n{i}"] = N("router", x, y, top, bot, GY)
        ls.append(L("c", f"n{i}", "", port))
    return F(n, ls, h, notes)


def lan_summary(r, nets):
    return F({"l": N("cloud", 70, 60, f"{r} のLAN", nets), "r": N("router", 200, 60, r), "n": N("router", 310, 60, "隣のルーター", "", GY)},
             [L("l", "r"), L("r", "n")], 60 + 14 * len(nets) + 40)


FIG = {
 # ---- スイッチ ----
 "P08-01": F({"s": N("switch", 180, 45, "SW1"), "a": N("pc", 70, 140, "PC-A"), "b": N("pc", 290, 140, "PC-B")},
             [L("s", "a"), L("s", "b", "", "ポート5")], 190, ["PC-A から PC-B あてのフレーム"]),
 "P10-11": F(dict({"s": N("switch", 180, 45, "SW1")},
                  **{f"p{i}": N("pc", x, 150, port, f"VLAN {v}") for i, (x, port, v) in
                     enumerate([(40, "Gi0/1", 10), (110, "Gi0/2", 10), (180, "Gi0/3", 10), (250, "Gi0/4", 20), (320, "Gi0/5", 20)])}),
             [L("s", f"p{i}") for i in range(5)], 220, ["Gi0/1 のPCからフレームが届く"]),
 "P11-03": pair("R1", "R2", "S0/1/0", "S0/1/0", "シリアル回線", kind="router"),
 "P11-07": F({"v": N("server", 55, 70, "サーバー群"), "s": N("switch", 180, 70, "SW3"), "u": N("switch", 305, 70, "上位スイッチ", "", GY)},
             [L("v", "s"), L("s", "u", "1Gbps", "Gi0/24")], 140, ["サーバー群の通信を Gi0/24 から上位へ送る"]),
 "P11-11": F({"s": N("switch", 80, 60, "SW1", "speed 100・duplex full"), "p": N("pc", 280, 60, "PC", "auto（自動）")},
             [L("s", "p", "", "Gi0/1")], 130),
 "P20-05": pair("SW1", "SW2", "Gi0/1", "Gi0/1", "", "dynamic desirable", "dynamic auto"),
 "P20-14": pair("SW1", "SW2", "Gi0/1", "Gi0/1", "", "dynamic auto", "dynamic auto"),
 "P20-06": F(dict({"a": N("switch", 100, 50, "SW1"), "b": N("switch", 260, 50, "SW2")},
                  **{f"p{i}": N("pc", x, 140, "", f"VLAN {v}") for i, (x, v) in enumerate([(35, 10), (95, 20), (155, 30), (205, 10), (265, 20), (325, 30)])}),
             [L("a", "b", "トランク", "Gi0/1", "Gi0/1")] + [L("a" if i < 3 else "b", f"p{i}") for i in range(6)], 210,
             ["VLAN 30 のPCどうしだけ通信できない"]),
 "P20-08": pair("SW1", "SW2", "Gi0/1", "Gi0/1", "トランク"),
 "P20-09": pair("SW3", "SW4", "Gi0/24", "", "up / up"),
 "P21-01": ros([30, 40]),
 "P21-06": ros([10, 20], "トランク"),
 "P21-07": ros([10, 20, 30], "トランク"),
 "P24-10": F({"a": N("switch", 80, 50, "DS1"), "b": N("switch", 280, 50, "DS2"), "c": N("switch", 180, 150, "アクセス", "", GY)},
             [L("a", "b"), L("a", "c"), L("b", "c")], 195, ["VLAN 10 のルート：DS1", "VLAN 20 のルート：DS2"]),
 "P25-03": pair("SW1", "SW2", "Gi1/0/1-2", "Gi1/0/1-2", "2本を束ねる", "mode passive", ""),
 "P44-11": F({"d": N("switch", 180, 40, "ディストリビューション", "", GY), "s": N("switch", 180, 155, "SW4"),
              "a": N("pc", 80, 235, "", "VLAN 30"), "b": N("pc", 280, 235, "", "VLAN 30")},
             [L("d", "s", "トランク"), L("s", "a"), L("s", "b")], 285),
 # ---- STP ----
 "P23-03": F({"r": N("switch", 180, 45, "ルートブリッジ", "", YE), "a": N("switch", 70, 115, "SW1"), "b": N("switch", 290, 115, "SW2"), "c": N("switch", 180, 195, "SW3")},
             [L("r", "a"), L("r", "b"), L("c", "a", "Gi0/1"), L("c", "b", "Gi0/2")], 245,
             ["SW1：32768.0011.1111.aaaa", "SW2：32768.0011.1111.0bbb", "SW3 からの合計コストはどちらも同じ"]),
 "P23-04": F({"r": N("switch", 180, 45, "ルートブリッジ", "", YE), "a": N("switch", 70, 125, "SW2"), "c": N("switch", 280, 190, "SW4")},
             [L("r", "a", "1Gbps"), L("c", "a", "1Gbps", "Gi0/1"), L("c", "r", "100Mbps", "Fa0/2")], 240),
 # ---- パケットの旅・ルーティング ----
 "P29-06": F({"p": N("pc", 35, 60, "PC-A"), "a": N("router", 135, 60, "R1"), "b": N("router", 235, 60, "R2"), "s": N("server", 330, 60, "サーバー")},
             [L("p", "a"), L("a", "b"), L("b", "s")], 120, ["NATなし"]),
 "P30-08": F({"a": N("router", 50, 100, "R1"), "b": N("router", 180, 40, "R2"), "c": N("router", 180, 160, "R3"), "d": N("cloud", 310, 100, "10.88.0.0/16")},
             [L("a", "b"), L("a", "c"), L("b", "d"), L("c", "d")], 205, ["R2 経由：合計コスト 20", "R3 経由：合計コスト 35"]),
 "P30-14": hub("R2", [("Gi0/0", "172.31.0.1", ""), ("Gi0/1", "172.31.0.5", ""), ("Gi0/2", "172.31.0.9", "")]),
 "P30-15": hub("R3", [("Gi0/0", "10.1.1.2", "OSPF"), ("Gi0/1", "10.1.2.2", "RIP"), ("Gi0/2", "10.1.3.2", "EIGRP")]),
 "P30-16": hub("R4", [("Gi0/1", "10.0.14.2", ""), ("Gi0/2", "10.0.15.2", ""), ("Gi0/3", "10.0.16.2", "")]),
 "P30-28": F({"a": N("router", 40, 135, "R1"), "b": N("router", 160, 45, "R2"), "c": N("router", 160, 105, "R3"), "d": N("router", 160, 165, "R4"),
              "e": N("router", 120, 230, "R5"), "f": N("router", 230, 230, "R6"), "z": N("cloud", 320, 135, "10.90.0.0/16")},
             [L("a", "b"), L("a", "c"), L("a", "d"), L("a", "e"), L("e", "f"), L("b", "z"), L("c", "z"), L("d", "z"), L("f", "z")], 265),
 "P31-04": F({"a": N("router", 55, 70, "10.0.0.2", "", GY), "r": N("router", 180, 70, "R1"), "b": N("router", 305, 70, "10.0.0.14", "", GY)},
             [L("r", "a", "10.0.0.0/30", "Gi0/0"), L("r", "b", "10.0.0.12/30", "Gi0/2")], 140),
 "P31-07": F({"r": N("router", 50, 100, "R1"), "e": N("router", 180, 40, "10.9.9.6", "", GY), "t": N("router", 180, 160, "R3", "10.9.9.10"), "d": N("cloud", 310, 100, "172.20.8.0/24")},
             [L("r", "e", "EIGRP", "Gi0/0"), L("r", "t", "", "Gi0/1 .9"), L("e", "d"), L("t", "d")], 215),
 "P31-23": F({"p": N("pc", 30, 60, "PC1"), "a": N("router", 130, 60, "R1"), "b": N("router", 240, 60, "R2"), "q": N("pc", 335, 60, "PC2")},
             [L("p", "a"), L("a", "b", "10.31.0.0/30", ".1", ".2"), L("b", "q")], 135,
             ["PC1 側：192.168.31.0/24", "PC2 側：172.18.5.0/24"]),
 "P13-01": lan_summary("R2", ["172.16.8.0/24", "172.16.9.0/24", "172.16.10.0/24", "172.16.11.0/24"]),
 "P13-07": lan_summary("R1", ["10.8.6.0/24", "10.8.7.0/24", "10.8.8.0/24", "10.8.9.0/24"]),
 # ---- OSPF ----
 "P32-08": F(dict({"s": N("switch", 180, 45, "1つのイーサネット", "", GY)},
                  **{k: N("router", x, 145, k) for k, x in (("R-A", 45), ("R-B", 135), ("R-C", 225), ("R-D", 315))}),
             [L("s", k) for k in ("R-A", "R-B", "R-C", "R-D")], 190),
 "P32-21": F(dict({"s": N("switch", 180, 45, "1つのイーサネット", "", GY)},
                  **{k: N("router", x, 145, k, b, c) for k, x, b, c in (("R1", 45, "DR", None), ("R2", 135, "", None), ("R3", 225, "", None), ("R4", 315, "追加・優先度255", YE))}),
             [L("s", k) for k in ("R1", "R2", "R3", "R4")], 195),
 "P33-07": F({"r": N("router", 180, 80, "R1"), "s": N("switch", 60, 80, "", "", GY), "p": N("pc", 60, 165, "PC"),
              "a": N("router", 300, 45, "R2", "", GY), "b": N("router", 300, 145, "R3", "", GY)},
             [L("r", "s", "", "G0/2"), L("s", "p"), L("r", "a", "OSPF"), L("r", "b", "OSPF")], 210),
 "P32-07": pair("R1", "R2", "Gi0/0", "Gi0/0", "10.4.4.0/29", kind="router"),
 "P32-22": pair("R1", "R2", "Gi0/1 .1", "Gi0/1 .2", "10.8.8.0/30", kind="router"),
 # ---- サービス ----
 "P36-22": pair("R1", "R2", "", "", "", "NTPサーバー 10.0.0.1", "時刻をもらう", kind="router"),
 "P36-29": F({"a": N("router", 60, 60, "R1", "ntp master 4"), "b": N("router", 180, 60, "R2", "ntp server R1"), "c": N("router", 300, 60, "R3", "ntp server R2")},
             [L("a", "b"), L("b", "c")], 130),
 "P35-06": F({"a": N("pc", 45, 40, "", "192.168.5.21"), "b": N("pc", 45, 120, "", "192.168.5.22"), "v": N("server", 45, 200, "", "192.168.5.200"),
              "r": N("router", 185, 120, "R1"), "i": N("cloud", 315, 120, "インターネット")},
             [L("a", "r"), L("b", "r", "inside"), L("v", "r"), L("r", "i", "outside")], 250),
 # ---- セキュリティ ----
 "P43-05": F({"p": N("pc", 45, 70, "PC", "10.20.3.4"), "r": N("router", 180, 70, "R1", "WEB-ONLY（in）"), "w": N("server", 315, 70, "Webサーバー", "192.0.2.80")},
             [L("p", "r", "", "", "G0/0"), L("r", "w")], 140),
}
