from skyjo.environment import EXPECTED_VALUE
from skyjo.policies.gliding_greedy_policy import linear_gliding_function


def test_linear_gliding_function():
    acceptance_value = 1
    assert linear_gliding_function(0, acceptance_value) == acceptance_value
    assert linear_gliding_function(11, acceptance_value) == EXPECTED_VALUE
