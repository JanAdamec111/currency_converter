import unittest
from cli_currency_converter.CLI_currency_converter import (currency_code_check,
input_output_converter, same_symbol_check, amount_check)


class TestAmount(unittest.TestCase):
    """Test for amount input."""
    def test_positive(self):
        self.assertEqual(amount_check(1, 1, 3.1), 3.1)


class TestSameSymbol(unittest.TestCase):
    """Test for currencies with same symbol. Input needed."""
    def test_signs(self):
        self.assertNotEqual(same_symbol_check("$", "£"), ("$", "£"))

    def test_three_letters(self):
        self.assertEqual(same_symbol_check("EUR", "AUD"), ("EUR", "AUD"))


class TestThreeLetterConverter(unittest.TestCase):
    """Test for converting signs to three-letter abbreviation."""
    def test_usd_dollar_sign(self):
        self.assertEqual(input_output_converter("USD", "$"), ("USD", "USD"))


class TestCurrencyCode(unittest.TestCase):
    """Test for currency code = True."""
    def test_CAD(self):
        self.assertTrue(currency_code_check("CAD"))

    def test_dollar_sign(self):
        self.assertFalse(currency_code_check("$"))

    def test_usd(self):
        self.assertTrue(currency_code_check("usd"))


if __name__ == "__main__":
    unittest.main()