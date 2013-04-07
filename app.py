# Copyright 2013 Globo.com. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import hashlib
import os

import pymongo
import requests

from flask import Flask, render_template, g, request

app = Flask(__name__)
MONGO_URI = os.environ.get("MONGO_URI", "localhost:27017")
MONGO_USER = os.environ.get("MONGO_USER", "")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", "")
MONGO_DATABASE_NAME = os.environ.get("MONGO_DATABASE_NAME", "test")
GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET", "")
FACEBOOK_APP_ID = os.environ.get("FACEBOOK_APP_ID", "")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
GOOGLE_USER_IP = os.environ.get("GOOGLE_USER_IP")
GOOGLE_OAUTH_ENDPOINT = os.environ.get("GOOGLE_OAUTH_ENDPOINT", "https://www.googleapis.com/oauth2/v2")
SIGN_KEY = os.environ.get("SIGN_KEY")


def sign(email):
    h = hashlib.sha1(email)
    h.update(SIGN_KEY)
    return h.hexdigest()


@app.route("/")
def index():
    return render_template("index.html", facebook_app_id=FACEBOOK_APP_ID,
                           github_client_id=GITHUB_CLIENT_ID), 200


@app.route("/confirmation")
def confirmation():
    return render_template("confirmation.html"), 200


@app.route("/software")
def software():
    return render_template("software.html"), 200


@app.route("/community")
def community():
    return render_template("community.html"), 200


@app.route("/register/facebook")
def facebook_register():
    if not has_token(request.args):
        return "Could not obtain access token from facebook.", 400
    url = "https://graph.facebook.com/me?fields=first_name,last_name,email&access_token={0}"
    url = url.format(request.args["access_token"])
    response = requests.get(url)
    info = response.json()
    user = {"first_name": info["first_name"],
            "last_name": info["last_name"],
            "email": info["email"]}
    g.db.users.insert(user)
    return render_template("confirmation.html", email=info["email"], signature=sign(info["email"]))


@app.route("/register/github")
def github_register():
    code = request.args.get("code")
    if code is None:
        return "Could not obtain code access to github.", 400
    data = "client_id={0}&code={1}&client_secret={2}".format(GITHUB_CLIENT_ID, code, GITHUB_CLIENT_SECRET)
    headers = {"Accept": "application/json"}
    url = "https://github.com/login/oauth/access_token"
    response = requests.post(url, data=data, headers=headers)
    token = response.json().get("access_token")
    if token is None or token == "":  # test me
        return "Could not obtain access token from github.", 400
    url = "https://api.github.com/user?access_token={0}".format(token)
    response = requests.get(url, headers=headers)
    info = response.json()
    first_name, last_name = parse_github_name(info)
    user = {"first_name": first_name,
            "last_name": last_name,
            "email": info["email"]}
    g.db.users.insert(user)
    return render_template("confirmation.html", email=info["email"], signature=sign(info["email"]))


def parse_github_name(info):
    splitted = info["name"].split(" ")
    if len(splitted) > 1:
        return splitted[0], splitted[-1]
    return splitted[0], ""


@app.route("/register/gplus", methods=["GET"])
def gplus_register():
    token = request.args.get("token")
    token_type = request.args.get("token_type")
    if token is None or token_type is None:
        return "Token is required.", 400
    headers = {"Authorization": "%s %s" % (token_type, token)}
    url = "%s/userinfo?key=%s&userIp=%s" % (GOOGLE_OAUTH_ENDPOINT, GOOGLE_API_KEY, GOOGLE_USER_IP)
    resp = requests.get(url, headers=headers)
    info = resp.json()
    user = {"first_name": info["given_name"],
            "last_name": info["family_name"],
            "email": info["email"]}
    if g.db.users.find({"email": info["email"]}).count() > 0:
        return render_template("confirmation.html", registered=True)
    g.db.users.insert(user)
    return render_template("confirmation.html", email=info["email"],
                           signature=sign(info["email"]))


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
