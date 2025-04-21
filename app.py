import streamlit as st
import requests

# ----- Page Setup -----
st.set_page_config(page_title="Crypto & Currency Converter", layout="centered")
st.title("💱 Real-Time Crypto & Currency Converter")

# ----- Supported Currency Lists -----
crypto_list = ["bitcoin", "ethereum", "dogecoin"]
fiat_list = ["usd", "inr", "eur", "gbp"]
all_currencies = crypto_list + fiat_list

# ----- User Input -----
amount = st.number_input("Enter the amount", min_value=0.0, value=1.0, step=0.1)
from_currency = st.selectbox("From Currency", all_currencies, index=0)
to_currency = st.selectbox("To Currency", fiat_list, index=1)

# ----- Conversion Functions -----
def get_crypto_price(crypto, fiat):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies={fiat}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[crypto][fiat]
    else:
        return None

def get_fiat_price(from_curr, to_curr):
    url = f"https://api.frankfurter.app/latest?from={from_curr.upper()}&to={to_curr.upper()}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["rates"][to_curr.upper()]
    else:
        return None

# ----- Get Conversion Rate -----
def get_conversion_rate(from_curr, to_curr):
    if from_curr in crypto_list:
        return get_crypto_price(from_curr, to_curr)
    elif from_curr in fiat_list and to_curr in fiat_list:
        return get_fiat_price(from_curr, to_curr)
    else:
        return None

# ----- Display Result -----
rate = get_conversion_rate(from_currency, to_currency)

if rate:
    result = amount * rate
    st.markdown(f"### 🧮 {amount} **{from_currency.upper()}** = {result:.2f} **{to_currency.upper()}**")
    st.caption(f"💹 Live Rate: 1 {from_currency.upper()} = {rate:.4f} {to_currency.upper()}")
else:
    st.error("Could not fetch real-time exchange rate.")
