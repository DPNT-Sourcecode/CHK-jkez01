from solutions.CHK import checkout_solution
import pytest


class TestCheckout():
    def test_one(self):
        assert checkout_solution.checkout("World") == "Hello, World!"

