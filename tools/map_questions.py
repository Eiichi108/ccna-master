"""【使用済み・2026-11-27 に切り替え】問題（旧50回の src/questions/lNN.json）を、作り直し版の81回（src/lessons_v2）に振り分ける。
1. 旧の回ごとに、入りうる新しい回（候補）を決めておく（CAND）。
2. 候補の中から、問題文・選択肢・解説に出てくる言葉の数で一番合う回を選ぶ（KW と新しい回の terms）。
3. 手で決めた問題は FIX で上書きする。
4. 新しい回の中で、言葉が一番重なる教科書のページ（確認の問題以外）を page にする。
結果は src/questions_v2/map.json（ID → [新しい回, ページ]）と、src/questions_v2/lNN.json（新しい番号の問題ファイル）に書き出す。
問題の ID は変えない（進捗は ID で保存されているため）。
使い方：python tools/map_questions.py [--report]   （--report で、決め手の弱い問題の一覧を出す）
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import srcio

CAND = {1: [1, 2, 4, 30], 2: [3, 17, 12, 14], 3: [4, 9, 30], 4: [5, 6], 5: [2, 7, 10], 6: [8], 7: [9, 4, 76, 81],
        8: [7, 10], 9: [11, 12], 10: [13, 14, 32], 11: [15, 16], 12: [17, 18, 19, 20, 27, 60], 13: [21, 22],
        14: [23, 24], 15: [25, 31], 16: [26], 17: [27], 18: [28, 29], 19: [29, 30, 31], 20: [32, 33, 34], 21: [35],
        22: [36], 23: [37, 38], 24: [39, 40], 25: [41], 26: [42], 27: [43, 44, 29], 28: [45, 46], 29: [47],
        30: [48, 49, 53], 31: [50, 51, 52], 32: [53, 54], 33: [55, 56], 34: [57], 35: [58, 59], 36: [60, 61, 62],
        37: [63], 38: [65, 64], 39: [65, 66], 40: [67, 68], 41: [69, 64], 42: [69, 70, 71], 43: [72, 73], 44: [74],
        45: [71, 75, 46], 46: [76, 31], 47: [77, 76], 48: [78, 79], 49: [78], 50: [80, 81]}

# 新しい回の terms に足す言葉（問題によく出る言い方）
KW = {
 1: ["LAN", "WAN", "インターネット", "サーバー", "クライアント", "ピアツーピア"],
 2: ["カプセル化", "ヘッダー", "パケット", "プロトコル"],
 3: ["MACアドレス", "IPアドレス", "48ビット", "OUI"],
 4: ["スイッチ", "ルーター", "アクセスポイント", "ファイアウォール", "ハブ"],
 7: ["OSI", "物理層", "データリンク層", "ネットワーク層", "レイヤー"],
 9: ["次世代", "NGFW", "IPS", "PoE", "WLC", "エンドポイント"],
 10: ["TCP/IP", "トランスポート層", "アプリケーション層", "セグメント", "フレーム", "PDU"],
 11: ["TCP", "UDP", "ハンドシェイク", "SYN", "ACK", "ウィンドウ", "再送", "コネクション"],
 12: ["ポート番号", "ウェルノウン", "22", "23", "53", "80", "443", "69", "161"],
 13: ["ケーブル", "UTP", "光ファイバー", "シングルモード", "マルチモード", "ストレート", "クロス", "SFP", "100m"],
 14: ["MACアドレステーブル", "フラッディング", "学習", "エージング", "ブロードキャスト"],
 15: ["show interfaces", "up/down", "全二重", "半二重", "duplex", "speed", "オートネゴシエーション", "administratively"],
 16: ["CRC", "コリジョン", "レイトコリジョン", "runts", "giants", "drops", "エラー"],
 17: ["プライベート", "APIPA", "169.254", "クラス", "デフォルトゲートウェイ", "ネットワーク部", "ホスト部"],
 18: ["サブネットマスク", "プレフィックス", "ブロードキャストアドレス", "ネットワークアドレス"],
 19: ["ブロックサイズ", "所属", "有効なホスト", "第4オクテット"],
 20: ["ホスト数", "2のn乗", "サブネット数", "/2", "/1"],
 21: ["VLSM", "割り当て"],
 22: ["集約", "サマリー"],
 23: ["IPv6", "省略", "::", "16進数"],
 24: ["グローバルユニキャスト", "リンクローカル", "fe80", "ユニークローカル", "fc00", "fd", "マルチキャスト", "ff02", "エニーキャスト", "2000::/3"],
 25: ["EUI-64", "ipv6 address", "ipv6 enable", "unicast-routing", "FFFE"],
 26: ["NDP", "SLAAC", "DAD", "RA", "RS", "NS", "NA", "DHCPv6", "ステートレス"],
 27: ["ipconfig", "ip addr", "ifconfig", "ping", "tracert", "traceroute", "nslookup", "arp -a"],
 28: ["2.4GHz", "5GHz", "6GHz", "チャネル", "802.11", "RSSI", "SNR", "干渉", "Wi-Fi 6"],
 29: ["SSID", "BSS", "BSSID", "ESS", "ローミング", "CSMA/CA", "アドホック", "IBSS"],
 30: ["3階層", "2階層", "コラプストコア", "スパイン", "リーフ", "SOHO", "トポロジー", "スター", "メッシュ", "コア", "ディストリビューション", "アクセス層", "WAN"],
 31: ["仮想マシン", "VM", "ハイパーバイザー", "コンテナ", "VRF", "クラウド", "IaaS", "PaaS", "SaaS", "仮想化"],
 32: ["VLAN", "アクセスポート", "switchport access", "show vlan"],
 33: ["トランク", "802.1Q", "タグ", "ネイティブVLAN"],
 34: ["DTP", "allowed vlan", "show interfaces trunk", "dynamic auto", "dynamic desirable", "nonegotiate"],
 35: ["VLAN間", "ルーターオンアスティック", "サブインターフェース", "encapsulation dot1q", "SVI", "interface vlan", "ip routing"],
 36: ["音声VLAN", "voice vlan", "管理", "ip default-gateway", "SSH", "Telnet", "vty"],
 37: ["ループ", "ブロードキャストストーム", "STP", "BPDU", "冗長"],
 38: ["ルートブリッジ", "ブリッジID", "ルートポート", "指定ポート", "非指定", "ブロッキング", "パスコスト", "プライオリティ"],
 39: ["RSTP", "Rapid PVST", "代替ポート", "バックアップポート", "802.1w", "ディスカーディング", "PVST"],
 40: ["PortFast", "BPDUガード", "BPDU Guard", "ルートガード", "err-disabled", "ループガード"],
 41: ["EtherChannel", "LACP", "PAgP", "Port-channel", "channel-group", "active", "passive", "desirable"],
 42: ["CDP", "LLDP"],
 43: ["自律型", "軽量", "WLC", "CAPWAP", "スプリットMAC", "クラウド", "Meraki", "5246", "5247"],
 44: ["Local", "FlexConnect", "Bridge", "Monitor", "Sniffer", "SE-Connect", "モード"],
 45: ["WLAN", "management", "dynamic", "サービスポート", "virtual", "インターフェース", "GUI", "Create New"],
 46: ["PSK", "802.1X", "RADIUS", "WPA3", "QoS", "Platinum", "Gold", "Silver", "Bronze", "LAG", "セキュリティ", "AAA"],
 47: ["ARP", "ネクストホップ", "TTL", "書き換", "書きかえ", "MAC"],
 48: ["show ip route", "ルーティングテーブル", "via", "directly connected", "コード"],
 49: ["ロンゲストマッチ", "プレフィックス長", "AD", "アドミニストレーティブ", "メトリック", "負荷分散", "最も長い"],
 50: ["ip route", "スタティック"],
 51: ["0.0.0.0", "デフォルトルート", "浮動", "フローティング", "ホストルート", "/32", "last resort"],
 52: ["ipv6 route", "::/0", "IPv6"],
 53: ["OSPF", "リンクステート", "LSA", "LSDB", "エリア", "ダイクストラ", "SPF", "ネイバー", "コスト", "Hello"],
 54: ["router ospf", "network", "router-id", "ルーターID", "passive-interface", "ip ospf", "show ip ospf", "reference-bandwidth", "ループバック"],
 55: ["DR", "BDR", "DROTHER", "priority", "プライオリティ", "ネットワークタイプ", "point-to-point", "broadcast"],
 56: ["INIT", "2WAY", "FULL", "EXSTART", "タイマー", "Dead", "MTU", "ネイバーにならない"],
 57: ["FHRP", "HSRP", "VRRP", "GLBP", "仮想IP", "仮想MAC", "preempt", "アクティブ", "スタンバイ"],
 58: ["NAT", "PAT", "inside local", "inside global", "outside", "オーバーロード", "変換"],
 59: ["ip nat", "overload", "pool", "translations", "static"],
 60: ["DHCP", "DORA", "Discover", "Offer", "リース", "helper-address", "リレー", "excluded"],
 61: ["DNS", "Aレコード", "AAAA", "CNAME", "MX", "名前解決", "name-server", "domain"],
 62: ["NTP", "stratum", "時刻", "ntp server", "ntp master", "clock"],
 63: ["SNMP", "MIB", "Trap", "Syslog", "重大度", "logging", "エージェント", "マネージャー", "debugging", "emergencies"],
 64: ["SSH", "RSA", "crypto key", "transport input", "TFTP", "FTP", "SCP", "copy", "flash", "IOS"],
 65: ["QoS", "遅延", "ジッター", "パケットロス", "マーキング", "分類", "DSCP", "EF", "CoS", "トラスト"],
 66: ["キュー", "FIFO", "CBWFQ", "LLQ", "シェーピング", "ポリシング", "WRED", "輻輳", "テールドロップ", "PHB", "AF"],
 67: ["機密性", "完全性", "可用性", "脆弱性", "エクスプロイト", "脅威", "対策", "CIA", "セキュリティプログラム", "教育"],
 68: ["フィッシング", "ソーシャルエンジニアリング", "DoS", "DDoS", "中間者", "マルウェア", "ウイルス", "ワーム", "トロイ", "ランサム", "スプーフィング", "偵察", "ブルートフォース", "辞書"],
 69: ["enable secret", "enable password", "password-encryption", "type 7", "type 5", "type 8", "type 9", "login local", "exec-timeout", "パスワード", "username"],
 70: ["AAA", "認証", "認可", "アカウンティング", "RADIUS", "TACACS", "MFA", "多要素", "証明書", "生体"],
 71: ["VPN", "IPsec", "GRE", "サイト間", "リモートアクセス", "AnyConnect", "トンネル", "ESP", "AH"],
 72: ["ACL", "標準", "暗黙", "ワイルドカード", "access-list", "access-group", "1-99"],
 73: ["拡張", "eq", "名前付き", "access-class", "tcp", "udp", "100-199", "ip access-list"],
 74: ["ポートセキュリティ", "port-security", "sticky", "violation", "shutdown", "restrict", "protect", "DHCPスヌーピング", "snooping", "DAI", "ARP inspection", "trusted"],
 75: ["WEP", "TKIP", "WPA", "WPA2", "WPA3", "AES", "CCMP", "SAE", "PMF", "サプリカント", "オーセンティケーター", "EAP", "無線"],
 76: ["データプレーン", "コントロールプレーン", "管理プレーン", "SDN", "コントローラー", "ノースバウンド", "サウスバウンド", "NETCONF", "RESTCONF", "OpenFlow", "DNA Center", "Catalyst Center"],
 77: ["アンダーレイ", "オーバーレイ", "ファブリック", "VXLAN", "LISP", "SD-Access", "TrustSec", "SGT"],
 78: ["API", "REST", "ステートレス", "CRUD", "GET", "POST", "PUT", "PATCH", "DELETE", "ステータスコード", "200", "201", "401", "404", "トークン", "認証", "HTTP"],
 79: ["JSON", "キー", "オブジェクト", "配列", "true", "null", "{", "["],
 80: ["Ansible", "Terraform", "Puppet", "Chef", "プレイブック", "YAML", "エージェントレス", "IaC", "冪等", "HCL", "構成管理"],
 81: ["AI", "機械学習", "生成AI", "予測AI", "ハルシネーション", "異常検知"],
}

# 手で決めた振り分け（ID → 新しい回）
FIX = {
 # 入門・基礎
 "P01-04": 7, "P01-08": 7, "P02-05": 19, "P04-04": 6, "P04-06": 6, "P04-08": 6, "P05-06": 10,
 "P07-02": 9, "P07-05": 14, "P07-08": 75, "P07-10": 9, "P08-01": 14, "P08-06": 11, "P08-07": 14,
 "P09-09": 12, "P09-13": 12, "P10-07": 14, "P11-08": 16, "P11-10": 13,
 "P12-03": 17, "P12-09": 19, "P12-10": 20, "P12-11": 19, "P12-14": 21, "P12-16": 19, "P12-18": 20, "P12-20": 20,
 "P13-04": 20, "P13-07": 22, "P14-07": 24, "P14-08": 24, "P14-09": 25,
 # アクセス
 "P20-03": 34, "P20-04": 33, "P20-05": 34, "P20-06": 33, "P20-07": 34, "P20-08": 33, "P20-09": 34,
 "P20-12": 34, "P20-13": 34, "P20-14": 34, "P20-16": 34,
 "P23-06": 40, "P23-11": 40, "P23-12": 40,
 "P27-10": 29, "P27-11": 28, "P27-12": 44, "P27-13": 44, "P27-14": 45, "P27-17": 45, "P27-19": 45,
 "P28-11": 46, "P28-12": 75, "P28-14": 46,
 # IPのつながり
 "P30-01": 49, "P30-02": 49, "P30-03": 48, "P30-05": 48, "P30-08": 49, "P30-09": 49, "P30-11": 49, "P30-32": 49, "P30-36": 51,
 "P31-03": 51, "P31-07": 51, "P31-22": 51,
 "P32-01": 55, "P32-03": 54, "P32-04": 56, "P32-05": 54, "P32-06": 54, "P32-07": 56, "P32-08": 55, "P32-09": 56,
 "P32-12": 54, "P32-13": 54, "P32-15": 54, "P32-16": 54, "P32-20": 55, "P32-21": 55, "P32-22": 56,
 "P33-07": 54, "P33-08": 53,
 # IPのサービス
 "P35-06": 59, "P35-16": 59, "P36-28": 61,
 # セキュリティ
 "P40-01": 70, "P40-02": 70, "P40-09": 70, "P40-16": 70, "P40-17": 70, "P40-18": 68,
 "P41-05": 69, "P41-10": 69, "P42-07": 67, "P42-11": 70,
 "P43-05": 73, "P43-06": 73, "P43-09": 73, "P43-10": 73, "P43-11": 73, "P43-13": 73, "P43-14": 73, "P43-16": 73,
 "P43-18": 73, "P43-20": 73, "P43-23": 73, "P43-24": 73, "P43-26": 73,
 "P45-03": 75, "P45-12": 46, "P45-13": 46,
 # 自動化
 "P47-04": 31, "P47-05": 80, "P47-10": 31, "P47-11": 31, "P48-08": 78,
}

ROOT = srcio.SRC


def load_new():
    L = {}
    for f in glob.glob(os.path.join(ROOT, "lessons_v2", "l*.json")):
        x = json.load(open(f, encoding="utf-8"))
        L[x["n"]] = x
    return L


def text_of(q):
    parts = [q.get("t", ""), q.get("e", ""), q.get("m", "")]
    o = q.get("o", [])
    for v in o:
        parts.append(v if isinstance(v, str) else json.dumps(v, ensure_ascii=False))
    for k in ("x", "c"):
        if k in q:
            parts.append(json.dumps(q[k], ensure_ascii=False))
    return re.sub(r"<[^>]+>", "", " ".join(parts))


def score(txt, words):
    low = txt.lower()
    return sum(low.count(w.lower()) * (2 if len(w) >= 4 else 1) for w in words if w)


def page_of(q, L):
    txt = text_of(q)
    best, bs = 3, -1
    for i, p in enumerate(L["pages"]):
        if "quiz" in p or i < 2 or p.get("t") in ("今日のまとめ", "まちがえやすい所"):
            continue
        body = re.sub(r"<[^>]+>", "", p.get("b", "") + " " + p.get("t", "") + " " + p.get("p", ""))
        words = set(re.findall(r"[A-Za-z][A-Za-z0-9./:+-]{1,}|[ァ-ヴー]{3,}|[一-龥]{2,}", body))
        s = score(txt, words)
        if s > bs:
            best, bs = i + 1, s
    return best


def main():
    sys.exit("2026-11-27 に切り替え済み。src/questions はもう新しい81回の番号なので、この道具は使わない（結果は src/questions/map_from_old.json）")
    report = "--report" in sys.argv
    NEW = load_new()
    out, files, weak = {}, {}, []
    for f in sorted(glob.glob(os.path.join(ROOT, "questions", "l*.json"))):
        old = int(re.search(r"l(\d+)\.json", f).group(1))
        for q in json.load(open(f, encoding="utf-8")):
            txt = text_of(q)
            cands = CAND[old]
            sc = [(score(txt, KW.get(n, []) + NEW[n]["terms"]), -k, n) for k, n in enumerate(cands)]
            sc.sort(reverse=True)
            n = FIX.get(q["id"], sc[0][2])
            if q["id"] not in FIX and len(cands) > 1 and (sc[0][0] == 0 or sc[0][0] - sc[1][0] <= 1):
                weak.append((q["id"], [(c, s) for s, _, c in sc], txt[:90]))
            p = page_of(q, NEW[n])
            out[q["id"]] = [n, p]
            q2 = dict(q)
            q2["page"] = p
            files.setdefault(n, []).append(q2)
    d = os.path.join(ROOT, "questions_v2")
    os.makedirs(d, exist_ok=True)
    for n in NEW:
        srcio.save(os.path.join(d, f"l{n:02d}.json"), files.get(n, []))
    with open(os.path.join(d, "map.json"), "w", encoding="utf-8") as fp:
        json.dump(out, fp, ensure_ascii=False, indent=0)
    cnt = {n: len(files.get(n, [])) for n in sorted(NEW)}
    print("問題数:", sum(cnt.values()), " 0問の回:", [n for n, c in cnt.items() if c == 0])
    print("回ごと:", " ".join(f"{n}:{c}" for n, c in cnt.items()))
    print("決め手の弱い問題:", len(weak))
    if report:
        for i, c, t in weak:
            print(i, c, t)


if __name__ == "__main__":
    main()
