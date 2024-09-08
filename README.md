Overview

This project is a simple game developed using Pygame and OpenCV. The objective of the game is to catch a butterfly with your hand using hand tracking technology. The game records scores and maintains a leaderboard to display the top three scores.

Features

    Hand Tracking: Utilizes OpenCV and CVZone's Hand Tracking module to detect hand movements.
    Butterfly Catching: Player controls a hand to catch a butterfly that moves upward.
    Leaderboard: Maintains a leaderboard to track and display the top three scores.
    Game Duration: The game runs for a fixed duration of 30 seconds.

Installation

git clone https://github.com/shreeharini-261/Opencv_Game.git


Install Dependencies:

    Ensure you have Python 3.x installed.
    Install the required packages using pip: 
    pip install pygame opencv-python numpy cvzone

Code Explanation

    project_1.py:
        Initializes Pygame and OpenCV.
        Displays the leaderboard and prompts the player to enter their name.
        Runs the main game loop, detecting hand movements and updating scores.
        Displays the final score and updates the leaderboard.

    leaderboard_1.py:
        Contains functions to load, save, and update the leaderboard stored in leaderboard_1.json.

    leaderboard_1.json:
        JSON file for storing leaderboard data, including player names and scores.

