from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Colors and their respective words
colors = ["red", "blue", "green", "yellow", "purple", "orange"]
words = ["RED", "BLUE", "GREEN", "YELLOW", "PURPLE", "ORANGE"]

# Function to generate a new word and color
def generate_new_word():
    word_index = random.randint(0, len(colors) - 1)
    display_color = random.choice([color for color in colors if color != colors[word_index]])
    return {"color": display_color, "word": words[word_index]}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start_game", methods=["POST"])
def start_game():
    player1_name = request.json.get("player1_name", "").strip()
    player2_name = request.json.get("player2_name", "").strip()

    if not player1_name or not player2_name:
        return jsonify({"error": "Both player names are required."}), 400

    game_data = {
        "player1_name": player1_name,
        "player2_name": player2_name,
        "player1_score": 0,
        "player2_score": 0,
        "color_word": generate_new_word(),
    }
    return jsonify(game_data)

@app.route("/next_word", methods=["POST"])
def next_word():
    return jsonify(generate_new_word())

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.json
    color_input = data.get("color_input", "").strip().lower()
    correct_color = data.get("correct_color", "").strip().lower()
    time_left = data.get("time_left", 30)
    player1_score = data.get("player1_score", 0)
    player2_score = data.get("player2_score", 0)

    if color_input == correct_color:
        if time_left > 15:
            player1_score += 1
        else:
            player2_score += 1

    return jsonify({
        "player1_score": player1_score,
        "player2_score": player2_score
    })

if __name__ == "__main__":
    app.run(debug=True)
