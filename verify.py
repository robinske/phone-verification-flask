from authy.api import AuthyApiClient
from authy import AuthyFormatException
from flask import (Flask, Response, request, redirect,
    render_template, session, url_for)


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']


api = AuthyApiClient(app.config['AUTHY_API_KEY'])


def create_verification():
    country_code = request.form.get("country_code")
    phone_number = request.form.get("phone_number")
    method = request.form.get("method")

    user = api.users.create('foo@bar.com', phone_number, country_code)
    session['authy_id'] = user.id

    if method == "sms":
        api.users.request_sms(user.id, {"force": True})
    elif method == "call":
        api.users.request_call(user.id, {"force": True})

    return redirect(url_for("verify"))


def verify_token():
    token = request.form.get("token")
    authy_id = session.get("authy_id")

    try:
        verification = api.tokens.verify(authy_id, token)

        if verification.ok():
            return Response("<h1>Success!</h1>")
    except:
        pass

    return render_template("verify.html")


@app.route("/phone_verification", methods=["GET", "POST"])
def phone_verification():
    if request.method == "POST":
        return create_verification()

    return render_template("new_verification.html")


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        return verify_token()

    return render_template("verify.html")


if __name__ == '__main__':
    app.run(debug=True)
