# Import the modules
import tkinter
import random
from tkinter import messagebox

# List of possible colors
colours = ['Red', 'Blue', 'Green', 'Pink', 'Black',
           'Yellow', 'Orange', 'White', 'Purple', 'Brown']
scores = [0, 0]  # Scores for Player 1 and Player 2
timeleft = 30
current_player = 0  # Player 1 starts (0 for Player 1, 1 for Player 2)

# Function that will start the game
def startGame(event):
    global timeleft
    if timeleft == 30:
        # Start the countdown timer
        countdown()
    # Run the function to choose the next color
    nextColour()

# Function to choose and display the next color
def nextColour():
    global scores, timeleft, current_player

    # If a game is currently in play
    if timeleft > 0:
        # Make the text entry box active
        e.focus_set()

        # Check if the color typed is correct
        if e.get().lower() == colours[1].lower():
            scores[current_player] += 1

        # Clear the text entry box
        e.delete(0, tkinter.END)

        # Shuffle and display the next color
        random.shuffle(colours)
        label.config(fg=str(colours[1]), text=str(colours[0]))

        # Update the score
        scoreLabel.config(
            text=f"Player 1: {scores[0]} | Player 2: {scores[1]}")

        # Switch to the next player
        current_player = 1 - current_player
        instructions.config(text=f"Player {current_player + 1}'s turn! Type the color of the word.")

# Countdown timer function
def countdown():
    global timeleft

    # If a game is in play
    if timeleft > 0:
        # Decrement the timer
        timeleft -= 1

        # Update the time left label
        timeLabel.config(text="Time left: " + str(timeleft))

        # Run the function again after 1 second
        timeLabel.after(1000, countdown)
    else:
        # End the game and display the winner
        endGame()

# Function to end the game
def endGame():
    if scores[0] > scores[1]:
        winner = "Player 1"
    elif scores[1] > scores[0]:
        winner = "Player 2"
    else:
        winner = "No one! It's a tie!"

    # Show the victory popup
    messagebox.showinfo("Game Over", f"Time's up! {winner} wins!")
    root.quit()

# Driver Code

# Create a GUI window
root = tkinter.Tk()

# Set the title
root.title("COLORGAME")

# Set the size
root.geometry("500x300")

# Add an instructions label
instructions = tkinter.Label(root, text="Press Enter to start Player 1's turn!",
                              font=('Helvetica', 12))
instructions.pack()

# Add a score label
scoreLabel = tkinter.Label(root, text="Player 1: 0 | Player 2: 0",
                           font=('Helvetica', 12))
scoreLabel.pack()

# Add a time left label
timeLabel = tkinter.Label(root, text="Time left: " +
                          str(timeleft), font=('Helvetica', 12))
timeLabel.pack()

# Add a label for displaying the colors
label = tkinter.Label(root, font=('Helvetica', 60))
label.pack()

# Add a text entry box for typing in colors
e = tkinter.Entry(root)

# Run the 'startGame' function when the enter key is pressed
root.bind('<Return>', startGame)
e.pack()

# Set focus on the entry box
e.focus_set()

# Start the GUI
root.mainloop()
