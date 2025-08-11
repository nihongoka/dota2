# Ability ファイル用ルール（abilities_{english,japanese}.txt.json）

## 文体
- **常体（〜する）**。短文は体言止め可（例：`効果時間: 3秒`）

## ラベル既定訳（例）
- `Cooldown` → **クールダウン**  
- `Mana Cost / AbilityManaCost` → **マナコスト**  
- `Cast Range / AbilityCastRange` → **キャスト範囲**（※「射程」に統一する場合はプロジェクト合意で）  
- `Range`/`AoE` → **範囲**、`Radius` → **半径**（文脈で選択）  
- `Duration` → **効果時間**  
- アビリティ挙動：`Passive` **パッシブ** / `AutoCast` **オートキャスト** / `Toggle` **トグル** / `Channeled` **チャネリング**  
- ％先頭ラベル：`%Damage Reduction` → **%ダメージ軽減**、`%Bonus Damage` → **%ボーナスダメージ**

## メカニクス・ステータス（例）
- **Basic Dispel** 基本ディスペル / **Strong Dispel** 強化ディスペル  
- **Spell Immunity / spell immune** スペル耐性  
- **Status/Magic/Slow Resistance** 異常/魔法/スロー耐性  
- **Movement Speed / Attack Speed / Armor / Damage** 移動速度 / 攻撃速度 / アーマー / ダメージ  
- **Health/HP** は **HP**（英略記固定）

## プレースホルダー/タグ
- **厳守**：`%s`, `%d`, `%1$s`, `%MODIFIER_*%%%`, `{s:*}`, `{d:*}`, `<...>` の**位置・個数・大小**  
- **SearchAlias**（もし該当キーがあれば）：**英語小文字＋セミコロン**、非翻訳（例：`qb;quelling blade`）

## 固有名詞
- ヒーロー/アイテム/スキル/Lore固有名は英語固定（keep_en）。別名・略称（BKB等）も同様
