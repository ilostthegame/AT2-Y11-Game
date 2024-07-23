import pygame
from pygame.locals import MOUSEBUTTONDOWN, KEYDOWN
from typing import Optional

class ButtonOutputGetter:
    """Class containing method that gets button outputs in a frame (iteration of game loop)."""

    # Methods
    def getOutputs(self, 
                   button_group: pygame.sprite.Group, 
                   pygame_events: list[pygame.event.Event], 
                   mouse_pos: tuple[int, int]) -> list[Optional[str]]:
        """Returns a list containing all button outputs, for buttons that were activated.
        
        NOTE: It is possible for the user to press multiple buttons in a single frame.
        To account for this in a situation where only a single button press should
        be interpreted, access only the first item of the returned list.
        """
        button_outputs = list()

        for event in pygame_events:
            # Handle left mouse button press
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Get all button outputs the mouse collides with
                buttons_pressed = [button for button in button_group if button.getRect().collidepoint(mouse_pos)] 
                for button in buttons_pressed:
                    button_outputs.append(button.getOutput())

            # Handle keypress
            elif event.type == KEYDOWN:
                for button in button_group:
                    connected_key = button.getConnectedKey()
                    if connected_key: # if connected key exists
                        if event.unicode.lower() == connected_key.lower(): # check if pressed key == connected key
                            button_outputs.append(button.getOutput())
        
        return button_outputs