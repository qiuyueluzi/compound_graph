pairs = [['set', 'computer'], ['set', 'number'], ['set', 'economics'], ['set', 'geometry'], ['number', 'computer'], ['analysis', 'algebra'], ['analysis', 'combinatorics'], ['analysis', 'probability'], ['analysis', 'numerical'], ['analysis', 'cryptography'], ['analysis', 'category'], ['algebra', 'combinatorics'], ['algebra', 'cryptography'], ['sequence', 'graph'], ['sequence', 'economics'], ['sequence', 'geometry'], ['logic', 'sequence'], ['logic', 'graph'], ['logic', 'combinatorics'], ['logic', 'probability'], ['logic', 'economics'], ['logic', 'geometry'], ['probability', 'combinatorics']]

directories = [
    {"id":"set", "x":13731.638682352936, "y":14704.517647058823},
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
    {"id":"category", "x":5579.7, "y":25596.000000000004},
]

# pairsのコピーを作成
pairs_copy = pairs.copy()

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
print(list2)
