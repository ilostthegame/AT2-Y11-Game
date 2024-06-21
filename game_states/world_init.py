import pygame
from game_states.game_state import GameState
from pygame.locals import *
from assets import GAME_ASSETS
from sprites.character import Character
from game_states.game_world import GameWorld

class WorldInit(GameState):
    """
    Class for world initialisation game state. Has parent GameState.
    Initialises Character and GameWorld objects
    Loaded when New Game is selected in TitleScreen

    Attributes:
        (Inherited)
        displayed_sprites: Sprite group that represents all pygame sprites that are to be sent to display
            
    Methods:
        run(self) -> str: Runs all functions to initialise the game world
            To be called each iteration of game loop while state == 'world_init'.
            Returns the next state game is to enter.
        initialiseGameWorld(self, character: Character) -> GameWorld: Creates and returns initial GameWorld object
        initialiseCharacter(self) -> Character: Creates and returns initial character object

    # TODO turn this into an actual class where you can select stuff actually.
    """

    # Methods

    def run(self) -> str:
        """
        Runs all functions to initialise the game world
        To be called each iteration of game loop while state == 'world_init'.
        Returns the next state game is to enter.
        """
        pass

    def initialiseGameWorld(self, character: Character) -> GameWorld:
        """
        Creates and returns initial GameWorld object
        """

    def initialiseCharacter(self) -> Character:
        """
        Creates and returns initial character object
        """
        init_character = Character(
            'blue_orb',
            25,
            25,
            100,
            100,

        )