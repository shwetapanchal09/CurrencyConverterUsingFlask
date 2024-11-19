
# Currency Converter Code Explanation

This document explains the currency converter code step-by-step, including the flow and logic of each part.

## Overview

This project is a simple currency converter web application built using Python's Flask framework. The application uses an external API to fetch currency conversion rates and displays the converted value based on user input.

### File Structure

- `app.py`: The main Python script that defines the Flask app and handles requests.
- `index.html`: The HTML template that renders the user interface for the currency converter.

## Explanation of `app.py`

```python
from flask import Flask, render_template, request
import requests
```
- **Importing Libraries**:
  - `Flask`: The core class for creating the web application.
  - `render_template`: A function to render HTML templates.
  - `request`: An object to access incoming request data (like form inputs).
  - `requests`: A library to handle HTTP requests, used here to fetch data from an external API.

```python
app = Flask(__name__)
```
- **Create a Flask application instance**: This line initializes the Flask app using `__name__` as the argument, which tells Flask to use the current module.

### Setting Up the API Details

```python
API_KEY = 'b2f05ff958fec0f96caddb74'
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"
```
- **API_KEY**: A placeholder API key for the currency conversion API.
- **BASE_URL**: The base URL for the API requests, using the provided `API_KEY`.

### Fetching Supported Currencies

```python
def get_supported_currencies():
    try:
        response = requests.get(f"{BASE_URL}/codes")
        data = response.json()
        if data['result'] == 'success':
            return data['supported_codes']
        else:
            return [['USD', 'United States Dollar'], ['EUR', 'Euro'], ['INR', 'Indian rupees'], ['JPY', 'Japanese Yen']]
    except Exception as e:
        print(f"Error fetching supported currencies: {e}")
        return [['USD', 'United States Dollar'], ['EUR', 'Euro'], ['INR', 'Indian rupees'], ['JPY', 'Japanese Yen']]
```
- **get_supported_currencies**:
  - This function fetches a list of supported currencies from the API.
  - If the API request is successful, it returns a list of currency codes and names.
  - If the API request fails (e.g., network error), it falls back to a default list of currencies.

### Homepage Route

```python
@app.route('/', methods=['GET', 'POST'])
def index():
    conversion_result = None
    currencies = get_supported_currencies()
```
- **Route setup**: This sets up the homepage route (`/`) to handle both `GET` and `POST` requests.
- **conversion_result**: Initially set to `None`, it will later hold the result of the currency conversion.
- **currencies**: A list of supported currencies is fetched using `get_supported_currencies()`.

### Handling GET and POST Requests

```python
    if request.method == 'POST':
        from_currency = request.form.get('from_currency')
        to_currency = request.form.get('to_currency')
        amount = float(request.form.get('amount', 1))
```
- **Check the request method**: If the method is `POST`, it means the form was submitted.
- **Extract form data**:
  - `from_currency`: The currency to convert from.
  - `to_currency`: The currency to convert to.
  - `amount`: The amount to be converted, defaulting to `1` if not specified.

### Fetching Conversion Rates

```python
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
```
- **API request**: Fetch the conversion rates using the `from_currency`.
- **Check for success**:
  - If successful, retrieve the conversion rate for `to_currency`.
  - Calculate the converted amount and format the result.
  - If the conversion rate is not available, set an error message.
  - If the API request fails, set a general error message.

### Rendering the Template

```python
    return render_template('index.html', result=conversion_result, currencies=currencies)
```
- **Render the template**: This line renders the `index.html` template and passes two variables:
  - **`currencies`**: Always sent to populate the dropdown lists for currency selection.
  - **`result`**: The conversion result, which can be `None`, a success message, or an error message depending on the POST request.

### Running the Application

```python
if __name__ == '__main__':
    app.run(debug=True)
```
- **Entry point**: If this file is executed directly, it will start the Flask server in debug mode, enabling detailed error messages.

## Explanation of `index.html`

The HTML template (`index.html`) handles the user interface for the currency converter.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Currency Converter</title>
</head>
<body>
    <h1>Currency Converter</h1>
    <form method="POST">
        <label for="amount">Amount:</label>
        <input
            type="number"
            step="0.01"
            id="amount"
            name="amount"
            required
            value="1"
        />

        <label for="from_currency">From:</label>
        <select id="from_currency" name="from_currency">
            {% for currency_info in currencies %}
                <option value="{{ currency_info[0] }}">
                    {{ currency_info[1] }} ({{ currency_info[0] }})
                </option>
            {% endfor %}
        </select>
        <br>
        <label for="to_currency">To:</label>
        <select id="to_currency" name="to_currency">
            {% for currency_info in currencies %}
                <option value="{{ currency_info[0] }}">
                    {{ currency_info[1] }} ({{ currency_info[0] }})
                </option>
            {% endfor %}
        </select>
        <br>
        <button type="submit">Convert</button>
    </form>

    {% if result %}
        <h2>{{ result }}</h2>
    {% endif %}
</body>
</html>
```

### Key Parts of the HTML

- **Form Setup**:
  - `<form method="POST">`: Specifies that the form will send data using a POST request.
  - **Input Fields**: 
    - `amount`: The amount to convert, a required number input.
    - `from_currency` and `to_currency`: Dropdowns populated using the `currencies` variable.
  - **Submit Button**: Triggers the POST request when clicked.

- **Conversion Result**:
  - `{% if result %}`: If a conversion result exists (i.e., after a POST request), it displays the result using `<h2>{{ result }}</h2>`.

## Program Flow

1. The Flask app starts and listens on the specified port.
2. On the first visit to the homepage (`GET request`):
   - `index()` function is called.
   - `get_supported_currencies()` is used to fetch the list of currencies.
   - The `index.html` template is rendered with `currencies`.
3. When the form is submitted (`POST request`):
   - Form data is captured and processed in `index()`.
   - Conversion rate is fetched using the external API.
   - Result is calculated and passed back to `index.html`.
   - The `result` is displayed on the page.

