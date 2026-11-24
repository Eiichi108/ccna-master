import sys;sys.path.insert(0,'/home/claude/lecture')
from fig import *;from mk import build
T="先生";S="生徒"
L=[
(1,T,"今日は、ネットワークアクセスの分野の最後。WLCのWeb画面で、WLANを作る手順を学びます。試験では、画面の図を見て答える問題がたくさん出ます。",None),
(1,T,"まず準備です。新しいWLANの設定は、認証サーバーの登録、ダイナミックインターフェースの作成、そしてWLANを作って、そのダイナミックインターフェースにひもづける、という流れです。",None),
(1,T,"ダイナミックインターフェースは、WLANの通信をどのVLANに流すかを決める出入口です。",None),
(2,T,"WLANsタブで、Create Newを選びます。ここで必ず入れるのは、プロファイル名とSSIDです。プロファイル名はWLCの中での管理用の名前、SSIDは利用者に見えるWi-Fiの名前です。",None),
(2,T,"次にGeneralタブ。StatusをEnabled、有効にします。これを忘れると、SSIDが電波に乗らず、クライアントから見えません。",None),
(2,T,"同じGeneralタブで、Interfaceを選びます。ここで、クライアントの通信をどのVLANに流すかが決まります。図でguestになっていたら、Dataに変える、という問題がよく出ます。",None),
(2,S,"見えないときはStatus、別のサブネットにつなぎたいときはInterface、ですね。",None),
(3,T,"次はSecurityタブのLayer 2。事前共有キー、つまり、みんな同じパスワードで接続するなら、WPA2 PolicyとAESを選び、認証キー管理をPSKにします。",None),
(3,T,"パスワードは、ASCIIなら8文字から63文字。16進数のHEXなら64文字ちょうどです。63文字のパスワードなら、ASCIIを選びます。",None),
(3,T,"WPA2だけを使うときは、古いWPAのポリシーと暗号化を無効にします。安全なハッシュを使うなら、PSKではなくPSK-SHA2を選びます。",None),
(3,T,"会社のIDとパスワードで、1人ずつ認証するなら、認証キー管理を802.1Xにします。そのとき、RADIUSサーバーの設定で、Network UserのEnableにチェックを入れておきます。",None),
(3,S,"共通のパスワードはPSK、1人ずつは802.1Xですね。",None),
(3,T,"その通り。WPA3などで使う、とても強い暗号化方式がGCMPで、これもLayer 2のセキュリティで設定します。",None),
(4,T,"次は、その他のセキュリティです。特定の端末だけを参加させたいなら、MACフィルタリングを有効にします。",None),
(4,T,"なりすましのアソシエーション要求を防ぐには、PMF、保護された管理フレームを有効にします。再試行まで待たせる時間が、カムバックタイマーです。",None),
(4,T,"ホテルのWi-Fiのように、Webページでログインさせるなら、Layer 3のセキュリティで、Webポリシー、つまりWeb認証を設定します。ログインまではDHCPとDNSだけが通ります。",None),
(4,T,"ISEなどの認証サーバーの指示で、人ごとにVLANを変えるなら、AdvancedタブでAAAオーバーライドを許可します。",None),
(5,T,"最後に、品質と速さの設定です。QoSタブのプロファイルは、音声がPlatinum、動画がGold、普通はSilver、優先度の低い通信がBronzeです。",None),
(5,T,"両方の周波数に対応した端末を、空いている5GHzへ誘導するのが、バンドセレクトです。FlexConnectのローカルスイッチングなどの細かい設定は、Advancedタブにあります。",None),
(5,T,"そして、WLCとスイッチのポートを束ねる機能はLAGです。WLCのLAGはLACPもPAgPも使わないので、スイッチ側はchannel-group 1 mode onにします。",None),
(6,T,"ここで小テストです。WLCのQoSプロファイルで、音声に使うものはどれでしょう？画面で選んでください。",None),
(6,T,"正解はPlatinumです。",None),
(7,T,"では、今日のまとめです。",None),
(7,T,"1つ目。Create Newでプロファイル名とSSID。GeneralでStatusを有効、Interfaceで流すVLAN。",None),
(7,T,"2つ目。Layer 2で、共通パスワードはWPA2とAESとPSK、ASCIIは8から63文字。1人ずつは802.1X。",None),
(7,T,"3つ目。Web認証はLayer 3、AAAオーバーライドはAdvanced、音声はPlatinum、LAGはmode on。",None),
(7,S,"画面のどこを見ればいいか、分かってきました！",None),
(7,T,"よく頑張りました。これでネットワークアクセスの分野はおしまいです。次回からは、IP接続、ルーティングの分野に入ります。お疲れさまでした。",None),
]
SC=["設定の流れ","WLANを作る","Layer 2セキュリティ","その他のセキュリティ","QoSとLAG","小テスト","まとめ"]
p1=svg(160,"".join(f'<rect x="{10+k*118}" y="30" width="104" height="70" rx="10" fill="{c}" opacity=".14"/>'+lab(62+k*118,58,a,13,800,c)+lab(62+k*118,82,b,11.5,700) for k,(a,b,c) in enumerate((("① 認証サーバー","RADIUSを登録",K),("② ダイナミックIF","VLANの出入口",B),("③ WLAN作成","IFにひもづけ",G))))+arrow(116,65,126,65)+arrow(234,65,244,65)+lab(180,136,"WLANの通信は、ひもづけたIFのVLANへ流れる",12,700,"var(--sub)"),"WLAN作成の流れ")
def scr(y,tab,rows_,c):
    s=f'<rect x="10" y="{y}" width="340" height="{30+len(rows_)*26}" rx="10" fill="var(--card)" stroke="var(--line)" stroke-width="2"/><rect x="10" y="{y}" width="340" height="26" rx="10" fill="{c}" opacity=".18"/>'+lab(24,y+18,tab,12.5,800,c,"start")
    for k,(a,b,hi) in enumerate(rows_): s+=lab(24,y+46+k*26,a,12.5,700,"var(--ink)","start")+lab(336,y+46+k*26,b,12.5,800,R if hi else "var(--sub)","end")
    return s
p2=svg(250,scr(8,"WLANs → Create New",[("Profile Name","Office",0),("SSID","Office",0)],B)+scr(100,"General",[("Status","☑ Enabled（忘れると見えない）",1),("Interface","guest → Data に",1),("Radio Policy","All",0)],G)+lab(180,236,"別のサブネットにつなぐ＝Interfaceを変える",12,700,"var(--sub)"),"WLANの作成画面")
R3=rows([(None,"WPA2 Policy＋AES（CCMP128）","WPAのみを無効にするとWPA2だけ",B),(None,"認証キー管理：PSK","共通パスワード。ASCII 8〜63文字／HEX 64文字",G),(None,"安全なハッシュ → PSK-SHA2","PSKより強い鍵の扱い",G),(None,"802.1X","1人ずつ認証（ドメインの資格情報）。RADIUSでNetwork UserをEnable",'#8a3ffc'),(None,"GCMP","WPA3などの強い暗号化（Layer 2で設定）",K)]);p3=svg(R3[1]+4,R3[0],"Layer 2セキュリティ")
R4=rows([(None,"MACフィルタリング","特定のクライアントだけ参加させる",B),(None,"PMF＋カムバックタイマー","なりすましのアソシエーション要求を防ぐ",R),(None,"Layer 3：Webポリシー（Web認証）","ログイン画面。認証まではDHCPとDNSだけ",A),(None,"AAAオーバーライド（Advanced）","ISEなどの指示で人ごとにVLANを変える",G)]);p4=svg(R4[1]+4,R4[0],"その他のセキュリティ")
R5=rows([(None,"QoS：Platinum／Gold／Silver／Bronze","音声／動画／普通（初期値）／低優先",A),(None,"バンドセレクト","両対応の端末を空いている5GHzへ誘導",B),(None,"Advancedタブ","FlexConnectローカルスイッチングなど",K),(None,"LAG（802.3adのような束ね）","スイッチ側は channel-group 1 mode on",G)]);p5=svg(R5[1]+4,R5[0],"QoSとLAG")
R7=rows([(None,"Create New：プロファイル名＋SSID","General：Status有効・Interfaceで流すVLAN",B),(None,"Layer 2：WPA2＋AES＋PSK／802.1X","ASCIIは8〜63文字",G),(None,"Web認証＝Layer 3／AAAオーバーライド","音声＝Platinum／LAG＝mode on",A)]);P7=svg(R7[1]+4,R7[0],"今日のまとめ")
qt=lambda t,c:f'<g>{tag(0,0,t,c,90)}</g>'
pages=[
 {"t":"設定の流れ","svg":p1,"b":"新しいWLAN（Wireless LAN）は、認証サーバー → <b>ダイナミックインターフェース</b> → <b>WLANを作ってダイナミックインターフェースにひもづけ</b>、の順に作ります。","p":"管理インターフェースは初期設定時に作ってある。"},
 {"t":"WLANを作る","svg":p2,"b":"Create Newで必ず入れるのは<b>プロファイル名</b>と<b>SSID</b>。Generalで<b>Status</b>を有効にし、<b>Interface</b>で通信を流すVLANを選びます。","p":"SSIDが見えない → Statusが無効。"},
 {"t":"Layer 2セキュリティ","svg":p3,"b":"Security → Layer 2 で暗号化と認証キー管理を設定します。AESは暗号化方式なので「認証キー管理」の欄には入りません。","p":"PSK（Pre-Shared Key）＝共通パスワード、802.1X＝1人ずつ。"},
 {"t":"その他のセキュリティ","svg":p4,"b":"","p":"Web認証はL3の設定（L2の802.1Xではない）。"},
 {"t":"QoSとLAG","svg":p5,"b":"WLCのLAG（Link Aggregation）はLACPもPAgPも使わないので、スイッチ側は<b>mode on</b>で束ねます。","p":"音声品質のため混雑の少ない5GHzへ → バンドセレクト。"},
 {"t":"小テスト","quiz":{"q":"WLCのQoSプロファイルで、音声に使うものは？","o":[["Platinum",qt("Platinum",A)],["Gold",qt("Gold",B)],["Bronze",qt("Bronze",K)]],"a":0,"e":"正解は<b>Platinum</b>。Goldは動画、Silverは普通（初期値）、Bronzeは優先度の低い通信です。"}},
 {"t":"今日のまとめ","svg":P7,"b":"これで「ネットワークアクセス」はおしまい。次回から「IP接続」に入ります。","p":"一問一答の「ネットワークアクセス」で、WLCの画面の問題を解いて確かめましょう。"}]
build(28,"nl27","WLCのGUIでWLANを作る","ネットワークアクセス",SC,L,pages,None)
