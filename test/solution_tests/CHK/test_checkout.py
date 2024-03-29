from solutions.CHK import checkout_solution
import pytest


class TestCheckout():

    def test_none(self):
        assert checkout_solution.checkout("") == 0

    def test_one_each(self):
        assert checkout_solution.checkout("ABCDEF") == 165

    def test_non_special(self):
        assert checkout_solution.checkout("C") == 20

    def test_special_a_one(self):
        assert checkout_solution.checkout("AAA") == 130

    def test_special_a_two(self):
        assert checkout_solution.checkout("AAAAA") == 200

    def test_special_a_both(self):
        assert checkout_solution.checkout("AAAAAAAA") == 330

    def test_special_b_one(self):
        assert checkout_solution.checkout("BB") == 45

    def test_special_e_one_no_b(self):
        assert checkout_solution.checkout("EE") == 80

    def test_special_e_one_with_one_b(self):
        assert checkout_solution.checkout("EEB") == 80

    def test_special_e_one_with_two_b(self):
        assert checkout_solution.checkout("EEBB") == 110

    def test_two_f(self):
        assert checkout_solution.checkout("FF") == 20

    def test_three_f(self):
        assert checkout_solution.checkout("FFF") == 20

    def test_four_f(self):
        assert checkout_solution.checkout("FFFF") == 30

    def test_six_f(self):
        assert checkout_solution.checkout("FFFFFF") == 40

    def test_three_nm(self):
        assert checkout_solution.checkout("NNNM") == 120

    def test_four_nm(self):
        assert checkout_solution.checkout("NNNNM") == 160

    def test_six_nm(self):
        assert checkout_solution.checkout("NNNNNNMM") == 240

    def test_anypack_not_applicable(self):
        assert checkout_solution.checkout("SA") == 70

    def test_anypack_applicable(self):
        assert checkout_solution.checkout("SSXA") == 95

    def test_anypack_applicable(self):
        assert checkout_solution.checkout("ZXYTSZXTSSXA") == 95

    def test_bad_type(self):
        assert checkout_solution.checkout(3) == -1

