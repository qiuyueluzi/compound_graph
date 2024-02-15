import json

# allgraph_objectsのオブジェクトの凡例
#{
#    "group": "nodes",
#    "data": {
#        "id": "Article名",
#        "name": "Article名",
#        "href": "URL",
#        "parent": "Directory名"
#    },
#    "position": {
#        "x": x座標,
#        "y": y座標
#    }
#},

def adjust_directory_positions(allgraph_objects, directories):
    # 重複したディレクトリを探すためディレクトリの上下端を取得
    top_positions = {}  # ディレクトリの上端のy座標を保持する辞書
    bottom_positions = {}  # ディレクトリの下端のy座標を保持する辞書
    left_positions = {}  # ディレクトリの左端のx座標を保持する辞書
    right_positions = {}  # ディレクトリの右端のx座標を保持する辞書

    for directory in directories:
        dir_id = directory['id']
        top_positions[dir_id] = float('inf')  # 初期値として十分に大きな値を設定
        bottom_positions[dir_id] = float('-inf')  # 初期値として十分に小さな値を設定
        left_positions[dir_id] = float('inf')  # 初期値として十分に大きな値を設定
        right_positions[dir_id] = float('-inf')  # 初期値として十分に小さな値を設定

    for obj in allgraph_objects['eleObjs']:
        if obj['group'] == 'nodes' and obj['data'].get('parent'):
            node_position_x = obj['position']['x']
            node_position_y = obj['position']['y']
            node_directory = obj['data']['parent'].split("/")[1]
            if node_directory != "":
                if node_position_y < top_positions[node_directory] :
                    top_positions[node_directory] = node_position_y
    
                if node_position_y > bottom_positions[node_directory] :
                    bottom_positions[node_directory] = node_position_y

                if node_position_x < left_positions[node_directory] :
                    left_positions[node_directory] = node_position_x
    
                if node_position_x > right_positions[node_directory] :
                    right_positions[node_directory] = node_position_x

    # 重なっているディレクトリのペアを格納する配列を作る
    overlapping_pairs = []  # 重なっているディレクトリのペアを格納する配列

    for dir1 in directories:
        for dir2 in directories:
            if dir1 != dir2:  # 同じディレクトリでないことを確認
                dir1_id = dir1['id']
                dir2_id = dir2['id']
                # ディレクトリの上下端と左右端の座標を取得
                dir1_top = top_positions[dir1_id]
                dir1_bottom = bottom_positions[dir1_id]
                dir1_left = left_positions[dir1_id]
                dir1_right = right_positions[dir1_id]
                dir2_top = top_positions[dir2_id]
                dir2_bottom = bottom_positions[dir2_id]
                dir2_left = left_positions[dir2_id]
                dir2_right = right_positions[dir2_id]
                #if (max(dir1_left, dir2_left) < min(dir1_right, dir2_right)) and (max(dir1_top, dir2_top) < min(dir1_bottom, dir2_bottom)):
                #    overlapping_pairs.append([dir1_id, dir2_id])
                if (dir1_top < dir2_top and dir1_bottom > dir2_bottom):
                    overlapping_pairs.append([dir1_id, dir2_id])

    # 以上を作りなおしたい　ifだけ残る
    gap_x = 1000
    gap_y = 800
    all_directories_set = set(directory['id'] for directory in directories)
    all_directories = list(all_directories_set)
    for i in range(len(all_directories)):
        for j in range(i+1, len(all_directories)):
            print()

    # pairsのコピーを作成
    pairs_list = overlapping_pairs.copy()

    # ペアの後者が同じであるペアを抽出して削除
    for i in range(len(pairs_list)):
        for j in range(i + 1, len(pairs_list)):
            if j >= len(pairs_list):
                break

            if pairs_list[i][1] == pairs_list[j][1]:
                pair1 = pairs_list[i]
                pair2 = pairs_list[j]

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
                    pairs_list.remove(pair1)
                else:
                    pairs_list.remove(pair2)

    # ソート処理を追加
    pairs_list.sort(key=lambda x: top_positions[x[0]])

    # (2)のリスト
    list2 = []

    # リストの結合と集合型を使って変換
    for l in pairs_list:
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
    # 以下の変数を追加します
    center_x = 27828.0 # 各レベルの中央の座標を表す変数です
    max_level = len(list2) - 1 # 最下位のレベルのインデックスを表す変数です

    for lst in list2:
        lst.sort(key=lambda dir_id: directories[next(i for i, d in enumerate(directories) if d["id"] == dir_id)]["x"])
    for level, list_x in enumerate(list2):
        #重なったディレクトリの端同士の距離を求め，距離+1000移動させる
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

            distance = max_x + 1000 - min_x

            for obj in allgraph_objects['eleObjs']:
                if obj['group'] == 'nodes' and obj['data'].get("parent"):
                    parent_dir = obj['data']['parent'].split('/')[1]
                    if parent_dir == list_x[i+1] and obj['position']['x'] < max_x + 1000:
                        obj['position']['x'] += distance

        # 以下の処理を追加します
        # 各レベルのディレクトリのxの値の最大値と最小値を求めます
        level_max_x = float('-inf')
        level_min_x = float('inf')
        for dir_id in list_x:
            for obj in allgraph_objects['eleObjs']:
                if obj['group'] == 'nodes' and obj['data'].get("parent"):
                    parent_dir = obj['data']['parent'].split('/')[1]
                    if parent_dir == dir_id:
                        dir_x = obj['position']['x']
                        if dir_x > level_max_x:
                            level_max_x = dir_x
                        if dir_x < level_min_x:
                            level_min_x = dir_x

        # 各レベルのディレクトリのxの値の平均値を求めます
        level_mean_x = (level_max_x + level_min_x) / 2

        # 各レベルのディレクトリとオブジェクトの位置を、center_xとlevel_mean_xの差だけずらします
        shift = center_x - level_mean_x
        for dir_id in list_x:
            directories[next(i for i, d in enumerate(directories) if d["id"] == dir_id)]["x"] += shift
        for obj in allgraph_objects['eleObjs']:
            if obj['group'] == 'nodes' and obj['data'].get("parent"):
                parent_dir = obj['data']['parent'].split('/')[1]
                if parent_dir in list_x:
                    obj['position']['x'] += shift
    moved_directories = [item for sublist in list2 for item in sublist]
    all_directories_set = set(directory['id'] for directory in directories)
    all_directories = list(all_directories_set)
    unique_ids = list(all_directories_set - set(moved_directories))
    # 新たに発生した重複の再帰的な処理：x軸方向の処理で動かしたディレクトリ同士は重なっていないので，重複の一方はunique_ids内のディレクトリになるため，そちらを動かす
    overlap = True
    while overlap == True:
        overlap = False
        for i in range(len(all_directories)):
            for j in range(i+1, len(all_directories)):
                min_x1, max_x1, min_y1, max_y1 = get_area(allgraph_objects, all_directories[i])
                min_x2, max_x2, min_y2, max_y2 = get_area(allgraph_objects, all_directories[j])
                # 2領域が重なっているか判定
                if (max(min_x1, min_x2) <= min(max_x1, max_x2)) and (max(min_y1, min_y2) <= min(max_y1, max_y2)):
                    overlap = True
                    if all_directories[i] in unique_ids:
                        distance = max_x2 + 1000 - min_x1
                        allgraph_objects = move_directories(allgraph_objects, all_directories[i], 'x', distance)
                    if all_directories[j] in unique_ids:
                        distance = max_x1 + 1000 - min_x2
                        allgraph_objects = move_directories(allgraph_objects, all_directories[j], 'x', distance)

    return directories

# 引数directory(string)の領域を求める
def get_area(allgraph_objects, directory):
    max_x = float('-inf')
    min_x = float('inf')
    max_y = float('-inf')
    min_y = float('inf')

    for obj in allgraph_objects['eleObjs']:
        if obj['group'] == 'nodes' and obj['data'].get('parent'):
            if obj['data']['parent'] == "/"+directory:
                # ノードのx座標とy座標を取得
                node_x = obj['position']['x']
                node_y = obj['position']['y']

                # x座標の最大値と最小値を更新
                if node_x > max_x:
                    max_x = node_x
                if node_x < min_x:
                    min_x = node_x

                # y座標の最大値と最小値を更新
                if node_y > max_y:
                    max_y = node_y
                if node_y < min_y:
                    min_y = node_y

    # 最大値と最小値を含むタプルを返す
    return (min_x, max_x, min_y, max_y)

# 引数directory(string)に属するノードをaxis方向(｢'x'｣もしくは｢'y'｣)にdistance(float)だけ動かす
def move_directories(allgraph_objects, directory, axis, distance):
    for obj in allgraph_objects['eleObjs']:
        if obj['group'] == 'nodes' and obj['data'].get('parent'):
            if obj['data']['parent'] == "/"+directory:
                obj['position'][axis] += distance
    
    return allgraph_objects



allGraph_json = open('graph_attrs/graph_class_gpt_1403.json', 'r')
allgraph_objects = json.load(allGraph_json)
directories = [{'id': 'Sets_and_TopologySets', 'x': 54745.29230769233, 'y': 26869.846153846152}, {'id': 'Sets_and_TopologyRelations', 'x': 45449.850000000006, 'y': 20412.0}, {'id': 'Sets_and_TopologyFunctions', 'x': 59652.78000000001, 'y': 25358.4}, {'id': 'Sets_and_TopologyOrdinal_Numbers', 'x': 52305.42857142857, 'y': 26583.428571428572}, {'id': 'Sets_and_TopologyOrder', 'x': 60806.880000000005, 'y': 24300.0}, {'id': 'Math_LogicAxiomatic_Set_Theory', 'x': 52247.165217391295, 'y': 36978.260869565216}, {'id': 'AlgebraRings', 'x': 49055.36347826087, 'y': 36433.565217391304}, {'id': 'Sets_and_TopologyCategories_and_Functors', 'x': 51296.799999999996, 'y': 34578.0}, {'id': 'AlgebraFields', 'x': 54097.151999999995, 'y': 34685.28}, {'id': 'Func_AnFunction_Space', 'x': 55064.25, 'y': 38664.0}, {'id': 'Sets_and_TopologyNumbers', 'x': 56559.321290322594, 'y': 20760.387096774193}, {'id': 'Math_LogicProof_Theory', 'x': 52389.6, 'y': 9180.0}, {'id': 'AlgebraAlgebra', 'x': 45905.100000000006, 'y': 25164.0}, {'id': 'Sets_and_TopologyCardinality', 'x': 65002.1, 'y': 29952.0}, {'id': 'Disc_MathGraph_Theory', 'x': 41976.15000000004, 'y': 38347.71428571428}, {'id': 'Sets_and_TopologyReal_Numbers_and_the_Real_Line', 'x': 54393.600000000006, 'y': 13500.0}, {'id': 'Number_TheoryElementary_Number_Theory', 'x': 65309.64444444446, 'y': 41164.0}, {'id': 'Math_LogicFormal_Systems_and_Proofs', 'x': 49316.85381818183, 'y': 39498.545454545456}, {'id': 'Num_AnNumerical_Analysis', 'x': 50976.600000000006, 'y': 15876.0}, {'id': 'AnalysisAnalysis', 'x': 59445.600000000006, 'y': 19980.0}, {'id': 'AlgebraPolynomials', 'x': 63814.2, 'y': 43153.71428571428}, {'id': 'Disc_MathEnumerative_Combinatorics', 'x': 80149.20000000001, 'y': 35676.0}, {'id': 'Sets_and_TopologyBoolean_Algebra', 'x': 46019.71764705882, 'y': 38454.35294117647}, {'id': 'Sets_and_TopologyConvergence', 'x': 76604.68235294118, 'y': 40182.35294117647}, {'id': 'AnalysisHarmonic_Analysis_Real_Analysis', 'x': 80160.0, 'y': 29052.0}, {'id': 'Complex_AnComplex_Analysis', 'x': 101106.0, 'y': 21276.0}, {'id': 'AnalysisContinuous_Functions', 'x': 58126.04999999999, 'y': 41688.0}, {'id': 'AnalysisDifferential_Calculus', 'x': 84894.08, 'y': 42094.28571428572}, {'id': 'AlgebraAlgebraic_Equations', 'x': 86130.98181818181, 'y': 46528.36363636364}, {'id': 'AnalysisSeries', 'x': 87836.59999999999, 'y': 44172.0}, {'id': 'Complex_AnHolomorphic_Functions', 'x': 72737.2, 'y': 39996.0}, {'id': 'Prob_TheoryProbability_Theory', 'x': 64666.84860000001, 'y': 44323.2}, {'id': 'AnalysisMeasure_Theory', 'x': 89748.87272727274, 'y': 42234.545454545456}, {'id': 'Sets_and_TopologyEquivalence_Relations', 'x': 42201.6, 'y': 22572.0}, {'id': 'Info_MathCoding_Theory', 'x': 38170.032, 'y': 40456.8}, {'id': 'Opt_TheoryCombinatorial_Optimization', 'x': 46569.6, 'y': 28188.000000000004}, {'id': 'AnalysisConvex_Analysis', 'x': 67262.16, 'y': 37260.0}, {'id': 'GeometryTrigonometry', 'x': 94925.23636363636, 'y': 43975.63636363636}, {'id': 'AnalysisElementary_Functions', 'x': 50740.4, 'y': 42444.0}, {'id': 'Info_MathInformation_Theory', 'x': 54707.200000000004, 'y': 38412.0}, {'id': 'AnalysisFourier_Transform', 'x': 109914.0, 'y': 42444.0}, {'id': 'Math_LogicComputable_Functions', 'x': 83825.55918367348, 'y': 46957.95918367347}, {'id': 'Number_TheoryContinued_Fractions', 'x': 47541.600000000006, 'y': 19116.0}, {'id': 'AnalysisIntegration', 'x': 70074.85, 'y': 43668.0}, {'id': 'Sets_and_TopologyLattices', 'x': 54387.96923076923, 'y': 41746.153846153844}, {'id': 'Info_MathCryptography', 'x': 60710.4, 'y': 44064.0}, {'id': 'GeometryFoundations_of_Geometry', 'x': 41130.600000000006, 'y': 26892.0}, {'id': 'Sets_and_TopologyTopological_Spaces', 'x': 42969.69032258069, 'y': 34900.25806451613}, {'id': 'AlgebraVector_Spaces', 'x': 59343.1542857143, 'y': 35593.71428571428}, {'id': 'Groups_and_RepGroup', 'x': 51302.52857142858, 'y': 38648.57142857143}, {'id': 'Sets_and_TopologyStructures', 'x': 50250.479999999996, 'y': 31212.0}, {'id': 'GeometryAffine_Geometry', 'x': 55010.640000000014, 'y': 37778.4}, {'id': 'AlgebraClifford_Algebras', 'x': 48849.600000000006, 'y': 23868.0}, {'id': 'Sets_and_TopologyMetric_Spaces', 'x': 51327.36, 'y': 38383.2}, {'id': 'GeometryProjective_Geometry', 'x': 63641.35384615384, 'y': 41646.46153846154}, {'id': 'AlgebraMatrices', 'x': 56448.771428571425, 'y': 42567.42857142857}, {'id': 'AlgebraModules', 'x': 55311.399999999994, 'y': 43332.0}, {'id': 'AlgebraPolynomial_Rings', 'x': 78338.64, 'y': 47196.0}, {'id': 'TopologyFiber_Bundle', 'x': 67446.0, 'y': 42444.0}, {'id': 'Complex_AnAnalytic_Space', 'x': 62986.8, 'y': 41796.0}, {'id': 'Func_AnBanach_Space', 'x': 60322.41600000001, 'y': 47092.32}, {'id': 'Func_AnHilbert_Space', 'x': 45100.8, 'y': 29160.0}, {'id': 'Info_MathFormal_Language_Theory_and_Automata', 'x': 56210.57142857143, 'y': 38741.142857142855}, {'id': 'Info_MathComputational_Complexity_Theory', 'x': 37401.600000000006, 'y': 26460.0}, {'id': 'GeometryEuclidean_Space', 'x': 55834.14545454544, 'y': 43465.09090909091}, {'id': 'GeometryEuclidean_Geometry', 'x': 48575.55, 'y': 40608.0}, {'id': 'Groups_and_RepFinite_Group', 'x': 65652.0, 'y': 36396.0}, {'id': 'GeometryCurves', 'x': 50433.80000000001, 'y': 40428.0}, {'id': 'Sets_and_TopologyUniform_Spaces', 'x': 65703.2, 'y': 42876.0}, {'id': 'GeometryConformal_Geometry', 'x': 61213.8, 'y': 39420.0}, {'id': 'AlgebraCommutative_Rings', 'x': 68932.8, 'y': 47700.0}, {'id': 'AlgebraJordan_Algebras', 'x': 33747.6, 'y': 43308.00000000001}, {'id': 'AlgebraMultivariate_Rings', 'x': 42219.6, 'y': 43308.00000000001}, {'id': 'Number_TheoryNumber-Theoretic_Functions', 'x': 83301.2, 'y': 48348.0}, {'id': 'TopologyComplex', 'x': 47080.4, 'y': 46908.0}, {'id': 'Math_LogicModel_Theory', 'x': 39865.499999999985, 'y': 47034.0}, {'id': 'Math_LogicDecision_Problems', 'x': 24441.6, 'y': 48060.00000000001}, {'id': 'Opt_TheoryGame_Theory', 'x': 104628.0, 'y': 48492.00000000001}, {'id': 'Alg_GeometryAlgebraic_Curves', 'x': 73027.2, 'y': 50220.0}, {'id': 'Number_TheoryGeometry_of_Numbers_and_Approximations_in_Number_Theory', 'x': 40881.6, 'y': 50436.0}, {'id': 'AlgebraGalois_Theory', 'x': 56660.24999999999, 'y': 52596.0}]

for n in range(len(directories)):
    part_json = open('graph_attrs/cluster/compound_dot_graph' + str(directories[n]['id']) + ".json", 'r')
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
with open('graph_attrs/graph_classHierar_1403_T.json', 'w') as f:
    json.dump(allgraph_objects, f, indent=4)