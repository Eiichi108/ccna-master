# CCNA Master（公開版）

CCNA 200-301 の学習サイト。GitHub Pages で公開している：https://eiichi108.github.io/ccna-master/
静的サイト（index.html が data.json と audio/*.mp3 を読み込むだけ）。data.json は `src/` から作る。

## 大事なルール
- 問題・教科書・授業台本は**すべてオリジナル**。既存の問題集（特に市販・有料サイトの問題）の文面・図・数値をまねしたものは入れない。
- 作業者の個人用サイト（別の問題集の問題を含む版）は claude.ai のアーティファクトとして別管理。このリポジトリには入れない。
- 文章は初心者向けのやさしい日本語。略語は初出で正式名を添える。ただし**本番レベル（lv 2）の問題文**は、本番に近い言い回しにしてよい（解説・覚え方はやさしいまま）。基準は `src/questions/INSTRUCTIONS.md`。
- **push するとすぐ公開される**。commit と push はセットで行う（ユーザーの OK をもらったら、commit してそのまま push まで）。
- **data.json は直接編集しない**。`src/` を直して `python tools/build.py` で作り直す。

## ファイル構成
- `src/` … 編集するのはここ
  - `lessons/lNN.json` … 第NN回の教科書 `pages`（`t` 見出し、`svg` 図、`b` 本文、`p` ポイント、`quiz` 小テスト）と授業 `cls`（`lines`: `sp` 先生/生徒、`t` 字幕、`y` 読み上げ用の読み、`w:1` 確認の問題で止まる行（1回に何か所あってもよい。止まる場面のページは `quiz`）、`sc` 場面。`seg` 各行の [開始秒, 長さ]、`a` 音声）。セリフは1行＝1つのオブジェクト
  - `questions/lNN.json` … 第NN回の問題。形式と作り方のルールは `src/questions/INSTRUCTIONS.md`。**問題IDの番号（P13-01 の 13）は旧50回のときのもので、今の回とは一致しない**（進捗がIDで保存されているので変えない）。どの回かはファイルで決まる。旧→新の対応は `map_from_old.json`
  - `lessons/DESIGN.md` … 授業（全81回）の設計書。新しい回を作るときの決まり（形・長さ・生徒の行30%以上など）
  - `base/` … `glossary`（用語集 G）、`figures`（図解レッスン L）、`commands`（コマンド練習 C）、`labs`（設定演習 B）、`guides`（図・出力の読み方ガイド RG）、`classes`（各回一覧 CP）、`domains`（分野 D）
- `data.json` … build で作る出力（1行に圧縮）。レコードの種類は `r` で区別し、Q（問題）・O（出題順）・QP（問題→[回, ページ]）と、CP・L の `q`（問題IDの一覧）は問題から自動で作られる（src/base 側の `q` は使われない）
- `index.html` … アプリ本体（HTML/CSS/JS を1ファイルに）。進捗は localStorage（キー `ccna_master_pub1`）に保存
- `audio/lNN.mp3` … 第NN回の授業音声（1回1本）。字幕との対応は `cls.seg`
- `tools/` … `build.py`（src→data.json、最後に check も実行）、`check.py`、`srcio.py`（src の読み書き・整形の共通部品）、`rd.py`（読み `y` の変換表 `auto()`）、`audio/voicevox_build.py`（授業音声づくり）

## よくある作業
- **問題を直す・追加する**：`src/questions/lNN.json` を編集 → `python tools/build.py`
- **教科書を直す**：`src/lessons/lNN.json` の `pages` を編集（図は SVG の文字列）→ `python tools/build.py`
- **字幕（t）には読み仮名を書かない**。「/24」「Gi0/1」「::」「192.168.1.1」のように表記で書き、読みは `y`（`tools/rd.py` の `auto()` が作る）に任せる。IPアドレスは「の」でつないで読む（192の168の1の1）
- **授業のセリフを直す**：`src/lessons/lNN.json` の `cls.lines` を編集（読みが特殊なら `y` も。`tools/rd.py` の `auto()` で作れる）→ 音声を作り直す：
  `python tools/audio/voicevox_build.py NN`（VOICEVOX を起動しておく。ffmpeg と numpy が必要。seg の保存と build まで自動）
  セリフの行数を変えたのに音声を作り直さないと、check で「seg と lines の数が違う」になる
- **用語集などを直す**：`src/base/*.json` を編集 → `python tools/build.py`
- src を Python で書き換えるときは `srcio.save()` を使うと、今の整形のまま保存できる
- 動作確認：`python -m http.server` → http://localhost:8000/

## 注意
- Windows の PowerShell でファイルを表示すると日本語が文字化けすることがある。Read ツールか、`python -X utf8` を使う。
- 音声は VOICEVOX（四国めたん／ずんだもん、各ノーマル）。サイトにクレジット表記を残すこと。
