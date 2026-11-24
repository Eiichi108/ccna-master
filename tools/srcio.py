"""src/ のファイルを読み書きする共通の部品（build.py と audio/voicevox_build.py が使う）。
書き出しは「人とエディタが読みやすい形」にそろえる：
  - 授業のセリフ（sp を持つ行）・短いオブジェクト・数値や文字列だけの配列は1行に
  - それ以外は1項目ずつ改行
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
DATA = os.path.join(ROOT, "data.json")

# src/base/ のファイル名と、data.json のレコードの種類（r）の対応
BASE = {"D": "domains", "L": "figures", "G": "glossary", "C": "commands",
        "B": "labs", "CP": "classes", "RG": "guides"}


def _one(o):
    return json.dumps(o, ensure_ascii=False, separators=(", ", ": "))


def _inline(o):
    if isinstance(o, list):
        if all(not isinstance(v, (dict, list)) for v in o):
            return True  # 数値や文字列だけの配列
        return all(isinstance(v, list) and _inline(v) for v in o) and len(_one(o)) <= 100
    if isinstance(o, dict):
        return "sp" in o or len(_one(o)) <= 160
    return True


def dumps(o, ind=0):
    if _inline(o):
        return _one(o)
    pad, pad1 = " " * ind, " " * (ind + 1)
    if isinstance(o, list):
        return "[\n" + ",\n".join(pad1 + dumps(v, ind + 1) for v in o) + "\n" + pad + "]"
    return "{\n" + ",\n".join(pad1 + json.dumps(k, ensure_ascii=False) + ": " + dumps(v, ind + 1)
                             for k, v in o.items()) + "\n" + pad + "}"


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, o):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(dumps(o) + "\n")


def lesson_path(n):
    return os.path.join(SRC, "lessons", f"l{n:02d}.json")


def base_path(r):
    return os.path.join(SRC, "base", BASE[r] + ".json")
