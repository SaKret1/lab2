from flask import Flask, render_template, request, redirect, session
import sqlite3
from database import init_db

app = Flask(__name__)
app.secret_key = "lab_secret_key"

def get_db():
    return sqlite3.connect("database.db")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        # Уязвимость SQL Injection
        #query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        #cursor.execute(query)

        # исправление уязвимости
        query = "SELECT * FROM users WHERE username=? AND password=?"
        cursor.execute(query, (username, password))

        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = user[1]
            return redirect("/dashboard")

        return "Неверный логин или пароль"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


@app.route("/search")
def search():
    if "username" not in session:
        return redirect("/")

    username = request.args.get("username", "")

    # Уязвимость XSS: отключаем экранирование пользовательского ввода
    return render_template(
        "search.html",
        username=username,
        results=username
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
