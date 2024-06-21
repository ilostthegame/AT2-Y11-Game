import pygame
from game_states.game_state import GameState
from pygame.locals import *
from assets import GAME_ASSETS
from sprites.character import Character
from game_states.game_world import GameWorld

class WorldLoad(GameState): # TODO very unfinished
    """
    Class that represents the game state for loading world. Has parent GameState.
    Loads Character and GameWorld objects from save file.
    Loaded when Load Game is selected in TitleScreen

    Attributes:
        save_file ???
    
        (Inherited)
        displayed_sprites: Sprite group that represents all pygame sprites that are to be sent to display
            
    Methods:
        run(self) -> str: Runs all functions to initialise the game world
            To be called each iteration of game loop while state == 'world_init'.
            Returns the next state game is to enter.
        initialiseGameWorld(self, character: Character) -> GameWorld: Creates and returns initial GameWorld object
        initialiseCharacter(self) -> Character: Creates and returns initial character object
    """

    def __init__(self):
        pass

    def run(self) -> str:
        return 'game_world'