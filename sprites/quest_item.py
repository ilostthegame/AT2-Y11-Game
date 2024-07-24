import pygame
from pygame.locals import *
from assets import GAME_ASSETS
from file_id_interpreter import FileIdInterpreter
from sprites.entity import Entity

class QuestItem(Entity):
    """Class representing a quest item entity.

    Attributes:
        name (str): Name of quest item

        (Inherited)
        surf (pygame.Surface): Represents quest item's image. Size: 64 x 64, transparent.
        rect (pygame.Rect): Rectangle representing entity's position
        xcoord (int): Board xcoord of quest item.
        ycoord (int): Board ycoord of quest item.
    """

    # Attributes
    __name = None

    # Constructor
    def __init__(self, quest_item_id: str, xcoord: int, ycoord: int) -> None:
        # Getting and unpacking file info
        attributes = FileIdInterpreter().interpretFileInfo('gameinfostorage/quest_item_id.txt', quest_item_id)
        image_name, name = attributes
        # Setting quest item's object's attributes
        super().__init__(pygame.image.load(GAME_ASSETS[image_name]).convert_alpha(),
                         xcoord, ycoord)
        self.setName(name)
    
    # Getters
    def getName(self):
        return self.__name

    # Setters
    def setName(self, name):
        self.__name = name