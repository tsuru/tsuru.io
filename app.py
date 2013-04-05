# Copyright 2013 Globo.com. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import requests
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


@app.route("/register/facebook", methods=["POST"])
def facebook_register():
    if not has_token(request.form):
        return "Could not obtain access token from facebook.", 400
    url = "https://graph.facebook.com/me?fields=first_name,last_name,email&access_token={0}".format(request.form["access_token"])
    response = requests.get(url)
    info = response.json()
    user = {"first_name": info["first_name"],
            "last_name": info["last_name"],
            "email": info["email"]}
    g.db.users.insert(user)
    return "", 201


def has_token(form):
    if "access_token" not in form.keys():
        return False
    if not form["access_token"] or form["access_token"] == "":
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
