from twilio.rest import Client
from flask import (Flask, Response, request, redirect,
    render_template, session, url_for)


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']


client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])
service_id = app.config['SERVICE_ID']


@app.route("/phone_verification", methods=["GET", "POST"])
def phone_verification():
    if request.method == "POST":
        phone_number = request.form.get("phone_number")
        method = request.form.get("method")

        session['phone_number'] = phone_number

        client.verify \
            .services(service_id) \
            .verifications \
            .create(to=phone_number, channel=method)

        return redirect(url_for("verify"))

    return render_template("phone_verification.html")


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
            token = request.form.get("token")
            phone_number = session.get("phone_number")

            verification = client.verify \
                .services(service_id) \
                .verification_checks \
                .create(to=phone_number, code=token)

            if verification.valid:
                return Response("<h1>Success!</h1>")

    return render_template("verify.html")


if __name__ == '__main__':
    app.run(debug=True)
