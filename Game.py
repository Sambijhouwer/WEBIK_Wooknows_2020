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
        self.question = ""
        self.game_id = self.generate_room_id()
        self.session_token = self.generate_session_token()
        self.quizmaster = None
        self.winners = None
        self.teller = 0

    def add_player(self, name):
        """Add player to game"""
        if len(self.players) >= MAX_PLAYERS:
            return False
        else:
            self.players.append(name)
            self.scores[name] = 0
            self.ready[name] = False
            return True

    def remove_player(self, name):
        """Delete player from game"""
        self.players.remove(name)
        self.scores.pop(name)

    def ready_up(self, name):
        """Ready ups player"""
        self.ready[name] = not self.ready[name] 
        if all(self.ready.values()) and len(self.players) > 1:
            return True
        else:
            return False

    def choose_quizmaster(self):
        """Choose a random quizmaster from player array"""
        self.quizmaster = random.choice(self.players)
        return True

    def add_questions(self, questions):
        """Add question to game"""
        self.questions = questions
        return True
    
    def up_score(self, name, correct):
        """Counts the game responses and increments score if correct answer"""
        self.teller += 1
        if correct:
            self.scores[name] += 1

    def check_winner(self):
        """Check if a player has won the game"""
        winner = []
        for player, score in self.scores.items():
            if score == 10:
                winner.append(player)
        if len(winner) != 0:
            self.winners = winner
            return True
        return False

    def to_json(self):
        """Turn object to JSON"""
        return {
            'game_name': self.game_name,
            'players': self.players,
            'scores': self.scores,
            'questions': self.questions,
            'quizmaster': self.quizmaster,
            'game_id': self.game_id,
            'ready': self.ready,
            'winner': self.winners 
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
        
        api_token = response.json()
        return api_token['token']
    
    def __str__(self):
        return f"Players: {self.players}, scores: {self.scores}, naam: {self.game_name}"