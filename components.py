import random, json, os

#function to return the location of a given file (for some reason just writing the name of the file wouldn't work DESPITE being in the same working directory????)
def getFileLocation(fileToGet):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), fileToGet)

def initialise_board(size = 10):
    #list comprehension to create 10 empty lists of size 10 (10x10 grid)
    board = [[None for _ in range(size)] for _ in range(size)]
    return board

#create battleships from file
def create_battleships(filename = getFileLocation("battleships.txt")):
    battleships = {}
    file = open(filename, "r")
    for line in file:
        parts = line.strip().split(",")
        if parts.__len__() == 2:
            #the file is structured like (Aircraft Carrier,5), so split each line into the ships name and its size
            name, size = parts[0], parts[1]
            #set each ship to have its size
            battleships[name] = int(size)                
    return battleships

def place_battleships(board, ships, algorithm="simple", placementShipFile = getFileLocation("placement.json")):
    #three sub-functions in a case-swap sort of thing dependent on what algorithm is chosen by the user
    def simple_placement():
        row = 0
        #place ships in first available slot
        for ship, shipSize in ships.items():
            if row < board.__len__():
                for column in range(min(shipSize, board[row].__len__())):
                    #assign the null slots in the board to the ship
                    board[row][column] = ship
                row += 1
    #random placement will place the ships in a random spot and orientation
    def random_placement():
        for ship, shipSize in ships.items():
            #flag that we can call later
            placed = False
            while not placed:
                #0 = horizontal, 1 = vertical
                orientation = random.randint(0,1)
                #if horizontal..
                if orientation == 0:
                    #assign some limits so that the boat cannot be placed outside the board
                    row = random.randint(0, board.__len__() - 1)
                    column = random.randint(0, board.__len__() - shipSize)
                    #another flag, this time to make sure its an eligible placement
                    eligible = True
                    #check every square of the ship
                    for i in range(shipSize):
                        #if one is found to not fit inside the board, the flag is called and therefore is not placed
                        if board[row][column + i] is not None:
                            eligible = False
                    if eligible:
                        for i in range(shipSize):
                            #place the ship in its position
                            board[row][column + i] = ship
                        placed = True
                #if vertical...
                elif orientation == 1:
                    #assign limits
                    row = random.randint(0, board.__len__() - shipSize)
                    column = random.randint(0, board.__len__() - 1)
                    #flag
                    eligible = True
                    #check every square of ship
                    for i in range(shipSize):
                        if board[row + i][column] is not None:
                            #call flag if it doesnt fit
                            eligible = False
                    if eligible:
                        for i in range(shipSize):
                            #place ship
                            board[row + i][column] = ship
                        placed = True
    #custom placement so that the user can use the JSON file to place ships wherever they fancy
    def custom_placement():
        with open(placementShipFile, "r") as file:
            #read the contents of the file into the config
            placementConfig = json.load(file)
        #place the ships based on the configuration in the JSON file
        for ship, coords in placementConfig.items():
            for i in coords:
                row, column = i
                if (0 <= row < board.__len__()) and (0 <= column < board.__len__()):
                    board[row][column] = ship
    
    #a dictionary of the functions so that the correct one can be called
    procedureMap = {
        "simple": simple_placement,
        "random": random_placement,
        "custom": custom_placement
        
    }
    
    #call the function
    if algorithm in procedureMap:
        procedureMap[algorithm]()

    return board  


#this is for the flask implementation

#function to count how many ship cells remain unsunk on the board
def countRemainingShips(board):
    return sum(1 for row in board for cell in row if cell not in [None, 'hit', 'miss'])
    