import components, random

#create a dictionary to store player data
players = {}
username = ""
AIUsername = "AI"

#function to initialise the players and their boards
def initialise_players():
    global username 
    #get the username from the player
    username = input("Enter your username: ").strip()
    #initialise the player
    board = components.initialise_board()
    ships = components.create_battleships()
    #store the player's board and ships in the players dictionary
    players[username] = {"board": board, "ships": ships}
    
    #initialise the ai
    AIBoard = components.initialise_board()
    AIShips = components.create_battleships()
    players[AIUsername] = {"board": AIBoard, "ships": AIShips}
    
    components.place_battleships(players[username]["board"], players[username]["ships"], algorithm="custom")
    components.place_battleships(players[AIUsername]["board"], players[AIUsername]["ships"], algorithm="random")
        
def generate_attack(board_size = 10):
    #generate a random coordinate inside the board
    row = random.randint(0, board_size - 1)
    column = random.randint(0, board_size - 1)
    return row, column

def attack(coordinates, player_name, opponent_name):
    row, column = coordinates
    target = players[opponent_name]["board"][row][column]
    
    #check if the target contains a ship
    if target is not None:
        #notify the player of a hit
        print(f"Hit {target} at position {coordinates}!")
        players[opponent_name]["board"][row][column] = None
        #decrease the health of the hit ship
        players[opponent_name]["ships"][target] -= 1
        
        #check if the ship has been completely sunk
        if players[opponent_name]["ships"][target] == 0:
            #notify the player that they sunk a ship
            print(f"You sunk {target}!")
            return True
    else:
        print(f"Miss at position {coordinates}!")
        return False

#function to get attack coordinates from the player
def cli_coordinates_input():
    while True:
        #prompt the player to enter coordinates
        userInput = input("Enter coordinates (row, column)").strip()
        #sanitise the input
        userInput = userInput.strip("()")
        row, column = map(int, userInput.split(","))
        return row, column

def print_board(board):
    for line in board:
        print(" ".join([str(cell) if cell else '.' for cell in line]))

def ai_opponent_game_loop():
    #display a welcome message
    print("Welcome to Battleships!")
    #initialise the player
    initialise_players()
    totalShipsUser = len(players[username]["ships"])
    sunkShipsUser = 0
    #get the total number of ships for the ai
    totalShipsAI = len(players[AIUsername]["ships"])
    #track the number of ai ships sunk
    sunkShipsAI = 0
    
    while (sunkShipsUser < totalShipsUser) and (sunkShipsAI < totalShipsAI):
        print(f"{username}'s turn:")
        #get attack coordinates from the player
        coords = cli_coordinates_input()
        #process the attack
        hit = attack(coords, username, AIUsername)
        
        if hit:
            sunkShipsAI += 1
        
        #swap to ai turn if the user still has ships
        if sunkShipsUser < totalShipsUser:
            print("Enemy's turn:")
            #generate random attack coordinates for the ai
            ai_coords = generate_attack()
            print(f"The enemy attacks at {ai_coords}")
            #process the ai's attack
            hit = attack(ai_coords, AIUsername, username)
            print_board(players[username]["board"])
               
            if hit:
                sunkShipsUser += 1
    
    #determine the outcome of the game
    if sunkShipsUser == totalShipsUser:
        #display that the user lost if they have no ships left
        print("Game over, you have lost. The Enemy wins!")
    else:
        #display player win
        print("Game over, you have won. Congratulations!")
        
if __name__ == "__main__":
    ai_opponent_game_loop()
