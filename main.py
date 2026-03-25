from flask import Flask, render_template, jsonify, request
import random, webbrowser, components

app = Flask(__name__)

playerBoard = None
AIBoard = None
gameOverFlag = False
playerAttacks = set()
AIAttacks = set()
AIDIfficulty = "easy"
AIHitTargets = []
shipsDict = {'Aircraft_Carrier': 5, 'Battleship': 4, 'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2}

@app.route('/placement', methods=['GET', 'POST'])
def placementInterface():
    global playerBoard, AIBoard, AIDIfficulty
    if request.method == 'GET':
        #render the placement interface where the user can place their ships
        return render_template('placement.html', ships=shipsDict, board_size=10, difficulties=["easy", "hard"])
    if request.method == 'POST':
        #initialise the boards and process the ship placement from user input
        data = request.get_json()
        playerBoard = components.initialise_board()
        AIBoard = components.initialise_board()
        AIDIfficulty = data.pop('difficulty', 'easy')
        for ship, (x, y, orientation) in data.items():
            shipSize = shipsDict[ship]
            #place the ships horizontally or vertically based on orientation
            if orientation == 'h':
                for i in range(shipSize):
                    playerBoard[int(y)][int(x) + i] = ship
            else:
                for i in range(shipSize):
                    playerBoard[int(y) + i][int(x)] = ship
        placeAIShips()
        return jsonify({'message': 'Received'}), 200

#place ships randomly for the ai player
def placeAIShips():
    global AIBoard
    for ship, size in shipsDict.items():
        placed = False
        while not placed:
            #easy mode: choose random coordinates and orientation for placement
            if AIDIfficulty == "easy":
                AIX, AIY = random.randint(0, 9), random.randint(0, 9)
                #0 = horizontal, 1 = vertical
                orientation = random.randint(0,1)
            #hard mode: cluster ships together as optimal strategy
            if AIDIfficulty == "hard":
                AIX, AIY = random.randint(2, 7), random.randint(2, 7)
                #0 = horizontal, 1 = vertical
                orientation = random.randint(0,1)
            #check if horizontal placement is valid
            eligible = True
            #check if all squares for horizontal placement are empty and within the board
            if orientation == 0 and AIX + size <= 10:
                for i in range(size):
                    if AIBoard[AIY][AIX + i] is not None:
                        eligible = False
                if eligible:
                    for i in range(size):
                        #place the ship horizontally
                        AIBoard[AIY][AIX + i] = ship
                    placed = True
            #check if all squares for vertical placement are empty and within the board
            elif orientation == 1 and AIY + size <= 10:
                for i in range(size):
                    if AIBoard[AIY + i][AIX] is not None:
                        eligible = False
                if eligible:
                    for i in range(size):
                        #place the ship vertically
                        AIBoard[AIY + i][AIX] = ship
                    placed = True


@app.route('/')
def root():
    global playerBoard
    #render the placement interface if the player board is not initialised
    if playerBoard is None:
        return render_template('placement.html', ships=shipsDict, board_size=10, difficulties=["easy", "hard"])
    #render the main game interface otherwise
    return render_template('main.html', player_board=playerBoard)

@app.route('/attack', methods=['GET'])
def processAttack():
    global playerBoard, AIBoard, gameOverFlag, playerAttacks, AIAttacks, AIHitTargets
    x, y = int(request.args.get('x')), int(request.args.get('y'))
    #if the player attacks a previously targeted location, notify them
    if (x, y) in playerAttacks:
        return jsonify({'hit': False, 'AI_Turn': (None, None), 'warning': 'You already attacked this spot!'}), 200
    #process player attack and check if it hits a ship
    hit = AIBoard[y][x] not in [None, 'hit', 'miss']
    if hit:
        AIBoard[y][x] = 'hit'
        playerAttacks.add((x, y))
    else:
        AIBoard[y][x] = 'miss'
    playerAttacks.add((x, y))
    #generate ai's attack and process its result
    AIX, AIY = generateAIAttack()
    AIHit = playerBoard[AIY][AIX] not in [None, 'hit', 'miss']
    if AIHit:
        playerBoard[AIY][AIX] = 'hit'
        AIHitTargets.append((AIX, AIY))
    else:
        playerBoard[AIY][AIX] = 'miss'
    AIAttacks.add((AIX, AIY))
    #check if the game is over
    playerRemainingShips = components.countRemainingShips(playerBoard)
    AIRemainingShips = components.countRemainingShips(AIBoard)
    if playerRemainingShips == 0 or AIRemainingShips == 0:
        gameOverFlag = True
        #notify player who wins
        return jsonify({'hit': hit, 'AI_Turn': (AIX, AIY), 'finished': f'Game Over! {"Player wins!" if AIRemainingShips == 0 else "AI wins!"}'}), 200
    return jsonify({'hit': hit, 'AI_Turn': (AIX, AIY)}), 200

#generate the ai's attack coordinates
def generateAIAttack():
    global AIHitTargets
    #easy mode: choose a random untargeted cell OR previous shot wasnt a hit in hard mode
    if AIDIfficulty == "easy" or not AIHitTargets:
        while True:
            x, y = random.randint(0, 9), random.randint(0, 9)
            if (x, y) not in AIAttacks:
                AIAttacks.add((x, y))
                return x, y
    #hard mode: target adjacent cells to previous hits
    lastHit = AIHitTargets[-1]
    #array of possible next moves based on current location
    possibleMoves = [
        (lastHit[0] + 1, lastHit[1]),
        (lastHit[0] - 1, lastHit[1]),
        (lastHit[0], lastHit[1] + 1),
        (lastHit[0], lastHit[1] - 1)
    ]
    for move in possibleMoves:
        if 0 <= move[0] < 10 and 0 <= move[1] < 10 and move not in AIAttacks:
            AIAttacks.add(move)
            return move
    #if no valid adjacent moves, backtrack and retry
    AIHitTargets.pop()
    return generateAIAttack()

#automatically open the game interface in a browser when the app starts
if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run()
