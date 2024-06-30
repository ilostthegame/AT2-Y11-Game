import pygame
from assets import GAME_ASSETS
from typing import Optional
from sprites.button import Button
from math import ceil
from button_output_getter import ButtonOutputGetter

class GameEventDisplay(pygame.sprite.Sprite):
    """
    Represents the display to which game events are sent. Has two separate parts:
        Valid events: Exist 6 slots, which can be cycled between.
        Invalid events: Exists 1 slot.

    Attributes:
        surf (pygame.Surface): Surface to which all events are displayed. Size: 432 x 324
        valid_event_list (Optional[list[str]]): List of valid events. To be updated after a valid turn
        invalid_event (Optional[str]): Invalid event. To be replaced after a valid or invalid turn
        total_pages (int): Number of pages. Defaults to 1 if valid_event_list is empty.
        current_page (int): Current page. 0-indexed, defaults to 0 when valid_event_list is updated.
        button_group (pygame.sprite.Group): Group containing 'Prev page' and 'Next page' buttons.

    Methods:
        update(self, 
               pygame_events: list[pygame.event.Event], 
               mouse_pos: tuple[int, int],
               valid_event_list: list[Optional[str]],
               invalid_event: Optional[str]) -> None:

            Updates the events displayed on surf.
            To be run each iteration of GameWorld.

        drawTemplate(self) -> None:
            Draws the template surface onto the surf attribute, overriding previously displayed events.
        getDisplayedEvents(self) -> list[str]:
            Returns a list of valid events to be displayed in the current iteration.
            Uses attributes valid_event_list, total_pages, and current_page.
    """

    # Attributes
    __surf = None
    __valid_event_list = None
    __invalid_event = None
    __total_pages = None
    __current_page = None
    __button_group = None

    # Constructor
    def __init__(self):
        super().__init__()
        self.setSurf(pygame.Surface((432, 324)))
        self.setValidEventList(list())
        self.setInvalidEvent(str())
        self.setTotalPages(1)
        self.setCurrentPage(0)

        # Initialise prev page/next page buttons
        button_group = pygame.sprite.Group()
        button_group.add(Button(pygame.Surface((80, 24)), 'prev page', 16, (255, 255, 255), 'prev page', (60, 248), '-')) 
        button_group.add(Button(pygame.Surface((80, 24)), 'next page', 16, (255, 255, 255), 'next page', (372, 248), '='))
        self.setButtonGroup(button_group)

    # Getters
    def getSurf(self):
        return self.__surf
    def getValidEventList(self):
        return self.__valid_event_list
    def getInvalidEvent(self):
        return self.__invalid_event
    def getTotalPages(self):
        return self.__total_pages
    def getCurrentPage(self):
        return self.__current_page
    def getButtonGroup(self):
        return self.__button_group

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setValidEventList(self, valid_event_list):
        self.__valid_event_list = valid_event_list
    def setInvalidEvent(self, invalid_event):
        self.__invalid_event = invalid_event
    def setTotalPages(self, total_pages):
        self.__total_pages = total_pages
    def setCurrentPage(self, current_page):
        self.__current_page = current_page
    def setButtonGroup(self, button_group):
        self.__button_group = button_group


    # Methods
    def update(self, 
               pygame_events: list[pygame.event.Event], 
               mouse_pos: tuple[int, int],
               valid_event_list: list[Optional[str]],
               invalid_event: Optional[str]) -> None:
        """
        Updates the events displayed on surf.
        To be run each iteration of GameWorld.
        """

        # Checks whether valid_event_list or invalid_event have changed.
        # If valid_event_list has changed, then replace valid_event_list attribute, and set current_page = 1.
        # If invalid_event has changed, then replace invalid_event attribute.
        if valid_event_list != self.getValidEventList():
            self.setValidEventList(valid_event_list)
            self.setCurrentPage(0)
            self.setTotalPages(max(ceil(len(valid_event_list) / 6), 1))
        if invalid_event != self.getInvalidEvent():
            self.setInvalidEvent(invalid_event)

        # Checks for button activations. Changes current_page accordingly
        relative_mouse_pos = (mouse_pos[0] - 768, mouse_pos[1] - 444)
        button_outputs = ButtonOutputGetter().getOutputs(self.getButtonGroup(), pygame_events, relative_mouse_pos)
        if button_outputs:
            button_output = button_outputs[0] # uses first button output
            match button_output:
                case 'prev page':
                    current_page = (self.getCurrentPage() - 1) % self.getTotalPages()
                case 'next page':
                    current_page = (self.getCurrentPage() + 1) % self.getTotalPages()
                case _:
                    raise ValueError(f"Button output '{button_output}' is unknown")
            self.setCurrentPage(current_page)
    
        self.drawTemplate() # Draws template, overriding previously displayed events.

        displayed_events = self.getDisplayedEvents() # list of events to display
        font = pygame.font.Font(None, 24)
        surf = self.getSurf()

        # Create font objects for each displayed valid event, and blit to surf
        for pos, event in enumerate(displayed_events):
            event_surf = font.render(f"> {event}", True, (255, 255, 255))
            event_rect = event_surf.get_rect()
            event_rect.topleft = (15, 50 + pos * 30) 
            surf.blit(event_surf, event_rect)
        
        # If invalid event exists, blit to surf
        if self.getInvalidEvent():
            event_surf = font.render(f"Error: {self.getInvalidEvent()}", True, (255, 255, 255))
            event_rect = event_surf.get_rect()
            event_rect.center = (216, 295)
            surf.blit(event_surf, event_rect)
        
        self.setSurf(surf)
        return

    def drawTemplate(self) -> None:
        """
        Draws the template surface onto the surf attribute, overriding previously displayed events.
        """

        font = pygame.font.Font(None, 24)
        
        # Create title text font object
        title_text_surf = font.render('GAME EVENT OUTPUT', True, (255, 255, 255))
        title_text_rect = title_text_surf.get_rect()
        title_text_rect.center = (216, 30)

        # Create page number font object
        page_number_surf = font.render(f"{self.getCurrentPage() + 1} / {self.getTotalPages()}", True, (255, 255, 255))
        page_number_rect = page_number_surf.get_rect()
        page_number_rect.center = (216, 250)

        # Blit template onto surf
        surf = self.getSurf()
        surf.fill((0, 0, 0))
        pygame.draw.rect(surf, (255, 255, 255), (5, 5, 422, 314), 5) # Border
        pygame.draw.line(surf, (255, 255, 255), (5, 270), (422, 270), 5) # Separator line between valid/invalid event
        surf.blit(title_text_surf, title_text_rect)
        surf.blit(page_number_surf, page_number_rect)
        for button in self.getButtonGroup():
            surf.blit(button.getSurf(), button.getRect())
        self.setSurf(surf)
        return

    def getDisplayedEvents(self) -> list[str]:
        """
        Returns a list of valid events to be displayed in the current iteration.
        Uses attributes valid_event_list, total_pages, and current_page.
        """

        current_page = self.getCurrentPage()
        valid_event_list = self.getValidEventList()
        num_events = len(valid_event_list) # total number of valid events
        
        # Compute the list indexes of events that are to be displayed
        event_indexes = [i for i in range((current_page) * 6, (current_page+1) * 6) if i < num_events]

        displayed_events = [valid_event_list[i] for i in event_indexes]
        return displayed_events
    