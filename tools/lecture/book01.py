import json
B="#0a5cff";G="#00a05a";R="#e6261f";A="#ffb400";K="#3d4450"
def lab(x,y,t,size=14,w=800,fill="var(--ink)",anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="font:{w} {size}px Figtree,\'Hiragino Sans\',sans-serif;fill:{fill};paint-order:stroke;stroke:var(--card);stroke-width:4px;stroke-linejoin:round">{t}</text>'
def pill(x,y,t,c):
    w=len(t)*13+18
    return f'<rect x="{x-w/2}" y="{y-13}" width="{w}" height="22" rx="11" fill="{c}" opacity=".14"/><text x="{x}" y="{y+3}" text-anchor="middle" style="font:700 12.5px Figtree,\'Hiragino Sans\',sans-serif;fill:{c}">{t}</text>'
def shadow(x,y,w): return f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="4" fill="var(--ink)" opacity=".12"/>'
def phone(x,y,c=B):
    return f'<g transform="translate({x},{y})">{shadow(0,26,16)}<rect x="-14" y="-24" width="28" height="48" rx="6" fill="{c}"/><rect x="-10" y="-18" width="20" height="32" rx="2" fill="#fff"/><path d="M-6-8h12M-6-2h8M-6 4h10" stroke="{c}" stroke-width="2" opacity=".5"/><circle cy="19" r="2" fill="#fff"/></g>'
def pc(x,y,c=B):
    return f'<g transform="translate({x},{y})">{shadow(0,26,22)}<rect x="-26" y="-22" width="52" height="34" rx="4" fill="{c}"/><rect x="-22" y="-18" width="44" height="26" rx="2" fill="#fff"/><path d="M-4 12v8M-12 22h24" stroke="{c}" stroke-width="4" stroke-linecap="round"/></g>'
def game(x,y,c=B):
    return f'<g transform="translate({x},{y})">{shadow(0,20,24)}<path d="M-26 0c0-10 8-16 18-16h16c10 0 18 6 18 16 0 12-4 18-10 18-5 0-8-6-12-6h-8c-4 0-7 6-12 6-6 0-10-6-10-18z" fill="{c}"/><path d="M-15-4v8M-19 0h8" stroke="#fff" stroke-width="3" stroke-linecap="round"/><circle cx="13" cy="-3" r="2.6" fill="#fff"/><circle cx="19" cy="3" r="2.6" fill="#fff"/></g>'
def ap(x,y,c=G):
    return f'<g transform="translate({x},{y})">{shadow(0,24,22)}<path d="M-14-2v-14M14-2v-14" stroke="{c}" stroke-width="4" stroke-linecap="round"/><rect x="-24" y="-4" width="48" height="24" rx="8" fill="{c}"/><circle cx="-10" cy="8" r="2.5" fill="#fff"/><circle cx="0" cy="8" r="2.5" fill="#fff"/><path d="M-30-24a40 40 0 0 1 60 0M-22-30a30 30 0 0 1 44 0" stroke="{c}" stroke-width="3" fill="none" stroke-linecap="round" opacity=".55"/></g>'
def switch(x,y,c=G):
    ports="".join(f'<rect x="{-24+i*8}" y="3" width="5" height="5" rx="1" fill="#fff"/>' for i in range(7))
    return f'<g transform="translate({x},{y})">{shadow(0,20,32)}<rect x="-32" y="-14" width="64" height="30" rx="5" fill="{c}"/>{ports}<path d="M-14-6h18l-4-4M14-2h-18l4 4" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
def router(x,y,c=R):
    return f'<g transform="translate({x},{y})">{shadow(0,22,28)}<path d="M-28-6v14c0 8 12 14 28 14s28-6 28-14v-14" fill="{c}"/><ellipse cy="-6" rx="28" ry="12" fill="{c}"/><ellipse cy="-6" rx="28" ry="12" fill="#fff" opacity=".18"/><path d="M-14-6h28M0-14v16M-10-6l-4-4v8zM10-6l4-4v8z" stroke="#fff" stroke-width="2.4" fill="#fff" stroke-linecap="round"/></g>'
def server(x,y,c=A):
    return f'<g transform="translate({x},{y})">{shadow(0,30,22)}<rect x="-20" y="-28" width="40" height="56" rx="5" fill="{c}"/><path d="M-12-16h24M-12-6h24M-12 4h24" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".85"/><circle cx="10" cy="17" r="3" fill="#fff"/><path d="M-12 14l8 4-8 4z" fill="#fff"/></g>'
def cloud(x,y,c=K,s=1):
    return f'<g transform="translate({x},{y}) scale({s})"><path d="M-34 16h66a20 20 0 0 0 2-40 28 28 0 0 0-52 6 18 18 0 0 0-16 34z" fill="{c}" opacity=".16"/><path d="M-34 16h66a20 20 0 0 0 2-40 28 28 0 0 0-52 6 18 18 0 0 0-16 34z" fill="none" stroke="{c}" stroke-width="2.5"/></g>'
def building(x,y,c,h=56):
    win="".join(f'<rect x="{-14+(i%3)*10}" y="{-h+8+(i//3)*12}" width="6" height="7" fill="#fff" opacity=".85"/>' for i in range(3*((h-14)//12)))
    return f'<g transform="translate({x},{y})">{shadow(0,2,26)}<rect x="-20" y="{-h}" width="40" height="{h}" rx="2" fill="{c}"/>{win}</g>'
def house(x,y,c):
    return f'<g transform="translate({x},{y})">{shadow(0,2,30)}<path d="M-28-24 0-46 28-24v24h-56z" fill="{c}"/><rect x="-6" y="-16" width="12" height="16" fill="#fff"/></g>'
def parcel(x,y,n,c=A):
    return f'<g transform="translate({x},{y})">{shadow(0,18,18)}<rect x="-18" y="-16" width="36" height="32" rx="3" fill="{c}"/><path d="M-18-6h36M0-16v10" stroke="#fff" stroke-width="2" opacity=".7"/><rect x="-12" y="0" width="24" height="11" rx="2" fill="#fff"/><text x="0" y="9" text-anchor="middle" style="font:800 9px Figtree,sans-serif;fill:{c}">宛先</text><circle cx="13" cy="-11" r="7" fill="var(--ink)"/><text x="13" y="-7.5" text-anchor="middle" style="font:800 10px Figtree,sans-serif;fill:var(--card)">{n}</text></g>'
def env(x,y): return f'<g transform="translate({x},{y})"><rect x="-11" y="-8" width="22" height="16" rx="2" fill="#ff8a00"/><path d="M-11-8l11 9 11-9" stroke="#fff" stroke-width="1.8" fill="none"/></g>'
def svg(h,body,label): return f'<svg class="tbfig" viewBox="0 0 360 {h}" role="img" aria-label="{label}">{body}</svg>'
reduce='<animateMotion dur="7s" repeatCount="indefinite" rotate="0" path="{p}"/>'

# P1
p1=svg(250,"".join([cloud(180,128,"var(--sub)",1.5),lab(180,138,"ネットワーク",15),
 '<path d="M68 70 128 106M292 70 232 106M180 170 180 180" stroke="var(--ink)" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round"/>',
 phone(52,56),lab(52,104,"スマホ",13,700),pc(308,52),lab(308,100,"パソコン",13,700),game(180,214) .replace('translate(180,214)','translate(180,200)'),lab(180,236,"ゲーム機",13,700)]),"スマホ・パソコン・ゲーム機がネットワークでつながっている図")
# P2 journey
path="M50 62 L165 62 L292 62 L292 190 L165 190 L52 190"
p2=svg(290,"".join([
 '<rect x="8" y="8" width="344" height="122" rx="14" fill="#00a05a" opacity=".08"/>',lab(20,28,"家・会社の中",12.5,800,"#00a05a","start"),
 '<rect x="8" y="140" width="344" height="142" rx="14" fill="#3d4450" opacity=".07"/>',lab(20,160,"外の世界（インターネット）",12.5,800,"var(--sub)","start"),
 f'<path d="{path}" stroke="var(--ink)" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".25"/>',
 phone(50,62),lab(50,106,"スマホ",13),pill(50,124,"手紙を出す人",B),
 ap(165,66),lab(165,106,"アクセスポイント",13),pill(165,124,"郵便受け",G),
 switch(292,62),lab(292,98,"スイッチ",13),pill(292,116,"マンションの管理人",G),
 router(292,192),lab(292,236,"ルーター",13),pill(292,254,"郵便局",R),
 cloud(165,196,"var(--sub)",0.9),lab(165,240,"インターネット",13),
 server(52,188),lab(52,240,"サーバー",13),pill(52,258,"お店・図書館",A),
 '<g class="mv">'+env(0,0)+reduce.format(p=path)+'</g>']),"スマホからサーバーまで、データが機器を順に通っていく図")
# P3 LAN WAN
p3=svg(300,"".join([
 '<rect x="10" y="10" width="340" height="120" rx="14" fill="#00a05a" opacity=".08"/>',
 house(70,104,G),pc(150,88),pc(270,88),switch(210,112),'<path d="M150 112 178 112M270 112 242 112" stroke="var(--ink)" stroke-width="3"/>',
 lab(70,34,"LAN",22),lab(70,54,"せまい範囲",12.5,700,"var(--sub)"),lab(210,30,"家や会社の中",13,700),
 '<rect x="10" y="144" width="340" height="146" rx="14" fill="#0a5cff" opacity=".07"/>',
 lab(180,172,"WAN",22),lab(180,192,"遠く離れた場所どうし",12.5,700,"var(--sub)"),
 building(70,262,B,64),lab(70,282,"東京本社",13),building(290,262,B,48),lab(290,282,"大阪支社",13),
 '<path d="M96 232 Q180 206 264 232" stroke="var(--ink)" stroke-width="3" stroke-dasharray="6 6" fill="none"/>',lab(180,256,"何百kmも離れている",12.5,700,"var(--sub)")]),"せまい範囲のLANと、遠く離れた場所をつなぐWANの図")
# P4 parcels
p4=svg(310,"".join([
 '<rect x="16" y="22" width="92" height="64" rx="6" fill="var(--ink)"/>','<path d="M50 40v28l24-14z" fill="var(--card)"/>',lab(62,104,"大きな動画",13),
 '<path d="M118 54h34" stroke="var(--ink)" stroke-width="3"/><path d="M152 48l10 6-10 6z" fill="var(--ink)"/>',
 parcel(184,52,1),parcel(226,52,2),parcel(268,52,3),parcel(310,52,4),lab(245,104,"小分けにして、1つずつ宛先を書く",12.5,700,"var(--sub)"),
 '<path d="M10 130h340" stroke="var(--line)" stroke-width="2"/>',lab(180,154,"カプセル化 ＝ 何重にも包む",15),
 '<rect x="60" y="170" width="240" height="124" rx="10" fill="#e6261f" opacity=".12" stroke="#e6261f" stroke-width="2"/>',lab(70,190,"段ボール：MACアドレス（L2）",12.5,800,R,"start"),
 '<rect x="90" y="202" width="180" height="80" rx="8" fill="#0a5cff" opacity=".12" stroke="#0a5cff" stroke-width="2"/>',lab(100,222,"封筒：IPアドレス（L3）",12.5,800,B,"start"),
 '<rect x="140" y="234" width="80" height="38" rx="6" fill="#ffb400"/>',lab(180,258,"データ",13,800,"#111")]),"大きな動画を小包に分け、データを封筒と段ボールで包んでいく図")
# P5 OSI tower
floors=[(7,"アプリケーション層","HTTP・DNS",0),(6,"プレゼンテーション層","",0),(5,"セッション層","",0),(4,"トランスポート層","TCP・UDP",1),(3,"ネットワーク層","ルーター・IPアドレス",1),(2,"データリンク層","スイッチ・MACアドレス",1),(1,"物理層","ケーブル・電波",1)]
cols={4:A,3:R,2:G,1:B}
fl=""
for k,(n,name,ex,imp) in enumerate(floors):
    y=40+k*38;c=cols.get(n,"#9aa4b2")
    fl+=f'<rect x="20" y="{y}" width="296" height="32" rx="6" fill="{c}" opacity="{0.9 if imp else 0.18}"/>'
    fl+=f'<text x="34" y="{y+21}" style="font:800 14px Figtree,sans-serif;fill:{"#fff" if imp else "var(--sub)"}">{n}</text>'
    fl+=f'<text x="56" y="{y+21}" style="font:{"800" if imp else "600"} 13.5px Figtree,\'Hiragino Sans\',sans-serif;fill:{"#fff" if imp else "var(--sub)"}">{name}</text>'
    if ex: fl+=f'<text x="306" y="{y+21}" text-anchor="end" style="font:700 12.5px Figtree,\'Hiragino Sans\',sans-serif;fill:{"#fff" if imp else "var(--sub)"}">{ex}</text>'
p5=svg(320,lab(180,24,"7つの係（層）に分けて考える",15)+fl+'<path d="M326 154v148" stroke="var(--ink)" stroke-width="3"/>'+f'<text x="333" y="190" style="font:800 12.5px Figtree,\'Hiragino Sans\',sans-serif;fill:var(--ink);writing-mode:vertical-rl">ここが大事</text>',"OSI参照モデルの7つの層。1から4層が色付きで大事な層")
# P7 summary
def row(y,icon,t1,t2,c): return f'<rect x="10" y="{y}" width="340" height="78" rx="12" fill="{c}" opacity=".1"/>{icon}{lab(112,y+32,t1,15,800,"var(--ink)","start")}{lab(112,y+56,t2,13,600,"var(--sub)","start")}'
sc=lambda x,y,k,g:f'<g transform="translate({x},{y}) scale({k})">{g}</g>'
p7=svg(270,"".join([row(8,sc(38,46,.7,switch(0,0))+sc(84,48,.62,router(0,0)),"スイッチ＝建物の中","ルーター＝建物の外へ",G),
 row(96,sc(38,154,.62,house(0,0,G))+sc(84,154,.7,building(0,0,B,44)),"LAN＝せまい範囲","WAN＝遠く離れた場所どうし",B),
 row(184,sc(40,224,.8,parcel(0,0,1))+sc(82,224,.8,parcel(0,0,2)),"データは小包（パケット）","ラベルを貼って包む＝カプセル化",A)]),"今日のまとめ3つ")
pages=[
 {"t":"ネットワークって何？","svg":p1,"b":"ネットワークとは、<b>機器と機器をつないで、データをやりとりできるようにしたもの</b>です。YouTubeを見るのも、LINEを送るのも、オンラインゲームで遊ぶのも、全部ネットワークのおかげです。","p":"CCNAは、ネットワークを「作る・管理する・直す」ための基本を学ぶ資格です。"},
 {"t":"データが届くまでの旅","svg":p2,"b":"YouTubeの動画は、<b>スマホ → アクセスポイント → スイッチ → ルーター → インターネット → サーバー</b>の道を通って届きます（実際の動画は、この逆向きにサーバーからスマホへ流れてきます）。下の色のラベルは、町の郵便にたとえたときの役割です。","p":"スイッチは「建物の中」担当、ルーターは「建物の外へ」担当。CCNAで一番よく出る区別です。"},
 {"t":"LANとWAN","svg":p3,"b":"<b>LAN</b>（Local Area Network）は、家や会社の中のような<b>せまい範囲</b>のネットワークです。<b>WAN</b>（Wide Area Network）は、東京の本社と大阪の支社のように<b>遠く離れた場所どうし</b>をつなぐネットワークです。","p":"インターネットは、世界中のネットワークをつないだ、巨大なWANのようなものです。"},
 {"t":"データは「小包」にして送る","svg":p4,"b":"大きなデータも一気には送らず、<b>小さく分けて、1つずつに宛先を書いて</b>送ります。この小分けにしたデータを<b>パケット</b>や<b>フレーム</b>と呼びます。宛先などのラベルを貼って包んでいくことを<b>カプセル化</b>と言います。","p":"封筒（IPアドレス）に入れて、さらに段ボール（MACアドレス）に入れる。何重にも包むイメージです。"},
 {"t":"OSI参照モデル ＝ 仕事の分担表","svg":p5,"b":"ネットワークの仕事を<b>7つの係（層）</b>に分けて考えたものが、<b>OSI</b>（Open Systems Interconnection）<b>参照モデル</b>です。全部を覚える必要はありません。CCNAで大事なのは<b>第1層〜第4層</b>です。","p":"「L2スイッチ」のL2は第2層のこと。L2＝スイッチとMACアドレス、L3＝ルーターとIPアドレス。"},
 {"t":"小テスト","quiz":{"q":"同じ建物の中で、宛先の機器にだけデータを届ける機器はどれ？","o":[["スイッチ",switch(0,0)],["ルーター",router(0,0)],["サーバー",server(0,0)]],"a":0,"e":"正解は<b>スイッチ</b>。建物の外へ道を選んで届けるのはルーター、サービスを提供するのはサーバーです。"}},
 {"t":"今日のまとめ","svg":p7,"b":"次回は「住所のしくみ」。IPアドレスとMACアドレスを学びます。","p":"一問一答の「入門」で、今日の内容の問題を解いて確かめましょう。"}]
rec={"r":"TB","lt":"kl1","n":1,"t":"ネットワークって何？","pages":pages}
json.dump(rec,open("/home/claude/lecture/tb01.json","w"),ensure_ascii=False)
print("ok",len(json.dumps(rec)))
