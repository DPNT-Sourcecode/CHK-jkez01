from solutions.HLO import hello_solution
import pytest


class TestHello():
    def test_one(self):
        assert hello_solution.hello("World") == "Hello, World!"

    def test_two(self):
        assert hello_solution.hello("John") == "Hello, John!"

