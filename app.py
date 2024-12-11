from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# List of possible colors
colours = ['Red', 'Blue', 'Green', 'Pink', 'Black', 'Yellow', 'Orange', 'White', 'Purple', 'Brown']
scores = [0, 0]  # Scores for Player 1 and Player 2
timeleft = 30
current_player = 0  # Player 1 starts (0 for Player 1, 1 for Player 2)

@app.route('/')
def home():
    global timeleft, current_player
    timeleft = 30  # Reset the timer when the game starts
    current_player = 0  # Player 1 starts
    return render_template('index.html', scores=scores, timeleft=timeleft, current_player=current_player)

@app.route('/start_game', methods=['POST'])
def start_game():
    global scores, timeleft, current_player
    # Shuffle and pick the color
    random.shuffle(colours)
    word_color = colours[1]
    text_color = colours[0]
    
    # Get the color typed by the player
    player_input = request.form.get('color_input')

    if player_input and player_input.lower() == word_color.lower():
        scores[current_player] += 1

    # Switch player after each input
    current_player = 1 - current_player

    # Check if the time is over (for simplicity, the timer is not dynamic here)
    if timeleft == 0:
        winner = "Player 1" if scores[0] > scores[1] else "Player 2" if scores[1] > scores[0] else "It's a tie!"
        return render_template('index.html', scores=scores, timeleft=timeleft, current_player=current_player, winner=winner)
    
    return render_template('index.html', scores=scores, timeleft=timeleft, current_player=current_player, word_color=word_color, text_color=text_color)

if __name__ == "__main__":
    app.run(debug=True)
