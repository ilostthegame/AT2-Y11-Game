import pygame
from game_states.game_state import GameState
from assets import GAME_ASSETS
from pygame.locals import *
from sprites.enemy import Enemy
from sprites.npc import Npc
from sprites.character import Character
from level_info import LevelInfo

class GameWorld(GameState):
    """
    Class representing the game world. Has parent GameState.
    TODO fix
    Attributes:
        output (str): Output to be returned to main once loop finished. Represents next state game will enter:
            ['startmenu' -> exit and run StartMenu, 'quit' -> end game loop]
        
        character (Character): Character object controlled by player
        level_info (LevelInfo): Initialises and tracks tile and entity information in a level.
        foo (Foo): Gui interface with action selections

        (Inherited)
        displayed_sprites: Sprite group that represents all pygame sprites that are to be sent to display

    Methods: TODO
        run(self) -> str: Runs all functions associated with GameWorld. To be called each iteration of game loop.
            Returns the next state game is to enter.

        handleWorld(self): Handles state where character is in world
        handleMenu(self, menu_type): 
        handleDisplay(self)

    """

    # Attributes
    __screen = None
    __state = None
    __is_running = None
    __character = None
    __current_level = None
    __output = None
    __displayed_sprites = None
    __tile_group = None
    __npc_group = None
    __enemy_group = None
    
    # Constructor
    def __init__(self, 
                 screen: pygame.Surface, 
                 state: str, 
                 is_running: bool, 
                 character: Character, 
                 current_level: int, 
                 output: str = 'quit', 
                 displayed_sprites = pygame.sprite.Group, 
                 tile_group = pygame.sprite.Group, 
                 npc_group = pygame.sprite.Group, 
                 enemy_group = pygame.sprite.Group):
        self.setScreen(screen)
        self.setState(state)
        self.setIsRunning(is_running)
        self.setCharacter(character)
        self.setCurrentLevel(current_level)
        self.setOutput(output)
        self.setDisplayedSprites(displayed_sprites)
        self.setTileGroup(tile_group)
        self.setNpcGroup(npc_group)
        self.setEnemyGroup(enemy_group)


    # Getters
    def getScreen(self):
        return self.__screen
    def getState(self):
        return self.__state
    def getIsRunning(self):
        return self.__is_running
    def getCharacter(self):
        return self.__character
    def getCurrentLevel(self):
        return self.__current_level
    def getOutput(self):
        return self.__output
    def getDisplayedSprites(self):
        return self.__displayed_sprites
    def getTileGroup(self):
        return self.__tile_group
    def getNpcGroup(self):
        return self.__npc_group
    def getEnemyGroup(self):
        return self.__enemy_group

    # Setters
    def setScreen(self, screen):
        self.__screen = screen
    def setState(self, state):
        self.__state = state
    def setIsRunning(self, is_running):
        self.__is_running = is_running
    def setCharacter(self, character):
        self.__character = character
    def setCurrentLevel(self, current_level):
        self.__current_level = current_level
    def setOutput(self, output):
        self.__output = output
    def setDisplayedSprites(self, displayed_sprites):
        self.__displayed_sprites = displayed_sprites
    def setTileGroup(self, tile_group):
        self.__tile_group = tile_group
    def setNpcGroup(self, npc_group):
        self.__npc_group = npc_group
    def setEnemyGroup(self, enemy_group):
        self.__enemy_group = enemy_group

    def handleWorld(self):
        pass
    
    def handleActionMenu(self):
        pass
    
    def handleNarrator(self, text):
        pass

    def handleInteraction(self, text, npc):
        pass

    def interpretButton(self):
        pass


    # Methods
    def run(self):
        """
        Runs the game world loop.
        Game world includes all stuff happening ingame after start button has been pressed.
        """
        while self.getIsRunning():
            while self.getIsRunning() == True:
            # Event handler for QUIT
                for event in pygame.event.get(): 
                    if event.type == QUIT:
                        self.setIsRunning(False)
                self.handleWorld()
            
        return self.getOutput()

        # TODO use pygame.event == KEYDOWN to do stuff with one movement at a time.