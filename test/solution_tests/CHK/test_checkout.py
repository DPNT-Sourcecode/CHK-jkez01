from solutions.CHK import checkout_solution
import pytest


class TestCheckout():
    def test_one_each(self):
        assert checkout_solution.checkout("ABCD") == 115


