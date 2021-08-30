from Pixel import Pixel
import random
import threading


class cells:
    def __init__(self, xCells, screenHeight, screen, pixels):
        self.window = None
        self.startRandRange = random.randrange(4, 6)
        self.randoms = [0, 0, 0, 0, 0, 0, 0, 0]
        self.pixels = pixels
        self.activeRows = 1
        self.row = {}
        self.screen = screen
        self.nextState = {}
        self.color = (205, 125, 255)
        self.width = xCells
        self.height = screenHeight - 1
        self.setRandoms()

        for x in range(self.width):
            self.row[self.pixels[(x, screenHeight - 1)]] = self.pixels[(x, screenHeight - 1)]
        self.pixels[(self.width // 2, self.height)].draw(self.color, self.pixels,
                                                         pix=self.pixels[(self.width // 2, self.height)])

    # Init random evolution ruleset
    def setRandoms(self):
        setRands = 0
        self.randoms = [0, 0, 0, 0, 0, 0, 0, 0]
        while setRands < self.startRandRange:
            rand = random.randrange(0, 7)
            if self.randoms[rand] != 1:
                self.randoms[rand] = 1
                setRands += 1

    def setWindow(self, window):
        self.window = window

    # Evolve row 0 cells and shift all rows up 1
    def evolve(self):
        # Generate next evolution for bottom row in sep thread
        newRowThread = threading.Thread(target=self.evolveCell())
        newRowThread.start()

        # Shift all rows up
        for y in range(self.activeRows):
            for x in range(self.width):
                cell = self.pixels[(x, self.height - self.activeRows + y + 1)]
                if cell.color != self.window.pixAtLocation(x, (cell.y) - 1).color:
                    cell.draw(cell.color, self.pixels, x=cell.x, y=cell.y - 1)

        # active rows cannot exceed screen height
        if self.activeRows < self.height:
            self.activeRows += 1

        # wait for next row thread
        newRowThread.join()
        # After shifting all past rows up, fill bottom row with previously generated next row
        for cell in self.row:
            if self.nextState[cell] == 1:
                cell.draw(self.color, self.pixels, pix=cell)
            else:
                cell.draw((0, 0, 0), self.pixels, pix=cell)
        self.nextState = {}

    # evolve cells in bottom row according to current evolution rule
    def evolveCell(self):
        for cell in self.row:
            state = cell.getNeighbors(cell, self.window)
            if state == [1, 1, 1]: self.nextState[cell] = self.randoms[0]
            if state == [1, 1, 0]: self.nextState[cell] = self.randoms[1]
            if state == [1, 0, 1]: self.nextState[cell] = self.randoms[2]
            if state == [1, 0, 0]: self.nextState[cell] = self.randoms[3]
            if state == [0, 1, 1]: self.nextState[cell] = self.randoms[4]
            if state == [0, 1, 0]: self.nextState[cell] = self.randoms[5]
            if state == [0, 0, 1]: self.nextState[cell] = self.randoms[6]
            if state == [0, 0, 0]: self.nextState[cell] = self.randoms[7]
