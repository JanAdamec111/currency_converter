import flask, json, urllib.request
from flask import request, jsonify, redirect, render_template, flash
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, SubmitField
from wtforms.validators import DataRequired, optional, NumberRange, ValidationError

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "it-is-all-about-the-money"


def input_check(form, field):
    """Function checks whether the input and output currency is valid, i.e. code or symbol.
    Function also checks input currency sign, because some of them are equal to more currencies, e.g. $, kr."""
    value = field.data
    if value != "":
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
                value = value.lower()
                if value == "$" or value == "kr" or value == "£":
                    raise ValidationError("Please specify {} with three-letter currency (e.g. AUD, GBP, USD,...): ".format(value))
                else:
                    value = value.upper()
                    return value
            else:
                raise ValidationError("This currency code or symbol does not exist. Try again!")


class InputsForm(FlaskForm):
    """Form for inputs: amount, input currency, output currency."""
    amount = FloatField("Amount:", validators=[DataRequired(),
                                               NumberRange(min=0,
                                                           message="Amount of money must be positive number. Try again!")])
    input_currency = StringField("Input currency:", validators=[DataRequired(),
                                                                input_check])
    output_currency = StringField("Output currency (optional*):", validators=[optional(),
                                                                              input_check],
                                                                  default="")
    submit = SubmitField("CONVERT!")


def api_amount():
    # Function checks whether amount was provided as part of the URL.
    if "amount" in request.args:
        amount = request.args["amount"]
        amount = float(amount)
        return amount
    else:
        return redirect("/currency_converter/home")


def api_input_currency():
    # Function checks whether input currency was provided as part of the URL.
    if "input_currency" in request.args:
        input_currency = request.args["input_currency"]
        input_currency = input_currency.upper()
        return input_currency
    else:
        return redirect("/currency_converter/home")


def api_output_currency():
    # Function checks whether output currency was provided as part of the URL.
    if "output_currency" in request.args:
        output_currency = request.args["output_currency"]
        output_currency = output_currency.upper()
        return output_currency
    else:
        return redirect("/currency_converter/home")


def input_output_converter(input_currency, output_currency):
    """Function converts input_c and output_c into currency CODE XXX, e.g. USD"""
    for i in input_currency, output_currency:
        i = str(i)
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
    string = str(string)
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

    final_data_all = ({"input": {"amount": amount,
                                 "currency": input_currency},
                       "output": final_output})
    return jsonify(final_data_all)


def final_json(input_currency, output_currency, amount, converted_amount):
    """Function prints final json file with the results."""
    final_data = ({"input": {"amount": amount,
                             "currency": input_currency},
                   "output": {output_currency: round(converted_amount, 2)}})
    return jsonify(final_data)


@app.route("/currency_converter/home", methods=["GET", "POST"])
def home_page():
    # A route to return home page with input form.
    form = InputsForm()
    if form.validate_on_submit():
        flash("Exchange requested for amount: {}, input currency: {}"
              " and output currency: {}".format(
              form.amount.data, form.input_currency.data, form.output_currency.data))
        return redirect("/currency_converter?amount={}&input_currency={}&output_currency={}".format(
               form.amount.data, form.input_currency.data, form.output_currency.data))
    return render_template("inputs.html", title="Inputs", form=form)


@app.route("/currency_converter", methods=["GET"])
def convert():
    # A route to convert and return exchange request.
    amount = api_amount()
    input_currency = api_input_currency()
    output_currency = api_output_currency()
    if output_currency != "":
        input_currency, output_currency = input_output_converter(input_currency, output_currency)
        data = get_data()
        converted_amount = rate_counting(input_currency, output_currency, data, amount)
        final_data = final_json(input_currency, output_currency, amount, converted_amount)
        return final_data
    else:
        data = get_data()
        final_data_all = all_currencies(data, input_currency, amount)
        return final_data_all


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


app.run(debug=True)