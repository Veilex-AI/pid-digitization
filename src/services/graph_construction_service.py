import networkx as nx
from networkx import Graph

from src.enums.graph_node_type import GraphNodeType
from src.models.bounding_box import BoundingBox
from src.models.symbol import Symbol

from src.utils.bounding_box_to_polygon import bounding_box_to_polygon


class GraphConstructionService:
    graph: Graph = None
    symbols: list[Symbol] = []
    line_segments: list[BoundingBox] = []

    def __init__(self, symbols: list[Symbol], line_segments: list[BoundingBox]):
        self.symbols = symbols
        self.line_segments = line_segments
        self.initialize_graph()

    def initialize_graph(self):
        '''
            symbols: list of sybols with label and bounding box
            lines: (startX, startY, endX, endY) line segments coordinate
        '''
        graph = nx.Graph()

        if(len(self.line_segments) == 0 or len(self.symbols) == 0):
            raise Exception("no symbols or line segments are defined.")
        
        for line in self.line_segments:
            node_id = line.name
            graph.add_node(node_id, type=GraphNodeType.line)

        for symbol in self.symbols:
            node_id = symbol.name
            graph.add_node(node_id, type=GraphNodeType.symbol)

        self.graph = graph

    def get_line_cycle_list(self):
        line_nodes = self.get_line_nodes()
        cycles = list(nx.simple_cycles(self.graph))

        filtered = [cycle if all(node in line_nodes for node in cycle) else None for cycle in cycles]

        return [x for x in filtered if x is not None]

    def define_graph_edges(self):
        intersections = self.get_node_intersections()

        for key, values in intersections.items():
            for v in values:
                self.graph.add_edge(key, v)

        self.graph = self.graph.to_undirected()

    
    def reduce_line_cycles(self):
        line_cycles = self.get_line_cycle_list()

        for index, cycle in enumerate(line_cycles):
            node_id = f"p-{index}"
            self.graph.add_node(node_id, type=GraphNodeType.connector)
            
            # Connect the new node P to all nodes in the cycle
            for node in cycle:
                self.graph.add_edge(node_id, node)
            
            # Remove the edges forming the cycle
            for i in range(len(cycle)):
                if self.graph.has_edge(cycle[i], cycle[(i + 1) % len(cycle)]):
                    self.graph.remove_edge(cycle[i], cycle[(i + 1) % len(cycle)])

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
    

    def get_node_intersections(self) -> dict[str, list[str]]:
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
    
    def set_largest_graph_connected_nodes(self):
        connected_components = list(nx.connected_components(self.graph))
        largest_component = max(connected_components, key=len)
        self.graph = self.graph.subgraph(largest_component).copy()
    
    def get_line_nodes(self):
        return {node for node, data in self.graph.nodes(data=True) if data.get('type') == GraphNodeType.line}