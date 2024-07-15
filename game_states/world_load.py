import pygame
from game_states.game_state import GameState
from pygame.locals import *
from assets import GAME_ASSETS
from sprites.character import Character
from game_states.game_world import GameWorld

class WorldLoad(GameState): # TODO very unfinished
    """Class that represents the game state for loading world.
    
    Loads Character and GameWorld objects from save file.
    Loaded when Load Game is selected in TitleScreen

    Attributes:
        save_file ???
    
        (Inherited)
        main_surf (pygame.Surface): Surface onto which all sprites in the game state are blitted.
            Size: 1200 x 768
    """

    def __init__(self):
        pass

    def run(self) -> str:
        return 'game_world'