from solutions.CHK import checkout_solution
import pytest


class TestCheckout():
    def test_one_each(self):
        assert checkout_solution.checkout("ABCD") == 115

    def test_one_product(self):
        assert checkout_solution.checkout("A") == 50

    def test_special(self):
        assert checkout_solution.checkout("AAA") == 130

    def test_non_special(self):
        assert checkout_solution.checkout("C") == 20

    def test_special_plus_one(self):
        assert checkout_solution.checkout("AAAA") == 180

    def test_bad_none(self):
        assert checkout_solution.checkout("") == 0

    def test_bad_unknown(self):
        assert checkout_solution.checkout("E") == -1

    def test_bad_type(self):
        assert checkout_solution.checkout(3) == -1

