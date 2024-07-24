import pygame
from pygame.locals import *
from assets import GAME_ASSETS
from file_id_interpreter import FileIdInterpreter
from sprites.entity import Entity
from typing import Optional
from sprites.quest_item import QuestItem

class Portal(Entity):
    """Class representing a portal entity.

    Attributes:
        destination (str): Represents the level portal leads to.
        is_activated (bool): Whether the portal has been activated by Character.
        requirement (Optional[str]): The required quest item to enter portal.

        (Inherited)
        surf (pygame.Surface): Represents portal's image. Size: 64 x 64, transparent.
        rect (pygame.Rect): Rectangle representing entity's position
        xcoord (int): Board xcoord of portal.
        ycoord (int): Board ycoord of portal.
    """

    # Attributes
    __destination = None
    __is_activated = None
    __requirement = None

    # Constructor
    def __init__(self, portal_id: str, xcoord: int, ycoord: int):
        # Getting and unpacking file info
        attributes = FileIdInterpreter().interpretFileInfo('gameinfostorage/portal_id.txt', portal_id)
        image_name, destination, requirement = attributes
        # Setting portal object's attributes
        super().__init__(pygame.image.load(GAME_ASSETS[image_name]).convert_alpha(),
                         xcoord, ycoord)
        self.setDestination(destination)
        self.setIsActivated(False)
        if requirement != 'None':
            self.setRequirement(requirement)
        else:
            self.setRequirement(None)

    # Getters
    def getDestination(self):
        return self.__destination
    def getIsActivated(self):
        return self.__is_activated
    def getRequirement(self):
        return self.__requirement

    # Setters
    def setDestination(self, destination):
        self.__destination = destination
    def setIsActivated(self, is_activated):
        self.__is_activated = is_activated
    def setRequirement(self, requirement):
        self.__requirement = requirement

    # Methods
    def handleEnterAttempt(self, 
                           num_enemies: int, 
                           character_quest_items: set[str]) -> str:
        """Handles character's attempt to enter portal.

        If attempt was successful, sets isActivated to True.
        Returns a string representing the game event caused by entering
        the portal.
        """
        # Checking that number of enemies is 0.
        if num_enemies != 0:
            return "You try to enter a portal, but there are still enemies remaining."
        # Checking that the quest item requirement is satisfied.
        requirement = self.getRequirement()
        if requirement != None:
            if requirement not in character_quest_items:
                return f"You need the {requirement} to enter this portal."
        # If both conditions satisfied, activates portal.
        self.setIsActivated(True)
        return "You entered a portal! You are teleported."