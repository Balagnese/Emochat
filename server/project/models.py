from server.project.app import db
from flask_login import UserMixin
import sqlalchemy as alc

# relational table
room_users = db.Table('room_users',
                       alc.Column('room_id', alc.Integer, alc.ForeignKey('rooms.id')),
                       alc.Column('user_id', alc.Integer, alc.ForeignKey('users.id')))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = alc.Column(alc.Integer, primary_key=True)
    name = alc.Column(alc.String)
    accepted = alc.Column(alc.Integer)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)

    rooms = db.relationship('Room', secondary=room_users)
    messages = db.relationship('Message', backref='user', lazy='dynamic')

    def to_dict(self):
        return dict(id=self.id,
                    email=self.email,
                    name=self.name)


class Room(db.Model):

    __tablename__ = 'rooms'

    id = alc.Column(alc.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    creator_user_id = alc.Column(alc.Integer, db.ForeignKey('users.id'))

    users = db.relationship('User', secondary=room_users)
    messages = db.relationship('Message', backref='room', lazy='dynamic')

    def to_dict(self):
        return dict(id=self.id,
                    name=self.name,
                    creator_user_id=self.creator_user_id)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    time = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    color = db.Column(db.String(1000), nullable=False)

    def to_dict(self, user_name):
        time = self.time
        str_time = str(time.time().hour) + ':' + str(time.time().minute) + ':' + str(time.time().second) + ' ' +\
                   str(time.date())
        return dict(id=self.id,
                    user_name=user_name,
                    room_id=self.room_id,
                    user_id=self.user_id,
                    time=str_time,
                    content=self.content,
                    color=self.color)



