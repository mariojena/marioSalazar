import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import math

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    info = db.execute("SELECT * FROM users WHERE id =?", user_id)
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]

    return render_template("index.html", info = info, cash = cash)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy fruits or Veggi"""
    if request.method == "GET":
        user_id = session["user_id"]
        role = db.execute("SELECT role FROM users WHERE id =?", user_id)
        available_db = db.execute("SELECT * FROM availability WHERE quantity > 0")

        if role[0]["role"] == 'buyer':
            return render_template("buy.html", available = available_db)
        else:
            return apology("You are not allowed to buy")

    else:

        id = request.form.get("id")
        quantity = int(request.form.get(f"quantity{id}"))

        purchase_db = db.execute("SELECT * FROM availability WHERE id=?", id)
        print(purchase_db)
        fruit_v = purchase_db[0]["fruit_v_a"]
        package_t = purchase_db[0]["package_a"]
        price = float(purchase_db[0]["price_a"])
        seller_id = purchase_db[0]["user_id"]
        quantityr = purchase_db[0]["quantity"]

        transaction_value = price * quantity

        # Get the money from the buyer
        buyer_id = session["user_id"]
        buyer_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", buyer_id)
        buyer_cash = buyer_cash_db[0]["cash"]

        #Check if the buyer has enough money
        if buyer_cash < transaction_value*1.05:
            flash(f"Not enough funds. Your current balance is {buyer_cash}")
            return redirect(request.url)

        if quantity > quantityr or quantity < 0:
            flash(f"Only {quantityr} is available of Fruit/vegtable {fruit_v}")
            return redirect(request.url)

        # Update cash from the buyer
        uptd_cash = buyer_cash - transaction_value*1.05
        db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash, buyer_id)

        # Get cash from seller
        seller_cash = db.execute("SELECT cash FROM users WHERE id=?", seller_id)
        seller_cash = seller_cash[0]["cash"]

        # Update cash from the buyer
        uptd_cash_seller = seller_cash + transaction_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash_seller, seller_id)

        date = datetime.datetime.now()

        db.execute("INSERT INTO transactions (seller_id, buyer_id, fruit_v, quantity, package_t, price, transaction_value, type, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",  seller_id, buyer_id, fruit_v, quantity, package_t, price, transaction_value, 'sell', date)
        db.execute("INSERT INTO transactions (fruit_v, package_t, quantity, price, date, type, buyer_id, transaction_value, seller_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", fruit_v, package_t, quantity, price*1.05, date, 'buy', buyer_id, transaction_value*1.05, seller_id)
        db.execute("UPDATE availability SET fruit_v_a=?, package_a=?, quantity=?, price_a=?, user_id=?, date=?   WHERE id=?", fruit_v, package_t, quantityr - quantity, price, seller_id, date, id)

        flash("Fruits and vegtables successfully bought!")

        return redirect("/")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    role = db.execute("SELECT role FROM users WHERE id =?", user_id)

    if role[0]["role"] == 'seller':
        transactions_db = db. execute ("SELECT * FROM transactions WHERE seller_id=? AND type=?", user_id, 'sell')
        return render_template("history.html", transactions = transactions_db)
    else:
        transactions_db = db. execute ("SELECT * FROM transactions WHERE buyer_id=? AND type=?", user_id, 'buy')
        return render_template("history.html", transactions = transactions_db)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            return redirect(request.url)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        role = request.form.get("role")
        city = request.form.get("city")
        neighbourhood = request.form.get("neighbourhood")
        address = request.form.get("address")
        birthday = request.form.get("birthday")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        document = request.form.get("document")
        citizen_id = request.form.get("citizen_id")
        email = request.form.get("email")
        zip_n = request.form.get("zip_n")

        if not username:
            flash("Create an username is mandatory.")
            return redirect(request.url)

        if not password:
            flash("Create a password is mandatory")
            return redirect(request.url)
        elif len(password)<12:
            flash("Password must have more than 12 Characters")
            return redirect(request.url)
        elif password.upper()==password or password.lower()==password or password.isalnum()==password:
            flash("Password must lower-, uppercase, numbers and letters")
            return redirect(request.url)
        elif password.upper()==password and password.lower()==password or password.isalnum()==password:
            flash("Password must lower-, uppercase, numbers and letters")
            return redirect(request.url)
        elif password.upper()==password and password.lower()==password and password.isalnum()==password:
            flash("Password must lower-, uppercase, numbers and letters")
            return redirect(request.url)

        if not confirmation:
            flash("Must enter confirmation")
            return redirect(request.url)

        if not role:
            flash("Must decide a role")
            return redirect(request.url)

        if password != confirmation:
            flash("Password and confirmation password do not match")
            return redirect(request.url)

        hash = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO users (username, role, hash, city, address, neighbourhood, zip_n, email, first_name, last_name, document, citizen_id, birthday) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", username, role, hash, city, address, neighbourhood, zip_n, email, first_name, last_name, document, citizen_id, birthday)
        except:
            return apology("Could not register your account")

        session["user_id"] = new_user

        return redirect("/")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        role = db.execute("SELECT role FROM users WHERE id =?", user_id)

        if role[0]["role"] == 'seller':
            return render_template("sell.html")
        else:
            return apology("You are not allowed to sell")


    else:
        fruit_v = request.form.get("fruit_v").upper()
        package_t = request.form.get("package_t").upper()
        quantity = int(request.form.get("quantity"))
        price = float(request.form.get("price"))

        if not fruit_v:
            flash("Must enter a fruit or vegetable")
            return redirect(request.url)

        if not package_t.isalpha():
            flash("Must enter a type of package")
            return redirect(request.url)

        if quantity < 0:
            flash("Must enter a valid quantity to sell")
            return redirect(request.url)

        if not price:
            flash("Must enter the quantity to sell")
            return redirect(request.url)

        user_id = session["user_id"]

        date = datetime.datetime.now()

        db.execute("INSERT INTO availability(fruit_v_a, package_a, quantity, price_a, user_id, date) VALUES(?, ?, ?, ?, ?,?)", fruit_v, package_t, quantity, price, user_id, date)

        flash("Fruits and vegetables successfully offered!!")

        return redirect("/")

@app.route("/add_money", methods=["GET", "POST"])
@login_required
def add_money():
    """Add more money to your account"""
    if request.method == "GET":
        return render_template("add_money.html")

    else:
        more_money = int(request.form.get("more_money"))
        number = int(request.form.get("number"))

        if not more_money:
            flash("Must digit a number")
            return redirect(request.url)

        count = 0
        n = number
        while True:
            n = n//10
            count += 1
            if n == 0:
                break

        # Set the variables to 0 and n to the number card
        n = number
        first = 0
        second = 0

        # Knowing that i is the number of digts
        # let us calculate the digits
        for j in range(count):
            # Get the last digit
            digit = n % 10
            # Short the digit
            n = n // 10
            if j % 2 == 0:
                second = second + digit
            else:
                digit = digit * 2
                if digit >= 10:
                    digitone = digit % 10
                    digittwo = digit // 10
                    digit = digitone + digittwo
                first = first + digit

        # Check if the mod of the sum is 0
        if (first + second) % 10 == 0:
            if (math.floor(number // (10 ** 13)) == 34) or (math.floor(number // (10 ** 13)) == 37):
                card_is="AMEX"
            elif (math.floor(number // (10 ** 14)) == 51) or (math.floor(number // (10**14)) == 52) or (math.floor(number // (10**14)) == 53) or (math.floor(number // (10**14)) == 54) or (math.floor(number // (10**14)) == 55):
                card_is="MASTERCARD"
            elif (math.floor(number // (10 ** 12)) == 4) or (math.floor(number // (10 ** 15)) == 4):
                card_is="VISA"
            else:
                flash("Card number is invalid")
                return redirect(request.url)
        else:
            flash("Card number is invalid")
            return redirect(request.url)

        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id = user_id)
        user_cash = user_cash_db[0]["cash"]

        uptd_cash = user_cash + more_money
        db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash, user_id)

        flash(f"Succesfully added {more_money} with {card_is}")
        return redirect("/")

@app.route("/set_account", methods=["GET", "POST"])
@login_required
def set_account():
    """Register user"""
    user_id = session["user_id"]
    db_person = db.execute("SELECT * FROM users WHERE id =?", user_id)

    if request.method == "GET":
        return render_template("set_account.html", db=db_person)

    else:
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        email = request.form.get("email")

        if not first_name or not last_name or not username or not email:
            flash("ALL fields must be filled, except password and confirmation")
            return redirect(request.url)
            
        if not password:
            db.execute("UPDATE users SET username=?, email=?, first_name=?, last_name=?", username, email, first_name, last_name)
            flash("Changes successfully saved!")
            return redirect(request.url)
        elif password:

            if confirmation:

                if password != confirmation:
                    flash("Password and confirmation password do not match")
                    return redirect(request.url)
                else:
                    if len(password)<12:
                        flash("Password must have more than 12 Characters")
                        return redirect(request.url)
                    elif password.upper()==password or password.lower()==password or password.isalnum()==password:
                        flash("Password must lower-, uppercase, numbers and letters")
                        return redirect(request.url)
                    elif password.upper()==password and password.lower()==password or password.isalnum()==password:
                        flash("Password must lower-, uppercase, numbers and letters")
                        return redirect(request.url)
                    elif password.upper()==password and password.lower()==password and password.isalnum()==password:
                        flash("Password must lower-, uppercase, numbers and letters")
                        return redirect(request.url)
                    else:
                        hash = generate_password_hash(password)
                        db.execute("UPDATE users SET username=?, email=?, first_name=?, last_name=?, hash=? ", username, email, first_name, last_name, hash)
                        flash("Changes successfully saved")
                        return redirect(request.url)

@app.route("/set_address", methods=["GET", "POST"])
@login_required
def set_address():
    user_id = session["user_id"]
    db_person = db.execute("SELECT * FROM users WHERE id =?", user_id)

    if request.method == "GET":
        return render_template("set_address.html", db=db_person)

    else:
        city = request.form.get("city")
        zip_n = request.form.get("zip_n")
        address = request.form.get("address")
        neighbourhood = request.form.get("neigbourhood")

        if not city or not zip_n or not address or not neighbourhood:
            flash("All fields must be filled!")
            return redirect(request.url)

        db.execute("UPDATE users SET username=?, city=?, zip_n=?, address=?, neighbourhood=? ", city, zip_n, address, neighbourhood)