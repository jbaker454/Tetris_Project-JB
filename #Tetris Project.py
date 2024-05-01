#Tetris Project
import tkinter as tk

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
rotateLeftButton = tk.Button(master=menuFrame,bg="#1a1aff",\
                              highlightthickness=2,highlightbackground="#000000",\
                              borderwidth=4)
moveDownButton = tk.Button(master=menuFrame,bg="#1a1aff",\
                            highlightthickness=2,highlightbackground="#000000",\
                            borderwidth=4)
rotateRightButton = tk.Button(master=menuFrame,bg="#1a1aff",\
                               highlightthickness=2,highlightbackground="#000000",\
                               borderwidth=4)
pauseButton = tk.Button(master=menuFrame,bg="#1a1aff",\
                         highlightthickness=2,highlightbackground="#000000",\
                         borderwidth=4)
exitButton = tk.Button(master=menuFrame,bg="#1a1aff",\
                        highlightthickness=2,highlightbackground="#000000",\
                        borderwidth=4)

print(scoreLabel.winfo_screenwidth())

scoreLabel.place(relx=.5,x=-(scoreLabel.winfo_screenwidth() / 50), y=5)
rotateLeftButton.place()
moveDownButton.place()
rotateRightButton.place()
pauseButton.place()
exitButton.place()

window.configure(height=550,width=650)

class Tile:
    def __init__(self, location, frame, color, dynamic = True):
        self.location = location
        self.frame = frame
        self.color = color
        self.dynamic = dynamic

def setupGUI ():
    boardFrame.place(x=0,y=0)
    queFrame.place(x=450,y=25)
    menuFrame.place(x=450,y=200)

def startGame (event):
    startFrame.destroy()
    setupGUI()
    return

startButton.bind("<Button-1>", startGame)

window.mainloop()