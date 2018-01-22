import utils.auth as auth
import utils.lockers as lockers
import utils.offers as offers
import utils.trades as trades

from flask import Flask, redirect, url_for, render_template, session, request, flash
import requests, os, time, json

USER_SESSION = "logged_in"

app = Flask(__name__)
app.secret_key = os.urandom(64)

def is_null(username, password, confpw):
    return username == "" or password == "" or confpw == ""

def is_logged():
    return USER_SESSION in session

def add_session(username, password):
    if is_null(username, password, "filler"):
        flash("Username or password is blank")
        return False
    if(auth.login(username, password)):
        session[USER_SESSION] = username
        return True
    else:
        flash("Incorrect login credentials")
        return False

@app.route("/", methods=["GET"])
def root():
    return render_template('home.html', logged = is_logged(), lockers_selling = offers.get_latest_offers(4,0), lockers_trading = offers.get_latest_offers(4,1))

@app.route("/login", methods=["GET", "POST"])
def login():
    if is_logged():
        return redirect(url_for("root"))
    elif (request.method == "GET"):
        return render_template("login.html")
    else:
        email = request.form["email"]
        password = request.form["password"]
        if request.form["form"] == "Login":
            if add_session(email, password):
                return redirect(url_for("root"))
        else:
            if(password != request.form["confirm_password"]):
                flash("Oops! Your Password and Confirm Password did not match. :(")
            elif not auth.create_account(email, password):
                flash("Invalid Email Address: It must be a  @stuy.edu email address that has not been previously registered.")
            else:
                flash("Congratulations! You have created an account successfully. :)")
    return render_template("login.html")

@app.route("/logout")
def logout():
    if is_logged():
        session.pop(USER_SESSION)
    return redirect(url_for("login"))

@app.route("/offers")
def offer():
    return render_template("offers.html", offers = offers.get_all_offers(), logged = is_logged())

@app.route("/display", methods=["GET", "POST"])
def display():
    if "lockerID" in request.args and "type" in request.args:
        if request.method == "POST":
            if request.form["your_lockerID"] != "":
                lockerID = request.args.get("lockerID")
                to_email = lockers.get_email(lockerID)
                if to_email != session[USER_SESSION]:
                    if trades.create_trade(lockerID, request.form["your_lockerID"], to_email, session[USER_SESSION]):
                        print "Trade Request Sent"
                        flash("Trade request sent")
                    else:
                        print "Error: Request exists!"
                        flash("Error sending trade request: Request exists!")
                else:
                    print "Error: This is your offer!"
                    flash("Error sending trade request: This is your offer!")
            else:
                print "No locker selected"
                flash("Please select a locker to trade")
        if is_logged():
            return render_template("display.html", offer = offers.get_offer(request.args.get("lockerID"),int(request.args.get("type"))), logged = is_logged(), current_user_email = session[USER_SESSION])
        
        return render_template("display.html", offer = offers.get_offer(request.args.get("lockerID"),int(request.args.get("type"))), logged = is_logged())
    else:
        return redirect(url_for("offer"))

@app.route("/edit", methods=["POST"])
def edit():
    if request.method == "POST":
        lockerID = request.form["lockerID"]
        type = request.form["type"]
        price = request.form["price"]
        description = request.form["description"]
        if "update" in request.form:
            print "Update offer"
            offers.set_price(lockerID, int(type), int(price))
            offers.set_type(lockerID, int(type), int(request.form["new_type"]))
            offers.set_description(lockerID, int(type), description)
            offers.set_lockerID(lockerID, int(type), request.form["new_lockerID"])
        elif "delete" in request.form:
            print "Delete Offer"
            offers.remove_offer(lockerID, int(type))
        else:
            dict = {"lockerID": request.form["lockerID"], "price": request.form["price"], "type": request.form["type"], "description": request.form["description"]}
            return render_template("edit.html", offer = dict, logged = is_logged())
    return redirect(url_for("offer"))

@app.route("/post", methods=["GET", "POST"])
def post():
    if not is_logged():
        return redirect(url_for("login"))
    if request.method == "GET":
        return render_template("post.html", logged = is_logged())
    else:
        offers.create_offer(request.form["lockerID"], int(request.form["type"]), int(request.form["price"]), request.form["desc"])
        return redirect(url_for("offer"))

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not is_logged():
        return redirect(url_for("login"))
    if request.method == "POST":
        if "accept" in request.form:
            print "Accept request"
            trades.accept_trade(request.form["lockerID"], request.form["your_lockerID"], request.form["to_email"], request.form["from_email"])
        elif "deny" in request.form:
            print "Deny request"
            trades.remove_trade(request.form["lockerID"], request.form["your_lockerID"], request.form["to_email"], request.form["from_email"])
        elif "delete" in request.form:
            print "Delete locker"
            lockers.remove_locker(request.form["lockerID"])
            offers.remove_offer(request.form["lockerID"], 0)
            offers.remove_offer(request.form["lockerID"], 1)              
        else:
            locker = {"lockerID": request.form["lockerID"], "email": session[USER_SESSION], "floor": request.form["floor"], "coords": request.form["coords"]}
            if lockers.create_locker(locker["lockerID"], locker["email"], int(locker["floor"]), locker["coords"]):
                return render_template("profile.html", logged = is_logged(), username = session[USER_SESSION], lockers = lockers.get_lockers(session[USER_SESSION]), trades = trades.get_your_trades(session[USER_SESSION]))
            else:
                flash("Locker exists")
    return render_template("profile.html", logged = is_logged(), username = session[USER_SESSION], lockers = lockers.get_lockers(session[USER_SESSION]), trades = trades.get_your_trades(session[USER_SESSION]))

if __name__ == "__main__":
    app.debug = True
    app.run()
