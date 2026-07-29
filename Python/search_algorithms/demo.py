from .graph import get_romania_map
from .bfs import bfs
from .dfs import dfs
from .depth_limited import depth_limited_search
from .gbfs import gbfs
from .ucs import ucs
from .astar import astar

def main():
    # Load the Romania map
    romania = get_romania_map()
    start_city = "Arad"
    goal_city = "Bucharest"
    
    print("=" * 80)
    print(f"SEARCH ALGORITHMS COMPARISON: FROM {start_city.upper()} TO {goal_city.upper()}")
    print("=" * 80)
    
    # 1. BFS
    res_bfs = bfs(romania, start_city, goal_city)
    print("\n--- Breadth-First Search (BFS) ---")
    print(f"Success:      {res_bfs['success']}")
    print(f"Path:         {' -> '.join(res_bfs['path'])}")
    print(f"Cost:         {res_bfs['cost']}")
    print(f"Expanded:     {res_bfs['expanded']}")
    
    # 2. DFS
    res_dfs = dfs(romania, start_city, goal_city)
    print("\n--- Depth-First Search (DFS) ---")
    print(f"Success:      {res_dfs['success']}")
    print(f"Path:         {' -> '.join(res_dfs['path'])}")
    print(f"Cost:         {res_dfs['cost']}")
    print(f"Expanded:     {res_dfs['expanded']}")
    
    # 3. Depth-Limited Search (DLS)
    for limit in [2, 3]:
        res_dls = depth_limited_search(romania, start_city, goal_city, limit)
        print(f"\n--- Depth-Limited Search (DLS) [Limit={limit}] ---")
        print(f"Status:       {res_dls['status']}")
        if res_dls['path']:
            print(f"Path:         {' -> '.join(res_dls['path'])}")
            print(f"Cost:         {res_dls['cost']}")
        print(f"Expanded:     {res_dls['expanded']}")
        
    # 4. Greedy Best-First Search (GBFS)
    res_gbfs = gbfs(romania, start_city, goal_city)
    print("\n--- Greedy Best-First Search (GBFS) ---")
    print(f"Success:      {res_gbfs['success']}")
    print(f"Path:         {' -> '.join(res_gbfs['path'])}")
    print(f"Cost:         {res_gbfs['cost']}")
    print(f"Expanded:     {res_gbfs['expanded']}")
    
    # 5. Uniform Cost Search (UCS)
    res_ucs = ucs(romania, start_city, goal_city)
    print("\n--- Uniform Cost Search (UCS) ---")
    print(f"Success:      {res_ucs['success']}")
    print(f"Path:         {' -> '.join(res_ucs['path'])}")
    print(f"Cost:         {res_ucs['cost']}")
    print(f"Expanded:     {res_ucs['expanded']}")
    
    # 6. A* Search
    res_astar = astar(romania, start_city, goal_city)
    print("\n--- A* Search ---")
    print(f"Success:      {res_astar['success']}")
    print(f"Path:         {' -> '.join(res_astar['path'])}")
    print(f"Cost:         {res_astar['cost']}")
    print(f"Expanded:     {res_astar['expanded']}")
    
    print("\n" + "=" * 80)
    print("SUMMARY COMPARISON")
    print("=" * 80)
    print(f"{'Algorithm':<25} | {'Path Cost':<10} | {'Nodes Expanded':<15} | {'Optimal?'}")
    print("-" * 80)
    print(f"{'BFS':<25} | {res_bfs['cost']:<10} | {len(res_bfs['expanded']):<15} | {'No (shortest step-count)'}")
    print(f"{'DFS':<25} | {res_dfs['cost']:<10} | {len(res_dfs['expanded']):<15} | {'No'}")
    
    res_dls_3 = depth_limited_search(romania, start_city, goal_city, 3)
    print(f"{'DLS (Limit=3)':<25} | {res_dls_3['cost']:<10} | {len(res_dls_3['expanded']):<15} | {'No'}")
    print(f"{'GBFS':<25} | {res_gbfs['cost']:<10} | {len(res_gbfs['expanded']):<15} | {'No'}")
    print(f"{'UCS':<25} | {res_ucs['cost']:<10} | {len(res_ucs['expanded']):<15} | {'Yes'}")
    print(f"{'A*':<25} | {res_astar['cost']:<10} | {len(res_astar['expanded']):<15} | {'Yes'}")
    print("=" * 80)

if __name__ == '__main__':
    main()
