"""授業の音声を VOICEVOX から直接作る（GUIの操作は不要）。
前提:
  - VOICEVOX（アプリ または エンジン）が起動していること（http://127.0.0.1:50021）
  - ffmpeg がインストールされていて PATH が通っていること
  - pip install numpy
使い方:
  python tools/audio/voicevox_build.py 12        # 第12回の音声を作り直す
  python tools/audio/voicevox_build.py 3 7 12    # 複数回
  python tools/audio/voicevox_build.py all       # 全50回
処理:
  src/lessons/lNN.json の cls.lines を1行ずつ読み上げ（読みは y、なければ t）
  → 行ごとに音量をそろえる → 0.35秒の間をはさんで1本につなぐ
  → audio/lNN.mp3 を書き出し、cls.seg（各行の開始秒・長さ）を src/lessons/lNN.json に保存
  → 最後に tools/build.py を実行して data.json に反映
"""
import json, os, sys, io, wave, subprocess, urllib.request, urllib.parse, re
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import srcio

ROOT = srcio.ROOT
API = os.environ.get("VOICEVOX_URL", "http://127.0.0.1:50021")
SR = 24000          # サンプリングレート
GAP = 0.35          # 行と行の間（秒）
T = -17.2           # 目標の音量（dB）
VOICE = {"先生": ("四国めたん", "ノーマル"), "生徒": ("ずんだもん", "ノーマル")}

def http(path, data=None, params=None):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, data=data, method="POST" if data is not None or path != "/speakers" else "GET",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

def speaker_ids():
    sp = json.loads(http("/speakers"))
    ids = {}
    for role, (name, style) in VOICE.items():
        for s in sp:
            if s["name"] == name:
                for st in s["styles"]:
                    if st["name"] == style: ids[role] = st["id"]
        if role not in ids: sys.exit(f"VOICEVOXに {name}({style}) が見つかりません")
    return ids

def chunks(text, n=100):
    """長い文は「。」などで区切って読ませる（長文は不安定になりやすいため）"""
    if len(text) <= n: return [text]
    parts, cur = [], ""
    for p in re.split(r"(?<=[。！？])", text):
        if cur and len(cur) + len(p) > n: parts.append(cur); cur = p
        else: cur += p
    if cur: parts.append(cur)
    return parts

def synth(text, sid):
    out = []
    for t in chunks(text):
        q = json.loads(http("/audio_query", b"", {"text": t, "speaker": sid}))
        q["outputSamplingRate"] = SR; q["outputStereo"] = False
        w = wave.open(io.BytesIO(http("/synthesis", json.dumps(q).encode(), {"speaker": sid})))
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        out.append(x)
    return np.concatenate(out)

def lvl(x):
    a = np.abs(x); m = a > 0.003
    y = x[m] if m.sum() > 100 else x
    return 20 * np.log10(np.sqrt((y ** 2).mean()) + 1e-9)

def fix(x):
    """行ごとに音量を T dB にそろえ、大きすぎる所はやわらかく抑える"""
    g = max(-8, min(30, T - lvl(x))); y = x * 10 ** (g / 20)
    pk = np.abs(y).max()
    if pk > 0.95: y = np.tanh(y / 0.95) * 0.95 if pk < 1.3 else y * (0.95 / pk)
    return y

def build(rec, ids):
    n = rec["n"]; c = rec["cls"]; parts, seg, cum = [], [], 0
    gap = np.zeros(int(GAP * SR), np.float32)
    for i, ln in enumerate(c["lines"], 1):
        x = fix(synth(ln.get("y") or ln["t"], ids[ln["sp"]])).astype(np.float32)
        seg.append([round(cum / SR, 3), round(len(x) / SR, 6)])
        parts += [x, gap]; cum += len(x) + len(gap)
        print(f"\r第{n}回 {i}/{len(c['lines'])}", end="", flush=True)
    y = np.concatenate(parts)
    mp3 = os.path.join(ROOT, "audio", f"l{n:02d}.mp3")
    subprocess.run(["ffmpeg", "-v", "quiet", "-y", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-i", "-",
                    "-c:a", "libmp3lame", "-b:a", "48k", mp3], input=y.tobytes(), check=True)
    c["seg"] = seg; c["a"] = f"audio/l{n:02d}/"
    print(f"  → audio/l{n:02d}.mp3（{cum / SR / 60:.1f}分）")

def main():
    args = sys.argv[1:]
    if not args: sys.exit(__doc__)
    ns = list(range(1, 51)) if args == ["all"] else [int(a) for a in args]
    ids = speaker_ids()
    for n in ns:
        rec = srcio.load(srcio.lesson_path(n))
        build(rec, ids)
        srcio.save(srcio.lesson_path(n), rec)  # 1回ごとに保存
    sys.exit(subprocess.call([sys.executable, "-X", "utf8", os.path.join(ROOT, "tools", "build.py")]))

if __name__ == "__main__":
    main()
