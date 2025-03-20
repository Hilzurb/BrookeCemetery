
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'database.db'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

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
    search_section = ''

    if request.method == 'POST':
        search_query = request.form.get('search', '').strip()
        search_section = request.form.get('search_section', '').strip()

        query = """
            SELECT * FROM burials
            WHERE (LOWER(name) LIKE LOWER(?) OR LOWER(lot) LIKE LOWER(?))
            AND LOWER(section) LIKE LOWER(?)
        """
        search_term_general = f'%{search_query}%'
        search_term_section = f'%{search_section}%'

        if not search_section:
            search_term_section = '%'

        if not search_query:
            search_term_general = '%'

        burials = conn.execute(query, (search_term_general, search_term_general, search_term_section)).fetchall()
    else:
        burials = conn.execute('SELECT * FROM burials LIMIT 100').fetchall()

    conn.close()
    return render_template('index.html', burials=burials, search_query=search_query, search_section=search_section)

# (rest of your app.py remains exactly the same)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    burials = []
    search_query = ''
    search_section = ''

    if request.method == 'POST':
        search_query = request.form.get('search', '').strip()
        search_section = request.form.get('search_section', '').strip()

        query = """
            SELECT * FROM burials
            WHERE (LOWER(name) LIKE LOWER(?) OR LOWER(lot) LIKE LOWER(?))
            AND LOWER(section) LIKE LOWER(?)
        """
        search_term_general = f'%{search_query}%'
        search_term_section = f'%{search_section}%'

        # If no section provided, search all sections
        if not search_section:
            search_term_section = '%'

        # If no general search, search all names and lots
        if not search_query:
            search_term_general = '%'

        burials = conn.execute(query, (search_term_general, search_term_general, search_term_section)).fetchall()
    else:
        burials = conn.execute('SELECT * FROM burials LIMIT 100').fetchall()

    conn.close()
    return render_template('index.html', burials=burials, search_query=search_query, search_section=search_section)
