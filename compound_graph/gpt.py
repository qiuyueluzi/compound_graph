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
