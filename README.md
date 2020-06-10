# このファイルについて
現職（非IT）でデータ整理などにPythonを利用したエビデンスとして記録しておきたいと思います。
だいたい2019年8月位に素人なりに作ってみました。

# 概要
現職でダムの水質シミュレーションを行っていました。
計算結果がdatファイルというテキストファイルで出力されるのですが、これを後のデータ分析で利用できるようエクセルファイルにデータ整型して出力します。

●対象datファイル数<br>
出力地点（10地点くらい）　×　水温や水質などの出力項目（20項目くらい）

●各datファイルの中身<br>
1万行（時間データ）　×　110列くらい

| t | 表層ブロック番号 |　aaa|
| -------- | ---------- | ---- |
| 内容セル  | 内容セル  |
| 内容セル  | 内容セル  |

※守秘義務のため実際のデータは無し。