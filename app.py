from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__)

# Colors and their respective words
colors = ["red", "blue", "green", "yellow", "purple", "orange"]
words = ["RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "ORANGE"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    player1_name = request.form['player1_name']
    player2_name = request.form['player2_name']
    game_data = {
        'player1_name': player1_name,
        'player2_name': player2_name,
        'player1_score': 0,
        'player2_score': 0,
        'current_player': player1_name,
        'time_left': 30,
        'color_word': generate_new_word(),
    }
    return jsonify(game_data)

@app.route('/next_word', methods=['POST'])
def next_word():
    color_word = generate_new_word()
    return jsonify({'color_word': color_word})

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    color_input = data['color_input']
    correct_color = data['correct_color']
    current_player = data['current_player']
    player1_score = data['player1_score']
    player2_score = data['player2_score']

    if color_input.lower() == correct_color.lower():
        if current_player == data['player1_name']:
            player1_score += 1
        else:
            player2_score += 1

    return jsonify({
        'player1_score': player1_score,
        'player2_score': player2_score,
    })

def generate_new_word():
    random_index = random.randint(0, len(colors) - 1)
    color = colors[random_index]
    word = words[random_index]
    return {'color': color, 'word': word}

if __name__ == "__main__":
    app.run(debug=True)
