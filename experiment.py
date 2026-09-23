"""
Full experiment for SLE-2:
Generates 3 puzzle instances of increasing difficulty (scramble depth)
to represent BEST CASE (easy/shallow), AVERAGE CASE (medium), and
WORST CASE (hard/deep) scenarios for BFS and DFS, and times each with
multiple repeats (timeit-style) for an average.
"""
import random
import time
import json
from eightpuzzle import bfs, dfs, get_neighbors, GOAL

random.seed(42)

def scramble(goal, moves):
    state = goal
    prev = None
    for _ in range(moves):
        nbs = get_neighbors(state)
        # avoid immediately undoing the previous move when possible
        choices = [n for n in nbs if n != prev] or nbs
        nxt = random.choice(choices)
        prev = state
        state = nxt
    return state

CASES = {
    "best_case (shallow scramble, 4 moves)": scramble(GOAL, 4),
    "average_case (medium scramble, 12 moves)": scramble(GOAL, 12),
    "worst_case (deep scramble, 22 moves)": scramble(GOAL, 22),
}

REPEATS = 5
results = {}

for label, start in CASES.items():
    results[label] = {"start_state": start}
    for name, fn in [("BFS", bfs), ("DFS", dfs)]:
        times = []
        nodes = None
        path_len = None
        for _ in range(REPEATS):
            t0 = time.perf_counter()
            path_len, nodes = fn(start, GOAL)
            t1 = time.perf_counter()
            times.append((t1 - t0) * 1000)
        results[label][name] = {
            "times_ms": [round(t, 4) for t in times],
            "avg_ms": round(sum(times) / len(times), 4),
            "min_ms": round(min(times), 4),
            "max_ms": round(max(times), 4),
            "nodes_expanded": nodes,
            "path_length": path_len,
        }

print(json.dumps(results, indent=2))
with open("results.json", "w") as f:
    json.dump(results, f, indent=2)
