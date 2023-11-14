# CS50 FINAL PROJECT

## FRUVI Market
created by Mario Salazar

#### **Files**

1. flask_session
2. static
    - favicon.ico
    - styles.css
3. templates
    - add_money.html
    - apology.html
    - buy.html
    - history.html
    - index.html
    - layout.html
    - login.html
    - register.html
    - sell.html
    - set_account.html
    - set_address.html
- app.py
- helpers.py
- project.db
- README.md
- requirements.txt

---
---

### __Project.db__

In this project I want to be the nearest possible to how a commerce platform works, that's why not just normal information like name, usernam and password have been saved. It is also important to save the email, so that it can be communicated to the user the state of the shipping or if something must be notified. The residence information like city, address, zip and neighbourhood is saved for shipping purposes. And finally the legal information and birthday in case the person does something against the law.

        CREATE TABLE users(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                username TEXT NOT NULL,
                role TEXT NOT NULL,
                hash TEXT NOT NULL,
                city TEXT NOT NULL,
                address TEXT NOT NULL,
                neighbourhood TEXT NOT NULL,
                zip_n INTEGER,
                email VARCHAR,
                birthday DATE,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                document TEXT NOT NULL,
                citizen_id TEXT NOT NULL,
                cash NUMERIC DEFAULT 0);

In this table will be collected all the information about the available products to sell, if no farmer offer their products, then no product will be offered. The table has an id, an user id which will conect the available product with the seller. This allows to pay to the right when the product is sold. fruit_v_a is the name of the fruit or the vegetable, package_a is the type of package used, quantity is the number of products to sell, price_a is the price in which each product is going to be sold and the date the product was offered.

        CREATE TABLE availability (
            id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
            user_id INTEGER,
            fruit_v_a TEXT,
            package_a TEXT,
            quantity INTEGER,
            price_a TEXT
            transaction_id INTEGER,
            date TIMESTAMP
            );

Every time a user buys something, a transaction will be registered in 2 ways, one for the person who is selling, which will get the price to which he sells, and for the buyer the transaction value is going to be 5% more, because that's the fee he has to pay for buying in our platform.

        CREATE TABLE transactions (
            id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
            seller_id INTEGER,
            buyer_id INTEGER,
            fruit_v TEXT,
            quantity INTEGER,
            package_t TEXT,
            price REAL,
            transaction_value REAL,
            type TEXT,
            date TIMESTAMP);

---
---

### __Explaining each folder__

#### __flask_session__
For good information about flask session which is relatted to cookies. We recommend you to visit [flask session](https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/)

#### __static__

##### __favicon.ico__
![Icon for header](/project/static/favicon.ico)

This is the Icon used for the header of the webpage.
##### __styles.css__
Here are all the styles that were manually created.

---

#### __templates__

##### __add_money.html__
```html
<input type="numeric" id="number" class="form-control form-control-lg active" siez="17" name="number" minlength="12" maxlength="19">
<input autocomplete="off" autofocus class="form-control mx-auto w-auto" name="more_money" placeholder="Add money" type="number">
```
Thanks to whis 2 inputs the app.py decides whether is valid to add money to the account or not. How does it do it? As we can see in the inputs, the names are <em>number</em> and <em>more_money</em>. The app.py requests these variables in the following way:

```python
more_money = int(request.form.get("more_money"))
number = int(request.form.get("number"))
```
After this, the code checks if the value to add is different to an empty variable, if it detects that the variable is empty, it will redirect the user back to the page with a flash (message) saying that there must be a value to add

```python
if not more_money:
    flash("Must digit a number")
    return redirect(request.url)
```

Then the number is processed, the first step is knowing how many digits does the card have, and classifying depending on whether is an odd position digit or not. The for loop goes until the total of the digits of the card is reached another statement could be <code> for j in len(number):</code>

If the digit is in an odd position, the digit is just taken as it is and added to the sum of all the odd position numbers. But if not, the digit is multiplied by 2 and if the result is greater than 10, each digit is added to the variable of not odd position numbers. For example if the not odd position number is 6, it is multiplied by 2, instead of adding 12 to the variable, 1+2 is added.
```python
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
```

Once all the digits were added, we must get the mod, if the mod is 0, then it could be a valid card, the first two digits are, 34 or 37, it is an American Express. If the first 2 digits are 51 to 55, the card is MASTERCARD. And if the first digit is 4, it is VISA.

```python
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
```

IF the card is invalid, the page will reload saying that the card namber is invalid. If valid, a string will be saved containing which card it is. After validating the card, the amount of money will be added to the user. After the money is added, a message will appear saying that the transaction was succesfully made, saying the amount of mony and the card used.

```python
user_id = session["user_id"]
    user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id = user_id)
    user_cash = user_cash_db[0]["cash"]

    uptd_cash = user_cash + more_money
    db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash, user_id)

    flash(f"Succesfully added {more_money} with {card_is}")
    return redirect("/")
```

---

##### __apology.html__
This page, will show a cat's image and a message, for asking Flask to use it, will be in the following way.

``` python
return apology("You are not allowed to buy")
```

The html code is

```html
<!-- https://memegen.link/ -->
<img alt="{{ top }}" class="border img-fluid" src="http://memegen.link/custom/{{ top | urlencode }}/{{ bottom | urlencode }}.jpg?alt=https://i.imgur.com/CsCgN7Ll.png&width=400" title="{{ top }}">
```

---

##### __buy.html__

In this page all the available vegetables are going to be shown, first the code is going to get the database of the available fruits and vegetables and all the information. After this, it is going to send it to the html code by the render_template function. And it will only allow to do this transaction if a user is a buyer.

````python
if request.method == "GET":
        user_id = session["user_id"]
        role = db.execute("SELECT role FROM users WHERE id =?", user_id)
        available_db = db.execute("SELECT * FROM availability WHERE quantity > 0")
    if role[0]["role"] == 'buyer':
                return render_template("buy.html", available = available_db)
            else:
                return apology("You are not allowed to buy")
````

When directed to the buy page, a table with appear with the information of the available fruits and vegetables. To know what the user wants to buy, the name of the submit button is dinamically assigned depending on the id of the available fruit or vegetable, as well as the desired quantity to buy <code>quantity{{ row["id"] }}</code>.

<!DOCTYPE html>
<html lang="en">
<head><title>none</title></head>
<table>
    <thead>
        <tr>
        <th>Id</th>
        <th>Fruit/vegetable</th>
        <th>Package</th>
        <th>Quantity available</th>
        <th>Price/unity</th>
        <th>Quantity order</th>
        <th></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>row["id"]</td>
            <td>row["fruit_v_a"]</td>
            <td>row["package_a"]</td>
            <td>row["quantity"]</td>
            <td>row["price_a"] * 1.05</td>
            <td><input></td>
            <td><button>Buy</button></td>
        </tr>
    </tbody>
</table>
</html>

The id and the quantity to buy will be requested in the following way.
````python
id = request.form.get("id")
quantity = int(request.form.get(f"quantity{id}"))
````
Once the id is gotten, a SQL statment will be executed to get the data from the available fruits.
````python
purchase_db = db.execute("SELECT * FROM availability WHERE id=?", id)
print(purchase_db)
fruit_v = purchase_db[0]["fruit_v_a"]
package_t = purchase_db[0]["package_a"]
price = float(purchase_db[0]["price_a"])
seller_id = purchase_db[0]["user_id"]
quantityr = purchase_db[0]["quantity"]
````
Then it will ask the database if the user has enough funds to buy the requested item. And althought in the HTML code there is limit to the maximum quantity available, the code can be manipulated. Thus there is an if statement to check if the user has typed a valid number. The buyer must pay a fee of 5% additional, which supposes that would be a fee for the platform

````python
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
````
If the buyer has enough funds, the money will be taken from the buyer and transfered to the seller
````python
# Update cash from the buyer
uptd_cash = buyer_cash - transaction_value*1.05
db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash, buyer_id)

# Get cash from seller
seller_cash = db.execute("SELECT cash FROM users WHERE id=?", seller_id)
seller_cash = seller_cash[0]["cash"]

# Update cash from the buyer
uptd_cash_seller = seller_cash + transaction_value
db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash_seller, seller_id)
````
After transfering the money from the buyer to the seller, the database transactions must register the purchase and the availability must be updated.

````python
date = datetime.datetime.now()

db.execute("INSERT INTO transactions (seller_id, buyer_id, fruit_v, quantity, package_t, price, transaction_value, type, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",  seller_id, buyer_id, fruit_v, quantity, package_t, price, transaction_value, 'sell', date)
db.execute("INSERT INTO transactions (fruit_v, package_t, quantity, price, date, type, buyer_id, transaction_value, seller_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", fruit_v, package_t, quantity, price*1.05, date, 'buy', buyer_id, transaction_value*1.05, seller_id)
db.execute("UPDATE availability SET fruit_v_a=?, package_a=?, quantity=?, price_a=?, user_id=?, date=?   WHERE id=?", fruit_v, package_t, quantityr - quantity, price, seller_id, date, id)

flash("Fruits and vegtables successfully bought!")

return redirect("/")
````

---

##### __history.html__

This page is not interactive, is only for showing purposes, first it will get the user id. Depending on the role of the user, the transaction is going to be shown. Knowing that the transaction value for the buyer is 5% greater, because is the supposed fee for the platform.
````python
user_id = session["user_id"]
role = db.execute("SELECT role FROM users WHERE id =?", user_id)

if role[0]["role"] == 'seller':
    transactions_db = db. execute ("SELECT * FROM transactions WHERE seller_id=? AND type=?", user_id, 'sell')
    return render_template("history.html", transactions = transactions_db)
else:
    transactions_db = db. execute ("SELECT * FROM transactions WHERE buyer_id=? AND type=?", user_id, 'buy')
    return render_template("history.html", transactions = transactions_db)
````

once the information is redirected to the HTML a table with the information of the transactions of the user wil be shown.

<!DOCTYPE html>
<html lang="en">
<head><title>none</title></head>
<table>
    <thead>
        <tr>
            <th scope="col">id</th>
            <th scope="col">Fruit/Vegetable</th>
            <th scope="col">Quantity</th>
            <th scope="col">Package</th>
            <th scope="col">Price</th>
            <th scope="col">Transaction Value</th>
            <th scope="col">Type</th>
            <th scope="col">Date</th>
            <th scope="col">Seller id</th>
            <th scope="col">Buyer id</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>row["id"]</td>
            <td>row["fruit_v"]</td>
            <td>row["quantity"]</td>
            <td>row["package_t"]</td>
            <td>row["price"]</td>
            <td>row["transaction_value"]</td>
            <td>row["type"]</td>
            <td>row["date"]</td>
            <td>row["seller_id"]</td>
            <td>row["buyer_id"]</td>
        </tr>
    </tbody>
</table>
</html>

---

##### __index.html__
In the index page, the name of the user will be shown and the amount of money that has available. After this, there will be an image of a farmer doing agricultural work, and then the some information.

To show the name and the amount of money that the user has available, first the information must be requested to the database and redirected to the html.

````python
user_id = session["user_id"]

info = db.execute("SELECT * FROM users WHERE id =?", user_id)
cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
cash = cash_db[0]["cash"]

return render_template("index.html", info = info, cash = cash)
````
Depending on wether the role of the user is buyer or seller, the message displayed will a different for each one.
````html
{% if info[0]["role"] == 'buyer' %}
        <h2 align="right">Hello <strong>{{ info[0]["first_name"] }}</strong> </h2>
        <h3 align="right">How may we help you?</h3>
        <h4 align="left"> Your current balance is: <strong class="text-success">{{cash}}</h4>
    {% else %}
        <h2 align="right">Hello <strong>{{ info[0]["first_name"] }}</strong> </h2>
        <h3 align="right">What do you want to sell today?</h3>
        <h4 align="left"> Your current balance is: <strong class="text-success">{{cash}}</h4>
    {% endif %}
    <div class="container-fluid mb-3 mw-3">
        <img src="https://i0.wp.com/www.lacoladerata.co/wp-content/uploads/2022/01/El-Convite-Campesino-en-Boyaca.jpg?fit=1920%2C1080&ssl=1" alt="..." style="height: auto; max-width: 100%;">
    </div>

    <p>
        <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#Collapse1" aria-expanded="false" aria-controls="Collapse1">
            Why to trade with FRUVI?
        </button>
        <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#Collapse2" aria-expanded="false" aria-controls="Collapse2">
            Tips
        </button>
    </p>
    <div class="row">
        <div class="col">
          <div class="collapse multi-collapse" id="Collapse1">
            <div class="card card-body border-success text-black" font color="black">
              Our providers offer fruits and vegetables of the best quality. Besides that, we offer a good logistic service, in our platform you can always check where your order is.
            </div>
          </div>
        </div>
        <div class="col">
          <div class="collapse multi-collapse" id="Collapse2">
            <div class="card card-body border-warning text-black">
              Always check the actual prices in the market. If something has happened, contact us immediately, sure we will help you to solve as quickly as possible.
            </div>
          </div>
        </div>
      </div>
````

---

##### __layout.html__
The layout will change depending on whether the user is already logged in or not, if it is not logged in, the navegation bar will display options for logging in or to register.
````html
{% else %}
    <ul class="navbar-nav ms-auto mt-2">
        <li class="nav-item"><a class="nav-link" href="/register">Register</a></li>
        <li class="nav-item"><a class="nav-link" href="/login">Log In</a></li>
    </ul>
{% endif %}
````
If instead the user is already logged in, the following navegation bar is going to be shown:
````html
{% if session["user_id"] %}
    <ul class="navbar-nav me-auto mt-2">
        <li class="nav-item"><a class="nav-link" href="/buy">Buy</a></li>
        <li class="nav-item"><a class="nav-link" href="/sell">Sell</a></li>
        <li class="nav-item"><a class="nav-link" href="/history">History</a></li>
        <li class="nav-item"><a class="nav-link" href="/add_money">Add money</a></li>
    </ul>
    <ul class="navbar-nav ms-auto mt-2">
        <div class="dropdown dropstart">
            <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                Options
            </button>
            <ul class="dropdown-menu container-fluid">
                <li class="nav-item"><a class="nav-link" href="/set_account">Account settings</a></li>
                <li class="nav-item"><a class="nav-link" href="/set_address">Change address</a></li>
                <li class="nav-item"><a class="nav-link" href="/logout">Log Out</a></li>
            </ul>
            </div>
    </ul>
````

---

##### __login.html__
This template is going to have two inputs, the first is the username, an the second is the password.
<!DOCTYPE html>
<html lang="en">
<head><title>none</title></head>
<form>
    <div class="mb-3">
        <input autocomplete="off" autofocus class="form-control mx-auto w-auto" id="username" name="username" placeholder="Username" type="text">
    </div>
    <div class="mb-3">
        <input class="form-control mx-auto w-auto" id="password" name="password" placeholder="Password" type="password">
    </div>
    <button class="btn btn-primary" type="submit">Log In</button>
</form>
</html>

After submitting this information, the code will check if the a username or password was typed in.
````python
# User reached route via POST (as by submitting a form via POST)
if request.method == "POST":

# Ensure username was submitted
if not request.form.get("username"):
    flash("must provide username")
    return redirect(request.url)

# Ensure password was submitted
elif not request.form.get("password"):
    return apology("must provide password", 403)
````
If the user has provided the requested data, it will be checked in the database if the submited information is valid.
````python
# Query database for username
rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

# Ensure username exists and password is correct
if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
    return apology("invalid username and/or password", 403)

# Remember which user has logged in
session["user_id"] = rows[0]["id"]

# Redirect user to home page
return redirect("/")
````
If the information is valid, it will redirect the user to index.html, else will redirect to the login page again.

---

##### __register.html__

In the register page, there will be a form that will ask some information to the user, which will be needed to acces the platform.

<form action="/register" method="post">
    <h2>Personal Information</h2>
            <div class="col mb-3">
                <label for="validationServer05" class="form-label"><strong>First name</strong></label>
                <input type="text" class="form-control mx-auto w-auto" autofocus placeholder="First name" aria-label="First name" name="first_name" required>
            </div>
            <div class="col mb-3">
                <label for="validationServer05" class="form-label"><strong>Last name</strong></label>
                <input type="text" class="form-control mx-auto w-auto" placeholder="Last name" aria-label="Last name" name="last_name" required>
            </div>
            <div class="col mb-3">
                <label for="validationServer05" class="form-label"><strong>Username</strong></label>
                <input autocomplete="off" class="form-control mx-auto w-auto" id="username" name="username" placeholder="Username" type="text" aria-describedby="inputGroupPrepend3" required>
            </div>
            <div class="col mb-3">
                <label for="validationServer05" class="form-label"><strong>Password</strong></label>
                <input class="form-control mx-auto w-auto" id="password" name="password" placeholder="Password" type="password" required>
            </div>
            <div class="col mb-3">
                <label for="validationServer05" class="form-label"><strong>Confirm Password</strong></label>
                <input class="form-control mx-auto w-auto" id="confirmation" name="confirmation" type="password" required>
            </div>
            <div class="col mb-3">
                <label for="validationServer05" class="form-label"><strong>E-mail</strong></label>
                <input class="form-control mx-auto w-auto" id="email" name="email" type="text" placeholder="e-mail" required>
            </div>
            <div class="col mb-3">
                <label><strong>Role</strong></label>
                <select class="form-select mx-auto w-auto" aria-label="Default select example" name="role" required>
                    <option selected><strong>Select your role</strong></option>
                    <option value="seller">Seller</option>
                    <option value="buyer">Buyer</option>
                </select>
            </div>
            <div class="col mb-3">
                <label for="validationServer05" class="form-label"><strong>Birthday (MM/DD/YYYY)</strong></label>
                <input class="form-control mx-auto w-auto" type="text" id="datepicker" placeholder="Birthday (MM/DD/YYYY)" name="birthday" required>
            </div>
        <h2>Residence Information</h2>
            <div class="col mb-3">
                <label for="validationServer05" class="form-label"><strong>City</strong></label>
                <input type="text" class="form-control mx-auto w-auto" name="city" placeholder="City" required>
            </div>
            <div class="col mb-3">
                <label for="validationServer05" class="form-label"><strong>Address</strong></label>
                <input type="text" class="form-control mx-auto w-auto" name="address" placeholder="Address" required>
            </div>
            <div class="col mb-3">
                <label for="validationServer05" class="form-label"><strong>Neighbourhood</strong></label>
                <input type="text" class="form-control mx-auto w-auto" name="neighbourhood" placeholder="Neighbourhood" required>
            </div>
            <div class="col mb-3">
                <label for="validationServer05" class="form-label"><strong>Zip</strong></label>
                <input type="text" class="form-control mx-auto w-auto" name="zip_n" placeholder="Zip" required>
            </div>
        <h2>Legal Information</h2>
            <div class="col mb-3">
                <label for="validationServer05" class="form-label"><strong>ID type</strong></label>
                <select class="form-select mx-auto w-auto" aria-label="Default select example" name="document" required>
                    <option selected>Select your ID type</option>
                    <option value="document">Document</option>
                    <option value="passport">Passport</option>
                </select>
            </div>
            <div class="col mb-3">
                <label for="validationServer05" class="form-label"><strong>ID number</strong></label>
                <input class="form-control mx-auto w-auto" type="text" placeholder="ID number" name="citizen_id">
            </div>
</form>
<button>Register</button>
<p> </p>

When the information is already submited, the flask code will check whether the information is valid and if the text is not empty. The first step is to get all the information from the form:

```python
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
```
After getting al the information, it will check that some inputs were not empty
```python
if not username:
    flash("Create an username is mandatory.")
    return redirect(request.url)

    if not password:
    flash("Create a password is mandatory")
    return redirect(request.url)

if not confirmation:
    flash("Must enter confirmation")
    return redirect(request.url)

if not role:
    flash("Must decide a role")
    return redirect(request.url)
```

Then it will check whether the password is strong or not, the first statement is to check if the password is greater than 12 characters, and the following statements check if the password has upper-, lowercase and numbers. Finally it checks whether the password is equal to the confirmation.

```python
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
if password != confirmation:
    flash("Password and confirmation password do not match")
    return redirect(request.url)

```

If the statements are True, then there must be generated a hash

```python
hash = generate_password_hash(password)
```
And finally, the information must be insert into the databases and log in.

```python
try:
    new_user = db.execute("INSERT INTO users (username, role, hash, city, address, neighbourhood, zip_n, email, first_name, last_name, document, citizen_id, birthday) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", username, role, hash, city, address, neighbourhood, zip_n, email, first_name, last_name, document, citizen_id, birthday)
    except:
    return apology("Could not register your account")

    session["user_id"] = new_user

    return redirect("/")
```

---

##### __sell.html__
The actual page consist of a formular, where the seller is going to fill the information about which product is going to sell, how it is going to be packed, to which price and the available quantity to sell.
<div>
    <label><strong>Fruit or vegtable</strong></label>
    <input>
</div>
<div>
    <label><strong>Type of package</strong></label>
    <input placeholder="Package">
</div>
<div>
    <label><strong>Quantity</strong></label>
    <input placeholder="Quantity">
</div>
<div>
    <label><strong>Price</strong></label>
    <input placeholder="Price">
</div>
<button>Sell</button>
<p></p>

Before displaying the webpage, the code will check whether the role of the person is buyer or seller. If the user is a seller, will be allowed to do the transaction, otherwise will show an apology template.
```python
if request.method == "GET":
    user_id = session["user_id"]
    role = db.execute("SELECT role FROM users WHERE id =?", user_id)

    if role[0]["role"] == 'seller':
        return render_template("sell.html")
    else:
        return apology("You are not allowed to sell")
```
After showing the page and the user has submitted the information, it will be saved in the database availability. But the seller, will only get the money, when a users buys their product. It means that the collected data in the form won't be submitted to a transaction.

```python
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
```

---

##### __set_account.html__

If the user wants to change some information, it will be possible,the only data that cannot be changed is the role, birthday and legal information. First, app.py must get the information of the user to display it on the screen.
```python
user_id = session["user_id"]
    db_person = db.execute("SELECT * FROM users WHERE id =?", user_id)

    if request.method == "GET":
        return render_template("set_account.html", db=db_person)
```
After getting the information about the user and send it the html file, the user can change the information they want by filling each box. The way to fill the information automatically in the page was by using <code>VALUE</code> and the variable <code>db</code>, here is an example of displaying the user's name <code>db[0]["first_name"]</code>.

If the user does not type anything, the new data in the database is going to be updated as something empty. If the user does not type anything in the password box, the password won't be neither cheked nor changed.
```python
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
```

But if a new password is typed in, then the code will check whether the new password is safe or not, then hash it and then updating the database.
```python
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
```

---

##### __set_address.html__
The last file is for changing the residence information, it works as the set_account, first it will get the information from the user and display it on the screen. Once the user has typed in the new information, the app.py code will be executed and update the database.
```python
city = request.form.get("city")
zip_n = request.form.get("zip_n")
address = request.form.get("address")
neighbourhood = request.form.get("neigbourhood")

if not city or not zip_n or not address or not neighbourhood:
    flash("All fields must be filled!")
    return redirect(request.url)

db.execute("UPDATE users SET username=?, city=?, zip_n=?, address=?, neighbourhood=? ", city, zip_n, address, neighbourhood)
```