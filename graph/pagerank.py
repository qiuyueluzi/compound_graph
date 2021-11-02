import os
import json
import networkx as nx

def min_max_normalization(node2value, max_val, min_val):
    node_size = dict()
    node2value_max = max(node2value.values())
    node2value_min = min(node2value.values())

    for k, v in node2value.items():
        node_size[k] = {'pagerank': 
            ((v - node2value_min) / (node2value_max - node2value_min)) * (max_val - min_val) + min_val}

    return node_size


def rank_nodes_with_pagerank(node2pagerank):
    pagerank = list(set(node2pagerank.values()))
    pagerank_sorted = sorted(pagerank, reverse=True)
    pagerank2ranking = dict()
    ranking = 0
    for v in pagerank_sorted:
        pagerank2ranking[v] = ranking
        ranking += 1

    node2ranking = dict()
    for k,v in node2pagerank.items():
        node2ranking[k] = {"ranking": pagerank2ranking[v]}

    return node2ranking


def update_pagerank_for_set_node_attribute(node2pagerank):
    a = dict()
    for k,v in node2pagerank.items():
        a[k] = {'pagerank': v}
    return a


def grouping_for_ranking(node2ranking):
    max_ranking = 0
    for v in node2ranking.values():
        if v["ranking"] > max_ranking:
            max_ranking = v["ranking"]
    
    node2group = dict()
    for k,v in node2ranking.items():
        if v["ranking"] < max_ranking/10:
            node2group[k] = {"group": 0}
        elif v["ranking"] < max_ranking/10 * 2:
            node2group[k] = {"group": 1}
        elif v["ranking"] < max_ranking/10 * 3:
            node2group[k] = {"group": 2}
        elif v["ranking"] < max_ranking/10 * 4:
            node2group[k] = {"group": 3}
        elif v["ranking"] < max_ranking/10 * 5:
            node2group[k] = {"group": 4}
        elif v["ranking"] < max_ranking/10 * 6:
            node2group[k] = {"group": 5}
        elif v["ranking"] < max_ranking/10 * 7:
            node2group[k] = {"group": 6}
        elif v["ranking"] < max_ranking/10 * 8:
            node2group[k] = {"group": 7}
        elif v["ranking"] < max_ranking/10 * 9:
            node2group[k] = {"group": 8}
        else:
            node2group[k] = {"group": 9}
    return node2group

cwd = os.getcwd()

try:
    os.chdir("graph_attrs")
    with open("sfdp_graph.json", "r") as f:
        sfdp_graph = json.load(f)
    with open("dot_graph.json", "r") as f:
        dot_graph = json.load(f)

finally:
    os.chdir(cwd)

# networkxのグラフを作成
dot_G = nx.cytoscape_graph(dot_graph)
sfdp_G = nx.cytoscape_graph(sfdp_graph)

# 作成したグラフをもとに，pagerankを計算
dot_node2pagerank = nx.pagerank(dot_G, max_iter=1000)
sfdp_node2pagerank = nx.pagerank(sfdp_G, max_iter=1000)

# pagerankに順位付け
dot_node2ranking = rank_nodes_with_pagerank(dot_node2pagerank)
sfdp_node2ranking = rank_nodes_with_pagerank(sfdp_node2pagerank)

# pagerankの順位をもとにグループ分け
dot_node2group = grouping_for_ranking(dot_node2ranking)
sfdp_node2group = grouping_for_ranking(sfdp_node2ranking)

# pagerankの値を正規化して，属性値'pagerank'に登録
# dot_node_pagerank = min_max_normalization(dot_node2pagerank, 1.0, 210.0)
# sfdp_node_pagerank = min_max_normalization(sfdp_node2pagerank, 1.0, 210.0)
dot_node2pagerank = update_pagerank_for_set_node_attribute(dot_node2pagerank)
sfdp_node2pagerank = update_pagerank_for_set_node_attribute(sfdp_node2pagerank)


# pagerankの値，順位をグラフの属性値として定義する
nx.set_node_attributes(dot_G, dot_node2ranking)
nx.set_node_attributes(sfdp_G, sfdp_node2ranking)

nx.set_node_attributes(dot_G, dot_node2pagerank)
nx.set_node_attributes(sfdp_G, sfdp_node2pagerank)

nx.set_node_attributes(dot_G, dot_node2group)
nx.set_node_attributes(sfdp_G, sfdp_node2group)

# グラフの描画
nx.draw_networkx(dot_G)
nx.draw_networkx(sfdp_G)

dot_graph_json = nx.cytoscape_data(dot_G, attrs=None)
sfdp_graph_json = nx.cytoscape_data(sfdp_G, attrs=None)

try:
    os.chdir("graph_attrs")
    with open("dot_graph_pagerank.json", "w") as f:
        f.write(json.dumps(dot_graph_json, indent=4))
    with open("sfdp_graph_pagerank.json", "w") as f:
        f.write(json.dumps(sfdp_graph_json, indent=4))

finally:
    os.chdir(cwd)
    