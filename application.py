from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from flask_socketio import SocketIO, emit, send, join_room
import eventlet
import Game
import random
from helpers import questions

#sys.path.append(os.getcwd())

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = 'asnkdansdkank'
params = {
    'cors_allowed_origins': '*'
}
socketio = SocketIO(app, **params)


GAME_ROOMS = {}
CATEGORIES = {9: 'General Knowledge', 10: 'Entertainment: Books', 11: 'Entertainment: Film', 12: 'Entertainment: Music', 13: 'Entertainment: Musicals & Theatres', 14: 'Entertainment: Television', 15: 'Entertainment: Video Games', 16: 'Entertainment: Board Games', 17: 'Science & Nature', 18: 'Science: Computers', 19: 'Science: Mathematics', 20: 'Mythology', 21: 'Sports', 22: 'Geography', 23: 'History', 24: 'Politics', 25: 'Art', 26: 'Celebrities', 27: 'Animals', 28: 'Vehicles', 29: 'Entertainment: Comics', 30: 'Science: Gadgets', 31: 'Entertainment: Japanese Anime & Manga', 32: 'Entertainment: Cartoon & Animations'}

@socketio.on('createGame')
def createGame(data):
    """ Creates Game object """
    game = Game.info(data['name'])
    room = game.game_id
    GAME_ROOMS[room] = game
    emit('join_room', {'room': GAME_ROOMS[room].to_json()})
    emit('new_room', {'room': GAME_ROOMS[room].to_json()}, broadcast=True)

# Join Game object
@socketio.on('joinGame')
def joinGame(data):
    """
    """
    room = data['room_id']
    if room in GAME_ROOMS:
        GAME_ROOMS[room].add_player(data['name'])
        join_room(room)
        json_room = GAME_ROOMS[room].to_json()
        emit("lobby", {'game': json_room }, room=room)
    else: 
        return False

# Send all rooms to client
@socketio.on('get_rooms')
def send_rooms():
    """
    """
    emit('all_rooms', [room.to_json() for room in GAME_ROOMS.values()])

# Ready ups user
@socketio.on("ready")
def ready(data):
    """
    """
    user = data['user']
    room = data['room_id']
    if GAME_ROOMS[room].ready_up(user):
        game_cats(room)
    else:
        json_room = GAME_ROOMS[room].to_json()
        emit("lobby", {'game': json_room }, room=room)

@socketio.on('categorie')
def question(data):
    """
    """
    cat_id = [i for i, item in CATEGORIES.items() if item == data['categorie']][0]
    room_id = data['room_id']
    api_questions = questions(cat_id, GAME_ROOMS[room_id].session_token)
    question = api_questions[0]['question']
    answers = [api_questions[0]['correct'], *api_questions[0]['incorrects']]
    emit('questions', {'question': question, 'answers': answers}, room=room_id)

@socketio.on('antwoorden')
def antwoorden(data):
    """
    """
    room = data['room_id']
    GAME_ROOMS[room].up_score(data['user'], data['antwoord'])
    json_room = GAME_ROOMS[room].to_json()
    emit("lobby", {'game': json_room }, room=room)
    if GAME_ROOMS[room].teller % len(GAME_ROOMS[room].players) == 0:
        if GAME_ROOMS[room].check_winner():
            emit('scoreboard', {'game': GAME_ROOMS[room].to_json()}, room=room)
        else:
            game_cats(room)
        

def game_cats(room):
    """
    """
    # Choose a quizmaster
    GAME_ROOMS[room].choose_quizmaster()
    
    # Choose 4 categories for the quizmaster to pick from
    categories = random.sample(range(9, 32), 4)
    categories = [CATEGORIES[c] for c in categories]
    emit('spel', {'categorie': categories, 'game': GAME_ROOMS[room].to_json()}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)