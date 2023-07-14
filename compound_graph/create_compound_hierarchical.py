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


        # list2[i+1]以降のノードの位置調整
        offset = lowest_node_y - highest_node_y + 800

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


    # list2の各インデックスに格納されているリスト内のディレクトリをx座標順にソートする

    for lst in list2:
        lst.sort(key=lambda dir_id: directories[next(i for i, d in enumerate(directories) if d["id"] == dir_id)]["x"])
    for list_x in list2:
        for i in range(len(list_x) - 1):
            max_x = float('-inf')
            min_x = float('inf')

            for obj in allgraph_objects['eleObjs']:
                if obj['group'] == 'nodes' and obj['data'].get("parent"):
                    parent_dir = obj['data']['parent'].split('/')[1]
                    if parent_dir == list_x[i]:
                        x = obj['position']['x']
                        if x > max_x:
                            max_x = x
                    if parent_dir == list_x[i+1]:
                        x = obj['position']['x']
                        if x < min_x:
                            min_x = x

            difference = max_x + 1000 - min_x

            for obj in allgraph_objects['eleObjs']:
                if obj['group'] == 'nodes' and obj['data'].get("parent"):
                    parent_dir = obj['data']['parent'].split('/')[1]
                    if parent_dir == list_x[i+1] and obj['position']['x'] < max_x + 1000:
                        obj['position']['x'] += difference

    return directories




allGraph_json = open('graph_attrs/graph_class_gptall.json', 'r')
allgraph_objects = json.load(allGraph_json)
#directories = [{'id': 'I9', 'x': 41908.0, 'y': 20880.0}, {'id': 'II1', 'x': 26236.8, 'y': 8143.2}, {'id': 'II2', 'x': 22587.0, 'y': 15984.0}, {'id': 'II4', 'x': 21176.0625, 'y': 19305.0}, {'id': 'II13', 'x': 35681.0, 'y': 16884.0}, {'id': 'II12', 'x': 25480.0, 'y': 19404.0}, {'id': 'III10', 'x': 29191.5, 'y': 17496.0}, {'id': 'II24', 'x': 24544.714285714286, 'y': 23929.714285714286}, {'id': 'III6', 'x': 30543.0, 'y': 21168.0}, {'id': 'XII6', 'x': 25188.000000000004, 'y': 9180.0}, {'id': 'I17', 'x': 30744.0, 'y': 23436.0}, {'id': 'III1', 'x': 34110.0, 'y': 24818.4}, {'id': 'XIX1', 'x': 24520.0, 'y': 12348.0}, {'id': 'II6', 'x': 31879.714285714286, 'y': 18869.14285714286}, {'id': 'XX1', 'x': 24874.2, 'y': 12981.6}, {'id': 'II9', 'x': 22278.0, 'y': 14988.0}, {'id': 'II10', 'x': 22884.0, 'y': 14580.0}, {'id': 'I3', 'x': 30945.36, 'y': 21517.92}, {'id': 'XV1', 'x': 22557.0, 'y': 16308.0}, {'id': 'X1', 'x': 10170.0, 'y': 21708.0}, {'id': 'III4', 'x': 26371.2, 'y': 23868.0}, {'id': 'I1', 'x': 29832.0, 'y': 22572.0}, {'id': 'I13', 'x': 23442.0, 'y': 16524.0}, {'id': 'XIX3', 'x': 25446.0, 'y': 16848.0}, {'id': 'II15', 'x': 39280.61538461538, 'y': 24266.76923076923}, {'id': 'II19', 'x': 13536.75, 'y': 23598.0}, {'id': 'XIX2', 'x': 32157.0, 'y': 21006.0}, {'id': 'III2', 'x': 31048.105263157893, 'y': 26596.42105263158}, {'id': 'X25', 'x': 9885.6, 'y': 21880.8}, {'id': 'XI1', 'x': 11340.000000000002, 'y': 23004.000000000004}, {'id': 'X2', 'x': 6144.0, 'y': 22140.0}, {'id': 'X6', 'x': 9475.565217391304, 'y': 24750.782608695652}, {'id': 'III5', 'x': 9732.0, 'y': 24516.0}, {'id': 'X18', 'x': 10374.0, 'y': 22572.0}, {'id': 'XI2', 'x': 19220.0, 'y': 24156.0}, {'id': 'XVII1', 'x': 14050.285714285714, 'y': 22942.285714285714}, {'id': 'X13', 'x': 3188.7272727272725, 'y': 23985.81818181818}, {'id': 'II3', 'x': 28008.0, 'y': 19116.0}, {'id': 'XXII16', 'x': 29898.0, 'y': 23436.0}, {'id': 'XXI9', 'x': 19434.0, 'y': 23868.0}, {'id': 'X4', 'x': 1650.0, 'y': 23436.0}, {'id': 'VII13', 'x': 7326.6, 'y': 24904.8}, {'id': 'X19', 'x': 4614.0, 'y': 23004.000000000004}, {'id': 'IV1', 'x': 13674.0, 'y': 23220.0}, {'id': 'IV6', 'x': 11880.0, 'y': 24300.0}, {'id': 'X23', 'x': 7716.0, 'y': 27756.0}, {'id': 'II8', 'x': 17130.0, 'y': 24084.0}, {'id': 'IV2', 'x': 23109.0, 'y': 24084.0}, {'id': 'IV3', 'x': 17574.0, 'y': 25164.0}, {'id': 'X11', 'x': 7454.333333333333, 'y': 26748.0}, {'id': 'II14', 'x': 26671.090909090908, 'y': 25870.909090909092}, {'id': 'XX6', 'x': 37290.0, 'y': 24300.0}, {'id': 'VII9', 'x': 30168.0, 'y': 7884.0}, {'id': 'II16', 'x': 36794.51612903226, 'y': 25972.25806451613}, {'id': 'III8', 'x': 28970.444444444445, 'y': 25180.0}, {'id': 'V1', 'x': 36438.88888888889, 'y': 25932.0}, {'id': 'II7', 'x': 33032.0, 'y': 24012.0}, {'id': 'VII6', 'x': 44324.16, 'y': 25716.96}, {'id': 'III27', 'x': 43374.00000000001, 'y': 25596.000000000004}, {'id': 'II17', 'x': 39613.5, 'y': 25380.0}, {'id': 'VII5', 'x': 49772.25, 'y': 25380.0}, {'id': 'III12', 'x': 31778.0, 'y': 26388.0}, {'id': 'III18', 'x': 29376.0, 'y': 26460.0}, {'id': 'IX9', 'x': 41022.0, 'y': 25164.0}, {'id': 'XII3', 'x': 18024.0, 'y': 25596.000000000004}, {'id': 'XX2', 'x': 31920.0, 'y': 24300.0}]
directories = [{'id': 'I9', 'x': 45916.8, 'y': 21708.0}, {'id': 'I3', 'x': 47477.714285714304, 'y': 33145.71428571428}, {'id': 'XIX1', 'x': 54282.36923076924, 'y': 38290.153846153844}, {'id': 'II7', 'x': 86734.80000000002, 'y': 23652.000000000004}, {'id': 'II4', 'x': 57256.512, 'y': 33976.8}, {'id': 'II1', 'x': 74672.16, 'y': 17215.2}, {'id': 'I1', 'x': 45532.15714285713, 'y': 29514.85714285714}, {'id': 'I17', 'x': 41463.79932203394, 'y': 34367.79661016949}, {'id': 'III1', 'x': 48273.31578947371, 'y': 29268.0}, {'id': 'III11', 'x': 50802.514285714286, 'y': 32076.0}, {'id': 'III8', 'x': 47182.83076923079, 'y': 35199.692307692305}, {'id': 'III5', 'x': 62596.12307692311, 'y': 38024.307692307695}, {'id': 'III4', 'x': 42585.39839999999, 'y': 36240.48}, {'id': 'I8', 'x': 54504.6, 'y': 16740.0}, {'id': 'I2', 'x': 53470.56000000001, 'y': 37260.0}, {'id': 'XX7', 'x': 63371.93333333335, 'y': 39516.0}, {'id': 'XX5', 'x': 38586.6, 'y': 23004.0}, {'id': 'IX1', 'x': 45450.479999999996, 'y': 35359.2}, {'id': 'II2', 'x': 35055.600000000006, 'y': 28836.0}, {'id': 'III10', 'x': 45787.91999999999, 'y': 37346.4}, {'id': 'II16', 'x': 53612.77904761901, 'y': 39265.71428571428}, {'id': 'IX6', 'x': 49224.428571428565, 'y': 41919.42857142857}, {'id': 'IX12', 'x': 60184.4, 'y': 33156.0}, {'id': 'IV1', 'x': 66292.16842105264, 'y': 42966.94736842105}, {'id': 'IV2', 'x': 62705.55, 'y': 39798.0}, {'id': 'X6', 'x': 98063.475, 'y': 40500.0}, {'id': 'IV6', 'x': 69927.24, 'y': 41709.6}, {'id': 'II10', 'x': 80215.88571428573, 'y': 28866.85714285714}, {'id': 'XIX8', 'x': 47651.59999999999, 'y': 36396.0}, {'id': 'III13', 'x': 47602.661684210514, 'y': 35645.68421052631}, {'id': 'XI6', 'x': 54015.600000000006, 'y': 18252.0}, {'id': 'X1', 'x': 94036.8, 'y': 38304.0}, {'id': 'III14', 'x': 36596.61333333332, 'y': 37308.0}, {'id': 'X14', 'x': 100803.96923076923, 'y': 43474.153846153844}, {'id': 'XI2', 'x': 99267.0, 'y': 42876.0}, {'id': 'X18', 'x': 103746.0, 'y': 32076.0}, {'id': 'XI1', 'x': 98388.0, 'y': 41493.6}, {'id': 'XVII1', 'x': 80961.15, 'y': 38772.0}, {'id': 'XIX2', 'x': 27925.49999999998, 'y': 45838.28571428572}, {'id': 'XXI9', 'x': 64470.0, 'y': 45252.0}, {'id': 'IV5', 'x': 64341.200000000004, 'y': 40284.0}, {'id': 'X10', 'x': 110328.0, 'y': 43999.2}, {'id': 'X2', 'x': 101106.0, 'y': 23868.0}, {'id': 'XVI4', 'x': 79554.0, 'y': 24732.0}, {'id': 'XII1', 'x': 88539.24705882353, 'y': 44985.17647058824}, {'id': 'XIV8', 'x': 106503.0, 'y': 43740.0}, {'id': 'XV5', 'x': 89448.0, 'y': 39852.0}, {'id': 'VII6', 'x': 62433.66352941178, 'y': 41529.17647058824}, {'id': 'XIV1', 'x': 103717.28, 'y': 44402.4}, {'id': 'X3', 'x': 117456.0, 'y': 51084.0}, {'id': 'IV11', 'x': 56474.700000000004, 'y': 44172.0}, {'id': 'IV7', 'x': 76566.9, 'y': 44280.0}, {'id': 'XIV4', 'x': 105264.0, 'y': 44604.0}, {'id': 'I4', 'x': 60036.0, 'y': 41364.0}, {'id': 'IV3', 'x': 55053.6, 'y': 47196.0}, {'id': 'X13', 'x': 102541.2, 'y': 45468.0}, {'id': 'XX1', 'x': 61323.36, 'y': 45986.4}, {'id': 'X12', 'x': 99224.4, 'y': 40543.2}, {'id': 'X11', 'x': 103152.0, 'y': 42660.0}, {'id': 'II13', 'x': 67158.0, 'y': 41580.0}, {'id': 'III6', 'x': 42061.79999999999, 'y': 40446.0}, {'id': 'II19', 'x': 93135.0, 'y': 42876.0}, {'id': 'XVII4', 'x': 75221.51999999999, 'y': 43048.8}, {'id': 'XVII2', 'x': 98103.0, 'y': 46332.0}, {'id': 'XIX6', 'x': 43684.8, 'y': 40176.0}, {'id': 'XIX3', 'x': 57061.740000000005, 'y': 47520.0}, {'id': 'XX6', 'x': 78248.0, 'y': 43596.00000000001}, {'id': 'I5', 'x': 26318.4, 'y': 42984.0}, {'id': 'I6', 'x': 16209.599999999999, 'y': 42012.0}, {'id': 'I18', 'x': 73738.8, 'y': 40284.0}, {'id': 'VII9', 'x': 57474.46153846153, 'y': 40981.846153846156}, {'id': 'III7', 'x': 35758.83199999999, 'y': 43092.0}, {'id': 'III27', 'x': 37611.600000000006, 'y': 25596.000000000004}, {'id': 'XXII21', 'x': 18921.600000000002, 'y': 26460.0}, {'id': 'VII5', 'x': 85783.47692307693, 'y': 44770.153846153844}, {'id': 'II17', 'x': 58366.89230769231, 'y': 39453.230769230766}, {'id': 'VII2', 'x': 62477.759999999995, 'y': 41191.2}, {'id': 'V1', 'x': 31749.600000000002, 'y': 25164.0}, {'id': 'IX14', 'x': 68433.2, 'y': 39276.0}, {'id': 'III2', 'x': 50485.482352941166, 'y': 43612.94117647059}, {'id': 'III12', 'x': 35808.799999999996, 'y': 39045.6}, {'id': 'III18', 'x': 22643.524, 'y': 42876.0}, {'id': 'VI7', 'x': 110142.0, 'y': 52812.0}, {'id': 'IX22', 'x': 41808.6, 'y': 28620.0}, {'id': 'IX8', 'x': 39690.600000000006, 'y': 40716.0}, {'id': 'III3', 'x': 69977.2, 'y': 43212.0}, {'id': 'III15', 'x': 63022.8, 'y': 40284.0}, {'id': 'XXI7', 'x': 59475.600000000006, 'y': 33372.0}, {'id': 'VII3', 'x': 63195.840000000004, 'y': 44949.6}, {'id': 'VII7', 'x': 64396.799999999996, 'y': 42972.0}, {'id': 'XII2', 'x': 79701.0, 'y': 45900.0}, {'id': 'XII9', 'x': 88262.4, 'y': 47676.0}, {'id': 'XII6', 'x': 89323.14545454545, 'y': 45684.0}, {'id': 'VII18', 'x': 66108.53333333333, 'y': 42684.0}, {'id': 'II18', 'x': 65448.0, 'y': 38124.0}, {'id': 'VII1', 'x': 60503.55, 'y': 41850.0}, {'id': 'VII19', 'x': 62007.0, 'y': 40716.0}, {'id': 'VII17', 'x': 77982.0, 'y': 41796.0}, {'id': 'III33', 'x': 61062.0, 'y': 39852.0}, {'id': 'XXI6', 'x': 54654.4, 'y': 45900.0}, {'id': 'III16', 'x': 42603.600000000006, 'y': 49500.0}, {'id': 'XVII11', 'x': 85047.0, 'y': 45252.0}, {'id': 'XIX4', 'x': 37509.6, 'y': 42660.0}, {'id': 'I13', 'x': 74382.0, 'y': 35100.0}, {'id': 'IX26', 'x': 70879.8, 'y': 45036.0}, {'id': 'VII11', 'x': 66663.0, 'y': 46764.0}, {'id': 'VII14', 'x': 82488.0, 'y': 43308.00000000001}, {'id': 'VIII1', 'x': 101040.0, 'y': 43740.0}, {'id': 'XX4', 'x': 73746.0, 'y': 41580.0}, {'id': 'II24', 'x': 85884.00000000001, 'y': 40716.0}, {'id': 'X27', 'x': 113676.0, 'y': 44172.0}, {'id': 'XIV13', 'x': 76896.0, 'y': 45036.0}, {'id': 'XIX7', 'x': 2163.36, 'y': 42876.00000000001}, {'id': 'IV4', 'x': 98258.0, 'y': 50076.0}, {'id': 'XII5', 'x': 91194.0, 'y': 48492.00000000001}, {'id': 'IV16', 'x': 45888.600000000006, 'y': 47196.0}, {'id': 'VIII11', 'x': 106461.0, 'y': 51084.0}, {'id': 'XIII7', 'x': 116124.0, 'y': 50652.0}, {'id': 'XV1', 'x': 20865.600000000002, 'y': 54108.00000000001}, {'id': 'XII3', 'x': 89298.0, 'y': 51732.0}, {'id': 'XX3', 'x': 101442.0, 'y': 47196.0}, {'id': 'XIII2', 'x': 111222.0, 'y': 51948.0}, {'id': 'XV7', 'x': 74718.0, 'y': 43308.00000000001}, {'id': 'VII13', 'x': 50013.600000000006, 'y': 52164.0}, {'id': 'IV9', 'x': 35704.4, 'y': 50652.0}, {'id': 'XII10', 'x': 24837.600000000006, 'y': 51084.0}, {'id': 'XVII3', 'x': 95268.0, 'y': 46332.0}, {'id': 'II22', 'x': 32307.600000000002, 'y': 47628.0}, {'id': 'XV4', 'x': 64164.0, 'y': 48492.00000000001}, {'id': 'IV8', 'x': 34059.600000000006, 'y': 51948.0}, {'id': 'XVII5', 'x': 96000.0, 'y': 46764.0}, {'id': 'XII12', 'x': 98244.0, 'y': 51948.0}, {'id': 'XVII9', 'x': 96000.0, 'y': 47196.0}, {'id': 'IV10', 'x': 27150.600000000006, 'y': 47844.0}, {'id': 'VII4', 'x': 94429.5, 'y': 54648.0}, {'id': 'XIII17', 'x': 106926.0, 'y': 50220.0}]

for n in range(len(directories)):
    part_json = open('graph_attrs/compound_dot_graph' + str(directories[n]['id']) + ".json", 'r')
    part_objects = json.load(part_json)

    positionXsum = 0
    positionYsum = 0
    count = 0
    for i in range(len(part_objects['eleObjs'])):
        if part_objects['eleObjs'][i]["group"] == "nodes" and part_objects['eleObjs'][i]["data"]["id"] != "TARSKI_0" and part_objects['eleObjs'][i]["data"]["id"] != "TARSKI_A":
            positionXsum += part_objects['eleObjs'][i]['position']['x']
            positionYsum += part_objects['eleObjs'][i]['position']['y']
            count += 1

    positionX = directories[n]['x'] - (positionXsum / count)
    positionY = directories[n]['y'] - (positionYsum / count)
    for j in range(len(allgraph_objects['eleObjs'])):
        if allgraph_objects['eleObjs'][j]["group"] == "nodes":
            for k in range(len(part_objects['eleObjs'])):
                if part_objects['eleObjs'][k]["group"] == "nodes" and part_objects['eleObjs'][k]["data"]["id"] != "TARSKI_0" and part_objects['eleObjs'][k]["data"]["id"] != "TARSKI_A":
                    if part_objects['eleObjs'][k]["data"]["id"] == allgraph_objects['eleObjs'][j]["data"]["id"]:
                        allgraph_objects['eleObjs'][j]['position']['x'] = part_objects['eleObjs'][k]['position']['x'] + positionX
                        allgraph_objects['eleObjs'][j]['position']['y'] = part_objects['eleObjs'][k]['position']['y'] + positionY
                        break


# ノードの重なりを解消する
adjust_directory_positions(allgraph_objects, directories)

with open('graph_attrs/graph_classHierar_all.json', 'w') as f:
    json.dump(allgraph_objects, f, indent=4)