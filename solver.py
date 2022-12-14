""" solver.py

Solve the ball sort puzzle.

Usage: #TODO

Input file format: #TODO

Created by Chaitanya Rajguru 23-Aug-2022
"""

import json
from dataclasses import dataclass


@dataclass
class TubeState:
    """Class for recording a state of the tube."""
    contents: str

    def is_empty(self) -> bool:
        balls = self.contents.replace('x', '')
        return not balls

    def is_full(self) -> bool:
        return 'x' not in self.contents

    def top_ball(self) -> str:
        balls = self.contents.replace('x', '')
        return balls[-1] if balls else 'x'

    def ball_count(self) -> int:
        balls = self.contents.replace('x', '')
        return len(balls)

    def remove_ball(self, t_cap) -> str:
        if self.is_empty():
            raise ValueError('Trying to remove ball from an empty tube')
        ball_count = self.ball_count()
        color = self.contents[ball_count - 1]
        new_state = ''
        if ball_count > 1:
            new_state += self.contents[0:(ball_count - 1)]
        new_state += (t_cap - ball_count + 1) * 'x'
        self.contents = new_state
        return color

    def add_ball(self, t_cap, color) -> int:
        if self.is_full():
            raise ValueError('Trying to add ball to a full tube')
        # TODO: create the new state string and overwrite
        ball_count = self.ball_count()
        new_state = ''
        new_state += self.contents[0:ball_count] + color
        new_state += (t_cap - ball_count - 1) * 'x'
        self.contents = new_state
        return ball_count + 1


@dataclass
class Move:
    """Class for recording a ball move in the puzzle."""
    from_t: int
    to_t: int


@dataclass
class MoveSequence:
    """Class for recording the move sequence."""
    m_seq: list[Move]


@dataclass
class MoveEval:
    """Class for recording a ball move in the puzzle, along with its evaluation."""
    mv: Move
    eval: int


@dataclass
class MoveEvalSequence:
    """Class for recording the MoveEval sequence."""
    me_seq: list[MoveEval]


@dataclass
class PuzzleState:
    """Class for recording a state of the puzzle."""
    p_state: list[TubeState]
    poss_moves: list[Move]


@dataclass
class PuzzleSequence:
    """Class for recording the puzzle solution sequence."""
    p_seq: list[PuzzleState]


@dataclass
class StatesVisited:
    """Class for recording every state reached."""
    s_visited: list[PuzzleState]


class BallSortGame:
    def __init__(self, game_init_file):
        """Readiness:Full"""
        # TODO: Check constraints
        with open(game_init_file, 'r') as game_file:
            game_data = json.load(game_file)
        self.game_name = game_data['game_name']
        self.no_t = game_data['no_t']  # Number of tubes
        self.t_cap = game_data['t_cap']  # Tube capacity
        self.no_c = game_data['no_c']  # Number of ball colors
        self.no_b = game_data['no_b']  # Number of balls of each color
        # Convention: tube contents listed bottom first

        # TODO: Remove i_state if not required
        self.i_state = []
        for _ in range(self.no_t):
            tube_contents = game_data['i_state'][_]
            self.i_state.append(TubeState(tube_contents))
        poss_moves = []
        initial_state = PuzzleState(self.i_state, poss_moves)

        self.state_sequence = PuzzleSequence([])
        for _i in range(len(game_data['state_sequence']['p_seq'])):
            p_state = []
            for _j in range(self.no_t):
                tube_contents = game_data['state_sequence']['p_seq'][_i]['p_state'][_j]
                p_state.append(TubeState(tube_contents))
            poss_moves = []
            for _j in range(len(game_data['state_sequence']['p_seq'][_i]['poss_moves'])):
                from_t = game_data['state_sequence']['p_seq'][_i]['poss_moves'][_j]['from_t']
                to_t = game_data['state_sequence']['p_seq'][_i]['poss_moves'][_j]['to_t']
                poss_moves.append(Move(from_t, to_t))
            self.state_sequence.p_seq.append(PuzzleState(p_state, poss_moves))

        self.states_visited = StatesVisited([])
        for _i in range(len(game_data['states_visited']['s_visited'])):
            p_state = []
            for _j in range(self.no_t):
                tube_contents = game_data['states_visited']['s_visited'][_i]['p_state'][_j]
                p_state.append(TubeState(tube_contents))
            poss_moves = []
            for _j in range(len(game_data['states_visited']['s_visited'][_i]['poss_moves'])):
                from_t = game_data['states_visited']['s_visited'][_i]['poss_moves'][_j]['from_t']
                to_t = game_data['states_visited']['s_visited'][_i]['poss_moves'][_j]['to_t']
                poss_moves.append(Move(from_t, to_t))
            self.states_visited.s_visited.append(PuzzleState(p_state, poss_moves))

        self.move_sequence = MoveSequence([])
        for _i in range(len(game_data['move_sequence']['m_seq'])):
            from_t = game_data['move_sequence']['m_seq'][_i]['from_t']
            to_t = game_data['move_sequence']['m_seq'][_i]['to_t']
            self.move_sequence.m_seq.append(Move(from_t, to_t))

        self.moves_eval = MoveEvalSequence([])
        self.game_solved = False
        self.game_over = False

    def check_if_solved(self):
        """Readiness:Partial"""
        # TODO: Need to also check if the correct number of balls are in each filled tube
        current_state = self.state_sequence.p_seq[-1].p_state
        solved = True
        for t in range(self.no_t):
            no_colors_t = len(set(current_state[t].contents) - set('x'))
            if no_colors_t > 1:
                solved = False
                break
        self.game_solved = solved

    def check_state_equivalence(self, s1, s2):
        """Readiness:Full"""
        "Make copies of both states. Loop through tubes in one and delete that tube from both states."
        "If both state copies are empty at the end, then the states are equivalent."
        _s1copy = PuzzleState([], [])
        _s2copy = PuzzleState([], [])
        for _ in range(self.no_t):
            tube_contents1 = s1.p_state[_].contents
            _s1copy.p_state.append(TubeState(tube_contents1))
            tube_contents2 = s2.p_state[_].contents
            _s2copy.p_state.append(TubeState(tube_contents2))

        for _1 in range(self.no_t):
            for _2 in range(self.no_t):
                if s1.p_state[_1].contents == s2.p_state[_2].contents:
                    _c = s1.p_state[_1].contents
                    _s1copy.p_state.remove(TubeState(_c))
                    _s2copy.p_state.remove(TubeState(_c))

        return False if _s1copy.p_state or _s2copy.p_state else True

    def identify_possible_moves(self):
        """Readiness:Full"""
        "For each tube, check all other tubes that can accept the top ball. Possible moves = pairs of (tube_from, "
        "tube_to). Can accept if fully empty or if at least one empty location with top ball of same color. Store "
        "along with current state."
        state = self.state_sequence.p_seq[-1].p_state
        for from_tube in range(self.no_t):
            if state[from_tube].is_empty():
                continue
            for to_tube in range(self.no_t):
                if to_tube == from_tube:
                    continue
                if state[to_tube].is_full():
                    continue
                if not state[to_tube].is_empty() and \
                        (state[from_tube].top_ball() != state[to_tube].top_ball()):
                    continue
                self.state_sequence.p_seq[-1].poss_moves += [[from_tube, to_tube]]

    def eliminate_loop_moves(self):
        """Readiness:Full"""
        "For each possible move, compute the next state. Check if the next state has already been visited,"
        "using check_state_equivalence(). If yes, delete that possible move."
        to_delete_moves = MoveSequence([])
        for _move in self.state_sequence.p_seq[-1].poss_moves:
            # Compute the possible next state
            poss_state = PuzzleState([], [])
            for _ in range(self.no_t):
                tube_contents = self.state_sequence.p_seq[-1].p_state[_].contents
                poss_state.p_state.append(TubeState(tube_contents))
            color = poss_state.p_state[_move.from_t].remove_ball(self.t_cap)
            poss_state.p_state[_move.to_t].add_ball(self.t_cap, color)
            # Check if the possible next state has already been visited and mark it for deletion
            for v_state in self.states_visited.s_visited:
                if self.check_state_equivalence(poss_state, v_state):
                    print(f'Possible state {poss_state} already visited as: {v_state}')
                    to_delete_moves.m_seq.append(_move)
        # Remove loop moves
        for del_move in to_delete_moves.m_seq:
            print(f'Deleting move {del_move}')
            self.state_sequence.p_seq[-1].poss_moves.remove(del_move)

    def moves_possible(self):
        """Readiness:Full"""
        "Check for non-empty set of possible moves."
        return False if len(self.state_sequence.p_seq[-1].poss_moves) == 0 else True

    def evaluate_possible_moves(self):
        """Readiness:Full"""
        "Evaluate possible moves and save their evaluation for further use."
        self.moves_eval.me_seq = []
        for _move in self.state_sequence.p_seq[-1].poss_moves:
            # Compute the possible next state
            poss_state = PuzzleState([], [])
            for _ in range(self.no_t):
                tube_contents = self.state_sequence.p_seq[-1].p_state[_].contents
                poss_state.p_state.append(TubeState(tube_contents))
            color = poss_state.p_state[_move.from_t].remove_ball(self.t_cap)
            poss_state.p_state[_move.to_t].add_ball(self.t_cap, color)
            # Compute the evaluation
            s_eval = self.evaluate_new_state(poss_state)
            # Add move and evaluation to self.moves_eval
            self.moves_eval.me_seq.append(MoveEval(_move, s_eval))

    def evaluate_new_state(self, state):
        """Readiness:Hardcoded"""
        "Convention: Evaluation result will be a positive number. A lower result is more likely to solve the game."
        "Option 1: Compute weight of the color by adding up weights of all same-color balls,"
        "with balls at top getting highest weights."
        "Option 2: Prioritize moving into empty tubes."
        "Option 3: Prioritize uncovering balls with maximum weights, calculated same as in Option 1."
        "Option 4: Prioritize moving out of empty tubes."
        return 1

    def make_best_move(self):
        """Readiness:Full"""
        # Find a move with the best assessment
        i_eval = 0
        i_index = 0
        for _i, i_move in enumerate(self.moves_eval.me_seq):
            if i_eval == 0 or i_move.eval < i_eval:
                i_index = _i
                i_eval = i_move.eval

        # Create new state. Append to visited states list, state history, and move history.
        p_state = []
        from_t = self.moves_eval.me_seq[i_index].mv.from_t
        to_t = self.moves_eval.me_seq[i_index].mv.to_t
        for _ in range(self.no_t):
            tube_contents = self.state_sequence.p_seq[-1].p_state[_].contents
            p_state.append(TubeState(tube_contents))
        color = p_state[from_t].remove_ball(self.t_cap)
        p_state[to_t].add_ball(self.t_cap, color)
        self.state_sequence.p_seq.append(PuzzleState(p_state, []))
        self.states_visited.s_visited.append(PuzzleState(p_state, []))
        self.move_sequence.m_seq.append(Move(from_t, to_t))

    def move_back(self):
        """Readiness:Full"""
        "Delete last entries in state history and move history, but not in visited states list."
        self.state_sequence.p_seq.pop()
        self.move_sequence.m_seq.pop()

    def at_starting_state(self):
        """Readiness:Full"""
        return self.check_state_equivalence(self.state_sequence.p_seq[0], self.state_sequence.p_seq[-1])

    def report_results(self):
        """Readiness:Partial"""
        print('Game result: ', 'Solved' if self.game_solved else 'Failed')
        print('STATE SEQUENCE:')
        print(*self.state_sequence.p_seq)
        #print(f'Starting state: {self.state_sequence.p_seq[0]}')
        #print(f'Ending state: {self.state_sequence.p_seq[-1]}')
        print('MOVE SEQUENCE:')
        print(*self.move_sequence.m_seq)
        print(f'Number of moves: {len(self.move_sequence.m_seq)}')


def main():
    """Solve a given game; Readiness:Partial"""
    this_game = BallSortGame("game_simple_GB.json")
    while not this_game.game_over:
        this_game.check_if_solved()
        if this_game.game_solved:
            this_game.game_over = True
            break
        this_game.identify_possible_moves()
        this_game.eliminate_loop_moves()
        if this_game.moves_possible():  # Go forward
            this_game.evaluate_possible_moves()
            this_game.make_best_move()
        else:  # Can't go forward
            if this_game.at_starting_state():  # Can't go backward either
                this_game.game_over = True
                break
            else:  # Go backward
                this_game.move_back()

    this_game.report_results()


if __name__ == '__main__':
    main()
