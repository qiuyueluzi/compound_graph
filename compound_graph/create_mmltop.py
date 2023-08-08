import json
import glob
import create_graph

# ノードを分類毎に分けたtxtファイルを生成

# mml_classification.jsonを読み込む
with open('graph_attrs/mml-classification_named.json', 'r') as file:
    classification_data = json.load(file)

# 分類ごとにテキストファイルを作成
for classification in classification_data['mml_classification']:
    if classification.get("directory"):
        ancestorDirectory = classification['directory']
        if ancestorDirectory != "":
            directory = ancestorDirectory.split("/")[1]
            directory = directory.replace("/", "")
            
            if directory != "" :
                nodes = classification['mml-name']
    
                # 同じ分類のノード名を記録したテキストファイルを作成
                with open(f'mml/{directory}.txt', mode='a') as txt_file:
                    print(directory)
                    txt_file.write(nodes + "\n")

files = glob.glob("mml/*.txt")
for fileName in files:
    directoryName = fileName.split(".")[0].split("/")[1]
    print("create:"+directoryName)
    create_graph.create_part_graph(directoryName)
