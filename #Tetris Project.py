#Tetris Project
import tkinter as tk
import asyncio
import random
import threading

window = tk.Tk()

boardFrame = tk.Frame(master=window,height=500,width=400, bg="#404040")
queFrame = tk.Frame(master=window,height=150,width=150, bg="#404040")
menuFrame = tk.Frame(master=window, height=275,width=150, bg="#3377ff", \
                      highlightthickness=2,highlightbackground="#000000",\
                      borderwidth=4)
gameOverFrame = tk.Frame(master=window, height=150,width=250, bg="#807060")

for row in range(10):
    for column in range(8):
        newTile = tk.Frame(master=boardFrame,width=50,height=50,bg="#404040", \
                            highlightthickness=2,highlightbackground="#000000",\
                            borderwidth=4)
        newTile.grid(column=column,row=row)

for row in range(3):
    for column in range(3):
        newTile = tk.Frame(master=queFrame,width=50,height=50,bg="#404040",\
                            highlightthickness=2,highlightbackground="#000000",\
                            borderwidth=4)
        newTile.grid(column=column,row=row)

scoreLabel = tk.Label(master=menuFrame,bg="#ffffff",text="score: 0",\
                       highlightthickness=2,highlightbackground="#000000",\
                       borderwidth=4)
highScoresLabelA = tk.Label(master=menuFrame,bg="#ffffff",text="1st place:",\
                       highlightthickness=2,highlightbackground="#000000",\
                       borderwidth=4)
highScoresLabelB = tk.Label(master=menuFrame,bg="#ffffff",text="2nd place:",\
                       highlightthickness=2,highlightbackground="#000000",\
                       borderwidth=4)
highScoresLabelC = tk.Label(master=menuFrame,bg="#ffffff",text="3rd place:",\
                       highlightthickness=2,highlightbackground="#000000",\
                       borderwidth=4)
moveLeftButton = tk.Button(master=menuFrame,bg="#1a1aff",width=2,height=1,text="A",\
                              highlightthickness=2,highlightbackground="#000000",\
                              borderwidth=4)
moveDownButton = tk.Button(master=menuFrame,bg="#1a1aff",width=2,height=1,text="S",\
                            highlightthickness=2,highlightbackground="#000000",\
                            borderwidth=4)
moveRightButton = tk.Button(master=menuFrame,bg="#1a1aff",width=2,height=1,text="D",\
                               highlightthickness=2,highlightbackground="#000000",\
                               borderwidth=4)
rotateButton = tk.Button(master=menuFrame,bg="#1a1aff",width=2,height=1,text="R",\
                               highlightthickness=2,highlightbackground="#000000",\
                               borderwidth=4)
pauseButton = tk.Button(master=menuFrame,bg="#1a1aff",width=5,height=1,text="pause",\
                         highlightthickness=2,highlightbackground="#000000",\
                         borderwidth=4)
newGameButton = tk.Button(master=menuFrame,bg="#1a1aff",width=7,height=1,text="new game",\
                        highlightthickness=2,highlightbackground="#000000",\
                        borderwidth=4)

scoreLabel.place(x=5, y=5)
highScoresLabelA.place(x=5, y=30)
highScoresLabelB.place(x=5, y=55)
highScoresLabelC.place(x=5, y=80)
rotateButton.place(relx=.75,x=-5, y=120)
moveLeftButton.place(relx=.25,x=-25, y=160)
moveDownButton.place(relx=.50,x=-15, y=160)
moveRightButton.place(relx=.75,x=-5, y=160)
pauseButton.place(relx=.25,x=-25, y=200)
newGameButton.place(relx=.50,x=0, y=200)

gameOverLabel = tk.Label(master=gameOverFrame, text="game over")
gameOverScoreLabel = tk.Label(master=gameOverFrame, text="your score: ")
gameOverHighscoreLabel = tk.Label(master=gameOverFrame, text="highscore: ")
gameOverUsernameEntry = tk.Entry(master=gameOverFrame)
gameOverUsernameEntry.insert(0,"username")
gameOversubmitButton = tk.Button(master=gameOverFrame, text="submit: ")

gameOverLabel.place(x=90,y=5)
gameOverScoreLabel.place(x=5,y=30)
gameOverHighscoreLabel.place(x=5,y=55)
gameOverUsernameEntry.place(x=5,y=80)
gameOversubmitButton.place(x=200,y=115)

window.configure(height=550,width=650)

class Tile:
    instances = []
    def __init__(self, color, location, frame, dynamic = True, active = False):
        self.instances.append(self)
        self.color = color
        self.location = location
        self.frame = frame
        self.dynamic = dynamic
        self.active = active

    def checkTileLocation(self, location):
        """returns the validity of a location based on other tiles and preset boundaries"""
        validLocation = True
        if location[0] == -1 or location[0] == 10 or\
              location[1] == -1 or location[1] == 8:
            validLocation = False
        else:
            tiles = self.instances
            for tile in tiles:
                if tile.location == location and not tile.dynamic and tile.active:
                    validLocation = False
                    break
        return validLocation

    def moveTile(self, newMaster):
        """destroys the tile frame and places a new frame in the desired master"""
        oldFrame = self.frame
        newFrame = tk.Frame(master=newMaster,width=46,height=46,bg=self.color)
        self.frame = newFrame
        if oldFrame is not None:
            oldFrame.destroy()
        newFrame.place(y=-4,x=-4)
    
    def reorganizeTileList(tiles):
        """takes a list of tiles and returns them in ascending order based on location"""
        lineFunction = lambda coord: (coord[0], coord[1])

        newLocationList = []
        for tile in tiles:
            newLocationList.append(tile.location)
        newLocationList = sorted(newLocationList, key=lineFunction)
        newTileList = []
        for location in newLocationList:
            for tile in tiles:
                if tile.location == location:
                    newTileList.append(tile)
                    break
        return newTileList


class Field:
    instances = []
    def __init__(self, tiles = [],gameOver = False, gamePaused = True, windowClosed = False, score = 0, totalRowsCompleted = 0):
        self.instances.append(self)
        self.tiles = tiles
        self.gameOver = gameOver
        self.windowClosed = windowClosed
        self.score = score
        self.totalRowsCompleted = totalRowsCompleted
        self.gamePaused = gamePaused
    
    def checkRowCompletion(self):
        """checks tiles on field by looping through all tiles and returns any full rows"""
        locationList = []
        for tile in self.tiles:
            locationList.append(tile.location)
        rowsCompleted = []
        count = 0
        for row in range(10):
            completeRow = True
            for column in range(8):
                if locationList[count][1] == column and locationList[count][0] == row:
                    count += 1
                else:
                    completeRow = False
                if column == 7 and completeRow:
                    rowsCompleted.append(row)
                if count == len(locationList):
                    break
        return rowsCompleted

    def deleteTile(self,location):
        """deletes the tile from the location"""
        tiles = self.tiles
        for tile in tiles:
            if tile.location == location and tile.active == True:
                tile.frame.destroy()
                tiles.remove(tile)
                Tile.instances.remove(tile)
                del tile

    def removeRow(self,rowsCompleted):
        """removes rows by taking out all tiles with that row number"""
        locationList = []
        for tile in self.tiles:
            locationList.append(tile.location)

        for row in rowsCompleted:
            for location in locationList:
                if location[0] == row:
                    self.deleteTile(location)
    
    def moveRowsDown(self,rowsCompleted):
        """moves all tiles above a row completed down 1 for each row"""
        for row in rowsCompleted:
            for tile in self.tiles:
                if tile.location[0] < row:
                    newTileLocation = [tile.location[0] + 1,tile.location[1]]
                    newMaster = boardFrame.grid_slaves(newTileLocation[0],newTileLocation[1])
                    tile.location = newTileLocation
                    tile.moveTile(newMaster[0])  
    
    def gameIsOver(self):
        """brings up the game over frame and sets final score"""
        self.totalRowsCompleted = 0
        gameOverScoreLabel.configure(text="score: " + str(self.score))
        gameOverFrame.place(relx=0.5,x=-125,rely=0.5,y=-75)
    
    def addPoints(self,rowsCompleted):
        """*based on the rows completed (1/2/3) add points (10/30/60) and display the new score and add rows completed"""
        rowsCompletedNumber = len(rowsCompleted)
        self.totalRowsCompleted += rowsCompletedNumber

        if rowsCompletedNumber == 1:
            points = 10
        elif rowsCompletedNumber == 2:
            points = 30
        elif rowsCompletedNumber == 3:
            points = 60
        score = self.score
        score += points
        self.score = score

        scoreLabel.configure(text= "score: " + str(score)) 
    
    def handleRows(self):
        """handles the potential removal of rows and the addition of points"""
        self.tiles = Tile.reorganizeTileList(self.tiles)
        rowsCompleted = self.checkRowCompletion()
        if rowsCompleted != []:
            self.removeRow(rowsCompleted)
            self.moveRowsDown(rowsCompleted)
            self.addPoints(rowsCompleted)


class Block:
    instances = []
    def __init__(self, name, tileConfig, tiles = [], isRotated = False, rotateMat = [], active = False):
        self.instances.append(self)
        self.name = name
        self.tileConfig = tileConfig
        self.tiles = tiles
        self.isRotated = isRotated
        self.rotateMat = rotateMat
        self.active = active
    
    colorList = ["#ff0000","#ff6600","#ffff00","#008000","#0000ff","#800080"]

    blockTuple = (\
        ("Dot", ([1,1],)),\
        ("SLine", ([1,0],[1,1])),\
        ("Corner", ([1,0],[0,1],[1,1])),\
        ("Square", ([0,0],[1,0],[0,1],[1,1])),\
        ("LLine", ([1,0],[1,1],[1,2])),\
        ("LRight", ([1,0],[1,1],[1,2],[2,2])),\
        ("LLeft", ([1,0],[2,0],[1,1],[1,2])),\
        ("HalfPlus", ([1,0],[1,1],[2,1],[1,2])),\
        ("ZLeft", ([1,0],[2,0],[1,1],[0,2],[1,2])),\
        ("ZRight", ([0,0],[1,0],[1,1],[1,2],[2,2]))\
    )

    rotateMatList = (\
        (([0,0],), ([0,0],)),\
        (([0,0],[0,1]), ([0,0],[1,-1])),\
        (([0,0],[1,0]), ([0,1],[-1,0])),\
        (([0,0],[0,1],[0,2]), ([-1,1],[0,0],[1,-1])),\
        (([0,0],[1,0],[2,0]), ([1,1],[0,0],[-1,-1])),\
        (([0,0],[0,1],[1,0],[1,1]), ([0,1],[1,0],[-1,0],[0,-1])),\
        (([0,0],[0,1],[0,2],[1,0],[1,1],[1,2]), ([0,1],[1,0],[2,-1],[-1,0],[0,-1],[1,-2])),\
        (([0,0],[0,1],[1,0],[1,1],[2,0],[2,1]), ([0,2],[1,1],[-1,1],[0,0],[-2,0],[-1,-1])),\
        (([0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]), ([0,2],[1,1],[2,0],[-1,1],[0,0],[1,-1],[-2,0],[-1,-1],[0,-2])),\
        )

    def findActiveBlock(active = True):
        """looks through all block objects and returns the active block"""
        blockList = Block.instances
        for block in blockList:
            if block.active == active:
                activeBlock = block
        return activeBlock
    
    def findRotateMatrix(blockName):
        """returns a predetermined matrix based on a block name"""
        if blockName == "Dot":
            rotateMatricies = [Block.rotateMatList[0][1],Block.rotateMatList[0][1]]
        elif blockName == "SLine":
            rotateMatricies = [Block.rotateMatList[1][1],Block.rotateMatList[2][1]]
        elif blockName == "LLine":
            rotateMatricies = [Block.rotateMatList[3][1],Block.rotateMatList[4][1]]
        elif blockName == "Square" or blockName == "Corner":
            rotateMatricies = [Block.rotateMatList[5][1],Block.rotateMatList[5][1]]
        elif blockName == "HalfPlus" or blockName == "LRight" or blockName == "LLeft":
            rotateMatricies = [Block.rotateMatList[6][1],Block.rotateMatList[7][1]]
        elif blockName == "ZRight" or blockName == "ZLeft":
            rotateMatricies = [Block.rotateMatList[8][1],Block.rotateMatList[8][1]]
        return rotateMatricies

    def createBlockObject():
        """creates and returns a block object for the que"""
        randomNumber = random.randint(0,(len(Block.blockTuple) - 1))
        blockName = Block.blockTuple[randomNumber][0]
        tileConfig = Block.blockTuple[randomNumber][1]
        rotateMatricies = Block.findRotateMatrix(blockName)
        queBlock = Block(name=blockName, tileConfig=tileConfig, rotateMat=rotateMatricies)
        Block.instances.append(queBlock)
        return queBlock

    def createTileObjects(self):
        """creates tiles for the block"""
        randomNumber =  random.randint(0,(len(self.colorList) - 1))
        color = self.colorList[randomNumber]
        tileList = []
        for tileLocation in self.tileConfig:
            newTileFrame = tk.Frame(width=46,height=46,bg=color)
            newTile = Tile(color,tileLocation,newTileFrame)
            tileList.append(newTile)
        self.tiles = tileList

    def placeBlockInQue(self):
        """uses moveTile to place the tiles in the que"""
        for tile in self.tiles:
            tileHolder = queFrame.grid_slaves(tile.location[0],tile.location[1])
            Tile.moveTile(tile,tileHolder[0])

    def preSetBlock():
        """build, place, and return a new block in the que"""
        queBlock = Block.createBlockObject()
        queBlock.createTileObjects()
        queBlock.placeBlockInQue()
        return queBlock

    def checkEmptyRowInTileConfig(self,row):
        """returns a check if there is an empty row in the tile configuration"""
        emptyTopRow = True
        for tileConfig in self.tileConfig:
            if tileConfig[0] == row:
                emptyTopRow = False
        return emptyTopRow

    def alignOffset(self):
        """returns an standard offset unless there is an empty row up top, offset up 1"""
        emptyTopRow = self.checkEmptyRowInTileConfig(0)
        if emptyTopRow:
            offset = [-1,3]
        else:
            offset = [0,3]
        return offset

    def checkBlockLocation(self, offset):
        """returns a validatation of the placement of all tiles in the queblock onto the board based on an offset"""
        validBlockLocation = True
        blockConfig = self.tileConfig
        for tileLocationInQue in blockConfig:
            tileLocation = [tileLocationInQue[0] + offset[0], tileLocationInQue[1] + offset[1]]
            validTileLocation = Tile.checkTileLocation(Tile,tileLocation)
            if not validTileLocation:
                validBlockLocation = False
        return validBlockLocation
    
    def findOffSet(self):
        """returns a valid offset to place the block onto the field if possible"""
        offset = self.alignOffset()
        validLocation = self.checkBlockLocation(offset)

        if validLocation == False:
            offset[1] -= 3
            validLocation = self.checkBlockLocation(offset)
            offset[1] += 1

        while validLocation == False and offset[1] <= 5:
            validLocation = self.checkBlockLocation(offset)
            offset[1] += 1
        if not validLocation:
            offset[1] += 1
        return offset

    def placeTiles(self, offset):
        """places the tiles in the queblock onto the field"""
        field = Field.instances[0]
        counter = 0
        for tile in self.tiles:
            blockConfig = self.tileConfig[counter]
            tileLocation = [blockConfig[0] + offset[0], blockConfig[1] + offset[1]]
            newMaster = boardFrame.grid_slaves(tileLocation[0],tileLocation[1])
            tile.location = tileLocation
            tile.moveTile(newMaster[0])
            field.tiles.append(tile)
            counter += 1

    def setBlock(self):
        """*places the block onto the field by finding its offset, if no offset is valid then it returns game over"""
        gameOver = False
        offset = self.findOffSet()
        if offset[1] == 7:
            gameOver = True
        else:
            offset[1] -= 1
            self.placeTiles(offset)
        return gameOver

    def activateTilesInBlock(self):
        """sets every tile in a block to active"""
        for tile in self.tiles:
            tile.active = True

    def setNewBlock(self):
        """moves the queblock to the board if possible(returns game over), makes a new queblock"""
        gameOver = self.setBlock()
        if gameOver == False:
            self.active = True
            self.activateTilesInBlock()
            Block.preSetBlock()
        return gameOver

    def checkBlockMove(self,moveOffset):
        """returns true if the block can move in the specified offset direction"""
        movable = True
        for tile in self.tiles:
            tileLocation = tile.location
            newTileLocation = [tileLocation[0] + moveOffset[0],tileLocation[1] + moveOffset[1]]
            validLocation = tile.checkTileLocation(newTileLocation)
            if not validLocation:
                movable = False
                break
        return movable

    def moveBlock(self, moveOffset):
        """moves the block in the specified offset direction"""
        for tile in self.tiles:
            tileLocation = tile.location
            newTileLocation = [tileLocation[0] + moveOffset[0],tileLocation[1] + moveOffset[1]]
            newMaster = boardFrame.grid_slaves(newTileLocation[0],newTileLocation[1])
            tile.location = newTileLocation
            tile.moveTile(newMaster[0])

    def locationsFromMat(self,rotateMatrix):
        """returns the locations matricies of the rotate matricies"""
        for Matricies in self.rotateMatList:
            if rotateMatrix == Matricies[1]:
                locationFromMat = Matricies[0]
        return locationFromMat

    def modifiedRotateMatrix(self,rotateMatrix):
        """modifies the rotate matrix and returns the tile offsets"""
        tileLocationList = []
        tiles = self.tiles
        for tile in tiles:
            tileLocationList.append(tile.location)
        sortedTileLocationList = sorted(tileLocationList, key=lambda coord: (coord[1], coord[0]))
        blockLocation = [tiles[0].location[0],sortedTileLocationList[0][1]]
        
        locationFromMat = self.locationsFromMat(rotateMatrix)
        modifiedMatrix = []
        for tile in tiles:
            tileLocation = tile.location
            count = 0
            for location in rotateMatrix:
                if tileLocation[0] - blockLocation[0] == locationFromMat[count][0] and\
                    tileLocation[1] - blockLocation[1] == locationFromMat[count][1]:
                    modifiedMatrix.append(location)
                count += 1
        return modifiedMatrix

    def checkBlockRotate(self):
        """returns movable = true if the block can rotate"""
        movable = True

        matNumber = 0
        if self.isRotated:
            matNumber = 1
        rotateMatrix = self.rotateMat[matNumber]

        tiles = self.tiles
        modifiedMatrix = self.modifiedRotateMatrix(rotateMatrix)

        count = 0
        for tile in tiles:
            tileLocation = tile.location
            newTileLocation = [tileLocation[0] + modifiedMatrix[count][0],tileLocation[1] + modifiedMatrix[count][1]]
            validLocation = tile.checkTileLocation(newTileLocation)
            if not validLocation:
                movable = False
                break
            count += 1

        return movable
    
    def rotateBlock(self):
        """rotates the block"""
        matNumber = 0
        if self.isRotated:
            matNumber = 1
        rotateMatrix = self.rotateMat[matNumber]

        tiles = self.tiles
        modifiedMatrix = self.modifiedRotateMatrix(rotateMatrix)

        count = 0
        for tile in self.tiles:
            tileLocation = tile.location
            newTileLocation = [tileLocation[0] + modifiedMatrix[count][0],tileLocation[1] + modifiedMatrix[count][1]]
            newMaster = boardFrame.grid_slaves(newTileLocation[0],newTileLocation[1])
            tile.location = newTileLocation
            tile.moveTile(newMaster[0])
            count += 1
    
    def makeTilesStatic(self):
        """makes the tiles in a block dynamic False"""
        tiles = self.tiles
        for tile in tiles:
            tile.dynamic = False


def getHighScore():
    try:
        tetrisHighScoreFile = open("tetrisHighScoreFile.txt","r")
    except:
        print("no highscore found")
        tetrisHighScoreFile = []

    highScores = []
    for line in tetrisHighScoreFile:
        lineList = line.split()
        if len(lineList) > 1:
            username = ""
            wordNumber = 0
            while wordNumber < len(lineList) - 1:
                username = username + lineList[wordNumber]
                wordNumber += 1
            highScore = [username,lineList[len(lineList) - 1]]
            highScores.append(highScore)
    if not (tetrisHighScoreFile == []):
        tetrisHighScoreFile.close()
    
    lineFunction = lambda coord: (coord[1], coord[0])
    highScores = sorted(highScores, key=lineFunction, reverse=True)
    return highScores

def DisplayHighScore(highScores):
    if len(highScores) > 0:
        highScoresLabelA.configure(text=("1st place: " + highScores[0][1] + " by " + highScores[0][0]))
    if len(highScores) > 1:
        highScoresLabelB.configure(text=("2nd place: " + highScores[1][1] + " by " + highScores[1][0]))
    if len(highScores) > 2:
        highScoresLabelC.configure(text=("3rd place: " + highScores[2][1] + " by " + highScores[2][0]))

def setupGUI ():
    """places main GUI(board, que, and menu)"""
    boardFrame.place(x=0,y=0)
    queFrame.place(x=450,y=25)
    menuFrame.place(x=450,y=200)

def pauseGameEvent(event):
    """reverses the state of game paused"""
    field = Field.instances[0]
    field.gamePaused = not field.gamePaused

def blockDownEvent(event):
    """all that happens when a block is to move down returns movable if game isn't paused"""
    field = Field.instances[0]
    if not field.gamePaused:
        activeBlock = Block.findActiveBlock()
        movable = activeBlock.checkBlockMove([1,0])
        if movable:
            activeBlock.moveBlock([1,0])
        else:
            field.handleRows()
            activeBlock.makeTilesStatic()
            del activeBlock
            queBlock = Block.findActiveBlock(active=False)
            gameOver = queBlock.setNewBlock()
            if gameOver:
                field.gameIsOver()
                pauseGameEvent(event="game over")
        return movable

def blockDownRepeatEvent (event):
    """all that happens when the user pushes down"""
    field = Field.instances[0]
    if not field.gamePaused:
        movable = True
        while movable:
            movable = blockDownEvent(event="blockDownRepeatEvent")

def blockLeftEvent(event):
    """all that happens when the user pushes left"""
    field = Field.instances[0]
    if not field.gamePaused:
        activeBlock = Block.findActiveBlock()
        movable = activeBlock.checkBlockMove([0,-1])
        if movable:
            activeBlock.moveBlock([0,-1])

def blockRightEvent(event):
    """all that happens when the user pushes left"""
    field = Field.instances[0]
    if not field.gamePaused:
        activeBlock = Block.findActiveBlock()
        movable = activeBlock.checkBlockMove([0,1])
        if movable:
            activeBlock.moveBlock([0,1])

def blockRotateEvent(event):
    """all that happens when the user rotates the block"""
    field = Field.instances[0]
    if not field.gamePaused:
        activeBlock = Block.findActiveBlock()
        activeBlock.tiles = Tile.reorganizeTileList(activeBlock.tiles)

        movable = activeBlock.checkBlockRotate()
        if movable:
            activeBlock.rotateBlock()
            activeBlock.isRotated = not activeBlock.isRotated

def submitScoresEvent(event):
    """close the gameOver screen"""
    username = gameOverUsernameEntry.get()
    gameOverFrame.place_forget()
    score = Field.instances[0].score
    tetrisHighScoreFile = open("tetrisHighScoreFile.txt","a")
    tetrisHighScoreFile.write(username + " " + str(score) + "\n")
    tetrisHighScoreFile.close()

def windowClosed():
    """destroy the window after signiling the user pressed close window"""
    try:
        field = Field.instances[0]
        field.windowClosed = True
    except:
        print("no field to get/game never started")
    window.destroy()

async def stepEvent(field):
    """a looped function to continually step the block down"""
    count = 0
    while True:
        window.update()
        await asyncio.sleep(.1)
        if not field.gameOver and count >= (10 - (field.totalRowsCompleted / 10)):
            blockDownEvent("step")
            count = 0
        count += 1
        if field.windowClosed:
            break

def destroyPreviousObjects(field):
    """destroys all blocks and tiles"""
    tilesInField = field.instances[0].tiles
    tilesInField.clear()

    tiles = Tile.instances
    for tile in tiles:
        tile.frame.destroy()
        tiles = Tile.instances
        del tile
    tiles.clear()
    
    blocks = Block.instances
    for block in blocks:
        blocks.remove(block)
        del block

def newGame (event):
    """sets up a new game"""
    field = Field.instances[0]
    field.gamePaused = True
    destroyPreviousObjects(field)

    queBlock = Block.preSetBlock()
    queBlock.setNewBlock()

    highScores = getHighScore()
    DisplayHighScore(highScores)

    field.gameOver = False
    field.gamePaused = False

def startStepEvent(field):
    """set up for seperate thread"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(stepEvent(field))
    loop.close()

def start_game_operations():
    """begin the game startup and setup"""
    field = Field(gameOver=True)
    Field.instances.append(field)
    startFrame.destroy()
    setupGUI()
    newGame("start game")
    threading.Thread(target=startStepEvent(field)).start()

startFrame = tk.Frame(master=window,height=550,width=650)
startButton = tk.Button(master=startFrame,text="Start Game",width=10, command=start_game_operations)
highScores = getHighScore()
if len(highScores) > 0:
    highScoreLabel = tk.Label(master=startFrame,text="HighScore: " + highScores[0][1] + " by " + highScores[0][0])
    highScoreLabel.place(relx=.70,rely=.90)
startButton.place(relx=.50,rely=.50, x=-50)
startFrame.place(x=0,y=0)

newGameButton.bind("<Button-1>",newGame)

pauseButton.bind("<Button-1>", pauseGameEvent)
window.bind("p", pauseGameEvent)

moveDownButton.bind("<Button-1>", blockDownRepeatEvent)
window.bind("s", blockDownRepeatEvent)
window.bind("<Down>", blockDownRepeatEvent)

moveLeftButton.bind("<Button-1>", blockLeftEvent)
window.bind("a", blockLeftEvent)
window.bind("<Left>", blockLeftEvent)

moveRightButton.bind("<Button-1>", blockRightEvent)
window.bind("d", blockRightEvent)
window.bind("<Right>", blockRightEvent)

rotateButton.bind("<Button-1>", blockRotateEvent)
window.bind("<space>", blockRotateEvent)

gameOversubmitButton.bind("<Button-1>", submitScoresEvent)

window.protocol("WM_DELETE_WINDOW", windowClosed)

window.mainloop()
