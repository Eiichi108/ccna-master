import sys;sys.path.insert(0,'/home/claude/lecture')
from fig import *;from mk import build
T="先生";S="生徒"
L=[
(1,T,"今日は、IP電話のための音声VLANと、スイッチやルーターを管理する方法を学びます。",None),
(1,T,"会社の机では、壁のポートにIP電話をつなぎ、その電話の後ろにPCをつなぐことがよくあります。ケーブル1本で、電話とPCの両方を使うんです。",None),
(1,S,"電話とPCの通信が、混ざっちゃいませんか？",None),
(1,T,"そこで音声VLANです。電話の通信には音声VLANのタグを付け、PCの通信はタグなしで、データVLANに流します。",None),
(1,T,"設定は、switchport mode access、switchport access vlan 10でPC用のデータVLAN、そしてswitchport voice vlan 20で音声VLANを決めます。",None),
(1,T,"Ciscoの電話は、使う音声VLANを、スイッチからCDPやLLDP-MEDで教えてもらいます。",None),
(1,T,"ポートのアクセスVLAN、音声VLAN、動いているモードは、show interfaces g0/1 switchportでまとめて確認できます。",None),
(2,T,"次は、機器の管理です。リモートからCLIを操作する方法は2つ。TelnetとSSHです。",None),
(2,T,"Telnetは通信が平文、つまり暗号化されないので、パスワードを盗み見られる危険があります。SSHはTCP 22番で、通信を暗号化します。必ずSSHを使いましょう。",None),
(2,T,"Webの画面で管理する場合も同じで、ip http secure-serverでHTTPSを有効にし、no ip http serverで平文のHTTPを止めます。",None),
(2,S,"暗号化されている方を使う、が鉄則ですね。",None),
(3,T,"では、L2スイッチに、管理用のIPアドレスはどこに付けるでしょう？",None),
(3,T,"L2スイッチのポートには、IPアドレスを付けられません。だから、interface vlan 1のようなSVIに付けます。",None),
(3,T,"さらに、ip default-gatewayでゲートウェイを設定します。これがないと、別のネットワークの管理用PCに、スイッチが返事を返せません。",None),
(3,T,"ネットワークが落ちていても使えるのが、コンソール接続です。ケーブルで機器に直接つなぐので、アウトオブバンド管理とも言います。",None),
(3,T,"line con 0でexec-timeout 5 0と設定すると、5分間操作がなければ自動でログアウトします。放置された画面を、ほかの人に操作されるのを防ぎます。",None),
(4,T,"ここで小テストです。暗号化された通信で、リモートから機器のCLIを操作する方法はどれでしょう？画面で選んでください。",None),
(4,T,"正解はSSHです。Telnetは平文でしたね。",None),
(5,T,"では、今日のまとめです。",None),
(5,T,"1つ目。IP電話は音声VLANのタグ付き、PCはタグなしでデータVLAN。switchport voice vlanで設定し、電話はCDPやLLDPで教えてもらう。",None),
(5,T,"2つ目。Telnetは平文、SSHは暗号化。WebもHTTPSにする。",None),
(5,T,"3つ目。L2スイッチの管理IPはSVIに付けて、ip default-gateway。コンソールはネットワークが落ちても使える。",None),
(5,S,"電話の後ろのPC、これで仕組みが分かりました！",None),
(5,T,"よかったです。次回は、スパニングツリー、STPを学びます。お疲れさまでした。",None),
]
SC=["音声VLAN","TelnetとSSH","L2スイッチの管理","小テスト","まとめ"]
p1=svg(250,"".join([sc(50,60,.8,switch(0,0)),lab(50,96,"スイッチ",12),sc(180,60,.8,phone(0,0,G)),lab(180,96,"IP電話",12),sc(310,60,.7,pc(0,0)),lab(310,96,"PC",12),'<path d="M84 60h70M206 60h76" stroke="var(--ink)" stroke-width="3"/>',
 tag(118,126,"音声VLAN 20：タグあり",G,170),tag(240,160,"PC：タグなし→データVLAN 10",B,210),
 f'<rect x="10" y="182" width="340" height="60" rx="10" fill="var(--card)" stroke="var(--line)" stroke-width="2"/>',f'<text x="22" y="206" style="font:700 12px {mono};fill:var(--ink)">switchport access vlan 10</text><text x="22" y="228" style="font:700 12px {mono};fill:{G}">switchport voice vlan 20</text>']),"音声VLANのしくみ")
R2=rows([(None,"Telnet（TCP 23）","平文。パスワードを盗み見られる",R),(None,"SSH（TCP 22）","通信を暗号化。リモート管理はこちら",G),(None,"Web管理","ip http secure-server（HTTPS）＋ no ip http server",B)]);p2=svg(R2[1]+4,R2[0],"TelnetとSSH")
R3=rows([(None,"管理IPはSVIに","interface vlan 1 などに ip address（L2スイッチのポートには付けられない）",B),(None,"ip default-gateway","別のネットワークの管理PCに返事を返すため",G),(None,"コンソール接続","ケーブルで直接。ネットワークが落ちても使える（アウトオブバンド）",K),(None,"exec-timeout 5 0","5分操作がなければ自動でログアウト",A)]);p3=svg(R3[1]+4,R3[0],"L2スイッチの管理")
R5=rows([(None,"音声VLAN：電話はタグ付き、PCはタグなし","switchport voice vlan／CDP・LLDP-MEDで電話に伝える",G),(None,"Telnet＝平文、SSH＝暗号化","WebもHTTPSに",R),(None,"管理IPはSVI＋ip default-gateway","コンソールはアウトオブバンド",B)]);P5=svg(R5[1]+4,R5[0],"今日のまとめ")
qt=lambda t,c:f'<g>{tag(0,0,t,c,90)}</g>'
pages=[
 {"t":"音声VLAN","svg":p1,"b":"IP電話の後ろにPCをつなぐとき、電話の通信には<b>音声VLAN</b>のタグを付け、PCの通信はタグなしで<b>データVLAN</b>（access vlan）に流します。Ciscoの電話は、スイッチから<b>CDP</b>や<b>LLDP-MED</b>で音声VLANを教えてもらいます。","p":"確認：show interfaces g0/1 switchport"},
 {"t":"TelnetとSSH","svg":p2,"b":"<b>SSH</b>（Secure Shell）は暗号化、<b>Telnet</b>は平文。Web管理もHTTPSにして、平文のHTTPは止めます。","p":"暗号化されたリモート操作＝SSH。"},
 {"t":"L2スイッチの管理","svg":p3,"b":"L2スイッチの管理用IPアドレスは<b>SVI</b>に付け、<b>ip default-gateway</b>を設定します。","p":"放置された画面対策 → exec-timeout。"},
 {"t":"小テスト","quiz":{"q":"暗号化された通信で、リモートから機器のCLIを操作する方法は？","o":[["SSH",qt("SSH",G)],["Telnet",qt("Telnet",R)],["HTTP",qt("HTTP",B)]],"a":0,"e":"正解は<b>SSH</b>（TCP 22）。Telnetは平文です。"}},
 {"t":"今日のまとめ","svg":P5,"b":"次回は「STP（スパニングツリー）」。","p":"一問一答の「ネットワークアクセス」で確かめましょう。"}]
build(22,"nl21","音声VLAN・管理アクセス","ネットワークアクセス",SC,L,pages,None)
