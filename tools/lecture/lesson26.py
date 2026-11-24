import sys;sys.path.insert(0,'/home/claude/lecture')
from fig import *;from mk import build
T="先生";S="生徒"
L=[
(1,T,"今日は短めの回です。隣につながっている機器の情報を教え合う、CDPとLLDPを学びます。",None),
(1,T,"どちらも、機器の名前、IPアドレス、機種、どのポートでつながっているかなどを、隣の機器に知らせるプロトコルです。",None),
(1,S,"ケーブルをたどらなくても、何がつながっているか分かるんですね。",None),
(2,T,"CDPはCisco独自で、Cisco機器では最初から有効です。60秒ごとに送られ、180秒届かないと情報が消えます。",None),
(2,T,"確認は、show cdp neighborsです。detailを付けると、隣の機器のIPアドレスや、IOSのバージョンまで表示されます。",None),
(2,T,"LLDPは、IEEE 802.1ABの標準規格です。Cisco以外の機器ともやりとりできますが、Cisco機器では最初は無効なので、lldp runで有効にします。確認はshow lldp neighborsです。",None),
(3,T,"出力の読み方が、試験によく出ます。show cdp neighborsには、Local IntrfceとPort IDという2つの欄があります。",None),
(3,T,"Local Intrfceは自分側のポート、Port IDは相手側のポートです。SW1で見て、Device IDがR1、Port IDがGig 0/0/0なら、R1のGig 0/0/0がSW1につながっています。",None),
(3,S,"Localが自分、Port IDが相手、ですね。",None),
(4,T,"最後に注意点。CDPには、機器名やIOSのバージョンなど、攻撃者が喜ぶ情報が入っています。だから、インターネットなど信頼できない相手とつながるポートでは、CDPを止めておきます。",None),
(5,T,"ここで小テストです。LLDPについて正しい説明はどれでしょう？画面で選んでください。",None),
(5,T,"正解は、IEEE標準で、Cisco機器では初期状態で無効、です。",None),
(6,T,"では、今日のまとめです。",None),
(6,T,"1つ目。CDPはCisco独自で最初から有効、60秒ごとに送って180秒で消える。LLDPはIEEE標準で、Ciscoではlldp runで有効にする。",None),
(6,T,"2つ目。detailでIPアドレスやバージョンまで見える。Local Intrfceは自分、Port IDは相手のポート。",None),
(6,T,"3つ目。外部とつながるポートでは、情報漏れを防ぐためにCDPを止める。",None),
(6,S,"短いけど、出力の読み方がよく分かりました！",None),
(6,T,"よかったです。次回は、無線LANの構成を学びます。お疲れさまでした。",None),
]
SC=["隣の機器を知る","CDPとLLDP","出力の読み方","セキュリティの注意","小テスト","まとめ"]
p1=svg(180,"".join([sc(70,70,.9,router(0,0)),lab(70,110,"R1",13),sc(290,70,.9,switch(0,0)),lab(290,110,"SW1",13),'<path d="M106 70h150" stroke="var(--ink)" stroke-width="3"/>',
 arrow(110,52,250,52,B),arrow(250,90,110,90,G),lab(180,44,"機器名・IP・機種・ポート",12,800,B),lab(180,152,"ケーブルをたどらなくても、つながっている相手が分かる",12.5,800)]),"CDP/LLDPで隣の機器を知る")
R2=rows([(None,"CDP（Cisco独自）","初期状態で有効。60秒ごとに送信、180秒で消える",B),(None,"show cdp neighbors (detail)","detailでIPアドレスやIOSのバージョンまで",B),(None,"LLDP（IEEE 802.1AB）","Ciscoでは初期状態で無効 → lldp run",G),(None,"show lldp neighbors","LLDPで見つけた隣の機器の一覧",G)]);p2=svg(R2[1]+4,R2[0],"CDPとLLDP")
p3=svg(220,term(10,10,340,104,[("SW1# show cdp neighbors",G),("Device ID Local Intrfce Port ID",K),("R1        Gig 0/1      Gig 0/0/0",B)]).replace("font:700 14px","font:700 13px")+lab(180,140,"Local Intrfce＝自分（SW1）側のポート",13,800,B)+lab(180,164,"Port ID＝相手（R1）側のポート",13,800,G)+lab(180,196,"→ R1のGig 0/0/0がSW1につながっている",13,800),"show cdp neighborsの読み方")
R4=rows([(None,"外部とつながるポートではCDPを止める","機器名やIOSのバージョンが漏れるのを防ぐ",R)]);p4=svg(R4[1]+4,R4[0],"セキュリティの注意")
R6=rows([(None,"CDP＝Cisco独自・初期有効","60秒ごと・180秒で消える",B),(None,"LLDP＝IEEE標準・Ciscoでは初期無効","lldp run で有効",G),(None,"Local Intrfce＝自分、Port ID＝相手","外部向けポートではCDPを止める",A)]);P6=svg(R6[1]+4,R6[0],"今日のまとめ")
qt=lambda t,c:f'<g>{tag(0,0,t,c,100)}</g>'
pages=[
 {"t":"隣の機器を知る","svg":p1,"b":"<b>CDP</b>（Cisco Discovery Protocol）と<b>LLDP</b>（Link Layer Discovery Protocol）は、隣につながっている機器の情報を教え合うプロトコルです。","p":"機器名・IPアドレス・機種・ポートが分かる。"},
 {"t":"CDPとLLDP","svg":p2,"b":"","p":"CDPの送信間隔60秒、保持時間180秒。"},
 {"t":"出力の読み方","svg":p3,"b":"","p":"Port IDは相手側のポート。"},
 {"t":"セキュリティの注意","svg":p4,"b":"CDPの情報は攻撃のヒントになるので、信頼できない相手とつながるポートでは無効にします。","p":"interface で no cdp enable。"},
 {"t":"小テスト","quiz":{"q":"LLDPについて正しい説明は？","o":[["IEEE標準で、Cisco機器では初期状態で無効",qt("IEEE標準",G)],["Cisco独自で、初期状態で有効",qt("Cisco独自",B)],["IPアドレスを配るプロトコル",qt("アドレス配布",K)]],"a":0,"e":"正解は<b>IEEE標準で、Cisco機器では初期状態で無効</b>。lldp run で有効にします。"}},
 {"t":"今日のまとめ","svg":P6,"b":"次回は「無線LANの構成」。","p":"一問一答の「ネットワークアクセス」で確かめましょう。"}]
build(26,"nl25","CDP / LLDP","ネットワークアクセス",SC,L,pages,None)
