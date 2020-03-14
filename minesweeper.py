# Python Version 3.7.6
# File: minesweeper.py

from tkinter import *
from tkinter import messagebox as tkMessageBox
from collections import deque
import random
import platform
import time
from datetime import time, date, datetime
from PIL import ImageTk, Image

SIZE_X = 15 # I think these values are flipped, but leaving as is for now
SIZE_Y = 30

STATE_DEFAULT = 0
STATE_CLICKED = 1
STATE_FLAGGED = 2

BTN_CLICK = "<Button-1>"
BTN_FLAG = "<Button-2>" if platform.system() == 'Darwin' else "<Button-3>"

window = None

class Minesweeper:

    def __init__(self, tk):

        # import images
        self.images = {
            "plain" : PhotoImage(file = "images/tile_plain.gif"),
            "clicked" : PhotoImage(file = "images/tile_clicked.gif"),
            "mine" : PhotoImage(file = "images/lowco/tile_mine.png"),
            "flag" : PhotoImage(file = "images/lowco/tile_flag.png"),
            "wrong" : PhotoImage(file = "images/lowco/tile_wrong.png"),
            "BEWM" : PhotoImage(file = "images/lowco/tile_bewm.png"),
            "happy" : PhotoImage(file = "images/lowco/tile_happy.png"),
            "win" : PhotoImage(file = "images/lowco/tile_win.png"),
            "lose" : PhotoImage(file = "images/lowco/tile_lose.png"),
            "numbers": []
        }
        for i in range(1, 9):
            self.images["numbers"].append(PhotoImage(file = "images/tile_"+str(i)+".gif"))

        # Set up frame
        self.tk = tk
        #self.label = Label(self.tk, bg="purple", padx=500, pady=500)
        self.frame = Frame(self.tk, bg="purple", padx=50, pady=30)
        self.frame.grid(row=1, column=0,columnspan=SIZE_Y)

        
        # set up labels/UI
        self.labels = {
            "time": Label(self.frame, text = "00:00:00", bg = "purple", fg="gold", font="Helvetica 10 bold"),
            "mines": Label(self.frame, text = "Mines: 0", bg = "purple", fg="gold", font="Helvetica 10 bold"),
            "flags": Label(self.frame, text = "Flags: 0", bg = "purple", fg="gold", font="Helvetica 10 bold")
        }

        self.labels["time"].grid(row = 1, column = 0, columnspan = SIZE_Y) # top full width
        self.labels["mines"].grid(row = SIZE_X+2, column = 0, columnspan = int(SIZE_Y/2)) #SIZE_Y/2) # bottom left
        self.labels["flags"].grid(row = SIZE_X+2, column = int(SIZE_Y/2-1), columnspan = int(SIZE_Y/2)) # bottom right

        # Create Menu:
        #self.menubar = Menu(self.tk)
        #self.filemenu = Menu(self.menubar, tearoff=0)
        #self.filemenu.add_command(label="Easy", command=self.setDiff("Easy", True))
        #self.filemenu.add_command(label="Medium", command=self.setDiff("Medium", True))
        #self.filemenu.add_command(label="Hard", command=self.setDiff("Hard", True))
        #self.menubar.add_cascade(label="File", menu=self.filemenu)
        #self.tk.config(menu=self.menubar)

        self.restart() # start game
        self.updateTimer() # init timer

    def setup(self):
        # create flag and clicked tile variables
        self.flagCount = 0
        self.correctFlagCount = 0
        self.clickedCount = 0
        self.startTime = None

        # create buttons
        self.tiles = dict({})
        self.mines = 0

        self.MasterButton = Button(self.frame, image=self.images["happy"])
        self.MasterButton.grid(row = 0, column =0, columnspan = SIZE_Y)

        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if y == 0:
                    self.tiles[x] = {}

                id = str(x) + "_" + str(y)
                isMine = False

                # tile image changeable for debug reasons:
                gfx = self.images["plain"]

                # currently random amount of mines
                if random.uniform(0.0, 1.0) < 0.3:
                    isMine = True
                    self.mines += 1

                tile = {
                    "id": id,
                    "isMine": isMine,
                    "state": STATE_DEFAULT,
                    "coords": {
                        "x": x,
                        "y": y
                    },
                    "button": Button(self.frame, image = gfx, activebackground="gold"),
                    "mines": 0 # calculated after grid is built
                }

                tile["button"].bind(BTN_CLICK, self.onClickWrapper(x, y))
                tile["button"].bind(BTN_FLAG, self.onRightClickWrapper(x, y))
                tile["button"].grid( row = x+2, column = y ) # offset by 2 row for timer

                self.tiles[x][y] = tile

        # loop again to find nearby mines and display number on tile
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                mc = 0
                for n in self.getNeighbors(x, y):
                    mc += 1 if n["isMine"] else 0
                self.tiles[x][y]["mines"] = mc

    def restart(self):
        self.setup()
        self.refreshLabels()

    def refreshLabels(self):
        self.labels["flags"].config(text = "Flags: "+str(self.flagCount))
        self.labels["mines"].config(text = "Mines: "+str(self.mines))

    def gameOver(self, won, xnum, ynum):
        for x in range(0, SIZE_X):
            for y in range(0, SIZE_Y):
                if self.tiles[x][y]["isMine"] == False and self.tiles[x][y]["state"] == STATE_FLAGGED:
                    self.tiles[x][y]["button"].config(image = self.images["wrong"])
                if self.tiles[x][y]["isMine"] == True and self.tiles[x][y]["state"] != STATE_FLAGGED:
                    self.tiles[x][y]["button"].config(image = self.images["mine"])

        if not won:
            self.tiles[xnum][ynum]["button"].config(image = self.images["BEWM"])
            self.MasterButton.config(image=self.images["lose"])
        else:
            self.MasterButton.config(image=self.images["win"])

        self.tk.update()

        msg = "You Win! Play again?" if won else "You Lose! Play again?"
        res = tkMessageBox.askyesno("Game Over", msg)
        if res:
            self.restart()
        else:
            self.tk.quit()

    def updateTimer(self):
        ts = "00:00:00"
        if self.startTime != None:
            delta = datetime.now() - self.startTime
            ts = str(delta).split('.')[0] # drop ms
            if delta.total_seconds() < 36000:
                ts = "0" + ts # zero-pad
        self.labels["time"].config(text = ts)
        self.frame.after(100, self.updateTimer)

    def getNeighbors(self, x, y):
        neighbors = []
        coords = [
            {"x": x-1,  "y": y-1},  #top right
            {"x": x-1,  "y": y},    #top middle
            {"x": x-1,  "y": y+1},  #top left
            {"x": x,    "y": y-1},  #left
            {"x": x,    "y": y+1},  #right
            {"x": x+1,  "y": y-1},  #bottom right
            {"x": x+1,  "y": y},    #bottom middle
            {"x": x+1,  "y": y+1},  #bottom left
        ]
        for n in coords:
            try:
                neighbors.append(self.tiles[n["x"]][n["y"]])
            except KeyError:
                pass
        return neighbors

    def onClickWrapper(self, x, y):
        return lambda Button: self.onClick(self.tiles[x][y], x, y)

    def onRightClickWrapper(self, x, y):
        return lambda Button: self.onRightClick(self.tiles[x][y])

    def onClick(self, tile, x, y):
        if self.startTime == None:
            self.startTime = datetime.now()

        if tile["isMine"] == True:
            # end game
            self.gameOver(False, x, y)
            return

        # change image
        if tile["mines"] == 0:
            tile["button"].config(image = self.images["clicked"])
            self.clearSurroundingTiles(tile["id"])
        else:
            tile["button"].config(image = self.images["numbers"][tile["mines"]-1])
        # if not already set as clicked, change state and count
        if tile["state"] != STATE_CLICKED:
            tile["state"] = STATE_CLICKED
            self.clickedCount += 1
        if self.clickedCount == (SIZE_X * SIZE_Y) - self.mines:
            self.gameOver(True, x, y)

    def onRightClick(self, tile):
        if self.startTime == None:
            self.startTime = datetime.now()

        # if not clicked
        if tile["state"] == STATE_DEFAULT:
            tile["button"].config(image = self.images["flag"])
            tile["state"] = STATE_FLAGGED
            tile["button"].unbind(BTN_CLICK)
            # if a mine
            if tile["isMine"] == True:
                self.correctFlagCount += 1
            self.flagCount += 1
            self.refreshLabels()
        # if flagged, unflag
        elif tile["state"] == 2:
            tile["button"].config(image = self.images["plain"])
            tile["state"] = 0
            tile["button"].bind(BTN_CLICK, self.onClickWrapper(tile["coords"]["x"], tile["coords"]["y"]))
            # if a mine
            if tile["isMine"] == True:
                self.correctFlagCount -= 1
            self.flagCount -= 1
            self.refreshLabels()

    def clearSurroundingTiles(self, id):
        queue = deque([id])
        
        while len(queue) != 0:
            key = queue.popleft()
            parts = key.split("_")
            x = int(parts[0])
            y = int(parts[1])

            for tile in self.getNeighbors(x, y):
                self.clearTile(tile, queue)

    def clearTile(self, tile, queue):
        if tile["state"] != STATE_DEFAULT:
            return

        if tile["mines"] == 0:
            tile["button"].config(image = self.images["clicked"])
            queue.append(tile["id"])
        else:
            tile["button"].config(image = self.images["numbers"][tile["mines"]-1])

        tile["state"] = STATE_CLICKED
        self.clickedCount += 1

    #def setDiff(self, diff, bypass):
    #    if diff == "Easy":
    #        SIZE_X = 10
    #        SIZE_Y = 10
    #    elif diff == "Medium":
    #        SIZE_X = 20
    #        SIZE_Y = 15
    #    elif diff == "Hard":
    #        SIZE_X = 30
    #        SIZE_Y = 20
    #
    #    if (bypass):
    #        self.restart()



### END OF CLASSES ###

def main():
    # create Tk instance
    window = Tk()
    # set program title
    window.title("Lowco's Minesweeper")
    # Change iso image
    window.iconbitmap("images/lowco/logo.ico")
    # create game instance
    minesweeper = Minesweeper(window)
    # run event loop
    window.mainloop()

if __name__ == "__main__":
    main()
