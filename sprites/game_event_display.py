import pygame
from typing import Optional
from button import Button

class GameEventDisplay(pygame.sprite.Sprite):
    """
    Represents the display to which game events are sent.
    Setting of valid_event_list, invalid_event should be handled outside function.
    There are two types:
        Valid: Represents events that have occurred during a user action
        4 lines of these displayed at a time, with cycle functionality. TODO later
        These events should be replaced when user next does a 'valid' action.
        The set of these events are:
            - User attacks enemy(s). 
            - Enemy attacks user.
            - Enemy faints.
            - Npc says something to user.

        Invalid: Represents an error message for an invalid user action
        1 line displayed at a time.
        Event should be replaced when user next does any action.
        These events represent erroneous user actions, these being:
            - User walks into wall/entity.
            - User selects invalid target(s) for attack.
            - User interacts with invalid/nonexistent entity.
            - User attempts to enter portal without clearing all enemies

    Attributes:
        surf (pygame.Surface): Surface to which all events are displayed. Size: 432 x 324
        valid_event_list (list[str]): List of valid events
        invalid_event (Optional[str]): invalid

    Methods:
        run(self) -> None:
            Draws all events onto surf.
            To be run whenever 
    """


    # Attributes
    __surf = None

    # Constructor
    def __init__(self):
        self.setSurf(pygame.Surface((432, 324)))
        self.getSurf().fill('red')

    # Getters
    def getSurf(self):
        return self.__surf

    # Setters
    def setSurf(self, surf):
        self.__surf = surf