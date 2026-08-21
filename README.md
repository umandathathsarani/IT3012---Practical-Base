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
