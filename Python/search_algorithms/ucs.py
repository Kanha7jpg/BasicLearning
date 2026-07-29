import heapq
from typing import Any, Dict, List, Set
from .graph import Graph

def ucs(graph: Graph, start: Any, goal: Any) -> Dict[str, Any]:
    """
    Uniform Cost Search (UCS) algorithm.
    Explores nodes based on the exact path cost g(n) from the start node.
    
    Returns a dictionary containing:
        - "path": List of nodes representing the path from start to goal.
        - "cost": Total path cost.
        - "expanded": List of nodes in the order they were expanded.
        - "success": Boolean indicating if the goal was reached.
    """
    counter = 0
    # Priority queue stores tuples of (path_cost_g, unique_counter, node, path_taken)
    pq = [(0.0, counter, start, [start])]
    
    explored: Set[Any] = set()
    expansion_order: List[Any] = []
    
    # Track the minimal path cost g(n) known to reach each node
    min_cost: Dict[Any, float] = {start: 0.0}
    
    while pq:
        g_val, _, node, path = heapq.heappop(pq)
        
        if node == goal:
            return {
                "path": path,
                "cost": g_val,
                "expanded": expansion_order,
                "success": True
            }
            
        if node not in explored:
            explored.add(node)
            expansion_order.append(node)
            
            for neighbor, edge_cost in graph.get_neighbors(node):
                new_cost = g_val + edge_cost
                if neighbor not in explored:
                    # If neighbor is not visited yet or we found a cheaper path to it
                    if neighbor not in min_cost or new_cost < min_cost[neighbor]:
                        min_cost[neighbor] = new_cost
                        counter += 1
                        heapq.heappush(pq, (new_cost, counter, neighbor, path + [neighbor]))
                        
    return {
        "path": [],
        "cost": 0.0,
        "expanded": expansion_order,
        "success": False
    }
