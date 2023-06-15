import tkinter as tk
class WireWorldButton():
    def __init__(self, parent, x, y):
        self.parent = parent
        self.colors = ["#000000", "#ffff00", "#0000ff", "#ff0000"]
        self.colorIndex = 0
        self.color = self.colors[self.colorIndex]
        self.button = tk.Button(self.parent, height= 2, width= 4, bg = self.color)
        self.button.grid(row = y, column= x)
        self.button.bind("<Button-1>", self.nextColor)
        self.button.bind("<Button-3>", self.previousColor)
    def nextColor(self, event):
        self.colorIndex += 1
        if self.colorIndex > 3: self.colorIndex = 0
        self.button.config(bg = self.colors[self.colorIndex])
    def previousColor(self, event):
        self.colorIndex -= 1
        if self.colorIndex < 0: self.colorIndex = 3
        self.button.config(bg = self.colors[self.colorIndex])
    def updateColor(self):
        self.button.config(bg = self.colors[self.colorIndex])
class World():
    def __init__(self, root, sizeX, sizeY):
        self.root = root
        self.gridFrame = tk.Frame(self.root)
        self.gridFrame.pack()
        self.infoFrame = tk.Frame(self.root)
        self.infoFrame.pack()
        self.speed = 1000
        self.controlsLabel = tk.Label(self.infoFrame, text= "Controls\n <s> Start <d> Pause\n <c> Clear\n <L-Shift> Increase Speed <L-Ctrl> Decrease Speed", font= "Arial 10")
        self.controlsLabel.pack(pady = 20, side= "left", anchor="w")
        self.updatingFrame = tk.Frame(self.infoFrame)
        self.updatingFrame.pack(side= "right")
        self.stateLabel = tk.Label(self.updatingFrame, text = "State: Stopped", font = "Arial 15", fg= "red")
        self.stateLabel.pack(padx= 30, side = "top")
        self.tickLabelText = "Ticking every: "+f"{self.speed:0.0f}ms"
        self.tickLabel = tk.Label(self.updatingFrame, text = self.tickLabelText, font = "Arial 15")
        self.tickLabel.pack(padx= 30, side = "bottom")
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.valueMatrix = []
        self.cellMatrix = []
        self.isTicking = False
        self.root.bind("<s>", self.start)
        self.root.bind("<c>", self.clear)
        self.root.bind("<d>", self.pause)
        self.root.bind("<Shift_L>", self.upSpeed)
        self.root.bind("<Control_L>", self.downSpeed)
        for y in range(self.sizeY):
            rawValueMatrix = []
            rawCellMatrix = []
            for x in range(self.sizeX):
                b= WireWorldButton(self.gridFrame, x, y)
                rawValueMatrix.append(b.colorIndex)
                rawCellMatrix.append(b)
            self.valueMatrix.append(rawValueMatrix)
            self.cellMatrix.append(rawCellMatrix)
    def start(self, event):
        if self.isTicking: return
        self.isTicking = True
        self.stateLabel.config(text= "State: Running", fg = "green")
        self.tick()
    def pause(self, event):
        self.isTicking = False
        self.stateLabel.config(text= "State: Stopped", fg = "red")
    def upSpeed(self, event):
        self.increaseSpeed()
    def downSpeed(self, event):
        self.decreaseSpeed()
    def printState(self):
        for y in self.valueMatrix:
            print(y)
    def updateDataValues(self):
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                self.valueMatrix[y][x] = self.cellMatrix[y][x].colorIndex
    def checkNeighbours(self, x, y):
        eh = 0
        for yIterator in range(-1, 2):
            for xIterator in range(-1, 2):
                if not(xIterator == 0 and yIterator == 0):
                    if x + xIterator >= 0 and x + xIterator < self.sizeX and y + yIterator >= 0 and y + yIterator < self.sizeY:
                        val = self.valueMatrix[y + yIterator][x + xIterator]
                        if val == 2: 
                            eh += 1
                            temp = 1
                        else: temp = 0
                        #print(f"{x},{y}   ---> {x+xIterator}, {y+yIterator} ({val}) [{temp}]")   
        return eh
    def tick(self):
        if not self.isTicking: return
        #self.printState()
        #print("")
        self.updateDataValues()
        tempValueMatrix = []
        for y in range(self.sizeY):
            rawValueMatrix = []
            for x in range(self.sizeX):
                eh = self.checkNeighbours(x, y)
                #print(f"{x}-{y} - > {eh}")
                cellValue = self.valueMatrix[y][x]
                if cellValue == 1 and eh > 0 and eh < 3: newValue = 2
                elif cellValue == 1: newValue = 1
                if cellValue == 2: newValue = 3
                elif cellValue == 3: newValue = 1
                elif cellValue == 0: newValue = 0
                rawValueMatrix.append(newValue)
            tempValueMatrix.append(rawValueMatrix)
        self.valueMatrix = tempValueMatrix[:]
        self.updateColors()
        self.root.after(int(self.speed), self.tick)  
        
    def updateColors(self):
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                self.cellMatrix[y][x].colorIndex = self.valueMatrix[y][x]
                self.cellMatrix[y][x].updateColor()
    def clear(self, event):
        self.isTicking = False
        self.stateLabel.config(text= "State: Stopped", fg = "red")
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                self.valueMatrix[y][x] = 0
            self.updateColors()
    def increaseSpeed(self):
        self.speed -= 50
        if self.speed <= 0: self.speed = 50
        self.tickLabelText = "Ticking every: "+f"{self.speed:0.0f}ms"
        self.tickLabel.config(text = self.tickLabelText)
    def decreaseSpeed(self):
        self.speed += 50
        if self.speed >= 5000: self.speed = 50000
        self.tickLabelText = "Ticking every: "+f"{self.speed:0.0f}ms"
        self.tickLabel.config(text = self.tickLabelText)
root = tk.Tk()
root.resizable(False, False)
w = World(root, 20, 15)
root.mainloop()