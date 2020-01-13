import requests
import random
import json

# Moet nog session toevoegen, zodat niet dezelfde vragen worden gesteld
# Maar eerst even kijken hoe we de session gaan 'storen'
def questions (category):
    """Contacts API and retrieves questions + answers based on category"""

    # Generate number of questions to be asked
    number_of_questions = str(random.randint(1, 3))

    # Retrieve questions and answers from API
    try:
        response = requests.get(f"https://opentdb.com/api.php?amount={number_of_questions}&category={category}&type=multiple")
        response.raise_for_status()
    except requests.RequestException:
        return None
    
    # Turn JSON format into a python dictionary
    response = json.loads(response.text)
    
    # A dictionary keyed by an integer with values being dicts as values question + (incorrect)answers
    try:
        question_dict = {}
        for i, item in enumerate(response['results']):
            question_dict[i] = {}
            question_dict[i]['question'] = item['question']
            question_dict[i]['correct'] = item['correct_answer']
            question_dict[i]['incorrects'] = item['incorrect_answers']
    except (KeyError, TypeError, ValueError):
        return None
    
    return question_dict