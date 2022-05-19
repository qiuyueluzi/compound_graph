import json

graph_json = open('graph_attrs/compound_dot_graph.json', 'r')
class_json = open('graph_attrs/mml_classification.json', 'r')
graph_objects = json.load(graph_json)
class_objects = json.load(class_json)



for index in range(334):
    if graph_objects['eleObjs'][index]['data']['id'].lower() == class_objects['mml_classification'][index]['mml-name']:
        graph_objects['eleObjs'][index].update(class_objects['mml_classification'][index])
        

with open('graph_attrs/graph_class.json', 'w') as f :
    json.dump(graph_objects, f, indent=4)