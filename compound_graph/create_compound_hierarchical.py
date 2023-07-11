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
            node_directory = obj['data']['parent'].split("/", 2)[1]
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
                node_parent = obj['data']['parent'].split("/", 2)[1]
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
                node_parent = obj['data']['parent'].split("/", 2)[1]

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


    return directories




allGraph_json = open('graph_attrs/graph_class.json', 'r')
allgraph_objects = json.load(allGraph_json)
directories = [{"id":"set", "x":13731.638682352936, "y":14704.517647058823},
{"id":"computer", "x":12350.653846153844, "y":15427.384615384615},
{"id":"number", "x":17255.066666666677, "y":15600.0},
{"id":"analysis", "x":20211.72911392403, "y":24376.556962025315},
{"id":"algebra", "x":12905.803125000008, "y":23949.0},
{"id":"sequence", "x":16584.38108108109, "y":21579.567567567567},
{"id":"graph", "x":7122.299999999999, "y":21384.0},
{"id":"combinatorics", "x":14603.400000000001, "y":23148.0},
{"id":"logic", "x":8920.987499999997, "y":21798.0},
{"id":"probability", "x":21580.542857142857, "y":22942.285714285714},
{"id":"economics", "x":11105.4, "y":19116.0},
{"id":"numerical", "x":25395.899999999998, "y":26460.0},
{"id":"geometry", "x":9567.500000000002, "y":19116.0},
{"id":"cryptography", "x":12683.400000000001, "y":24300.0},
{"id":"category", "x":5579.7, "y":25596.000000000004},]

for n in range(len(directories)):
    part_json = open('graph_attrs/compound_dot_graph' + str.capitalize(directories[n]['id']) + ".json", 'r')
    part_objects = json.load(part_json)

    positionXsum = 0
    positionYsum = 0
    for i in range(len(part_objects['eleObjs'])):
        positionXsum += part_objects['eleObjs'][i]['position']['x']
        positionYsum += part_objects['eleObjs'][i]['position']['y']

    positionX = directories[n]['x'] - (positionXsum / len(part_objects['eleObjs']))
    positionY = directories[n]['y'] - (positionYsum / len(part_objects['eleObjs']))
    for j in range(len(part_objects['eleObjs'])):
        for k in range(len(allgraph_objects['eleObjs'])):
            if allgraph_objects['eleObjs'][k]['data']['id'] == part_objects['eleObjs'][j]['data']['id']:
                allgraph_objects['eleObjs'][k]['position']['x'] = part_objects['eleObjs'][j]['position']['x'] + positionX
                allgraph_objects['eleObjs'][k]['position']['y'] = part_objects['eleObjs'][j]['position']['y'] + positionY
                break

# ノードの重なりを解消する
adjust_directory_positions(allgraph_objects, directories)


with open('graph_attrs/graph_classHierar_test.json', 'w') as f:
    json.dump(allgraph_objects, f, indent=4)