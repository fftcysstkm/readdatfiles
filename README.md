# このファイルについて
素人なりにではありますが、現職（非IT系）でデータ整理などにPythonを利用したエビデンスとして記録しておきたいと思います。

# 概要
現職でダムの水質シミュレーションを行っていた。
水質計算結果はdatファイルというテキストファイルで出力され、この計算結果は地点ごと・水質項目ごとにバラバラに出力されてるなど、扱いづらい状況だった。

●対象datファイル数<br>
出力地点（10地点くらい）　×　水温や水質などの出力項目（20項目くらい）

●各datファイルの中身の例<br>
1万行（時間データ）　×　110列くらい
例）ある地点の水質Aの出力
| time |表層の水深ブロック番号|水質A1|~|水質A55|水深1|~|水深55|
| -------- | ----- | ---- | ---- |---- |---- |---- |---- |
| 1  |  37 |xxx|xxx|xxx|xxx|xxx|xxx|
| 2  |   | |
| ・・・  | | |

これを後のデータ分析で利用しやすいように、地点ごとの水質計算結果を集約するようにした。
↓
| time |表層の水深ブロック番号|水質A1|~|水質A55|水質B1|~|水質B55|・・・他の水質項目・・・|水深1|~|水深55|
| -------- | ----- | ---- | ---- |---- |---- |---- |---- |---- |---- |---- |---- |
| 1  |  37 |xxx|xxx|xxx|xxx|xxx|xxx|
| 2  |   | |
| ・・・  | | |
