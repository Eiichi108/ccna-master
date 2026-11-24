import sys;sys.path.insert(0,'/home/claude/lecture')
from fig import *;from mk import build
T="先生";S="生徒"
L=[
(1,T,"今日は、OSPFの続きです。ネットワークタイプと、ネイバーの状態を学びます。出力を読む問題が多いので、表示の意味を押さえましょう。",None),
(1,T,"ネットワークタイプは、主に2つ。broadcastとpoint-to-pointです。",None),
(1,T,"broadcastは、イーサネットの初期値です。たくさんのルーターがつながる前提なので、DRとBDRを選びます。HelloとDeadは10秒と40秒です。",None),
(1,T,"point-to-pointは、シリアル回線の初期値です。2台しかいないので、DRとBDRを選びません。",None),
(1,S,"ルーター2台だけを、イーサネットでつないだときは？",None),
(1,T,"初期値はbroadcastなので、DRの選出のために待ち時間がかかります。そこで、ip ospf network point-to-pointを設定すると、選出がなくなり、すぐにFullになります。",None),
(1,T,"DRとBDRが選ばれるのは、broadcastと、non-broadcast、NBMAの2つです。",None),
(2,T,"次は、ネイバーの状態です。Down、Init、2-Way、ExStart、Exchange、Loading、そしてFullと進みます。",None),
(2,T,"Fullは、データベースの交換が終わって、完全に同期した状態です。",None),
(2,T,"大事なのは、DR、BDRとは、Fullになりますが、DROTHERどうしは2-Wayで止まることです。これは正常です。",None),
(2,S,"2-Wayで止まっていても、故障じゃないんですね。",None),
(2,T,"そうです。Helloの役割は、ネイバーを見つけて、関係を保ち、DRとBDRを選ぶことです。経路の情報そのものは、LSAでやりとりします。Helloでルーティングテーブル全体を送るわけではありません。",None),
(3,T,"では出力を読みます。show ip ospf neighborで、R1のネイバーが、2.2.2.2がFULL/DR、3.3.3.3が2WAY/DROTHERと出ていたら、R1の役割は何でしょう？",None),
(3,S,"DROTHERと2-Wayだから、R1もDROTHERですか？",None),
(3,T,"正解です。もしR1がBDRなら、DROTHERともFullになるはずですからね。",None),
(3,T,"FULLのあとが、ハイフンになっていたら、point-to-pointで、DRとBDRを選んでいない、という意味です。show ip ospf interfaceで、StateがP2Pなら、point-to-pointです。",None),
(3,T,"StateがDRで、Designated Routerが自分のIDなら、自分がDRです。Adjacent neighbor countは、Fullになっている相手の数です。DRなら、ほかの全部のルーターとFullになります。",None),
(4,T,"最後に、便利な設定を3つ。passive-interfaceは、Helloを送らなくする設定です。PCしかつながっていないポートに設定します。そのネットワークの経路は、ちゃんと広告され続けます。",None),
(4,T,"default-information originateは、デフォルトルートをOSPFで配る設定。auto-cost reference-bandwidthは、前回の、参照帯域幅を大きくする設定です。",None),
(4,T,"マルチキャストアドレスは、224.0.0.5がOSPFルーター全員、224.0.0.6がDRとBDR宛てです。",None),
(5,T,"ここで小テストです。DROTHERどうしのネイバーの状態として、正常なものはどれでしょう？画面で選んでください。",None),
(5,T,"正解は2-Wayです。",None),
(6,T,"では、今日のまとめです。",None),
(6,T,"1つ目。イーサネットはbroadcastでDRとBDRあり、シリアルはpoint-to-pointでなし。2台だけのイーサネットはpoint-to-pointにすると速い。",None),
(6,T,"2つ目。状態は、Down、Init、2-Way、ExStart、Exchange、Loading、Full。DROTHERどうしは2-Wayが正常。",None),
(6,T,"3つ目。FULLのあとのハイフンはpoint-to-point。passive-interfaceはHelloを止めても経路は広告する。",None),
(6,S,"出力の読み方、自信がついてきました！",None),
(6,T,"いいですね。次回は、デフォルトゲートウェイを冗長化するFHRPを学びます。お疲れさまでした。",None),
]
SC=["ネットワークタイプ","ネイバーの状態","出力を読む","便利な設定","小テスト","まとめ"]
R1=rows([(None,"broadcast（イーサネットの初期値）","DR/BDRあり・Hello 10秒/Dead 40秒",B),(None,"point-to-point（シリアルの初期値）","DR/BDRなし。2台だけのイーサネットにも設定 → すぐFull",G),(None,"ip ospf network point-to-point","インターフェースで設定",A),(None,"DR/BDRが選ばれるタイプ","broadcast と non-broadcast（NBMA）",K)]);p1=svg(R1[1]+4,R1[0],"OSPFのネットワークタイプ")
st=["Down","Init","2-Way","ExStart","Exchange","Loading","Full"]
p2=svg(220,"".join(f'<rect x="{8+k*50}" y="30" width="46" height="40" rx="6" fill="{G if k==6 else (A if k==2 else "#e8ecf2")}" opacity="{.8 if k in (2,6) else 1}"/><text x="{31+k*50}" y="55" text-anchor="middle" style="font:800 9.5px sans-serif;fill:{"#fff" if k in (2,6) else "var(--ink)"}">{s}</text>' for k,s in enumerate(st))+lab(180,100,"DR・BDRとは Full",13.5,800,G)+lab(180,126,"DROTHERどうしは 2-Way（正常）",13.5,800,"#b77d00")+lab(180,160,"Hello：ネイバーの発見と維持・DR/BDRの選出",12.5,700)+lab(180,182,"経路の情報はLSAでやりとり（Helloではない）",12.5,700,"var(--sub)"),"ネイバーの状態")
p3=svg(270,term(10,10,340,144,[("R1# show ip ospf neighbor",G),("Neighbor ID  State",K),("2.2.2.2      FULL/DR",B),("3.3.3.3      2WAY/DROTHER",A),("4.4.4.4      FULL/ -",R)]).replace("font:700 14px","font:700 12.5px")+lab(180,178,"DROTHERと2WAY → R1もDROTHER",12.5,800,"#b77d00")+lab(180,200,"FULL/ - → point-to-point（DR/BDRなし）",12.5,800,R)+lab(180,226,"show ip ospf interface：State P2P／DR",12,700,"var(--sub)")+lab(180,248,"Adjacent neighbor count＝Fullの相手の数",12,700,"var(--sub)"),"OSPFの出力を読む")
R4=rows([(None,"passive-interface g0/1","Helloを送らない。そのネットワークの経路は広告し続ける",B),(None,"default-information originate","デフォルトルートをOSPFで配る",G),(None,"auto-cost reference-bandwidth","1Gbpsと10Gbpsのコストを区別",A),(None,"224.0.0.5／224.0.0.6","OSPFルーター全部／DR・BDR",K)]);p4=svg(R4[1]+4,R4[0],"便利な設定")
R6=rows([(None,"broadcast＝DR/BDRあり／P2P＝なし","2台だけのイーサネットはP2Pで速く",B),(None,"Down→Init→2-Way→…→Full","DROTHERどうしは2-Wayが正常",A),(None,"FULL/ - ＝ point-to-point","passive-interface＝Helloを止めても経路は広告",G)]);P6=svg(R6[1]+4,R6[0],"今日のまとめ")
qt=lambda t,c:f'<g>{tag(0,0,t,c,80)}</g>'
pages=[
 {"t":"ネットワークタイプ","svg":p1,"b":"ギガビットイーサネットをOSPFでアドバタイズすると、初期値は<b>broadcast</b>。クロスケーブルで2台を直結しているなら<b>point-to-point</b>にすると、DR/BDRの選出がなくなりすぐFullになります。","p":"point-to-point＝相手と直接Full。"},
 {"t":"ネイバーの状態","svg":p2,"b":"Fullはデータベースの交換が終わって同期した状態です。","p":"DROTHERどうしの2-Wayは故障ではない。"},
 {"t":"出力を読む","svg":p3,"b":"R1がBDRならDROTHERともFullになるはずなので、2WAYならR1もDROTHERです。","p":"DRは、ほかのすべてのルーターとFullになる。"},
 {"t":"便利な設定","svg":p4,"b":"","p":"PCしかつながっていないポート → passive-interface。"},
 {"t":"小テスト","quiz":{"q":"DROTHERどうしのOSPFのネイバーの状態として正常なものは？","o":[["2-Way",qt("2-Way",A)],["Full",qt("Full",G)],["Init",qt("Init",K)]],"a":0,"e":"正解は<b>2-Way</b>。DROTHERどうしは2-Wayで止まり、DR/BDRとはFullになります。"}},
 {"t":"今日のまとめ","svg":P6,"b":"次回は「FHRP（デフォルトゲートウェイの冗長化）」。","p":"一問一答の「IP接続」で確かめましょう。"}]
build(33,"nl32","OSPFのネットワークタイプと状態","IP接続",SC,L,pages,None)
