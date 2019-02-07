import click, json, urllib.request


class InputException(Exception):
    """Class raised when the input or output currency does not exist."""
    def __init__(self, value):
        self.value = value


def amount_check(ctx, param, value):
    """Function checks whether amount is positive float."""
    try:
        value = float(value)
        if value > 0:
            return value
        else:
            raise ValueError
    except ValueError:
        print("Amount of money must be positive number, nothing else. Try again!")
        value = click.prompt(param.prompt)
        return amount_check(ctx, param, value)


def input_check(ctx, param, value):
    """Function checks whether the input and output currency is valid, i.e. code or symbol."""
    if value != "All currencies. Press ENTER.":
        try:
            value = value.upper()
            with open("list_of_currencies.json", "r") as f:
                data = json.load(f)
                assess = False
                for currency in data.values():
                    if value in currency["symbol_native"]:
                        assess = True
                    if value in currency["code"]:
                        assess = True
                if assess:
                    return value
                else:
                    raise InputException(value)
        except InputException:
            print("This currency code or symbol does not exist. Try again!")
            value = click.prompt(param.prompt)
            return input_check(ctx, param, value)
    else:
        return value


@click.command()
@click.option("--amount", prompt="Amount to be converted",
              help="Amount of money to convert.", callback=amount_check)
@click.option("--input_currency", prompt="Input currency",
              help="Input currency code or currency symbol.",
              callback=input_check)
@click.option("--output_currency", prompt="Output currency", default="All currencies. Press ENTER.",
              help="Output currency code or currency symbol.",
              callback=input_check)

def main_converter(amount, input_currency, output_currency):
    """Main body function."""
    if output_currency != "All currencies. Press ENTER.":
        input_currency, output_currency = same_symbol_check(input_currency, output_currency)
        input_currency, output_currency = input_output_converter(input_currency, output_currency)
        data = get_data()
        converted_amount = rate_counting(input_currency, output_currency, data, amount)
        final_json(input_currency, output_currency, amount, converted_amount)
    # Else-branch for not entered output currency.
    else:
        data = get_data()
        all_currencies(data, input_currency, amount)


def same_symbol_check(input_currency, output_currency):
    """Function checks currency sign, because there're more some of them, e.g. $, kr."""
    if input_currency == "$" or input_currency == "kr" or input_currency == "£":
        input_currency = input("Please specify input with three-letter currency (e.g. AUD, GBP, USD,...): ")
        if not currency_code_check(input_currency):
            input_currency = "$"
            same_symbol_check(input_currency, output_currency)
        else:
            input_currency = input_currency.upper()
    if output_currency == "$" or output_currency == "kr" or output_currency == "£":
        output_currency = input("Please specify output with three-letter currency (e.g. AUD, GBP, USD,...): ")
        if not currency_code_check(output_currency):
            input_currency = "$"
            same_symbol_check(input_currency, output_currency)
        else:
            output_currency = output_currency.upper()
    return input_currency, output_currency


def input_output_converter(input_currency, output_currency):
    """Function converts input_c and output_c into currency CODE XXX, e.g. USD"""
    for i in input_currency, output_currency:
        if not currency_code_check(i):
            with open("list_of_currencies.json", "r") as f:
                data = json.load(f)

                # For cycle finds the three-letter code.
                for currency in data.values():
                    if i in currency["symbol_native"]:
                        if i == input_currency:
                            input_currency = currency["code"]
                        elif i == output_currency:
                            output_currency = currency["code"]
    return input_currency, output_currency


def currency_code_check(string):
    """Function checks the input whether it's currency code (True) or symbol (False)."""
    string = string.upper()
    with open("list_of_currencies.json", "r") as f:
        data = json.load(f)
        result = False
        for currency in data.values():
            if string in currency["code"]:
                result = True
        return result


def get_data():
    """Function gets latest exchange rates from web."""
    with urllib.request.urlopen(
        "http://data.fixer.io/api/latest?access_key=af46552a3c2b1dd2594377d4a6e2815b&format=1") as response:
        source = response.read()
    return json.loads(source)


def rate_counting(input_currency, output_currency, data, amount):
    """Function counts exchange rate of entered currencies - input and output."""
    if input_currency and output_currency in data["rates"]:
        a, b = ((data["rates"][input_currency]), (data["rates"][output_currency]))
        converted_amount = b / a * amount
        return float(converted_amount)


def all_currencies(data, input_currency, amount):
    """Function counts all exchange rates, because user did not enter output currency."""
    if input_currency == "$" or input_currency == "kr" or input_currency == "£":
        input_currency = input("Please specify input with three-letter currency (e.g. AUD, GBP, USD,...): ")
        if not currency_code_check(input_currency):
            input_currency = "$"
            all_currencies(data, input_currency, amount)
        else:
            input_currency = input_currency.upper()

    if not currency_code_check(input_currency):
        with open("list_of_currencies.json", "r") as f:
            data_currency = json.load(f)
            for currency in data_currency.values():
                if input_currency in currency["symbol_native"]:
                    input_currency = currency["code"]

    code = (data["rates"].keys())
    new_code = list(code)
    final_output = {}
    for index, i in enumerate(data["rates"]):
        a = (data["rates"][input_currency])
        b = (data["rates"][i])
        cur_code = (new_code[index])
        converted_amount_not_rounded = b / a * amount
        converted_amount = (round(converted_amount_not_rounded, 2))
        if cur_code != input_currency:
            final_output[cur_code] = converted_amount
        else:
            pass

    json_txt = dict(input={"amount": amount,
                           "currency": input_currency},
                    output=final_output)
    final_data = json.dumps(json_txt, indent=2)
    print(final_data)


def final_json(input_currency, output_currency, amount, converted_amount):
    """Function prints final json file with the results."""
    json_txt = dict(input={"amount": amount,
                           "currency": input_currency},
                    output={output_currency: round(converted_amount, 2)})
    final_data = json.dumps(json_txt, indent=2)
    print(final_data)


if __name__ == "__main__":
    print(">>>CURRENCY CONVERTER<<<")
    main_converter()