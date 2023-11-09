import json
import copy

graph_json = open('graph_attrs/compound_dot_graph538.json', 'r')
class_json = open('graph_attrs/mml_classification_gpt_named.json', 'r')
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
    if class_objects['mml_classification'][index].get("directory") and len(class_objects['mml_classification'][index]['directory']) > 0:
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

positions = {}
counts = {}
for obj in graph_objects["eleObjs"]:
    if obj["group"] == "nodes" and obj["data"].get("parent"):
        parent_top = obj["data"]["parent"].split("/")[1]
        position = obj["position"]
        if parent_top not in positions:
            positions[parent_top] = {"id": parent_top, "x": position["x"], "y": position["y"]}
            counts[parent_top] = 1
        else:
            positions[parent_top]["x"] += position["x"]
            positions[parent_top]["y"] += position["y"]
            counts[parent_top] += 1
for parent_top in positions:
    positions[parent_top]["x"] /= counts[parent_top]
    positions[parent_top]["y"] /= counts[parent_top]
print(list(positions.values()))

with open('graph_attrs/graph_class_gpt538.json', 'w') as f :
    json.dump(graph_objects, f, indent=4)

