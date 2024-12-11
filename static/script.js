let player1Name = "";
let player2Name = "";
let player1Score = 0;
let player2Score = 0;
let timeLeft = 30;
let currentPhase = 1;
let correctColor = "";
let gameInterval = null;

document.getElementById("start-game").addEventListener("click", startGame);
document.getElementById("submit-answer").addEventListener("click", submitAnswer);

function startGame() {
    player1Name = document.getElementById("player1-name").value.trim();
    player2Name = document.getElementById("player2-name").value.trim();

    if (!player1Name || !player2Name) {
        alert("Both players must enter their names.");
        return;
    }

    fetch("/start_game", {
        method: "POST",
        body: new URLSearchParams({ player1_name: player1Name, player2_name: player2Name }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                alert(data.error);
                return;
            }

            correctColor = data.color_word.color;
            document.getElementById("color-word-text").innerText = data.color_word.word;
            document.getElementById("player-input").style.display = "none";
            document.getElementById("game-info").style.display = "block";

            gameInterval = setInterval(updateTime, 1000);
        });
}

function updateTime() {
    timeLeft--;
    document.getElementById("time-left").innerText = timeLeft;

    if (timeLeft === 15) {
        currentPhase = 2;
        document.getElementById("current-phase").innerText = `Player 2's turn!`;
    }

    if (timeLeft <= 0) {
        clearInterval(gameInterval);
        declareWinner();
    }
}

function submitAnswer() {
    const colorInput = document.getElementById("color-input").value.trim();

    fetch("/submit_answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            color_input: colorInput,
            correct_color: correctColor,
            time_left: timeLeft,
            player1_score: player1Score,
            player2_score: player2Score,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            player1Score = data.player1_score;
            player2Score = data.player2_score;

            document.getElementById("player1-score").innerText = player1Score;
            document.getElementById("player2-score").innerText = player2Score;

            fetchNextWord();
        });

    document.getElementById("color-input").value = "";
}

function fetchNextWord() {
    fetch("/next_word", { method: "POST" })
        .then((response) => response.json())
        .then((data) => {
            correctColor = data.color;
            document.getElementById("color-word-text").innerText = data.word;
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
