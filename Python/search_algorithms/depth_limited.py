from typing import Any, Dict, List, Set, Tuple
from .graph import Graph

def depth_limited_search(graph: Graph, start: Any, goal: Any, limit: int) -> Dict[str, Any]:
    """
    Depth-Limited Search (DLS) algorithm.
    A form of DFS with a specified limit on search depth.
    
    Returns a dictionary containing:
        - "path": List of nodes representing the path from start to goal.
        - "cost": Total path cost.
        - "expanded": List of nodes in the order they were expanded.
        - "status": "success", "cutoff" (reached limit), or "failure" (no path exists).
    """
    expansion_order: List[Any] = []
    
    # Recursive helper function
    def recursive_dls(node: Any, current_limit: int, visited: Set[Any], path: List[Any], cost: float) -> Tuple[str, List[Any], float]:
        expansion_order.append(node)
        
        if node == goal:
            return "success", path, cost
        
        if current_limit == 0:
            return "cutoff", [], 0.0
            
        cutoff_occurred = False
        
        for neighbor, edge_cost in graph.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                status, result_path, result_cost = recursive_dls(
                    neighbor,
                    current_limit - 1,
                    visited,
                    path + [neighbor],
                    cost + edge_cost
                )
                visited.remove(neighbor)
                
                if status == "success":
                    return "success", result_path, result_cost
                elif status == "cutoff":
                    cutoff_occurred = True
                    
        return "cutoff" if cutoff_occurred else "failure", [], 0.0

    visited_set = {start}
    status, final_path, final_cost = recursive_dls(start, limit, visited_set, [start], 0.0)
    
    return {
        "path": final_path,
        "cost": final_cost,
        "expanded": expansion_order,
        "status": status
    }
