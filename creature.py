import pygame as py
import random
import math
import os
import numpy as np
#from PIL import Image, ImageEnhance


CREATURE_IMG = py.transform.scale(py.image.load(os.path.join("Bilder", "Slime.png")), (40, 40))
ENERGY = 500

class Creature:
    def __init__(self, mutVel = 1, mutSize = 1, mutEff = 1, mutRisk = 1):

        #Objekteigenschaften
        #Als Bild
        self.creatureIMG_ = CREATURE_IMG
        #Als Rechteck
        self.rectSurface_ = py.Surface((40,40))
        self.rect_ = py.Rect(0,0,40, 40)
        self.colorFill_ = [125, 125, 125]
        self.colorBorder_ = (0, 0, 0)

        self.width_ = 0
        self.height_ = 0
        #self.initSize(self.creatureIMG_)
        self.initSize(self.rectSurface_)

        #Position
        self.side_ = random.randint(0, 1)       #0 -> links rechts, 1 -> oben unten
        self.sideIndex_ = random.randint(0, 1)
        self.x_ = 0
        self.y_ = 0
        self.initPos()

        #Mutationseigenschaften
        self.energy_ = ENERGY
        self.vel_ = 5
        self.size_ = self.width_ * self.height_ * 0.05
        self.mass_ = self.size_ * 0.1
        self.effizienz_ = 12
        self.risk_ = 0.5        #Welches Risiko gehen sie ein, noch ein zweites Essen zu suchen -> Eigentlich nur, bis zu welchem Mindestenergielevel sie auf Suche sind
        self.initMutation(mutVel, mutSize, mutEff, mutRisk)
        
        #Rundeneigenschaften
        self.state_ = 0
        self.amountIntus_ = 0
        self.atHome_ = False
        
#INITS      
    def initSize(self, surface):
        self.width_ = surface.get_width()
        self.height_ = surface.get_height()
    
    #Positioniert Kreatur zufällig um das Rechteck
    def initPos(self):
        if(self.side_ == 0 and self.sideIndex_ == 0):
            self.x_ = 10
            self.y_ = random.random()*600+50
        if(self.side_ == 0 and self.sideIndex_ == 1):
            self.x_ = 950
            self.y_ = random.random()*600+50
        if(self.side_ == 1 and self.sideIndex_ == 0):
            self.x_ = random.random()*900+50
            self.y_ = 10
        if(self.side_ == 1 and self.sideIndex_ == 1):
            self.x_ = random.random()*900+50
            self.y_ = 650

    def initMutation(self, mutVel = 1, mutSize = 1, mutEff = 1, mutRisk = 1):
        #print(mutVel, mutSize, mutEff, mutRisk)
        #Vel
        self.vel_ *= mutVel
        self.colorFill_[1] *= mutVel
        self.colorFill_[0] *= mutVel

        #Size
        self.size_ *= mutSize
        #self.creatureIMG_ = py.transform.scale(self.creatureIMG_, (self.creatureIMG_.get_width()*mutSize, self.creatureIMG_.get_height()*mutSize))
        #self.width_ = self.creatureIMG_.get_width()
        #self.height_ = self.creatureIMG_.get_height() 
        
        self.rectSurface_ = py.transform.scale(self.rectSurface_, (self.rectSurface_.get_width()*mutSize, self.rectSurface_.get_height()*mutSize))
        self.width_ = self.rectSurface_.get_width()
        self.height_ = self.rectSurface_.get_height()
        self.rect_ = py.Rect(0,0, self.width_, self.height_)

        self.mass_ = self.size_ * 0.1

        self.effizienz_ *= mutEff
        self.risk_ *= (1/mutRisk)
        

    def reInit(self):
        self.amountIntus_ = 0
        self.atHome_ = False
        self.energy_ = ENERGY
        self.state_ = 0

#DRAW
    def draw(self, win):
        #win.blit(self.creatureIMG_, (self.x_, self.y_))
        py.draw.rect(self.rectSurface_, self.colorFill_, self.rect_)
        py.draw.rect(self.rectSurface_, self.colorBorder_, self.rect_, 5)
        py.draw.rect(self.rectSurface_, self.colorBorder_, py.Rect(self.x_+self.width_*0.25, self.y_+self.width_*0.25, self.width_*0.1, self.height_*0.1))
        py.draw.rect(self.rectSurface_, self.colorBorder_, py.Rect(self.x_+self.width_*0.75, self.y_+self.width_*0.25, self.width_*0.1, self.height_*0.1))
        win.blit(self.rectSurface_, (self.x_, self.y_))

#MOVE
    def move(self, direction):
        self.x_ += self.vel_ * direction[0]/math.sqrt(direction[0]**2+direction[1]**2)      #Normierung
        self.y_ += self.vel_ * direction[1]/math.sqrt(direction[0]**2+direction[1]**2)

#UPDATE
    def updateEnergy(self):
        self.energy_ -= (self.vel_ * self.mass_) / self.effizienz_

#GETTER
    def getMask(self):
        #return py.mask.from_surface(self.creatureIMG_)
        return py.mask.from_surface(self.rectSurface_)
    
    def getMaxEnergy(self):
        return ENERGY


#anderer Shit der nicht funktioniert, wie er soll
    def setIMG(self, newColor):
        self.creatureIMG_.fill((0,0,0,255), None, py.BLEND_RGBA_ADD)
        self.creatureIMG_.fill(newColor[0:3] + (0,), None, py.BLEND_RGBA_ADD)
    
    def paletteSwap(self, oldC, newC):
        imc = py.Surface(self.creatureIMG_.get_size())
        imc.fill(newC)
        self.creatureIMG_.set_colorkey(oldC)
        imc.blit(self.creatureIMG_, (0,0))
        return imc


    