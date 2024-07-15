import pygame
from pygame.locals import *
from typing import Optional

class Button(pygame.sprite.Sprite):
    """Class that represents a GUI button
    
    Attributes:
        surf (pygame.Surface): Surface for the button. Variable size.
        rect (pygame.Rect): Rectangle underlying the button.
        text (str): What the button says on it
        font_size (int): Font size of text on button
        colour (tuple[int, int, int]): Background colour of button
        output (str): What the button should return when activated (clicked/connected_key pressed)
        centre_coords (tuple[int, int]): Coordinates of the centre of button
        connected_key (str): Key that when pressed activates button. May be None.
    """

    # Attributes
    __surf = None
    __rect = None
    __text = None
    __font_size = None
    __colour = None
    __output = None
    __centre_coords = None
    __connected_key = None

    # Constructor
    def __init__(self, 
                surf: pygame.Surface, 
                text: str,
                font_size: int,
                colour: tuple[int, int, int], 
                output: str, 
                centre_coords: tuple[int, int], 
                connected_key: Optional[str] = None):
        super().__init__()
        self.setSurf(surf)
        self.setRect(self.getSurf().get_rect())
        self.setText(text)
        self.setFontSize(font_size)
        self.setColour(colour)
        self.setOutput(output)
        self.setCentreCoords(centre_coords)
        self.setConnectedKey(connected_key)
        self.initialiseButtonSurf()

    # Getters
    def getSurf(self):
        return self.__surf
    def getRect(self):
        return self.__rect
    def getText(self):
        return self.__text
    def getFontSize(self):
        return self.__font_size
    def getColour(self):
        return self.__colour
    def getOutput(self):
        return self.__output
    def getCentreCoords(self):
        return self.__centre_coords
    def getConnectedKey(self):
        return self.__connected_key

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setRect(self, rect):
        self.__rect = rect
    def setText(self, text):
        self.__text = text
    def setFontSize(self, font_size):
        self.__font_size = font_size
    def setColour(self, colour):
        self.__colour = colour
    def setOutput(self, output):
        self.__output = output
    def setCentreCoords(self, centre_coords):
        self.__centre_coords = centre_coords
    def setConnectedKey(self, connected_key):
        self.__connected_key = connected_key


    # Methods
    def initialiseButtonSurf(self):
        """
        Sets position and colour of button, and writes text onto button surface
        """
        button_surf = self.getSurf()
        button_rect = self.getRect()

        # Change position of button surf, and fill it specified colour
        button_rect.center = self.getCentreCoords()
        button_surf.fill((self.getColour()))

        # Create text displayed on button
        text = self.getText()
        if self.getConnectedKey(): # adds "(connected_key)" to text if key exists
            text += f" ({self.getConnectedKey().upper()}) " 
        
        # Create text surface, and blit onto button surface
        pygame.font.init()
        font = pygame.font.Font(None, self.getFontSize())
        text_surf = font.render(text, True, (0,0,0))
        text_rect = text_surf.get_rect()
        button_surf.blit(text_surf, ((button_rect.width - text_rect.width)/2, (button_rect.height - text_rect.height)/2)) # blits text onto button, at centre

        # Re-set surface and button rect
        self.setSurf(button_surf)
        self.setRect(button_rect)
