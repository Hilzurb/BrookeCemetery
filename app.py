from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set your secure secret key!

DATABASE = 'database.db'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'  # Set your own password!

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
    search_query = ''
    if request.method == 'POST':
        search_query = request.form['search']
        query = """
            SELECT * FROM burials 
            WHERE name LIKE ? OR section LIKE ? OR lot LIKE ?
        """
        search_term = f'%{search_query}%'
        burials = conn.execute(query, (search_term, search_term, search_term)).fetchall()
    else:
        burials = conn.execute('SELECT * FROM burials LIMIT 100').fetchall()
    conn.close()
    return render_template('index.html', burials=burials, search_query=search_query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET'])
def admin():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/add_burial', methods=['POST'])
def add_burial():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    section = request.form['section']
    lot = request.form['lot']
    name = request.form['name']
    dob = request.form['dob']
    dod = request.form['dod']
    stone = request.form['stone']
    notes = request.form['notes']
    direction = request.form['direction']

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO burials (section, lot, name, dob, dod, stone, notes, direction)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (section, lot, name, dob, dod, stone, notes, direction))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)


