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


