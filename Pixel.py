# A class containing info on a particular pixel on the screen at some given time
# Location, color, direction...

import pygame
import tkinter as tk

sysInfo = tk.Tk()


class Pixel:

    # inits a matrix of all pixels, each pixel 10x10 real pixels (subject to change)
    # EDGES: Left, top: 0,0  --  bottom,right: 104, 192
    def __init__(self, screen, x, y):
        self.scaleFactor = 7
        self.screenWidth = sysInfo.winfo_screenwidth()
        self.screenHeight = sysInfo.winfo_screenheight()
        self.screenWidth = self.screenWidth // self.scaleFactor
        self.screenHeight = self.screenHeight // self.scaleFactor
        self.x = x
        self.y = y
        self.screen = screen
        self.neighbors = []
        self.color=(0,0,0)

    # RGB color
    def draw(self, color, pixels, x=0, y=0, pix=None,):
        if pix is not None:
            pygame.draw.rect(self.screen, color, (pix.x * self.scaleFactor, pix.y * self.scaleFactor, self.scaleFactor, self.scaleFactor))
            pixels[(pix.x,pix.y)].color = color
            self.color = color
        else:
            pygame.draw.rect(self.screen, color, (x * self.scaleFactor, y * self.scaleFactor, self.scaleFactor, self.scaleFactor))
            pixels[(x,y)].color = color
            self.color = color

    #set neighbors
    def setNeighbors(self, pixel, window):
        self.neighbors = self.getNeighbors(pixel, window)

    # if pixel is touching the border, which border
    def isOnEdge(self, pixel):
        if pixel.x == 0: return "left"
        if pixel.x + 1 == self.screenWidth: return "right"
        return None

    def getNeighbors(self, pixel, window):
        if self.isOnEdge(pixel) is None: return [self.isLive(window.pixAtLocation(pixel.x - 1, pixel.y)),self.isLive(pixel),
                                                 self.isLive(window.pixAtLocation(pixel.x + 1, pixel.y))]

        if self.isOnEdge(pixel) == "left": return [self.isLive(window.pixAtLocation(pixel.x + 1, pixel.y)), self.isLive(pixel), self.isLive(window.pixAtLocation(self.screenWidth-1, pixel.y))]

        if self.isOnEdge(pixel) == "right": return [self.isLive(window.pixAtLocation(pixel.x - 1, pixel.y)),self.isLive(pixel), self.isLive(window.pixAtLocation(0, pixel.y))]

    def isLive(self,cell):
        if self.screen.get_at((cell.x * 7, cell.y * 7))[:3] != (0,0,0):
            return True
        else:
            return False



