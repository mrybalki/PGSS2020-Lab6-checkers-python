import numpy as np
gamePGN = ""

gameOn = True
#dictionary with user inputs and corresponding commands
cmdDictionary = {"help": "helpCmd()",
                 "quit": "gameOn = False",
                 "rules": "rulesCmd()",
                 "start new game": "startCmd()",
                 "display board": "displayBoard(piece_positions)",
                 "reset board": "piece_positions = setUpPieces()",
                 "show PGN": "pgnCmd()",
                 "resign": "resignCmd()",
                 "analyze": "analyzeCmd()"
}

#dictionary with user commands available in the game analyzer
analyzeDictionary = {"help": "helpAnalyze()",
                     "show PGN": cmdDictionary["show PGN"]
}

#print the current board
def displayBoard(piece_positions=np.full((8,8)," "),playing=True): 
    board = createBackground() #creates background for the board
    emptyLine = "\n  |---|---|---|---|---|---|---|---|\n"
    outputDisplay = "CURRENT GAME:" if playing else "GAME ANALYZER:"
    for i, row in enumerate(board, start=0):
        outputDisplay+=emptyLine
        outputDisplay+=str(8-i)+" "
        for j, pieceEntry in enumerate(row, start=0):
            if piece_positions[i,j] == " ": #if there isn't a piece at this position...
                outputDisplay+=("| "+pieceEntry+" ") #...print the background
            else:
                outputDisplay+=("| "+piece_positions[i,j]+" ") #...print that piece instead of the background
        outputDisplay+="|"
    outputDisplay+=emptyLine
    outputDisplay+="    a   b   c   d   e   f   g   h"
    print(outputDisplay)
   
#creates background for the board (called in displayBoard())
def createBackground(): 
    outputBackground = np.full((8,8), ".")
    outputBackground[::2,::2] = " "
    outputBackground[1::2,1::2] = " "
    return outputBackground

#creates 8x8 array of piece chars
def setUpPieces(): 
    pieceOutput = np.full((8,8), " ")
    pieceOutput[0,1::2] = "b"
    pieceOutput[1,::2] = "b"
    pieceOutput[2,1::2] = "b"
    pieceOutput[5,::2] = "r"
    pieceOutput[6,1::2] = "r"
    pieceOutput[7,::2] = "r"
    #pieceOutput[0,1] = 'b'
    #pieceOutput[2,7] = 'r'
    return pieceOutput

#returns all possible moves a normal piece can make
def checkNormalPieceMoves(piecePositions,coords): 
    pieceColor = piecePositions[coords[0],coords[1]]
    emptyAdjacent = []
    pieceY = coords[0]
    pieceX = coords[1]
    for xOffset in range(-1,2,2): 
        try:
            if pieceColor == "r" and piecePositions[pieceY-1,pieceX+xOffset] == " " and pieceX+xOffset >= 0: #if this is a legal move for red and the legal move is on the board
                emptyAdjacent.append((pieceY,pieceX,pieceY-1,pieceX+xOffset)) #append the piece and a possible location
        except: #a possible peice's location has a coordinate 8 (off the board)
            print("checkerbot: this isn't a valid move.")
        try:
            if pieceColor == "b" and piecePositions[pieceY+1,pieceX+xOffset] == " " and pieceX+xOffset >= 0: #if this is a legal move for black and the legal move is on the board
                emptyAdjacent.append((pieceY,pieceX,pieceY+1,pieceX+xOffset)) #append the piece and a possible location
        except: #a possible peice's location has a coordinate 8 (off the board)
            print("checkerbot: this isn't a valid move.")
    return list(emptyAdjacent)
#possible moves are stored in the following format:
#piece's current Y, piece's current X, piece's possible new Y, piece's possible new X
#the origin is at the top left corner. So the top right corner is (0,7) and the bottom left corner is (7,0)
#each move is a list containing that information, so emptyAdjacent is a list of lists

#returns all possible moves a king could make
def checkKingPieceMoves(piecePositions,coords):
    emptyAdjacent = []
    pieceY = coords[0]
    pieceX = coords[1]
    for xOffset in range(-1,2,2):
        for yOffset in range(-1,2,2):
            try:
                if piecePositions[pieceY+yOffset,pieceX+xOffset] == " " and pieceY+yOffset >= 0 and pieceX+xOffset >=0: #an adjacent space is empty
                    emptyAdjacent.append((pieceY,pieceX,pieceY+yOffset,pieceX+xOffset))
            except: #a piece's possible new location is off the board
                continue #do nothing
    return list(emptyAdjacent)

#if a normal piece has reached the end of the board, it is replaced with a king
def checkPromote(desiredCoords):
    dY, dX = desiredCoords
    if piece_positions[dY,dX] == 'r' and desiredCoords[0] == 0: #red peice has reached the top of the board
        piece_positions[dY,dX] = 'R' #king
        return True
    if piece_positions[dY,dX] == 'b' and desiredCoords[0] == 7: #black piece has reached the bottom of the board
        piece_positions[dY,dX] = 'B' #king
        return True
    return False

#attempts a player's move
def attemptMove(coords, desiredCoords):
    global gamePGN
    pieceY, pieceX = coords
    destY, destX = desiredCoords
    if (gamePGN.count(".")%2 == 0 and piece_positions[pieceY,pieceX].lower() == 'b') or (gamePGN.count(".")%2 == 1 and piece_positions[pieceY,pieceX].lower() == 'r'):
        print("checkerbot: You cannot move this piece, it is not that player's turn.")
        return None
    if piece_positions[pieceY,pieceX] in ('r','b'):
        pMoves = checkNormalPieceMoves(piece_positions,coords)
        if (pieceY, pieceX, destY, destX) in pMoves:
            piece_positions[destY,destX] = piece_positions[pieceY,pieceX]
            piece_positions[pieceY,pieceX] = " "
            if checkPromote(desiredCoords):
                gamePGN = updatePGN(gamePGN, pieceY,pieceX,destY,destX,["move","king"])
            else:
                gamePGN = updatePGN(gamePGN, pieceY,pieceX,destY,destX)
            displayBoard(piece_positions)
        else: #this move cannot be made with the piece
            print("checkerbot: this isn't a valid move.")
    elif piece_positions[pieceY,pieceX] in ('R','B'):
        pMoves = checkKingPieceMoves(piece_positions,coords)
        if (pieceY, pieceX, destY, destX) in pMoves:
            piece_positions[destY,destX] = piece_positions[pieceY,pieceX]
            piece_positions[pieceY,pieceX] = " "
            displayBoard(piece_positions)
            gamePGN = updatePGN(gamePGN, pieceY,pieceX,destY,destX)
        else: #this move cannot be made with the piece
            print("checkerbot: this isn't a valid move.")
    else: #empty tile is selected
        print("checkerbot: this isn't a valid move.")

#converts between user coordinates and array indices
def convertCoords(coordStr,toIndices = True):
    output = []
    if toIndices:
        for item in coordStr:
            if item.isdigit(): #item is a digit
                output.append(8-int(item))
            else: #item is a chr
                output.append(ord(item)-97)
    elif not toIndices:
        output.append(8-int(coordStr[0]))
        output.append(chr(int(coordStr[1])+97))
    return output[::-1]      
#a has an ascii value of 97, increments by 1 for following letters

#updates the record of all moves played in a game
def updatePGN(PGN,pY,pX,dY,dX,flags=["move"]):
    flagDict = {"move":"m",
                "take":'t',
                "king":'k'}
    pX, pY = convertCoords(str(pY)+str(pX),False)
    dX, dY = convertCoords(str(dY)+str(dX),False)
    if PGN.count(".") < 9: #add 0 for 1 digit number moves
        PGN+="0"
    PGN+=str(PGN.count(".")+1)+"." #add move number
    PGN+=pX+str(pY)+dX+str(dY) #add coordinates
    for flag in flags:
      PGN+=flagDict[str(flag)] #add flags
    return PGN+","

#USER COMMANDS FROM HERE ON
def helpCmd():
    print("checkerbot: commands...\n    quit: closes game\n    rules: prints rules\n    start new game: starts a game\n    display board: displays the checkers board\n    reset board: resets the board\n    show PGN: prints the current saved PGN\n    move __ __: moves a checkers piece after a game is started. enter the current coordinates of the piece first, and the desired coordinates of the piece second. (ex: move a3 b4)\n    paste __: pastes in a checkers PGN for later analysis. Make sure that the PGN is in the format (move number).(piece's old coordinate)(piece's new coordinate)(move flag), ... and so on with no spaces. (ex: 01.a3b4m,02.b6a5m ...). This command will restart any games in progress.\n    analyze: opens the game analyzer, using the current PGN")

def rulesCmd():
    print("checkerbot: the rules for our checkers game should be here.")

def startCmd():
    global piece_positions
    piece_positions = setUpPieces()
    displayBoard(piece_positions)

def pgnCmd():
    print("checkerbot: the current PGN is\n    "+gamePGN)

def resignCmd():
    piece_positions = setUpPieces()
    loser, winner = ("Red Player","Black Player") if gamePGN.count(".") % 2 == 0 else ("Black Player","Red Player")
    print("checkerbot: "+loser+" resigns, "+winner+" wins!")

def analyzeCmd():
    if len(gamePGN) == 0:
        print("checkerbot: no PGN to analyze. Play a game of checkers or use the paste command to analyze an existing PGN.")
    else: #we have a PGN
        analyzing = True
        piece_positions = setUpPieces()
        displayBoard(piece_positions,playing=False)
        while analyzing:
            userCmd = input("you: ")
            if userCmd == "quit":
                analyzing = False
            else:
                exec(analyzeDictionary[userCmd])
        print("checkerbot: exiting analyzer...")

def helpAnalyze():
    print("checkerbot: analyzer commands...\n    quit: exits the analyzer\n    n: moves to the next move in the game\n    b: moves to the previous move in the game\n    show PGN: prints the entire PGN being analyzed")


#checkOnePieceMoves(piece_positions,[2,1])
print("checkerbot: hello! welcome to PGSS checkers!")
print("checkerbot: for commands and rules, type \"help\".")
while gameOn: #prompt user for input and execute user's commands until stopped
    #print(gameOn)
    userCmd = input("you: ")
    try:
        if userCmd[:4] == "move": #if a move is being made
            userCoords = convertCoords(userCmd[5:7])
            userDestination = convertCoords(userCmd[8:10])
            attemptMove(userCoords,userDestination)
        elif userCmd[:5] == "paste": #if a PGN is being pasted
            gamePGN = userCmd[6:]
            print("checkerbot: PGN recieved starting with "+gamePGN[:8]+"...")
            piece_positions = setUpPieces()
        else: #some other command is entered
            exec(cmdDictionary[userCmd]) #execute user's command
    except:
        print("chessbot: "+userCmd+" isn't a valid command. If you are trying to display a board, make sure you have started a game")
print("checkerbot: exiting PGSS chess...")
