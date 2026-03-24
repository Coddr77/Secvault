from flask import Flask, render_template, request, redirect, url_for, flash, session
import bcrypt
import os
from dotenv import load_dotenv

from db_config import get_db_connection
from crypto import encrypt_password, decrypt_password

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


# ================= LOGIN =================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user:
            if bcrypt.checkpw(password.encode(), user['master_password_hash'].encode()):
                session['user_id'] = user['user_id']
                session['username'] = user['username']
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))

        flash("Invalid credentials", "danger")

        cursor.close()
        conn.close()

    return render_template("login.html")


# ================= REGISTER =================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (username, master_password_hash) VALUES (%s, %s)",
                (username, hashed.decode())
            )

            conn.commit()

            flash("Account created!", "success")
            return redirect(url_for('login'))

        except Exception as e:
            print(e)
            flash("Username already exists!", "danger")

        finally:
            cursor.close()
            conn.close()

    return render_template("register.html")


# ================= DASHBOARD =================
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM vault WHERE user_id=%s", (session['user_id'],))
    data = cursor.fetchall()

    for item in data:
        try:
            item['encrypted_password'] = decrypt_password(item['encrypted_password'])
        except:
            item['encrypted_password'] = "ERROR"

    cursor.close()
    conn.close()

    return render_template("dashboard.html", vault=data)


# ================= ADD PASSWORD =================
@app.route('/add', methods=['POST'])
def add_password():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    site = request.form['site']
    username = request.form['username']
    password = encrypt_password(request.form['password'])

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO vault (user_id, site_name, site_username, encrypted_password) VALUES (%s, %s, %s, %s)",
        (session['user_id'], site, username, password)
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Password added!", "success")
    return redirect(url_for('dashboard'))


# ================= DELETE =================
@app.route('/delete/<int:id>')
def delete_password(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ FIXED SECURITY BUG
    cursor.execute(
        "DELETE FROM vault WHERE vault_id=%s AND user_id=%s",
        (id, session['user_id'])
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Deleted!", "success")
    return redirect(url_for('dashboard'))


# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for('login'))


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=False)