# Sarah Wang + junewang + Section II
# Partner: Megha Joshi (meghajos)

from tkinter import *
import random

#Seven "standard" pieces (tetrominoes)
iPiece = [
    [ True,  True,  True,  True]
  ]
  
jPiece = [
    [ True, False, False ],
    [ True, True,  True]
  ]
  
lPiece = [
    [ False, False, True],
    [ True,  True,  True]
  ]
  
oPiece = [
    [ True, True],
    [ True, True]
  ]
  
sPiece = [
    [ False, True, True],
    [ True,  True, False ]
  ]
  
tPiece = [
    [ False, True, False ],
    [ True,  True, True]
  ]

zPiece = [
    [ True,  True, False ],
    [ False, True, True]
  ]

tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ] 
tetrisPieceColors = ["red","yellow","magenta","pink","cyan","green","orange"]

def init(data):
    # set board dimensions and margin
    data.rows = 15
    data.cols = 10
    data.margin = 20
    # make board
    data.emptyColor = "blue"
    data.board = [([data.emptyColor] * data.cols) for row in range(data.rows)]
    data.tetrisPieces = tetrisPieces
    data.tetrisPieceColors = tetrisPieceColors
    data.isGameOver = False
    data.score = 0 #player's score
    newFallingPiece(data)

# getCellBounds from grid-demo.py
def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.margin + gridHeight * row / data.rows
    y1 = data.margin + gridHeight * (row+1) / data.rows
    return (x0, y0, x1, y1)

#initialize a new piece
def newFallingPiece(data):
    data.fallingPiece = random.choice(tetrisPieces)
    data.fallingPieceColor = random.choice(tetrisPieceColors)
    data.fallingPieceRow = 0
    data.fallingPieceCols = len(data.fallingPiece[0])
    #below equation taken from tetris tutorial
    data.fallingPieceCol = (data.cols // 2) - (data.fallingPieceCols // 2)

#draw the piece
def drawFallingPiece(canvas, data):
    rows, cols = len(data.fallingPiece), len(data.fallingPiece[0])
    startRow, startCol = data.fallingPieceRow, data.fallingPieceCol
    for row in range(rows):
        #iterate through lists
        for col in range(cols):
            #iterate through each boolean in list
            if data.fallingPiece[row][col] == True and data.isGameOver != True:
                drawCell(canvas, data, row + startRow, 
                    col + startCol, data.fallingPieceColor)

#get all the tuple coordinates of a piece on the board
def getCoordinatesOfPiece(data):
    rows, cols = len(data.fallingPiece), len(data.fallingPiece[0])
    dataRow, dataCol = data.fallingPieceRow, data.fallingPieceCol
    newList = []
    for row in range(rows):
        for col in range(cols):
            if (data.fallingPiece[row][col] == True):
                #we need to add all coordinates of the block to a list
                newList.append((row + dataRow, col + dataCol))
                #append the tuples
    return newList

#check if a falling piece is legal
def fallingPieceIsLegal(data):
    newList = getCoordinatesOfPiece(data)
    for indices in newList:
        #iterate through all the coordinates of the list
        row, col = indices[0], indices[1]
        if (row > data.rows - 1) or (row < 0): return False
        #check if row is past top/bottom side of screen
        elif (col > data.cols - 1) or (col < 0): return False
        #check if column is past left/right side of screen
        elif (data.board[row][col]) != data.emptyColor: return False
        #check if the position is already filled with a block
    return True

#move a falling piece
def moveFallingPiece(data, drow, dcol):
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    if (fallingPieceIsLegal(data) == False):
        #return the piece to its original place if not legal move
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
    return True

#rotate a block by switching the rows and columns
def rotateList(rows, cols, data):
    newList = []
    for row in range(cols):
        newList.append([None]*rows)
    #initialize list of "None", switching rows and cols
    for row in range(cols):
        for col in range(rows): 
            newList[row][col] = data.fallingPiece[col][cols-row-1]
            #input new values in new row/col
    return newList

#rotate a falling piece
def rotateFallingPiece(data):  
    #all these instructions below taken from tetris tutorial
    oldPiece = data.fallingPiece
    oldRow, oldCol = data.fallingPieceRow, data.fallingPieceCol
    oldRows, oldCols = len(data.fallingPiece), len(data.fallingPiece[0]) 
    newRows, newCols = oldCols, oldRows
    oldCenterRow = oldRow + oldRows//2  
    newCenterRow = oldCenterRow
    newRow = newCenterRow - newRows//2  
    oldCenterCol = oldCol + oldCols//2
    newCenterCol = oldCenterCol
    newCol = newCenterCol - newCols//2 
    newPiece = rotateList(oldRows, oldCols, data)
    #rotate the newPiece by switching rows and cols
    data.fallingPiece = newPiece 
    data.fallingPieceRows, data.fallingPieceCols = newRows, newCols
    data.fallingPieceRow, data.fallingPieceCol = newRow, newCol
    if (fallingPieceIsLegal(data) == False): #if not legal move, reset all
        data.fallingPiece = oldPiece
        data.fallingPieceRows, data.fallingPieceCols = oldRows, oldCols
        data.fallingPieceRow, data.fallingPieceCol = oldRow, oldCol

#put the piece on the board
def placeFallingPiece(data):
    pieceCoordinates = getCoordinatesOfPiece(data)
    for (row, col) in pieceCoordinates:
        data.board[row][col] = data.fallingPieceColor
        #this places the piece on the board by changing the corresponding cells
        #to its color

#remove rows that contain only non-blue cells
def removeFullRows(data):
    rows, cols = data.rows, data.cols
    newBoard = []
    for row in range(rows):
        count = 0
        for col in range(cols):
            if data.board[row][col] != data.emptyColor: count += 1
            #count how many non-blue blocks there are
        if count != cols: newBoard.append(data.board[row])
            #if count is not 10 (meaning there is a blue in the row)
            #then add it to the board, because it's not complete yet
        else: data.score += 1
            #otherwise, increase player's score by 1 and then remove the row
    newBoard = newBoard[::-1]
    #switch board to topside
    while len(newBoard) != rows:
        newBoard.append([data.emptyColor]*cols)
        #add blue rows to the top of the board
    data.board = newBoard[::-1]
    #we still have to reverse the board because right now it's going from 
    #bottom to top, and we want top to bottom

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    # for now, for testing purposes, just choose a new falling piece
    # whenever ANY key is pressed!
    if (event.keysym == "r"): init(data) #restart
    if (data.isGameOver): return #stop all key presses except "r" if game over
    elif (event.keysym == "Down"): moveFallingPiece(data, +1, 0)
    elif (event.keysym == "Left"): moveFallingPiece(data, 0, -1)
    elif (event.keysym == "Right"):moveFallingPiece(data, 0, +1)
    elif (event.keysym == "Up"): rotateFallingPiece(data) #rotate

#timer fired every second
def timerFired(data):
    if (data.isGameOver): return
    if moveFallingPiece(data, +1, 0) == False:
        placeFallingPiece(data) #place the piece
        newFallingPiece(data) #get a new piece from the top
        removeFullRows(data) #check if we need to remove any rows
        if fallingPieceIsLegal(data) == False:
            #if the new piece is immediately illegal after getting it
            data.isGameOver = True #then game over

#draw the game
def drawGame(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="orange")
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)

#draw the tetris board
def drawBoard(canvas, data):
    # draw grid of cells
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col, data.board[row][col])

#draw a cell in the board
def drawCell(canvas, data, row, col, color):
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    m = 1 # cell outline margin
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=color)

#draws a box saying "Game Over!"
def drawGameOver(canvas, data):
    rectXtop, rectYtop = 40, 120 #rectangle top coordinates
    rectXbot, rectYbot = 200, 190 #rectangle bottom coordinates
    gameOverX, gameOverY = 120, 140 #game over text coordinates
    if (data.isGameOver):
        canvas.create_rectangle(rectXtop, rectYtop, rectXbot,
            rectYbot, fill="white")
        canvas.create_text(gameOverX, gameOverY, text="Game Over!",
            font="Arial 26 bold", fill="black")
        canvas.create_text(data.width/2, data.height/2, 
            text="Press r to restart", font="Arial 15 bold", fill="black")

#draws player's score above the board
def drawScore(canvas, data):
    score = str(data.score)
    scoreX, scoreY = 40, 12 #coordinates of the score text
    canvas.create_text(scoreX, scoreY, 
        text="Score: " + score, font="Arial 12 bold", fill="black")

#draws game, score, and game over (if it is game over)
def redrawAll(canvas, data):
    drawGame(canvas, data)
    drawScore(canvas, data)
    drawGameOver(canvas, data)

def run(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

####################################
# playTetris() [calls run()]
####################################

def playTetris():
    rows = 15
    cols = 10
    margin = 20 # margin around grid
    cellSize = 20 # width and height of each cell
    width = 2*margin + cols*cellSize
    height = 2*margin + rows*cellSize
    run(width, height)

playTetris()
