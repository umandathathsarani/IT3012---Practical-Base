import random
from collections import deque
import heapq
import math

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

class SimpleReflexAgent:
    """A reflex agent that uses only current percepts to act (no memory)."""
    
    def sense_and_act(self, percept: dict) -> str:
        # Example Logic: IF food_here THEN suck; IF wall_ahead THEN turn_left; ELSE move_forward
        if percept.get('food_here'):
            return 'suck'
        if percept.get('wall_ahead'):
            return 'turn_left'
        else:
            return 'move_forward'

class ModelBasedAgent:
    """An agent that maintains internal state to avoid loops."""
    
    def __init__(self):
        # We don't get global coordinates, so we track a relative position
        # Start at a relative origin (0, 0) facing Up
        self.rel_pos = [0, 0]
        self.rel_dir = 'Up'
        self.visited_cells = set()
        self.visited_cells.add(tuple(self.rel_pos))
        self.last_action = None

    def sense_and_act(self, percept: dict) -> str:
        # 1. Update internal state (Transition & Sensor Model) based on last action taken
        directions = ['Up', 'Right', 'Down', 'Left']
        
        if self.last_action == 'turn_left':
            idx = directions.index(self.rel_dir)
            self.rel_dir = directions[(idx - 1) % 4]
        elif self.last_action == 'turn_right':
            idx = directions.index(self.rel_dir)
            self.rel_dir = directions[(idx + 1) % 4]
        elif self.last_action == 'move_forward' and not percept.get('collision', False):
            # Assume we moved forward successfully
            if self.rel_dir == 'Up': self.rel_pos[1] += 1
            elif self.rel_dir == 'Down': self.rel_pos[1] -= 1
            elif self.rel_dir == 'Left': self.rel_pos[0] -= 1
            elif self.rel_dir == 'Right': self.rel_pos[0] += 1
            self.visited_cells.add(tuple(self.rel_pos))

        # 2. Select next action based on IF-THEN rules querying memory
        if percept.get('food_here'):
            action = 'suck'
        else:
            def get_rel_adj(direction, pos):
                if direction == 'Up': return (pos[0], pos[1] + 1)
                elif direction == 'Down': return (pos[0], pos[1] - 1)
                elif direction == 'Left': return (pos[0] - 1, pos[1])
                elif direction == 'Right': return (pos[0] + 1, pos[1])
            
            idx = directions.index(self.rel_dir)
            dir_ahead = self.rel_dir
            dir_left = directions[(idx - 1) % 4]
            dir_right = directions[(idx + 1) % 4]
            
            pos_ahead = get_rel_adj(dir_ahead, self.rel_pos)
            pos_left = get_rel_adj(dir_left, self.rel_pos)
            pos_right = get_rel_adj(dir_right, self.rel_pos)
            
            left_visited = pos_left in self.visited_cells
            right_visited = pos_right in self.visited_cells
            ahead_visited = pos_ahead in self.visited_cells
            
            # Example logic with memory: IF wall_ahead AND left_is_visited THEN turn_right
            if percept.get('wall_ahead'):
                if left_visited and not percept.get('wall_right'):
                    action = 'turn_right'
                else:
                    action = 'turn_left'
            else:
                if ahead_visited and not percept.get('wall_left') and not left_visited:
                    action = 'turn_left'
                elif ahead_visited and not percept.get('wall_right') and not right_visited:
                    action = 'turn_right'
                else:
                    action = 'move_forward'

        self.last_action = action
        return action

class SearchAgent:
    """A goal-based planning agent that uses offline search to find optimal paths."""
    
    def __init__(self):
        self.plan = []
        self.active_algo = 'BFS'  # Switch between 'BFS', 'DFS', 'UCS'
        
    def sense_and_act(self, percept: dict) -> str:
        # If we reached food, suck it
        if percept.get('food_here'):
            return 'suck'
            
        # If we have no plan, formulate one
        if not self.plan:
            all_food = percept.get('all_food')
            if not all_food:
                return 'Stay'  # No more goals
                
            agent_pos = percept['agent_pos']
            
            # Find the closest food pellet as the goal (Manhattan distance)
            goal = min(all_food, key=lambda f: abs(f[0] - agent_pos[0]) + abs(f[1] - agent_pos[1]))
            
            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(agent_pos, goal, percept)
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(agent_pos, goal, percept)
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(agent_pos, goal, percept)
            elif self.active_algo == 'AStar':
                self.plan = self.astar_search(agent_pos, goal, percept['walls'], percept['grid_size'])
                
            if not self.plan:
                # If no path is found, just stay or move randomly
                return 'Stay'
                
        # Execute the next action in the offline plan
        return self.plan.pop(0)

    def get_successors(self, state, percept):
        successors = []
        x, y = state
        width, height = percept['grid_size']
        walls = set(percept['walls'])
        
        # Valid moves (assuming absolute coordinates can be moved directly in our modified execute_action)
        moves = [('Up', (x, y + 1)), ('Right', (x + 1, y)), ('Down', (x, y - 1)), ('Left', (x - 1, y))]
        
        for action, (nx, ny) in moves:
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls:
                successors.append((action, (nx, ny)))
                
        return successors

    def bfs_search(self, start, goal, percept):
        frontier = deque([(start, [])])
        reached = {start}
        
        while frontier:
            state, path = frontier.popleft()
            if state == goal:
                return path
                
            for action, next_state in self.get_successors(state, percept):
                if next_state not in reached:
                    reached.add(next_state)
                    frontier.append((next_state, path + [action]))
        return []

    def dfs_search(self, start, goal, percept):
        frontier = [(start, [])]
        reached = set()
        
        while frontier:
            state, path = frontier.pop()
            if state == goal:
                return path
                
            if state not in reached:
                reached.add(state)
                for action, next_state in self.get_successors(state, percept):
                    if next_state not in reached:
                        frontier.append((next_state, path + [action]))
        return []

    def manhattan_distance(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        
    def euclidean_distance(self, pos, goal):
        return math.sqrt((pos[0] - goal[0])**2 + (pos[1] - goal[1])**2)
        
    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        frontier = []
        reached_states = set()
        
        # Initial g(n) = 0
        g_cost = 0
        
        if heuristic_type == 'manhattan':
            h_cost = self.manhattan_distance(start_pos, goal_pos)
        else:
            h_cost = self.euclidean_distance(start_pos, goal_pos)
            
        f_cost = g_cost + h_cost
        
        # Tuple format: (f_cost, g_cost, current_pos, path_taken)
        heapq.heappush(frontier, (f_cost, g_cost, start_pos, []))
        
        # Helper to get successors specifically for AStar since signature differs from get_successors
        def get_valid_neighbors(pos):
            x, y = pos
            width, height = grid_size
            walls_set = set(walls)
            moves = [('Up', (x, y + 1)), ('Right', (x + 1, y)), ('Down', (x, y - 1)), ('Left', (x - 1, y))]
            valid = []
            for action, (nx, ny) in moves:
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls_set:
                    valid.append((action, (nx, ny)))
            return valid

        while frontier:
            f, g, current_pos, path_taken = heapq.heappop(frontier)
            
            if current_pos == goal_pos:
                return path_taken
                
            if current_pos in reached_states:
                continue
                
            reached_states.add(current_pos)
            
            for action, neighbor in get_valid_neighbors(current_pos):
                if neighbor not in reached_states:
                    g_new = g + 1
                    if heuristic_type == 'manhattan':
                        h_new = self.manhattan_distance(neighbor, goal_pos)
                    else:
                        h_new = self.euclidean_distance(neighbor, goal_pos)
                    f_new = g_new + h_new
                    heapq.heappush(frontier, (f_new, g_new, neighbor, path_taken + [action]))
                    
        return []

    def ucs_search(self, start, goal, percept):
        frontier = []
        heapq.heappush(frontier, (0, start, []))
        reached = {start: 0}
        
        while frontier:
            cost, state, path = heapq.heappop(frontier)
            
            if state == goal:
                return path
                
            for action, next_state in self.get_successors(state, percept):
                new_cost = cost + 1 # Each move has a cost of 1
                if next_state not in reached or new_cost < reached[next_state]:
                    reached[next_state] = new_cost
                    heapq.heappush(frontier, (new_cost, next_state, path + [action]))
        return []