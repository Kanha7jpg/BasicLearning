import heapq
from typing import Any, Dict, List, Set
from .graph import Graph

def gbfs(graph: Graph, start: Any, goal: Any) -> Dict[str, Any]:
    """
    Greedy Best-First Search (GBFS) algorithm.
    Explores nodes based on the heuristic value h(n) of the estimated cost to the goal.
    
    Returns a dictionary containing:
        - "path": List of nodes representing the path from start to goal.
        - "cost": Total path cost.
        - "expanded": List of nodes in the order they were expanded.
        - "success": Boolean indicating if the goal was reached.
    """
    # Counter is used to break ties in the priority queue and avoid direct comparison of node objects
    counter = 0
    
    # Priority queue stores tuples of (h_value, unique_counter, node, path_taken, path_cost)
    start_h = graph.get_heuristic(start, goal)
    pq = [(start_h, counter, start, [start], 0.0)]
    
    explored: Set[Any] = set()
    expansion_order: List[Any] = []
    
    while pq:
        h_val, _, node, path, cost = heapq.heappop(pq)
        
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
            
            for neighbor, edge_cost in graph.get_neighbors(node):
                if neighbor not in explored:
                    counter += 1
                    neighbor_h = graph.get_heuristic(neighbor, goal)
                    heapq.heappush(
                        pq,
                        (neighbor_h, counter, neighbor, path + [neighbor], cost + edge_cost)
                    )
                    
    return {
        "path": [],
        "cost": 0.0,
        "expanded": expansion_order,
        "success": False
    }
