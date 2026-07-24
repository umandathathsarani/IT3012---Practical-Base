# IT3012 - Intelligent Agents - Lab Practical 01

## Overview
This branch contains the completed tasks for **Practical 01: Environment Architecture & Theoretical Evaluation**.
The modifications map back to the theoretical nature of intelligent agents, focusing on the PEAS framework (Performance, Environment, Actuators, Sensors).

## Modifications Made
- **Environment State**: Initialized toxic traps safely avoiding the agent's start position, food, and walls.
- **Perception Subsystem**: Added a `smells_toxin` sensor to alert the agent when it's positioned on a toxic trap.
- **Action Execution**: Programmed a penalty score of 15 points if the agent steps on a toxic trap to prevent metric exploitation.
- **Visual Rendering**: Updated the `visual_grid_game.py` to render the newly created toxic traps as purple shapes on the graphical canvas.
