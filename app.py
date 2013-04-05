import os
import pymongo
from flask import Flask, render_template, g, request

app = Flask(__name__)
MONGO_URI = os.environ.get("MONGO_URI", "localhost:27017")
MONGO_USER = os.environ.get("MONGO_USER", "")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", "")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME", "test")


@app.route("/")
def index():
    return render_template("index.html"), 200


@app.route("/confirmation")
def confirmation():
    return render_template("confirmation.html"), 200


@app.route("/login/facebook", methods=["POST"])
def facebook_login():
    if not is_login_valid(request.form):
        return "Missing required fields for login.", 400
    user = {"first_name": request.form["first_name"],
            "last_name": request.form["last_name"]}
    g.db.users.insert(user)
    return "", 201


def is_login_valid(form):
    if "first_name" not in form.keys() or "last_name" not in form.keys():
        return False
    if not form["first_name"] or form["first_name"] == "" or not form["last_name"] \
       or form["last_name"] == "":
        return False
    return True


@app.before_request
def before_request():
    g.conn, g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    g.conn.close()


def connect_db():
    mongo_uri_port = MONGO_URI.split(":")
    host = mongo_uri_port[0]
    port = int(mongo_uri_port[1])
    conn = pymongo.Connection(host, port)
    return conn, conn[MONGO_DATABASE_NAME]


if __name__ == "__main__":
    app.run()
