from solver import TubeState, PuzzleState, BallSortGame

def test_compare_states_success_0():
    test_game = BallSortGame()
    test_state1 = PuzzleState([TubeState('xxx'), TubeState('GBx'), TubeState('BGx')], [])
    test_state2 = PuzzleState([TubeState('xxx'), TubeState('GBx'), TubeState('BGx')], [])
    assert test_game.check_state_equivalence(test_state1, test_state2) == True