import json,sys
p='/home/claude/site/data.json';L=open(p).read().split('\n')
recs={}
for n in sys.argv[1:]:
    r=json.load(open(f'/home/claude/lecture/l{int(n):02d}/tb.json'));recs[r['n']]=r
keep=[];tbs=[]
for l in L:
    if '"r":"TB"' in l:
        o=json.loads(l.rstrip(','));tbs.append(o)
    else: keep.append(l)
d={o['n']:o for o in tbs};d.update(recs)
i=next(k for k,l in enumerate(keep) if '"r":"O"' in l)
for n in sorted(d,reverse=True): keep.insert(i,json.dumps(d[n],ensure_ascii=False,separators=(',',':'))+',')
open(p,'w').write('\n'.join(keep));json.load(open(p));print('installed',sorted(d))
