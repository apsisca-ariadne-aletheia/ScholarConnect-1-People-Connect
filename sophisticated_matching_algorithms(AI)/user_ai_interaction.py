# I have created a messaging system between matched users and use ChatGPT to provide chat responses. Integrating ChatGPT would require an API key from OpenAI ([How to do this:](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import openai

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Setup Flask-SQLAlchemy
db = SQLAlchemy(app)

# Setup Flask-Bcrypt
bcrypt = Bcrypt(app)

# Configure OpenAI API
openai.api_key = 'your_openai_api_key'  # Replace with your actual API key

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    interests = db.Column(db.String(100), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class MatchingAlgorithm:
    @staticmethod
    def calculate_matching_score(user1, user2):
        # ... (unchanged)

@app.route('/connect/<int:user_id>')
@login_required
def connect(user_id):
    current_user_data = User.query.get(current_user.id)
    other_user_data = User.query.get(user_id)

    matching_score = MatchingAlgorithm.calculate_matching_score(current_user_data, other_user_data)

    # Get a prompt for ChatGPT based on user interests or any relevant information
    chat_prompt = f"You have been matched with {other_user_data.username}. Your common interests include {matching_score}%."

    # Call the ChatGPT API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=chat_prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    chat_response = response['choices'][0]['text']

    return render_template('connect.html', user_id=user_id, matching_score=matching_score, chat_response=chat_response)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
