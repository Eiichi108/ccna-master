import sys;sys.path.insert(0,'/home/claude/lecture')
from fig import *;from mk import build
T="先生";S="生徒"
L=[
(1,T,"今日は、EtherChannelです。複数の物理リンクを束ねて、1本の論理リンクとして扱う機能です。",None),
(1,T,"スイッチの間を2本でつなぐと、STPが片方をブロックしてしまいますよね。EtherChannelで束ねると、1本として扱われるので、ブロックされず、帯域も増えます。",None),
(1,S,"2本分の速さが出るんですか？",None),
(1,T,"全体ではそうです。ただし、1つの通信の流れ、フローは、送信元や宛先のMACやIPからハッシュで計算した、1本のリンクだけを使います。たくさんのフローを、線に振り分けるイメージです。",None),
(2,T,"束ね方は3つ。1つ目はLACP。IEEE標準の802.3adで、モードはactiveとpassiveです。",None),
(2,T,"activeは自分から交渉を始める、passiveは相手から始められるのを待つ、です。だから、activeとactive、activeとpassiveは成立しますが、passive同士は成立しません。",None),
(2,T,"2つ目はPAgP。Cisco独自の方式で、モードはdesirableとautoです。desirableが自分から、autoが待つ側です。",None),
(2,T,"3つ目はmode on。交渉をせずに、静的に束ねます。両端ともonにする必要があります。",None),
(2,S,"LACPの問題で、desirableやautoを選んではいけないんですね。",None),
(2,T,"その通り。それはPAgPの言葉です。相手がpassiveなら、こちらはactive。相手から誘われたら応えて、自分からは誘わない、と言われたらpassiveです。",None),
(3,T,"設定は、束ねたい物理ポートで、channel-group 1 mode activeのように打ちます。チャネルグループの番号は、スイッチの中だけの番号なので、両端で違っていても構いません。",None),
(3,T,"大事なのは、束ねるポートの設定を、全部そろえることです。速度とデュプレックス、アクセスかトランクか、許可するVLANなどが1つでも違うと、そのポートは束ねられません。",None),
(3,S,"もし1本だけ、許可VLANに300が抜けていたら？",None),
(3,T,"その1本が仲間外れになります。switchport trunk allowed vlan add 300で、そろえてあげます。addを忘れずに。",None),
(3,T,"L3のEtherChannelを作るときは、物理ポートとPort-channelの両方でno switchportにして、Port-channelにIPアドレスを付けます。既存の束に新しいポートを追加するときも、同じno switchportとchannel-groupの設定にします。",None),
(3,T,"LACPでは、アクティブに使えるリンクは最大8本です。最大16本まで設定でき、残りは待機になります。",None),
(4,T,"確認は、show etherchannel summaryです。Po1の横のSUは、Sがレイヤー2、Uが使用中。RはL3、Dはダウンです。",None),
(4,T,"ポートの横に、Pが付いていれば束ねられています。Iはスタンドアロンで、束ねられずに単独で動いている状態です。相手側でLACPが設定されていない、などが原因です。",None),
(5,T,"ここで小テストです。LACPでEtherChannelを組むとき、束になる組み合わせはどれでしょう？画面で選んでください。",None),
(5,T,"正解は、activeとpassiveです。",None),
(6,T,"では、今日のまとめです。",None),
(6,T,"1つ目。EtherChannelは物理リンクを束ねて1本に。STPでブロックされず、フローはハッシュで1本に振り分ける。",None),
(6,T,"2つ目。LACPはactiveとpassiveで、passive同士はだめ。PAgPはdesirableとauto。onは両端on。",None),
(6,T,"3つ目。束ねるポートの設定はそろえる。確認はshow etherchannel summaryで、SUは使用中、Iは単独。",None),
(6,S,"activeとpassive、もう迷いません！",None),
(6,T,"いいですね。次回は、隣の機器を調べる、CDPとLLDPを学びます。お疲れさまでした。",None),
]
SC=["EtherChannelとは","3つの束ね方","設定とそろえる項目","show etherchannel summary","小テスト","まとめ"]
p1=svg(200,"".join([sc(60,80,.8,switch(0,0)),sc(300,80,.8,switch(0,0)),"".join(f'<path d="M100 {66+k*10}h160" stroke="var(--ink)" stroke-width="3"/>' for k in range(3)),f'<ellipse cx="180" cy="76" rx="34" ry="24" fill="none" stroke="{A}" stroke-width="3"/>',lab(180,40,"Port-channel 1（1本として扱う）",12.5,800,"#b77d00"),
 lab(180,138,"STPでブロックされない・帯域が増える",13,800),lab(180,162,"1つのフローはハッシュで決めた1本のリンクを使う",12,700,"var(--sub)")]),"EtherChannelのしくみ")
tbl=[("LACP（IEEE 802.3ad）","active ／ passive","active-active・active-passive ○　passive-passive ✕",B),("PAgP（Cisco独自）","desirable ／ auto","desirable-desirable・desirable-auto ○　auto-auto ✕",G),("静的","on","両端とも on",K)]
R2=rows([(None,a+"："+b,c,col) for a,b,c,col in tbl]);p2=svg(R2[1]+4,R2[0],"EtherChannelの3つの束ね方")
R3=rows([(None,"channel-group 1 mode active","物理ポートで設定。番号は両端で違ってもよい",B),(None,"そろえる：速度・デュプレックス","アクセス／トランク・許可VLAN・ネイティブVLAN",R),(None,"L3のEtherChannel","物理ポートとPort-channelで no switchport、Port-channelにIP",K),(None,"アクティブなリンクは最大8本","LACPは16本まで設定でき、残りは待機",A)]);p3=svg(R3[1]+4,R3[0],"設定とそろえる項目")
p4=svg(240,term(10,10,340,124,[("SW1# show etherchannel summary",G),("Group Port-channel Protocol Ports",K),("1     Po1(SU)      LACP  Gi0/1(P)",B),("                         Gi0/2(I)",R)]).replace("font:700 14px","font:700 12.5px")+lab(180,160,"S＝Layer2　U＝使用中　R＝Layer3　D＝ダウン",12.5,800)+lab(180,186,"P＝束ねられている",12.5,800,B)+lab(180,210,"I＝単独（stand-alone）：相手にLACPがないなど",12.5,800,R),"show etherchannel summaryの読み方")
R6=rows([(None,"束ねて1本・STPでブロックされない","フローはハッシュで1本に",A),(None,"LACP active/passive・PAgP desirable/auto・on","passive同士・auto同士は不成立",B),(None,"設定はそろえる","Po1(SU)＝L2で使用中、(I)＝単独",G)]);P6=svg(R6[1]+4,R6[0],"今日のまとめ")
qt=lambda t,c:f'<g>{tag(0,0,t,c,110)}</g>'
pages=[
 {"t":"EtherChannelとは","svg":p1,"b":"<b>EtherChannel</b>は、複数の物理リンクを束ねて1本の論理リンク（Port-channel）として扱う機能。帯域が増え、STPでブロックされません。","p":"フローごとにハッシュで使うリンクを決める。"},
 {"t":"3つの束ね方","svg":p2,"b":"<b>LACP</b>（Link Aggregation Control Protocol）はIEEE標準、<b>PAgP</b>（Port Aggregation Protocol）はCisco独自。どちらか一方が自分から交渉（active／desirable）すれば成立します。","p":"「応答するが開始しない」＝passive。"},
 {"t":"設定とそろえる項目","svg":p3,"b":"束ねるポートの設定が1つでも違うと、そのポートはバンドルされません。","p":"許可VLANをそろえるときも add を忘れずに。"},
 {"t":"show etherchannel summary","svg":p4,"b":"Po1(SU)＝L2のEtherChannelで使用中。ポートの(P)は束ねられている、(I)は単独で動いている状態です。","p":"(I)の原因：相手側でLACPが設定されていない、など。"},
 {"t":"小テスト","quiz":{"q":"LACPでEtherChannelを組むとき、束になる組み合わせは？","o":[["active と passive",qt("active–passive",G)],["passive と passive",qt("passive–passive",R)],["desirable と auto（LACP）",qt("desirable–auto",K)]],"a":0,"e":"正解は<b>active と passive</b>。passive同士では成立しません。desirable/autoはPAgPの言葉です。"}},
 {"t":"今日のまとめ","svg":P6,"b":"次回は「CDP / LLDP」。","p":"一問一答の「ネットワークアクセス」で確かめましょう。"}]
build(25,"nl24","EtherChannel","ネットワークアクセス",SC,L,pages,None)
