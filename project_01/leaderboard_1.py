import json

def load_leaderboard():
    try:
        with open('leaderboard_1.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
     
        return [{"name": "Player 1", "score": 0}, {"name": "Player 2", "score": 0}, {"name": "Player 3", "score": 0}]


def save_leaderboard(leaderboard):
    with open('/home/shree-xd/Documents/CVgameclub/project_01/leaderboard_1.json', 'w') as file:
        json.dump(leaderboard, file)

def update_leaderboard(leaderboard, player_name, player_score):
    leaderboard.append({"name": player_name, "score": player_score})
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    leaderboard = leaderboard[:3]
    save_leaderboard(leaderboard)
