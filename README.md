# compound_graph

[compound emgraph](https://qiuyueluzi.github.io/compound_graph)

compound_dot_graph.json作成時の留意点
 - create_graph.pyを実行する
 - pythonライブラリnetworkxをインストールする
 - mizarをインストールし、MIZAR/mml下に存在する.mizファイル全てをコピーし、  
create_graph.pyが存在するフォルダ内に2層のmml/2020-6-18(例、日付は適宜コピーした日に)フォルダを作成、日付フォルダにペーストする
 - 作成したmmlフォルダ内にmml-lar-top199.txt(数字は例)ファイルを作成し、  
グラフに描画したい(クラスタリングが完了した)article名を1行ずつ書き込む  
ファイル名の数字はここで書き込んだarticle数を記入する
 - retrieve_dependency.pyの文頭にある2つの変数を、  
 作成した.txtファイルのarticle数と.mizファイルを格納したフォルダ名に書き換える

mml-lar-topファイル内の様式(一部)
```
tarski
xboole_0
boole
xboole_1
enumset1
```