import pygame
from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN

class ButtonOutputGetter:
    """
    Contains method that returns all button outputs in an iteration of game cycle

    Methods:
        getOutputs(self, button_group: pygame.sprite.Group, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> list[str]:
            Finds all buttons in button_group that were activated, either by mouse or connected_key.
            Returns a list containing all button outputs.
    """

    # Methods
    def getOutputs(self, 
                   button_group: pygame.sprite.Group, 
                   pygame_events: list[pygame.event.Event], 
                   mouse_pos: tuple[int, int]) -> list[str]:
        """
        Finds all buttons in button_group that were activated.
        Returns a list containing all button outputs.
        """
        button_outputs = list()

        for event in pygame_events:
            # Handle left mouse button press
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                buttons_pressed = [button for button in button_group if button.getRect().collidepoint(mouse_pos)] # gets all button rects colliding with mouse
                for button in buttons_pressed:
                    button_outputs.append(button.getOutput())

            # Handle keypress
            elif event.type == KEYDOWN:
                for button in button_group:
                    connected_key = button.getConnectedKey()
                    if connected_key: # if connected key exists
                        if event.unicode.lower() == connected_key.lower(): # check if pressed key == connected key
                            button_outputs.append(button.getOutput())
            
            else:
                continue
        
        return button_outputs