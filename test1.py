import numpy as np
gamePGN = ""

gameOn = True
#dictionary with user inputs and corresponding commands
cmdDictionary = {"help": "helpCmd()",
                 "quit": "gameOn = False",
                 "rules": "rulesCmd()",
                 "start game": "startCmd()",
                 "display board": "displayBoard(piece_positions)",
                 "display empty board": "displayBoard()",
                 "move": "attemptMove(coords,desiredCoords)",
                 "reset board": "piece_positions = setUpPieces()",
                 "show PGN":"pgnCmd()"
}

#print the current board
def displayBoard(piece_positions=np.full((8,8)," ")): 
    board = createBackground() #creates background for the board
    emptyLine = "\n  |---|---|---|---|---|---|---|---|\n"
    outputDisplay = ""
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
            continue #don't add anything to legal moves
        try:
            if pieceColor == "b" and piecePositions[pieceY+1,pieceX+xOffset] == " " and pieceX+xOffset >= 0: #if this is a legal move for black and the legal move is on the board
                emptyAdjacent.append((pieceY,pieceX,pieceY+1,pieceX+xOffset)) #append the piece and a possible location
        except: #a possible peice's location has a coordinate 8 (off the board)
            continue #don't add anything to legal moves
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
    if (gamePGN.count("\n")%2 == 0 and piece_positions[pieceY,pieceX].lower() == 'b') or (gamePGN.count("\n")%2 == 1 and piece_positions[pieceY,pieceX].lower() == 'r'):
        print("chessbot: You cannot move this piece, it is not that player's turn.")
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
        else:
            print("chessbot: this isn't a valid move")
    elif piece_positions[pieceY,pieceX] in ('R','B'):
        pMoves = checkKingPieceMoves(piece_positions,coords)
        if (pieceY, pieceX, destY, destX) in pMoves:
            piece_positions[destY,destX] = piece_positions[pieceY,pieceX]
            piece_positions[pieceY,pieceX] = " "
            displayBoard(piece_positions)
            gamePGN = updatePGN(gamePGN, pieceY,pieceX,destY,destX)
        else:
            print("chessbot: this isn't a valid move")

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
    if PGN.count("\n") < 9: #add 0 for 1 digit number moves
        PGN+="0"
    PGN+=str(PGN.count("\n")+1)+". " #add move number
    PGN+='B ' if PGN.count("\n") %2 else 'R ' #add player
    PGN+=pX+str(pY)+dX+str(dY) #add coordinates
    for flag in flags:
      PGN+=flagDict[str(flag)] #add flags
    return PGN+"\n"

#USER COMMANDS FROM HERE ON
def helpCmd():
    print("COMMANDS:\n    quit: closes game\n    rules: prints rules\n    start game: starts a game\n    display board: displays the checkers board\n    display empty board: displayes an empty chess board(temporary command)\n    reset board: resets the board")

def rulesCmd():
    print("chessbot: the rules for our checkers game should be here")

def startCmd():
    global piece_positions
    piece_positions = setUpPieces()
    displayBoard(piece_positions)

def pgnCmd():
    print(gamePGN)

#checkOnePieceMoves(piece_positions,[2,1])
print("chessbot: hello! welcome to PGSS checkers!")
print("chessbot: for commands and rules, type \"help\"")
while gameOn: #prompt user for input and execute user's commands until stopped
    #print(gameOn)
    userCmd = input("you: ")
    #try:
    if userCmd[:4] == "move": #if a move is being made
        userCoords = convertCoords(userCmd[5:7])
        userDestination = convertCoords(userCmd[8:10])
        attemptMove(userCoords,userDestination)
    elif userCmd[:5] == "paste": #if a PGN is being pasted
        gamePGN = userCmD[5:]
        print(gamePGN)
    else:
        exec(cmdDictionary[userCmd]) #execute user's command
    #except:
        #print("chessbot: "+userCmd+" isn't a valid command. If you are trying to display a board, make sure you have started a game")
