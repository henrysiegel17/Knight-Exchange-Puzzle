import random
from pprint import pprint

def randomized_grid_graph(n, m, p=0.7, holes=None):
    """
    Build a randomized grid graph with n rows and m columns.
    
    Parameters:
        n (int): number of rows
        m (int): number of columns
        p (float): probability (0-1) of including an edge between neighbors
        
    Returns:
        dict: adjacency list representation {(r,c): [(r2,c2), ...], ...}
    """
    G = {(r, c): [] for r in range(n) for c in range(m)}
    for r in range(n):
        for c in range(m):
            if holes and (r, c) in holes:
                del G[(r, c)]

    def add_edge(a, b):
        G[a].append(b)
        G[b].append(a)

    for r in range(n):
        for c in range(m):
            if holes and (r, c) in holes:
                continue
            # Try right neighbor
            if c + 1 < m and (r,c+1) in G and random.random() < p:
                add_edge((r, c), (r, c+1))

            # Try bottom neighbor
            if r + 1 < n and (r+1,c) in G and random.random() < p:
                add_edge((r, c), (r+1, c))
    
    return G

if __name__ == "__main__":
    print("hello world")
