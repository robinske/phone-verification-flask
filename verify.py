from authy.api import AuthyApiClient
from flask import (Flask, Response, request, redirect,
    render_template, session, url_for)


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']


api = AuthyApiClient(app.config['AUTHY_API_KEY'])


@app.route("/phone_verification", methods=["GET", "POST"])
def phone_verification():
    if request.method == "POST":
        country_code = request.form.get("country_code")
        phone_number = request.form.get("phone_number")
        method = request.form.get("method")

        session['country_code'] = country_code
        session['phone_number'] = phone_number

        api.phones.verification_start(phone_number, country_code, via=method)

        return redirect(url_for("verify"))

    return render_template("phone_verification.html")


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
            token = request.form.get("token")

            phone_number = session.get("phone_number")
            country_code = session.get("country_code")

            verification = api.phones.verification_check(phone_number,
                                                         country_code,
                                                         token)

            if verification.ok():
                return Response("<h1>Success!</h1>")

    return render_template("verify.html")


if __name__ == '__main__':
    app.run(debug=True)
