import sys;sys.path.insert(0,'/home/claude/lecture')
from fig import *;from mk import build
T="先生";S="生徒"
L=[
(1,T,"今日は、REST APIとJSONです。プログラムからネットワークを操作するときの、言葉と文法のようなものです。",None),
(1,T,"REST APIは、HTTPのメソッドで操作を表します。操作は4つで、頭文字をとってCRUD、作成、読み取り、更新、削除です。",None),
(1,T,"作成がPOST、読み取りがGET、更新がPUTかPATCH、削除がDELETEです。",None),
(1,S,"情報を取得するならGET、新しく作るならPOST、ですね。",None),
(1,T,"その通り。REMOVEやPOPのような名前は、HTTPのメソッドではないので、ひっかけに注意しましょう。",None),
(2,T,"サーバーからの返事には、ステータスコードが付きます。200はOK、201は作成できた、Created。",None),
(2,T,"400はリクエストがおかしい、401は認証されていない、403は認証はされたけど権限がない、404は見つからない。500はサーバー側のエラーです。",None),
(2,T,"URLの後ろの、はてなマーク以降は、クエリパラメーターと言い、条件などをサーバーに渡します。",None),
(3,T,"次はJSONです。データを、キーと値の組で書きます。コロンの左がキー、右が値です。",None),
(3,T,"波かっこで囲んだ、キーと値のまとまりがオブジェクト。角かっこで囲んで並べたものが配列です。",None),
(3,S,"波かっこがオブジェクト、角かっこが配列、ですね。",None),
(3,T,"値の型は、文字列、数値、真偽値のtrueとfalse、null、配列、オブジェクトです。日付という型はなく、文字列で書きます。",None),
(3,T,"大事なルールが2つ。キーと文字列は、必ずダブルクォートで囲みます。シングルクォートは使えません。そして、最後の要素の後ろに、カンマを付けてはいけません。",None),
(3,T,"ダブルクォートのないtrueは真偽値、ダブルクォートで囲んだtrueは文字列です。",None),
(4,T,"試験では、JSONの図を見て、オブジェクトとキーと値の数を数える問題が出ます。波かっこの組がオブジェクト、コロンの左がキー、と数えていきます。",None),
(4,T,"送るデータがJSONだと伝えるHTTPヘッダーは、Content-Type、application/jsonです。",None),
(5,T,"ここで小テストです。REST APIで、情報を取得するメソッドはどれでしょう？画面で選んでください。",None),
(5,T,"正解はGETです。",None),
(6,T,"では、今日のまとめです。",None),
(6,T,"1つ目。CRUDは、POSTで作成、GETで読み取り、PUTとPATCHで更新、DELETEで削除。",None),
(6,T,"2つ目。200はOK、201は作成、401は未認証、403は権限なし、404は見つからない。",None),
(6,T,"3つ目。JSONは、波かっこがオブジェクト、角かっこが配列、コロンの左がキー。ダブルクォート、最後にカンマなし。",None),
(6,S,"JSONの図、数えられるようになりました！",None),
(6,T,"いいですね。次回は、REST APIの特徴と認証を学びます。お疲れさまでした。",None),
]
SC=["CRUDとHTTPメソッド","ステータスコード","JSONの書き方","JSONを読む","小テスト","まとめ"]
p1=svg(220,"".join(f'<rect x="{10+k*86}" y="20" width="80" height="110" rx="10" fill="{c}" opacity=".14"/>'+lab(50+k*86,48,a,13,800)+lab(50+k*86,80,b,15,800,c)+lab(50+k*86,108,d,11,700,"var(--sub)") for k,(a,b,d,c) in enumerate((("作成","POST","Create",G),("読み取り","GET","Read",B),("更新","PUT/PATCH","Update",A),("削除","DELETE","Delete",R))))+lab(180,160,"CRUD＝Create・Read・Update・Delete",13,800)+lab(180,186,"REMOVE・POP・REDIRECT はHTTPメソッドではない",12,700,"var(--sub)"),"CRUDとHTTPメソッド")
R2=rows([(None,"200 OK／201 Created","成功／作成できた",G),(None,"400 Bad Request","リクエストがおかしい",A),(None,"401 Unauthorized／403 Forbidden","認証されていない／権限がない",R),(None,"404 Not Found／500","見つからない／サーバーのエラー",K),(None,"?id=5","クエリパラメーター",B)]);p2=svg(R2[1]+4,R2[0],"ステータスコード")
p3=svg(250,term(10,10,340,164,[("{",K),('  "hostname": "R1",',B),('  "interfaces": ["G0/0", "G0/1"],',G),('  "enabled": true,',A),('  "vlan": 10',R),("}",K)]).replace("font:700 14px","font:700 13px")+lab(180,198,"{ }＝オブジェクト　[ ]＝配列　コロンの左＝キー",12.5,800)+lab(180,222,"キーと文字列はダブルクォート／最後の要素にカンマなし",12,700,"var(--sub)"),"JSONの書き方")
R4=rows([(None,"型","文字列・数値・真偽値（true/false）・null・配列・オブジェクト",B),(None,"数え方","{ }の組＝オブジェクト、コロンの左＝キー、右＝値",G),(None,"Content-Type: application/json","送るデータがJSON",A)]);p4=svg(R4[1]+4,R4[0],"JSONを読む")
R6=rows([(None,"POST・GET・PUT/PATCH・DELETE","作成・読み取り・更新・削除",B),(None,"200・201・401・403・404","OK・作成・未認証・権限なし・見つからない",G),(None,"{ }＝オブジェクト・[ ]＝配列","ダブルクォート・最後にカンマなし",A)]);P6=svg(R6[1]+4,R6[0],"今日のまとめ")
qt=lambda t,c:f'<g>{tag(0,0,t,c,80)}</g>'
pages=[
 {"t":"CRUDとHTTPメソッド","svg":p1,"b":"<b>REST</b>（Representational State Transfer）APIは、HTTPのメソッドで操作を表します。","p":"PUT＝更新（DNSサーバーを更新する、など）。"},
 {"t":"ステータスコード","svg":p2,"b":"","p":"401と403の違いがよく出る。"},
 {"t":"JSONの書き方","svg":p3,"b":"<b>JSON</b>（JavaScript Object Notation）は「\"キー\": 値」の組で書きます。","p":"'text'（シングルクォート）はJSONとして正しくない。"},
 {"t":"JSONを読む","svg":p4,"b":"","p":"\"port\" のようにコロンの左にあるのはキー、\"FW18\" のように右にあるのは値。"},
 {"t":"小テスト","quiz":{"q":"REST APIで情報を「取得」するメソッドは？","o":[["GET",qt("GET",B)],["POST",qt("POST",G)],["DELETE",qt("DELETE",R)]],"a":0,"e":"正解は<b>GET</b>。POST＝作成、PUT/PATCH＝更新、DELETE＝削除です。"}},
 {"t":"今日のまとめ","svg":P6,"b":"次回は「REST APIの特徴と認証」。","p":"一問一答の「自動化とプログラマビリティ」で確かめましょう。"}]
build(48,"nl47","REST APIとJSON","自動化",SC,L,pages,None)
