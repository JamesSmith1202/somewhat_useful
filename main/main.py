from utils.auth import *
from utils.lockers import *
from utils.offers import *

from flask import Flask, redirect, url_for, render_template, session, request, flash
import requests, os, time, json

app = Flask(__name__)
app.secret_key = os.urandom(64)

@app.route("/", methods=["GET"])
def root():
    return render_template('home.html')


USER_SESSION = "logged_in"

app = Flask(__name__)
app.secret_key = os.urandom(16)

def is_null(username, password, confpw):
    return username == "" or password == "" or confpw == ""

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
@app.route("/")
def root():
    return render_template("home.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if USER_SESSION in session:
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
                if not signup(email, password, request.form["confirm_password"]:
                    flash("Invalid Email: must be @stuy.edu email")
    return render_template("login.html")

@app.route("/logout")
def logout():
    if USER_SESSION in session:
		session.pop(USER_SESSION)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.debug = True
    app.run()
