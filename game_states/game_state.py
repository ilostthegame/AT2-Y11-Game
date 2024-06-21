from abc import ABC, abstractmethod
import pygame

class GameState(ABC):
    """
    Class that represents a general game state.

    Attributes:
        displayed_sprites (pygame.sprite.Group): Sprite group that represents all pygame sprites that are to be sent to display

    Methods:
        run(self) -> str @abstractmethod: Runs all functions associated with game state. To be called each iteration of game loop.
            Returns the next state game is to enter.
    """
    # Attributes
    __displayed_sprites = None

    # Constructor
    def __init__(self):
        self.setDisplayedSprites(pygame.sprite.Group())

    # Getters
    def getDisplayedSprites(self):
        return self.__displayed_sprites

    # Setters
    def setDisplayedSprites(self, displayed_sprites):
        self.__displayed_sprites = displayed_sprites
    
    # Methods
    @abstractmethod
    def run(self):
        """
        Runs all functions associated with game state. To be called each iteration of game loop.
        """
        pass
