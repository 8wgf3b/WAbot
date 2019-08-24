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



class Resub(db.Model):
    __tablename__ = "resub"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chatid = db.Column(db.String(50), unique=True, nullable=False)
    subs = db.Column(db.String(200), nullable=False, default='')

    def __init__(self, chatid, subs=''):
        self.chatid = chatid
        self.subs = subs

    @classmethod
    def getall(cls):
        return cls.query.all()

    @classmethod
    def sublist(cls, cid):
        return cls.query.filter(cls.chatid == cid).first().subs

    def upsert(self):
        item = Resub.query.filter_by(chatid = self.chatid).first()
        if item != None:
            db.session.delete(item)
            db.session.commit()
        db.session.add(self)
        db.session.commit()

    @classmethod
    def redappend(cls, cid, new = []):
        item = cls.query.filter(cls.chatid == cid).first()
        if item == None:
            return
        buffer = item.subs.split()
        buffer.extend(new)
        item.subs = ' '.join(buffer)
        db.session.commit()

    @classmethod
    def redremove(cls, cid, subslist = []):
        item = cls.query.filter(cls.chatid == cid).first()
        if item == None:
            return
        buffer = item.subs.split()
        buffer = list(set(buffer) - set(subslist))
        item.subs = ' '.join(buffer)
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
            new = Resub('riori')
            new.upsert()
            new = Resub('riori')
            new.upsert()
            new = Resub('rioasifuri')
            new.upsert()
            Resub.redappend('riori', ['lol', 'lmao'])
            Resub.redremove('rioasifuri', ['qwrwr'])
            s = ''
            for item in Resub.getall():
                s += item.chatid + ' ' + item.subs + '\n\n'
            s += Resub.sublist('riori')
            return Response(s, status=200)


    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
