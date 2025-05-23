from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

DATABASE = 'database.db'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    search_name = request.form.get('search_name', '').strip()
    search_section = request.form.get('search_section', '').strip()
    search_lot = request.form.get('search_lot', '').strip()

    query = "SELECT * FROM burials WHERE 1=1"
    params = []

    if search_name:
        query += " AND LOWER(name) LIKE LOWER(?)"
        params.append(f"%{search_name}%")

    if search_section:
        query += " AND LOWER(section) = LOWER(?)"
        params.append(search_section.lower())

    if search_lot:
        query += " AND LOWER(lot) = LOWER(?)"
        params.append(search_lot.lower())

    burials = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('index.html', burials=burials, search_name=search_name, search_section=search_section, search_lot=search_lot)

if __name__ == '__main__':
    app.run(debug=True)
