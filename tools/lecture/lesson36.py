import sys;sys.path.insert(0,'/home/claude/lecture')
from fig import *;from mk import build
T="先生";S="生徒"
L=[
(1,T,"今日は、ネットワークを支える3つのサービス、DHCP、DNS、NTPを学びます。",None),
(1,T,"まずDHCP。端末にIPアドレスなどを、自動で配る仕組みです。手で設定する手間が減り、リース期間で、アドレスを使える時間も管理できます。",None),
(1,T,"やりとりは4ステップ。クライアントがDiscoverで、サーバーいますか、と探す。サーバーがOfferで、このアドレスはどう、と提案。クライアントがRequestで、それください、と頼む。サーバーがAckで、どうぞ、と確定します。",None),
(1,S,"頭文字でDORAですね。",None),
(1,T,"その通り。DiscoverとRequestはクライアントから、OfferとAckはサーバーから送ります。リースを更新するときは、貸してくれたDHCPサーバーに連絡します。",None),
(2,T,"ここで問題です。DHCPサーバーが、別のネットワークにあったらどうなるでしょう？",None),
(2,T,"最初のDiscoverはブロードキャストなので、ルーターを越えられません。そこで、PC側のインターフェースに、ip helper-address、DHCPサーバーのIP、と設定します。これをDHCPリレーエージェントと言います。",None),
(2,T,"ルーターが、ブロードキャストをユニキャストにして、サーバーへ転送してくれます。L3スイッチなら、そのVLANのSVIに設定します。",None),
(2,S,"設定するのは、PCがつながっている側のインターフェースなんですね。",None),
(3,T,"ルーター自身をDHCPサーバーにするなら、ip dhcp poolでアドレスプールを作ります。中で、network、default-routerでゲートウェイ、dns-serverでDNSサーバーを配ります。",None),
(3,T,"ip dhcp excluded-addressで、ゲートウェイやサーバー用のアドレスを配らないように除外します。特定の機器にいつも同じアドレスを配る、手動バインディングもできます。配ったアドレスは、show ip dhcp bindingで確認します。",None),
(3,T,"逆に、ルーターのインターフェースをDHCPのクライアントにするなら、ip address dhcpです。",None),
(4,T,"次はDNS。www.example.comのような名前を、IPアドレスに変換する、ネットの電話帳です。クライアントが名前の解決要求をDNSサーバーに送り、ポートは53番です。",None),
(4,T,"レコードの種類は、AがIPv4、AAAAがIPv6、CNAMEは別名、MXはメールサーバー、NSはネームサーバーです。",None),
(4,T,"DNSフォワーダーは、自分で分からない名前の問い合わせを、外部のDNSサーバーに転送する仕組み。ルーター自身が名前を引くときのDNSサーバーは、ip name-serverで指定します。",None),
(5,T,"最後はNTP。機器の時刻を合わせるプロトコルです。時刻がずれていると、ログを比べて障害の原因を追えなくなります。",None),
(5,T,"stratumという数字は、時刻源からの距離です。小さいほど、原子時計などの正確な時刻源に近く、受け取る側は1つ大きくなります。R1が3なら、そのサーバーは2です。",None),
(5,T,"ntp serverと設定したルーターは、ほかから時刻を受け取るクライアント。ntp masterは、自分が時刻源になる設定です。",None),
(6,T,"ここで小テストです。DHCPのやりとりの正しい順番はどれでしょう？画面で選んでください。",None),
(6,T,"正解は、Discover、Offer、Request、Ackです。",None),
(7,T,"では、今日のまとめです。",None),
(7,T,"1つ目。DHCPはDORA。別のネットワークのサーバーには、PC側にip helper-address。",None),
(7,T,"2つ目。サーバーはip dhcp poolとexcluded-address、クライアントはip address dhcp。",None),
(7,T,"3つ目。DNSはポート53、AとAAAAとCNAME。NTPはstratumが小さいほど正確、ntp serverはクライアント。",None),
(7,S,"3つのサービスの役割、すっきりしました！",None),
(7,T,"よかったです。次回は、SNMPとSyslogで、ネットワークを見張る方法を学びます。お疲れさまでした。",None),
]
SC=["DHCPのDORA","DHCPリレー","ルーターのDHCP設定","DNS","NTP","小テスト","まとめ"]
p1=svg(250,"".join([sc(50,40,.7,pc(0,0)),lab(50,72,"クライアント",11.5),sc(310,40,.7,server(0,0)),lab(310,74,"DHCPサーバー",11.5),'<path d="M50 84v150M310 84v150" stroke="var(--line)" stroke-width="3"/>',
 arrow(56,104,304,112,B),lab(180,100,"① Discover（ブロードキャスト）",12,800,B),arrow(304,140,56,148,G),lab(180,136,"② Offer",12,800,G),arrow(56,176,304,184,B),lab(180,172,"③ Request",12,800,B),arrow(304,212,56,220,G),lab(180,208,"④ Ack",12,800,G),lab(180,244,"DORA：クライアント＝D・R／サーバー＝O・A",12,800)]),"DHCPのDORA")
p2=svg(220,"".join([sc(50,70,.7,pc(0,0)),lab(50,102,"PC（VLAN10）",11.5),sc(180,70,.8,router(0,0)),lab(180,108,"ルーター",12),sc(310,70,.7,server(0,0)),lab(310,104,"DHCPサーバー",11.5),'<path d="M74 70h70M216 70h70" stroke="var(--ink)" stroke-width="3"/>',
 lab(110,52,"ブロードキャスト",11,800,R),lab(250,52,"ユニキャスト",11,800,G),tag(130,140,"PC側のIF：ip helper-address サーバーIP",B,280),lab(180,180,"ブロードキャストはルーターを越えられない → DHCPリレー",12,800),lab(180,202,"L3スイッチならそのVLANのSVIに設定",11.5,700,"var(--sub)")]),"DHCPリレー")
R3=rows([(None,"ip dhcp pool","network／default-router（GW）／dns-server",B),(None,"ip dhcp excluded-address","GWやサーバー用のアドレスを配らない",G),(None,"手動バインディング","特定の機器にいつも同じアドレス",A),(None,"show ip dhcp binding／ip address dhcp","配ったアドレスの一覧／IFをDHCPクライアントに",K)]);p3=svg(R3[1]+4,R3[0],"ルーターのDHCP設定")
R4=rows([(None,"DNS＝名前→IPアドレス","クライアントが解決要求を送る。ポート53",B),(None,"A／AAAA／CNAME／MX／NS","IPv4／IPv6／別名／メール／ネームサーバー",G),(None,"DNSフォワーダー","分からない問い合わせを外部のDNSへ転送",A),(None,"ip name-server 8.8.8.8","ルーター自身が使うDNSサーバー",K)]);p4=svg(R4[1]+4,R4[0],"DNS")
p5=svg(230,"".join([f'<rect x="130" y="10" width="100" height="34" rx="8" fill="{A}"/>',lab(180,32,"時刻源 stratum 0",12,800),sc(180,80,.6,server(0,0)),lab(240,84,"stratum 1",12,800,"var(--ink)","start"),sc(110,140,.6,router(0,0)),lab(160,144,"2",13,800,"var(--ink)","start"),sc(250,140,.6,router(0,0)),lab(300,144,"3",13,800,"var(--ink)","start"),'<path d="M180 44v18M174 98L118 126M190 98L240 126" stroke="var(--ink)" stroke-width="2"/>',
 lab(180,186,"小さいほど正確／受け取る側は＋1",13,800),lab(180,210,"ntp server＝クライアント、ntp master＝自分が時刻源",12,700,"var(--sub)")]),"NTPとstratum")
R7=rows([(None,"DHCP＝DORA","別ネットワークのサーバー → PC側に ip helper-address",B),(None,"ip dhcp pool／excluded-address","クライアントは ip address dhcp",G),(None,"DNS 53・A・AAAA・CNAME","NTP：stratum小＝正確、ntp server＝クライアント",A)]);P7=svg(R7[1]+4,R7[0],"今日のまとめ")
qt=lambda t,c:f'<g><text x="0" y="5" text-anchor="middle" style="font:800 10px {mono};fill:{c}">{t}</text></g>'
pages=[
 {"t":"DHCPのDORA","svg":p1,"b":"<b>DHCP</b>（Dynamic Host Configuration Protocol）は IPアドレスを自動で配ります。利点は<b>管理の手間が減る</b>ことと、<b>リース期間</b>で使える時間を管理できること。","p":"リースの更新 → 貸してくれたDHCPサーバー（ipconfigのDHCP Server）へ。"},
 {"t":"DHCPリレー","svg":p2,"b":"<b>DHCPリレーエージェント</b>は、ブロードキャストのDHCPDISCOVERを別ネットワークのサーバーへ届けます。","p":"設定するのはPCがつながっている側のインターフェース。"},
 {"t":"ルーターのDHCP設定","svg":p3,"b":"ルーターをDHCPサーバーにするとき設定するのは<b>アドレスプール</b>と<b>手動バインディング</b>。","p":"ip helper-address はリレー、ip address dhcp はクライアント。"},
 {"t":"DNS","svg":p4,"b":"<b>DNS</b>（Domain Name System）はネットの電話帳。普通のルックアップは名前→IP。","p":"IPv6アドレスを返す＝AAAA。"},
 {"t":"NTP","svg":p5,"b":"<b>NTP</b>（Network Time Protocol）で時刻をそろえると、ログを比べて障害の原因を追えます。","p":"ntp server が設定されているルーターはクライアント。"},
 {"t":"小テスト","quiz":{"q":"DHCPのやりとりの正しい順番は？","o":[["Discover→Offer→Request→Ack",qt("D→O→R→A",B)],["Request→Offer→Discover→Ack",qt("R→O→D→A",G)],["Discover→Request→Offer→Ack",qt("D→R→O→A",K)]],"a":0,"e":"正解は<b>Discover → Offer → Request → Ack</b>（DORA）。"}},
 {"t":"今日のまとめ","svg":P7,"b":"次回は「SNMP・Syslog」。","p":"一問一答の「IPサービス」で確かめましょう。"}]
build(36,"nl35","DHCP・DNS・NTP","IPサービス",SC,L,pages,None)
