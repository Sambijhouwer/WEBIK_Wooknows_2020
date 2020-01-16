from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_socketio import SocketIO, emit, send, join_room
import Game
#sys.path.append(os.getcwd())


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = 'asnkdansdkank'
socketio = SocketIO(app)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

GAME_ROOMS = {}
USERS = {}
# Ensure responses aren't cached
# @app.after_request
# def after_request(response):
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response


@app.route("/")
def index():
    return render_template('homepage.html')

@app.route("/floep")
def floep():
    return render_template("game-lobby.html")

@socketio.on('username')
def create_user_ses(data):
    session.clear()
    session['username'] = data['username']
    return True

@socketio.on('createGame')
def createGame(data):
    if data['name'] not in GAME_ROOMS:
        gm = Game.info(data['name'])
        room = gm.game_id
        GAME_ROOMS[room] = gm
        rdata = GAME_ROOMS[room].to_json()
        emit('join_room', {'room': rdata})
        emit('new_room', rdata, broadcast=True)
    else:
        return False

@socketio.on('joinGame')
def joinGame(data):
    room = data['room_id']
    if room in GAME_ROOMS:
        if not GAME_ROOMS[room].add_player(session['username']):
            return False
        join_room(room)
        emit("lobby", {'url': lobby_render(GAME_ROOMS[room].to_json())}, room=room)
        emit("lobby_update", {'room': room}, room=room)
    else: 
        return False

@socketio.on('get rooms')
def send_rooms():
    emit('all_rooms', [room.to_json() for room in GAME_ROOMS.values()])

@socketio.on("lobbyupdate")
def lobbyupdate(data):
    emit("lobby", {'url': lobby_render(GAME_ROOMS[data['id']].to_json())}, room=room)

def lobby_render(info):
    return render_template("game-lobby.html", info=info)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template('404.html', name=e.name, code=e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    socketio.run(app)