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

class Punktdiagramm:
  def __init__(self, pos, numSets = 1):
    self.posX = pos[0]
    self.posY = pos[1]

    self.fig = pylab.figure(figsize=[4,4], dpi= 70)
    self.ax1 = self.fig.gca()
    
    #plt.ylabel("Alive")
    plt.xlabel("Days")
    plt.grid(True)
    #plt.legend(self.ax1.get_label(), loc= 'upper left')

    self.labels = []

    self.canvas = agg.FigureCanvasAgg(self.fig)       #Workaround mpl mit pygame, weil mpl normal über tkinter
    self.canvas.draw()
    self.renderer = self.canvas.get_renderer()
    self.raw_data = self.renderer.tostring_rgb()
    
    self.win = pygame.display.set_mode((900, 400))
    self.screen = pygame.display.get_surface()

    self.size = self.canvas.get_width_height()

    self.surf = pygame.image.fromstring(self.raw_data, self.size, "RGB")
    self.x_ = []
    self.y_ = []
    for n in range(numSets):
      print("true")
      self.x_.append([])
      self.y_.append([])


  def update(self, datasets):             #datasets: [(x1,x1, name1, col1), (x2,y2, name2, col2), ...]
    for i,data in enumerate(datasets):
      self.x_[i].append(data[0])
      self.y_[i].append(data[1])
    
    for n, i in enumerate(datasets):
      self.ax1.plot([np.array(self.x_[n])],[np.array(self.y_[n])], datasets[n][3], label=datasets[n][2],)
      if datasets[n][2] not in self.labels:
        self.labels.append(datasets[n][2])
    
    self.ax1.legend(loc= 'lower right', labels= self.labels)
    plt.grid(True)
    self.canvas = agg.FigureCanvasAgg(self.fig)
    self.canvas.draw()
    self.renderer = self.canvas.get_renderer()
    self.raw_data = self.renderer.tostring_rgb()
    
    pygame.display.flip()

  def animate(self):
    #self.ax1.clear()
    self.ax1.plot([np.array(self.x_)],[np.array(self.y_)])
  
  def show(self):
    
    self.surf = pygame.image.fromstring(self.raw_data, self.size, "RGB")
    self.screen.blit(self.surf, (self.posX,self.posY))
    pygame.display.flip()
    #ani = animation.FuncAnimation(self.fig, self.animate, interval = 1000)
    #pygame.display.update()