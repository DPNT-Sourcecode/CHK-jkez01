from solutions.CHK import checkout_solution
import pytest


class TestCheckout():
    def test_none(self):
        assert checkout_solution.checkout("") == 0
        
    def test_one_each(self):
        assert checkout_solution.checkout("ABCDE") == 155

    def test_non_special(self):
        assert checkout_solution.checkout("C") == 20

    def test_special_a_one(self):
        assert checkout_solution.checkout("AAA") == 130

    def test_special_a_two(self):
        assert checkout_solution.checkout("AAAAA") == 200

    def test_special_a_both(self):
        assert checkout_solution.checkout("AAAAAAAA") == 430

    def test_special_b_one(self):
        assert checkout_solution.checkout("BB") == 45

    def test_special_e_one_no_b(self):
        assert checkout_solution.checkout("EE") == 80

    def test_special_e_one_with_one_b(self):
        assert checkout_solution.checkout("EEB") == 80

    def test_special_e_one_with_two_b(self):
        assert checkout_solution.checkout("EEBB") == 110

    def test_bad_unknown(self):
        assert checkout_solution.checkout("F") == -1

    def test_bad_type(self):
        assert checkout_solution.checkout(3) == -1


