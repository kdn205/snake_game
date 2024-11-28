# score_manager.py
import json

SCORE_FILE = 'player_scores.json'

def save_score(player_name, score):
    try:
        with open(SCORE_FILE, 'r') as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = {}

    scores[player_name] = score

    with open(SCORE_FILE, 'w') as file:
        json.dump(scores, file)

def load_scores():
    try:
        with open(SCORE_FILE, 'r') as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = {}

    return scores