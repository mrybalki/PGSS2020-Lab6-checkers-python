def legalMoves(piecePositions, playerColor):
  allMoves = []
  for x in range(0, 8):
    for y in range(0, 8):
      if piecePositions[y, x] == playerColor:
        if len(checkNormalPieceMoves(piecePositions, [y,x])) > 0:
            allMoves.append(checkNormalPieceMoves(piecePositions, [y,x]))
  return allMoves
def makeMove(piecePositions, playerColor, pType="Computer",fromCoords = [], toCoords=[]):
    possibleMoves = legalMoves(piecePositions, playerColor) #get all possible moves for this player based on color piece
    if(pType == "Human"):
        hasMoved = False #boolean value to test if move is valid
        for pMove in possibleMoves:
            if(len(pMove) > 1): #since possibleMoves is a list of tuples, check if each index contains more than 1 tuple
                for i in range(0, len(pMove)): #compare all the coordinates of all possible moves
                    if((pMove[i][0] == fromCoords[0] and pMove[i][1] == fromCoords[1]) and (pMove[i][2] == toCoords[0] and pMove[i][3] == toCoords[1])):
                        piecePositions[pMove[0][0], pMove[0][1]] = " " #if matched up move the piece and update that the piece was moved
                        piecePositions[pMove[0][2], pMove[0][3]] = playerColor
                        hasMoved = True
            else:
                if((pMove[0][0] == fromCoords[0] and pMove[0][1] == fromCoords[1]) and (pMove[0][2] == toCoords[0] and pMove[0][3] == toCoords[1])):
                    piecePositions[pMove[0][0], pMove[0][1]] = " "
                    piecePositions[pMove[0][2], pMove[0][3]] = playerColor
                    hasMoved = True
        if(not hasMoved):
            print("Enter valid coordinates!")
    else:
        pos = 0 #similar logic, just that pos and pos2 are ways to identify which tuple in which tuple in the list you want
        pos2 = 0
        bestVal = -10000
        for i in range(0, len(possibleMoves)):
            if(len(possibleMoves[i]) > 1):
                for j in range(0,2):
                    if(bestMove(piecePositions, playerColor, possibleMoves[i][j]) >= bestVal):#compares against best moves and values
                        bestVal = bestMove(piecePositions, playerColor, possibleMoves[i][j])
                        pos = i
                        pos2 = j
            else:
                if(bestMove(piecePositions, playerColor, possibleMoves[i]) >= bestVal):
                    bestVal = bestMove(piecePositions, playerColor, possibleMoves[i])
                    pos = i
                    pos2 = 0
        move = possibleMoves[pos][pos2]
        piecePositions[move[0], move[1]] = " "
        print("Moving from", str(move[0]) + str(move[1]) + " to",  str(move[2]) +  str(move[3]))
        piecePositions[move[2], move[3]] = playerColor
    displayBoard(piecePositions)
def bestMove(piecePositions, playerColor, move):
    #dummy function, always returns 10000 for now
    return 10000
def checkJumps(piecePositions, pieceColor, coords):
    pieceX = coords[1]
    pieceY = coords[0]
    emptyAdjacent = []
    level2jumps = []
    for xOffset in range(-1, 2, 2):
        try:
            if xOffset < 0:
                newOffset = -2
                if pieceColor.upper() == "R" and piecePositions[pieceY-1, pieceX+xOffset].upper() == "B" and piecePositions[pieceY-2, pieceX+newOffset] == " " and pieceX+newOffset >=0:
                    emptyAdjacent.append([pieceY, pieceX, pieceY-2, pieceX+newOffset])
                    temp = checkJumps(piecePositions, pieceColor, [pieceY-2, pieceX+newOffset])
                    if temp:
                        if temp not in level2jumps:
                            level2jumps.append(list(temp))
            else:
                newOffset = 2
                if pieceColor.upper() == "R" and piecePositions[pieceY-1, pieceX+xOffset].upper() == "B" and piecePositions[pieceY-2, pieceX+newOffset] == " " and pieceX+newOffset >=0:
                    emptyAdjacent.append([pieceY, pieceX, pieceY-2, pieceX+newOffset])
                    temp = checkJumps(piecePositions, pieceColor, [pieceY-2, pieceX+newOffset])
                    if temp:
                        if temp not in level2jumps:
                            level2jumps.append(list(temp))
        except:
            continue
        try:
            if xOffset < 0:
                newOffset = -2
                if pieceColor.upper() == "B" and piecePositions[pieceY+1, pieceX+xOffset].upper() == "R" and piecePositions[pieceY+2, pieceX+newOffset] == " " and pieceX+newOffset >=0:
                    emptyAdjacent.append([pieceY, pieceX, pieceY+2, pieceX+newOffset])
                    temp = checkJumps(piecePositions, pieceColor, [pieceY+2, pieceX+newOffset])
                    if temp:
                        if temp not in level2jumps:
                            level2jumps.append(list(temp))
            else:
                newOffset = 2
                if pieceColor.upper() == "B" and piecePositions[pieceY+1, pieceX+xOffset].upper() == "R" and piecePositions[pieceY+2, pieceX+newOffset] == " " and pieceX+newOffset >=0:
                    emptyAdjacent.append([pieceY, pieceX, pieceY+2, pieceX+newOffset])
                    temp =  checkJumps(piecePositions, pieceColor, [pieceY+2, pieceX+newOffset])
                    if temp:
                        if temp not in level2jumps:
                            level2jumps.append(list(temp))
        except:
            continue
    if not level2jumps and not emptyAdjacent:
        return []
    else:
        for l in level2jumps:
            for x in l:
                if x not in emptyAdjacent:
                    emptyAdjacent.append(x)
        for i in range(0, len(emptyAdjacent)):
            print(emptyAdjacent[i])
        return emptyAdjacent
