#Tetris Project
import tkinter as tk
import threading
import time

window = tk.Tk()

startFrame = tk.Frame(master=window,height=550,width=650)
startButton = tk.Button(master=startFrame,text="Start Game",width=10)
highScoreLabel = tk.Label(master=startFrame,text="HighScore goes here")
startButton.place(relx=.50,rely=.50, x=-50)
highScoreLabel.place(relx=.70,rely=.90)
startFrame.place(x=0,y=0)

boardFrame = tk.Frame(master=window,height=500,width=400, bg="#404040")
queFrame = tk.Frame(master=window,height=150,width=150, bg="#404040")
menuFrame = tk.Frame(master=window, height=275,width=150, bg="#3377ff", \
                      highlightthickness=2,highlightbackground="#000000",\
                      borderwidth=4)

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

scoreLabel = tk.Label(master=menuFrame,bg="#ffffff",text="score: ",\
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
exitButton = tk.Button(master=menuFrame,bg="#1a1aff",width=5,height=1,text="exit",\
                        highlightthickness=2,highlightbackground="#000000",\
                        borderwidth=4)

scoreLabel.place(x=5, y=5)
rotateButton.place(relx=.75,x=-5, y=100)
moveLeftButton.place(relx=.25,x=-25, y=150)
moveDownButton.place(relx=.50,x=-15, y=150)
moveRightButton.place(relx=.75,x=-5, y=150)
pauseButton.place(relx=.25,x=-25, y=200)
exitButton.place(relx=.50,x=10, y=200)

window.configure(height=550,width=650)

class Field:
    def __init__(self):
        pass
    
    def checkRowCompletion():
        return

    def removeRow():
        return

class Block:
    def __init__(self, color, name, tileConfig):
        self.color = color
        self.name = name
        self.tileConfig = tileConfig
    
    def setBlock():
        return

    def preSetBlock():
        return

    def setNewBlock(self):
        self.setBlock()
        self.preSetBlock()
        return

    def checkBlockDown():
        return

    def moveBlockDown():
        return
    
    def makeTilesStatic():
        return

class Tile:
    def __init__(self, location, frame, dynamic = True):
        self.location = location
        self.frame = frame
        self.dynamic = dynamic

def setupGUI ():
    boardFrame.place(x=0,y=0)
    queFrame.place(x=450,y=25)
    menuFrame.place(x=450,y=200)
    return

def blockDown():
    movable = Block.checkBlockDown()
    if movable:
        Block.moveBlockDown()
    else:
        rowComplete = Field.checkRowCompletion()
        if rowComplete:
            Field.removeRow()
        Block.makeTilesStatic()
        Block.setNewBlock
        print("move down")
    return movable

def blockDownRepeat (event):
    movable = True
    while movable:
        movable = blockDown()
    return

def blockLeft():
    return

def blockRight():
    return

def blockRotate():
    return

def newGame (event):
    startFrame.destroy()
    setupGUI()
    Block.preSetBlock()
    threading.Timer(function=blockDown(),interval=2)


startButton.bind("<Button-1>", newGame)
moveDownButton.bind("<Button-1>", blockDownRepeat)

window.mainloop()