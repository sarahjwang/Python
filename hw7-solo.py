# hw7-solo.py
# Sarah Wang + junewang + Section II

from tkinter import *
from math import sqrt

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.rows, data.cols = data.rows, data.cols
    data.margin, data.lineLength = 100, 100
    data.circleDiameter, data.circleRadius = 40, 20
    data.seconds = data.seconds
    data.counter, data.counterLimit = 0, data.seconds * 5
    #we have to make a counter for if data.seconds has passed yet
    data.width = data.circleDiameter*data.cols + data.lineLength*(data.cols+1)
    data.height = data.circleDiameter*data.rows + data.lineLength*(data.rows+1)
    data.currentP, data.otherP = 1, 2
    data.circleCoords = {}
    data.circleColors = circleColors(data)
    data.circleA, data.circleB = None, None
    #initialize the values of the first and second mouse click above
    data.lines, data.linesSet, data.letterCoordinates = [], set(), {}
    data.score1, data.score2 = 0,0
    data.turnLost, data.playerMadeMove = False, False
    data.totalLines = data.rows * (data.cols - 1) + data.cols * (data.rows-1)
    data.gameOver = False

#initialize all circle colors as black
def circleColors(data):
    dict = {}
    for row in range(data.cols):
        for col in range(data.rows):
            dict[(row, col)] = "black"
    return dict

# getCircleBounds: idea from grid-demo.py
def getCircleBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    x0 = data.margin * (row + 1) + data.circleDiameter * (row)
    x1 = x0 + data.circleDiameter
    y0 = data.margin * (col + 1) + data.circleDiameter * (col)
    y1 = y0 + data.circleDiameter
    return (x0, y0, x1, y1)

#checks if you clicked in a circle or not
def clickedCircle(point, circle, data):
    distance = sqrt(((point[0] - circle[0]) ** 2) + 
                    ((point[1] - circle[1]) ** 2))
    #return True if the click is within a circle
    return distance < data.circleRadius

def isLegalMove(circle1, circle2):
    row1, col1 = circle1
    row2, col2 = circle2
    dirs = [(-1, 0),( 0, -1),( 0, +1),(+1, 0)]
    for direction in dirs:
        if row1 + direction[0] == row2 and col1 + direction[1] == col2:
            return True
            #returns True if the move is 1 left, right, top or bottom
    return False

def mousePressed(event, data):
    if data.gameOver == True: return
    # use event.x and event.y
    for key in data.circleCoords:
        row, col = key[0], key[1]
        circle = data.circleCoords[key]
        circleCenter = (circle[0] + data.circleDiameter/2, 
            circle[1] + data.circleDiameter/2)
        #gets the center x and y of the circle
        if clickedCircle((event.x, event.y), circleCenter, data):
            data.circleColors[(row, col)] = "red"
            #if they clicked a dot make it red
            if data.circleA == None:
                data.circleA = (row, col)
                #set dot 1's coordinates to data.circleA
            else:
                #if dot1 is already clicked, then this dot must be dot2
                data.circleB = (row, col)

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

#timer fired every 200 ms
def timerFired(data):
    if data.gameOver: return
    data.counter += 1
    #when counter reaches the number of the seconds * 5, check:
    if data.counter == data.counterLimit:
        if data.playerMadeMove == False:
            data.currentP, data.otherP = data.otherP, data.currentP
            #give turn to other player if timer's up and they didn't make move
            data.turnLost = True
        data.counter = 0
        data.playerMadeMove = False
    if data.playerMadeMove == True:
        data.counter = 0 #reset counter after a player makes a turn
        data.playerMadeMove = False

#prints a big "TURN LOST" in a red box
def turnLost(canvas, data):
    x0, y0 = data.width//2 - data.margin, data.height//2 - data.margin//2
    x1, y1 = data.width//2 + data.margin, data.height//2 + data.margin//2
    canvas.create_rectangle(x0, y0, x1, y1, fill="red")
    canvas.create_text(data.width//2, data.height//2, text="TURN LOST!",
        font="Arial 30 bold", fill="white")

#draw a single dot
def drawCircle(canvas, data, row, col, color):
    (x0, y0, x1, y1) = getCircleBounds(row, col, data)
    canvas.create_oval(x0, y0, x1, y1, fill=color)
    return (x0, y0, x1, y1)

#draws all legal moves from a dot when player clicks it
def drawLegalMove(canvas, data, circle):
    for circle2 in data.circleColors:
        row1, col1 = circle
        row2, col2 = circle2
        line1 = getCircleBounds(row1, col1, data)
        line2 = getCircleBounds(row2, col2, data)
        if isLegalMove(circle, circle2):
            if (line1,line2) not in data.lines:
                if (line2,line1) not in data.lines:
                    #only draw a line if the line isn't already made
                    #means that they can only make a move if that move hasn't
                    #already been made
                    canvas.create_line(line1[0] + data.circleRadius, 
                    line1[1] + data.circleRadius, 
                    line2[0] + data.circleRadius, 
                    line2[1] + data.circleRadius, fill="red", width="5")

def checkBorderingLines(circle1, circle2, direction, data):
    lines, score, (row1, col1), (row2, col2) = data.linesSet,0,circle1,circle2
    wordLocation = {}
    #basically, a player can only make a square in two conditions:
    #if the line they made is horizontal:
        #1. the horizontal line above them, the left vertical line on top,
            #or the right vertical line on top is already made
            #this indicates a square is made ABOVE their line
        #2. the horizontal line below, the left vertical line on the bottom,
            #of the right vertical line on the bottom is already made
            #this indicates a square is made BELOW their line
    #and the same goes for the vertical lines, just check for if they made
    #squares on the LEFT and RIGHT side of that line
    #we also have to increase score of player every time they make a square
    #wordLocation is used for the below function (drawLetter) so we know
    #which coordinates to make the text on
    if direction == "horizontal":
        top = ((row1, col1),(row1, col1 - 1))
        bot = ((row1, col1),(row1, col1 + 1))
        top2 = ((row2, col2),(row2, col2 - 1))
        bot2 = ((row2, col2),(row2, col2 + 1))
        topHor = (row1, col1 - 1), (row2, col2 - 1)
        botHor = (row1, col1 + 1), (row2, col2 + 1)
        if (top in lines) and (top2 in lines) and (topHor in lines):
            score += 1
            wordLocation[topHor] = "topHor"
        if (bot in lines) and (bot2 in lines) and (botHor in lines):
            score += 1
            wordLocation[botHor] = "botHor"
    else:
        left = ((row1 - 1, col1),(row1, col1))
        right = ((row1 + 1, col1),(row1, col1))
        left2 = ((row2 - 1, col2),(row2, col2))
        right2 = ((row2 + 1, col2),(row2, col2))
        leftVert = ((row1 - 1, col1),(row2 - 1, col2))
        rightVert = ((row1 + 1, col1),(row2 + 1, col2))
        if (left in lines) and (left2 in lines) and (leftVert in lines):
            score += 1
            wordLocation[leftVert] = "leftVert"
        if (right in lines) and (right2 in lines) and (rightVert in lines):
            score += 1
            wordLocation[rightVert] = "rightVert"
    return score, wordLocation

#draws the player number in the box they made
def drawLetter(canvas, dict, data, player):
    for key in dict:
        coord = key #row, col coordinates of a side of the square
        direction = dict[key]
        directionMoved = 0.5
        newX = (coord[0][0] + coord[1][0])/2
        newY = (coord[0][1] + coord[1][1])/2
        #we have to calculate the coordinates of where exactly we draw the
        #player number. However this is easy, as we know we must place the 
        #player numbers directly in the MIDDLE of the box they made.
        if direction == "topHor":
            newY += directionMoved
        elif direction == "botHor":
            newY -= directionMoved
        elif direction == "leftVert":
            newX += directionMoved
        elif direction == "rightVert":
            newX -= directionMoved
        x0, y0, x1, y1 = getCircleBounds(newX, newY, data)
        x, y = (x0 + x1)//2, (y0 + y1)//2
        canvas.create_text(x, y, text=str(player), font="Arial 25 bold",
            fill="red")
        data.letterCoordinates[(x, y)] = str(player)

#this makes sure that the function above repeats for all the drawn boxes
def drawAllLetters(canvas, data):
    for key in data.letterCoordinates:
        x, y = key
        player = data.letterCoordinates[key]
        canvas.create_text(x, y, text=player, font="Arial 25 bold",
            fill="red")

#draws a single line connecting 2 dots
def drawLine(canvas, data, circle1, circle2):
    (row1, col1), (row2, col2) = circle1, circle2
    line1 = getCircleBounds(row1, col1, data)
    line2 = getCircleBounds(row2, col2, data)
    if row1 != row2: d = "horizontal" #direction of the line
    else: d = "vertical"
    if isLegalMove(circle1, circle2):
        if (line1,line2) not in data.lines and (line2,line1) not in data.lines:
            data.lines.append((line1, line2))
            if checkBorderingLines(circle1, circle2, d, data)[0] != 0:
                #if score is not 0 then:
                #1. the player increases score
                #2. we draw the player number in the square
                #3. they keep their turn
                score = checkBorderingLines(circle1,circle2,d,data)[0]
                word = checkBorderingLines(circle1,circle2,d,data)[1]
                if data.currentP == 2: data.score2 += score
                else: data.score1 += score
                drawLetter(canvas, word, data, data.currentP)
                (data.currentP, data.otherP) = (data.otherP, data.currentP)
            #now we add the lines to our set of lines (we use this later)
            data.linesSet.add(((row1, col1),(row2, col2)))
            data.linesSet.add(((row2, col2),(row1, col1)))
        else: canvas.create_text(data.width//2, 
            data.height-data.circleDiameter, text="Not a legal move!")
    else: canvas.create_text(data.width//2,
        data.height-data.circleDiameter, text="Not a legal move!")
    #must reset color of the dots when they make a move (regardless of whether
    #legal or not)
    data.circleColors[(row1,col1)] = "black"
    data.circleColors[(row2,col2)] = "black"
    data.circleA, data.circleB = None, None

#keep all lines on the board (otherwise they disappear after every timerFired)
def drawAllLines(canvas, data, circle1, circle2):
    if circle1 != None and circle2 != None:
        drawLine(canvas, data, circle1, circle2)
        data.currentP, data.otherP = data.otherP, data.currentP
        data.playerMadeMove = True
    for line in data.lines:
        line1 = line[0]
        line2 = line[1]
        lineWidth = "5"
        canvas.create_line(line1[0] + data.circleRadius, 
        line1[1] + data.circleRadius, 
        line2[0] + data.circleRadius, 
        line2[1] + data.circleRadius, fill="black", width=lineWidth)

#draw the game board
def drawBoard(canvas, data):
    #draw grid of dots
    drawAllLines(canvas, data, data.circleA, data.circleB)
    for row in range(data.cols):
        for col in range(data.rows):
            color = data.circleColors[(row, col)]
            data.circleCoords[(row, col)] = drawCircle(canvas, 
                data, row, col, color) #draw all dots
    if data.circleA != None and data.circleB == None:
        drawLegalMove(canvas, data, data.circleA)
        #if player has clicked one dot, then show them all possible moves
        #from the dot
    elif data.circleA != None and data.circleB != None:
        drawAllLines(canvas, data, data.circleA, data.circleB)
        #this means player has clicked 2 dot, so connect the lines
        #only if the lines are legal!
    if data.turnLost == True: #if the player has lost the turn
        turnLost(canvas, data)
        data.turnLost = False

#this is just some text on the canvas
def drawText(canvas, data):
    margin, marginBot = data.lineLength//4, data.lineLength//1.5
    widthMargin = data.width//4
    canvas.create_text(data.width//2, data.lineLength//2,
        text="Red lines: legal move. If you make an illegal move, " +
        "lose a turn!", font="14", fill="red") #a warning
    canvas.create_text(data.width//2, margin,
        text="Welcome to Dots and Boxes!", font="Arial 20 bold")
    canvas.create_text(widthMargin, data.lineLength - margin,
        text="Player 1: " + str(data.score1), fill="black")
    canvas.create_text(data.width//2 + widthMargin, data.lineLength
        - margin, text="Player 2: " + str(data.score2), fill="black")
    #player 1 and player 2 score above
    canvas.create_text(data.width//2, data.height - marginBot,
        text="Player " + str(data.currentP) + "'s turn")
    #shows who's turn it is

def redrawAll(canvas, data):
    # draw in canvas
    drawBoard(canvas, data)
    drawText(canvas, data)
    drawAllLetters(canvas, data)
    if len(data.lines) == data.totalLines:
        #if number of lines = number of total possible lines on the board
        data.gameOver = True
        sWidth, sHeight = 200, 50 #rectangle sub width and sub height
        canvas.create_rectangle(data.width//2 - sWidth,data.height//2-sHeight,
        data.width//2 + sWidth, data.height//2 + sHeight, fill="red")
        canvas.create_text(data.width//2, data.height//2,
        text="GAME OVER!", font="Arial 50 bold", fill="white")

####################################
# use the run function as-is
####################################

def run(rows, cols, width, height, maxSecondsPerTurn):
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
    data.rows, data.cols = rows + 1, cols + 1
    data.seconds = maxSecondsPerTurn
    data.timerDelay = 200 #milliseconds
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

def playDotsAndBoxes(rows, cols, maxSecondsPerTurn):
    margin = 100 # margin around grid
    diameter = 24 # diameter of dots
    width = 2*margin + diameter*(rows+1) + margin*(cols)
    height = 2*margin + diameter*(cols+1) + margin*(rows)
    run(rows, cols, width, height, maxSecondsPerTurn)

playDotsAndBoxes(3,3,5)