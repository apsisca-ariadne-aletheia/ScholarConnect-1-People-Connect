pip install Flask-Login Flask-WTF

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user


# Setup Flask-WTF
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# update submit route in the app.py file to handle user registration and login:

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')
    interests = request.form.get('interests')

    # Check if the user already exists
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, interests FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()
    conn.close()

    if existing_user:
        # User exists, log them in
        user = User()
        user.id = existing_user[0]
        login_user(user)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('dashboard', user_id=user.id))
    else:
        # User doesn't exist, register them
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, interests) VALUES (?, ?, ?)',
                       (username, password, interests))
        conn.commit()
        conn.close()

        # Log in the newly registered user
        user = User()
        user.id = cursor.lastrowid
        login_user(user)
        flash('Registered and logged in successfully!', 'success')
        return redirect(url_for('dashboard', user_id=user.id))


# Create the login and dashboard routes:

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if the username and password are valid
        conn = sqlite3.connect('user_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password FROM users WHERE username = ? AND password = ?',
                       (username, password))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            # Valid credentials, log the user in
            user = User()
            user.id = user_data[0]
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard', user_id=user.id))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html', form=form)


@app.route('/dashboard/<int:user_id>')
@login_required
def dashboard(user_id):
    return render_template('dashboard.html', user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))




