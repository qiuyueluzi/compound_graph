import json
import math

def adjust_directory_positions(allgraph_objects, directories):
    # ディレクトリの中央位置を求める
    center_x = sum(dir['x'] for dir in directories) / len(directories)
    center_y = sum(dir['y'] for dir in directories) / len(directories)

    # ディレクトリの範囲を調整する関数
    def adjust_directory_range(directory, center_x, center_y):
        node_positions = []
        for obj in allgraph_objects['eleObjs']:
            if obj['group'] == 'nodes':
                node_positions.append(obj['position'])

        while True:
            # ディレクトリの範囲を計算
            min_x = directory['x'] - 200
            max_x = directory['x'] + 200
            min_y = directory['y'] - 200
            max_y = directory['y'] + 200

            # 範囲とノード位置の判定
            overlapping = False
            for pos in node_positions:
                if min_x <= pos['x'] <= max_x and min_y <= pos['y'] <= max_y:
                    overlapping = True
                    break

            if not overlapping:
                break

            # ディレクトリを中央位置から遠ざける
            angle = math.atan2(directory['y'] - center_y, directory['x'] - center_x)
            directory['x'] += math.cos(angle)
            directory['y'] += math.sin(angle)

    # ディレクトリの範囲を調整
    for directory in directories:
        adjust_directory_range(directory, center_x, center_y)

    # ディレクトリに属するノードの位置を調整
    for directory in directories:
        for obj in allgraph_objects['eleObjs']:
            if obj['group'] == 'nodes' and obj['data'].get('parent') and obj['data']['parent'].split("/", 2)[1] == directory['id']:
                obj['position']['x'] += directory['x'] - center_x
                obj['position']['y'] += directory['y'] - center_y


    # ディレクトリを中央位置から遠ざける
    angle = math.atan2(directory['y'] - center_y, directory['x'] - center_x)
    directory['x'] += int(500 * math.cos(angle))
    directory['y'] += int(500 * math.sin(angle))
    for node in node_positions:
        if node['data'].get('parent') and node['data']['parent'].split("/", 2)[1] == directory['id']:
            node['position']['x'] += int(500 * math.cos(angle))
            node['position']['y'] += int(500 * math.sin(angle))

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
allgraph_objects = adjust_directory_positions(allgraph_objects, directories)

with open('graph_attrs/graph_classHierar_test.json', 'w') as f:
    json.dump(allgraph_objects, f, indent=4)