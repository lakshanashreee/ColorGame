document.getElementById("start-game").addEventListener("click", startGame);
document.getElementById("submit-answer").addEventListener("click", submitAnswer);

let player1Name = "";
let player2Name = "";
let player1Score = 0;
let player2Score = 0;
let timeLeft = 30;
let correctColor = "";
let gameInterval = null;

function startGame() {
    player1Name = document.getElementById("player1-name").value.trim();
    player2Name = document.getElementById("player2-name").value.trim();

    if (!player1Name || !player2Name) {
        alert("Both players must enter their names.");
        return;
    }

    // Reset scores and time
    player1Score = 0;
    player2Score = 0;
    timeLeft = 30;

    document.getElementById("player1-score").innerText = player1Score;
    document.getElementById("player2-score").innerText = player2Score;
    document.getElementById("time-left").innerText = timeLeft;

    fetch("/start_game", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `player1_name=${encodeURIComponent(player1Name)}&player2_name=${encodeURIComponent(player2Name)}`
    })
        .then((response) => response.json())
        .then((data) => {
            initializeGame(data);
        })
        .catch((error) => {
            alert(`Error: ${error.message}`);
        });
}

function initializeGame(data) {
    correctColor = data.color_word.color;
    document.getElementById("color-word-text").innerText = data.color_word.word;
    document.getElementById("player-input").style.display = "none";
    document.getElementById("game-info").style.display = "block";

    const colorInput = document.getElementById("color-input");
    colorInput.value = ""; // Clear input field
    colorInput.focus(); // Set focus on the input field

    gameInterval = setInterval(updateTime, 1000);
}

function updateTime() {
    timeLeft--;
    document.getElementById("time-left").innerText = timeLeft;

    if (timeLeft === 15) {
        document.getElementById("current-phase").innerText = `Player 2's turn!`;
    }

    if (timeLeft <= 0) {
        clearInterval(gameInterval);
        declareWinner();
    }
}

function submitAnswer() {
    const colorInput = document.getElementById("color-input");
    const colorInputValue = colorInput.value.trim();

    if (!colorInputValue) {
        alert("Please type a color.");
        return;
    }

    fetch("/submit_answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            color_input: colorInputValue,
            correct_color: correctColor,
            time_left: timeLeft,
            player1_score: player1Score,
            player2_score: player2Score,
        })
    })
        .then((response) => response.json())
        .then((data) => {
            player1Score = data.player1_score;
            player2Score = data.player2_score;

            document.getElementById("player1-score").innerText = player1Score;
            document.getElementById("player2-score").innerText = player2Score;

            fetchNextWord();
        })
        .catch((error) => {
            alert(`Error: ${error.message}`);
        });

    // Clear the input field after submission and refocus
    colorInput.value = "";
    colorInput.focus();
}

function fetchNextWord() {
    fetch("/next_word", { method: "POST" })
        .then((response) => response.json())
        .then((data) => {
            correctColor = data.color;
            document.getElementById("color-word-text").innerText = data.word;

            // Prepare the input field for the next word
            const colorInput = document.getElementById("color-input");
            colorInput.value = "";
            colorInput.focus();
        });
}

function declareWinner() {
    const winner =
        player1Score > player2Score
            ? player1Name
            : player2Score > player1Score
            ? player2Name
            : "It's a tie!";

    document.getElementById("game-info").style.display = "none";
    document.getElementById("winner-info").style.display = "block";
    document.getElementById("winner-message").innerText = `${winner} wins!`;
}
