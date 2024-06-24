import pygame
from pygame.locals import *
from assets import GAME_ASSETS
from file_id_interpreter import FileIdInterpreter

class Portal(pygame.sprite.Sprite):
    """
    Class representing a portal object

    Attributes:
        image (pygame.Surface): Represents portal's image. Size: 64 x 64, transparent
        xcoord (int): Board xcoord of portal
        ycoord (int): Board ycoord of portal
        destination (str): Represents the level portal leads to
    """

    # Attributes
    __image = None
    __xcoord = None
    __ycoord = None
    __destination = None

    # Constructor
    def __init__(self, portal_id: str, xcoord: int, ycoord: int):
        # Getting and unpacking file info
        image_name, destination = FileIdInterpreter().interpretFileInfo('gameinfostorage/portal_id.txt', portal_id) 
        
        # Initialising portal object.
        super().__init__()
        self.setImage(pygame.image.load(GAME_ASSETS(image_name)).convert_alpha())
        self.setXcoord(xcoord)
        self.setYcoord(ycoord)
        self.setDestination(destination)

    # Getters
    def getImage(self):
        return self.__image
    def getXcoord(self):
        return self.__xcoord
    def getYcoord(self):
        return self.__ycoord
    def getDestination(self):
        return self.__destination

    # Setters
    def setImage(self, image):
        self.__image = image
    def setXcoord(self, xcoord):
        self.__xcoord = xcoord
    def setYcoord(self, ycoord):
        self.__ycoord = ycoord
    def setDestination(self, destination):
        self.__destination = destination
