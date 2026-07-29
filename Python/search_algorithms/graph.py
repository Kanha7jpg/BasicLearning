from typing import Dict, List, Tuple, Any

class Graph:
    """
    A Graph class that represents a graph with weighted edges and heuristic values.
    Used for implementing various search algorithms.
    """
    def __init__(self):
        # Maps node -> list of (neighbor_node, edge_cost)
        self.adjacency_list: Dict[Any, List[Tuple[Any, float]]] = {}
        # Maps node -> {goal_node: heuristic_value}
        self.heuristics: Dict[Any, Dict[Any, float]] = {}

    def add_edge(self, u: Any, v: Any, cost: float = 1.0, bidirectional: bool = True) -> None:
        """
        Adds a weighted edge between node u and node v.
        """
        if u not in self.adjacency_list:
            self.adjacency_list[u] = []
        self.adjacency_list[u].append((v, cost))
        
        if bidirectional:
            if v not in self.adjacency_list:
                self.adjacency_list[v] = []
            self.adjacency_list[v].append((u, cost))

    def get_neighbors(self, node: Any) -> List[Tuple[Any, float]]:
        """
        Returns a list of (neighbor_node, cost) for a given node.
        """
        return self.adjacency_list.get(node, [])

    def set_heuristic(self, node: Any, goal: Any, value: float) -> None:
        """
        Sets the heuristic value from a node to a goal node.
        """
        if node not in self.heuristics:
            self.heuristics[node] = {}
        self.heuristics[node][goal] = value

    def get_heuristic(self, node: Any, goal: Any) -> float:
        """
        Returns the heuristic value from a node to a goal node.
        Defaults to 0.0 if not defined.
        """
        return self.heuristics.get(node, {}).get(goal, 0.0)


def get_romania_map() -> Graph:
    """
    Constructs and returns the classic Romania map graph from Russell & Norvig's
    'Artificial Intelligence: A Modern Approach'.
    """
    g = Graph()
    
    # Standard edges (cities and step costs)
    edges = [
        ("Arad", "Zerind", 75.0),
        ("Arad", "Sibiu", 140.0),
        ("Arad", "Timisoara", 118.0),
        ("Zerind", "Oradea", 71.0),
        ("Oradea", "Sibiu", 151.0),
        ("Timisoara", "Lugoj", 111.0),
        ("Lugoj", "Mehadia", 70.0),
        ("Mehadia", "Drobeta", 75.0),
        ("Drobeta", "Craiova", 120.0),
        ("Sibiu", "Fagaras", 99.0),
        ("Sibiu", "Rimnicu Vilcea", 80.0),
        ("Rimnicu Vilcea", "Craiova", 146.0),
        ("Rimnicu Vilcea", "Pitesti", 97.0),
        ("Craiova", "Pitesti", 138.0),
        ("Fagaras", "Bucharest", 211.0),
        ("Pitesti", "Bucharest", 101.0),
        ("Bucharest", "Giurgiu", 90.0),
        ("Bucharest", "Urziceni", 85.0),
        ("Urziceni", "Vaslui", 142.0),
        ("Vaslui", "Iasi", 92.0),
        ("Iasi", "Neamt", 87.0),
        ("Urziceni", "Hirsova", 98.0),
        ("Hirsova", "Eforie", 86.0)
    ]
    
    for u, v, cost in edges:
        g.add_edge(u, v, cost, bidirectional=True)
        
    # Straight-line distance heuristics to Bucharest
    heuristics_to_bucharest = {
        "Arad": 366.0,
        "Bucharest": 0.0,
        "Craiova": 160.0,
        "Drobeta": 242.0,
        "Eforie": 161.0,
        "Fagaras": 176.0,
        "Giurgiu": 77.0,
        "Hirsova": 151.0,
        "Iasi": 226.0,
        "Lugoj": 244.0,
        "Mehadia": 241.0,
        "Neamt": 234.0,
        "Oradea": 380.0,
        "Pitesti": 100.0,
        "Rimnicu Vilcea": 193.0,
        "Sibiu": 253.0,
        "Timisoara": 329.0,
        "Urziceni": 80.0,
        "Vaslui": 199.0,
        "Zerind": 374.0
    }
    
    for node, h_val in heuristics_to_bucharest.items():
        g.set_heuristic(node, "Bucharest", h_val)
        
    return g
