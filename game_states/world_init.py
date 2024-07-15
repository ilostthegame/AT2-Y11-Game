import pygame
from game_states.game_state import GameState
from pygame.locals import *
from assets import GAME_ASSETS
from sprites.character import Character
from game_states.game_world import GameWorld

class WorldInit(GameState): # TODO unfinished
    """Class for world initialisation game state.
    
    Initialises Character and GameWorld objects
    Loaded when New Game is selected in TitleScreen

    Attributes:
        (Inherited)
        main_surf (pygame.Surface): Surface onto which all sprites in the game state are blitted.
            Size: 1200 x 768
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
        initial_character = Character('placeholder_image', 'placeholder_name', 'placeholder_weapon_id')