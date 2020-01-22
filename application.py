from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_socketio import SocketIO, emit, send, join_room
import Game
import random

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
CATEGORIES = {9: 'General Knowledge', 10: 'Entertainment: Books', 11: 'Entertainment: Film', 12: 'Entertainment: Music', 13: 'Entertainment: Musicals & Theatres', 14: 'Entertainment: Television', 15: 'Entertainment: Video Games', 16: 'Entertainment: Board Games', 17: 'Science & Nature', 18: 'Science: Computers', 19: 'Science: Mathematics', 20: 'Mythology', 21: 'Sports', 22: 'Geography', 23: 'History', 24: 'Politics', 25: 'Art', 26: 'Celebrities', 27: 'Animals', 28: 'Vehicles', 29: 'Entertainment: Comics', 30: 'Science: Gadgets', 31: 'Entertainment: Japanese Anime & Manga', 32: 'Entertainment: Cartoon & Animations'}

# Home page
@app.route("/")
def index():
    return render_template('homepage.html')

@app.route("/game")
def game():
    return render_template("game-lobby.html")

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

# Ready ups user

@socketio.on("ready")
def ready(data):
    user = data['user']
    room = data['room_id']
    if GAME_ROOMS[room].ready_up(user):
<<<<<<< HEAD
        # start_game(GAME_ROOMS[room])
=======
>>>>>>> 45f40bc0a9d6f641fed114814dd9602ebd334673
        # Choose a quizmaster
        quizmaster = choose_quizmaster()

        # Choose 4 categories for the quizmaster to pick from
        categories = random.sample(range(9, 32), 4)
        categories = {c : CATEGORIES[c] for c in categories}





        # For now, just pass
        pass
    
    json_room = GAME_ROOMS[room].to_json()
    emit("lobby", {'url': lobby_render(json_room), 'title':json_room }, room=room)

def lobby_render(info):
    return render_template("game-lobby.html")

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