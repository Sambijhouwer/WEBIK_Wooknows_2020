from helpers import questions
import random
import json

playerlist = ['Sascha', 'Ana', 'Steijn', 'Sam']
CATEGORIES = {9: 'General Knowledge', 10: 'Entertainment: Books', 11: 'Entertainment: Film', 12: 'Entertainment: Music', 13: 'Entertainment: Musicals & Theatres', 14: 'Entertainment: Television', 15: 'Entertainment: Video Games', 16: 'Entertainment: Board Games', 17: 'Science & Nature', 18: 'Science: Computers', 19: 'Science: Mathematics', 20: 'Mythology', 21: 'Sports', 22: 'Geography', 23: 'History', 24: 'Politics', 25: 'Art', 26: 'Celebrities', 27: 'Animals', 28: 'Vehicles', 29: 'Entertainment: Comics', 30: 'Science: Gadgets', 31: 'Entertainment: Japanese Anime & Manga', 32: 'Entertainment: Cartoon & Animations'}

def gameplay(playerlist, token = None):
    score = 9
    while score < 10:
        # pick a random quizmaster
        quizmaster = random.choice(playerlist)
        
        # Pick four random categories
        categories = random.sample(range(9, 32), 4)
        categories = {c : CATEGORIES[c] for c in categories}
        # emit lobby, lobby komt binnen
        # If game.quizmaster == store.username
        # modalActive == True
        # click event listeners

        # Get the category and send that to the API

        category = 9
        round_questions = questions(category, token)

        # Play a round
        answers = dict()
        for play_round in round_questions: 
            correct_answer = play_round['correct']
            wrong_answers = play_round['incorrects']
            answers = {play_round['question']:[correct_answer, wrong_answers]}
            print(answers)

        if score >= 10:
            
            break

gameplay(playerlist)
            
