from solutions.SUM import sum_solution
import pytest


class TestSum():
    def test_sum(self):
        assert sum_solution.compute(1, 2) == 3

    def test_min(self):
        assert sum_solution.compute(0,0) == 0
    
    def test_max(self):
        assert sum_solution.compute(100,100) == 200

    def test_edge_one(self):
        assert sum_solution.compute(0,100) == 100

    def test_edge_two(self):
        assert sum_solution.compute(100,0) == 100

    def test_middle(self):
        assert sum_solution.compute(49,52) == 101

    def test_bad_left_str(self):
        with pytest.raises(Exception):
            sum_solution.compute('a',0)

    def test_bad_left_low(self):
        with pytest.raises(ValueError):
            sum_solution.compute(-1,0)

    def test_bad_left_high(self):
        with pytest.raises(ValueError):
            sum_solution.compute(101,0)

    def test_bad_left_float(self):
        with pytest.raises(ValueError):
            sum_solution.compute(1.2,0)
