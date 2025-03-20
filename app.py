
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
