import json
import copy

allGraph_json = open('graph_attrs/graph_class.json', 'r')
allgraph_objects = json.load(allGraph_json)

directories = [{"id":"Economics", "x":7324.71, "y":24110.085}, {"id":"Combinatorics", "x":11077.830000000002, "y":29782.085}, 
                {"id":"Logic", "x":7104.59, "y":20406.085}, {"id":"Set", "x":14799.244, "y":14800.550000000001}, 
                {"id":"Cryptography", "x":11954.580000000002, "y":30294.085}, {"id":"Graph", "x":3987.990000000002, "y":22270.085}, 
                {"id":"Computer", "x":6819.310000000001, "y":13494.085000000001}, {"id":"Probability", "x":26829.079999999998, "y":23838.085}, 
                {"id":"Category", "x":5255.33, "y":25596.000000000004}, {"id":"Geometry", "x":8289.330000000002, "y":16302.085000000001}, 
                {"id":"Sequence", "x":15159.830000000002, "y":27202.085}, {"id":"Number", "x":23087.96, "y":18366.085}, 
                {"id":"Numerical", "x":27409.68, "y":34800.17}, {"id":"Analysis", "x":19177.81, "y":32440.55}, {"id":"Algebra", "x":15022.840000000002, "y":22974.085}]

for n in range(len(directories)):
    part_json = open('graph_attrs/compound_dot_graph'+str(directories[n]['id'])+".json", 'r')
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



with open('graph_attrs/graph_classHierar.json', 'w') as f :
    json.dump(allgraph_objects, f, indent=4)
