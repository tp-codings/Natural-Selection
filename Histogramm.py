import numpy as np
import pygame
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import pylab
pygame.init()

class Histogramm:
  def __init__(self, pos, xlabel):
    self.posX = pos[0]
    self.posY = pos[1]
    self.data_ = []

    self.fig = pylab.figure(figsize=[4,4], dpi= 70)
    self.ax1 = self.fig.gca()
    
    plt.ylabel("Amount")
    plt.xlabel(xlabel)
    plt.grid(True)

    self.canvas = agg.FigureCanvasAgg(self.fig)       #Workaround mpl mit pygame, weil mpl normal über tkinter
    self.canvas.draw()
    self.renderer = self.canvas.get_renderer()
    self.raw_data = self.renderer.tostring_rgb()
    
    self.win = pygame.display.set_mode((900, 400))
    self.screen = pygame.display.get_surface()

    self.size = self.canvas.get_width_height()

    self.surf = pygame.image.fromstring(self.raw_data, self.size, "RGB")


  def update(self, data):         #die werden scheinbar die ganze Zeit übereinander gelegt...
    self.data_ = data
    self.ax1.hist(np.array(self.data_))
    plt.grid(True)
    self.canvas = agg.FigureCanvasAgg(self.fig)
    self.canvas.draw()
    self.renderer = self.canvas.get_renderer()
    self.raw_data = self.renderer.tostring_rgb()
    pygame.display.flip()
  
  def show(self):
    self.surf = pygame.image.fromstring(self.raw_data, self.size, "RGB")
    self.screen.blit(self.surf, (self.posX,self.posY))
    pygame.display.flip()
