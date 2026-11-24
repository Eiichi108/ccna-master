import sys;sys.path.insert(0,'/home/claude/lecture')
from fig import *;from mk import build
T="先生";S="生徒"
L=[
(1,T,"前回、VLANが違えば別のネットワークなので、つなぐにはL3の機器が必要、と学びました。今日はその方法、VLAN間ルーティングです。",None),
(1,T,"方法は2つ。ルーターを使うルーターオンアスティックと、L3スイッチのSVIを使う方法です。",None),
(2,T,"ルーターオンアスティックは、ルーターの1つの物理ポートを、サブインターフェースという仮想のポートに分けて、VLANごとのゲートウェイにします。",None),
(2,S,"1本のケーブルで、全部のVLANをルーティングするんですか？",None),
(2,T,"そうです。だから、スイッチ側の、ルーターにつなぐポートはトランクにします。ここをアクセスポートにしてしまうと、1つのVLANしか届きません。",None),
(2,T,"設定は3点セットです。1つ目、interface g0/0.10のように、サブインターフェースを作る。2つ目、encapsulation dot1Q 10で、VLAN10のタグを扱うと決める。3つ目、IPアドレスを付ける。",None),
(2,T,"ネイティブVLANのサブインターフェースには、encapsulation dot1Q 1 nativeのように、nativeを付けます。タグなしのフレームを、そこで受け取ります。",None),
(2,S,"VLAN20なら、interface e0/0.20、encapsulation dot1q 20、ip addressの3つですね。",None),
(2,T,"完璧です。1つでも欠けると動きません。",None),
(3,T,"2つ目の方法は、L3スイッチのSVIです。SVIは、スイッチの中に作る、VLANごとの仮想インターフェースです。",None),
(3,T,"interface vlan 10と打ってIPアドレスを付けると、それがVLAN10のゲートウェイになります。そして、ip routingでルーティングを有効にします。",None),
(3,S,"SVIを作ったのに、down、downのままのときは？",None),
(3,T,"そのVLANが存在して、そのVLANに、upしたポートか、そのVLANを通すトランクが1つ以上ないと、SVIはupしません。VLAN30にポートが1つもなければ、downのままです。",None),
(3,T,"また、L3スイッチのポートは、no switchportで、ルーターのポートのようにIPアドレスを直接付ける、ルーテッドポートにもできます。",None),
(4,T,"ここで小テストです。サブインターフェースで、VLAN10の802.1Qタグを扱うためのコマンドはどれでしょう？画面で選んでください。",None),
(4,T,"正解はencapsulation dot1Q 10です。",None),
(5,T,"では、今日のまとめです。",None),
(5,T,"1つ目。ルーターオンアスティックは、サブインターフェース、encapsulation dot1Q、IPアドレスの3点セット。スイッチ側はトランク。ネイティブはnative。",None),
(5,T,"2つ目。SVIは、interface vlanにIPアドレス、そしてip routing。VLANにupしたポートがないとupしない。",None),
(5,T,"3つ目。no switchportで、ルーテッドポート。",None),
(5,S,"3点セット、覚えやすいです！",None),
(5,T,"よかったです。次回は、音声VLANと、機器を管理する方法を学びます。お疲れさまでした。",None),
]
SC=["2つの方法","ルーターオンアスティック","SVI（L3スイッチ）","小テスト","まとめ"]
p1=svg(200,"".join([f'<rect x="10" y="10" width="164" height="180" rx="12" fill="{R}" opacity=".08"/>',lab(92,34,"ルーターオンアスティック",13,800,R),sc(92,76,.8,router(0,0)),f'<path d="M92 96v30" stroke="var(--ink)" stroke-width="5"/>',lab(124,116,"トランク",11,800,"var(--sub)"),sc(92,146,.7,switch(0,0)),lab(92,180,"1本で全VLAN",12,700,"var(--sub)"),
 f'<rect x="186" y="10" width="164" height="180" rx="12" fill="#8a3ffc" opacity=".08"/>',lab(268,34,"SVI（L3スイッチ）",13,800,"#8a3ffc"),sc(268,90,.9,switch(0,0,"#8a3ffc")),lab(268,130,"interface vlan 10",11.5,800),lab(268,148,"interface vlan 20",11.5,800),lab(268,180,"＋ ip routing",12,800,"#8a3ffc")]),"VLAN間ルーティングの2つの方法")
p2=svg(250,term(10,10,340,166,[("R1(config)# interface g0/0.10",B),("R1(config-subif)# encapsulation dot1Q 10",B),("R1(config-subif)# ip address 10.10.10.1 255.255.255.0",B),("R1(config)# interface g0/0.20",G),("R1(config-subif)# encapsulation dot1Q 20",G),("R1(config-subif)# ip address 10.20.20.1 255.255.255.0",G)]).replace("font:700 14px","font:700 10.5px")+lab(180,198,"サブインターフェース＋dot1Q＋IP の3点セット",13,800)+lab(180,222,"ネイティブ：encapsulation dot1Q 1 native／スイッチ側はトランク",11.5,700,"var(--sub)"),"ルーターオンアスティックの設定")
R3=rows([(None,"interface vlan 10 ＋ ip address","VLAN 10のゲートウェイになる仮想インターフェース",'#8a3ffc'),(None,"ip routing","L3スイッチでルーティングを有効にする",B),(None,"SVIが down/down","VLANが存在し、upしたポート（またはトランク）が1つ以上必要",R),(None,"no switchport","ルーテッドポート（IPを直接付ける）",K)]);p3=svg(R3[1]+4,R3[0],"SVIの設定と注意点")
R5=rows([(None,"ROAS：サブIF＋encapsulation dot1Q＋IP","スイッチ側はトランク、ネイティブは native",R),(None,"SVI：interface vlan＋ip routing","VLANにupしたポートがないとupしない",'#8a3ffc'),(None,"no switchport","ルーテッドポート",K)]);P5=svg(R5[1]+4,R5[0],"今日のまとめ")
qt=lambda t,c:f'<g><text x="0" y="5" text-anchor="middle" style="font:800 10px {mono};fill:{c}">{t}</text></g>'
pages=[
 {"t":"VLAN間ルーティングの2つの方法","svg":p1,"b":"違うVLANどうしをつなぐには、<b>ルーターオンアスティック</b>（ROAS：Router on a Stick）か、L3スイッチの<b>SVI</b>（Switch Virtual Interface）を使います。","p":"どちらも、VLANごとにゲートウェイを用意する。"},
 {"t":"ルーターオンアスティック","svg":p2,"b":"ルーターの1つの物理ポートを<b>サブインターフェース</b>に分け、VLANごとのゲートウェイにします。スイッチ側のルーターにつなぐポートは<b>トランク</b>（switchport mode trunk）にします。","p":"1つでも欠けるとNG。"},
 {"t":"SVI（L3スイッチ）","svg":p3,"b":"L3スイッチでは、VLANごとのSVIにIPアドレスを付け、<b>ip routing</b>でルーティングを有効にします。","p":"VLAN 30にポートがない → interface vlan 30 は down/down のまま。"},
 {"t":"小テスト","quiz":{"q":"サブインターフェースで、VLAN 10の802.1Qタグを扱うためのコマンドは？","o":[["encapsulation dot1Q 10",qt("encapsulation dot1Q 10",B)],["switchport access vlan 10",qt("switchport access vlan 10",G)],["interface vlan 10",qt("interface vlan 10",'#8a3ffc')]],"a":0,"e":"正解は<b>encapsulation dot1Q 10</b>。サブインターフェースでVLAN 10のタグ付きフレームを扱えるようになります。"}},
 {"t":"今日のまとめ","svg":P5,"b":"次回は「音声VLAN・管理アクセス」。","p":"一問一答の「ネットワークアクセス」で確かめましょう。"}]
build(21,"nl20","VLAN間ルーティング（ルーターオンアスティック・SVI）","ネットワークアクセス",SC,L,pages,None)
