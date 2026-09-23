# SLE2-IAI

# BFS vs DFS — 8-Puzzle Profiling Report

**PRN:** 25UAM116
**Name:** Madhur Pravin Bhandari
**Division:** B
**Date:** 21 September 2026

## Overview

This project profiles and compares two uninformed search algorithms — **Breadth-First Search (BFS)** and **depth-limited Depth-First Search (DFS, limit = 30)** — on the classic **8-Puzzle** (3×3 sliding tile puzzle).

## Algorithms Profiled

- **Algorithm A:** Breadth-First Search (BFS)
- **Algorithm B:** Depth-First Search (DFS), depth-limited to 30
- **Problem:** 8-Puzzle (3×3 sliding tile puzzle)

## Profiling Method

- **Tools:** [py-spy](https://github.com/benfred/py-spy) (sampling profiler / flame graph), Python's `time.perf_counter()` for precise per-run timing, and a manual node counter.
- `get_neighbors()` generates valid blank-tile moves; `bfs()` and `dfs()` both return `(path_length, nodes_expanded)` for an apples-to-apples comparison.
- The flame graph was captured by running the driver script under `py-spy record` at 100 samples/sec.
- Exact timings used `time.perf_counter()`, since py-spy's sampling isn't precise enough for very fast function calls.
- Each algorithm was timed on 3 puzzles of increasing difficulty (4, 12, and 22 moves from the goal) to capture best, average, and worst-case behavior.
- Nodes expanded = number of states popped off the frontier, counted directly inside each function.
- **Runs:** 5 runs per algorithm per test case → 15 runs total per algorithm.

## Results

### Summary Comparison

| Metric | BFS (Algorithm A) | DFS (Algorithm B) | Better? |
|---|---|---|---|
| Best-case time (ms) | 0.0364 | 13.02 | BFS |
| Average-case time (ms) | 18.54 | 30.80 | BFS |
| Worst-case time (ms) | 53.91 | 43.97 | DFS (case-dependent) |
| Nodes Expanded (avg. of 3 cases) | 10,892 | 30,247 | BFS |
| Solution optimal? (path length) | Yes (shortest) | No (hits depth limit) | BFS |

### Detailed Results by Test Case

| Test Case | Algo | Avg Time (ms) | Nodes Expanded | Path Length |
|---|---|---|---|---|
| Best case (4-move scramble) | BFS | 0.0364 | 24 | 4 |
| Best case (4-move scramble) | DFS | 43.97 | 42,235 | 4 |
| Average case (12-move scramble) | BFS | 1.664 | 1,128 | 12 |
| Average case (12-move scramble) | DFS | 35.42 | 34,661 | 30 |
| Worst case (22-move scramble) | BFS | 53.91 | 31,523 | 18 |
| Worst case (22-move scramble) | DFS | 13.02 | 13,846 | 30 |

## Justification & Analysis

Across all three test cases, BFS comes out ahead overall. It always finds the shortest path (4, 12, 18 moves — matching the actual scramble distance exactly), while DFS almost never does. In two of the three cases DFS returned a 30-move solution, because it commits to the depth limit along whichever branch it reaches first instead of searching level by level like BFS does.

This matches theory:
- **BFS** expands nodes level by level → **O(b^d)** time and space (b = branching factor, ~2–3 here; d = solution depth). Guaranteed complete and optimal for this problem.
- **DFS** is **O(b^m)**, where m is the depth limit (30). Its actual cost depends far more on neighbor-generation order than on how close the goal really is — which is why it chewed through 42,235 nodes on the "easy" puzzle.

The flame graph confirms this: almost all sampled time sits inside `dfs()` and `get_neighbors()`. BFS calls finish so fast (sub-millisecond to a couple of milliseconds) that a 100 Hz sampler barely catches them — itself evidence of how much cheaper BFS is here.

For larger problems (e.g., a 15-puzzle or much deeper scrambles), BFS would start to struggle due to memory (O(b^d) space) — it has to keep every visited state in memory. DFS wouldn't have that problem (O(m) memory) but its results would remain unreliable, and it would need a heuristic (turning it into A* or IDA*) to be useful at that scale.

## Conclusion

This exercise confirmed the textbook comparison of BFS and DFS, but seeing it in actual numbers made it click. BFS is optimal and, on this problem, generally cheaper when the solution isn't too deep, while plain DFS wastes a huge amount of effort exploring branches unrelated to the goal and usually returns a much longer solution than necessary. Using py-spy's flame graph made the cost difference visible directly, while manual timing and node counts backed it up with numbers.

**Bottom line:** picking the right algorithm matters far more than micro-optimizing the code. BFS beat unguided DFS by 1–3 orders of magnitude in nodes expanded, even on something as small as an 8-puzzle.



GitHub: https://github.com/madhur-184/IAI-SLE

See [`AI_CONTRIBUTION_LOG.md`](./AI_CONTRIBUTION_LOG.md) for a breakdown of AI-assisted vs. self-done work.
