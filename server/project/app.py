import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import server.project.models as m
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['TESTING'] = True

CORS(app)

db.init_app(app)
db.create_all(app=app)

login_manager = LoginManager()
# login_manager.login_view = 'auth.login_post'
login_manager.init_app(app)

socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('connect')
def client_connect():
    print("client_connect")



@socketio.on('disconnect')
def client_disconnect():
    print("client_disconnect")


@socketio.on('send_message')
def client_send_message(data):
    print(data)


@socketio.on('registration')
def registration(data):
    email = data['email']
    name = data['name']
    password = data['password']

    user = m.User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        emit('registration_response', {"code": 400, "message": 'Email уже существует'}, broadcast=False)
        return

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = m.User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    emit('registration_response', {"code": 200, "message": 'Вы успешно зарегистрировались'}, broadcast=False)


@socketio.on('login')
def login(data):
    email = data['email']
    password = data['password']
    remember = True if data['remember'] else False

    user = m.User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        emit('login_response', {"code": 400, "message": 'Не удалось зайти'}, broadcast=False)
        return

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    emit('login_response', {"code": 200, "user": user.to_dict()}, broadcast=False)


@socketio.on('create_room')
def create_room(data):
    room_name = data['room_name']
    id = data['id']
    new_room = m.Room(creator_user_id=id, name=room_name)

    user = m.User.query.filter_by(id=id).first()
    user.rooms.append(new_room)
    current_db_sessions = db.session.object_session(new_room)
    current_db_sessions.add(new_room)
    current_db_sessions.commit()
    emit('add_room_response', {"code": 200, "message": "Вы добавились в беседу"}, broadcast=False)
    get_rooms_by_user_id(id)


@socketio.on('get_rooms')
def get_rooms(data):
    get_rooms_by_user_id(data['id'])


def get_rooms_by_user_id(id):
    user = m.User.query.filter_by(id=id).first()
    emit('get_rooms_response', {"code": 200, "rooms": [r.to_dict() for r in user.rooms]}, broadcast=False)


@socketio.on("get_rooms_by_name")
def get_rooms_by_name(data):
    room_name = data['room_name']
    rooms = m.Room.query.filter(m.Room.name.contains(room_name)).all()
    emit('get_rooms_by_name_response', {"code": 200, "rooms": [r.to_dict() for r in rooms]}, broadcast=False)


@socketio.on("add_room")
def add_room(data):
    room_id = data['room_id']
    user_id = data['user_id']

    user = m.User.query.filter_by(id=user_id).first()
    room = m.Room.query.filter_by(id=room_id).first()
    if room in user.rooms:
        emit('add_room_response', {"code": 400, "message": "В ваших беседах уже есть эта беседа"}, broadcast=False)
        return

    user.rooms.append(room)
    current_db_sessions = db.session.object_session(room)
    current_db_sessions.add(room)
    current_db_sessions.commit()
    emit('add_room_response', {"code": 200, "message": "Вы добавились в беседу"}, broadcast=False)
    get_rooms_by_user_id(user_id)


@socketio.on('get_room_info')
def get_room_info(data):
    room_id = data['room_id']
    user_id = data['user_id']

    user = m.User.query.filter_by(id=user_id).first()
    room = m.Room.query.filter_by(id=room_id).first()
    if not (room in user.rooms):
        emit('get_room_info_response', {"code": 400, "message": "В ваших беседах нет этой беседы"}, broadcast=False)
        return

    emit('get_room_info_response', {"code": 200, "message": "Получена информация о беседе",
                                    "room": room.to_dict()}, broadcast=False)


@socketio.on('send_message')
def send_message(data):
    room_id = data['room_id']
    user_id = data['user_id']
    content = data['content']
    color = data['color']
    time = datetime.datetime.now()
    user = m.User.query.filter_by(id=user_id).first()
    message = m.Message(room_id=room_id, user_id=user_id, time=time, content=content, color=color)
    db.session.add(message)
    db.session.commit()
    emit('send_message_response', {"code": 200, "message":  "Сообщение успешно отправлено"}, broadcast=False)
    emit('new_message_broadcast', {"code": 200, "message":  message.to_dict(user.name)}, broadcast=True)


@socketio.on('get_messages')
def get_messages(data):
    room_id = data['room_id']
    user_id = data['user_id']
    user = m.User.query.filter_by(id=user_id).first()
    room = m.Room.query.filter_by(id=room_id).first()
    if not (room in user.rooms):
        emit('get_messages_response', {"code": 400, "message": "В ваших беседах нет этой беседы"}, broadcast=False)
        return

    messages = room.messages.all()

    result = []
    for mes in messages:
        user_id = mes.user_id
        user = m.User.query.filter_by(id=user_id).first()
        result.append(mes.to_dict(user.name))
    emit('get_messages_response', {"code": 200, "messages": result[-40:]}, broadcast=False) #мб вот здесь broadcast true


@socketio.on('leave_room')
def leave_room(data):
    room_id = data['room_id']
    user_id = data['user_id']

    user = m.User.query.filter_by(id=user_id).first()
    room = m.Room.query.filter_by(id=room_id).first()
    if not (room in user.rooms):
        emit('leave_room_response', {"code": 400, "message": "Вы не добавлены в беседу"}, broadcast=False)
        return

    user = m.User.query.filter_by(id=user_id).first()

    user.rooms.remove(room)
    current_db_sessions = db.session.object_session(room)
    current_db_sessions.commit()

    emit('leave_room_response', {"code": 200, "message": "Вы покинули беседу"}, broadcast=False)
    get_rooms_by_user_id(user_id)


if __name__ == '__main__':
    socketio.run(app, port=2345)
