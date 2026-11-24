import sys;sys.path.insert(0,'/home/claude/lecture')
from fig import *;from mk import build
T="先生";S="生徒"
L=[
(1,T,"今日は、ネットワークを見張る2つの仕組み、SNMPとSyslogを学びます。",None),
(1,T,"SNMPは、機器を監視・管理するプロトコルです。管理サーバーをマネージャー、監視される機器をエージェントと言います。",None),
(1,T,"エージェントは、CPUの使い方やインターフェースの状態などの管理情報を、MIBという形で持っています。MIBの1つ1つは、OIDという番号で整理されています。",None),
(1,T,"多くの機器の設定を、管理ツールからまとめて取得して、バックアップするのにも使えます。",None),
(2,T,"情報の集め方は2つ。ポーリングは、マネージャーから機器に、調子はどう、と定期的に聞きに行く方法です。",None),
(2,T,"Trapは、何かが起きたときに、機器のほうから、大変です、と知らせるプッシュ型の通知です。送りっぱなしで、届いたかは確かめません。",None),
(2,T,"Informは、マネージャーが受け取ったよ、と返事をする通知です。確認応答があるので、Trapより信頼性が高いです。",None),
(2,S,"誰から始めるかが、ポーリングとTrapで逆なんですね。",None),
(3,T,"バージョンも大事です。v1とv2cは、コミュニティ名というパスワードのようなものを、平文で送ります。盗み見られる危険があります。",None),
(3,T,"認証と暗号化ができるのは、SNMPv3だけです。最高のセキュリティで監視したいなら、v3を選びます。",None),
(4,T,"次はSyslog。機器のログを、Syslogサーバーに送って保存する仕組みです。ログには、重大度レベルが0から7まであります。",None),
(4,T,"0がEmergency、1がAlert、2がCritical、3がError、4がWarning、5がNotification、6がInformational、7がDebuggingです。数字が小さいほど深刻です。",None),
(4,S,"8つも覚えられるかな…",None),
(4,T,"英語の頭文字で、Every Awesome Cisco Engineer Will Need Ice cream Dailyと覚えます。インターフェースのアップダウンのような出来事は、5のNotificationです。",None),
(5,T,"ログの形は、パーセント、ファシリティ、重大度、ニーモニックです。%LINK-3-UPDOWNなら、LINKがファシリティ、つまりログを出した機能やプロセス。3が重大度でError。UPDOWNが短い名前です。",None),
(5,T,"logging trapで、Syslogサーバーに送るレベルを決めます。指定したレベルと、それより深刻な、数字の小さいレベルが送られます。logging trap warningsなら、0から4です。",None),
(5,T,"デバッグのログが多すぎて困るときは、informational、つまり6にすれば、7のデバッグだけを止められます。",None),
(6,T,"ここで小テストです。Syslogで最も深刻な重大度レベルはどれでしょう？画面で選んでください。",None),
(6,T,"正解は0、Emergencyです。",None),
(7,T,"では、今日のまとめです。",None),
(7,T,"1つ目。SNMPは、マネージャーがエージェントのMIBを取得する。ポーリングはマネージャーから、Trapは機器から、Informは確認応答つき。",None),
(7,T,"2つ目。認証と暗号化はSNMPv3だけ。v2cのコミュニティ名は平文。",None),
(7,T,"3つ目。Syslogは0から7、小さいほど深刻。指定したレベル以下の数字が送られる。ファシリティはログを出したプロセス。",None),
(7,S,"Every Awesome Cisco Engineer、覚えました！",None),
(7,T,"いいですね。次回は、QoS、SSH、ファイル転送を学びます。お疲れさまでした。",None),
]
SC=["SNMPとは","ポーリングとTrap","SNMPのバージョン","Syslogの重大度","ログの形とlogging trap","小テスト","まとめ"]
p1=svg(200,"".join([sc(60,70,.8,server(0,0)),lab(60,108,"マネージャー",12.5),sc(280,70,.8,router(0,0)),lab(280,108,"エージェント（機器）",12.5),'<path d="M90 70h154" stroke="var(--ink)" stroke-width="3"/>',f'<rect x="240" y="122" width="80" height="30" rx="6" fill="{A}" opacity=".25"/>',lab(280,142,"MIB（OID）",12,800),
 lab(180,180,"CPU・インターフェースの状態などを取得／設定のバックアップにも",11.5,700,"var(--sub)")]),"SNMPのしくみ")
p2=svg(220,"".join([sc(50,40,.7,server(0,0)),lab(50,72,"マネージャー",11.5),sc(310,40,.7,router(0,0)),lab(310,72,"機器",11.5),arrow(80,40,284,40,B),lab(180,32,"ポーリング：マネージャーから聞く",12,800,B),
 arrow(284,100,80,100,R),lab(180,92,"Trap：機器から通知（送りっぱなし）",12,800,R),arrow(284,150,80,150,G),lab(180,142,"Inform：機器から通知",12,800,G),arrow(80,172,284,172,G,2),lab(180,192,"確認応答あり → 信頼性が高い",11.5,700,G)]),"ポーリング・Trap・Inform")
R3=rows([(None,"v1・v2c","コミュニティ名を平文で送る → 盗み見られる",R),(None,"SNMPv3","認証と暗号化に対応（最高のセキュリティ）",G)]);p3=svg(R3[1]+4,R3[0],"SNMPのバージョン")
lv=[("0","Emergency","緊急"),("1","Alert","警報"),("2","Critical","重大"),("3","Error","エラー"),("4","Warning","警告"),("5","Notification","通知"),("6","Informational","情報"),("7","Debugging","デバッグ")]
p4=svg(290,"".join(f'<rect x="10" y="{8+k*34}" width="340" height="30" rx="6" fill="{R if k<3 else (A if k<5 else B)}" opacity="{.25-k*.02}"/>'+num(30,28+k*34,n,"var(--ink)",15)+lab(54,28+k*34,e,13,800,"var(--ink)","start")+lab(336,28+k*34,j,12.5,700,"var(--sub)","end") for k,(n,e,j) in enumerate(lv)),"Syslogの重大度レベル")
p5=svg(230,"".join([f'<text x="180" y="40" text-anchor="middle" style="font:800 17px {mono}"><tspan fill="var(--ink)">%</tspan><tspan fill="{B}">LINK</tspan><tspan fill="var(--ink)">-</tspan><tspan fill="{R}">3</tspan><tspan fill="var(--ink)">-</tspan><tspan fill="{G}">UPDOWN</tspan></text>',lab(116,66,"ファシリティ",12,800,B),lab(172,86,"重大度",12,800,R),lab(236,66,"ニーモニック",12,800,G),lab(180,110,"ファシリティ＝ログを出した機能・プロセス",12.5,800),
 '<path d="M10 128h340" stroke="var(--line)" stroke-width="2"/>',f'<text x="180" y="156" text-anchor="middle" style="font:800 14px {mono};fill:var(--ink)">logging trap warnings</text>',lab(180,180,"→ 0〜4 を送る（指定したレベル以下の数字）",13,800,"#b77d00"),lab(180,206,"デバッグを止めたい → informational（6）",12.5,700,"var(--sub)")]),"ログの形とlogging trap")
R7=rows([(None,"SNMP：マネージャーがエージェントのMIBを取得","ポーリング＝聞く／Trap＝通知／Inform＝確認つき",B),(None,"認証・暗号化はSNMPv3だけ","v2cのコミュニティ名は平文",G),(None,"Syslog 0〜7、小さいほど深刻","UP/DOWN＝5 Notification",A)]);P7=svg(R7[1]+4,R7[0],"今日のまとめ")
qt=lambda t,c:f'<g>{tag(0,0,t,c,100)}</g>'
pages=[
 {"t":"SNMPとは","svg":p1,"b":"<b>SNMP</b>（Simple Network Management Protocol）で、マネージャーがエージェントの<b>MIB</b>（Management Information Base）を取得します。","p":"20台のルーターの設定をまとめてバックアップ → SNMP。"},
 {"t":"ポーリングとTrap","svg":p2,"b":"<b>Trap</b>は機器が始めるプッシュ型、<b>ポーリング</b>はサーバーが始めます。<b>Inform</b>はマネージャーからの確認応答があるので信頼性が高い。","p":"主語が逆になっている選択肢に注意。"},
 {"t":"SNMPのバージョン","svg":p3,"b":"","p":"最高のセキュリティでの監視 → SNMPv3。"},
 {"t":"Syslogの重大度","svg":p4,"b":"数字が小さいほど深刻。覚え方：「<b>E</b>very <b>A</b>wesome <b>C</b>isco <b>E</b>ngineer <b>W</b>ill <b>N</b>eed <b>I</b>ce cream <b>D</b>aily」。","p":"インターフェースのUP/DOWN＝5（通知）。"},
 {"t":"ログの形とlogging trap","svg":p5,"b":"%OSPF-5-ADJCHG なら、OSPFがファシリティ（発生元）、5（Notification）が重大度です。","p":"指定したレベル＋それより深刻なレベルが送られる。"},
 {"t":"小テスト","quiz":{"q":"Syslogで最も深刻な重大度レベルは？","o":[["0 Emergency",qt("0",R)],["7 Debugging",qt("7",B)],["4 Warning",qt("4",A)]],"a":0,"e":"正解は<b>0 Emergency</b>。数字が小さいほど深刻です。"}},
 {"t":"今日のまとめ","svg":P7,"b":"次回は「QoS・SSH・ファイル転送」。","p":"一問一答の「IPサービス」で確かめましょう。"}]
build(37,"nl36","SNMP・Syslog","IPサービス",SC,L,pages,None)
