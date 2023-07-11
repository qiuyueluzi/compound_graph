import json
import glob
import create_graph
# ノードを分類毎に分けたtxtファイルを生成

# mml_classification.jsonを読み込む
with open('graph_attrs/mml_classification_gpt.json', 'r') as file:
    classification_data = json.load(file)

# 分類ごとにテキストファイルを作成
for classification in classification_data['mml_classification']:
    ancestorDirectory = classification['directory']
    directory = ancestorDirectory.split("/", 2)[1]
    directory = directory.replace("/", "")
    if directory != "" :
        nodes = classification['mml-name']

        # 同じ分類のノード名を記録したテキストファイルを作成
        with open(f'mml/{directory}.txt', mode='a') as txt_file:
            txt_file.write(nodes + "\n")

files = glob.glob("mml/*.txt")
for fileName in files:
    directoryName = fileName.split(".")[0].split("/")[1]
    create_graph.create_part_graph(directoryName)