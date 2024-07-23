import pygame
from pygame.locals import *
from assets import GAME_ASSETS
from file_id_interpreter import FileIdInterpreter
from sprites.entity import Entity

class Npc(Entity):
    """Class representing an Npc entity.
    
    Attributes:
        name (str): Name of npc.
        dialogue (str): Dialogue npc says when interacted with.

        (Inherited)
        surf (pygame.Surface): Image of npc. Size: 64 x 64, transparent.
        xcoord (int): Board xcoord of npc.
        ycoord (int): Board ycoord of npc.
    """

    # Attributes
    __name = None
    __dialogue = None

    # Constructor
    def __init__(self, npc_id: str, xcoord: int, ycoord: int):
        # Getting and unpacking file info
        attrib_list = FileIdInterpreter().interpretFileInfo('gameinfostorage/npc_id.txt', npc_id)
        image_name, name, dialogue = attrib_list
        # Setting npc object's attributes.
        super().__init__(pygame.image.load(GAME_ASSETS[image_name]).convert_alpha(), 
                         xcoord, ycoord)
        self.setName(name)
        self.setDialogue(dialogue)

    # Getters
    def getName(self):
        return self.__name
    def getDialogue(self):
        return self.__dialogue

    # Setters
    def setName(self, name):
        self.__name = name
    def setDialogue(self, dialogue):
        self.__dialogue = dialogue