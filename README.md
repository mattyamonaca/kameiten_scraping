# 使い方

##初回起動時

1. tmpフォルダを空にする
2. conf.yamlを開く
3. conf.yamlの"prefecture"に都道府県コードを入れる。（都道府県コード : https://nlftp.mlit.go.jp/ksj/gml/codelist/PrefCd.html）
4. conf.yamlの"encode"を自分の環境に合わせる。（デフォルトはcp932。Pandasのto_csv関数のencoding引数に相当）
5. conf.yamlの上記2項目を覗く全ての項目に何も入力されていないことを確認
6. getStoreInfo.pyを起動（Python3.7.6以降推奨）
7. getStioreInfo.pyの実行が完了したのを確認したのち、make_data.pyを起動（Python3.7.6以降推奨）
8. outputフォルダにoutput_{conf.yamlでprefectureに入力した都道府県コード}.csvが出力されている事を確認する。

##中断再開時(使用非推奨)
1. log/log.yamlを開く。中断時のgc,ac,startが記入されているので、その値を記録する。
2. conf.yamlを開く
3. conf.yamlの"ac","gc","start"にlog.yamlに記入されていたものと同じ値を入力する。
4. getStoreInfo.pyを起動（Python3.7.6以降推奨）
5. conf.yamlで指定した"ac","gc","start"まで処理がスキップされている事を標準出力の文面にて確認。
6. getStioreInfo.pyの実行が完了したのを確認したのち、make_data.pyを起動（Python3.7.6以降推奨）
7. outputフォルダにoutput_{conf.yamlでprefectureに入力した都道府県コード}.csvが出力されている事を確認する。


