import pygame
import Pixel
import onedimcells
import tkinter as tk

sysInfo = tk.Tk()


class window:
    def __init__(self):
        #init display settings
        pygame.init()
        pygame.display.set_caption("1D Cellular automata")
        self.width = sysInfo.winfo_screenwidth()
        self.height = sysInfo.winfo_screenheight()
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.frozen = False
        self.color = (0,0,0)
        self.scaleFactor = 7
        self.bottomRow = (self.height//self.scaleFactor) -1
        #init pixel matrix
        self.pixels = {}
        self.cleanSlate()
        self.initRowNeighbors()
        self.cells = onedimcells.cells(self.width//self.scaleFactor,self.height//self.scaleFactor,self.screen, self.pixels)



    #blank pixel setup
    def cleanSlate(self):
        for x in range(self.width//self.scaleFactor):
            for y in range(self.height//self.scaleFactor):

                cPix = Pixel.Pixel(self.screen,x,y)
                self.pixels[(x, y)] = cPix
                cPix.draw(self.color,self.pixels, x=x, y=y)

    def initRowNeighbors(self):
        print(self.bottomRow)
        for x in range(self.width//self.scaleFactor):
            self.pixels[(x, self.bottomRow)].setNeighbors(self.pixels[(x, self.bottomRow)], self)



    #return current keyboard/mouse input
    def getEvent(self):
        return pygame.event.get()

    #Get pixel at x,y
    def pixAtLocation(self,x,y):
        return self.pixels[(x,y)]

    # Start/Pause animation
    def freeze(self):
        self.frozen = not self.frozen

    #update screen graphics
    def update(self):
        self.cells.evolve()
        pygame.display.flip()

    #reset sim
    def reset(self):
        self.cleanSlate()
        self.cells.activeRows = 1
        self.pixels[((self.width//self.scaleFactor)//2, self.bottomRow)].draw(self.cells.color, self.pixels, pix=self.pixels[((self.width//self.scaleFactor)//2, self.bottomRow)])
        self.cells.setRandoms()
        self.update()
