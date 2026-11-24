G=[]
def g(id,t,s,ex,mk,tips): G.append(dict(id=id,t=t,s=s,ex=ex.strip('\n'),mk=mk,tips=tips))

g("topo","構成図（ネットワーク図）","問題の舞台。まず「誰が・どこに・どうつながっているか」を書き出す。",
"""【構成】
PC1 ── Fa0/1 [SW1] Gi0/1 ── G0/0 [R1] S0/0 ──(10.0.12.0/30)── S0/0 [R2]
                                                                   G0/1
PC1: 192.168.1.10/24  GW 192.168.1.1                               |
R1 G0/0: 192.168.1.1/24                                      192.168.2.0/24""",
[[1,1,"[ ]で囲まれたのが機器。PC・スイッチ（SW）・ルーター（R）を区別する"],[1,2,"Fa0/1・G0/0・S0/0 は線がつながっているポート（インターフェース）の名前。線の両端に1つずつある"],[1,3,"線の上の 10.0.12.0/30 は、その線（リンク）のネットワーク"],[3,4,"PCのIP・マスク・デフォルトゲートウェイ（GW）。GWは同じネットワークのルーターのIPになっているはず"]],
["最初に「PC → スイッチ → ルーター → … → 宛先」の通り道を指でなぞる。","1本の線の両端は、必ず同じネットワーク（同じサブネット）。違っていたらそこが問題。","Fa＝FastEthernet（100M）、Gi/G＝GigabitEthernet（1G）、S/Se＝シリアル。番号は「スロット/ポート」。","問題文で聞かれている機器に印を付け、関係ない機器は無視する。"])

g("route","show ip route（ルーティングテーブル）","ルーターが「この宛先はどこへ送るか」を書いた表。1行＝1つの経路。",
"""R1# show ip route
Codes: C - connected, S - static, O - OSPF, D - EIGRP, R - RIP ...
Gateway of last resort is 10.0.0.2 to network 0.0.0.0

S*    0.0.0.0/0 [1/0] via 10.0.0.2
      10.0.0.0/8 is variably subnetted, 2 subnets, 2 masks
C        10.0.0.0/30 is directly connected, GigabitEthernet0/1
L        10.0.0.1/32 is directly connected, GigabitEthernet0/1
O        172.16.1.0/24 [110/20] via 10.0.0.2, 00:05:12, GigabitEthernet0/1
D        172.16.2.0/24 [90/3072] via 10.0.0.2, 00:03:40, GigabitEthernet0/1""",
[[2,1,"Gateway of last resort＝デフォルトルート。not set なら無い"],[4,2,"行頭の記号＝経路の覚え方（Codes表で確認）。S*＝デフォルトルートのスタティック"],[6,3,"C＝直接つながったネットワーク、L＝自分のインターフェースのIP（/32）"],[8,4,"宛先ネットワーク/プレフィックス長"],[8,5,"[AD/メトリック]。左がAD（信頼度、小さいほど優先）、右がメトリック（距離）"],[8,6,"via ＝ ネクストホップ（次に渡すルーター）のIP、最後が出ていくインターフェース"]],
["「宛先 X はどの行で送られる？」→ X を含む行をすべて探し、プレフィックス長（/の数字）が一番長い行を選ぶ（ロンゲストマッチ）。","同じ宛先が複数のプロトコルで届いたときはADが小さい方、同じプロトコルならメトリックが小さい方がテーブルに載る。","AD：接続0・スタティック1・EIGRP90・OSPF110・RIP120。","どの行にも当てはまらない→デフォルトルート（0.0.0.0/0）。それも無ければ破棄。"])

g("intf","show interfaces（インターフェースの詳細）","1つのポートの状態・速度・エラーの数がまとめて出る。上から順に見る場所が決まっている。",
"""R1# show interfaces GigabitEthernet0/1
GigabitEthernet0/1 is up, line protocol is up
  Internet address is 10.0.0.1/30
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Full-duplex, 1000Mb/s, media type is RJ45
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  5 minute input rate 2000 bits/sec, 3 packets/sec
     Received 120 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 output errors, 0 collisions, 0 interface resets
     0 late collision, 0 deferred""",
[[1,1,"1つ目＝物理層（線）、2つ目＝データリンク層の状態。up/up が正常"],[4,2,"reliability は 255/255 が満点。txload/rxload は混み具合（255/255 は満杯）"],[5,3,"デュプレックスと速度。相手と違うと（Half と Full など）衝突やエラーが出る"],[6,4,"Input queue の drops・Total output drops が多い＝処理しきれずに捨てている（混雑）"],[8,5,"broadcasts が受信パケットに比べて多すぎる→ブロードキャストストーム"],[10,6,"CRC・input errors が多い＝ケーブルの不良やノイズ"],[11,7,"collisions・late collision が多い＝デュプレックスの不一致を疑う"]],
["まず1行目の up/down を見る。administratively down＝shutdownされている。down/down＝線やポートの問題。","数字が0でない行を探すと、問題のありかがすぐ分かる。","Half-duplex と collisions → デュプレックス不一致、CRC → ケーブル、drops → 混雑、broadcasts大量 → ストーム、と結び付けて覚える。"])

g("brief","show ip interface brief","全部のポートを1行ずつ並べた一覧。IPと状態だけ素早く見る。",
"""R1# show ip interface brief
Interface            IP-Address     OK? Method Status                Protocol
GigabitEthernet0/0   192.168.1.1    YES manual up                    up
GigabitEthernet0/1   10.0.0.1       YES manual up                    down
Serial0/0/0          unassigned     YES unset  administratively down down""",
[[2,1,"Status＝物理層、Protocol＝データリンク層。up / up が正常"],[3,2,"up / down＝線はつながっているが通信の約束（カプセル化・キープアライブなど）が合っていない"],[4,3,"administratively down＝shutdown コマンドで止められている。no shutdown で起動"],[4,4,"unassigned＝IPアドレスが設定されていない"]],
["左から「ポート名 → IP → 状態」の順に読むだけ。","down / down は線が抜けている・相手が止まっているなど物理の問題。"])

g("run","show running-config（今の設定）","機器に今入っている設定の全文。「!」で区切られたかたまりごとに読む。",
"""R1# show running-config
hostname R1
!
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 ip nat inside
 no shutdown
!
interface GigabitEthernet0/1
 ip address 203.0.113.2 255.255.255.252
 ip nat outside
!
ip route 0.0.0.0 0.0.0.0 203.0.113.1
!
line vty 0 4
 login local
 transport input ssh""",
[[3,1,"interface ～ の下の字下げされた行が、そのポートだけの設定"],[4,2,"IPとサブネットマスク。マスクを /24 などに直して、どのネットワークか確かめる"],[10,3,"ip nat inside/outside など、内側と外側が正しく付いているか"],[12,4,"字下げの無い行は機器全体の設定（ここではデフォルトルート）"],[14,5,"line vty＝リモートログイン（Telnet/SSH）の設定"]],
["問題の機能（NAT、ACL、OSPFなど）に関係するかたまりだけを探して読む。","「足りない行」を聞かれることが多い。正しい設定の手順を思い出して、抜けている1行を探す。","shutdown が付いているポートは止まっている。"])

g("vlan","show vlan brief / show interfaces trunk","どのポートがどのVLANか、トランクで何が通れるかの一覧。",
"""SW1# show vlan brief
VLAN Name        Status    Ports
1    default     active    Fa0/3, Fa0/4
10   SALES       active    Fa0/1, Fa0/2
20   HR          active    Fa0/5

SW1# show interfaces trunk
Port    Mode   Encapsulation  Status    Native vlan
Gi0/1   on     802.1q         trunking  1
Port    Vlans allowed on trunk
Gi0/1   10,30""",
[[3,1,"VLAN 10 に入っているアクセスポート。トランクポートはここに出てこない"],[8,2,"trunking＝トランクとして動いている。Native vlan は両端でそろえる"],[10,3,"トランクで通してよいVLAN。ここに無いVLAN（例：20）は相手のスイッチへ届かない"]],
["「PCどうしが通信できない」→ ①同じVLANか ②トランクで許可されているか ③ネイティブVLANが一致しているか、の順に確かめる。"])

g("stp","show spanning-tree（STP）","どのスイッチがルートで、各ポートがどの役割・状態かの表。",
"""SW2# show spanning-tree vlan 10
VLAN0010
  Root ID    Priority    4106
             Address     0011.1111.1111
             Cost        19
             Port        1 (FastEthernet0/1)
  Bridge ID  Priority    32778  (priority 32768 sys-id-ext 10)
             Address     0022.2222.2222
Interface   Role Sts Cost  Prio.Nbr Type
Fa0/1       Root FWD 19    128.1    P2p
Fa0/2       Altn BLK 19    128.2    P2p
Fa0/3       Desg FWD 19    128.3    P2p""",
[[2,1,"Root ID＝ルートブリッジの情報。Bridge ID＝このスイッチ自身の情報"],[6,2,"Root ID と Bridge ID のアドレスが同じなら、自分がルートブリッジ（This bridge is the root と出る）"],[6,3,"プライオリティ＝設定値＋VLAN番号（32768＋10＝32778）"],[9,4,"Role：Root＝ルートポート、Desg＝指定ポート、Altn＝代替ポート（予備）"],[10,5,"Sts：FWD＝転送中、BLK＝ブロック中（ループ防止で止めている）"]],
["ルートブリッジ＝プライオリティが一番小さいスイッチ。同じならMACアドレスが小さい方。","ルートブリッジのポートは全部 Desg（指定ポート）。","Cost はルートまでの道のりの合計。小さい方の道のポートがルートポートになる。"])

g("ospf","show ip ospf neighbor / interface","OSPFでつながった相手（ネイバー）と、各ポートのOSPF設定。",
"""R1# show ip ospf neighbor
Neighbor ID   Pri  State      Dead Time  Address    Interface
2.2.2.2       1    FULL/DR    00:00:35   10.0.0.2   Gi0/0
3.3.3.3       1    2WAY/DROTHER 00:00:31 10.0.0.3   Gi0/0

R1# show ip ospf interface Gi0/0
  Internet Address 10.0.0.1/24, Area 0
  Router ID 1.1.1.1, Network Type BROADCAST, Cost: 1
  Transmit Delay is 1 sec, State BDR, Priority 1
  Timer intervals configured, Hello 10, Dead 40""",
[[2,1,"Neighbor ID＝相手のルーターID（IPアドレスではない）"],[2,2,"State：FULL＝情報交換完了。/DR は相手の役割"],[3,3,"2WAY/DROTHER＝DRでもBDRでもない者どうしは2WAYのままで正常"],[6,4,"Area・Cost・Network Type（BROADCAST なら DR/BDR を選ぶ）"],[9,5,"Hello/Dead タイマー。相手と違うとネイバーになれない"]],
["ネイバーにならない理由は「エリア・Hello/Dead・サブネット・認証・MTU・ルーターID重複・passive」のどれかを比べる。","ExStart/Exchange で止まる → MTU不一致。"])

g("acl","show access-lists（ACL）","上の行から順に比べ、最初に一致した行で許可・拒否が決まる。",
"""R1# show access-lists
Extended IP access list 110
    10 deny tcp 192.168.1.0 0.0.0.255 host 10.1.1.10 eq 23
    20 permit tcp any host 10.1.1.10 eq 80 (12 matches)
    30 permit icmp any any""",
[[2,1,"行番号（シーケンス番号）。小さい順にチェックする"],[2,2,"拡張ACLは「プロトコル 送信元 宛先 ポート」の順。eq 23＝Telnet"],[3,3,"(12 matches)＝この行に一致した回数"],[4,4,"最後には見えない deny any がある。ここに無い通信は全部拒否"]],
["ワイルドカード：0は「同じでないとダメ」、255は「何でもよい」。0.0.0.255 なら最後の数字だけ自由。","host X ＝ X 1台だけ（X 0.0.0.0 と同じ）、any ＝ 全部。","聞かれた通信（送信元・宛先・ポート）を1行目から当てはめ、最初に一致した行の結果が答え。"])

g("nat","show ip nat translations（NAT）","内側のアドレスが外でどう見えるかの変換表。",
"""R1# show ip nat translations
Pro Inside global      Inside local       Outside local      Outside global
tcp 203.0.113.5:1025   192.168.1.10:51000 198.51.100.7:80    198.51.100.7:80
tcp 203.0.113.5:1026   192.168.1.11:51000 198.51.100.7:80    198.51.100.7:80
--- 203.0.113.20       192.168.1.50       ---                ---""",
[[1,1,"Inside local＝社内の本当のIP、Inside global＝外から見えるIP"],[2,2,":1025 などポート番号付きで1つのグローバルIPを共有→PAT（オーバーロード）"],[4,3,"--- だけの行（ポートなし）＝スタティックNATの固定の対応"]],
["inside/outside は「どちら側の機器か」、local/global は「どちらから見たアドレスか」。"])

g("sw","スイッチの確認コマンド（MAC表・EtherChannel・CDP・HSRPなど）","1行＝1つの対応。列の見出しを先に読む。",
"""SW1# show mac address-table
Vlan  Mac Address     Type     Ports
10    aaaa.0001.0001  DYNAMIC  Fa0/1

SW1# show etherchannel summary
Group  Port-channel  Protocol  Ports
1      Po1(SU)       LACP      Gi0/1(P) Gi0/2(P)

R1# show standby brief
Interface Grp Pri P State  Active  Standby  Virtual IP
Gi0/0     1   110 P Active local   10.0.0.3 10.0.0.254""",
[[2,1,"MAC表：このMACあての通信はこのポートへ送る。DYNAMIC＝学習した"],[6,2,"(SU)＝レイヤ2で使用中。(P)＝束ねられている。(I)＝単独・(s)＝停止中"],[10,3,"HSRP：State Active＝今のゲートウェイ役。P＝プリエンプト有効。Virtual IP をPCのGWにする"]],
["まず列の見出しを読み、聞かれている列だけ追う。","show cdp neighbors は Device ID＝相手の名前、Local Intrfce＝自分のポート、Port ID＝相手のポート。"])

g("wlc","WLCの画面（無線LANコントローラー）","WLANの設定画面。タブ（General・Security・QoS・Advanced）ごとに見る場所が決まっている。",
"""WLANs > Edit 'Corp'
[General]  Status [x] Enabled   SSID Corp   Interface data
[Security] Layer 2: WPA+WPA2
           WPA2 Policy [x]  Encryption AES(CCMP128) [x]
           Auth Key Mgmt  PSK [x]   802.1X [ ]
[Advanced] Allow AAA Override [ ]""",
[[1,1,"General：Status が Enabled でないとSSIDが出ない。Interface＝流すVLAN"],[2,2,"Security の Layer 2：WPA2/WPA3 などの方式"],[3,3,"暗号化は AES（CCMP128）。TKIP は古い"],[4,4,"認証キー管理：PSK＝共通パスワード、802.1X＝RADIUSで1人ずつ"]],
["チェックが入っている [x] と入っていない [ ] を見比べる。","「〇〇だけにするには？」→ 余計なチェックを外す、が答えになりやすい。"])

g("data","JSON・API・自動化の出力","{ } と [ ] の入れ子を、外側から内側へたどる。",
"""{
  "hostname": "R1",
  "interfaces": [
    {"name": "Gi0/0", "ip": "10.0.0.1", "enabled": true},
    {"name": "Gi0/1", "ip": "10.0.1.1", "enabled": false}
  ]
}""",
[[1,1,"\"キー\": 値 の組。コロンの左がキー、右が値"],[2,2,"[ ] は配列（リスト）。中に同じ形のものが並ぶ"],[3,3,"{ } はオブジェクト。1つのかたまり。true/false は真偽値"]],
["数を聞かれたら：{ }の組＝オブジェクト、コロン＝キー、[ ]の中の要素＝配列の値、と数える。","APIの応答は ステータスコード（200・201・401・404…）を最初に見る。"])

g("pc","PCのコマンド（ipconfig・ping・tracert）","PC側から見た設定と、どこまで届いたか。",
"""C:\\> ipconfig
   IPv4 Address. . . . . : 192.168.1.10
   Subnet Mask . . . . . : 255.255.255.0
   Default Gateway . . . : 192.168.1.1

C:\\> tracert 10.3.3.3
  1    1 ms   192.168.1.1
  2    2 ms   10.0.12.2
  3    *      Request timed out.""",
[[1,1,"PCのIPとマスク。同じネットワークの範囲を計算しておく"],[3,2,"デフォルトゲートウェイ。PCと同じネットワークのルーターのIPか確かめる"],[7,3,"tracert は1行＝1台のルーター。* が続く手前（10.0.12.2）の先で止まっている"]],
["ping：! 成功、. タイムアウト、U 到達不能の通知。","ゲートウェイが別のネットワークだったり、他の機器のIPだったりしたら、そこが原因。"])

g("log","ログ（Syslog）メッセージ","「%機能-重大度-種類: 内容」の形。",
"""%LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to down
%CDP-4-NATIVE_VLAN_MISMATCH: Native VLAN mismatch discovered on Gi0/1 (1), with SW2 Gi0/1 (10).""",
[[0,1,"LINK＝どの機能のメッセージか、3＝重大度（0が最も深刻〜7がdebug）"],[0,2,"コロンの後ろが中身。どのポートがどうなったか"],[1,3,"NATIVE_VLAN_MISMATCH＝両端のネイティブVLANが違う（1 と 10）"]],
["重大度は 0緊急・1警報・2重大・3エラー・4警告・5通知・6情報・7デバッグ。"])
