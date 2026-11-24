import sys;sys.path.insert(0,'/home/claude/lecture')
from fig import *;from mk import build
T="先生";S="生徒"
L=[
(1,T,"今日は、セキュリティの分野の最後。VPNのおさらいと、無線LANのセキュリティを学びます。",None),
(1,T,"VPNは2種類でした。拠点どうしをIPsecでつなぐのがサイト間VPN。カフェの公衆Wi-Fiのような外から、1人の利用者が会社につなぐのが、リモートアクセスVPNです。",None),
(2,T,"無線では、電波が誰にでも届きます。暗号化の役割は、電波を傍受されても、中身を読めなくすることです。",None),
(2,T,"暗号化の方式は、時代とともに進化しました。WEPはRC4を使う古い方式で、脆弱なので使いません。初代のWPAはTKIP。WPA2はAES、正確にはAES-CCMP。WPA3は、さらに強いGCMPです。",None),
(2,S,"WEP、TKIP、CCMP、GCMPの順に強くなるんですね。",None),
(2,T,"その通り。なお、SHAやMD5はハッシュで、PEAPやEAPは認証の方式です。暗号化の方式ではないので、ひっかけに注意しましょう。",None),
(3,T,"WPAには2つのモードがあります。Personalは、全員で同じパスワード、事前共有キーのPSKを使う、家庭向けのモードです。",None),
(3,T,"Enterpriseは、802.1XとEAPを使って、利用者ごとにRADIUSサーバーで認証する、企業向けのモードです。",None),
(3,T,"PSKの弱点は、全員で同じキーを使うので、1人から漏れると全体が危険になることです。人の出入りが多い組織では、Enterpriseがおすすめです。",None),
(3,T,"802.1Xに対応していない機器があるときは、iPSK、機器ごとに違うパスワードをRADIUSから配る方式も使えます。",None),
(4,T,"WPA3の特徴は2つ。Personalモードでは、SAEという方式で認証するので、パスワードを盗み見て総当たりする、辞書攻撃に強くなりました。",None),
(4,T,"SAEのおかげで、もし将来パスワードがばれても、過去の通信は解読できません。この性質を、前方秘匿性、PFSと言います。",None),
(4,T,"もう1つ、WPA3では、PMF、保護された管理フレームが必須です。PMFは、802.11wとも呼ばれます。WPA2では任意でした。",None),
(4,S,"WLCの画面で802.11wを有効にするなら、PMFをRequiredにするんですね。",None),
(4,T,"完璧です。最後に、MACアドレスのフィルタリングだけでは不十分です。MACアドレスは電波から分かり、簡単に偽装できるからです。WPA2やWPA3で認証と暗号化をしましょう。",None),
(5,T,"ここで小テストです。WPA3-Personalで使われる認証方式はどれでしょう？画面で選んでください。",None),
(5,T,"正解はSAEです。",None),
(6,T,"では、今日のまとめです。",None),
(6,T,"1つ目。公衆Wi-Fiから会社へはリモートアクセスVPN、拠点どうしはサイト間VPN。",None),
(6,T,"2つ目。WEPは使わない、WPAはTKIP、WPA2はAES-CCMP、WPA3はGCMP。",None),
(6,T,"3つ目。PersonalはPSK、Enterpriseは802.1XとRADIUS。WPA3はSAEとPMFが必須。",None),
(6,S,"これでセキュリティの分野も終わりです！",None),
(6,T,"よく頑張りました。次回からは、最後の分野、自動化とプログラマビリティです。お疲れさまでした。",None),
]
SC=["VPNのおさらい","暗号化の進化","PersonalとEnterprise","WPA3","小テスト","まとめ"]
R1=rows([(None,"サイト間VPN","拠点どうしをIPsecでつなぐ",B),(None,"リモートアクセスVPN","1人の利用者が外（公衆Wi-Fiなど）から会社へ",G)]);p1=svg(R1[1]+4,R1[0],"VPNの種類")
p2=svg(210,"".join(f'<rect x="{10+k*86}" y="30" width="80" height="90" rx="10" fill="{c}" opacity="{.15+k*.08}"/>'+lab(50+k*86,58,a,14,800,"var(--ink)")+lab(50+k*86,86,b,12.5,800,c)+lab(50+k*86,108,d,11,700,"var(--sub)") for k,(a,b,d,c) in enumerate((("WEP","RC4","使わない",R),("WPA","TKIP","古い",A),("WPA2","AES-CCMP","今の標準",B),("WPA3","GCMP","最も強い",G))))+arrow(20,140,340,140,G)+lab(180,164,"右へいくほど強い",12.5,800,G)+lab(180,190,"SHA・MD5＝ハッシュ／EAP・PEAP＝認証方式（暗号化ではない）",11.5,700,"var(--sub)"),"無線の暗号化の進化")
R3=rows([(None,"Personal（PSK）","全員共通のパスワード。家庭向け。1人から漏れると全体が危険",A),(None,"Enterprise（802.1X/EAP＋RADIUS）","利用者ごとに認証。企業向け",B),(None,"iPSK","機器ごとに違うPSKをRADIUSから配る（802.1X非対応の機器向け）",G)]);p3=svg(R3[1]+4,R3[0],"PersonalとEnterprise")
R4=rows([(None,"SAE（Personal）","辞書攻撃に強い・前方秘匿性（PFS）",G),(None,"PMF（802.11w）が必須","WLCではPMFをRequiredに（WPA2では任意）",B),(None,"MACフィルタリングだけ ✕","MACは簡単に偽装できる",R)]);p4=svg(R4[1]+4,R4[0],"WPA3の特徴")
R6=rows([(None,"公衆Wi-Fiから会社 → リモートアクセスVPN","拠点どうし → サイト間VPN",B),(None,"WEP✕・WPA＝TKIP","WPA2＝AES-CCMP・WPA3＝GCMP",G),(None,"Personal＝PSK／Enterprise＝802.1X","WPA3＝SAE＋PMF必須",A)]);P6=svg(R6[1]+4,R6[0],"今日のまとめ")
qt=lambda t,c:f'<g>{tag(0,0,t,c,80)}</g>'
pages=[
 {"t":"VPNのおさらい","svg":p1,"b":"","p":"従業員が公衆Wi-Fiからサーバーへ → リモートアクセスVPN。"},
 {"t":"暗号化の進化","svg":p2,"b":"暗号化は、傍受されたデータを簡単に読み取られないようにします。<b>WEP</b>（Wired Equivalent Privacy）は脆弱。WPA2だけでサポートされる暗号＝<b>AES</b>。","p":"WPA1＝TKIP、WPA3＝GCMP。"},
 {"t":"PersonalとEnterprise","svg":p3,"b":"PSK認証を使うWPAのモード＝<b>Personal</b>。","p":"WPA2で事前共有キー → 暗号化AES（CCMP）＋認証キー管理PSK。"},
 {"t":"WPA3","svg":p4,"b":"<b>SAE</b>（Simultaneous Authentication of Equals）。<b>PMF</b>（Protected Management Frames）。","p":"Perfect Forward Secrecyに依存する＝WPA3。"},
 {"t":"小テスト","quiz":{"q":"WPA3-Personalで使われる認証方式は？","o":[["SAE",qt("SAE",G)],["TKIP",qt("TKIP",A)],["WEP",qt("WEP",R)]],"a":0,"e":"正解は<b>SAE</b>。オフラインの辞書攻撃に強くなっています。"}},
 {"t":"今日のまとめ","svg":P6,"b":"これで「セキュリティの基礎」はおしまい。次回から「自動化とプログラマビリティ」に入ります。","p":"一問一答の「セキュリティの基礎」で確かめましょう。"}]
build(45,"nl44","VPN・無線LANのセキュリティ","セキュリティ",SC,L,pages,None)
