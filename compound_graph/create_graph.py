import sys
import json
import networkx as nx
import retrieve_dependency

class Node:
    """
    ノードをクラスとして定義する．

    Attributes:
        name: ノードの名前．str()．
        targets: 自身が指しているノードの集合．set()．デフォルトは空集合set()．
        sources: 自身を指しているノードの集合．set()．デフォルトは空集合set()．
        x, y: ノードの座標(x,y)．ともにint()．デフォルトは-1．
        href: ノードのリンク．str()．デフォルトは空列 ""．
        is_dummy: ノードがダミーか否か．bool()．デフォルトはFalse．
    """

    def __init__(self, name, targets=None, sources=None,
                 x=None, y=None, href=None, is_dummy=None):
        self.name = name
        self.targets = set() if targets is None else targets
        self.sources = set() if sources is None else sources
        self.x = -1 if x is None else x
        self.y = -1 if y is None else y
        self.href = "" if href is None else href
        self.is_dummy = False if is_dummy is None else is_dummy

    def __str__(self):
        name = self.name
        targets = self.targets
        sources = self.sources
        x = self.x
        y = self.y
        return f"name: {name}, targets: {targets},\
               sources: {sources}, (x, y)= ({x}, {y})"


class Stack:
    """
    スタック構造のクラス．

    Attributes:
        items: スタックの内容．list．
    """

    def __init__(self):
        self.items = []

    def is_empty(self):
        """スタック内が空かどうか調べる"""
        return self.items == []

    def push(self, item):
        """スタックに値をプッシュする"""
        self.items.append(item)

    def pop(self):
        """スタックの内容をポップする"""
        return self.items.pop()


class Count:
    """
    関数が何度呼ばれたかをカウントするクラス．

    Attributes:
        count: 関数funcを読んだ回数．int．
        func: 関数オブジェクト．
    """

    def __init__(self, func):
        self.count = 0
        self.func = func

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

    def reset(self):
        """カウンタをリセットする"""
        self.count = 0


def create_nodes(node2targets):
    """
    node2targetsをNodeクラスでインスタンス化したものをリストにまとめる．
    各属性には次の物を格納する．
        - name:    node2targetsのkey．
        - targets: node2targetsのvalue．set[str]．
        - sources: node2targetsのnodeのソースノードの集合．set[str]．
        - x, y:    -1．
        - href:    (ノード名).html．ただし，ノード名は小文字．
        - is_dummy: False
    Args:
        node2targets: key:ノード名，value:keyのノードのターゲットノードの集合
    Returns:
        インスタンス化されたノードのlist.
    """
    nodes = []
    name2node = {}
    # nodes, name2nodeの作成
    # k: ノードの名前(str)
    for k in node2targets.keys():
        n = Node(name=k)
        name2node[k] = n
        nodes.append(n)

    # リンクの作成
    for n in nodes:
        n.href = n.name.lower() + '.html'

    # targetsの作成
    # k: ノードの名前(str)、v: ノードkのターゲットノードのset[str]
    for k, v in node2targets.items():
        for target in v:
            name2node[k].targets.add(name2node[target])

    # sourcesの作成
    # k: ノードの名前、v: ノードkのNodeオブジェクト
    for k, v in name2node.items():
        for target in v.targets:
            target.sources.add(name2node[k])
    return nodes


"""
循環除去
"""
def remove_cycle(nodes):
    cycles = discover_cycle(nodes)
    if cycles:
        name2node = create_name2node(nodes)
        for cycle in cycles:
            name2node[cycle[0]].targets.remove(name2node[cycle[1]])
            name2node[cycle[1]].sources.remove(name2node[cycle[0]])
        return cycles
    else:
        return list()


def discover_cycle(nodes):
    G = nx.DiGraph()
    create_dependency_graph(nodes, G)
    try:
        cycles = list(nx.find_cycle(G, orientation='original'))
    except nx.exception.NetworkXNoCycle:
        cycles = list()
    return cycles


def create_name2node(nodes):
    name2node = dict()
    for node in nodes:
        name2node[node.name] = node
    return name2node


def restore_removed_cycles(nodes, cycles):
    name2node = create_name2node(nodes)
    for cycle in cycles:
        name2node[cycle[0]].targets.add(name2node[cycle[1]])
        name2node[cycle[1]].sources.add(name2node[cycle[0]])
        

"""
間引き
"""


def remove_redundant_dependency(nodes):
    """
    エッジ(依存関係)の間引きを行う．
    各ノードのターゲットから、間引いてよいターゲットを見つけ、間引く．
    Args:
        nodes: 間引きを行いたいノード(1個以上)
    Return:
    """
    node2ancestors = dict()  # key=node, value=keyの全祖先
    for node in nodes:
        make_node2ancestors_recursively(node, node2ancestors)

    for node in nodes:
        removable_dependency_list = \
            search_removable_dependency(node, node2ancestors)
        for source, target in removable_dependency_list:
            source.targets.remove(target)
            target.sources.remove(source)


def make_node2ancestors_recursively(node, node2ancestors):
    """
    key=node, value=keyの全祖先のノードのセット
    となる辞書を作る．
    Args:
        node: 全祖先を知りたいノード
        node2ancestors: key=ノード, value=keyの全祖先のセット
    Return:
        nodeにターゲットが存在しない：要素がnodeのみのセット
        nodeがnode2ancestors.keys()に存在する:node2ancestors[node]
        それ以外：nodeの全祖先のノードのセット
    """
    if node in node2ancestors:
        return node2ancestors[node]

    if not node.targets:
        node2ancestors[node] = set()
        return {node}

    ancestors = set()
    for target in node.targets:
        ancestors |= {target}
        ancestors |= make_node2ancestors_recursively(target, node2ancestors)
    node2ancestors[node] = ancestors
    return ancestors


def search_removable_dependency(node, node2ancestors):
    """
    取り除いてもよいエッジ(依存関係)を見つける．
    Args:
        node: 間引きたいノード(ソース側)．
        node2ancestors: key=nodeのtarget, value=keyの全祖先のノードのセット の辞書．
    Return:
        removable_dependency_list: 間引いてよいエッジ(source, target)のリスト．
                                source,targetはともにNodeオブジェクト．
    """
    removable_dependency_list = list()
    all_target_ancestors = set()
    for target in node.targets:
        all_target_ancestors |= node2ancestors[target]
    for target in node.targets:
        if target in all_target_ancestors:
            removable_dependency_list.append((node, target))
    return removable_dependency_list


"""
階層グラフ(graphviz dot style)
"""


def assgin_dot_coordinate(nodes):
    """
    graphvizのdotレイアウトを適用したときの座標を返す
    """
    G = nx.DiGraph(nodes_to_node2targets(nodes))
    pos = nx.nx_pydot.pydot_layout(G, prog="dot")
    for n in nodes:
        n.x = pos[n.name][0] * 0.02
        n.y = pos[n.name][1] * 0.02


def nodes_to_node2targets(nodes):
    node2targets = dict()
    for n in nodes:
        node2targets[n.name] = list()
        for t in n.targets:
            node2targets[n.name].append(t.name)
    return node2targets


"""
仕上げ
"""


def node_list2node_dict(node_list):
    """
    ノードについての情報（属性）をリスト形式から辞書形式に変換する．
    Args:
        node_list:全ノードをNodeクラスでまとめたリスト．
    Return:
        各ノードのname, href, x, y, is_dummyを持つ辞書．
        キーはnameで、その値としてhref, x, y, is_dummyをキーに持つ辞書が与えられる．
        例:
        node_dict = \
            {"f": { "href": "example.html", "x": 0, "y": 2,
             "is_dummy": false}, ... }
    """
    node_dict = {}
    for node in node_list:
        node_dict[node.name] = {
            "href": node.href,
            "x": node.x,
            "y": node.y,
            "is_dummy": node.is_dummy
        }
    return node_dict


def create_dependency_graph(node_list, graph):
    """
    依存関係を示すグラフを作成する．
    Args:
        node_list:全ノードをNodeクラスでまとめたリスト．
        graph:操作する有向グラフ．networkx.DiGraph()
    Return:
    """
    for source in node_list:
        graph.add_node(source.name)
        for target in source.targets:
            graph.add_node(target.name)
            graph.add_edge(source.name, target.name)


def format_output_graph_file(nodes):
    graph = list()
    for n in nodes:
        node = dict()
        node["group"] = "nodes"
        node["data"] = {"id": n.name, "name": n.name, "href": n.href}
        node["position"] = {"x": n.x * 300, "y": n.y * 300}
        graph.append(node)

    for node in nodes:
        for target in node.targets:
            edge = dict()
            edge["group"] = "edges"
            edge["data"] = {"source": node.name, "target": target.name}
            graph.append(edge)

    ele_object = {"eleObjs": graph}

    return ele_object

def create_graph(node2targets, output_json_file):
    """
    依存関係を示すグラフを作る．
    Args:
        node2targets: valueがkeyのtargetsとなる辞書.
        output_json_file: 出力ファイル名．末尾に'.json'を記述．
    Return:
    """
    nodes = create_nodes(node2targets)

    # 閉路除去
    cycles = remove_cycle(nodes)
    # 間引き
    sys.setrecursionlimit(1000)
    remove_redundant_dependency(nodes)

    if cycles:
        restore_removed_cycles(nodes, cycles)

    # レイアウト
    assgin_dot_coordinate(nodes)

    node_attributes = node_list2node_dict(nodes)

    graph = format_output_graph_file(nodes)

    with open('graph_attrs/' + output_json_file, 'w') as f:
        f.write(json.dumps(graph, indent=4))


if __name__ == '__main__':
    article2ref_articles = retrieve_dependency.make_miz_dependency()
    create_graph(article2ref_articles, "compound_dot_graph.json")