"""
Waarschijnlijk alles wegkieperen
"""

import requests
import random
import json

def QandA (category, token = None):
    """Contacts API and retrieves questions + answers based on category"""

    # Als geen token is meegegeven, maak replacement voor debuggen
    if not token:
        token = requests.get("https://opentdb.com/api_token.php?command=request")
        token = json.loads(token.text)['token']


    # Generate number of questions to be asked
    number_of_questions = random.randint(1, 3)

    # Retrieve questions and answers from API 
    try:
        response = requests.get(f"https://opentdb.com/api.php?amount={number_of_questions}&category={category}&type=multiple&token={token}")
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
        
    return question_list
