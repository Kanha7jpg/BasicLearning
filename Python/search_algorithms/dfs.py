from typing import Any, Dict, List, Set
from .graph import Graph

def dfs(graph: Graph, start: Any, goal: Any) -> Dict[str, Any]:
    """
    Depth-First Search (DFS) algorithm.
    Explores the deepest nodes in the search tree first.
    
    Returns a dictionary containing:
        - "path": List of nodes representing the path from start to goal.
        - "cost": Total path cost.
        - "expanded": List of nodes in the order they were expanded.
        - "success": Boolean indicating if the goal was reached.
    """
    # Stack stores tuples of (current_node, path_taken, path_cost)
    stack = [(start, [start], 0.0)]
    explored: Set[Any] = set()
    expansion_order: List[Any] = []
    
    while stack:
        node, path, cost = stack.pop()
        
        if node == goal:
            return {
                "path": path,
                "cost": cost,
                "expanded": expansion_order,
                "success": True
            }
            
        if node not in explored:
            explored.add(node)
            expansion_order.append(node)
            
            # Reverse neighbors so the first declared neighbor is processed first (LIFO stack behavior)
            neighbors = graph.get_neighbors(node)
            for neighbor, edge_cost in reversed(neighbors):
                if neighbor not in explored:
                    stack.append((neighbor, path + [neighbor], cost + edge_cost))
                    
    return {
        "path": [],
        "cost": 0.0,
        "expanded": expansion_order,
        "success": False
    }
