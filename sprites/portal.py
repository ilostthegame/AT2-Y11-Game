import pygame
from pygame.locals import *
from assets import GAME_ASSETS
from file_id_interpreter import FileIdInterpreter

class Portal(pygame.sprite.Sprite):
    """Class representing a portal entity.

    Attributes:
        surf (pygame.Surface): Represents portal's image. Size: 64 x 64, transparent
        xcoord (int): Board xcoord of portal
        ycoord (int): Board ycoord of portal
        destination (str): Represents the level portal leads to
    """

    # Attributes
    __surf = None
    __xcoord = None
    __ycoord = None
    __destination = None

    # Constructor
    def __init__(self, portal_id: str, xcoord: int, ycoord: int):
        # Getting and unpacking file info
        image_name, destination = FileIdInterpreter().interpretFileInfo('gameinfostorage/portal_id.txt', portal_id) 
        
        # Setting portal object's attributes
        super().__init__()
        self.setSurf(pygame.image.load(GAME_ASSETS[image_name]).convert_alpha())
        self.setXcoord(xcoord)
        self.setYcoord(ycoord)
        self.setDestination(destination)

    # Getters
    def getSurf(self):
        return self.__surf
    def getXcoord(self):
        return self.__xcoord
    def getYcoord(self):
        return self.__ycoord
    def getDestination(self):
        return self.__destination

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setXcoord(self, xcoord):
        self.__xcoord = xcoord
    def setYcoord(self, ycoord):
        self.__ycoord = ycoord
    def setDestination(self, destination):
        self.__destination = destination
