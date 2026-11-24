# write plan.json into data.json CP record
import json
plan=json.load(open('/home/claude/work/plan.json'))
p='/home/claude/site/data.json';L=open(p).read().split('\n')
L=[l for l in L if '"r":"CP"' not in l]
i=next(k for k,l in enumerate(L) if '"r":"O"' in l)
L.insert(i,json.dumps({"r":"CP","list":plan},ensure_ascii=False,separators=(',',':'))+',')
open(p,'w').write('\n'.join(L));json.load(open(p));print('cp ok')
