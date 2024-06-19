import pygame
from pygame.locals import *
from assets import GAME_ASSETS
from file_id_interpreter import FileIdInterpreter

class Npc(pygame.sprite.Sprite):
    """
    Attributes:
        surf (pygame.Surface): Surface of npc
        image (pygame.image): Image for npc
        rect (pygame.Rect): Rectangle representing position of npc surface
        name (str): Name of npc
        dialogue (str): Dialogue npc says
        xcoord (int): xcoord of npc
        ycoord (int): ycoord of npc

    Methods: TODO
    """

    # Attributes
    __surf = None
    __image = None
    __rect = None
    __name = None
    __dialogue = None
    __xcoord = None
    __ycoord = None

    # Constructor
    def __init__(self, npc_id: str, xcoord: int, ycoord: int):
        # Getting and unpacking file info
        attribute_list = FileIdInterpreter().interpretFileInfo('gameinfostorage/npc_id.txt', npc_id) # [image, name, dialogue]
        image, name, dialogue = attribute_list # unpacks all npc information
        
        # Initialising npc object.
        super().__init__()
        self.setImage(pygame.image.load(GAME_ASSETS[image]))
        self.setName(name)
        self.setDialogue(dialogue)
        self.setXcoord(xcoord)
        self.setYcoord(ycoord)
        self.setSurf(pygame.Surface((64, 64), SRCALPHA))
        self.setRect(self.getSurf().get_rect())


    # Getters
    def getSurf(self):
        return self.__surf
    def getImage(self):
        return self.__image
    def getRect(self):
        return self.__rect
    def getName(self):
        return self.__name
    def getDialogue(self):
        return self.__dialogue
    def getXcoord(self):
        return self.__xcoord
    def getYcoord(self):
        return self.__ycoord

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setImage(self, image):
        self.__image = image
    def setRect(self, rect):
        self.__rect = rect
    def setName(self, name):
        self.__name = name
    def setDialogue(self, dialogue):
        self.__dialogue = dialogue
    def setXcoord(self, xcoord):
        self.__xcoord = xcoord
    def setYcoord(self, ycoord):
        self.__ycoord = ycoord