import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, unique_stocks

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # store the buy stocks from history
    stocks = db.execute(
        "SELECT symbol, shares, price, operation_name FROM history WHERE user_id = :uid and operation_name = :oper_name", uid=int(session['user_id']), oper_name="BUY")
    # store the sell stocks from history
    soled_stocks = db.execute(
        "SELECT symbol, shares, operation_name, price FROM history WHERE user_id = :uid and operation_name = :oper_name", uid=int(session['user_id']), oper_name="SELL")

    # filter the sold stocks by symbol and add the shares of the same symbol
    unique_soled_stocks = unique_stocks(soled_stocks)

    # filter the buy stocks by symbol and add the shares of the same symbol
    unique_stocks_list = unique_stocks(stocks)

    # if the unique-stock-list is not empty and if sold-stock in not empty
    if len(unique_stocks_list) >= 1 and len(unique_soled_stocks) >= 1:
        # for each element (stock) in unique-stock-list
        for stock in unique_stocks_list:
            # for each element (sold-stock) in sold-stock
            for sold_stock in unique_soled_stocks:
                # if stock equals sold-stock
                if stock["symbol"] == sold_stock["symbol"]:
                    # substract shares from stock
                    stock["shares"] -= sold_stock["shares"]

    # delete the zero shares stocks
    l = len(unique_stocks_list)
    unique_stocks_list_copy = unique_stocks_list.copy()
    for i in range(l):
        if unique_stocks_list[i]["shares"] == 0:
            unique_stocks_list_copy.remove(unique_stocks_list[i])
    unique_stocks_list = unique_stocks_list_copy

    # List to add all totals
    total_sum = []

    # Iterate over the stocks list to append the information needed in index.html table
    if len(unique_stocks_list) >= 1:
        for stock in unique_stocks_list:
            symbol = str(stock["symbol"])
            name = lookup(symbol)["name"]
            price = float(stock["price"])
            shares = int(stock["shares"])
            total = shares * price
            stock["name"] = name
            stock["price"] = usd(price)
            stock["total"] = usd(total)
            total_sum.append(float(total))

    cash = db.execute("SELECT cash FROM users WHERE id = :uid",
                      uid=int(session['user_id']))[0]["cash"]

    cash = sum(total_sum) + float(cash)
    available_cash = float(cash) - sum(total_sum)
    print("CASH :", cash)
    print("available_cash :", available_cash)
    print("total_sum :", total_sum)

    return render_template("index.html", stocks=unique_stocks_list, available_cash=usd(available_cash), cash=usd(cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Store the dictionary returned from the search in a variable
        look = lookup(request.form.get("symbol"))

        # Store the shares inputed
        shares = request.form.get("shares")

        # If the symbol searched or number of shares is invalid, return apology
        if look == None:
            return apology("invalid symbol", 400)
        elif not shares.isdigit() or int(shares) < 1:
            return apology("share must be at least 1", 400)

        # Store how much money the user has
        cash = db.execute(
            "SELECT cash FROM users WHERE id = :uid", uid=int(session['user_id']))

        # Store the value of purchase
        value = look["price"] * int(shares)

        # If the user don't have enough money, apologize
        if int(cash[0]["cash"]) < value:
            return apology("You don't have enough money to proceed", 403)

        # If the user can afford the purchase, proceed
        else:
            # Subtract the value of purchase from the user's cash
            db.execute("UPDATE users SET cash = cash - :value WHERE id = :uid",
                       value=value, uid=int(session['user_id']))

            # Add the transaction to the user's history
            db.execute("INSERT INTO history (user_id, symbol, shares, price, operation_name) VALUES (:uid, :symbol, :shares, :price, 'BUY')",
                       uid=int(session['user_id']),
                       symbol=look['symbol'], shares=request.form.get('shares'), price=look['price'])

            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Put information from 'history' into a list
    stocks = db.execute(
        "SELECT operation_name, symbol, price, sqltime, shares FROM history WHERE user_id = :uid", uid=int(session["user_id"]))

    # Iterate over the stocks list to append the faulty information needed in history.html table
    for stock in stocks:
        symbol = str(stock["symbol"])
        name = lookup(symbol)["name"]
        stock["name"] = name

    return render_template("history.html", stocks=stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Store the dictionary returned from the search
        look = lookup(request.form.get("symbol"))

        # If the symbol searched is invalid, return apology
        if look == None:
            return apology("invalid symbol", 400)

        # If the symbol exists, return the search
        else:
            return render_template("quoted.html", name=look["name"], symbol=look["symbol"], price=usd(look["price"]))
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username is not empty
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password is not empty
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("your passwords don't match", 400)

        try:
            # Insert username and hash of password in the database
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                       username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))
        except:
            return apology("username unavailable", 400)

        # Start session
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        session["user_id"] = rows[0]["id"]

        # redirect user to home
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Store the symbol inputed
        look = lookup(str(request.form.get("symbol")))

        # Store shares inputed
        input_shares = request.form.get("shares")

        # store the buy stocks from history
        stocks = db.execute(
            "SELECT symbol, shares, operation_name FROM history WHERE user_id = :uid and symbol = :symbol and operation_name = :oper_name", uid=int(session['user_id']), symbol=look["symbol"], oper_name="BUY")
        # store the sell stocks from history
        soled_stocks = db.execute(
            "SELECT symbol, shares, operation_name FROM history WHERE user_id = :uid and symbol = :symbol and operation_name = :oper_name", uid=int(session['user_id']), symbol=look["symbol"], oper_name="SELL")

        # filter the sold stocks by symbol and add the shares of the same symbol
        unique_soled_stocks = unique_stocks(soled_stocks)

        # filter the buy stocks by symbol and add the shares of the same symbol
        unique_stocks_list = unique_stocks(stocks)

        # if the unique-stock-list is not empty and if sold-stock in not empty
        if len(unique_stocks_list) >= 1 and len(unique_soled_stocks) >= 1:
            # for each element (stock) in unique-stock-list
            for stock in unique_stocks_list:
                # for each element (sold-stock) in sold-stock
                for sold_stock in unique_soled_stocks:
                    # substract shares from stock
                    stock["shares"] = stock["shares"] - sold_stock["shares"]
                    # delete the stock if it has zero shares
                    if int(stock["shares"]) == 0:
                        unique_stocks_list.remove(stock)

        # count the total shares for this symbol
        shares = 0
        for stock in unique_stocks_list:
            shares += stock["shares"]

        # Store the value of sale
        value = look["price"] * int(input_shares)

        # If the symbol searched or number of shares is invalid, return apology
        if not request.form.get("symbol") or look == None:
            return apology("you must provide a stock", 400)
        elif not shares or int(shares) < 1 or int(input_shares) > int(shares):
            return apology("share number is invalid", 400)
        else:
            # Add the value of sale to the user's cash
            db.execute("UPDATE users SET cash = cash + :value WHERE id = :uid",
                       value=value, uid=int(session['user_id']))

            # Add the transaction to the user's history
            db.execute("INSERT INTO history (user_id, symbol, shares, price, operation_name) VALUES (:uid, :symbol, :shares, :price, 'SELL')",
                       uid=int(session['user_id']),
                       symbol=look['symbol'], shares=request.form.get('shares'), price=look['price'])
           
        return redirect("/")
    else:
        # get the current user symbols
        stocks = db.execute(
            "SELECT symbol, shares, operation_name FROM history WHERE user_id = :uid", uid=int(session['user_id']))
        stocks_unique = unique_stocks(stocks)
        
        return render_template("sell.html", stocks=stocks_unique)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
