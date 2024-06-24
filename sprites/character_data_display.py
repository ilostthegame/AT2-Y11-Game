import pygame

class CharacterDataDisplay(pygame.sprite.Sprite):
    """
    Sprite which displays the following:
    - Character level, healthbar and xp bar with hover capabilities.
    - Current level name, enemy count.

    Attributes: TODO
        surf
    
    Methods: TODO
    """
    # Attributes
    __surf = None

    # Constructor
    def __init__(self):
        self.setSurf(pygame.Surface((432, 200)))
        self.getSurf().fill(('blue'))

    # Getters
    def getSurf(self):
        return self.__surf

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
