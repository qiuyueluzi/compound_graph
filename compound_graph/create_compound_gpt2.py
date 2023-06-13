import json
import math

cnt = 0

def adjust_directory_positions(allgraph_objects, directories):
    # ディレクトリの中央位置を求める
    center_x = sum(dir['x'] for dir in directories) / len(directories)
    center_y = sum(dir['y'] for dir in directories) / len(directories)

    """for directory in directories:
        for obj in allgraph_objects['eleObjs']:
            if obj['group'] == 'nodes' and obj['data'].get('parent') and obj['data']['parent'].split("/", 2)[1] == directory['id']:
                obj['position']['x'] += (directory['x'] - center_x)
                obj['position']['y'] += (directory['y'] - center_y)
        directory['x'] = directory['x'] - center_x
        directory['y'] = directory['y'] - center_y"""

    # ディレクトリの範囲を調整
    adjust_directory_range(allgraph_objects, directories, center_x, center_y)

    # ディレクトリの範囲を調整する関数
def adjust_directory_range(allgraph_objects, directories, center_x, center_y):
    node_positions = []
    inverse = 1

    for obj in allgraph_objects['eleObjs']:
        if obj['group'] == 'nodes':
            node_positions.append(obj)

    while True:
        overlapping_directories = []
        for directory in directories:
            # ディレクトリに属するノードの矩形領域を計算
            min_x = float('inf')
            max_x = float('-inf')
            min_y = float('inf')
            max_y = float('-inf')
            for pos in node_positions:
                if pos['data'].get('parent') and pos['data']['parent'].split("/", 2)[1] == directory['id']:
                    if pos['position']['x'] < min_x:
                        min_x = pos['position']['x']
                    if pos['position']['x'] > max_x:
                        max_x = pos['position']['x']
                    if pos['position']['y'] < min_y:
                        min_y = pos['position']['y']
                    if pos['position']['y'] > max_y:
                        max_y = pos['position']['y']

            # 矩形領域を調整して範囲を計算
            min_x -= 200
            max_x += 200
            min_y -= 200
            max_y += 200

            # 範囲と他のディレクトリに属するノードの判定

            for dir in directories:
                if dir['id'] != directory['id']:
                    for pos in node_positions:
                        if pos['data'].get('parent') and pos['data']['parent'].split("/", 2)[1] == dir['id']:
                            if min_x <= pos['position']['x'] <= max_x and min_y <= pos['position']['y'] <= max_y:
                                overlapping_directories.append(directory)
                                overlapping_directories.append(dir)

        if overlapping_directories == []:
            break
        print("hiraku")

        for directory in directories:
            for obj in node_positions:
                if obj['group'] == 'nodes' and obj['data'].get('parent') and obj['data']['parent'].split("/", 2)[1] == directory['id']:
                    obj['position']['x'] += (directory['x'] - center_x)/inverse
                    obj['position']['y'] += (directory['y'] - center_y)/inverse

        it = iter(overlapping_directories)
        while True:
            try:
                dir1 = next(it)
                dir2 = next(it)
            except StopIteration:
                break

            directorydata1 = count_nodes_in_directory(dir1, node_positions)
            directorydata2 = count_nodes_in_directory(dir2, node_positions)

            if directorydata1["node_count"] >= directorydata2["node_count"]:
                mini_directory = directorydata2
                big_directory = directorydata1
            else :
                mini_directory = directorydata1
                big_directory = directorydata2

            for node in node_positions:
                if node['data'].get('parent') and node['data']['parent'].split("/", 2)[1] == mini_directory["id"]:
                    node['position']['x'] += int((mini_directory['center_x'] - big_directory['center_x']) * inverse/100)
                    node['position']['y'] += int((mini_directory['center_y'] - big_directory['center_y']) * inverse/100)
        
        inverse += 5
        print(inverse)

            


def count_nodes_in_directory(directory, node_positions):
    global cnt
    cnt += 1
    count = 0
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    for node in node_positions:
        if node['data'].get('parent') and node['data']['parent'].split("/", 2)[1] == directory['id']:

            count += 1
            if node['position']['x'] < min_x:
                min_x = node['position']['x']
            if node['position']['x'] > max_x:
                max_x = node['position']['x']
            if node['position']['y'] < min_y:
                min_y = node['position']['y']
            if node['position']['y'] > max_y:
                max_y = node['position']['y']
    
    return {"id":directory["id"], "node_count":count, "center_x":int((min_x + max_x)/2), "center_y":int((min_y + max_y)/2)}
            

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