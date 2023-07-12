import json


def adjust_directory_positions(allgraph_objects, directories):
    # ディレクトリの上端と下端の座標を求める
    top_positions = {}  # ディレクトリの上端のy座標を保持する辞書
    bottom_positions = {}  # ディレクトリの下端のy座標を保持する辞書

    for directory in directories:
        dir_id = directory['id']
        top_positions[dir_id] = float('inf')  # 初期値として十分に大きな値を設定
        bottom_positions[dir_id] = float('-inf')  # 初期値として十分に小さな値を設定

    for obj in allgraph_objects['eleObjs']:
        if obj['group'] == 'nodes' and obj['data'].get('parent'):
            node_position_y = obj['position']['y']
            node_directory = obj['data']['parent'].split("/")[1]
            if node_directory != "":
                if node_position_y < top_positions[node_directory] :
                    top_positions[node_directory] = node_position_y
    
                if node_position_y > bottom_positions[node_directory] :
                    bottom_positions[node_directory] = node_position_y

    same_level_directories = []

    for directory in directories:
        dir_id = directory['id']
        for compare_directory in directories:
            compare_dir_id = compare_directory['id']
            if dir_id != compare_dir_id:
                if top_positions[dir_id] < top_positions[compare_dir_id] and bottom_positions[dir_id] > bottom_positions[compare_dir_id]:
                    same_level_directories.append([dir_id, compare_dir_id])


    print(same_level_directories)

    # pairsのコピーを作成
    pairs_copy = same_level_directories.copy()

    # ペアの後者が同じであるペアを抽出して削除
    for i in range(len(pairs_copy)):
        for j in range(i + 1, len(pairs_copy)):
            if j >= len(pairs_copy):
                break

            if pairs_copy[i][1] == pairs_copy[j][1]:
                pair1 = pairs_copy[i]
                pair2 = pairs_copy[j]

                id_1 = pair1[0]
                id_2 = pair1[1]
                obj_1 = next(obj for obj in directories if obj["id"] == id_1)
                obj_2 = next(obj for obj in directories if obj["id"] == id_2)
                diff1 = abs(obj_1["y"] - obj_2["y"])

                id_1 = pair2[0]
                id_2 = pair2[1]
                obj_1 = next(obj for obj in directories if obj["id"] == id_1)
                obj_2 = next(obj for obj in directories if obj["id"] == id_2)
                diff2 = abs(obj_1["y"] - obj_2["y"])

                if diff1 > diff2:
                    pairs_copy.remove(pair1)
                else:
                    pairs_copy.remove(pair2)

    print(pairs_copy)

    # (1)のリスト
    list1 = pairs_copy

    # ソート処理を追加
    list1.sort(key=lambda x: top_positions[x[0]])

    # (2)のリスト
    list2 = []

    # リストの結合と集合型を使って変換
    for l in list1:
        # 結合する前に集合型に変換して重複を削除
        s = set(l)
        # 結合先のリストが空ならそのまま追加
        if not list2:
            list2.append(s)
        else:
            # 結合先のリストに同じ要素があるかどうか調べる
            for i, t in enumerate(list2):
                # 同じ要素があれば結合して更新
                if s & t:
                    list2[i] = s | t
                    break
            # 同じ要素がなければそのまま追加
            else:
                list2.append(s)

    # 集合型からリスト型に戻す
    list2 = [list(t) for t in list2]

    # 結果を表示
    print("result:", list2)

    # ループで処理
    for i in range(len(list2) - 1):
        # list2[i]に属する最も下のノードの座標を格納する変数
        lowest_node_y = float('-inf')

        # list2[i+1]以降に属する最も上のノードの座標を格納する変数
        highest_node_y = float('inf')
        bottom_y = []
        top_y = []
        if(i>0):
            print(highest_node_y)

        for obj in allgraph_objects['eleObjs']:
            if obj['group'] == 'nodes' and obj['data'].get('parent'):
                node_id = obj['data']['id']
                node_parent = obj['data']['parent'].split("/")[1]
                node_y = obj['position']['y']

                # list2[i]に属するノードの処理
                if node_parent in list2[i]:
                    if node_y > lowest_node_y:
                        lowest_node_y = node_y
                        bottom_y = node_id

                # list2[i+1]以降に属するノードの処理
                for j in range(i + 1, len(list2)):
                    if node_parent in list2[j]:
                        if node_y < highest_node_y:
                            highest_node_y = node_y
                            top_y = node_id
                            if(i>0):
                                print(node_id,list2[j],node_parent)

        print("Lowest Node Y:", lowest_node_y, bottom_y)
        print("Highest Node Y:", highest_node_y, top_y)

        # list2[i+1]以降のノードの位置調整
        offset = lowest_node_y - highest_node_y + 1000

        for obj in allgraph_objects['eleObjs']:
            if obj['group'] == 'nodes' and obj['data'].get('parent'):
                node_parent = obj['data']['parent'].split("/")[1]

                for j in range(i + 1, len(list2)):
                    if node_parent in list2[j]:
                        obj['position']['y'] += offset
                        break

        # list2[i+1]以降のディレクトリの位置調整
        for directory in directories:
            dir_id = directory['id']
            if dir_id in list2[i]:
                continue

            for j in range(i + 1, len(list2)):
                if dir_id in list2[j]:
                    directory['y'] += offset
                    break

        print("Lowest Node Y:", lowest_node_y, bottom_y)
        print("Highest Node Y:", highest_node_y, top_y)

    # list2の各インデックスに格納されているリスト内のディレクトリをx座標順にソートする
    '''print(list2)
    for lst in list2:
        lst.sort(key=lambda dir_id: directories[next(i for i, d in enumerate(directories) if d["id"] == dir_id)]["x"])
    print(list2)
    for list_x in list2:
        for i in range(len(list_x) - 1):
            # list2[i]に属する最も下のノードの座標を格納する変数
            lowest_node_x = float('-inf')

            # list2[i+1]以降に属する最も上のノードの座標を格納する変数
            highest_node_x = float('inf')
            bottom_x = []
            top_x = []
            if(i>0):
                print(highest_node_x)

            for obj in allgraph_objects['eleObjs']:
                if obj['group'] == 'nodes' and obj['data'].get('parent'):
                    node_id = obj['data']['id']
                    node_parent = obj['data']['parent'].split("/")[1]
                    node_x = obj['position']['x']

                    # list2[i]に属するノードの処理
                    if node_parent in list_x[i]:
                        if node_x > lowest_node_x:
                            lowest_node_x = node_x
                            bottom_x = node_id

                    # list2[i+1]以降に属するノードの処理
                    for j in range(i + 1, len(list_x)):
                        if node_parent in list_x[j]:
                            if node_x < highest_node_x:
                                highest_node_x = node_x
                                top_x = node_id
                                if(i>0):
                                    print(node_id,list_x[j],node_parent)


            # list2[i+1]以降のノードの位置調整
            offset = lowest_node_x - highest_node_x + 1000

            for obj in allgraph_objects['eleObjs']:
                if obj['group'] == 'nodes' and obj['data'].get('parent'):
                    node_parent = obj['data']['parent'].split("/")[1]

                    for j in range(i + 1, len(list_x)):
                        if node_parent in list_x[j]:
                            obj['position']['x'] += offset
                            break

            # list2[i+1]以降のディレクトリの位置調整
            for directory in directories:
                dir_id = directory['id']
                if dir_id in list_x[i]:
                    continue

                for j in range(i + 1, len(list_x)):
                    if dir_id in list_x[j]:
                        directory['x'] += offset
                        break'''

    return directories




allGraph_json = open('graph_attrs/graph_class_gpt.json', 'r')
allgraph_objects = json.load(allGraph_json)
directories = [{'id': 'I9', 'x': 5237.649999999998, 'y': 20628.0}, {'id': 'II1', 'x': 18145.610526315795, 'y': 7315.578947368421}, {'id': 'II2', 'x': 17695.6875, 'y': 14418.0}, {'id': 'II4', 'x': 16931.593548387104, 'y': 18962.709677419356}, {'id': 'II13', 'x': 10567.55, 'y': 16740.0}, {'id': 'II12', 'x': 10499.550000000001, 'y': 16092.000000000002}, {'id': 'III10', 'x': 18284.4, 'y': 10908.0}, {'id': 'II24', 'x': 11930.550000000001, 'y': 16956.0}, {'id': 'III6', 'x': 17435.4, 'y': 8748.0}, {'id': 'XII6', 'x': 17435.4, 'y': 9180.0}, {'id': 'I17', 'x': 425.688, 'y': 17388.0}, {'id': 'III1', 'x': 18662.4, 'y': 18252.0}, {'id': 'XIX1', 'x': 18777.4, 'y': 12348.0}, {'id': 'II6', 'x': 11122.628571428571, 'y': 18684.0}, {'id': 'XX1', 'x': 14349.63, 'y': 12549.6}, {'id': 'II9', 'x': 17234.63076923078, 'y': 14663.076923076924}, {'id': 'II10', 'x': 16052.400000000001, 'y': 14580.0}, {'id': 'I3', 'x': 9786.712499999998, 'y': 21258.0}, {'id': 'XV1', 'x': 16391.4, 'y': 16308.0}, {'id': 'X1', 'x': 27737.399999999998, 'y': 17820.0}, {'id': 'III4', 'x': 15714.6, 'y': 22658.4}, {'id': 'I1', 'x': 803.6999999999999, 'y': 18684.0}, {'id': 'I13', 'x': 16421.4, 'y': 16524.0}, {'id': 'XIX3', 'x': 13598.4, 'y': 16848.0}, {'id': 'II15', 'x': 9332.699999999999, 'y': 23632.363636363636}, {'id': 'II19', 'x': 20257.399999999998, 'y': 23220.0}, {'id': 'XIX2', 'x': 7122.299999999999, 'y': 21384.0}, {'id': 'III2', 'x': 15161.400000000001, 'y': 19548.0}, {'id': 'X25', 'x': 21303.0, 'y': 21880.8}, {'id': 'XI1', 'x': 10031.400000000001, 'y': 23004.000000000004}, {'id': 'X2', 'x': 23295.399999999998, 'y': 22140.0}, {'id': 'X6', 'x': 21036.704347826097, 'y': 24750.782608695652}, {'id': 'III5', 'x': 23909.4, 'y': 24300.0}, {'id': 'X18', 'x': 20993.4, 'y': 22572.0}, {'id': 'XI2', 'x': 10382.4, 'y': 23652.0}, {'id': 'XVII1', 'x': 21580.542857142857, 'y': 22942.285714285714}, {'id': 'X13', 'x': 24883.581818181814, 'y': 23632.363636363636}, {'id': 'II3', 'x': 9377.400000000001, 'y': 19116.0}, {'id': 'XXII16', 'x': 7391.400000000001, 'y': 23436.0}, {'id': 'XXI9', 'x': 12593.4, 'y': 23868.0}, {'id': 'X4', 'x': 27725.399999999998, 'y': 23436.0}, {'id': 'VII13', 'x': 20286.6, 'y': 24904.8}, {'id': 'X19', 'x': 13559.4, 'y': 23004.000000000004}, {'id': 'IV1', 'x': 12245.400000000001, 'y': 23220.0}, {'id': 'IV6', 'x': 15779.400000000001, 'y': 24300.0}, {'id': 'X23', 'x': 16313.4, 'y': 27756.0}, {'id': 'II8', 'x': 13508.400000000001, 'y': 24084.0}, {'id': 'IV2', 'x': 10073.400000000001, 'y': 24300.0}, {'id': 'IV3', 'x': 15815.400000000001, 'y': 25164.0}, {'id': 'X11', 'x': 18662.066666666666, 'y': 26748.0}, {'id': 'II14', 'x': 6593.400000000001, 'y': 24732.0}, {'id': 'XX6', 'x': 12683.400000000001, 'y': 24300.0}, {'id': 'VII9', 'x': 18173.4, 'y': 7452.0}, {'id': 'II16', 'x': 3935.7000000000003, 'y': 25164.0}]

for n in range(len(directories)):
    part_json = open('graph_attrs/compound_dot_graph' + str(directories[n]['id']) + ".json", 'r')
    part_objects = json.load(part_json)

    positionXsum = 0
    positionYsum = 0
    for i in range(len(part_objects['eleObjs'])):
        if part_objects['eleObjs'][i]["group"] == "nodes":
            positionXsum += part_objects['eleObjs'][i]['position']['x']
            positionYsum += part_objects['eleObjs'][i]['position']['y']

    positionX = directories[n]['x'] - (positionXsum / len(part_objects['eleObjs']))
    positionY = directories[n]['y'] - (positionYsum / len(part_objects['eleObjs']))
    for j in range(len(part_objects['eleObjs'])):
        if part_objects['eleObjs'][j]["group"] == "nodes":
            for k in range(len(allgraph_objects['eleObjs'])):
                if allgraph_objects['eleObjs'][k]["group"] == "nodes":
                    if allgraph_objects['eleObjs'][k]['data']['id'] == part_objects['eleObjs'][j]['data']['id']:
                        allgraph_objects['eleObjs'][k]['position']['x'] = part_objects['eleObjs'][j]['position']['x'] + positionX
                        allgraph_objects['eleObjs'][k]['position']['y'] = part_objects['eleObjs'][j]['position']['y'] + positionY
                        break


# ノードの重なりを解消する
adjust_directory_positions(allgraph_objects, directories)

with open('graph_attrs/graph_classHierar_test.json', 'w') as f:
    json.dump(allgraph_objects, f, indent=4)