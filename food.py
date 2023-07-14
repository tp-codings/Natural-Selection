import random
import pygame as py
import os

FOOD_IMG = py.transform.scale(py.image.load(os.path.join("Bilder", "Cookie.png")), (15, 15))

class Food:
    def __init__(self):
        self.x_ = random.random() * 850 + 50
        self.y_ = random.random() * 550 + 50
        self.width_ = FOOD_IMG.get_width()
        self.height_ = FOOD_IMG.get_height()
        self.foodIMG_ = FOOD_IMG
        #self.colorFill_ = (0, 255, 0)
        #self.colorBorder_ = (0, 0, 0)
    
    def draw(self, win):
        #py.draw.rect(win, self.colorFill_, py.Rect(self.x_, self.y_, self.width_, self.height_))
        #py.draw.rect(win, self.colorBorder_, py.Rect(self.x_, self.y_, self.width_, self.height_),2)
        win.blit(self.foodIMG_, (self.x_, self.y_))
    
    def getMask(self):
        return py.mask.from_surface(self.foodIMG_)
        