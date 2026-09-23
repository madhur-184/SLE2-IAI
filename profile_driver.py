"""
Driver script used only for py-spy sampling.
Repeats BFS and DFS many times so the process runs long enough
for py-spy to attach and collect stack samples.
"""
from eightpuzzle import bfs, dfs, START, GOAL

ITERATIONS = 4000

if __name__ == "__main__":
    for _ in range(ITERATIONS):
        bfs(START, GOAL)
    for _ in range(ITERATIONS):
        dfs(START, GOAL)
    print("done")
