from flask import Flask
from flask_socketio import SocketIO, emit, send, join_room
import eventlet
import Game
import random
from helpers import questions

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
PLAYERS = []
CATEGORIES = {9: 'General Knowledge', 10: 'Entertainment: Books', 11: 'Entertainment: Film', 12: 'Entertainment: Music', 13: 'Entertainment: Musicals & Theatres', 14: 'Entertainment: Television', 15: 'Entertainment: Video Games', 16: 'Entertainment: Board Games', 17: 'Science & Nature', 18: 'Science: Computers', 19: 'Science: Mathematics', 20: 'Mythology', 21: 'Sports', 22: 'Geography', 23: 'History', 24: 'Politics', 25: 'Art', 26: 'Celebrities', 27: 'Animals', 28: 'Vehicles', 29: 'Entertainment: Comics', 30: 'Science: Gadgets', 31: 'Entertainment: Japanese Anime & Manga', 32: 'Entertainment: Cartoon & Animations'}

@socketio.on('check_name')
def check_name(data):
    """Check if username is available"""
    username = data['name']
    print('hello')
    if username in PLAYERS:
        emit('username', {'available': False})
    else:
        PLAYERS.append(username)
        emit('username', {'available': True, 'username': username})

@socketio.on('createGame')
def createGame(data):
    """Create a new Game object"""
    gm = Game.info(data['name'])
    room = gm.game_id
    GAME_ROOMS[room] = gm
    emit('join_room', {'room': GAME_ROOMS[room].to_json()})
    emit('new_room', {'room': GAME_ROOMS[room].to_json()}, broadcast=True)

# Join Game object
@socketio.on('joinGame')
def joinGame(data):
    """Joins user to a Game"""
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
    """Sends existing rooms to new connecting users"""
    emit('all_rooms', [room.to_json() for room in GAME_ROOMS.values()])

# Ready ups user
@socketio.on("ready")
def ready(data):
    """Ready up user, if every player is ready start game"""
    user = data['user']
    room = data['room_id']
    if GAME_ROOMS[room].ready_up(user):
        game_cats(room)
    else:
        json_room = GAME_ROOMS[room].to_json()
        emit("lobby", {'game': json_room }, room=room)

@socketio.on('categorie')
def question(data):
    """Fetch and send questions from user choosen category"""
    cat_id = [i for i, item in CATEGORIES.items() if item == data['categorie']][0]
    room_id = data['room_id']
    api_questions = questions(cat_id, GAME_ROOMS[room_id].session_token)
    question = api_questions[0]['question']
    answers = [api_questions[0]['correct'], *api_questions[0]['incorrects']]
    emit('questions', {'question': question, 'answers': answers}, room=room_id)

@socketio.on('answers')
def answers(data):
    """Checks answers, send to scoreboard if there is a winner"""
    room = data['room_id']
    GAME_ROOMS[room].up_score(data['user'], data['ans'])
    json_room = GAME_ROOMS[room].to_json()
    emit("lobby", {'game': json_room }, room=room)
    if GAME_ROOMS[room].teller % len(GAME_ROOMS[room].players) == 0:
        if GAME_ROOMS[room].check_winner():
            emit('scoreboard', {'game': GAME_ROOMS[room].to_json()}, room=room)
            del GAME_ROOMS[room]
            emit('all_rooms', [room.to_json() for room in GAME_ROOMS.values()])
        else:
            game_cats(room)
        

def game_cats(room):
    """Helper function to emit categories to users"""
    GAME_ROOMS[room].choose_quizmaster()
    
    categories = random.sample(range(9, 32), 4)
    categories = [CATEGORIES[c] for c in categories]
    emit('game', {'categories': categories, 'game': GAME_ROOMS[room].to_json()}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)