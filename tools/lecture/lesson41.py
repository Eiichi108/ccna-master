import sys;sys.path.insert(0,'/home/claude/lecture')
from fig import *;from mk import build
T="先生";S="生徒"
L=[
(1,T,"今日は短めの回です。ルーターやスイッチのパスワードを、安全に設定する方法を学びます。",None),
(1,T,"特権EXECモードに入るためのパスワードには、enable passwordとenable secretの2つがあります。",None),
(1,T,"enable secretは、パスワードをハッシュ化して保存します。enable passwordは平文です。両方が設定されているときは、secretが優先されます。だから、secretを使うのがおすすめです。",None),
(1,S,"ハッシュ化って、何ですか？",None),
(1,T,"元に戻せない形に変えることです。設定ファイルを見られても、パスワードそのものは分かりません。",None),
(2,T,"show running-configで、enable secret 5と表示されていたら、5はMD5でハッシュ化されているという意味です。8と9は、もっと強い方式です。",None),
(2,T,"コンソールやvtyのパスワードは、普通は平文で保存されます。service password-encryptionを設定すると、設定ファイルの中の平文のパスワードを、すべて暗号化して見えなくします。",None),
(2,T,"ただし、これはtype 7という弱い方式で、簡単に元に戻せます。だから、それだけに頼らず、secretを使うのが基本です。",None),
(3,T,"ログイン時の警告文は、banner motdで設定します。許可された人だけ使えます、のような文を表示します。",None),
(3,T,"username admin privilege 15 secretのprivilege 15は、最高の権限という意味です。権限は0から15まであります。",None),
(3,T,"リモートのログインを安全にするなら、transport input sshでSSHだけを許可します。SSHだけを許可して、設定の中のパスワードも隠すなら、transport input sshとservice password-encryptionの2つです。",None),
(4,T,"ここで小テストです。enable passwordとenable secretが両方設定されているとき、どうなるでしょう？画面で選んでください。",None),
(4,T,"正解は、secretが優先される、です。",None),
(5,T,"では、今日のまとめです。",None),
(5,T,"1つ目。enable secretはハッシュ化、enable passwordは平文。両方あればsecretが優先。",None),
(5,T,"2つ目。service password-encryptionは、平文のパスワードを隠すが、type 7で弱い。5はMD5。",None),
(5,T,"3つ目。banner motdで警告文、privilege 15は最高の権限、transport input sshでSSHだけ。",None),
(5,S,"secretを使う、を習慣にします！",None),
(5,T,"いいですね。次回は、パスワードのルールとIPsecを学びます。お疲れさまでした。",None),
]
SC=["enable secret","保存形式","その他の設定","小テスト","まとめ"]
R1=rows([(None,"enable secret Str0ng!","ハッシュ化して保存（推奨）。passwordより優先",G),(None,"enable password cisco","平文で保存",R)]);p1=svg(R1[1]+4,R1[0],"enable secretとenable password")
R2=rows([(None,"type 7（service password-encryption）","平文のパスワードを隠すが、簡単に元に戻せる",A),(None,"type 5","MD5のハッシュ",B),(None,"type 8・9","より強い方式（9＝scrypt）",G)]);p2=svg(R2[1]+4,R2[0],"パスワードの保存形式")
R3=rows([(None,"banner motd #Authorized only#","ログイン時の警告文",B),(None,"privilege 15","最高の権限（0〜15）",G),(None,"transport input ssh","SSHだけを許可",A)]);p3=svg(R3[1]+4,R3[0],"その他の設定")
R5=rows([(None,"secret＝ハッシュ・優先","password＝平文",G),(None,"service password-encryption＝type 7","5＝MD5、8・9＝より強い",A),(None,"banner motd・privilege 15・transport input ssh","警告文・最高権限・SSHだけ",B)]);P5=svg(R5[1]+4,R5[0],"今日のまとめ")
qt=lambda t,c:f'<g>{tag(0,0,t,c,90)}</g>'
pages=[
 {"t":"enable secret","svg":p1,"b":"両方設定されているときは<b>secretが優先</b>されます。","p":"secretを使うのが基本。"},
 {"t":"保存形式","svg":p2,"b":"<b>service password-encryption</b>は、設定ファイルの全部の平文パスワードを暗号化して見えなくします（強くはない）。","p":"enable secret 5 $1$... の5＝MD5。"},
 {"t":"その他の設定","svg":p3,"b":"","p":"SSHだけ＋パスワードを隠す → transport input ssh ＋ service password-encryption。"},
 {"t":"小テスト","quiz":{"q":"enable password と enable secret が両方設定されている場合、どうなる？","o":[["secretが優先される",qt("secret",G)],["passwordが優先される",qt("password",R)],["両方入力が必要",qt("両方",K)]],"a":0,"e":"正解は<b>secretが優先される</b>。secretはハッシュ化して保存されます。"}},
 {"t":"今日のまとめ","svg":P5,"b":"次回は「パスワードポリシーとIPsec」。","p":"一問一答の「セキュリティの基礎」で確かめましょう。"}]
build(41,"nl40","パスワードと機器の保護","セキュリティ",SC,L,pages,None)
