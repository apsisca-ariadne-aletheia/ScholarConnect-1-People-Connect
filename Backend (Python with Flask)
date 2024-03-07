# Install Flask
pip install Flask
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create a SQLite database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        interests TEXT
    )
''')
conn.commit()
conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    interests = request.form.get('interests')

    # Save user data to the database
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, interests) VALUES (?, ?)', (username, interests))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


@app.route('/connect/<int:user_id>')
def connect(user_id):
    # Retrieve the user's interests
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT interests FROM users WHERE id = ?', (user_id,))
    interests = cursor.fetchone()[0]
    conn.close()

    # Find other users with similar interests (simple matching for demonstration)
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username FROM users WHERE interests = ?', (interests,))
    matched_users = cursor.fetchall()
    conn.close()

    return render_template('connect.html', user_id=user_id, matched_users=matched_users)


if __name__ == '__main__':
    app.run(debug=True)
