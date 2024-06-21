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
                 game_world = 'foobar', # game_world: GameWorld = GameWorld(), 
                 game_menu = 'barfoo'): # game_menu: GameMenu = GameMenu()):
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
            pygame_events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            print(pygame_events)
            print(mouse_pos)

            # Event handler for if game is closed
            for event in pygame_events: 
                if event.type == QUIT:
                    self.setIsRunning(False)
            
            # Runs corresponding function to state
            state = self.getState()
            match state:
                case 'title_screen':
                    displayed_sprites = self.runTitleScreen(pygame_events, mouse_pos)
                case 'game_world':
                    displayed_sprites = self.runGameWorld()
                case 'game_menu':
                    displayed_sprites = self.runGameMenu()
                case 'quit':
                    self.setIsRunning(False)
                case _:
                    raise Exception("State does not exist")
            
            # Sends all sprites to the display.
            screen = self.getScreen()
            screen.fill((255, 255, 255))
            for sprite in displayed_sprites:
                screen.blit(sprite.getSurf(), sprite.getRect())
            pygame.display.flip()

        self.handleCleanup() # Runs cleanup, TODO save game.


    def runTitleScreen(self, pygame_events: dict, mouse_pos: tuple[int, int]) -> pygame.sprite.Group:
        """
        To run if state == 'title_screen'. Runs TitleScreen class.
        Returns sprite group containing all sprites associated with TitleScreen state.
        """
        title_screen = self.getTitleScreen()
        next_state = title_screen.run(pygame_events, mouse_pos)
        displayed_sprites = title_screen.getDisplayedSprites()

        self.setTitleScreen(title_screen)
        self.setState(next_state)
        return displayed_sprites
    

    def runGameWorld(self, pygame_events: dict) -> pygame.sprite.Group:
        """
        To run if state == 'game_world'. Runs GameWorld class.
        Returns sprite group containing all sprites associated with GameWorld state.
        """
        game_world = self.getGameWorld()
        next_state = game_world.run(pygame_events)
        displayed_sprites = game_world.getDisplayedSprites()

        self.setGameWorld(game_world)
        self.setState(next_state)
        return displayed_sprites
        

    def runGameMenu(self) -> pygame.sprite.Group:
        """
        TODO
        """
        pass
    

    def handleCleanup(self):
        """
        To run when game loop is exited. Quits pygame. TODO save system.
        """
        pygame.quit()

