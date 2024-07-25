import pygame
from assets import GAME_ASSETS
from typing import Optional
from sprites.button import Button
from math import ceil
from button_output_getter import ButtonOutputGetter
from multiline_text_converter import multiLineSurface

class GameEventDisplay(pygame.sprite.Sprite):
    """Sidebar component that represents the display to which game events are sent.

    Attributes:
        surf (pygame.Surface): Surface to which all events are displayed. Size: 432 x 324
        event_list (list[Optional[str]]): List of events. 
        total_pages (int): Number of pages. Defaults to 1 if event_list is empty.
        current_page (int): Current page. 0-indexed, defaults to 0 when event_list is updated.
        page_nav_buttons (pygame.sprite.Group): Group containing 'Prev page' and 'Next page' buttons.
    """

    # Attributes
    __surf = None
    __event_list = None
    __total_pages = None
    __current_page = None
    __page_nav_buttons = None

    # Constructor
    def __init__(self):
        super().__init__()
        self.setSurf(pygame.Surface((432, 324)))
        self.setEventList([])
        self.setTotalPages(1)
        self.setCurrentPage(0)
        self.createPageNavButtons()

    # Getters
    def getSurf(self) -> pygame.Surface:
        return self.__surf
    def getEventList(self) -> Optional[list[str]]:
        return self.__event_list
    def getTotalPages(self) -> int:
        return self.__total_pages
    def getCurrentPage(self) -> int:
        return self.__current_page
    def getPageNavButtons(self) -> pygame.sprite.Group:
        return self.__page_nav_buttons

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setEventList(self, event_list):
        self.__event_list = event_list
    def setTotalPages(self, total_pages):
        self.__total_pages = total_pages
    def setCurrentPage(self, current_page):
        self.__current_page = current_page
    def setPageNavButtons(self, page_nav_buttons):
        self.__page_nav_buttons = page_nav_buttons

    # Methods
    def updateSurf(self) -> None:
        """Updates the surface with the currently active events.

        To be run each frame.
        """
        self.drawTemplate() # Draws template, overriding previously displayed events.
        displayed_events = self.getDisplayedEvents() # List of events to display.
        font = pygame.font.Font(None, 20)
        surf = self.getSurf()

        # Create font objects for each displayed event, and blit to surf.
        for pos, event in enumerate(displayed_events): 
            text_surf = multiLineSurface(f"> {event}", font, 
                                         pygame.Rect(0, 0, 400, 60), 
                                         (255, 255, 255), (0,0,0))
            text_rect = text_surf.get_rect()
            text_rect.topleft = (15, 50 + pos * 59)      
            surf.blit(text_surf, text_rect)
        return

    def updatePage(self,
                   pygame_events: list[pygame.event.Event], 
                   mouse_pos: tuple[int, int]) -> None:
        """Updates current_page if user presses prev/next page.
        
        To be run each frame.
        """
        # Mouse position relative to the topleft of surface.
        relative_mouse_pos = (mouse_pos[0] - 768, mouse_pos[1] - 444)
        # Checking if prev/next page buttons have been pressed.
        button_outputs = ButtonOutputGetter().getOutputs(self.getPageNavButtons(), 
                                                         pygame_events, relative_mouse_pos)
        if button_outputs:
            button_output = button_outputs[0]
            match button_output:
                case 'prev page':
                    current_page = (self.getCurrentPage() - 1) % self.getTotalPages()
                case 'next page':
                    current_page = (self.getCurrentPage() + 1) % self.getTotalPages()
                case _:
                    raise ValueError(f"Button output '{button_output}' is unknown")
            self.setCurrentPage(current_page)
        return

    def updateEvents(self, events: list[str]) -> None:
        """Updates the list of events that are to be displayed on surface.

        To be run at the end of a turn.
        """
        self.setEventList(events)
        self.setCurrentPage(0)
        self.setTotalPages(max(ceil(len(events) / 4), 1))
        return
    
    def getDisplayedEvents(self) -> list[str]:
        """Returns the list of events to be displayed, depending on current_page."""
        current_page = self.getCurrentPage()
        event_list = self.getEventList()
        num_events = len(event_list) # total number of events
        
        # Compute the list indexes of events that are to be displayed
        event_indexes = [i for i in range((current_page) * 4, (current_page+1) * 4) if i < num_events]

        displayed_events = [event_list[i] for i in event_indexes]
        return displayed_events

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
        page_number_rect.center = (216, 300)

        # Blit template onto surf
        surf = self.getSurf()
        surf.fill((0, 0, 0))
        pygame.draw.rect(surf, (255, 255, 255), (5, 5, 422, 314), 5) # Border
        surf.blit(title_text_surf, title_text_rect)
        surf.blit(page_number_surf, page_number_rect)
        for button in self.getPageNavButtons():
            surf.blit(button.getSurf(), button.getRect())
        self.setSurf(surf)
        return
    
    def createPageNavButtons(self) -> None:
        """Creates the group containing prev page and next page buttons."""
        page_nav_buttons = pygame.sprite.Group()
        page_nav_buttons.add(Button(pygame.Surface((100, 24)), 'prev page', 16, 
                                    (255, 255, 255), 'prev page', (70, 300), ',')) 
        page_nav_buttons.add(Button(pygame.Surface((100, 24)), 'next page', 16, 
                                    (255, 255, 255), 'next page', (362, 300), '.'))
        self.setPageNavButtons(page_nav_buttons)