import sys;sys.path.insert(0,'/home/claude/lecture')
from fig import *;from mk import build
T="先生";S="生徒"
L=[
(1,T,"今日は、スイッチを守る、L2セキュリティを学びます。主役は3つ。ポートセキュリティ、DHCPスヌーピング、DAIです。",None),
(1,T,"ポートセキュリティは、ポートにつないでよい機器を、MACアドレスで制限する機能です。何も設定しなければ、許可されるMACアドレスは1つだけです。",None),
(1,T,"設定するには、先にswitchport mode accessで、アクセスポートに固定します。dynamicのポートには設定できず、エラーになります。",None),
(1,T,"stickyを使うと、学習したMACアドレスを、running-configに書き込みます。保存すれば、再起動しても残ります。MACを手で書く方法もあります。",None),
(2,T,"許可していない機器がつながったときの動作、違反モードは3つです。",None),
(2,T,"protectは、違反したフレームを、記録せずに捨てるだけ。restrictは、捨てて、ログを出し、カウンターを増やします。どちらもポートは止まりません。",None),
(2,T,"shutdownは初期値で、ポートを止めて、err-disable状態にします。show port-securityで、Secure-shutdownと出ます。",None),
(2,S,"止まったポートは、どうやって戻すんですか？",None),
(2,T,"原因の機器を外してから、shutdown、no shutdownで戻します。errdisable recoveryを設定しておけば、自動で戻すこともできます。",None),
(3,T,"次は、DHCPスヌーピングです。攻撃者が、偽のDHCPサーバーを置いて、自分をデフォルトゲートウェイに見せかける攻撃を防ぎます。",None),
(3,T,"正規のDHCPサーバーがある方向のポートを、trust、信頼するポートにします。それ以外の信頼しないポートから、サーバーの応答であるOfferやAckが届いたら、偽物とみなして遮断します。",None),
(3,T,"設定は、グローバルでip dhcp snoopingと、対象のVLANを指定するip dhcp snooping vlan 10の両方が必要です。limit rateで、DHCPの要求を大量に送ってアドレスを使い切らせる、DHCPスタベーション攻撃も防げます。",None),
(3,T,"DHCPスヌーピングは、誰にどのIPアドレスが配られたか、IPとMACの対応表、バインディングテーブルを作ります。",None),
(4,T,"最後はDAI、ダイナミックARPインスペクションです。偽のARP応答を送って、通信を横取りする中間者攻撃を防ぎます。",None),
(4,T,"DAIは、DHCPスヌーピングで作ったバインディングテーブルと照らし合わせて、合わないARPを遮断します。",None),
(4,S,"DHCPスヌーピングが先に必要なんですね。",None),
(4,T,"その通り。設定はip arp inspection vlan 10。ほかのスイッチやルーターにつながる、信頼できるポートは、ip arp inspection trustにして、検査を省きます。",None),
(5,T,"ここで小テストです。ポートセキュリティで、違反したときの動作の初期値はどれでしょう？画面で選んでください。",None),
(5,T,"正解はshutdownです。",None),
(6,T,"では、今日のまとめです。",None),
(6,T,"1つ目。ポートセキュリティはMACの数を制限、初期値1、アクセスポートに固定してから。stickyで学習したMACを保存。",None),
(6,T,"2つ目。違反時は、protectが捨てるだけ、restrictが捨てて記録、shutdownが初期値でerr-disable。",None),
(6,T,"3つ目。DHCPスヌーピングは偽のDHCPサーバーを防ぎ、正規の方向をtrustに。DAIはその表で偽のARPを防ぐ。",None),
(6,S,"3つの守り、つながりが分かりました！",None),
(6,T,"よかったです。次回は、VPNと無線LANのセキュリティを学びます。お疲れさまでした。",None),
]
SC=["ポートセキュリティ","違反モード","DHCPスヌーピング","DAI","小テスト","まとめ"]
R1=rows([(None,"MACアドレスの数を制限","maximum の初期値は1",B),(None,"switchport mode access が先","dynamic のポートには設定できない",K),(None,"sticky","学習したMACをrunning-configに書き込む",G)]);p1=svg(R1[1]+4,R1[0],"ポートセキュリティ")
R2=rows([(None,"protect","違反フレームを捨てるだけ（記録なし）",G),(None,"restrict","捨てて、ログとカウンター（ポートは止まらない）",A),(None,"shutdown（初期値）","err-disable（Secure-shutdown）。原因を外して shutdown → no shutdown",R)]);p2=svg(R2[1]+4,R2[0],"違反モード")
p3=svg(250,"".join([sc(180,50,.9,switch(0,0)),sc(60,140,.7,server(0,0)),lab(60,178,"正規のDHCP",12,800,G),tag(110,96,"trust",G,60),sc(300,140,.7,pc(0,0,R)),lab(300,176,"偽のDHCP",12,800,R),'<path d="M166 66L74 120M196 66L286 120" stroke="var(--ink)" stroke-width="2.5"/>',f'<path d="M250 100l20 20M270 100l-20 20" stroke="{R}" stroke-width="4"/>',lab(260,90,"Offer/Ack遮断",11,800,R),
 lab(180,206,"ip dhcp snooping ＋ ip dhcp snooping vlan 10",12,800),lab(180,228,"limit rate でDHCPスタベーション対策／バインディングテーブルを作る",11,700,"var(--sub)")]),"DHCPスヌーピング")
R4=rows([(None,"DAI（ダイナミックARPインスペクション）","偽のARPによる中間者攻撃を防ぐ",B),(None,"バインディングテーブルと照合","DHCPスヌーピングで作ったIPとMACの対応表",G),(None,"ip arp inspection vlan 10","ほかのスイッチ・ルーター側は ip arp inspection trust",A)]);p4=svg(R4[1]+4,R4[0],"DAI")
R6=rows([(None,"ポートセキュリティ：初期1台・アクセスに固定","sticky＝学習したMACを保存",B),(None,"protect／restrict／shutdown（初期値）","捨てる／捨てて記録／err-disable",R),(None,"DHCPスヌーピング→DAI","正規の方向をtrust、その表で偽ARPを遮断",G)]);P6=svg(R6[1]+4,R6[0],"今日のまとめ")
qt=lambda t,c:f'<g>{tag(0,0,t,c,90)}</g>'
pages=[
 {"t":"ポートセキュリティ","svg":p1,"b":"<b>ポートセキュリティ</b>は、ポートにつないでよい機器をMACアドレスで制限する機能です。動的に学習して保存するなら <b>sticky</b>。","p":"「dynamic port」エラー → switchport mode access。"},
 {"t":"違反モード","svg":p2,"b":"","p":"ポートを止めずに記録だけ残す → restrict。"},
 {"t":"DHCPスヌーピング","svg":p3,"b":"<b>DHCPスヌーピング</b>は、信頼しないポートから届くDHCPサーバーの応答（Offer・Ack）を遮断し、偽のDHCPサーバーを防ぎます。","p":"trustにするのは正規のDHCPサーバーがある方向のポート。"},
 {"t":"DAI","svg":p4,"b":"<b>DAI</b>（Dynamic ARP Inspection）は、DHCPスヌーピングのバインディングテーブルを使って偽のARPを遮断します。","p":"信頼できる機器側のポートはtrust。"},
 {"t":"小テスト","quiz":{"q":"ポートセキュリティで、違反したときの動作の初期値は？","o":[["shutdown",qt("shutdown",R)],["restrict",qt("restrict",A)],["protect",qt("protect",G)]],"a":0,"e":"正解は<b>shutdown</b>。ポートがerr-disable状態になります。"}},
 {"t":"今日のまとめ","svg":P6,"b":"次回は「VPN・無線LANのセキュリティ」。","p":"一問一答の「セキュリティの基礎」で確かめましょう。"}]
build(44,"nl43","L2セキュリティ","セキュリティ",SC,L,pages,None)
