import json
import pandas

graph_json = open('graph_attrs/compound_dot_graph.json', 'r')
graph_objects = json.load(graph_json)

classfication = pandas.read_excel('graph_attrs/mml_classification')