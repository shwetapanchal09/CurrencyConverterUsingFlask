from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
# Replace with your actual API key
API_KEY = os.getenv('API_KEY')
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"

# Fetch supported currencies
def get_supported_currencies():
    try:
        response = requests.get(f"{BASE_URL}/codes")
        data = response.json()
        if data['result'] == 'success':
            # Return the supported currencies as a list of [currency_code, currency_name]
            return data['supported_codes']
        else:
            # Fallback currencies in case of error
            return [['USD', 'United States Dollar'], ['EUR', 'Euro'], ['GBP', 'British Pound'], ['JPY', 'Japanese Yen']]
    except Exception as e:
        print(f"Error fetching supported currencies: {e}")
        return [['USD', 'United States Dollar'], ['EUR', 'Euro'], ['GBP', 'British Pound'], ['JPY', 'Japanese Yen']]

# Homepage route
@app.route('/', methods=['GET', 'POST'])
def index():
    conversion_result = None
    currencies = get_supported_currencies()  # Fetch the supported currencies

    if request.method == 'POST':
        from_currency = request.form.get('from_currency')
        to_currency = request.form.get('to_currency')
        amount = float(request.form.get('amount', 1))

        # Fetch conversion rates
        response = requests.get(f"{BASE_URL}/latest/{from_currency}")
        data = response.json()

        if data['result'] == 'success':
            conversion_rate = data['conversion_rates'].get(to_currency)
            if conversion_rate:
                converted_amount = round(amount * conversion_rate, 2)
                conversion_result = f"{amount} {from_currency} = {converted_amount} {to_currency}"
            else:
                conversion_result = "Conversion rate not available for the selected currencies."
        else:
            conversion_result = "Error fetching data from the currency API."

    return render_template('index.html', result=conversion_result, currencies=currencies)

if __name__ == '__main__':
    app.run(debug=True)
