from enum import Enum

class GraphNodeType(str, Enum):
    '''Enum for the graph node types'''
    unknown = 'unknown'
    line = 'line'
    symbol = 'symbol'
    text = 'text'  # Not used for creating the graph, just as a intermediate for candidate matching
    connector = 'connector'
