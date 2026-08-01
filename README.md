# IT3012 - Intelligent Agents - Lab Practical 02

## Overview
This branch contains the completed tasks for **Practical 02: Agent Architectures**.
The modifications implement a Simple Reflex Agent and a Model-Based Agent in a partially observable environment.

## Modifications Made
- **Partial Observability**: Modified `get_percept` in `visual_grid_game.py` so the agent only receives local boolean flags (`wall_ahead`, `wall_left`, `wall_right`, `food_here`) based on its current facing direction, rather than global coordinates.
- **Simple Reflex Agent**: Created `SimpleReflexAgent` using strict condition-action rules (`IF food_here THEN suck; IF wall_ahead THEN turn_left; ELSE move_forward`). This agent struggles and falls into infinite loops in complex map structures due to a lack of memory.
- **Model-Based Agent**: Created `ModelBasedAgent` which tracks its relative movement and history (`visited_cells`) to avoid getting trapped in loops. It updates its internal state before deciding on its next action.
- **Agent Direction**: Modified the core game environment to track and visually display the agent's facing direction.
