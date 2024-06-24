import pygame


class GameEventDisplay(pygame.sprite.Sprite):
    """
    Class representing the 

    Make it so you can press a key to cycle around events if too many. Have designated slots for event text placement, and cycle like mod 4
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