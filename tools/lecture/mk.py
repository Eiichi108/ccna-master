import json,sys
sys.path.insert(0,"/home/claude/lecture")
from rd import auto
TEA="四国めたん(ノーマル)";STU="ずんだもん(ノーマル)"
def build(n,lt,title,dom_label,scenes,L,pages,wait_line):
    L=[(a,b,c,d if d else (auto(c) if auto(c)!=c else None)) for a,b,c,d in L]
    names={"先生":TEA,"生徒":STU}
    wait_line=next(i for i,x in enumerate(L,1) if x[2].startswith("ここで小テスト"))
    d=f"/home/claude/lecture/l{n:02d}";import os;os.makedirs(d,exist_ok=True)
    with open(f"{d}/第{n:02d}回_VOICEVOX読み込み用.txt","w",encoding="utf-8") as f:
        for sc,sp,t,r in L: f.write(f"{names[sp]},{r or t}\n")
    with open(f"{d}/第{n:02d}回_台本（確認用）.txt","w",encoding="utf-8") as f:
        f.write(f"CCNA Master 授業 第{n}回「{title}」（{dom_label}）\n先生：四国めたん（ノーマル）／生徒：ずんだもん（ノーマル）\n");cur=None
        for i,(sc,sp,t,r) in enumerate(L,1):
            if sc!=cur: f.write(f"\n■ シーン{sc}　{scenes[sc-1]}\n");cur=sc
            f.write(f"{i:03d}　{sp}：{t}\n")
    lines=[dict(sc=sc,sp=sp,t=t,**({"w":1} if i==wait_line else {})) for i,(sc,sp,t,r) in enumerate(L,1)]
    rec={"r":"TB","lt":lt,"n":n,"t":title,"pages":pages,"cls":{"a":f"audio/l{n:02d}/","lines":lines}}
    json.dump(rec,open(f"{d}/tb.json","w"),ensure_ascii=False)
    tot=sum(len(r or t) for _,_,t,r in L);print(n,len(L),"lines","~%.1f min"%(tot/330),"pages",len(pages))
