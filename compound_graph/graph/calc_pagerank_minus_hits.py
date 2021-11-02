import os
import json


cwd = os.getcwd()

try:
    os.chdir("graph_attrs")
    with open("dot_graph_pagerank.json", "r") as f:
        dot_graph_pagerank = json.load(f)
    with open("dot_graph_hits_authority.json", "r") as f:
        dot_graph_authority = json.load(f)

finally:
    os.chdir(cwd)

node2pagerank = dict()
node2hits_authority = dict()

for i in dot_graph_pagerank['elements']['nodes']:
    node2pagerank[i['data']['id']] = i['data']['pagerank']

for i in dot_graph_authority['elements']['nodes']:
    node2hits_authority[i['data']['id']] = i['data']['authority']

node2pagerank_minus_hits = dict()
for k in node2pagerank.keys():
    node2pagerank_minus_hits[k] = \
        node2pagerank[k] - node2hits_authority[k]

with open("pagerank_minus_hits.txt", 'w') as fout:
    for k,v in sorted(node2pagerank_minus_hits.items(), key=lambda x:x[1]):
        fout.write(f'{k} {v} \n')