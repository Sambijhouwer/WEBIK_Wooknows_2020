from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
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
app.config['SECRET_KEY'] = 'secret'
params = {
    'ping_timeout': 30,
    'ping_interval': 15
}
socketio = SocketIO(app, **params)

GAME_ROOMS = {}
USER_LOCATIONS = {}
# Home page
@app.route("/")
def index():
    return render_template('homepage.html')

@socketio.on('disconnect')
def disconnect():
    pass

# Create Game object 
@socketio.on('createGame')
def createGame(data):
    gm = Game.info(data['name'])
    room = gm.game_id
    GAME_ROOMS[room] = gm
    emit('join_room', {'room': GAME_ROOMS[room].to_json()})
    emit('new_room', {'room': GAME_ROOMS[room].to_json()}, broadcast=True)

# Join Game object
@socketio.on('joinGame')
def joinGame(data):
    room = data['room_id']
    if room in GAME_ROOMS:
        GAME_ROOMS[room].add_player(data['name'])
        join_room(room)
        # json_room = GAME_ROOMS[room].to_json()
        return render_template("game-lobby.html")
        # emit("lobby", {'url': render_template("game-lobby.html"), 'game': json_room }, room=room)
    else: 
        return False

# Send all rooms to client
@socketio.on('get_rooms')
def send_rooms():
    emit('all_rooms', [room.to_json() for room in GAME_ROOMS.values()])


@socketio.on("lobbyupdate")
def lobbyupdate(data):
    room = data['id']
    emit("lobby", {'url': lobby_render(GAME_ROOMS[room].to_json())}, room=room)

@socketio.on("ready")
def ready(data):
    user = data['user']
    room = data['room_id']
    if GAME_ROOMS[room].ready_up(user):
        """
        Game start (separate emit probably):
        Update game-lobby to show that players are playing a game (probably with Vue)
        Pick quizmaster --> quizmaster = choose_quizmaster(GAME_ROOMS[room])
        Let quizmaster pick category --> emit("pick", {'quizmaster': quizmaster})
        Contact API with category and session token --> questions(category, session_token)
        Somehow send questions and answers to game-lobby, (hopefully with Vue)
        """

        # For now, just pass
        pass
    
    json_room = GAME_ROOMS[room].to_json()
    emit("lobby", {'url': lobby_render(json_room), 'title':json_room }, room=room)

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