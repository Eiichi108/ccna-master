import sys;sys.path.insert(0,'/home/claude/lecture')
from fig import *;from mk import build
T="先生";S="生徒"
L=[
(1,T,"今日は、STPの続きです。速くなったRSTPと、VLANごとに動かすRapid PVST+、そしてSTPを守る機能を学びます。",None),
(1,T,"RSTPは、ラピッドスパニングツリー。従来のSTPより、ずっと速く切り替わります。ポートの状態は、ディスカーディング、ラーニング、フォワーディングの3つです。",None),
(1,S,"従来のSTPにあった、リスニングは？",None),
(1,T,"RSTPにはありません。リスニングは、従来のSTP、802.1Dの状態です。それから、状態と役割は別物なので、区別しましょう。",None),
(1,T,"RSTPのポートの役割は4つ。ルートポート、指定ポート、そして代替ポートとバックアップポートです。",None),
(1,T,"代替ポートは、ルートブリッジへの別の経路で、ルートポートが壊れたらすぐ切り替わる予備です。バックアップポートは、同じスイッチの指定ポートと同じセグメントにある予備で、ハブを使ったときなどに出てきます。",None),
(2,T,"CiscoのRapid PVST+は、VLANごとにRSTPを動かす方式です。spanning-tree mode rapid-pvstで有効にします。",None),
(2,T,"VLANごとにルートブリッジを変えられるので、VLAN10はこちらの線、VLAN20はあちらの線、と負荷を分けて、リンクを有効に使えます。",None),
(2,T,"このスイッチをVLAN10のルートにするなら、spanning-tree vlan 10 root primary。プライオリティが自動で低くなり、普通は24576になります。予備のルートなら、root secondaryで28672です。",None),
(2,T,"手動で設定するなら、プライオリティは0から61440の範囲で、4096の倍数です。8192はOKですが、1000のような数字は設定できません。",None),
(3,T,"では、show spanning-treeの出力の読み方です。表示されるプライオリティは、設定した値に、VLAN番号を足した値です。これを拡張システムIDと言います。",None),
(3,S,"4106と出ていたら、4096にVLAN10を足したもの、ですか？",None),
(3,T,"正解です。逆に24596なら、24576を引いて、VLAN20の出力だと分かります。",None),
(3,T,"Root IDとBridge IDのアドレスが同じなら、そのスイッチがルートブリッジ。違えば、ルートではありません。Roleの、Rootはルートポート、Desgは指定ポート、Altnは代替ポートです。StsのBLKはブロック、FWDは転送中です。",None),
(3,T,"コストからリンクの速さも分かります。19なら100メガ、4なら1ギガです。protocol rstpと書いてあれば、Rapid PVST+で動いています。",None),
(4,T,"最後に、STPを守る機能です。前回のBPDUガードに加えて、3つ紹介します。",None),
(4,T,"ルートガードは、予定外のスイッチがルートブリッジになろうとするのを防ぎます。より優れたBPDUを受け取ると、そのポートをroot-inconsistent状態にしてブロックします。",None),
(4,T,"ループガードは、片方向だけリンクが壊れてBPDUが届かなくなったとき、ブロックしているポートが勝手に転送を始めないようにします。",None),
(4,T,"BPDUガードで止まったポートは、errdisable recovery cause bpduguardで、初期値300秒後に自動で復旧させられます。また、グローバルでspanning-tree portfast defaultと打つと、すべてのアクセスポートでPortFastが有効になります。",None),
(5,T,"ここで小テストです。このスイッチを、VLAN10のルートブリッジにするコマンドはどれでしょう？画面で選んでください。",None),
(5,T,"正解はspanning-tree vlan 10 root primaryです。",None),
(6,T,"では、今日のまとめです。",None),
(6,T,"1つ目。RSTPの状態は、ディスカーディング、ラーニング、フォワーディング。役割は、ルート、指定、代替、バックアップ。",None),
(6,T,"2つ目。Rapid PVST+はVLANごと。root primaryで24576、root secondaryで28672。プライオリティは4096の倍数で、表示はVLAN番号を足した値。",None),
(6,T,"3つ目。ルートガードはroot-inconsistent、ループガードは片方向の故障対策、BPDUガードの復旧はerrdisable recovery。",None),
(6,S,"出力の数字から、VLAN番号まで分かるようになりました！",None),
(6,T,"すごいですね。次回は、線を束ねるEtherChannelです。お疲れさまでした。",None),
]
SC=["RSTPの状態と役割","Rapid PVST+","出力の読み方","STPを守る機能","小テスト","まとめ"]
R1=rows([(None,"状態：Discarding／Learning／Forwarding","Listeningは従来のSTP（802.1D）の状態",B),(None,"ルートポート・指定ポート","ルートへの近道／各リンクに1つ",G),(None,"代替ポート（Alternate）","ルートへの別経路の予備。故障するとすぐ切り替わる",A),(None,"バックアップポート","同じスイッチの指定ポートと同じセグメントの予備",K)]);p1=svg(R1[1]+4,R1[0],"RSTPの状態と役割")
p2=svg(250,"".join([sc(80,40,.8,switch(0,0,B)),lab(80,74,"VLAN 10のルート",12,800,B),sc(280,40,.8,switch(0,0,G)),lab(280,74,"VLAN 20のルート",12,800,G),sc(180,160,.8,switch(0,0)),f'<path d="M96 56L164 144" stroke="{B}" stroke-width="5"/>',f'<path d="M264 56L196 144" stroke="{G}" stroke-width="5"/>',
 lab(180,198,"VLANごとにルートを変えて負荷を分ける",12.5,800),f'<text x="180" y="224" text-anchor="middle" style="font:700 12px {mono};fill:var(--ink)">spanning-tree vlan 10 root primary（24576）</text>',f'<text x="180" y="244" text-anchor="middle" style="font:700 12px {mono};fill:var(--sub)">root secondary（28672）・4096の倍数</text>']),"Rapid PVST+")
p3=svg(270,term(10,10,340,196,[("VLAN0010",B),(" Root ID  Priority 4106",G),(" Bridge ID Priority 4106",G),("Interface Role Sts Cost",K),("Gi0/1     Desg FWD 4",B),("Gi0/2     Altn BLK 19",R),("protocol rstp",A)]).replace("font:700 14px","font:700 13px")+lab(180,232,"4106 ＝ 4096 ＋ VLAN 10（拡張システムID）",12.5,800)+lab(180,254,"Root ID＝Bridge ID → ルートブリッジ／Altn BLK＝代替・ブロック",11.5,700,"var(--sub)"),"show spanning-treeの読み方")
R4=rows([(None,"ルートガード","より優れたBPDUを受けたら root-inconsistent でブロック",R),(None,"ループガード","BPDUが届かなくなっても、ブロック中のポートが勝手に転送しない",B),(None,"errdisable recovery cause bpduguard","BPDUガードで止まったポートを300秒後に自動復旧",A),(None,"spanning-tree portfast default","すべてのアクセスポートでPortFast",G)]);p4=svg(R4[1]+4,R4[0],"STPを守る機能")
R6=rows([(None,"RSTP：Discarding・Learning・Forwarding","役割：ルート・指定・代替・バックアップ",B),(None,"Rapid PVST+：VLANごと","primary 24576／secondary 28672／表示＝設定＋VLAN番号",G),(None,"ルートガード・ループガード・BPDUガード","root-inconsistent／片方向故障／err-disable",R)]);P6=svg(R6[1]+4,R6[0],"今日のまとめ")
qt=lambda t,c:f'<g><text x="0" y="5" text-anchor="middle" style="font:800 9.5px {mono};fill:{c}">{t}</text></g>'
pages=[
 {"t":"RSTPの状態と役割","svg":p1,"b":"<b>RSTP</b>（Rapid Spanning Tree Protocol）は速く切り替わるSTP。リスニングやラーニングは「状態」、ルートや指定は「役割」です。","p":"RSTPに含まれない状態＝Listening。"},
 {"t":"Rapid PVST+","svg":p2,"b":"<b>Rapid PVST+</b>（Per-VLAN Spanning Tree）はVLANごとにRSTPを動かすCisco独自の方式。<b>spanning-tree mode rapid-pvst</b>で有効にします。","p":"プライオリティは0〜61440の4096の倍数（8192はOK）。"},
 {"t":"出力の読み方","svg":p3,"b":"表示されるプライオリティ＝設定値＋VLAN番号。24596なら24576＋20でVLAN 20。コスト19は100Mbps、4は1Gbps。","p":"Root IDとBridge IDが違えば、そのスイッチはルートではない。"},
 {"t":"STPを守る機能","svg":p4,"b":"","p":"予定外のスイッチがルートになるのを防ぐ＝ルートガード。"},
 {"t":"小テスト","quiz":{"q":"このスイッチをVLAN 10のルートブリッジにするコマンドは？","o":[["spanning-tree vlan 10 root primary",qt("vlan 10 root primary",G)],["spanning-tree vlan 10 root secondary",qt("vlan 10 root secondary",B)],["spanning-tree mode rapid-pvst",qt("mode rapid-pvst",K)]],"a":0,"e":"正解は<b>spanning-tree vlan 10 root primary</b>。プライオリティが自動で低い値に設定されます。"}},
 {"t":"今日のまとめ","svg":P6,"b":"次回は「EtherChannel」。","p":"一問一答の「ネットワークアクセス」で確かめましょう。"}]
build(24,"nl23","Rapid PVST+とSTPの保護機能","ネットワークアクセス",SC,L,pages,None)
