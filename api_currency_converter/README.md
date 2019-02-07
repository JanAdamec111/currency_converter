# API Currency Converter

This web API is currency converter for dealing with online exchange rates and contains 139 currencies.


## Technologies

- Python 3.7.2
- Flask framework 1.0.2
- wtforms 2.2.1


## Launch

Launching the project in terminal with following commands.
- activating virtual environment:
source venv/bin/activate
- running the project:
python3 API_currency_converter.py
- you receive http, add "currency_converter/home" and browse it!


## Usage

User enters amount of money to be converted and input currency, both parameters are obligatory. Output currency is optional and if this parameter is missing, amount of input currency is converted to 138 currencies. On the other hand, if output currency is entered, amount of input currency is converted to this currency. Both currencies (input and output) may be entered either with three-letter abbreviation (e.g. for US Dollar - USD, for British Pound - GBP, etc.) or with currency sign (e.g. $, €, £,...). Be aware that some currency signs are connected with more than one currency (e.g. $ may be American, Australian, Canadian, etc. If these signs are entered, user is asked to specify it with three-letter abbreviation.