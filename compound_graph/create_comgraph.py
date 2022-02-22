import json

graph_json = open('graph_attrs/compound_dot_graph.json', 'r')
class_json = open('graph_attrs/mml_classification.json', 'r')
graph_objects = json.load(graph_json)
class_objects = json.load(class_json)

print(graph_objects)
print(class_objects)