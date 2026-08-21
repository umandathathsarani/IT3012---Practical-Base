# IT3012 - Intelligent Agents - Lab Practical 03

## Overview
This branch contains the completed tasks for **Practical 03: Uninformed Search**.
We transition to a **Goal-Based/Planning Agent** that uses Breadth-First Search (BFS), Depth-First Search (DFS), and Uniform-Cost Search (UCS) to plan an optimal path to the food before taking action.

## Modifications Made
- **Exposing the World Model**: We modified `get_percept` to provide the global state (`grid_size`, `walls`, `all_food`, `agent_pos`) so the agent is no longer "blind" and can simulate future states.
- **Implementing Search Algorithms**: We implemented the `SearchAgent` with `bfs_search`, `dfs_search`, and `ucs_search` algorithms utilizing `deque` and `heapq` structures.
- **Offline Planning**: The agent now formulates a complete `self.plan` before making its first move, popping actions off the list step-by-step.

---

## Part 2: Theoretical Evaluation Answers

### Question 1
> **What is the fundamental difference between the "State Space" and the "Search Tree"?**

**Answer:**
- **State Space:** The physical or mathematical layout of the environment (the grid itself, with its coordinates, walls, and food). It is finite in this game. 
- **Search Tree:** The data structure generated in memory by the search algorithm as it explores paths. Even if the state space is small, the search tree can become infinitely large if the agent loops back and forth between the same states without a `reached` set.

### Question 2
> **In graph search theory, what specific problem does this `reached` set solve, and what would happen to your DFS agent without it?**

**Answer:**
The `reached` set solves the problem of redundant paths and infinite loops by keeping track of which states have already been explored. 

Without it (i.e., operating as a *Tree Search* instead of a *Graph Search*), a DFS agent could get stuck infinitely walking back and forth between two adjacent empty cells (e.g., `Left -> Right -> Left -> Right`).

### Question 3
> **Why is BFS guaranteed to be optimal in this specific grid, whereas DFS produces winding, suboptimal routes?**

**Answer:**
- **BFS (Breadth-First Search):** Expands nodes layer by layer (shallowest nodes first). In a grid where every step has the exact same uniform cost of 1, the first time BFS encounters the goal, it is mathematically guaranteed to have taken the fewest number of steps. 
- **DFS (Depth-First Search):** Dives blindly down the deepest path first. It will take the first route it stumbles upon that eventually reaches the goal, regardless of how winding or long that path is.

### Question 4
> **If we scaled up to a massive 1000x1000 grid, BFS and UCS might crash before finding food. Contrast the memory bottlenecks of BFS versus DFS.**

**Answer:**
- **BFS Space Complexity ($O(b^d)$):** BFS has an exponential space complexity (where $b$ is the branching factor and $d$ is the depth). In a 1000x1000 grid, the frontier queue size grows massively as it holds the entire perimeter of the expanding search radius in memory, easily causing Out-of-Memory crashes.
- **DFS Space Complexity ($O(b \times m)$):** DFS has a linear space complexity (where $m$ is the maximum depth). It only needs to store a single path from the root to a leaf node at any given time, making it incredibly memory efficient even on massive grids, though it may return terrible paths.

---

# IT3012 - Intelligent Agents - Lab Practical 04

## Overview
This branch contains the completed tasks for **Practical 04: Informed Search**.
We enhance the Goal-Based/Planning Agent by implementing **A* Search**, which uses heuristics to drastically reduce the number of explored nodes in the environment.

## Modifications Made
- **Heuristic Functions**: Added `manhattan_distance` and `euclidean_distance` functions to calculate distance metrics on the 2D grid.
- **A* Search Implementation**: Created `astar_search` which evaluates nodes using $f(n) = g(n) + h(n)$, prioritizing the most promising paths using a priority queue.
- **Decision Loop Integration**: Integrated A* into the agent's decision loop, setting it up to find the closest food item and plot an optimized path to it.

---

## Part 2: Theoretical Evaluation Answers

### Question 1
> **What is the key difference between how Uniform-Cost Search (UCS) and A* Search prioritize which node to explore next?**

**Answer:**
- **UCS** prioritizes exploring nodes strictly based on the actual path cost accumulated from the start node so far, denoted as $g(n)$. 
- **A* Search** prioritizes nodes based on both the cost so far AND an estimated cost to the goal, denoted as $f(n) = g(n) + h(n)$ (where $h(n)$ is the heuristic). This makes A* much more directed toward the goal rather than expanding uniformly in all directions.

### Question 2
> **In Step 1.1, you used Manhattan Distance. Why is Manhattan Distance considered an "admissible" heuristic for this specific 4-way movement grid, and what would happen to your A* algorithm if the heuristic was NOT admissible?**

**Answer:**
Manhattan Distance is admissible for a 4-way grid because it calculates the absolute minimum number of steps required to reach the goal assuming there are no obstacles. Because of this, it will **never overestimate** the true cost. 

If the heuristic was not admissible (i.e., it overestimates the cost), A* would lose its mathematical guarantee of optimality. It might return a sub-optimal, longer path because it could unfairly penalize and avoid the truly optimal route.

### Question 3
> **If we modified `visual_grid_game.py` to allow the agent to move diagonally (8-way movement), would Manhattan distance still be an admissible heuristic? Why or why not? Which metric should you switch to?**

**Answer:**
No, Manhattan distance would **not** be admissible in an 8-way movement grid. In an 8-way grid, a diagonal move covers both horizontal and vertical distance in a single step (cost of 1), whereas Manhattan distance would count it as 2 steps. This would cause the heuristic to overestimate the true cost. 

You should switch to **Chebyshev distance** (which treats diagonal moves correctly as 1 step) or **Euclidean distance**.

### Question 4
> **When targeting multiple food items simultaneously, calculating the distance to just the single closest food item is a weak heuristic. Propose (in text) a stronger heuristic for navigating the grid to eat ALL remaining food efficiently.**

**Answer:**
A much stronger heuristic for targeting multiple food items is to calculate the **Minimum Spanning Tree (MST)** of all remaining food items plus the agent's current position. You can use the total edge weight of the MST as the heuristic $h(n)$. This considers the spatial layout and clustering of all remaining food collectively, rather than just greedily focusing on the nearest single item which often leads to backtracking later.
