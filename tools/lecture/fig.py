from lib import *
mono="ui-monospace,Menlo,monospace"
def num(x,y,t,c="var(--ink)",size=20,anchor="middle"): return f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="font:800 {size}px {mono};fill:{c}">{t}</text>'
W8=[128,64,32,16,8,4,2,1]
def bits(y,b,c=B,x0=44,w=36,show_w=False,lbl=None):
    s=""
    if show_w: s+="".join(num(x0+k*w+w/2-2,y-8,v,"var(--sub)",12) for k,v in enumerate(W8))
    for k,ch in enumerate(b):
        on=ch=="1";s+=f'<rect x="{x0+k*w}" y="{y}" width="{w-4}" height="32" rx="6" fill="{c if on else "var(--line)"}"/>'+num(x0+k*w+w/2-2,y+23,ch,"#fff" if on else "var(--sub)",17)
    if lbl: s+=lab(x0+8*w+10,y+22,lbl,16,800,"var(--ink)","start")
    return s
def tw(t): return sum(0.62 if ord(c)<128 else 1 for c in t)
def wrap(t,mx):
    out=[];cur=""
    for ch in t:
        if tw(cur+ch)>mx: out.append(cur);cur=ch
        else: cur+=ch
    if cur: out.append(cur)
    return out
def rows(items,y0=6,h=None,gap=6):
    s="";y=y0
    for (ic,t1,t2,c) in items:
        x=92 if ic else 24;avail=(346-x)
        ts=14.5 if tw(t1)*14.5<=avail else max(11.5,avail/tw(t1))
        sub=wrap(t2,avail/12.5) if t2 else []
        hh=max(h or 0,26+ts+len(sub)*17)
        s+=f'<rect x="10" y="{y}" width="340" height="{hh}" rx="12" fill="{c}" opacity=".1"/>'
        if ic: s+=ic.replace("@Y@",str(y+hh/2))
        ty=y+hh/2-(len(sub)*17)/2+ts/2-2
        s+=lab(x,ty,t1,round(ts,1),800,"var(--ink)","start")
        for k,ln in enumerate(sub): s+=lab(x,ty+19+k*17,ln,12.5,600,"var(--sub)","start")
        y+=hh+gap
    return s,y
def badge(x,y,t,c,w=56):
    return f'<rect x="{x-w/2}" y="{y-16}" width="{w}" height="32" rx="8" fill="{c}"/><text x="{x}" y="{y+6}" text-anchor="middle" style="font:800 15px {mono};fill:#fff">{t}</text>'
def term(x,y,w,h,lines,title="Router"):
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#1d2330"/><circle cx="{x+14}" cy="{y+13}" r="4" fill="#ff5f57"/><circle cx="{x+28}" cy="{y+13}" r="4" fill="#febc2e"/><circle cx="{x+42}" cy="{y+13}" r="4" fill="#28c840"/>'
    for k,(t,c) in enumerate(lines):
        s+=f'<text x="{x+12}" y="{y+42+k*22}" style="font:700 14px {mono};fill:{c}">{t}</text>'
    return s
