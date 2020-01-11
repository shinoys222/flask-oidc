import json
from flask_oidc_ex import OpenIDConnect
from flask import Flask, g, jsonify, request, session
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

app.config.from_json("config/config.json")
oidc = OpenIDConnect(app)


@app.route("/flask-oidc/")
def home():
    if oidc.user_loggedin:
        email = oidc.user_getfield("email")
        return f"""
            <div>
                <div>Hello, {email}</dic>
                <ul>
                    <li><a href="/flask-oidc/profile/">Profile</a></li>
                    <li><a href="/flask-oidc/token_info/">token_info</a></li>
                    <li><a href="/flask-oidc/role_protected/token_info/">role_token_info</a></li>
                    <li><a href="/flask-oidc/logout/">Log out</a></li>
                </ul>
            </div>
        """
    else:
        return 'Welcome anonymous, <a href="/flask-oidc/login/">Log in</a>'


@app.route("/flask-oidc/login/")
@oidc.require_login
def login():
    info = oidc.user_getinfo(["email"])
    return 'Hello, %s! <a href="/flask-oidc/">Home</a>' % (info.get("email"))


@app.route("/flask-oidc/profile/")
@oidc.require_login
def profile():
    fields = [
        "given_name",
        "family_name",
        "email",
        "email_verified",
        "roles",
        "resouce_access",
        "username",
        "active",
        "scopes",
    ]
    info = oidc.user_getinfo(fields)
    return f"""
            <div>
                <a href="/flask-oidc/logout/">Log out</a>
                <div>Profile: {info}</dic>
            </div>
        """


@app.route("/flask-oidc/token_info/")
@oidc.require_login
@oidc.accept_token(require_token=False, scopes_required=["flask-oidc:read-token"])
def token_info():
    fields = [
        "given_name",
        "family_name",
        "email",
        "email_verified",
        "roles",
        "resouce_access",
        "username",
        "active",
        "scopes",
    ]
    info = oidc.user_getinfo(fields)
    return jsonify(info)


@app.route("/flask-oidc/role_protected/token_info")
@oidc.require_login
@oidc.require_keycloak_role(client="flask-oidc-example", role="x-admin")
def role_proctected_token_info():
    fields = [
        "given_name",
        "family_name",
        "email",
        "email_verified",
        "roles",
        "resouce_access",
        "username",
        "active",
        "scopes",
    ]
    info = oidc.user_getinfo(fields)
    return jsonify(info)


@app.route("/flask-oidc/api/role_protected/token_info")
@oidc.require_keycloak_role(client="flask-oidc-example", role="x-admin")
def api_role_proctected_token_info():
    fields = [
        "given_name",
        "family_name",
        "email",
        "email_verified",
        "roles",
        "resouce_access",
        "username",
        "active",
        "scopes",
    ]
    info = oidc.user_getinfo(fields)
    return jsonify(info)


@app.route("/flask-oidc/api/token_protected/token_info")
@oidc.accept_token(require_token=True, scopes_required=["flask-oidc:read-token"])
def api_token_proctected_token_info():
    return jsonify(g.oidc_token_info)


@app.route("/flask-oidc/api/role_and_token_protected/token_info")
@oidc.accept_token(require_token=True, scopes_required=["flask-oidc:read-profile"])
@oidc.require_keycloak_role(client="flask-oidc-example", role="x-admin")
def api_role_and_token_proctected_token_info():
    return jsonify(g.oidc_token_info)


@app.route("/flask-oidc/logout/")
def logout():
    oidc.logout()
    session.clear()
    return 'Hi, you have been logged out! <a href="/flask-oidc/">Home</a>'


if __name__ == "__main__":
    app.run(host="0.0.0.0")
