# gtfs_merge.py
複数のGTFS-JP（標準的なバス情報フォーマット 第2版）形式のデータを、1つのGTFS-JPデータに統合するツール

## 概要
このツールでは、複数のGTFS-JPデータに対して、キーとなる項目にアルファベットからなる接頭辞を付与することにより、整合性を確保した上で1つのGTFS-JPデータに統合します。
統合するデータが26個以下の場合は1文字（A, B, C, ...）、27個以上の場合は2文字（AA, AB, AC, ... ,AZ , BA, BB, ...）が接頭辞となります。
データセットと接頭辞の対応はツール実行後に作成されるmemo.txtにて確認できます。

|項目名|変更後の内容|
|:--|:--|
|agency_id|接頭辞|
|agency_number|本来のagency_id|
|route_id|接頭辞+本来のroute_id|
|trip_id|接頭辞+本来のtrip_id|
|service_id|接頭辞+本来のservice_id|
|office_id|接頭辞+本来のoffice_id|
|jp_office_id|接頭辞+本来のjp_office_id|
|shape_id|接頭辞+本来のshape_id|
|stop_id|接頭辞+本来のstop_id|
|from_stop_id|接頭辞+本来のfrom_stop_id|
|to_stop_id|接頭辞+本来のto_stop_id|
|fare_id|接頭辞+本来のfare_id|
|zone_id|接頭辞+本来のzone_id|
|origin_id|接頭辞+本来のorigin_id|
|destination_id|接頭辞+本来のdestination_id|
|contains_id|接頭辞+本来のcontains_id|

## 動作環境
* Python3 （標準ライブラリのみで動作するはず）

## 使い方
1. 統合したいGTFS-JPデータセットを、それぞれ**zipファイルから展開して**、同一ディレクトリに配置する
2.  ```python gtfs_merge.py [統合したいGTFS-JPを置いたディレクトリ]```
3. mergeディレクトリが作成され、その中に統合されたGTFS-JPファイル（展開状態）が格納される
4. gtfs_merge.pyと同一ディレクトリにmemo.txt（接頭辞対応表・前述）が配置される

## ライセンス
本ソフトウェアは、[MITライセンス](./LICENSE)の下に提供されています。

## Contact
* Twitter [@eng_oozora283](https://twitter.com/eng_oozora283) までご連絡ください