import pygame
from game_states.game_state import GameState
from pygame.locals import *
from assets import GAME_ASSETS
from sprites.character import Character
from game_states.game_world import GameWorld

class WorldInit(GameState): # TODO unfinished
    """
    Class for world initialisation game state. Has parent GameState.
    Initialises Character and GameWorld objects
    Loaded when New Game is selected in TitleScreen

    Attributes:
        (Inherited)
        main_surf (pygame.Surface): Surface onto which all sprites in the game state are blitted.

    Methods:
        run(self, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> str: 
            Runs all functions to initialise the game world
            To be called each iteration of game loop while state == 'world_init'.
            Returns the next state game is to enter.
        initialiseGameWorld(self, character: Character) -> GameWorld: 
            Creates and returns initial GameWorld object
        initialiseCharacter(self) -> Character: 
            Creates and returns initial character object

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
        pass

    def initialiseCharacter(self) -> Character:
        """
        Creates and returns initial character object
        """
        pass
        # init_character = Character(
        #     'blue_orb',
        #     25,
        #     25,
        #     100,
        #     100,

        # )