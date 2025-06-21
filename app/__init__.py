import os

from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="Jia Xuan Li", url=os.getenv("URL"))
