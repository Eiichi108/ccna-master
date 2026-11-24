# CCNA Master（公開版）

CCNA 200-301 の学習サイト。GitHub Pages で公開している：https://eiichi108.github.io/ccna-master/
ビルド不要の静的サイト（index.html が data.json と audio/*.mp3 を読み込むだけ）。

## 大事なルール
- 問題・教科書・授業台本は**すべてオリジナル**。既存の問題集（特に市販・有料サイトの問題）の文面・図・数値をまねしたものは入れない。
- 作業者の個人用サイト（別の問題集の問題を含む版）は claude.ai のアーティファクトとして別管理。このリポジトリには入れない。
- 文章は初心者向けのやさしい日本語。略語は初出で正式名を添える。

## ファイル構成
- `index.html` … アプリ本体（HTML/CSS/JS を1ファイルに）。進捗は localStorage（キー `ccna_master_pub1`）に保存。
- `data.json` … 全データ。レコードの種類は `r` で区別：
  - `Q` 問題（`k`: one / multi / sel / match / order、`h:1` なら t/e/o の HTML をそのまま表示、`x` 図・出力、`rd` 図の読み方、`rg` 読み方ガイドの種類）
  - `TB` 各回（1〜50）の教科書 `pages` と授業 `cls`（`lines`: `sp` 先生/生徒、`t` 字幕、`y` 読み上げ用の読み、`w:1` 小テストで止まる行、`seg` 各行の [開始秒, 長さ]）
  - `CP` 各回の一覧と問題ID、`QP` 問題→[回, 教科書ページ]、`O` 出題順、`RG` 図・出力の読み方ガイド、`L` 図解レッスン、`G` 用語集、`C`/`B` コマンド練習、`D` 分野
- `audio/lNN.mp3` … 第NN回の授業音声（1回1本）。字幕との対応は `cls.seg`。
- `tools/` … 作業用

## よくある作業
- **問題を直す・追加する**：`tools/questions/lNN.json`（第NN回の問題。形式は `tools/questions/INSTRUCTIONS.md`）を編集 →
  `python tools/build_questions.py` → `python tools/check.py`
- **授業のセリフを直す**：data.json の `TB` → `cls.lines` を直す（読みが特殊なら `y` も）→ その回の音声を作り直す：
  `python tools/audio/voicevox_build.py NN`（VOICEVOX を起動しておく。ffmpeg と numpy が必要）
  読み方の変換表は `tools/lecture/rd.py`（`auto()`）。新しい行の `y` を作るときに使える。
- **教科書を直す**：data.json の `TB` → `pages` を直接編集（図は SVG の文字列）。
- 動作確認：`python -m http.server` → http://localhost:8000/

## 注意
- `tools/lecture/` の lessonNN.py などは最初に台本・教科書を作ったときのスクリプトで、**今の data.json より古い**（あとで直した内容が入っていない）。参考用。中のパスも旧環境（/home/claude/...）のまま。正しい最新データは常に data.json。
- 音声は VOICEVOX（四国めたん／ずんだもん、各ノーマル）。サイトにクレジット表記を残すこと。
