from abc import ABC, abstractmethod
import pygame

class GameState(ABC):
    """
    Class that represents a general game state.

    Attributes:
        main_surf (pygame.Surface): Surface onto which all sprites in the game state are blitted.

    Methods:
        run(self) -> str @abstractmethod: 
            Runs all functions associated with game state. To be called each iteration of game loop.
            Returns the next state game is to enter.
    """
    # Attributes
    __main_surf = None

    # Constructor
    def __init__(self):
        self.setMainSurf(pygame.Surface((1200, 800)))

    # Getters
    def getMainSurf(self):
        return self.__surf

    # Setters
    def setMainSurf(self, surf):
        self.__surf = surf
    
    # Methods
    @abstractmethod
    def run(self) -> str:
        """
        Runs all functions associated with game state. To be called each iteration of game loop.
        """
        pass
