from collections import deque
from typing import Any, Dict, List, Set
from .graph import Graph

def bfs(graph: Graph, start: Any, goal: Any) -> Dict[str, Any]:
    """
    Breadth-First Search (BFS) algorithm.
    Explores the shallowest nodes in the search tree first.
    
    Returns a dictionary containing:
        - "path": List of nodes representing the path from start to goal.
        - "cost": Total path cost.
        - "expanded": List of nodes in the order they were expanded.
        - "success": Boolean indicating if the goal was reached.
    """
    if start == goal:
        return {
            "path": [start],
            "cost": 0.0,
            "expanded": [],
            "success": True
        }
        
    # Queue stores tuples of (current_node, path_taken, path_cost)
    queue = deque([(start, [start], 0.0)])
    explored: Set[Any] = set()
    expansion_order: List[Any] = []
    
    # Track frontier set to avoid duplicate additions to the queue
    frontier_set: Set[Any] = {start}
    
    while queue:
        node, path, cost = queue.popleft()
        
        expansion_order.append(node)
        explored.add(node)
        
        for neighbor, edge_cost in graph.get_neighbors(node):
            if neighbor not in explored and neighbor not in frontier_set:
                new_path = path + [neighbor]
                new_cost = cost + edge_cost
                
                # Goal test on node generation (standard BFS optimization)
                if neighbor == goal:
                    return {
                        "path": new_path,
                        "cost": new_cost,
                        "expanded": expansion_order,
                        "success": True
                    }
                    
                frontier_set.add(neighbor)
                queue.append((neighbor, new_path, new_cost))
                
    return {
        "path": [],
        "cost": 0.0,
        "expanded": expansion_order,
        "success": False
    }
