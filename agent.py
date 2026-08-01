import random

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