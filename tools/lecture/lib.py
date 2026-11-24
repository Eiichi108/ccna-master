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


def sc(x,y,k,g): return f'<g transform="translate({x},{y}) scale({k})">{g}</g>'
def firewall(x,y,c="#b5482f"):
    bricks="".join(f'<rect x="{-26+((r%2)*8)+i*17}" y="{-22+r*11}" width="15" height="9" rx="1.5" fill="#fff" opacity=".28"/>' for r in range(4) for i in range(3) if -26+((r%2)*8)+i*17+15<=28)
    return f'<g transform="translate({x},{y})">{shadow(0,24,30)}<rect x="-28" y="-24" width="56" height="46" rx="4" fill="{c}"/>{bricks}<path d="M10-34c6 6 10 10 10 16a10 10 0 0 1-20 0c0-4 3-7 5-9 0 4 2 6 4 6 0-5-1-9 1-13z" fill="#ff8a00"/></g>'
def tag(x,y,t,c,w=None):
    w=w or len(t)*8.6+20
    return f'<g transform="translate({x},{y})"><rect x="{-w/2}" y="-13" width="{w}" height="26" rx="6" fill="var(--card)" stroke="{c}" stroke-width="2.5"/><text y="5" text-anchor="middle" style="font:800 13.5px ui-monospace,Menlo,monospace;fill:{c}">{t}</text></g>'
def arrow(x1,y1,x2,y2,c="var(--ink)",w=3):
    import math
    a=math.atan2(y2-y1,x2-x1);hx=x2-9*math.cos(a);hy=y2-9*math.sin(a)
    p1=(hx+5*math.sin(a),hy-5*math.cos(a));p2=(hx-5*math.sin(a),hy+5*math.cos(a))
    return f'<path d="M{x1} {y1}L{hx:.1f} {hy:.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/><path d="M{x2} {y2}L{p1[0]:.1f} {p1[1]:.1f}L{p2[0]:.1f} {p2[1]:.1f}z" fill="{c}"/>'
def laptop(x,y,c=B):
    return f'<g transform="translate({x},{y})">{shadow(0,14,26)}<rect x="-20" y="-20" width="40" height="27" rx="3" fill="{c}"/><rect x="-16" y="-16" width="32" height="19" rx="1.5" fill="#fff"/><path d="M-26 9h52l-4 5h-44z" fill="{c}"/></g>'
