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
