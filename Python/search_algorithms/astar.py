import heapq
from typing import Any, Dict, List, Set
from .graph import Graph

def astar(graph: Graph, start: Any, goal: Any) -> Dict[str, Any]:
    """
    A* Search Algorithm.
    
    Explores nodes based on the evaluation function:
        f(n) = g(n) + h(n)
    
    where:
        - g(n) is the exact cost of the path from the start node to node n.
        - h(n) is the heuristic estimate of the cost to reach the goal from node n.
        - f(n) is the total estimated cost of the cheapest solution through node n.
        
    Returns a dictionary containing:
        - "path": List of nodes representing the path from start to goal.
        - "cost": Total path cost (which is g(goal)).
        - "expanded": List of nodes in the order they were expanded.
        - "success": Boolean indicating if the goal was reached.
    """
    counter = 0
    
    # Calculate g(start) and h(start) to get f(start)
    g_start = 0.0
    h_start = graph.get_heuristic(start, goal)
    f_start = g_start + h_start
    
    # Priority queue stores tuples of (f_val, unique_counter, node, path_taken, g_val)
    # The queue is ordered by f_val. Tie-breaking is done using the unique_counter.
    pq = [(f_start, counter, start, [start], g_start)]
    
    explored: Set[Any] = set()
    expansion_order: List[Any] = []
    
    # Track the minimal path cost g(n) known to reach each node
    min_g: Dict[Any, float] = {start: g_start}
    
    while pq:
        f_val, _, node, path, g_val = heapq.heappop(pq)
        
        # Goal test when a node is popped/expanded
        if node == goal:
            return {
                "path": path,
                "cost": g_val,  # The final path cost is g(goal)
                "expanded": expansion_order,
                "success": True
            }
            
        if node not in explored:
            explored.add(node)
            expansion_order.append(node)
            
            for neighbor, edge_cost in graph.get_neighbors(node):
                # g(neighbor) = g(node) + cost(node -> neighbor)
                g_neighbor = g_val + edge_cost
                
                if neighbor not in explored:
                    # Check if neighbor is not visited yet or if we found a cheaper path to it
                    if neighbor not in min_g or g_neighbor < min_g[neighbor]:
                        min_g[neighbor] = g_neighbor
                        
                        # h(neighbor) = heuristic estimate from neighbor to goal
                        h_neighbor = graph.get_heuristic(neighbor, goal)
                        
                        # f(neighbor) = g(neighbor) + h(neighbor)
                        f_neighbor = g_neighbor + h_neighbor
                        
                        counter += 1
                        heapq.heappush(
                            pq,
                            (f_neighbor, counter, neighbor, path + [neighbor], g_neighbor)
                        )
                        
    return {
        "path": [],
        "cost": 0.0,
        "expanded": expansion_order,
        "success": False
    }
