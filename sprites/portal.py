import pygame
from pygame.locals import *
from assets import GAME_ASSETS
from file_id_interpreter import FileIdInterpreter
from sprites.entity import Entity

class Portal(Entity):
    """Class representing a portal entity.

    Attributes:
        destination (str): Represents the level portal leads to.
        is_activated (bool): Whether the portal has been activated by Character.

        (Inherited)
        surf (pygame.Surface): Represents portal's image. Size: 64 x 64, transparent.
        xcoord (int): Board xcoord of portal.
        ycoord (int): Board ycoord of portal.
    """

    # Attributes
    __destination = None
    __is_activated = None

    # Constructor
    def __init__(self, portal_id: str, xcoord: int, ycoord: int):
        # Getting and unpacking file info
        attrib_list = FileIdInterpreter().interpretFileInfo('gameinfostorage/portal_id.txt', portal_id)
        image_name, destination = attrib_list
        # Setting portal object's attributes
        super().__init__(pygame.image.load(GAME_ASSETS[image_name]).convert_alpha(),
                         xcoord, ycoord)
        self.setDestination(destination)
        self.setIsActivated(False)

    # Getters
    def getDestination(self):
        return self.__destination
    def getIsActivated(self):
        return self.__is_activated

    # Setters
    def setDestination(self, destination):
        self.__destination = destination
    def setIsActivated(self, is_activated):
        self.__is_activated = is_activated