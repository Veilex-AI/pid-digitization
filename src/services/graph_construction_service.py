from collections import deque
import networkx as nx
from networkx import Graph

from src.exceptions import EmptyLineOrSymbolError
from src.enums import GraphNodeType
from src.models import BoundingBox, Symbol
from src.utils import bounding_box_to_polygon

class GraphConstructionService:
    """
        A graph service responsible for graph management.
        Utilized to create, modify, prune the graph alongside other functionalities.
    """
    graph: Graph = None
    symbols: list[Symbol] = []
    line_segments: list[BoundingBox] = []

    def __init__(self, symbols: list[Symbol], line_segments: list[BoundingBox]):
        self.symbols = symbols
        self.line_segments = line_segments
        self.initialize_graph()

    def initialize_graph(self) -> None:
        '''
            initializes the graph with line and symbol nodes.

            symbols: list of sybols with label and bounding box
            lines: (startX, startY, endX, endY) line segments coordinate
        '''
        graph = nx.Graph()

        if(len(self.line_segments) == 0 or len(self.symbols) == 0):
            raise EmptyLineOrSymbolError()
        
        for line in self.line_segments:
            node_id = line.name
            graph.add_node(node_id, type=GraphNodeType.line)

        for symbol in self.symbols:
            node_id = symbol.name
            graph.add_node(node_id, type=GraphNodeType.symbol, label=symbol.label)

        self.graph = graph

    def get_line_cycle_list(self, degree=0):
        """
            gets all graph cycles.
        """
        line_nodes = self.get_line_nodes()
        cycles = list(nx.simple_cycles(self.graph))

        # finds cycles with n-degree (defined in the parameter)
        filtered_cycles = [cycle for cycle in cycles if all(node in line_nodes for node in cycle) and len(cycle) == degree]

        # gets only the unique results.
        unique_cycles = set(
            [ tuple(sorted(f)) for f in filtered_cycles ]
        )

        return [sorted(list(cycle)) for cycle in unique_cycles]

    def define_graph_edges(self):
        intersections = self.get_node_intersections()

        for key, values in intersections.items():
            for v in values:
                self.graph.add_edge(key, v)

        self.graph = self.graph.to_undirected()

    def reduce_line_cycles(self):
        """
            Remove all redundent line cycles.
        """
        line_cycles = self.find_3degree_cycles()

        for index, cycle in enumerate(line_cycles):
            node_id = f"p-{index}"
            self.graph.add_node(node_id, type=GraphNodeType.connector)
            
            # Connect the new node P to all nodes in the cycle
            for node in cycle:
                self.graph.add_edge(node_id, node)

            self.graph.remove_edges_from([(u,v) for u in cycle for v in cycle if u != v])

    # Don't use this function, this is buggy.
    def remove_unnecessary_lines(self):
        """
            buggy code.
        """
        # Iterate over all edges to check connections between 'symbol' nodes
        for u, v, data in list(self.graph.edges(data=True)):
            if self.graph.nodes[u].get('type') == GraphNodeType.symbol and self.graph.nodes[v].get('type') == GraphNodeType.symbol:
                # Find line nodes between the two symbol nodes
                line_nodes = [n for n in self.graph.neighbors(u) if self.graph.nodes[n].get('type') == GraphNodeType.line]
                line_nodes += [n for n in self.graph.neighbors(v) if self.graph.nodes[n].get('type') == GraphNodeType.line]
                
                # Remove redundant line nodes, keep only one
                if len(line_nodes) > 1:
                    for node in line_nodes[1:]:
                        self.graph.remove_edge(u, node)
                        self.graph.remove_edge(v, node)
                        self.graph.remove_node(node)
            
            # Remove isolated line nodes (only connected to one symbol)
            if self.graph.nodes[u].get('type') == GraphNodeType.line and len(list(self.graph.neighbors(u))) == 1:
                self.graph.remove_node(u)

            if self.graph.nodes[v].get('type') == GraphNodeType.line and len(list(self.graph.neighbors(v))) == 1:
                self.graph.remove_node(v)

    def remove_zero_or_single_connection_line_nodes(self):
        single_connection_nodes = [node for node, degree in self.graph.degree() if (degree == 1 or degree == 0) and self.graph.nodes[node]['type'] == GraphNodeType.line]
        self.graph.remove_nodes_from(single_connection_nodes)
    
    def get_node_intersections(self) -> dict[str, list[str]]:
        """
            figures out all possible interactions via polygon, creates a key-value pair if interaction exist.
        """
        nodes = [ *self.line_segments, *self.symbols ]
        intersection = {}

        for index, n1 in enumerate(nodes):
            for n2 in nodes[index + 1:]:
                if n1 != n2:
                    topX, topY, bottomX, bottomY = [*n1.pointSrc.get_dimensions(), *n1.pointDest.get_dimensions()]
                    n1Poly = bounding_box_to_polygon(topX, topY, bottomX, bottomY)

                    topX, topY, bottomX, bottomY = [*n2.pointSrc.get_dimensions(), *n2.pointDest.get_dimensions()]
                    n2Poly = bounding_box_to_polygon(topX, topY, bottomX, bottomY)

                    if(n1Poly.intersects(n2Poly)):
                        if(intersection.get(n1.name) is None):
                            intersection[n1.name] = []
                        intersection[n1.name].append(n2.name)
        
        return intersection
    
    def set_largest_graph_connected_nodes(self) -> None:
        connected_components = list(nx.connected_components(self.graph))
        largest_component = max(connected_components, key=len)
        self.graph = self.graph.subgraph(largest_component).copy()
    
    def line_node_to_edges(self):
        """
            any extra line nodes that are not required are removed from the graph.
            this function has a huge time complexity and thus is slow for large nodes.
        """
        symbol_and_connector_nodes = [node for node, data in self.graph.nodes(data=True) if data['type'] in [GraphNodeType.connector, GraphNodeType.symbol]]
        node_to_node_paths = []
        for u in symbol_and_connector_nodes:
            for v in symbol_and_connector_nodes:
                if u != v:
                    # push only those links to array that have symbols at boths ends.
                    for path in list(nx.all_simple_paths(self.graph, source=u, target=v)):
                        all_lines = path[1: -1]
                        if len(all_lines) > 1 and all(self.graph.nodes[l]['type'] == GraphNodeType.line for l in all_lines):
                            valid_path = True
                            for i in range(1, len(path) - 1):
                                neighbors = list(self.graph.neighbors(path[i]))
                                if not all(neighbor in [path[i-1], path[i+1]] for neighbor in neighbors):
                                    valid_path = False
                                    break
                            if valid_path:
                                node_to_node_paths.append(path)

        node_to_node_paths = self.uniqify_paths(self.graph, node_to_node_paths)

        for path in node_to_node_paths:
            last_node = path[len(path) - 1]
            first_line = path[1]
            self.graph.add_edge(first_line, last_node)

            for node in path[2:len(path) - 1]:
                if self.graph.has_node(node): self.graph.remove_node(node)

    def find_3degree_cycles(self):
        """
        Return a set of triangles (as sorted 3-tuples) in the undirected graph G.
        """
        G = self.graph
        triangles = set()
        for u in G:
            for v in G[u]:
                if u < v:
                    # Intersection of neighbors gives candidates for forming a triangle
                    common_neighbors = set(G[u]).intersection(G[v])
                    for w in common_neighbors:
                        # Ensure each triangle is added once by enforcing an ordering
                        if v < w:
                            triangles.add((u, v, w))
        return triangles

    def generate_graphml(self) -> str:
        graph_copy = self.graph.copy()
        for node in self.graph.nodes():
            if graph_copy.nodes[node]['type'] == GraphNodeType.connector:
                 graph_copy.nodes[node]['type'] = "connector"
            elif graph_copy.nodes[node]['type'] == GraphNodeType.line:
                graph_copy.nodes[node]['type'] = "line"
            elif graph_copy.nodes[node]['type'] == GraphNodeType.symbol:
                graph_copy.nodes[node]['type'] = "symbol"

        
        return '\n'.join(nx.generate_graphml(graph_copy))

    def find_valid_paths(self):
        G = self.graph
        node_types = nx.get_node_attributes(G, 'type')
        non_line_nodes = [n for n, t in node_types.items() if t in (GraphNodeType.symbol, GraphNodeType.connector)]
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
                    neighbor_type = node_types.get(neighbor, GraphNodeType.line)  
                    if neighbor_type == GraphNodeType.line:
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

    def prune_multiple_path_nodes(self, paths):
        G = self.graph
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

    def remove_connected_line_nodes(self):
        """
            delete node connection whose all nodes are of type line.
        """
        connections = list(nx.connected_components(self.graph))
        for connection in connections:
            if all([True if self.graph.nodes[item]['type'] == GraphNodeType.line else False for item in list(connection)]):
                self.graph.remove_nodes_from(connection)

    # PRIVATE FUNCTIONS
    def uniqify_paths(self, G, paths):
        unique_paths = []
        seen = []
        
        for path in paths:
            subgraph = G.subgraph(path)
            
            # Check if it is isomorphic to any previously seen subgraph
            if not any(nx.is_isomorphic(subgraph, G.subgraph(seen_path)) for seen_path in seen):
                seen.append(path)
                unique_paths.append(path)
        
        return unique_paths

    def get_line_nodes(self):
        return {node for node, data in self.graph.nodes(data=True) if data.get('type') == GraphNodeType.line}