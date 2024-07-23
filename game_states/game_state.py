from abc import ABC, abstractmethod
import pygame

class GameState(ABC):
    """Abstract class that represents a general game state.

    Attributes:
        main_surf (pygame.Surface): Surface onto which all sprites in the game state are blitted. 
            Size: 1200 x 768
    """

    # Attributes
    __main_surf = None

    # Constructor
    def __init__(self):
        self.setMainSurf(pygame.Surface((1200, 768)))

    # Getters
    def getMainSurf(self) -> pygame.Surface:
        return self.__main_surf

    # Setters
    def setMainSurf(self, main_surf):
        self.__main_surf = main_surf
    
    # Methods
    @abstractmethod
    def run(self) -> str:
        """
        Runs all functions associated with game state. To be called each iteration of game loop.
        """
        pass
