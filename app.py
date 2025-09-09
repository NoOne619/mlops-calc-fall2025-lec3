from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for sessions & flash messages

# Hardcoded credentials for demo
USERNAME = "admin"
PASSWORD = "password123"

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("welcome"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            flash("Login successful!", "success")
            return redirect(url_for("welcome"))
        else:
            flash("Invalid credentials. Try again.", "danger")

    return render_template("login.html")

@app.route("/welcome")
def welcome():
    if "user" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("login"))
    return render_template("welcome.html", user=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)