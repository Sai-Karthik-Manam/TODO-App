from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',  # Change if needed
    database='TODO_LIST'  # Ensure this DB and 'notes' table exist
)
cursor = conn.cursor()

@app.route('/')
def index():
    query = request.args.get('query')
    if query:
        cursor.execute("SELECT * FROM notes WHERE title LIKE %s OR content LIKE %s ORDER BY created_at DESC", (f"%{query}%", f"%{query}%"))
    else:
        cursor.execute("SELECT * FROM notes ORDER BY created_at ASC")
    notes = cursor.fetchall()
    return render_template('index.html', notes=notes)


@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        cursor.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete_note(id):
    cursor.execute("DELETE FROM notes WHERE id=%s", (id,))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        cursor.execute("UPDATE notes SET title=%s, content=%s WHERE id=%s", (title, content, id))
        conn.commit()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM notes WHERE id=%s", (id,))
    note = cursor.fetchone()
    return render_template('edit.html', note=note)

if __name__ == '__main__':
    app.run(debug=True)
