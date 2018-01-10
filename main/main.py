from utils.auth import *
from utils.lockers import *
from utils.offers import *

from flask import Flask, redirect, url_for, render_template, session, request, flash
import requests, os, time, json

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
    if(auth.login(username, password)):#if credentials match up in the db...
            session[USER_SESSION] = username
            return True
    else:
        flash("Incorrect login credentials")
        return False

@app.route("/", methods=["GET"])
def root():
    return render_template('home.html', logged = is_logged())
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if is_logged():
        return redirect(url_for("root"))
    elif (request.method == "GET"):
        return render_template("login.html")
    else:
        email = request.form["email"]
        password = request.form["password"]
        if "login" in request.form:
            if add_session(email, password):
                return redirect(url_for("root"))
            else:
                if not signup(email, password, request.form["confirm_password"]):
                    flash("Invalid Email: must be @stuy.edu email")
    return render_template("login.html")

@app.route("/logout")
def logout():
    if is_logged():
		session.pop(USER_SESSION)
    return redirect(url_for("login"))

@app.route("/offers")
def offers():
    return render_template("offers.html", offers = offer.get_all_offers(), logged = is_logged())

@app.route("/display")
def display():
    if id in request.args:
        return render_template("display", offer = get_offer(request.args.get("id")))
    else:
        return redirect(url_for("offers"))

@app.route("/post", methods=["GET", "POST"])
def post():
    if not is_logged():
        return redirect(url_for("login"))
    if request.method == "GET":
        return render_template("post.html", logged = is_logged())
    else:
        create_offer(request.form["lockerID"], request.form["type"], request.form["price"], request.form["desc"])
        return redirect(url_for("profile"))

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not is_logged():
        return redirect(url_for("login"))
    if method.request == "GET":
        locker_list = get_lockers(session[USER_SESSION])
        return render_template("profile.html", logged = is_logged(), 

if __name__ == "__main__":
    app.debug = True
    app.run()
