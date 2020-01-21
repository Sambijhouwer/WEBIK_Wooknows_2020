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
socketio = SocketIO(app)

GAME_ROOMS = {}

@app.route("/")
def index():
    if request.method == 'POST':
        # Make sure a user put in a username
        if not request.form.get('username'):
            return render_template('homepage.html')

        username = request.form.get('username')
        return render_template("game-lobby.html")
    
    else:
        return render_template('homepage.html')

@app.route('/test')
def test():
    return render_template("test.html")

@app.route("/game")
def game_lobby():
    return render_template("game-lobby.html")

@app.route("/spelding")
def spel_ding():
    return render_template("spelding.html")
    
@socketio.on('username')
def create_user_ses():
    session['user_id'] = request.sid
    return


@socketio.on('createGame')
def createGame(data):
    gm = Game.info(data['name'])
    room = gm.game_id
    GAME_ROOMS[room] = gm
    emit('join_room', {'room': GAME_ROOMS[room].to_json()})
    emit('new_room', {'room': GAME_ROOMS[room].to_json()}, broadcast=True)

@socketio.on('joinGame')
def joinGame(data):
    room = data['room_id']
    if room in GAME_ROOMS:
        GAME_ROOMS[room].add_player(session['user_id'])
        join_room(room)
        json_room = GAME_ROOMS[room].to_json()
        emit("lobby", {'url': lobby_render(json_room), 'title':json_room }, room=room)
    else: 
        return False

@socketio.on('get rooms')
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