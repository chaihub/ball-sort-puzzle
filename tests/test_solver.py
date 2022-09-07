from solver import BallSortGame, PuzzleState, TubeState

class TestBallSortGame:
    def test_check_state_equivalence(self):
        assert True

    def test_compare_states_success_0(self):
        test_game = BallSortGame()
        test_state1 = PuzzleState([TubeState('xxx'), TubeState('GBx'), TubeState('BGx')], [])
        test_state2 = PuzzleState([TubeState('xxx'), TubeState('GBx'), TubeState('BGx')], [])
        assert if test_game.check_state_equivalence(test_state1, test_state2) is True
