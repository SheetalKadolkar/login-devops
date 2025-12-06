from flask import Flask, render_template, request
import mysql.connector
import time

app = Flask(__name__)

# ✅ Retry logic to wait for MySQL
while True:
    try:
        db = mysql.connector.connect(
            host="mysql",
            user="root",
            password="root",
            database="logindb"
        )
        print("✅ Connected to MySQL")
        break
    except mysql.connector.Error:
        print("⏳ Waiting for MySQL to be ready...")
        time.sleep(5)

cursor = db.cursor()

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/submit', methods=["POST"])
def submit():
    username = request.form['username']
    password = request.form['password']

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s,%s)",
        (username, password)
    )
    db.commit()

    return "✅ Login Data Stored Successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
