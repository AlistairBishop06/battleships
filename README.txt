Battleships is a Python-based implementation of the classic strategy game. This version features a command-line player vs AI mode with additional web-based placement functionality using Flask.

Features Completed:

1. Battleships as a Python application
	- Initialise Board
	- Create Battleships
	- Place Battleships
	- Attack
	- Command-Line Input for Attack Coordinates
	- Simple Game Loop
2. Multi-player Constructs
	- Players
	- AI Opponent
	- Ai Opponent Command-Line Game Loop
3. Graphical User Interface using Flask
	- Battleship Placement Page
	- Gameplay Page
4. Optional Extra Challenges
	- Difficulty Levels
	- Improved AI Ship Placement and Guessing

Usage:
To play the simple battleships application where the player can only guess enemy positions, run the following line in the terminal at the root directory:
py game_engine.py

To play the command-line interface adaptation of battleships, use the placement.json file to configure your placements of the ships and then run the following line in the terminal at the root directory:
py mp_game_engine.py

To play battleships with the Flask-based GUI, run the following line in the terminal at the root directory:
py main.py


Self-Assessment:

Overall, I think this project went well – with all the required features being complete. At the start of the project, I felt like I didn’t struggle to come up with solutions to the basic and command line interface versions of the game, completing them quickly and effectively. However, since I have never used Flask before, nor made a web interface – my progress slowed down significantly within that stage. It took a lot of research, testing and redesign to create the working GUI, with many bugs along the way, such as double clicking a square to remove its hit registration, or the ai guessing outside of the grid, but ultimately these were ironed out and a successful project was created. I also managed to add a difficulty selector, making a more comprehensive AI that has better ship placement and chooses coordinates adjacent to other hits. However, I was unsuccessful in creating a multi-player implementation on remote devices, this is simply due to having little experience doing this before, but if I had more time or stronger guidance, this would be something I would want to do in the future. Ultimately, I am happy with the end result.