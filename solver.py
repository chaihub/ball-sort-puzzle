""" solver.py

Solve the ball sort puzzle.

Usage: #TODO

Input file format: #TODO

Created by Chaitanya Rajguru 23-Aug-2022
"""

import sys
import os

class BallSortGame:
    def __init__(self):
        """Readiness:Hardcoded"""
        self.no_t = 3    # Number of tubes
        self.t_cap = 3   # Tube capacity
        self.no_c = 2    # Number of ball colors
        self.no_b = 2    # Number of balls of each color
        self.state_history = [['xxx', 'GBx', 'BGx']]     # Convention: tube contents listed bottom first
        self.move_history = []
        #TODO: Read inputs and check constraints
        self.game_solved = False
        self.game_over = False

    def check_if_solved(self):
        """Readiness:Full"""
        #current_state = self.state_history[len(self.state_history) - 1]
        current_state = self.state_history[-1]
        solved = True
        for t in range(self.no_t):
            no_colors_t = len(set(current_state[t]) - set('x'))
            if no_colors_t > 1:
                solved = False
                break
        self.game_solved = solved

    def check_state_equivalence(s1, s2):
        """Readiness:Hardcoded"""
        "Make copies of both states. Loop through tubes in one and delete that tube from both states. If both state copies are empty at the end, then the states are equivalent."
        pass

    def identify_possible_moves(self):
        """Readiness:Hardcoded"""
        "For each tube, check all other tubes that can accept the top ball. Possible moves = pairs of (tube_from, tube_to). Can accept if fully empty or if at least one empty location with top ball of same color. Store along with current state."
        pass

    def eliminate_loop_moves(self):
        """Readiness:Hardcoded"""
        "For the possible move, compute the next state. Check if the next state has already been visited, using check_state_equivalence(). If yes, delete that possible move."
        pass

    def moves_possible(self):
        """Readiness:Hardcoded"""
        "Check for non-empty set of possible moves."
        pass

    def evaluate_possible_moves(self):
        """Readiness:Hardcoded"""
        pass

    def record_possible_moves(self):
        """Readiness:Hardcoded"""
        "Option 1: Compute weight of the color by adding up weights of all same-color balls, with balls at top getting highest weights."
        "Option 2: Prioritize moving into empty tubes."
        "Option 3: Prioritize uncovering balls with maximum weights, calculated same as in Option 1."
        "Option 4: Prioritize moving out of empty tubes."
        pass

    def make_best_move(self):
        """Readiness:Hardcoded"""
        "Find moves with best assessments, and pick the first one."
        "Create new state. Append to visited states list, state history, and move history."
        pass

    def move_back(self):
        """Readiness:Hardcoded"""
        "Delete last entries in state history and move history, but not in visited states list."
        pass

    def at_starting_state(self):
        """Readiness:Hardcoded"""
        pass


def report_results(game):
    """Readiness:Partial"""
    print('Game result: ', 'Solved' if game.game_solved else 'Failed')
    print(f'Starting state: {game.state_history[0]}')
    print(f'Starting state: {game.state_history[-1]}')
    #print(f'Ending state:   {game.state_history[len(game.state_history) - 1]}')
    print(f'Number of moves: {len(game.move_history)}')


def main():
    """Solve a given game; Readiness:Partial"""
    this_game = BallSortGame()
    while not this_game.game_over:
        this_game.check_if_solved()
        if this_game.game_solved:
            this_game.game_over = True
            break
        this_game.identify_possible_moves()
        this_game.eliminate_loop_moves()
        if this_game.moves_possible():  # Go forward
            this_game.evaluate_possible_moves()
            this_game.record_possible_moves()
            this_game.make_best_move()
        else:  # Can't go forward
            if this_game.at_starting_state():  # Can't go backward either
                this_game.game_over = True
                break
            else:  # Go backward
                this_game.move_back()

    report_results(this_game)

if __name__ == '__main__':
    main()