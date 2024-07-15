import pygame
from pygame.locals import *
from assets import GAME_ASSETS
from file_id_interpreter import FileIdInterpreter

class Npc(pygame.sprite.Sprite):
    """Class representing an Npc entity.
    
    Attributes:
        surf (pygame.Surface): Image of npc. Size: 64 x 64, transparent
        name (str): Name of npc
        dialogue (str): Dialogue npc says when interacted with
        xcoord (int): Xcoord of npc
        ycoord (int): Ycoord of npc
    """

    # Attributes
    __surf = None
    __name = None
    __dialogue = None
    __xcoord = None
    __ycoord = None

    # Constructor
    def __init__(self, npc_id: str, xcoord: int, ycoord: int):
        # Getting and unpacking file info
        attribute_list = FileIdInterpreter().interpretFileInfo('gameinfostorage/npc_id.txt', npc_id) # [image_name, name, dialogue]
        image_name, name, dialogue = attribute_list # unpacks all npc information
        
        # Initialising npc object.
        super().__init__()
        self.setSurf(pygame.image.load(GAME_ASSETS[image_name]).convert_alpha())
        self.setName(name)
        self.setDialogue(dialogue)
        self.setXcoord(xcoord)
        self.setYcoord(ycoord)


    # Getters
    def getSurf(self):
        return self.__surf
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
    def setName(self, name):
        self.__name = name
    def setDialogue(self, dialogue):
        self.__dialogue = dialogue
    def setXcoord(self, xcoord):
        self.__xcoord = xcoord
    def setYcoord(self, ycoord):
        self.__ycoord = ycoord