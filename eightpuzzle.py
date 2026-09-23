"""
8-Puzzle solver using BFS and DFS.
Used for SLE-2 profiling exercise (02AML204).
"""
import time
from collections import deque

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# A solvable 8-puzzle start state (0 = blank)
START = (1, 2, 3,
         4, 0, 6,
         7, 5, 8)

def get_neighbors(state):
    """Return list of states reachable by sliding the blank tile."""
    neighbors = []
    idx = state.index(0)
    row, col = divmod(idx, 3)
    moves = []
    if row > 0: moves.append(-3)   # up
    if row < 2: moves.append(3)    # down
    if col > 0: moves.append(-1)   # left
    if col < 2: moves.append(1)    # right
    for m in moves:
        new_idx = idx + m
        new_state = list(state)
        new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
        neighbors.append(tuple(new_state))
    return neighbors


def bfs(start, goal):
    """Breadth-First Search — returns (path_length, nodes_expanded)."""
    frontier = deque([start])
    visited = {start}
    parent = {start: None}
    nodes_expanded = 0

    while frontier:
        state = frontier.popleft()
        nodes_expanded += 1
        if state == goal:
            path_len = 0
            s = state
            while parent[s] is not None:
                s = parent[s]
                path_len += 1
            return path_len, nodes_expanded
        for nb in get_neighbors(state):
            if nb not in visited:
                visited.add(nb)
                parent[nb] = state
                frontier.append(nb)
    return -1, nodes_expanded


def dfs(start, goal, depth_limit=30):
    """Depth-First Search (depth-limited to avoid infinite loops)
    — returns (path_length, nodes_expanded)."""
    stack = [(start, 0)]
    visited = {start}
    nodes_expanded = 0

    while stack:
        state, depth = stack.pop()
        nodes_expanded += 1
        if state == goal:
            return depth, nodes_expanded
        if depth >= depth_limit:
            continue
        for nb in get_neighbors(state):
            if nb not in visited:
                visited.add(nb)
                stack.append((nb, depth + 1))
    return -1, nodes_expanded


def run_algo(fn, start, goal, runs=5):
    """Run an algorithm several times, return timing stats + nodes."""
    times = []
    nodes = None
    path_len = None
    for _ in range(runs):
        t0 = time.perf_counter()
        path_len, nodes = fn(start, goal)
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000)  # ms
    return {
        "times_ms": times,
        "best_ms": min(times),
        "worst_ms": max(times),
        "avg_ms": sum(times) / len(times),
        "nodes_expanded": nodes,
        "path_length": path_len,
    }


if __name__ == "__main__":
    print("Start state:", START)
    print("Goal state :", GOAL)
    print()

    bfs_stats = run_algo(bfs, START, GOAL, runs=5)
    dfs_stats = run_algo(dfs, START, GOAL, runs=5)

    print("=== BFS ===")
    for k, v in bfs_stats.items():
        print(f"{k}: {v}")
    print()
    print("=== DFS ===")
    for k, v in dfs_stats.items():
        print(f"{k}: {v}")
