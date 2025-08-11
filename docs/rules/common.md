# 共通ルール（全ファイル共通）

## 基本
- **glossary.csv を最優先**（訳さない/固定訳の双方を指示）
- **固有名詞は英語固定（keep_en）**：hero/item/ability/lore_proper/aliases
  ※例外で日本語にしたい時だけ `policy=translate` を `glossary.csv` に追加
- **プレースホルダー/タグ非改変**：`%s`, `%d`, `%1$s`, `%MODIFIER_*%%%`, `{s:...}`, `{d:...}`, `<h1>`, `<br>`, `<font ...>` など
- **Key/Value形式**は **Key不変・Valueのみ翻訳**

## 書式・数値・単位
- 半角：数字/英字/コロン/カンマ/ピリオド（例：`クールダウン: 20秒`）
- 単位は日本語で続け書き（`20 秒`× → `20秒`○）
- UI文字量：英語比 **×1.4** を警戒域（超える場合は簡潔に言い換え）

## glossary.csv 仕様（要旨）
- 列：`en, ja, policy, category, match, notes`
- policy：`keep_en`（訳さない）/ `translate`（訳語固定）
- match：`exact` > `word` > `ci`（優先順）＋**最長一致優先**（同点は行順）

## 変更管理
- 訳の統一変更はPRで理由・影響範囲を記載
- 既存訳と衝突する場合はまず既存優先、要議論
