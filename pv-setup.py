from flask import Flask


app = Flask(__name__)


@app.route("/phone_verification", methods=["GET", "POST"])
def phone_verification():
    pass


@app.route("/verify", methods=["GET", "POST"])
def verify():
    pass


if __name__ == '__main__':
    app.run(debug=True)
