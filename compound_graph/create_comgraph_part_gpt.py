import json
import copy

def resolve_node_overlap(allgraph_objects):
    # ノードの重なりを解消する関数
    positions = {}  # 各座標に配置されたノードの情報を保持する辞書

    # 重なりをチェックし、重なりがある場合はノードを移動させる
    for node in allgraph_objects['eleObjs']:
        nonOverlap = True
        if node["group"] == 'nodes':
            node_id = node['data']['id']
            x = node['position']['x']
            y = node['position']['y']

            if (x, y) in positions:
                # 重なりが発生した場合、ノードを移動させる
                while (x, y) in positions:
                    x += 5000  # X座標方向に50ずつずらす（任意の移動量）

                # 移動後の座標を設定
                node['position']['x'] = x
                node['position']['y'] = y
                nonOverlap = False

            # ノードの座標を辞書に追加
            positions[(x, y)] = node_id

    return allgraph_objects


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
allgraph_objects = resolve_node_overlap(allgraph_objects)

with open('graph_attrs/graph_classHierar_test.json', 'w') as f:
    json.dump(allgraph_objects, f, indent=4)