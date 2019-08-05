from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, Response
from flask import Flask
import os

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    key = db.Column(db.String(80), nullable=False)

    def __init__(self, username, key):
        self.username = username
        self.key = key

    @classmethod
    def getall(cls):
        return cls.query.all()

    def upsert(self):
        item = User.query.filter_by(username = self.username).first()
        if item != None:
            db.session.delete(item)
            db.session.commit()
        db.session.add(self)
        db.session.commit()

if __name__ == '__main__':
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
    db.init_app(app)
    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    @app.route('/ifttt', methods=['GET', 'POST'])
    def ifttt():
        if request.method == 'POST':
            try:
                return Response('ok', status=200)

            except Exception as e:
                print(e)
                return Response('ok', status=200)
        else:
            new = User('riori', 'ew535325')
            new.upsert()
            new = User('riori', 'ewewt535325')
            new.upsert()
            new = User('rioasifuri', 'ewewt535325')
            new.upsert()
            s = ''
            for item in User.getall():
                s += item.username +'\n'
            return Response(s, status=200)


    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
