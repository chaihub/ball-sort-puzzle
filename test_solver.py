from solver import BallSortGame, PuzzleState, TubeState, Move


class TestBallSortGame:
    def test_init(self):
        test_game = BallSortGame()
        assert test_game.no_t and test_game.t_cap and test_game.no_c and test_game.no_b and \
               test_game.state_sequence and test_game.states_visited and test_game.move_sequence and \
               not test_game.game_solved and not test_game.game_over

    def test_check_if_solved_negative(self):
        test_game = BallSortGame()
        test_game.check_if_solved()
        assert test_game.game_solved is False

    def test_check_if_solved_positive(self):
        test_game = BallSortGame()
        test_game.state_sequence.p_seq[0].p_state[0].contents = 'GGG'
        test_game.state_sequence.p_seq[0].p_state[1].contents = 'BBB'
        test_game.state_sequence.p_seq[0].p_state[2].contents = 'xxx'
        test_game.check_if_solved()
        assert test_game.game_solved is True

    def test_check_state_equivalence_degenerate(self):
        test_game = BallSortGame()
        assert test_game.check_state_equivalence(test_game.state_sequence.p_seq[0],
                                                 test_game.state_sequence.p_seq[0]) is True

    def test_check_state_equivalence_negative(self):
        test_game = BallSortGame()
        state1 = PuzzleState([], [])
        state1.p_state = [TubeState('xxx'), TubeState('RGx'), TubeState('GRx')]
        test_game.state_sequence.p_seq.append(state1)
        assert test_game.check_state_equivalence(test_game.state_sequence.p_seq[0],
                                                 test_game.state_sequence.p_seq[1]) is False

    def test_check_state_equivalence_positive(self):
        test_game = BallSortGame()
        state1 = PuzzleState([], [])
        state1.p_state = [TubeState('GBx'), TubeState('xxx'), TubeState('BGx')]
        test_game.state_sequence.p_seq.append(state1)
        assert test_game.check_state_equivalence(test_game.state_sequence.p_seq[0],
                                                 test_game.state_sequence.p_seq[1]) is True

    def test_identify_possible_moves(self):
        assert False

    def test_eliminate_loop_moves_degenerate(self):
        test_game = BallSortGame()
        test_game.state_sequence.p_seq[0].poss_moves.append(Move(1, 0))
        test_game.state_sequence.p_seq[0].poss_moves.append(Move(2, 0))
        test_game.eliminate_loop_moves()
        assert (test_game.state_sequence.p_seq[0].poss_moves[0] == Move(1, 0) and
                test_game.state_sequence.p_seq[0].poss_moves[1] == Move(2, 0))

    def test_eliminate_loop_moves_negative(self):
        assert False

    def test_moves_possible(self):
        assert False

    def test_evaluate_possible_moves(self):
        assert False

    def test_record_possible_moves(self):
        assert False

    def test_make_best_move(self):
        assert False

    def test_move_back(self):
        assert False

    def test_at_starting_state(self):
        assert False
