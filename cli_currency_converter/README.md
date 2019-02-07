# CLI Currency Converter

This command line interface currency converter is for dealing with online exchange rates in terminal and contains 139 currencies.


## Technologies

- Python 3.7.2
- click 7.0


## Launch

Launching the project in terminal with following commands.
- activating virtual environment:
source venv/bin/activate
- running the project (examples):
python3 CLI_currency_converter.py (in this case, user is asked for parameters)
python3 CLI_currency_converter.py --amount 10.2, input_currency USD
python3 CLI_currency_converter.py --amount 1.1, input_currency EUR --output_currency CZK
python3 CLI_currency_converter.py --amount 1.1, input_currency AUD --output_currency ¥


# Usage

User enters amount of money to be converted and input currency, both parameters are obligatory. Output currency is optional and if this parameter is missing, amount of input currency is converted to 138 currencies. On the other hand, if output currency is entered, amount of input currency is converted to this currency. Both currencies (input and output) may be entered either with three-letter abbreviation (e.g. for US Dollar - USD, for British Pound - GBP, etc.) or with currency sign (e.g. $, €, £,...). Be aware that some currency signs are connected with more than one currency (e.g. $ may be American, Australian, Canadian, etc. If these signs are entered, user is asked to specify it with three-letter abbreviation.