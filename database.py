from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_babel import Babel, format_datetime


app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
babel = Babel(app)

@app.context_processor
def inject_conf_vars():
    return dict(format_datetime=format_datetime)






app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mega_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    speciality = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False, nullable=False)
    content = db.Column(db.String(2000), unique=False, nullable=False)
    date_of_create = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

news = db.relationship('News', backref='author', lazy=True)

with app.app_context():
    db.create_all()