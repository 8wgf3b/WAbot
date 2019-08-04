from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db.create_all()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    plaform = db.Column(db.String(80), unique=True, nullable=False, default='telegram')
    key = db.Column(db.String(80), unique=True, nullable=False)
