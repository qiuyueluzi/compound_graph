# (1)のリスト
list1 = [['set', 'number'], ['number', 'computer'], ['analysis', 'algebra'], ['analysis', 'numerical'], ['analysis', 'cryptography'], ['analysis', 'category'], ['sequence', 'graph'], ['sequence', 'economics'], ['sequence', 'geometry'], ['logic', 'sequence'], ['logic', 'graph'], ['logic', 'probability'], ['probability', 'combinatorics']]

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
