import sys
import json
import networkx as nx
import retrieve_dependency

class Node:
    def __init__(self, name, targets=None, sources=None, x=None, y=None, href=None, is_dummy=None):
        self.name = name
        self.targets = set() if targets is None else targets
        self.sources = set() if sources is None else sources
        self.x = -1 if x is None else x
        self.y = -1 if y is None else y
        self.href = "" if href is None else href
        self.is_dummy = False if is_dummy is None else is_dummy

    def __str__(self):
        return f"name: {self.name}, targets: {self.targets}, sources: {self.sources}, (x, y) = ({self.x}, {self.y})"

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

class Count:
    def __init__(self, func):
        self.count = 0
        self.func = func

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

    def reset(self):
        self.count = 0

def create_nodes(node2targets):
    nodes = []
    name2node = {}

    for k in node2targets.keys():
        n = Node(name=k)
        name2node[k] = n
        nodes.append(n)

    for n in nodes:
        n.href = f"http://mizar.org/version/current/html/{n.name.lower()}.html"

    for k, v in node2targets.items():
        for target in v:
            try:
                name2node[k].targets.add(name2node[target])
            except:
                print(target + " is None")

    for k, v in name2node.items():
        for target in v.targets:
            target.sources.add(name2node[k])

    return nodes

def remove_cycle(nodes):
    cycles = discover_cycle(nodes)
    if cycles:
        name2node = create_name2node(nodes)
        for cycle in cycles:
            name2node[cycle[0]].targets.remove(name2node[cycle[1]])
            name2node[cycle[1]].sources.remove(name2node[cycle[0]])
        return cycles
    else:
        return []

def discover_cycle(nodes):
    G = nx.DiGraph()
    create_dependency_graph(nodes, G)
    try:
        cycles = list(nx.find_cycle(G, orientation='original'))
    except nx.exception.NetworkXNoCycle:
        cycles = []
    return cycles

def create_name2node(nodes):
    name2node = {}
    for node in nodes:
        name2node[node.name] = node
    return name2node

def create_dependency_graph(nodes, G):
    for node in nodes:
        for target in node.targets:
            G.add_edge(node.name, target.name)

def assign_positions(nodes):
    for node in nodes:
        if not node.is_dummy:
            node.x, node.y = calculate_position(node)

def calculate_position(node):
    sources = list(node.sources)
    if not sources:
        return 0, 0

    min_x = min(source.x for source in sources)
    max_x = max(source.x for source in sources)
    min_y = min(source.y for source in sources)
    max_y = max(source.y for source in sources)

    x = (min_x + max_x) / 2
    y = max_y + 1

    return x, y

def assign_dummy_nodes(nodes):
    for node in nodes:
        if not node.sources:
            dummy_node = Node(name=f"dummy_{node.name}", targets={node}, is_dummy=True)
            node.sources.add(dummy_node)
            nodes.append(dummy_node)

def serialize_nodes(nodes):
    serialized_nodes = []
    for node in nodes:
        serialized_node = {
            "name": node.name,
            "x": node.x,
            "y": node.y,
            "href": node.href,
            "is_dummy": node.is_dummy
        }
        serialized_nodes.append(serialized_node)
    return serialized_nodes

def main():
    if len(sys.argv) != 2:
        print("Usage: python create_graph.py <path/to/dependencies.json>")
        return

    path = sys.argv[1]
    with open(path) as f:
        data = json.load(f)
        node2targets = retrieve_dependency.get_node2targets(data)
        nodes = create_nodes(node2targets)

        remove_cycle(nodes)
        assign_dummy_nodes(nodes)
        assign_positions(nodes)

        serialized_nodes = serialize_nodes(nodes)
        with open("graph.json", "w") as output:
            json.dump(serialized_nodes, output, indent=2)

if __name__ == "__main__":
    main()