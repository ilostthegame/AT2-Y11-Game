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
        main_surf (pygame.Surface): Surface onto which all sprites in the game state are blitted.
            Size: 1200 x 768
            
    Methods:
        run(self, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> str: 
            Runs all functions to initialise the game world
            To be called each iteration of game loop while state == 'world_init'.
            Returns the next state game is to enter.
        initialiseGameWorld(self, character: Character) -> GameWorld: 
            Creates and returns initial GameWorld object
        initialiseCharacter(self) -> Character: 
            Creates and returns initial character object
    """

    def __init__(self):
        pass

    def run(self) -> str:
        return 'game_world'