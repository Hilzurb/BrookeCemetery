from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    burials = []
    search_name = request.form.get('search_name', '').strip()
    search_section = request.form.get('search_section', '').strip()
    search_lot = request.form.get('search_lot', '').strip()

    query = "SELECT * FROM burials WHERE 1=1"
    params = []

    if search_name:
        query += " AND LOWER(name) LIKE LOWER(?)"
        params.append(f'%{search_name}%')

    if search_section:
        query += " AND LOWER(section) = LOWER(?)"
        params.append(search_section.lower())

    if search_lot:
        query += " AND LOWER(lot) = LOWER(?)"
        params.append(search_lot.lower())

    if request.method == 'POST':
        burials = conn.execute(query, params).fetchall()
    else:
        burials = conn.execute('SELECT * FROM burials LIMIT 100').fetchall()

    conn.close()
    return render_template('index.html', burials=burials, search_name=search_name, search_section=search_section, search_lot=search_lot)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Dummy login logic
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
