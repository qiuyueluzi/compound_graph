import json
import copy

graph_json = open('graph_attrs/compound_dot_graph.json', 'r')
class_json = open('graph_attrs/mml_classification.json', 'r')
graph_objects = json.load(graph_json)
class_objects = json.load(class_json)

def searchVal(name):
    for index in range(len(graph_objects['parents'])):
        if graph_objects['parents'][index]['data']['id'] == name:
            return index

def nums(first_number, last_number, step=1):
    return range(first_number, last_number, step)

graph_objects.update({'parents':[]})
nodeData = {"group": "nodes",
            "data": {
                "id": None,
                "name": None,
                "parent": None
            },}

parents = []

for index in range(334):
    if graph_objects['eleObjs'][index]['data']['id'].lower() == class_objects['mml_classification'][index]['mml-name']:
        graph_objects['eleObjs'][index]['data']['parent'] = class_objects['mml_classification'][index]['directory']

        parent = class_objects['mml_classification'][index]['directory']
        parents.append(parent)
        ance = parent.split('/')
        parentName = ""
        for gene in nums(1, len(ance)):
            parentName += "/" + ance[gene]
            if not parentName in parents:
                parents.append(parentName)

parentIds = list(set(parents))
for index in range(len(parentIds)):
    graph_objects['parents'].append(copy.deepcopy(nodeData))
    parentId = parentIds[index]
    parentNameIndex = parentId.rfind('/')
    displayName = parentId[parentNameIndex+1:]
    graph_objects['parents'][index]['data']['id'] = parentId
    graph_objects['parents'][index]['data']['name'] = displayName
    graph_objects['parents'][index]['data']['parent'] = parentId[0:parentNameIndex]


with open('graph_attrs/graph_class.json', 'w') as f :
    json.dump(graph_objects, f, indent=4)
