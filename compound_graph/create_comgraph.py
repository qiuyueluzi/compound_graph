import json
import copy

graph_json = open('graph_attrs/compound_dot_graph.json', 'r')
class_json = open('graph_attrs/mml_classification_gpt.json', 'r')
graph_objects = json.load(graph_json)
class_objects = json.load(class_json)

def searchVal(name):
    for index in range(len(graph_objects['parents'])):
        if graph_objects['parents'][index]['data']['id'] == name:
            return index

graph_objects.update({'parents':[]})
nodeData = {"group": "nodes",
            "data": {
                "id": None,
                "name": None,
                "parent": None
            },}

parents_set = set()

for index in range(len(class_objects['mml_classification'])):
    if len(class_objects['mml_classification'][index]['directory']) > 0:
        elementData = graph_objects['eleObjs'][index]['data']
        classData = class_objects['mml_classification'][index]
        directoryData = classData['directory']
        for node in graph_objects['eleObjs']:
            if node['data'].get('id'):
                if node['data']['id'].lower() == classData['mml-name'] and directoryData:
                    node['data']['parent'] = directoryData

                    parent = directoryData
                    parents_set.add(parent)
                    ancestors = parent.split('/')
                    parentName = ""
                    for generation in range(1, len(ancestors)):
                        parentName += "/" + ancestors[generation]
                        parents_set.add(parentName)

parentIds = list(parents_set)
for index in range(len(parentIds)):
    graph_objects['parents'].append(copy.deepcopy(nodeData))
    parentId = parentIds[index]
    parentNameIndex = parentId.rfind('/')
    displayName = parentId[parentNameIndex+1:]
    parentsData = graph_objects['parents'][index]['data']
    parentsData['id'] = parentId
    parentsData['name'] = displayName
    parentsData['parent'] = parentId[0:parentNameIndex]

# ノードの位置情報と親IDのマッピングを作成
node_positions = {}
for obj in graph_objects['eleObjs']:
    if obj['group'] == 'nodes':
        node_id = obj['data']['id']
        position = obj['position']
        node_positions[node_id] = position

# ノードの一覧を取得してparentのリストを作成
parent_set = set()
parent_list = []
for obj in graph_objects['eleObjs']:
    if 'parent' in obj['data']:
        parent_id = obj['data']['parent'].split('/')[1]
        if parent_id and parent_id not in parent_set:
            parent_set.add(parent_id)
            positions = [node_positions[node_id] for node_id in node_positions if node_id in parent_id]
            avg_position = {
                'x': sum(pos['x'] for pos in positions) / len(positions),
                'y': sum(pos['y'] for pos in positions) / len(positions)
            }
            parent_list.append({"id": parent_id, "x": avg_position['x'], "y": avg_position['y']})

# 結果の表示
print(parent_list)

with open('graph_attrs/graph_class_gpt.json', 'w') as f :
    json.dump(graph_objects, f, indent=4)

