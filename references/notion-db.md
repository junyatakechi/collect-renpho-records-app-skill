# 記録先のDB

どの測定を、どのDBの、どの列に書くか。判断ではなく、この環境での記録の取り決め。
**列名の正は `scripts/sync_renpho_to_notion.py` の定数**（`TITLE_COLUMN`・`DATE_COLUMN`・`ID_COLUMN`・`VALUE_COLUMNS`）。この表は説明で、変えるときはスクリプトとNotion側を同時に直す。

## DB

- Notionの「体重記録」DB。URLは環境ファイルの `RENPHO_COLLECTION_DB_URL` にある。
- 体組成計の自動記録より前の、手入力の体重の履歴が続いている。**新しいDBを作らない。** 体重の時系列が分割され、このDBを読んでいる評価のスキルの参照先も直すことになるため。
- このスキルが書くのはこのDBだけ。評価やLogへの記録はしない。

## 列

| 列 | 型 | 中身 | RENPHOのキー |
|---|---|---|---|
| `Name` | title | 測定日の `YYYY-MM-DD`。期間で絞る・並べるのは `対象日時` であって、この列ではない | — |
| `対象日時` | date | 測定時刻（JST） | `timeStamp` |
| `RENPHO ID` | rich_text | 一意キー | `id` |
| `体重(kg)` | number | | `weight` |
| `BMI` | number | | `bmi` |
| `体脂肪率(%)` | number | | `bodyfat` |
| `体水分率(%)` | number | | `water` |
| `骨格筋量(kg)` | number | | `muscle` |
| `筋肉量(kg)` | number | | `sinew` |
| `骨量(kg)` | number | | `bone` |
| `基礎代謝(kcal)` | number | | `bmr` |
| `内臓脂肪レベル` | number | | `visfat` |
| `皮下脂肪率(%)` | number | | `subfat` |
| `タンパク質率(%)` | number | | `protein` |
| `体年齢` | number | | `bodyage` |
| `除脂肪体重(kg)` | number | | `fatFreeWeight` |
| `標準体重(kg)` | number | | `TW` |
| `体重コントロール(kg)` | number | | `WC` |
| `生体インピーダンス(Ω)` | number | | `resistance` |
| `体型分類` | number | | `bodytype` |

- どのキーが何で、単位は何か、どの値を空にするかは renpho-api-generic-logic の判断（項目の意味と単位・体組成が空のレコード）に従う。ここでは対応だけを持つ。
- `RENPHO ID` がテキストなのは、renpho-api-generic-logic のレコードIDの持ち方の判断による。
- Elis Aspire で常に空の項目（`heartRate`・`cardiacIndex`・`bodyShape`）と、重複の `FC` には列を作っていない。

## 記録の限界

| 記録の限界 | 扱い |
|---|---|
| 体組成は、体組成計の導入以降にしか無い | それより前の行は体重だけ。欠測ではない |
| 体組成が測れなかった測定は、体重とBMIだけ | 他の列は空のまま。0ではない |
| 取れるのは本人のアカウントの測定だけ | 家族メンバーの測定は記録しない |
