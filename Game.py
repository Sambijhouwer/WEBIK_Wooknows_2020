import string
import random
import requests

MIN_PLAYERS = 2
MAX_PLAYERS = 4

class info(object):
    """Object which handles game status"""
    def __init__(self, name):
        self.game_name = name
        self.players = []
        self.ready = {}
        self.scores = {}
        self.questions = []
        self.game_id = self.generate_room_id()
        self.session_token = self.generate_session_token()
        self.quizmaster = None

    def add_player(self, name):
        """Add player to game"""
        if len(self.players) >= MAX_PLAYERS:
            return False
        else:
            self.players.append(name)
            self.scores[name] = 0
            return True

    def remove_player(self, name):
        """Delete player from game"""
        self.players.remove(name)
        self.scores.pop(name)

    def ready_up(self, name):
        try:
            self.ready[name] = not self.ready[name] 
        except:
            self.ready[name] = True
        if all(self.ready.values()):
            return True
        else:
            return False

    def choose_quizmaster(self):
        self.quizmaster = random.choice(self.players)
        return True

    def to_json(self):
        """Turn object to JSON"""
        return {
            'game_name': self.game_name,
            'players': self.players,
            'scores': self.scores,
            'questions': self.questions,
            'quizmaster': self.quizmaster,
            'game_id': self.game_id
        }

    @classmethod
    def generate_room_id(cls):
        """Generate a random room ID"""
        id_length = 6
        return ''.join(random.SystemRandom().choice(
            string.ascii_uppercase) for _ in range(id_length))
    
    @classmethod
    def generate_session_token(cls):
        """Generate session token for api"""
        try:
            response = requests.get("https://opentdb.com/api_token.php?command=request")
        except:
            response.raise_for_status()
            return None
        
        api_token = response.text
        return api_token
    
    def __str__(self):
        return f"Players: {self.players}, scores: {self.scores}, naam: {self.game_name}"