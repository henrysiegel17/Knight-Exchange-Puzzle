# Hamiltonian-path solver for your 9x9-with-4-extras knights graph.
# Paste your adjacency dictionary into `graph` (or read from a file).
# Adjust TIMEOUT_SECS, MAX_DFS_SECONDS, RANDOM_TRIES as needed.

from print_path import display_path
from Utils.utlities import transpose_graph, transpose_path
import time, random, collections, sys
sys.setrecursionlimit(10000)

# --- Paste your graph here (exactly as you provided) ---
graph = {(1, 0): [(3, 1), (2, 2)],
 (1, 1): [(3, 2), (2, 3)],
 (1, 2): [(3, 3), (2, 4), (3, 1)],
 (1, 3): [(3, 4), (2, 5), (2, 1), (3, 2)],
 (1, 4): [(3, 5), (2, 6), (2, 2), (3, 3)],
 (1, 5): [(3, 6), (2, 7), (2, 3), (3, 4)],
 (2, 1): [(4, 2), (3, 3), (1, 3)],
 (2, 2): [(4, 3), (3, 4), (1, 4), (1, 0), (4, 1)],
 (2, 3): [(4, 4), (3, 5), (1, 5), (1, 1), (3, 1), (4, 2)],
 (2, 4): [(4, 5), (3, 6), (1, 2), (3, 2), (4, 3)],
 (2, 5): [(4, 6), (3, 7), (1, 3), (3, 3), (4, 4)],
 (2, 6): [(4, 7), (1, 4), (3, 4), (4, 5)],
 (2, 7): [(1, 5), (3, 5), (4, 6)],
 (3, 1): [(5, 2), (4, 3), (2, 3), (1, 2), (1, 0)],
 (3, 2): [(5, 3), (4, 4), (2, 4), (1, 3), (1, 1), (5, 1)],
 (3, 3): [(5, 4), (4, 5), (2, 5), (1, 4), (1, 2), (2, 1), (4, 1), (5, 2)],
 (3, 4): [(5, 5), (4, 6), (2, 6), (1, 5), (1, 3), (2, 2), (4, 2), (5, 3)],
 (3, 5): [(5, 6), (4, 7), (2, 7), (1, 4), (2, 3), (4, 3), (5, 4)],
 (3, 6): [(5, 7), (1, 5), (2, 4), (4, 4), (5, 5)],
 (3, 7): [(2, 5), (4, 5), (5, 6)],
 (4, 1): [(6, 2), (5, 3), (3, 3), (2, 2)],
 (4, 2): [(6, 3), (5, 4), (3, 4), (2, 3), (2, 1), (6, 1)],
 (4, 3): [(6, 4), (5, 5), (3, 5), (2, 4), (2, 2), (3, 1), (5, 1), (6, 2)],
 (4, 4): [(6, 5), (5, 6), (3, 6), (2, 5), (2, 3), (3, 2), (5, 2), (6, 3)],
 (4, 5): [(6, 6), (5, 7), (3, 7), (2, 6), (2, 4), (3, 3), (5, 3), (6, 4)],
 (4, 6): [(2, 7), (2, 5), (3, 4), (5, 4), (6, 5)],
 (4, 7): [(2, 6), (3, 5), (5, 5), (6, 6)],
 (5, 1): [(7, 2), (6, 3), (4, 3), (3, 2)],
 (5, 2): [(7, 3), (6, 4), (4, 4), (3, 3), (3, 1)],
 (5, 3): [(7, 4), (6, 5), (4, 5), (3, 4), (3, 2), (4, 1), (6, 1), (7, 2)],
 (5, 4): [(7, 5), (6, 6), (4, 6), (3, 5), (3, 3), (4, 2), (6, 2), (7, 3)],
 (5, 5): [(7, 6), (4, 7), (3, 6), (3, 4), (4, 3), (6, 3), (7, 4)],
 (5, 6): [(3, 7), (3, 5), (4, 4), (6, 4), (7, 5)],
 (5, 7): [(3, 6), (4, 5), (6, 5), (7, 6)],
 (6, 1): [(7, 3), (5, 3), (4, 2)],
 (6, 2): [(7, 4), (5, 4), (4, 3), (4, 1)],
 (6, 3): [(7, 5), (5, 5), (4, 4), (4, 2), (5, 1)],
 (6, 4): [(7, 6), (5, 6), (4, 5), (4, 3), (5, 2), (7, 2)],
 (6, 5): [(5, 7), (4, 6), (4, 4), (5, 3), (7, 3)],
 (6, 6): [(4, 7), (4, 5), (5, 4), (7, 4)],
 (7, 2): [(6, 4), (5, 3), (5, 1)],
 (7, 3): [(6, 5), (5, 4), (5, 2), (6, 1)],
 (7, 4): [(6, 6), (5, 5), (5, 3), (6, 2)],
 (7, 5): [(5, 6), (5, 4), (6, 3)],
 (7, 6): [(5, 7), (5, 5), (6, 4)]}
for u, nbrs in list(graph.items()):
    for v in nbrs:
        if v not in graph:
            graph[v] = []
for u in list(graph.keys()):
    for v in graph[u]:
        if u not in graph[v]:
            graph[v].append(u)

start = (2,1)
end = (7,2)
nodes = list(graph.keys())
N = len(nodes)
print("Nodes:", N)

# adjacency lists for speed
adj = {u: list(graph[u]) for u in graph}

# Parameters you can tweak:
TIMEOUT_SECS = 300         # total runtime cap (seconds)
MAX_DFS_SECONDS = 10      # cap for the deeper DFS phase
RANDOM_TRIES = 2000        # number of randomized greedy attempts (fast)
VERBOSE = True

# --- Utilities and heuristics ---
def greedy_warnsdorff_randomized(seed_none=False):
    """One randomized greedy Warnsdorff attempt (fast)."""
    if not seed_none:
        random.seed()
    visited = {start}
    path = [start]
    u = start
    for step in range(N-1):
        nbrs = [v for v in adj[u] if v not in visited]
        # don't go to end early
        nbrs = [v for v in nbrs if not (v == end and step < N-2)]
        if not nbrs:
            break
        # key: (onward moves, random tie) -> pick smallest
        keys = []
        for x in nbrs:
            onward = sum(1 for w in adj[x] if w not in visited and w != end)
            keys.append((onward, random.random(), x))
        keys.sort()
        u = keys[0][2]
        path.append(u); visited.add(u)
    return path

# strong pruning checks used in DFS
def has_isolated_vertex(unvisited, curr):
    for v in unvisited:
        # count neighbors inside unvisited or curr (curr connects into remaining graph)
        cnt = 0
        for w in adj[v]:
            if w in unvisited or w == curr:
                cnt += 1
                break
        if cnt == 0:
            return True
    return False

def is_connected_unvisited(unvisited):
    if not unvisited:
        return True
    from collections import deque
    s = next(iter(unvisited))
    q = deque([s]); seen = {s}
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v in unvisited and v not in seen:
                seen.add(v); q.append(v)
    return len(seen) == len(unvisited)

# DFS with pruning and ordering
def dfs_with_pruning(start_time_limit):
    start_time_local = time.time()
    unvisited_init = set(nodes); unvisited_init.remove(start)
    path = [start]
    visited = {start}
    found = [False]
    result_path = [None]
    calls = 0

    def order_neighbors(u, unvisited):
        nbrs = [v for v in adj[u] if v in unvisited]
        # avoid end too early
        if end in nbrs and len(unvisited) > 1:
            nbrs.remove(end)
        # sort by onward-degree (fewest first) to reduce branching
        nbrs.sort(key=lambda x: sum(1 for w in adj[x] if w in unvisited and w != end))
        return nbrs

    def dfs(u, unvisited):
        nonlocal calls, start_time_local
        calls += 1
        if time.time() - start_time_local > start_time_limit:
            return False
        if not unvisited:
            if u == end:
                result_path[0] = list(path); found[0] = True; return True
            return False
        # pruning: isolated vertices
        if has_isolated_vertex(unvisited, u):
            return False
        # pruning: connectivity of unvisited
        if not is_connected_unvisited(unvisited):
            return False
        nbrs = order_neighbors(u, unvisited)
        for v in nbrs:
            # push
            unvisited.remove(v); path.append(v)
            if dfs(v, unvisited):
                return True
            # pop
            path.pop(); unvisited.add(v)
        return False

    dfs(start, unvisited_init)
    return found[0], result_path[0], calls

# --- MAIN: quick randomized tries, then deep DFS attempt ---
t0 = time.time()
best_path = None
best_len = 0

found = False
# Fast randomized phase
for i in range(RANDOM_TRIES):
    p = greedy_warnsdorff_randomized()
    L = len(p)
    if L > best_len:
        best_len = L; best_path = p[:]
    if L == N and p[-1] == end:
        print("Found Hamiltonian via greedy on try", i)
        print(p)
        found = True
        break
if VERBOSE:
    print("Randomized greedy best length:", best_len, "after", RANDOM_TRIES, "tries. Time spent:", time.time()-t0)

# If greedy didn't find a Hamiltonian, try DFS with pruning for up to MAX_DFS_SECONDS
remaining_time = 0
if found == False:
    remaining_time = min(MAX_DFS_SECONDS, TIMEOUT_SECS - (time.time() - t0))
    if remaining_time <= 0:
        print("Time budget exhausted after randomized phase.")
        print("Best length found:", best_len)
        sys.exit(0)
    print("Starting deeper DFS with pruning (time budget seconds):", remaining_time)
    found, path_res, calls = dfs_with_pruning(start_time_limit=remaining_time)
    print("DFS finished. Found:", found, "Calls:", calls, "Elapsed:", time.time()-t0)
    if found:
        print("Hamiltonian path from", start, "to", end, "found! Length:", len(path_res))
        print(path_res)
    else:
        print("No Hamiltonian path found within time budget.")
        print("Best greedy length:", best_len)
        if best_path:
            print("Example best path (length {}):".format(best_len))
            print(best_path)

display_path(best_path, graph, show_axes=False, show_title=False)

