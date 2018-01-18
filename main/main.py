import utils.auth as auth
import utils.lockers as lockers
import utils.offers as offers

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
        if request.form["form"] == "login":
            if add_session(email, password):
                return redirect(url_for("root"))
        else:
            if(password != request.form["confirm_password"]):
                flash("Passwords did not match")
            elif not auth.create_account(email, password):
                flash("Invalid Email: must be unique @stuy.edu email")
            else:
                flash("account creation successful")
    return render_template("login.html")

@app.route("/logout")
def logout():
    if is_logged():
        session.pop(USER_SESSION)
    return redirect(url_for("login"))

@app.route("/offers")
def offer():
    return render_template("offers.html", offers = offers.get_all_offers(), logged = is_logged())

@app.route("/display")
def display():
    if "lockerID" in request.args and "type" in request.args:
        return render_template("display.html", offer = offers.get_offer(request.args.get("lockerID"),int(request.args.get("type"))))
    else:
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
    if request.method == "GET":
        return render_template("profile.html", logged = is_logged(), username = session[USER_SESSION], lockers = lockers.get_lockers(session[USER_SESSION]))
    elif request.method == "POST":
        locker = {"lockerID": request.form["lockerID"], "email": session[USER_SESSION], "floor": request.form["floor"], "coords": request.form["coords"]}
        if lockers.create_locker(locker["lockerID"], locker["email"], int(locker["floor"]), locker["coords"]):
            return render_template("profile.html", logged = is_logged(), username = session[USER_SESSION], lockers = lockers.get_lockers(session[USER_SESSION]))
            
if __name__ == "__main__":
    app.debug = True
    app.run()
