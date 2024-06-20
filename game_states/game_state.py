from abc import ABC, abstractmethod

class GameState(ABC):
    """
    Class that represents a general game state.

    Attributes:
        all_sprites: Sprite group that represents all pygame sprites. To be blitted each iteration

    Methods:
        run(self) @abstractmethod: Runs all functions associated with game state. To be called each iteration of game loop.
    """
    # Attributes
    __all_sprites = None

    # Constructor
    def __init__(self, all_sprites):
        self.setAllSprites(all_sprites)

    # Getters
    def getAllSprites(self):
        return self.__all_sprites

    # Setters
    def setAllSprites(self, all_sprites):
        self.__all_sprites = all_sprites
    
    # Methods
    @abstractmethod
    def run(self):
        """
        Runs all functions associated with game state. To be called each iteration of game loop.
        """
        pass
