import json,subprocess,numpy as np,os,sys,shutil
S='/home/claude/site/';SR=24000;T=-17.2
os.makedirs('/home/claude/work/abak',exist_ok=True)
def dec(p):
    b=subprocess.run(['ffmpeg','-v','quiet','-i',p,'-f','f32le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
    return np.frombuffer(b,np.float32).copy()
def enc(x,p):
    subprocess.run(['ffmpeg','-v','quiet','-y','-f','f32le','-ac','1','-ar',str(SR),'-i','-','-c:a','libmp3lame','-b:a','48k',p],input=x.astype(np.float32).tobytes(),check=True)
def lvl(x):
    a=np.abs(x);m=a>0.003
    y=x[m] if m.sum()>100 else x
    return 20*np.log10(np.sqrt((y**2).mean())+1e-9)
def fix(x):
    g=T-lvl(x);g=max(-8,min(30,g));k=10**(g/20);y=x*k
    pk=np.abs(y).max()
    if pk>0.95: y=np.tanh(y/0.95*1.0)*0.95 if pk<1.3 else y*(0.95/pk)
    return y,g
d=json.load(open(S+'data.json'));log=[]
only=set(map(int,sys.argv[1:])) if len(sys.argv)>1 else None
for r in d:
    if r.get('r')!='TB' or 'cls' not in r: continue
    n=r['n'];c=r['cls']
    if only and n not in only: continue
    if c.get('seg'):
        p=S+f'audio/l{n:02d}.mp3';b=f'/home/claude/work/abak/l{n:02d}.mp3'
        if not os.path.exists(b): shutil.copy(p,b)
        x=dec(b)
        for a,du in c['seg']:
            i0=int(a*SR);i1=min(len(x),int((a+du)*SR))
            x[i0:i1],g=fix(x[i0:i1]);log.append(g)
        enc(x,p)
    else:
        for i in range(len(c['lines'])):
            p=S+f'audio/l{n:02d}/{i+1:03d}.mp3'
            if not os.path.exists(p): continue
            b=f'/home/claude/work/abak/l{n:02d}_{i+1:03d}.mp3'
            if not os.path.exists(b): shutil.copy(p,b)
            y,g=fix(dec(b));log.append(g);enc(y,p)
    print(n,end=' ',flush=True)
log=np.array(log);print();print('gains',np.percentile(log,[0,10,50,90,100]).round(1))
