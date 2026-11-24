import json,sys,shutil,os
U='/mnt/user-data/uploads/Documents/CCNA授業/mp3/'
for n in sys.argv[1:]:
    n=int(n);t=f'/home/claude/lecture/l{n:02d}/tb.json';r=json.load(open(t))
    seg=json.load(open(f'{U}l{n:02d}.json'));assert len(seg)==len(r['cls']['lines']),(n,len(seg),len(r['cls']['lines']))
    r['cls']['seg']=[[round(a,3),round(b,3)] for a,b in seg];r['cls']['a']=f'audio/l{n:02d}/'
    json.dump(r,open(t,'w'),ensure_ascii=False);shutil.copy(f'{U}l{n:02d}.mp3',f'/home/claude/site/audio/l{n:02d}.mp3');print('ok',n)
os.system('python3 /home/claude/lecture/install.py '+' '.join(sys.argv[1:]))
