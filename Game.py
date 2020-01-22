import string
import random
import requests
import json

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
        self.quizmaster_length = 0
        self.QandA = {}
        self.answers = []
        self.correct_answer = ''

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
            'game_id': self.game_id,
            'ready': self.ready
        }

    def game_start(self):

        while any(self.scores) < 15:
            
            if self.quizmaster_length <= 0:
                self.choose_quizmaster()
                self.quizmaster_length = random.randint(1,3)
                self.category = 15      # To be implemented
                self.QandA = self.API()
                
                # Separate answers and questions into separate lists
                for item in self.QandA:
                    self.questions.append(item['question'])
                    correct_dict = {item['correct']:True}
                    self.answers.append(correct_dict.update({answer:False for answer in item['incorrects']}))

                print(self.answers)

            self.play_round()



            
            """
            Game start:
            Update game-lobby to show that players are playing a game
            Pick quizmaster --> self.quizmaster = choose_quizmaster()
            Let quizmaster pick category --> ....
            Contact API with category and session token --> self.API
            Somehow send questions and answers to game-lobby
            """
            pass

        pass

    def API (self):
        """Contacts API and retrieves questions + answers based on category"""

        # Generate number of questions to be asked
        number_of_questions = random.randint(1, 3)

        # Retrieve questions and answers from API 
        try:
            response = requests.get(f"https://opentdb.com/api.php?amount={number_of_questions}&category={self.category}&type=multiple&token={self.session_token}")
            response.raise_for_status()
        except requests.RequestException:
            return None
        
        # Turn JSON format into a python dictionary
        response = json.loads(response.text)

        # Check for Response Code
        if response['response_code'] == 0:

            # A dictionary keyed by an integer with values being dicts as values question + (incorrect)answers
            try:
                question_list = []
                for i, item in enumerate(response['results']):
                    question_list.append({})
                    question_list[i]['question'] = item['question']
                    question_list[i]['correct'] = item['correct_answer']
                    question_list[i]['incorrects'] = item['incorrect_answers']
            except (KeyError, TypeError, ValueError):
                return None
        
        # Something went wrong with the API
        else:
            return None
            
        self.QandA = question_list

        return True

    def play_round (self):
        self.questions.pop()    # Stuur naar game (vraag)
        self.answers.pop()    # Stuur naar game (antwoorden)
        # Stuur vragen en antwoorden naar game
        self.quizmaster_length -= 1
        pass


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