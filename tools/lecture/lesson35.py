import sys;sys.path.insert(0,'/home/claude/lecture')
from fig import *;from mk import build
T="先生";S="生徒"
L=[
(1,T,"今日から、IPサービスの分野です。最初は、入門でも少し出てきたNATを、しっかり学びます。",None),
(1,T,"NATは、プライベートIPアドレスを、インターネットで使えるグローバルIPアドレスに変換する仕組みです。",None),
(1,T,"種類は3つ。1つ目、スタティックNAT。1対1で固定して変換します。外から決まったアドレスでアクセスさせたい、公開サーバー向けです。",None),
(1,T,"2つ目、ダイナミックNAT。グローバルアドレスのプールから、順に割り当てます。3つ目、PAT、別名NATオーバーロード。1つのグローバルIPを、ポート番号で区別して、たくさんの端末で共有します。",None),
(1,S,"家のWi-Fiルーターは、PATですか？",None),
(1,T,"その通りです。家の何台もの機器が、1つのグローバルIPを共有していますね。",None),
(2,T,"NATの用語が、試験でよく出ます。insideは社内側、outsideは外部側。localは本当のアドレス、globalは外から見えるアドレスです。",None),
(2,T,"inside localは、社内の端末の、変換前の本当のプライベートアドレス。inside globalは、その端末が外から見えるときの、変換後のアドレスです。outside globalは、外の相手の本当のアドレスです。",None),
(2,S,"insideかoutsideか、localかglobalか、の組み合わせですね。",None),
(3,T,"設定の最初の一歩は、どのインターフェースが社内側か外部側かを決めることです。社内側にip nat inside、外部側にip nat outsideを設定します。",None),
(3,T,"これを忘れると、変換されません。設定漏れの定番です。",None),
(3,T,"スタティックNATは、ip nat inside source static、変換前の社内のアドレス、変換後の公開アドレス、の順です。",None),
(3,T,"PATは、access-listで変換する社内のアドレスを決め、ip nat inside source list 1 interface g0/1 overloadのように、最後にoverloadを付けます。",None),
(3,T,"使えるグローバルIPが3つで、同時接続が15万なら、1つのIPで約6万5千のポートを使えるので、3つのプールにoverloadを付けます。",None),
(4,T,"確認は、show ip nat translationsです。2台のPCが同じグローバルIPを使い、ポート番号で区別されていたら、PATです。",None),
(4,T,"プロトコルやポートの欄がハイフンのエントリは、スタティックNATです。1対1の対応は、通信がなくても常に表示されます。",None),
(5,T,"ここで小テストです。1つのグローバルIPアドレスを多数のPCで共有するNATはどれでしょう？画面で選んでください。",None),
(5,T,"正解は、PAT、NATオーバーロードです。",None),
(6,T,"では、今日のまとめです。",None),
(6,T,"1つ目。スタティックは1対1で公開サーバー向け、ダイナミックはプールから、PATはポート番号で1つのIPを共有。",None),
(6,T,"2つ目。inside localは社内の本当のアドレス、inside globalは外から見えるアドレス。",None),
(6,T,"3つ目。最初にip nat insideとoutsideを設定。PATはoverload。確認はshow ip nat translations。",None),
(6,S,"insideとoutside、忘れないようにします！",None),
(6,T,"いいですね。次回は、DHCP、DNS、NTPを学びます。お疲れさまでした。",None),
]
SC=["NATの種類","NATの用語","設定","変換表の読み方","小テスト","まとめ"]
R1=rows([(None,"スタティックNAT","1対1で固定。公開サーバー向け",B),(None,"ダイナミックNAT","アドレスプールから順に割り当て",G),(None,"PAT（NATオーバーロード）","1つのグローバルIPをポート番号で区別して共有",A)]);p1=svg(R1[1]+4,R1[0],"NATの種類")
p2=svg(250,"".join([sc(50,70,.7,pc(0,0)),lab(50,102,"社内PC",12),sc(180,70,.8,router(0,0)),lab(180,108,"NATルーター",12),cloud(300,70,"var(--sub)",.7),sc(300,140,.6,server(0,0)),lab(300,176,"外の相手",12),'<path d="M74 70h70M216 70h44" stroke="var(--ink)" stroke-width="3"/>',
 lab(110,52,"inside",12,800,B),lab(250,52,"outside",12,800,R),
 tag(70,140,"inside local",B,110),lab(70,162,"192.168.1.10（本当）",11,700,"var(--sub)"),tag(180,196,"inside global",G,110),lab(180,218,"203.0.113.5（外から見える）",11,700,"var(--sub)"),tag(300,214,"outside global",R,116),lab(300,236,"相手の本当のアドレス",11,700,"var(--sub)")]),"NATの用語")
p3=svg(260,term(10,10,340,190,[("interface g0/0",B),(" ip nat inside",B),("interface g0/1",R),(" ip nat outside",R),("access-list 1 permit 192.168.1.0 0.0.0.255",K),("ip nat inside source list 1",G),("   interface g0/1 overload",G)]).replace("font:700 14px","font:700 11.5px")+lab(180,226,"まず inside／outside。PATは最後に overload",13,800)+lab(180,248,"スタティック：ip nat inside source static 変換前 変換後",11.5,700,"var(--sub)"),"NATの設定")
p4=svg(230,term(10,10,340,124,[("R1# show ip nat translations",G),("Pro Inside global     Inside local",K),("tcp 203.0.113.5:1025 192.168.1.10:1025",B),("tcp 203.0.113.5:1026 192.168.1.11:1026",B)]).replace("font:700 14px","font:700 10.5px")+lab(180,160,"同じグローバルIP＋違うポート → PAT",13,800,"#b77d00")+lab(180,186,"プロトコル・ポートが「---」→ スタティックNAT",13,800,B)+lab(180,210,"スタティックの対応は通信がなくても常に表示",11.5,700,"var(--sub)"),"NAT変換表の読み方")
R6=rows([(None,"スタティック・ダイナミック・PAT","1対1／プール／ポートで共有",B),(None,"inside local＝本当、inside global＝外から見える","outside global＝相手の本当のアドレス",G),(None,"ip nat inside／outside → overload","確認：show ip nat translations",A)]);P6=svg(R6[1]+4,R6[0],"今日のまとめ")
qt=lambda t,c:f'<g>{tag(0,0,t,c,90)}</g>'
pages=[
 {"t":"NATの種類","svg":p1,"b":"<b>NAT</b>（Network Address Translation）は、プライベートIPアドレスをグローバルIPアドレスに変換する仕組みです。","p":"家庭のWi-FiルーターはPAT。"},
 {"t":"NATの用語","svg":p2,"b":"inside＝社内側、outside＝外部側。local＝本当のアドレス、global＝外から見えるアドレス。","p":"社内PCの変換前のアドレス＝inside local。"},
 {"t":"設定","svg":p3,"b":"NAT設定の最初のステップは、内部・外部のインターフェースを定義すること。並び順は「変換前（社内）→ 変換後（公開用）」。","p":"PAT1つで約65,000ポート。15万接続 → 3つのアドレスのプール＋overload。"},
 {"t":"変換表の読み方","svg":p4,"b":"","p":"変換されない → ip nat inside/outside の設定漏れを疑う。"},
 {"t":"小テスト","quiz":{"q":"1つのグローバルIPアドレスを多数のPCで共有するNATは？","o":[["PAT（NATオーバーロード）",qt("PAT",A)],["スタティックNAT",qt("スタティック",B)],["ダイナミックNAT",qt("ダイナミック",G)]],"a":0,"e":"正解は<b>PAT</b>。ポート番号で区別して1つのIPを共有します。"}},
 {"t":"今日のまとめ","svg":P6,"b":"次回は「DHCP・DNS・NTP」。","p":"一問一答の「IPサービス」で確かめましょう。"}]
build(35,"nl34","NAT / PAT","IPサービス",SC,L,pages,None)
