# cs50-web-finance [Live](https://cs50-web-finance-pset.herokuapp.com/login)

## Introduction 
This application was the 8th week's exercise of Harvard's CS50 - Introduction to Computer Science online course. You can learn more about CS50 at Harvard's CS50.
Implemented a website via which users can login , register, logout , “buy” and “sell” stocks, and view all the histroy transctions, a la the below.

![REGISTER PAGE](./screenshot/REGISTER.png)
![INDEX PAGE](./screenshot/INDEX.png)
![HISTORY PAGE](./screenshot/HISTORY.png)


## Created with
This application uses Python, HTML and styling with Bootstrap. It also uses [IEX API](https://iexcloud.io/) to get the stocks values in real time and a SQL database to store users information, such as username, a hash of the password, the stocks they bought or sold and the history. Technologies have been used :
* cs50==6.0.2
* Flask==1.1.2
* Flask-Session==0.3.2
* Bootstrap - version 4.5.3
* Jinja2==2.11.2
* SQLAlchemy==1.3.22
* Werkzeug==1.0.1

## Specification
### `register`
Complete the implementation of  `register`  in such a way that it allows a user to register for an account via a form.
-   Require that a user input a username, implemented as a text field whose  `name`  is  `username`. Render an apology if the user’s input is blank or the username already exists.
-   Require that a user input a password, implemented as a text field whose  `name`  is  `password`, and then that same password again, implemented as a text field whose  `name`  is  `confirmation`. Render an apology if either input is blank or the passwords do not match.
-   Submit the user’s input via  `POST`  to  `/register`.
-   `INSERT`  the new user into  `users`, storing a hash of the user’s password, not the password itself. Hash the user’s password with  [`generate_password_hash`](http://werkzeug.pocoo.org/docs/0.14/utils/#werkzeug.security.generate_password_hash.*)  Odds are you’ll want to create a new template (e.g.,  `register.html`) that’s quite similar to  `login.html`.

Once you’ve implemented  `register`  correctly, you should be able to register for an account and log in (since  `login`  and  `logout`  already work)! And you should be able to see your rows via phpLiteAdmin or  `sqlite3`.
### `quote`

Complete the implementation of  `quote`  in such a way that it allows a user to look up a stock’s current price.

-   Require that a user input a stock’s symbol, implemented as a text field whose  `name`  is  `symbol`.
-   Submit the user’s input via  `POST`  to  `/quote`.
-   Odds are you’ll want to create two new templates (e.g.,  `quote.html`  and  `quoted.html`). When a user visits  `/quote`  via GET, render one of those templates, inside of which should be an HTML form that submits to  `/quote`  via POST. In response to a POST,  `quote`  can render that second template, embedding within it one or more values from  `lookup`.

### `buy`

Complete the implementation of  `buy`  in such a way that it enables a user to buy stocks.

-   Require that a user input a stock’s symbol, implemented as a text field whose  `name`  is  `symbol`. Render an apology if the input is blank or the symbol does not exist (as per the return value of  `lookup`).
-   Require that a user input a number of shares, implemented as a text field whose  `name`  is  `shares`. Render an apology if the input is not a positive integer.
-   Submit the user’s input via  `POST`  to  `/buy`.
-   Odds are you’ll want to call  `lookup`  to look up a stock’s current price.
-   Odds are you’ll want to  `SELECT`  how much cash the user currently has in  `users`.
-   Add one or more new tables to  `finance.db`  via which to keep track of the purchase. Store enough information so that you know who bought what at what price and when.
    -   Use appropriate SQLite types.
    -   Define  `UNIQUE`  indexes on any fields that should be unique.
    -   Define (non-`UNIQUE`) indexes on any fields via which you will search (as via  `SELECT`  with  `WHERE`).
-   Render an apology, without completing a purchase, if the user cannot afford the number of shares at the current price.
-   You don’t need to worry about race conditions (or use transactions).

Once you’ve implemented  `buy`  correctly, you should be able to see users’ purchases in your new table(s) via phpLiteAdmin or  `sqlite3`.

### `index`

Complete the implementation of  `index`  in such a way that it displays an HTML table summarizing, for the user currently logged in, which stocks the user owns, the numbers of shares owned, the current price of each stock, and the total value of each holding (i.e., shares times price). Also display the user’s current cash balance along with a grand total (i.e., stocks’ total value plus cash).

-   Odds are you’ll want to execute multiple  `SELECT`s. Depending on how you implement your table(s), you might find  [GROUP BY](https://www.google.com/search?q=SQLite+GROUP+BY,)  [HAVING](https://www.google.com/search?q=SQLite+HAVING,)  [SUM](https://www.google.com/search?q=SQLite+SUM,)  and/or  [WHERE](https://www.google.com/search?q=SQLite+WHERE)  of interest.
-   Odds are you’ll want to call  `lookup`  for each stock.

### `sell`

Complete the implementation of  `sell`  in such a way that it enables a user to sell shares of a stock (that he or she owns).

-   Require that a user input a stock’s symbol, implemented as a  `select`  menu whose  `name`  is  `symbol`. Render an apology if the user fails to select a stock or if (somehow, once submitted) the user does not own any shares of that stock.
-   Require that a user input a number of shares, implemented as a text field whose  `name`  is  `shares`. Render an apology if the input is not a positive integer or if the user does not own that many shares of the stock.
-   Submit the user’s input via  `POST`  to  `/sell`.
-   You don’t need to worry about race conditions (or use transactions).

### `history`
Complete the implementation of  `history`  in such a way that it displays an HTML table summarizing all of a user’s transactions ever, listing row by row each and every buy and every sell.

-   For each row, make clear whether a stock was bought or sold and include the stock’s symbol, the (purchase or sale) price, the number of shares bought or sold, and the date and time at which the transaction occurred.
-   You might need to alter the table you created for  `buy`  or supplement it with an additional table. Try to minimize redundancies.

## Run

You will need  [Python](https://www.python.org/downloads/)  and  [Flask](https://flask.palletsprojects.com/en/1.1.x/installation/)  installed on your computer to run this application.
Start by installing  [Python 3](https://www.python.org/downloads/). Here's a  [guide on the installation](https://wiki.python.org/moin/BeginnersGuide/Download). Once you have Python, and clonned this repository, run the following commands:

To install pip, run:
`sudo apt install python3-pip`
To install Flask, run:
`sudo apt install python3-flask`
To install this project's dependencies, run:
`pip3 install -r requirements.txt`
Define the correct file as the default Flask application:

Unix Bash (Linux, Mac, etc.):
`export FLASK_APP=application.py`
Windows CMD:
`set FLASK_APP=application.py`
Windows PowerShell:
`$env:FLASK_APP = "application.py"`

Run Flask and you're good to go!
`flask run`
