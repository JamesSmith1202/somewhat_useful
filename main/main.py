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
    
if __name__ == "__main__":
    app.debug = True
    app.run()
