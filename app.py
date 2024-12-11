# app.py
from flask import Flask, render_template, request, jsonify
import random

def create_app():
    app = Flask(__name__)

    # Colors and their respective words
    colors = ["red", "blue", "green", "yellow", "purple", "orange"]
    words = ["RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "ORANGE"]

    def generate_new_word():
        random_index = random.randint(0, len(colors) - 1)
        return {"color": colors[random_index], "word": words[random_index]}

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/start_game', methods=['POST'])
    def start_game():
        player1_name = request.form.get('player1_name', '').strip()
        player2_name = request.form.get('player2_name', '').strip()
        if not player1_name or not player2_name:
            return jsonify({"error": "Both player names are required."}), 400

        game_data = {
            "player1_name": player1_name,
            "player2_name": player2_name,
            "player1_score": 0,
            "player2_score": 0,
            "time_left": 30,
            "phase": 1,
            "color_word": generate_new_word()
        }
        return jsonify(game_data)

    @app.route('/next_word', methods=['POST'])
    def next_word():
        return jsonify(generate_new_word())

    @app.route('/submit_answer', methods=['POST'])
    def submit_answer():
        data = request.get_json()
        try:
            color_input = data['color_input']
            correct_color = data['correct_color']
            time_left = data['time_left']
            player1_score = data['player1_score']
            player2_score = data['player2_score']
        except KeyError as e:
            return jsonify({"error": f"Missing parameter: {e.args[0]}"}), 400

        if color_input.lower() == correct_color.lower():
            if time_left > 15:
                player1_score += 1
            else:
                player2_score += 1

        return jsonify({
            "player1_score": player1_score,
            "player2_score": player2_score
        })

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
