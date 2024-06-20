import pygame
from game_states.title_screen import TitleScreen
from game_states.game_world import GameWorld
from game_states.game_menu import GameMenu
from assets import load_assets, GAME_ASSETS
from pygame.locals import *
from sprites.character import Character
from sprites.healthbar import Healthbar

load_assets()

# Constants
class Game:
    """
    A class representing the game. Contains game main loop. TODO fix up everything such that everything running is in the game main loop
    TODO Give this class attributes such as the TitleScreen, GameWorld classes.

    Attributes:
        screen (pygame.Surface): Display on which all objects are sent.
        state (str): Represents the state the game is in: in ['title_screen', 'game_world', 'game_menu', 'quit']
        is_running (bool): Whether game loop is to continue iteration.
        clock (pygame.time.Clock): Clock to track framerate

        Game States:
        title_screen (TitleScreen)
        game_world (GameWorld)
        game_menu (GameMenu)
        
    Methods:
        run(self): Runs the game main loop
        runTitleScreen(self): If state == 'title_screen', runs title screen
        runGameWorld(self): If state == 'game_world', runs game world
        runGameMenu(self): If state == 'game_menu, runs game menu
        handleCleanup(self): To run when game loop is exited. Quits pygame. TODO save system.
    """

    # Attributes
    __screen = None
    __state = None
    __is_running = None
    __clock = None
    __title_screen = None
    __game_world = None
    __game_menu = None

    # Constructor
    def __init__(self, 
                 state: str, 
                 is_running: bool, 
                 screen: pygame.Surface = pygame.display.set_mode((1200, 800)), 
                 clock: pygame.time.Clock = pygame.time.Clock(), 
                 title_screen: TitleScreen = TitleScreen(), 
                 game_world: GameWorld = GameWorld(), 
                 game_menu: GameMenu = GameMenu()):
        self.setState(state)
        self.setIsRunning(is_running)
        self.setScreen(screen)
        self.setClock(clock)
        self.setTitleScreen(title_screen)
        self.setGameWorld(game_world)
        self.setGameMenu(game_menu)

    # Getters
    def getScreen(self):
        return self.__screen
    def getState(self):
        return self.__state
    def getIsRunning(self):
        return self.__is_running
    def getClock(self):
        return self.__clock
    def getTitleScreen(self):
        return self.__title_screen
    def getGameWorld(self):
        return self.__game_world
    def getGameMenu(self):
        return self.__game_menu

    # Setters
    def setScreen(self, screen):
        self.__screen = screen
    def setState(self, state):
        self.__state = state
    def setIsRunning(self, is_running):
        self.__is_running = is_running
    def setClock(self, clock):
        self.__clock = clock
    def setTitleScreen(self, title_screen):
        self.__title_screen = title_screen
    def setGameWorld(self, game_world):
        self.__game_world = game_world
    def setGameMenu(self, game_menu):
        self.__game_menu = game_menu

    # Methods
    def run(self):
        """
        Runs the game loop
        """
        while self.getIsRunning() == True:
            # Event handler for if game is closed
            for event in pygame.event.get(): 
                if event.type == QUIT:
                    self.setIsRunning(False)
            
            # Runs corresponding function to state
            state = self.getState()
            match state:
                case 'title_screen':
                    self.runTitleScreen()
                case 'game_world':
                    self.runGameWorld()
                case 'game_menu':
                    self.runGameMenu()
                case 'quit':
                    self.setIsRunning(False)
                case _:
                    raise Exception("State does not exist")
                

        self.handleCleanup() # Runs cleanup, TODO save game.


    def runTitleScreen(self):
        """
        Runs if state == 'title_screen'. Runs TitleScreen class.
        Returns 'quit' if quit button hit; Returns 'start' if start button hit.
        """
        title_screen = TitleScreen(self.getScreen(), pygame.sprite.Group(), True) # StartMenu object
        title_screen.run()
        result = title_screen.getOutput()
        if result == 'start':
            self.setState('game_world')
        elif result == 'quit':
            self.setIsRunning(False)
    

    def runGameWorld(self):
        """
        Runs if state == 'game_world'. Runs GameWorld class
        Returns 'quit' if game is quit. Returns
        """
        game_world = GameWorld(self.getScreen(), 'explore', True, 
                               Character(pygame.Surface((64,64)), pygame.image.load(GAME_ASSETS['blue_orb']), # surface and image
                                         'Bob', 25, 25, 100, 100, 'sword', True, 0, 0, 1, 0, list(), 0, # stats
                                         Healthbar(pygame.Surface((64, 16)), 100, 100, 0, 0))) # healthbar object
        result = game_world.run()
        if result == 'title_screen':
            self.setState('game_menu')
        elif result == 'quit':
            self.setIsRunning(False)
        

    def runGameMenu(self):
        """
        TODO
        """
        pass
    

    def handleCleanup(self):
        """
        To run when game loop is exited. Quits pygame. TODO save system.
        """
        pygame.quit()

