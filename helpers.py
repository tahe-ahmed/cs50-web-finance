from config import API_KEY
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = API_KEY
        response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def unique_stocks(stocks):
    """filter the stocks to a unique stocks list"""
    stocks_unique_list = []
    stocks_length = len(stocks)
    #iterate over the stocks to filter them to the stocks_unique
    for i in range(stocks_length):
        # if stocks_unique empty append the first item 
        if len(stocks_unique_list) < 1:
            stocks_unique_list.append(stocks[i])
        else:
            # iterate over the unique stocks
            for x in range(len(stocks_unique_list)):
                # if the stock already exits add the shares number
                if stocks[i]["symbol"] == stocks_unique_list[x]["symbol"]:
                    stocks_unique_list[x]["shares"] += stocks[i]["shares"]
                    break
                # if the stock does not exit before append it to the unique stocks list
                elif x == len(stocks_unique_list) - 1:
                    stocks_unique_list.append(stocks[i])
    
    return stocks_unique_list

