import numpy as np

gameOn = True
cmdDictionary = {"help": "helpCmd()", #list of user commands
                 "quit": "gameOn = False",
                 "rules": "rulesCmd()",
                 "start game": "startCmd()",
                 "display board": "displayBoard(piece_positions)",
                 "display empty board": "displayBoard()",
                 "move" : "attemptMove(coords,desiredCoords)"
}

def displayBoard(piece_positions=np.full((8,8)," ")): #print board
    board = createBackground() #creates background for the board
    emptyLine = "\n  |---|---|---|---|---|---|---|---|\n"
    outputDisplay = ""
    for i, row in enumerate(board, start=0):
        outputDisplay+=emptyLine
        outputDisplay+=str(i+1)+" "
        for j, pieceEntry in enumerate(row, start=0):
            if piece_positions[i,j] == " ": #if there isn't a piece at this position...
                outputDisplay+=("| "+pieceEntry+" ") #...print the background
            else:
                outputDisplay+=("| "+piece_positions[i,j]+" ") #...print that piece instead of the background
        outputDisplay+="|"
    outputDisplay+=emptyLine
    outputDisplay+="    a   b   c   d   e   f   g   h"
    print(outputDisplay)
   
def createBackground(): #creates background for the board
    outputBackground = np.full((8,8), ".")
    outputBackground[::2,::2] = " "
    outputBackground[1::2,1::2] = " "
    return outputBackground

def setUpPieces(): #creates 8x8 array of piece chars
    pieceOutput = np.full((8,8), " ")
    pieceOutput[0,1::2] = "B"
    pieceOutput[1,::2] = "B"
    pieceOutput[2,1::2] = "B"
    pieceOutput[5,::2] = "R"
    pieceOutput[6,1::2] = "R"
    pieceOutput[7,::2] = "R"
    return pieceOutput

def checkOnePieceMoves(piecePositions,coords):
    pieceColor = piecePositions[coords[0],coords[1]]
    emptyAdjacent = []
    pieceX = coords[1]
    pieceY = coords[0]
    for xOffset in range(-1,2,2): 
        try:
          if pieceColor == "R" and piecePositions[pieceY-1,pieceX+xOffset] == " " and pieceX+xOffset >= 0: #if this is a legal move for red and the legal move is on the board
              emptyAdjacent.append((pieceY,pieceX,pieceY-1,pieceX+xOffset)) #append the piece and a possible location
        except: #a possible peice's location has a coordinate 8 (off the board)
            continue #don't add anything to legal moves
        try:
            if pieceColor == "B" and piecePositions[pieceY+1,pieceX+xOffset] == " " and pieceX+xOffset >= 0: #if this is a legal move for black and the legal move is on the board
                emptyAdjacent.append((pieceY,pieceX,pieceY+1,pieceX+xOffset)) #append the piece and a possible location
        except: #a possible peice's location has a coordinate 8 (off the board)
            continue #don't add anything to legal moves
        return emptyAdjacent
#possible moves are stored in the following format:
#piece's current Y, piece's current X, piece's possible new Y, piece's possible new X
#the origin is at the top left corner. So the top right corner is (7,0) and the bottom left corner is (0,7)
#each move is a list containing that information, so emptyAdjacent is a list of lists
  
def attemptMove(coords, desiredCoords):
    pieceY, pieceX = coords
    destY, destX = desiredCoords
    pMoves = checkOnePieceMoves(piece_positions,coords)
    if (pieceY, pieceX, destY, destX) in pMoves:
        piece_positions[destY,destX] = piece_positions[pieceY,pieceX]
        piece_positions[pieceY,pieceX] = " "
    else:
        print("This is not a valid move")
    displayBoard(piece_positions)

def convertCoords(coordStr):
    output = []
    for item in coordStr:
        if item.isdigit(): #item contains a digit
            output.append(8-int(item))
        else: #item contains a chr
            output.append(ord(item)-97)
    return output[::-1]
#a has an ascii value of 97, increments by 1 for following letters

#USER COMMANDS FROM HERE ON
def helpCmd():
    print("COMMANDS:\n    quit: closes game\n    rules: prints rules\n    start game: starts a game\n    display starting board: displays a chess board with pieces in their starting positions(temporary command)\n    display empty board: displayes an empty chess board(temporary command)")

def rulesCmd():
    print("chessbot: the rules for our checkers game should be here")

def startCmd():
    print("chessbot: this function could start a game, but it hasn't been written yet")

piece_positions = setUpPieces()
#checkOnePieceMoves(piece_positions,[2,1])
print("chessbot: hello! welcome to PGSS checkers!")
print("chessbot: for commands and rules, type \"help\"")
while gameOn: #prompt user for input and execute user's commands until stopped
    userCmd = input("you: ")
    try:
        if userCmd[:4] == "move": #if a move is being made
            userCoords = convertCoords(userCmd[5:7])
            userDestination = convertCoords(userCmd[8:10])
            attemptMove(userCoords,userDestination)
        else:
            exec(cmdDictionary[userCmd]) #execute user's command
    except:
        print("chessbot: "+userCmd+" isn't a valid command")

