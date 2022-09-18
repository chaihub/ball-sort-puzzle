from solver import BallSortGame, PuzzleState, TubeState, Move, MoveEval


class TestBallSortGame:
    def test_init(self):
        test_game = BallSortGame("game_simple_GB.json")
        assert test_game.no_t and test_game.t_cap and test_game.no_c and test_game.no_b and \
               test_game.state_sequence and test_game.states_visited and test_game.move_sequence and \
               test_game.moves_eval and not test_game.game_solved and not test_game.game_over

    def test_check_if_solved_negative(self):
        test_game = BallSortGame("game_simple_GB.json")
        test_game.check_if_solved()
        assert test_game.game_solved is False

    def test_check_if_solved_positive(self):
        test_game = BallSortGame("game_simple_GB.json")
        test_game.state_sequence.p_seq[0].p_state[0].contents = 'GGG'
        test_game.state_sequence.p_seq[0].p_state[1].contents = 'BBB'
        test_game.state_sequence.p_seq[0].p_state[2].contents = 'xxx'
        test_game.check_if_solved()
        assert test_game.game_solved is True

    def test_check_state_equivalence_degenerate(self):
        test_game = BallSortGame("game_simple_GB.json")
        assert test_game.check_state_equivalence(test_game.state_sequence.p_seq[0],
                                                 test_game.state_sequence.p_seq[0]) is True

    def test_check_state_equivalence_negative(self):
        test_game = BallSortGame("game_simple_GB.json")
        state1 = PuzzleState([], [])
        state1.p_state = [TubeState('xxx'), TubeState('RGx'), TubeState('GRx')]
        test_game.state_sequence.p_seq.append(state1)
        assert test_game.check_state_equivalence(test_game.state_sequence.p_seq[0],
                                                 test_game.state_sequence.p_seq[1]) is False

    def test_check_state_equivalence_positive(self):
        test_game = BallSortGame("game_simple_GB.json")
        state1 = PuzzleState([], [])
        state1.p_state = [TubeState('GBx'), TubeState('xxx'), TubeState('BGx')]
        test_game.state_sequence.p_seq.append(state1)
        assert test_game.check_state_equivalence(test_game.state_sequence.p_seq[0],
                                                 test_game.state_sequence.p_seq[1]) is True

    def test_identify_possible_moves(self):
        assert False

    def test_eliminate_loop_moves_negative(self):
        test_game = BallSortGame("game_simple_GB.json")
        test_game.state_sequence.p_seq[0].poss_moves.append(Move(1, 0))
        test_game.state_sequence.p_seq[0].poss_moves.append(Move(2, 0))
        test_game.eliminate_loop_moves()
        assert (test_game.state_sequence.p_seq[0].poss_moves[0] == Move(1, 0) and
                test_game.state_sequence.p_seq[0].poss_moves[1] == Move(2, 0))

    def test_eliminate_loop_moves_positive(self):
        test_game = BallSortGame("game_simple_RGB_almostdone.json")
        test_game.eliminate_loop_moves()
        assert test_game.state_sequence.p_seq[-1].poss_moves == [Move(2, 1)]

    def test_moves_possible_negative(self):
        test_game = BallSortGame("game_simple_GB.json")
        assert test_game.moves_possible() is False

    def test_moves_possible_positive(self):
        test_game = BallSortGame("game_simple_RGB_almostdone.json")
        assert test_game.moves_possible() is True

    def test_evaluate_possible_moves_degenerate(self):
        test_game = BallSortGame("game_simple_GB.json")
        test_game.evaluate_possible_moves()
        assert len(test_game.moves_eval.me_seq) == len(test_game.state_sequence.p_seq[-1].poss_moves)

    def test_evaluate_possible_moves_simple1(self):
        test_game = BallSortGame("game_simple_GB.json")
        test_game.state_sequence.p_seq[0].poss_moves.append(Move(1, 0))
        test_game.state_sequence.p_seq[0].poss_moves.append(Move(2, 0))
        test_game.evaluate_possible_moves()
        assert len(test_game.moves_eval.me_seq) == len(test_game.state_sequence.p_seq[-1].poss_moves)

    def test_evaluate_possible_moves_simple2(self):
        test_game = BallSortGame("game_simple_RGB_almostdone.json")
        test_game.evaluate_possible_moves()
        assert len(test_game.moves_eval.me_seq) == len(test_game.state_sequence.p_seq[-1].poss_moves)

    def test_make_best_move_degenerate(self):
        test_game = BallSortGame("game_simple_GB.json")
        test_game.moves_eval.me_seq.append(MoveEval(Move(1,0), 1))
        test_game.moves_eval.me_seq.append(MoveEval(Move(2,0), 1))
        test_game.make_best_move()

        if test_game.state_sequence.p_seq[-1].p_state == \
                [TubeState("Bxx"), TubeState("Gxx"), TubeState("BGx")]:
            correct_state_sequence = True
        else:
            correct_state_sequence = False
        if test_game.states_visited.s_visited[-1].p_state == \
                [TubeState("Bxx"), TubeState("Gxx"), TubeState("BGx")]:
            correct_states_visited = True
        else:
            correct_states_visited = False
        if test_game.move_sequence.m_seq[-1] == Move(1, 0):
            correct_move_sequence = True
        else:
            correct_move_sequence = False
        assert correct_state_sequence and correct_states_visited and correct_move_sequence

    def test_make_best_move_evaluate(self):
        test_game = BallSortGame("game_simple_GB.json")
        test_game.moves_eval.me_seq.append(MoveEval(Move(1,0), 2))
        test_game.moves_eval.me_seq.append(MoveEval(Move(2,0), 1))
        test_game.make_best_move()

        if test_game.state_sequence.p_seq[-1].p_state == \
            [TubeState("Gxx"), TubeState("GBx"), TubeState("Bxx")]:
            correct_state_sequence = True
        else:
            correct_state_sequence = False
        if test_game.states_visited.s_visited[-1].p_state == \
            [TubeState("Gxx"), TubeState("GBx"), TubeState("Bxx")]:
            correct_states_visited = True
        else:
            correct_states_visited = False
        if test_game.move_sequence.m_seq[-1] == Move(2, 0):
            correct_move_sequence = True
        else:
            correct_move_sequence = False
        assert correct_state_sequence and correct_states_visited and correct_move_sequence

    def test_move_back(self):
        assert False

    def test_at_starting_state(self):
        assert False
