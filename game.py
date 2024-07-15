import pygame
from game_states.title_screen import TitleScreen
from game_states.game_world import GameWorld
from game_states.game_menu import GameMenu
from game_states.world_init import WorldInit
from game_states.world_load import WorldLoad
from assets import load_assets, GAME_ASSETS
from pygame.locals import *
from sprites.character import Character
from sprites.healthbar import Healthbar
import random

load_assets()

# Constants
class Game:
    """A class representing the game. Contains game main loop.

    Attributes:
        screen (pygame.Surface): Display on which all objects are sent. Size: 1200 x 768
        state (str): Represents the state the game is in: 
            in ['title_screen', 'world_init', 'world_load', 'game_world', 'game_menu', 'quit']
        is_running (bool): Whether game loop is to continue iteration.
        clock (pygame.time.Clock): Clock to track framerate
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
                 is_running: bool):
        self.setState(state)
        self.setIsRunning(is_running)
        self.setScreen(pygame.display.set_mode((1200, 768)))
        self.setClock(pygame.time.Clock())
        self.setTitleScreen(TitleScreen())
        self.setGameMenu('placeholder')

        # Temporary GameWorld initialisation. Can edit character's stuff here for testing.
        character = Character(pygame.image.load(GAME_ASSETS['blue_orb']).convert_alpha(), 'Bob', 'Sw')
        game_world = GameWorld('Dining Hall', character)
        game_world.initialiseLevel()
        self.setGameWorld(game_world)

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
    def runMainLoop(self) -> None:
        """
        Runs the main game loop
        """
        while self.getIsRunning() == True:
            pygame_events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()

            # Event handler for if game is closed
            for event in pygame_events: 
                if event.type == QUIT:
                    self.setIsRunning(False)
            
            # Runs corresponding function to state
            state = self.getState()
            match state:
                case 'title_screen':
                    main_surf = self.runTitleScreen(pygame_events, mouse_pos)
                case 'world_init': # TODO fix up worldinit
                    main_surf = self.runGameWorld(pygame_events, mouse_pos) # self.runWorldInit()
                case 'world_load':
                    main_surf = self.runWorldLoad()
                case 'game_world':
                    main_surf = self.runGameWorld(pygame_events, mouse_pos)
                case 'game_menu':
                    main_surf = self.runGameMenu() 
                case 'quit':
                    self.setIsRunning(False)
                case _:
                    raise ValueError(f"State ({state}) is unknown")
            
            # Sends all sprites to the display.
            screen = self.getScreen()
            screen.fill((255, 255, 255))
            screen.blit(main_surf, (0, 0))
            pygame.display.flip()

            self.getClock().tick(20)

        self.handleCleanup() # Runs cleanup, TODO save game.


    def runTitleScreen(self, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> pygame.sprite.Group:
        """
        To run if state == 'title_screen'. Runs TitleScreen class.
        Returns sprite group containing all sprites associated with TitleScreen state.
        """
        title_screen = self.getTitleScreen()
        next_state = title_screen.run(pygame_events, mouse_pos)
        main_surf = title_screen.getMainSurf()

        self.setTitleScreen(title_screen)
        self.setState(next_state)
        return main_surf
    
    def runWorldInit(self):
        pass

    def runWorldLoad(self):
        pass

    def runGameWorld(self, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> pygame.sprite.Group:
        """
        To run if state == 'game_world'. Runs GameWorld class.
        Returns sprite group containing all sprites associated with GameWorld state.
        """
        game_world = self.getGameWorld()
        
        next_state = game_world.run(pygame_events, mouse_pos)
        main_surf = game_world.getMainSurf()

        self.setGameWorld(game_world)
        self.setState(next_state) # no problems here I think
        return main_surf
        

    def runGameMenu(self) -> pygame.sprite.Group:
        """
        TODO
        """
        pass
    

    def handleCleanup(self) -> None:
        """To run when game loop is exited. Quits pygame. TODO save system."""
        pygame.quit()

