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


    return directories




allGraph_json = open('graph_attrs/graph_class_gpt_1403.json', 'r')
allgraph_objects = json.load(allGraph_json)
#directories = [{'id': 'I9', 'x': 24754.5, 'y': 20628.0}, {'id': 'II1', 'x': 21586.736842105263, 'y': 7315.578947368421}, {'id': 'II2', 'x': 24209.25, 'y': 14418.0}, {'id': 'II4', 'x': 14694.0, 'y': 18962.709677419356}, {'id': 'II13', 'x': 23904.0, 'y': 16740.0}, {'id': 'II12', 'x': 20295.0, 'y': 16092.000000000002}, {'id': 'III10', 'x': 21438.0, 'y': 10908.0}, {'id': 'II24', 'x': 19410.0, 'y': 16956.0}, {'id': 'III6', 'x': 22200.0, 'y': 8748.0}, {'id': 'XII6', 'x': 22200.0, 'y': 9180.0}, {'id': 'I17', 'x': 25080.000000000004, 'y': 17388.0}, {'id': 'III1', 'x': 17565.0, 'y': 18252.0}, {'id': 'XIX1', 'x': 19612.0, 'y': 12348.0}, {'id': 'II6', 'x': 23484.0, 'y': 18684.0}, {'id': 'XX1', 'x': 21313.8, 'y': 12549.6}, {'id': 'II9', 'x': 18130.615384615383, 'y': 14663.076923076924}, {'id': 'II10', 'x': 19575.0, 'y': 14580.0}, {'id': 'I3', 'x': 22170.75, 'y': 21258.0}, {'id': 'XV1', 'x': 19623.0, 'y': 16308.0}, {'id': 'X1', 'x': 618.0, 'y': 17820.0}, {'id': 'III4', 'x': 12801.6, 'y': 22658.4}, {'id': 'I1', 'x': 22938.000000000004, 'y': 18684.0}, {'id': 'I13', 'x': 19710.0, 'y': 16524.0}, {'id': 'XIX3', 'x': 19849.5, 'y': 16848.0}, {'id': 'II15', 'x': 18757.636363636364, 'y': 23632.363636363636}, {'id': 'II19', 'x': 11726.0, 'y': 23220.0}, {'id': 'XIX2', 'x': 20033.25, 'y': 21384.0}, {'id': 'III2', 'x': 10968.0, 'y': 19548.0}, {'id': 'X25', 'x': 9102.0, 'y': 21880.8}, {'id': 'XI1', 'x': 1752.0, 'y': 23004.000000000004}, {'id': 'X2', 'x': 8552.0, 'y': 22140.0}, {'id': 'X6', 'x': 7154.608695652174, 'y': 24750.782608695652}, {'id': 'III5', 'x': 6325.5, 'y': 24300.0}, {'id': 'X18', 'x': 9504.0, 'y': 22572.0}, {'id': 'XI2', 'x': 2724.0000000000005, 'y': 23652.0}, {'id': 'XVII1', 'x': 12291.42857142857, 'y': 22942.285714285714}, {'id': 'X13', 'x': 8280.545454545454, 'y': 23632.363636363636}, {'id': 'II3', 'x': 19182.0, 'y': 19116.0}, {'id': 'XXII16', 'x': 21558.0, 'y': 23436.0}, {'id': 'XXI9', 'x': 22548.0, 'y': 23868.0}, {'id': 'X4', 'x': 5856.0, 'y': 23436.0}, {'id': 'VII13', 'x': 5618.4, 'y': 24904.8}, {'id': 'X19', 'x': 12246.0, 'y': 23004.000000000004}, {'id': 'IV1', 'x': 14823.000000000002, 'y': 23220.0}, {'id': 'IV6', 'x': 9216.0, 'y': 24300.0}, {'id': 'X23', 'x': 11802.000000000002, 'y': 27756.0}, {'id': 'II8', 'x': 19014.0, 'y': 24084.0}, {'id': 'IV2', 'x': 15318.0, 'y': 24300.0}, {'id': 'IV3', 'x': 10236.0, 'y': 25164.0}, {'id': 'X11', 'x': 12064.333333333334, 'y': 26748.0}, {'id': 'II14', 'x': 21768.0, 'y': 24732.0}, {'id': 'XX6', 'x': 16584.0, 'y': 24300.0}, {'id': 'VII9', 'x': 21870.0, 'y': 7452.0}, {'id': 'II16', 'x': 15654.0, 'y': 25164.0}]
directories = [{'id': 'Sets_and_TopologySets', 'x': 54745.29230769233, 'y': 26869.846153846152}, {'id': 'Sets_and_TopologyRelations', 'x': 45449.850000000006, 'y': 20412.0}, {'id': 'Sets_and_TopologyFunctions', 'x': 59652.78000000001, 'y': 25358.4}, {'id': 'Sets_and_TopologyOrdinal_Numbers', 'x': 52305.42857142857, 'y': 26583.428571428572}, {'id': 'Sets_and_TopologyOrder', 'x': 60806.880000000005, 'y': 24300.0}, {'id': 'Math_LogicAxiomatic_Set_Theory', 'x': 52247.165217391295, 'y': 36978.260869565216}, {'id': 'AlgebraRings', 'x': 49055.36347826087, 'y': 36433.565217391304}, {'id': 'Sets_and_TopologyCategories_and_Functors', 'x': 51296.799999999996, 'y': 34578.0}, {'id': 'AlgebraFields', 'x': 54097.151999999995, 'y': 34685.28}, {'id': 'Func_AnFunction_Space', 'x': 55064.25, 'y': 38664.0}, {'id': 'Sets_and_TopologyNumbers', 'x': 56559.321290322594, 'y': 20760.387096774193}, {'id': 'Math_LogicProof_Theory', 'x': 52389.6, 'y': 9180.0}, {'id': 'AlgebraAlgebra', 'x': 45905.100000000006, 'y': 25164.0}, {'id': 'Sets_and_TopologyCardinality', 'x': 65002.1, 'y': 29952.0}, {'id': 'Disc_MathGraph_Theory', 'x': 41976.15000000004, 'y': 38347.71428571428}, {'id': 'Sets_and_TopologyReal_Numbers_and_the_Real_Line', 'x': 54393.600000000006, 'y': 13500.0}, {'id': 'Number_TheoryElementary_Number_Theory', 'x': 65309.64444444446, 'y': 41164.0}, {'id': 'Math_LogicFormal_Systems_and_Proofs', 'x': 49316.85381818183, 'y': 39498.545454545456}, {'id': 'Num_AnNumerical_Analysis', 'x': 50976.600000000006, 'y': 15876.0}, {'id': 'AnalysisAnalysis', 'x': 59445.600000000006, 'y': 19980.0}, {'id': 'AlgebraPolynomials', 'x': 63814.2, 'y': 43153.71428571428}, {'id': 'Disc_MathEnumerative_Combinatorics', 'x': 80149.20000000001, 'y': 35676.0}, {'id': 'Sets_and_TopologyBoolean_Algebra', 'x': 46019.71764705882, 'y': 38454.35294117647}, {'id': 'Sets_and_TopologyConvergence', 'x': 76604.68235294118, 'y': 40182.35294117647}, {'id': 'AnalysisHarmonic_Analysis,_Real_Analysis', 'x': 80160.0, 'y': 29052.0}, {'id': 'Complex_AnComplex_Analysis', 'x': 101106.0, 'y': 21276.0}, {'id': 'AnalysisContinuous_Functions', 'x': 58126.04999999999, 'y': 41688.0}, {'id': 'AnalysisDifferential_Calculus', 'x': 84894.08, 'y': 42094.28571428572}, {'id': 'AlgebraAlgebraic_Equations', 'x': 86130.98181818181, 'y': 46528.36363636364}, {'id': 'AnalysisSeries', 'x': 87836.59999999999, 'y': 44172.0}, {'id': 'Complex_AnHolomorphic_Functions', 'x': 72737.2, 'y': 39996.0}, {'id': 'Prob_TheoryProbability_Theory', 'x': 64666.84860000001, 'y': 44323.2}, {'id': 'AnalysisMeasure_Theory', 'x': 89748.87272727274, 'y': 42234.545454545456}, {'id': 'Sets_and_TopologyEquivalence_Relations', 'x': 42201.6, 'y': 22572.0}, {'id': 'Info_MathCoding_Theory', 'x': 38170.032, 'y': 40456.8}, {'id': 'Opt_TheoryCombinatorial_Optimization', 'x': 46569.6, 'y': 28188.000000000004}, {'id': 'AnalysisConvex_Analysis', 'x': 67262.16, 'y': 37260.0}, {'id': 'GeometryTrigonometry', 'x': 94925.23636363636, 'y': 43975.63636363636}, {'id': 'AnalysisElementary_Functions', 'x': 50740.4, 'y': 42444.0}, {'id': 'Info_MathInformation_Theory', 'x': 54707.200000000004, 'y': 38412.0}, {'id': 'AnalysisFourier_Transform', 'x': 109914.0, 'y': 42444.0}, {'id': 'Math_LogicComputable_Functions', 'x': 83825.55918367348, 'y': 46957.95918367347}, {'id': 'Number_TheoryContinued_Fractions', 'x': 47541.600000000006, 'y': 19116.0}, {'id': 'AnalysisIntegration', 'x': 70074.85, 'y': 43668.0}, {'id': 'Sets_and_TopologyLattices', 'x': 54387.96923076923, 'y': 41746.153846153844}, {'id': 'Info_MathCryptography', 'x': 60710.4, 'y': 44064.0}, {'id': 'GeometryFoundations_of_Geometry', 'x': 41130.600000000006, 'y': 26892.0}, {'id': 'Sets_and_TopologyTopological_Spaces', 'x': 42969.69032258069, 'y': 34900.25806451613}, {'id': 'AlgebraVector_Spaces', 'x': 59343.1542857143, 'y': 35593.71428571428}, {'id': 'Groups_and_RepGroup', 'x': 51302.52857142858, 'y': 38648.57142857143}, {'id': 'Sets_and_TopologyStructures', 'x': 50250.479999999996, 'y': 31212.0}, {'id': 'GeometryAffine_Geometry', 'x': 55010.640000000014, 'y': 37778.4}, {'id': 'AlgebraClifford_Algebras', 'x': 48849.600000000006, 'y': 23868.0}, {'id': 'Sets_and_TopologyMetric_Spaces', 'x': 51327.36, 'y': 38383.2}, {'id': 'GeometryProjective_Geometry', 'x': 63641.35384615384, 'y': 41646.46153846154}, {'id': 'AlgebraMatrices', 'x': 56448.771428571425, 'y': 42567.42857142857}, {'id': 'AlgebraModules', 'x': 55311.399999999994, 'y': 43332.0}, {'id': 'AlgebraPolynomial_Rings', 'x': 78338.64, 'y': 47196.0}, {'id': 'TopologyFiber_Bundle', 'x': 67446.0, 'y': 42444.0}, {'id': 'Complex_AnAnalytic_Space', 'x': 62986.8, 'y': 41796.0}, {'id': 'Func_AnBanach_Space', 'x': 60322.41600000001, 'y': 47092.32}, {'id': 'Func_AnHilbert_Space', 'x': 45100.8, 'y': 29160.0}, {'id': 'Info_MathFormal_Language_Theory_and_Automata', 'x': 56210.57142857143, 'y': 38741.142857142855}, {'id': 'Info_MathComputational_Complexity_Theory', 'x': 37401.600000000006, 'y': 26460.0}, {'id': 'GeometryEuclidean_Space', 'x': 55834.14545454544, 'y': 43465.09090909091}, {'id': 'GeometryEuclidean_Geometry', 'x': 48575.55, 'y': 40608.0}, {'id': 'Groups_and_RepFinite_Group', 'x': 65652.0, 'y': 36396.0}, {'id': 'GeometryCurves', 'x': 50433.80000000001, 'y': 40428.0}, {'id': 'Sets_and_TopologyUniform_Spaces', 'x': 65703.2, 'y': 42876.0}, {'id': 'GeometryConformal_Geometry', 'x': 61213.8, 'y': 39420.0}, {'id': 'AlgebraCommutative_Rings', 'x': 68932.8, 'y': 47700.0}, {'id': 'AlgebraJordan_Algebras', 'x': 33747.6, 'y': 43308.00000000001}, {'id': 'AlgebraMultivariate_Rings', 'x': 42219.6, 'y': 43308.00000000001}, {'id': 'Number_TheoryNumber-Theoretic_Functions', 'x': 83301.2, 'y': 48348.0}, {'id': 'TopologyComplex', 'x': 47080.4, 'y': 46908.0}, {'id': 'Math_LogicModel_Theory', 'x': 39865.499999999985, 'y': 47034.0}, {'id': 'Math_LogicDecision_Problems', 'x': 24441.6, 'y': 48060.00000000001}, {'id': 'Opt_TheoryGame_Theory', 'x': 104628.0, 'y': 48492.00000000001}, {'id': 'Alg_GeometryAlgebraic_Curves', 'x': 73027.2, 'y': 50220.0}, {'id': 'Number_TheoryGeometry_of_Numbers_and_Approximations_in_Number_Theory', 'x': 40881.6, 'y': 50436.0}, {'id': 'AlgebraGalois_Theory', 'x': 56660.24999999999, 'y': 52596.0}]
#directories = [{'id': 'Math_LogicAxiomatic_Set_Theory', 'x': 41908.0, 'y': 20880.0}, {'id': 'Sets_and_TopologySets', 'x': 26236.8, 'y': 8143.2}, {'id': 'Sets_and_TopologyRelations', 'x': 22587.0, 'y': 15984.0}, {'id': 'Sets_and_TopologyFunctions', 'x': 21176.0625, 'y': 19305.0}, {'id': 'Sets_and_TopologyOrdinal_Numbers', 'x': 35681.0, 'y': 16884.0}, {'id': 'Sets_and_TopologyOrder', 'x': 25480.0, 'y': 19404.0}, {'id': 'AlgebraRings', 'x': 29191.5, 'y': 17496.0}, {'id': 'Sets_and_TopologyCategories_and_Functors', 'x': 24544.714285714286, 'y': 23929.714285714286}, {'id': 'AlgebraFields', 'x': 30543.0, 'y': 21168.0}, {'id': 'Func_AnFunction_Space', 'x': 25188.000000000004, 'y': 9180.0}, {'id': 'Math_LogicProof_Theory', 'x': 30744.0, 'y': 23436.0}, {'id': 'AlgebraAlgebra', 'x': 34110.0, 'y': 24818.4}, {'id': 'Disc_MathDiscrete_Mathematics_and_Combinatorics', 'x': 24520.0, 'y': 12348.0}, {'id': 'Sets_and_TopologyCardinality', 'x': 31879.714285714286, 'y': 18869.14285714286}, {'id': 'Info_MathMathematics_in_Computer_Science', 'x': 24874.2, 'y': 12981.6}, {'id': 'Sets_and_TopologyNumbers', 'x': 22278.0, 'y': 14988.0}, {'id': 'Sets_and_TopologyReal_Numbers_and_the_Real_Line', 'x': 22884.0, 'y': 14580.0}, {'id': 'Math_LogicFormal_Systems_and_Proofs', 'x': 30945.36, 'y': 21517.92}, {'id': 'Num_AnNumerical_Analysis', 'x': 22557.0, 'y': 16308.0}, {'id': 'AnalysisAnalysis', 'x': 10170.0, 'y': 21708.0}, {'id': 'AlgebraPolynomials', 'x': 26371.2, 'y': 23868.0}, {'id': 'Math_LogicFoundations_of_Mathematics', 'x': 29832.0, 'y': 22572.0}, {'id': 'Math_LogicRecursive_Theory', 'x': 23442.0, 'y': 16524.0}, {'id': 'Disc_MathEnumerative_Combinatorics', 'x': 25446.0, 'y': 16848.0}, {'id': 'Sets_and_TopologyBoolean_Algebra', 'x': 39280.61538461538, 'y': 24266.76923076923}, {'id': 'Sets_and_TopologyConvergence', 'x': 13536.75, 'y': 23598.0}, {'id': 'Disc_MathGraph_Theory', 'x': 32157.0, 'y': 21006.0}, {'id': 'AlgebraMatrices', 'x': 31048.105263157893, 'y': 26596.42105263158}, {'id': 'AnalysisHarmonic_Analysis,_Real_Analysis', 'x': 9885.6, 'y': 21880.8}, {'id': 'Complex_AnComplex_Analysis', 'x': 11340.000000000002, 'y': 23004.000000000004}, {'id': 'AnalysisContinuous_Functions', 'x': 6144.0, 'y': 22140.0}, {'id': 'AnalysisDifferential_Calculus', 'x': 9475.565217391304, 'y': 24750.782608695652}, {'id': 'AlgebraAlgebraic_Equations', 'x': 9732.0, 'y': 24516.0}, {'id': 'AnalysisSeries', 'x': 10374.0, 'y': 22572.0}, {'id': 'Complex_AnHolomorphic_Functions', 'x': 19220.0, 'y': 24156.0}, {'id': 'Prob_TheoryProbability_Theory', 'x': 14050.285714285714, 'y': 22942.285714285714}, {'id': 'AnalysisMeasure_Theory', 'x': 3188.7272727272725, 'y': 23985.81818181818}, {'id': 'Sets_and_TopologyEquivalence_Relations', 'x': 28008.0, 'y': 19116.0}, {'id': 'Mech_PhysCircuits', 'x': 29898.0, 'y': 23436.0}, {'id': 'Opt_TheoryCombinatorial_Optimization', 'x': 19434.0, 'y': 23868.0}, {'id': 'AnalysisConvex_Analysis', 'x': 1650.0, 'y': 23436.0}, {'id': 'GeometryTrigonometry', 'x': 7326.6, 'y': 24904.8}, {'id': 'AnalysisAsymptotic_Series', 'x': 4614.0, 'y': 23004.000000000004}, {'id': 'Number_TheoryNumber_Theory', 'x': 13674.0, 'y': 23220.0}, {'id': 'Number_TheoryDistribution_of_Prime_Numbers', 'x': 11880.0, 'y': 24300.0}, {'id': 'AnalysisFourier_Transform', 'x': 7716.0, 'y': 27756.0}, {'id': 'Sets_and_TopologyPermutations_and_Combinations', 'x': 17130.0, 'y': 24084.0}, {'id': 'Number_TheoryElementary_Number_Theory', 'x': 23109.0, 'y': 24084.0}, {'id': 'Number_TheoryContinued_Fractions', 'x': 17574.0, 'y': 25164.0}, {'id': 'AnalysisIntegration', 'x': 7454.333333333333, 'y': 26748.0}, {'id': 'Sets_and_TopologyLattices', 'x': 26671.090909090908, 'y': 25870.909090909092}, {'id': 'Info_MathCryptography', 'x': 37290.0, 'y': 24300.0}, {'id': 'GeometryFoundations_of_Geometry', 'x': 30168.0, 'y': 7884.0}, {'id': 'Sets_and_TopologyTopological_Spaces', 'x': 36794.51612903226, 'y': 25972.25806451613}, {'id': 'AlgebraVector_Spaces', 'x': 28970.444444444445, 'y': 25180.0}, {'id': 'Groups_and_RepGroup', 'x': 36438.88888888889, 'y': 25932.0}, {'id': 'Sets_and_TopologyStructures', 'x': 33032.0, 'y': 24012.0}, {'id': 'GeometryAffine_Geometry', 'x': 44324.16, 'y': 25716.96}, {'id': 'AlgebraClifford_Algebras', 'x': 43374.00000000001, 'y': 25596.000000000004}, {'id': 'Sets_and_TopologyMetric_Spaces', 'x': 39613.5, 'y': 25380.0}, {'id': 'GeometryProjective_Geometry', 'x': 49772.25, 'y': 25380.0}, {'id': 'AlgebraModules', 'x': 31778.0, 'y': 26388.0}, {'id': 'AlgebraPolynomial_Rings', 'x': 29376.0, 'y': 26460.0}, {'id': 'TopologyFiber_Bundle', 'x': 41022.0, 'y': 25164.0}, {'id': 'Func_AnBanach_Space', 'x': 18024.0, 'y': 25596.000000000004}, {'id': 'Info_MathFormal_Language_Theory_and_Automata', 'x': 31920.0, 'y': 24300.0}]

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
print(directories)
with open('graph_attrs/graph_classHierar_1403.json', 'w') as f:
    json.dump(allgraph_objects, f, indent=4)