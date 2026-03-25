import components, random

#handle attacks
def attack(coordinates, battleships, board):
    #seperate user input into row and column and initialise it as a target
    row, column = coordinates
    target = board[row][column]
    if target is not None:
        #handle hit if the location in the board is not nothing
        print(f"Hit {target} at position {coordinates}!")
        board[row][column] = None
        #decrement the battleship and if there are no segments left, alert the user they have sunk the ship
        battleships[target] -= 1
        if battleships[target] == 0:
            print(f"You sunk {target}!")
            return True
    else:
        print(f"Miss at position {coordinates}!")
        return False

def cli_coordinates_input():
    while True:
        #ask the user for input
        userInput = input("Enter coordinates (row, column)").strip()
        #sanitise the input
        userInput = userInput.strip("()")
        row, column = map(int, userInput.split(","))
        return row, column
    
def simple_game_loop():
    #welcome screen
    print("Welcome to Battleships!")
    #initialisation
    board = components.initialise_board()
    ships = components.create_battleships()
    board = components.place_battleships(board, ships)
    totalShips = ships.__len__()
    sunkShips = 0
    sunkShipNames = []
    #gameloop to handle if the game ends
    while sunkShips < totalShips:
        coords = cli_coordinates_input()
        #handle attack
        hit = attack(coords, ships, board)
        for ship, size in ships.items():
            #if the ship hasnt already been sunk, identify it as sunk and increment the number of sunk ships
            if size == 0 and ship not in sunkShipNames:
                sunkShips += 1
                sunkShipNames.append(ship)
    
    print("Game Over! All ships have been sunk.")

if __name__ == "__main__":
    simple_game_loop()