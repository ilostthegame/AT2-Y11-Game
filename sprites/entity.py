import pygame
from pygame.locals import SRCALPHA

class Entity(pygame.sprite.Sprite):
    """Class representing a board entity.

    Attributes:
        surf (pygame.Surface): Size: 64 x 64, transparent.
        xcoord (int): Board xcoord of entity.
        ycoord (int): Board ycoord of entity.
    """

    # Attributes
    __surf = None
    __xcoord = None
    __ycoord = None

    # Constructor
    def __init__(self, 
                 surf: pygame.Surface,
                 xcoord: int, 
                 ycoord: int):
        super().__init__()
        self.setSurf(surf)
        self.setXcoord(xcoord)
        self.setYcoord(ycoord)

    # Getters
    def getSurf(self):
        return self.__surf
    def getXcoord(self):
        return self.__xcoord
    def getYcoord(self):
        return self.__ycoord

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setXcoord(self, xcoord):
        self.__xcoord = xcoord
    def setYcoord(self, ycoord):
        self.__ycoord = ycoord

