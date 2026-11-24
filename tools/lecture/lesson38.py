import sys;sys.path.insert(0,'/home/claude/lecture')
from fig import *;from mk import build
T="先生";S="生徒"
L=[
(1,T,"今日は、3つのテーマ。大事な通信を優先するQoS、安全なリモート管理のSSHの設定、そしてファイル転送です。",None),
(1,T,"QoSは、音声などの大事な通信を、優先して流す仕組みです。処理の順番は、分類、マーキング、そしてキューイングやポリシング、シェーピングです。",None),
(1,T,"マーキングでは、パケットに優先度の印を付けます。IPヘッダーでは、DSCPというフィールドに入れます。音声には、遅延の少ないEF、数字で46を付けるのが一般的です。",None),
(1,S,"くわしくは次回ですか？",None),
(1,T,"そうです。次回、QoSの細かい部分を学びます。",None),
(2,T,"次は、SSHの設定です。SSHを使えるようにするには、いくつかの準備が必要です。",None),
(2,T,"1つ目、hostnameでホスト名。2つ目、ip domain-nameでドメイン名。この2つから、鍵の名前が作られます。",None),
(2,T,"3つ目、crypto key generate rsaで、RSAの鍵を作ります。RSAは、公開鍵と秘密鍵のペアを使う、公開鍵暗号です。ちなみに、同じ鍵を両方が持つ共通鍵暗号の代表は、AESです。",None),
(2,T,"4つ目、username admin secretで、ログイン用のユーザーを作ります。passwordではなく、secretを使うと、パスワードが安全に保存されます。privilege 15を付けると、ログインしてすぐに特権モードに入れます。",None),
(2,T,"5つ目、line vty 0 4、または0 15で、login localとtransport input sshを設定します。login localは、登録したユーザーでログインすること、transport input sshは、SSHだけを受け付けることです。",None),
(2,S,"DHCPプールは、SSHには関係ないですね。",None),
(2,T,"その通り。図の問題では、何がすでに設定済みかを見て、足りないものを選びます。show crypto key mypubkey rsaが空なら、鍵がまだありません。",None),
(3,T,"最後に、ファイル転送です。TFTPは、UDPの69番を使う簡単な方式で、ユーザー名もパスワードもいりません。送ったブロックごとに確認をもらいます。",None),
(3,T,"ルーターのIOSのイメージを、サーバーから機器にコピーしてアップグレードしたり、設定をバックアップしたりするのに、よく使われます。",None),
(3,T,"FTPはTCPを使い、制御用の21番と、データ用の20番などの、2つの接続を使います。認証はありますが平文です。SCPやSFTPも、ログインが必要です。",None),
(4,T,"ここで小テストです。SSHを使えるようにするために、必要ないものはどれでしょう？画面で選んでください。",None),
(4,T,"正解はDHCPプールです。",None),
(5,T,"では、今日のまとめです。",None),
(5,T,"1つ目。QoSは、分類、マーキング、キューイング。音声にはDSCPのEF、46。",None),
(5,T,"2つ目。SSHには、ホスト名、ドメイン名、RSAの鍵、username secret、vtyでlogin localとtransport input ssh。",None),
(5,T,"3つ目。TFTPはUDP69で認証なし、IOSのコピーに使う。FTPはTCPで2つの接続と認証。",None),
(5,S,"SSHの5つの準備、手順で覚えます！",None),
(5,T,"いいですね。次回は、QoSをくわしく学びます。お疲れさまでした。",None),
]
SC=["QoSの入口","SSHの設定","ファイル転送","小テスト","まとめ"]
R1=rows([(None,"分類 → マーキング → キューイング／ポリシング・シェーピング","QoSの処理の順番",B),(None,"マーキング：IPヘッダーのDSCP","音声には EF（DSCP 46）",G)]);p1=svg(R1[1]+4,R1[0],"QoSの入口")
p2=svg(270,term(10,10,340,190,[("hostname R1",B),("ip domain-name example.com",B),("crypto key generate rsa modulus 2048",G),("username admin privilege 15 secret P@ss",A),("line vty 0 15",K),(" login local",K),(" transport input ssh",R)]).replace("font:700 14px","font:700 11.5px")+lab(180,226,"①ホスト名 ②ドメイン名 ③RSA鍵 ④ユーザー ⑤vty",12.5,800)+lab(180,250,"secret＝安全に保存／privilege 15＝すぐ特権モード",11.5,700,"var(--sub)"),"SSHの設定")
R3=rows([(None,"TFTP（UDP 69）","認証なし。ブロックごとに確認。IOSのアップグレード・設定のバックアップ",G),(None,"FTP（TCP 20・21）","制御とデータの2つの接続。認証あり（平文）",B),(None,"SCP・SFTP","ログインが必要",K)]);p3=svg(R3[1]+4,R3[0],"ファイル転送")
R5=rows([(None,"QoS：分類→マーキング→キューイング","音声＝DSCP EF（46）",B),(None,"SSH：ホスト名・ドメイン名・RSA・secret・vty","login local＋transport input ssh",G),(None,"TFTP＝UDP 69・認証なし","FTP＝TCP・2つの接続・認証",A)]);P5=svg(R5[1]+4,R5[0],"今日のまとめ")
qt=lambda t,c:f'<g>{tag(0,0,t,c,90)}</g>'
pages=[
 {"t":"QoSの入口","svg":p1,"b":"<b>QoS</b>（Quality of Service）は大事な通信を優先して流す仕組み。DSCP（Differentiated Services Code Point）はIPヘッダーにある6ビットのフィールドです。","p":"くわしくは次回。"},
 {"t":"SSHの設定","svg":p2,"b":"<b>RSA</b>は公開鍵暗号（鍵がペア）、<b>AES</b>は共通鍵暗号。図で鍵がない（show crypto key mypubkey rsaが空）なら crypto key generate rsa、vtyがSSHだけでないなら transport input ssh。","p":"password 0（平文）ではなく secret を使う。"},
 {"t":"ファイル転送","svg":p3,"b":"","p":"認証なしで送ったデータを確認する＝TFTP。"},
 {"t":"小テスト","quiz":{"q":"SSHを使えるようにするために必要ないものは？","o":[["DHCPプール",qt("DHCPプール",R)],["RSA鍵",qt("RSA鍵",G)],["ドメイン名",qt("ドメイン名",B)]],"a":0,"e":"正解は<b>DHCPプール</b>。SSHにはホスト名・ドメイン名・RSA鍵・ユーザー設定が必要です。"}},
 {"t":"今日のまとめ","svg":P5,"b":"次回は「QoSのPHB（詳しく）」。","p":"一問一答の「IPサービス」で確かめましょう。"}]
build(38,"nl37","QoS・SSH・ファイル転送","IPサービス",SC,L,pages,None)
