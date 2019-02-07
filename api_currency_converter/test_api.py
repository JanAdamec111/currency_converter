import unittest
from api_currency_converter.API_currency_converter import (currency_code_check,
input_output_converter)


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