import pygame
from assets import GAME_ASSETS
from typing import Optional
from sprites.button import Button
from math import ceil

class GameEventDisplay(pygame.sprite.Sprite):
    """
    Represents the display to which game events are sent.
    There are two types:
        Valid: Represents events that have occurred during the last valid user turn.
        4 lines of these displayed at a time. TODO add cycle functionality between pages
        These events should be replaced when user next has a valid turn.
        The set of these events are:
            - User attacks enemy(s). 
            - Enemy attacks user.
            - Enemy faints.
            - Npc says something to user.

        Invalid: Represents an error message for an invalid user turn
        1 line displayed at a time.
        Event should be replaced when user next has a valid or invalid turn.
        These events represent erroneous user turns, these being:
            - User walks into wall/entity.
            - User selects invalid target(s) for attack.
            - User interacts with invalid/nonexistent entity.
            - User attempts to enter portal without clearing all enemies

    Attributes:
        surf (pygame.Surface): Surface to which all events are displayed. Size: 432 x 324
        valid_event_list (Optional[list[str]]): List of valid events. To be updated after a valid turn
        event_dict (Optional[dict[tuple[int, int], str]])
        invalid_event (Optional[str]): Invalid event. To be replaced after a valid or invalid turn
        displayed_event (list[str]): Currently displayed valid events, 
        button_group (pygame.sprite.Group): Group containing all buttons.
            Up to 1 button: 'Next Page'

    Methods: TODO just turn into update() method
        updateSurf(self, pygame_events: list[pygame.event.Event]) -> None:
            Draws all text representing events onto surf.
            To be run upon a user action - after a turn has been calculated
        cycleEventDisplay(self) -> None:
            TODO eventdisplay has to be some separate attribute. Otherwise we cannot interact with it from game_world. 
        
    """

    # Attributes
    __surf = None
    __valid_event_list = None
    __invalid_event = None

    # Constructor
    def __init__(self):
        super().__init__()
        self.setSurf(pygame.Surface((432, 324)))

    # Getters
    def getSurf(self):
        return self.__surf
    def getValidEventList(self):
        return self.__valid_event_list
    def getInvalidEvent(self):
        return self.__invalid_event

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setValidEventList(self, valid_event_list):
        self.__valid_event_list = valid_event_list
    def setInvalidEvent(self, invalid_event):
        self.__invalid_event = invalid_event

    # Methods
    def updateSurf(self, pygame_events: list[pygame.event.Event]) -> None:
        """
        Draws all text representing events onto surf.
        To be run upon a user action - after a turn has been calculated
        """
        font = pygame.font.Font(None, 24)
        valid_event_list = self.getValidEventList()
        invalid_event = self.getInvalidEvent()

        # Clears surface, and draws template.
        surf = self.getSurf()
        surf.fill((0, 0, 0))
        pygame.draw.rect(surf, (255, 255, 255), (5, 5, 422, 314), 5) # Border
        pygame.draw.line(surf, (255, 255, 255), (5, 250), (422, 250), 5) # Separator between valid/invalid event
        title_text = font.render('GAME EVENT OUTPUT', True, (255, 255, 255))
        title_text_rect = title_text.get_rect()
        title_text_rect.center = (216, 24)
        surf.blit(title_text, title_text_rect)

        # Creates event_dict:
        #   Relates position tuples (page_number, page_pos), to each element in valid_event_list.
        event_dict = dict()
        total_pages = max(ceil(len(valid_event_list) / 4), 1) # if 0 elements exist, set to 1 page.
        for pos, event in enumerate(valid_event_list):
            page_number = ceil(pos / 4)
            page_pos = pos % 4
            event_dict[(page_number, page_pos)] = event

        # TODO initialises 'Next Page' button
        if total_pages >= 2:
            pass # init it

        
    def cycleEventDisplay(self) -> None:
        pass