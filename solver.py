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
        self.state_history = [['BGx', 'GBx', 'xxx']]     # Convention: tube contents listed bottom first
        self.move_history = []
        #TODO: Read inputs and check constraints
        self.game_solved = False
        self.game_over = False

    def check_if_solved(self):
        """Readiness:Hardcoded"""
        self.game_solved = True

def report_results(game):
    """Readiness:Partial"""
    print('Game result: ', 'Solved' if game.game_solved else 'Failed')
    print(f'Starting state: {game.state_history[0]}')
    print(f'Ending state:   {game.state_history[len(game.state_history) - 1]}')
    print(f'Number of moves: {len(game.move_history)}')

def main():
    """Solve a given game; Readiness:Partial"""
    this_game = BallSortGame()
    while not this_game.game_over:
        this_game.check_if_solved()
        if this_game.game_solved:
            this_game.game_over = True
            break
        identify_possible_moves()
        eliminate_loop_moves()
        if moves_possible():  # Go forward
            evaluate_possible_moves()
            record_possible_moves()
            make_best_move()
        else:  # Can't go forward
            if at_starting_state():  # Can't go backward either
                this_game.game_over = True
                break
            else:  # Go backward
                move_back()

    report_results(this_game)

if __name__ == '__main__':
    main()