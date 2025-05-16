import networkx as nx
from collections import deque


def prune_multiple_path_nodes(G, paths):
    nodes_to_remove = set()
    remaining_nodes_set = set()

    for path in paths:
        if(len(path) <= 2):
            continue
        to_remove_nodes = []
        remaining_nodes = []

        for i in range(1, len(path) - 1):
            node = path[i]
            if(len(G[node]) > 2):
                remaining_nodes.append(node)
            else:
                to_remove_nodes.append(node)

        if(len(remaining_nodes) == 0):
            remaining_nodes.append(to_remove_nodes.pop())

        nodes_to_remove.update(to_remove_nodes)
        remaining_nodes_set.update(remaining_nodes)

    for node in nodes_to_remove:
        if node not in remaining_nodes_set:
            neighbors = list(G.neighbors(node))
            if len(neighbors) == 2:
                G.add_edge(neighbors[0], neighbors[1])
            G.remove_node(node)


def find_valid_paths(G):
    node_types = nx.get_node_attributes(G, 'type')
    non_line_nodes = [n for n, t in node_types.items() if t in ('symbol', 'connector')]
    valid_paths = []    
    
    for start in non_line_nodes:
        queue = deque()
        queue.append((start, [start], 0))
        while queue:
            current, path, line_count = queue.popleft()
            
            for neighbor in G.neighbors(current):
                if neighbor in path:
                    continue
                
                # Default to line if not specified
                neighbor_type = node_types.get(neighbor, 'line')  
                if neighbor_type == 'line':
                    new_path = path + [neighbor]
                    new_line_count = line_count + 1
                    queue.append((neighbor, new_path, new_line_count))
                else:
                    if line_count >= 2 and neighbor != start:
                        valid_path = path + [neighbor]
                        valid_paths.append(valid_path)

    unique_paths_set = set()
    unique_paths_arr = []

    for row in valid_paths:
        pair = frozenset([row[0], row[-1]])

        if pair not in unique_paths_set:
            unique_paths_set.add(pair)
            unique_paths_arr.append(row)

    return unique_paths_arr

graph_ml = '<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n  <key id="d1" for="node" attr.name="label" attr.type="string" />\n  <key id="d0" for="node" attr.name="type" attr.type="string" />\n  <graph edgedefault="undirected">\n    <node id="l-0">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-1">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-2">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-3">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-4">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-5">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-6">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-7">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-8">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-9">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-10">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-11">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-12">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-13">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-14">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-15">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-16">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-17">\n      <data key="d0">line</data>\n    </node>\n    <node id="l-18">\n      <data key="d0">line</data>\n    </node>\n    <node id="s-0">\n      <data key="d0">symbol</data>\n      <data key="d1">14</data>\n    </node>\n    <node id="s-1">\n      <data key="d0">symbol</data>\n      <data key="d1">14</data>\n    </node>\n    <node id="s-2">\n      <data key="d0">symbol</data>\n      <data key="d1">4</data>\n    </node>\n    <node id="s-3">\n      <data key="d0">symbol</data>\n      <data key="d1">11</data>\n    </node>\n    <node id="s-4">\n      <data key="d0">symbol</data>\n      <data key="d1">23</data>\n    </node>\n    <node id="s-5">\n      <data key="d0">symbol</data>\n      <data key="d1">24</data>\n    </node>\n    <node id="s-6">\n      <data key="d0">symbol</data>\n      <data key="d1">21</data>\n    </node>\n    <node id="s-7">\n      <data key="d0">symbol</data>\n      <data key="d1">21</data>\n    </node>\n    <node id="p-0">\n      <data key="d0">connector</data>\n    </node>\n    <node id="p-1">\n      <data key="d0">connector</data>\n    </node>\n    <edge source="l-0" target="l-1" />\n    <edge source="l-0" target="l-14" />\n    <edge source="l-0" target="s-4" />\n    <edge source="l-0" target="p-0" />\n    <edge source="l-1" target="s-6" />\n    <edge source="l-2" target="l-5" />\n    <edge source="l-2" target="s-0" />\n    <edge source="l-3" target="l-4" />\n    <edge source="l-3" target="s-2" />\n    <edge source="l-4" target="s-3" />\n    <edge source="l-5" target="l-12" />\n    <edge source="l-6" target="l-11" />\n    <edge source="l-6" target="s-5" />\n    <edge source="l-6" target="p-1" />\n    <edge source="l-7" target="l-10" />\n    <edge source="l-7" target="s-7" />\n    <edge source="l-8" target="p-0" />\n    <edge source="l-8" target="p-1" />\n    <edge source="l-9" target="l-15" />\n    <edge source="l-9" target="l-17" />\n    <edge source="l-10" target="s-4" />\n    <edge source="l-11" target="s-0" />\n    <edge source="l-12" target="s-1" />\n    <edge source="l-13" target="s-3" />\n    <edge source="l-14" target="s-1" />\n    <edge source="l-15" target="p-0" />\n    <edge source="l-16" target="s-5" />\n    <edge source="l-17" target="s-2" />\n    <edge source="l-18" target="p-1" />\n  </graph>\n</graphml>'

graph = nx.parse_graphml(graph_ml)

print(graph)

paths = find_valid_paths(graph)

print(paths)

# prune_multiple_path_nodes(graph, paths)

# print(graph)