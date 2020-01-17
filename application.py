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

<<<<<<< HEAD
=======
@app.route("/spelding")
def spel_ding():
    return render_template("spelding.html")
    
>>>>>>> 9fa40386b1a97681df400b0367294739be4b540d
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
        send(GAME_ROOMS[room].to_json(), room=room)

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