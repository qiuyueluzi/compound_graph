import json

# JSONファイルを読み込む
with open('graph_attrs/graph_class.json') as file:
    data = json.load(file)

# 共通の親を持つノードの座標を格納する辞書
node_positions = {}

# ノードデータを走査する
for eleObj in data['eleObjs']:
    # "group"ステータスが"nodes"であるオブジェクトを処理する
    if eleObj['group'] == 'nodes':
        # "parent"ステータスから共通の親を取得する
        parent = eleObj['data'].get('parent', None)
        if parent:
            # 共通の親を親リストに追加する
            parent_key = parent.split('/')[1]
            node_positions.setdefault(parent_key, [])
            # ノードの座標を取得して辞書に追加する
            position = eleObj['position']
            node_positions[parent_key].append((position['x'], position['y']))

# 各親の重心を計算する
for parent_key, positions in node_positions.items():
    # ノードの数と座標の合計値を計算する
    node_count = len(positions)
    sum_x = sum(position[0] for position in positions)
    sum_y = sum(position[1] for position in positions)
    # 座標の重心を計算する
    center_x = sum_x / node_count
    center_y = sum_y / node_count
    # 重心の座標を表示する
    print(f'{{"id":"{parent_key}", "x":{center_x}, "y":{center_y}}},')