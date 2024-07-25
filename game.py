import pygame
from game_states.title_screen import TitleScreen
from game_states.game_world import GameWorld
from game_states.game_menu import GameMenu
from game_states.world_init import WorldInit
from game_states.world_load import WorldLoad
from game_states.game_over import GameOver
from assets import load_assets, GAME_ASSETS
from pygame.locals import *
from sprites.character import Character
from sprites.healthbar import Healthbar
from typing import Optional

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
        music1 (pygame.mixer.Sound): Happy music.
        music2 (pygame.mixer.Sound): Epic music.

        GameState instances:
        title_screen (TitleScreen): Title screen.
        game_world (GameWorld): Game world - main game.
        game_menu (GameMenu): Game menu
        world_init (WorldInit): World initialiser.
        world_load (WorldLoad): Load from save file.
        game_over (GameOver): Game over screen.
        
    """
    # Attributes
    __screen = None
    __state = None
    __is_running = None
    __clock = None
    __title_screen = None
    __game_world = None
    __game_menu = None
    __world_init = None
    __world_load = None
    __game_over = None
    __music1 = None
    __music2 = None

    # Constructor
    def __init__(self, 
                 state: str, 
                 is_running: bool):
        self.setState(state)
        self.setIsRunning(is_running)
        self.setScreen(pygame.display.set_mode((1200, 768)))
        self.setClock(pygame.time.Clock())
        self.setTitleScreen(TitleScreen())
        self.setGameMenu(GameMenu())
        self.setGameOver(GameOver())
        self.setWorldInit(WorldInit())
        self.setWorldLoad(WorldLoad())
        self.setGameWorld(None)
        self.setMusic1(pygame.mixer.Sound('music/epic song 1.wav'))
        self.setMusic2(pygame.mixer.Sound('music/more epic song.wav'))
        self.getMusic1().play(-1)

    # Getters
    def getScreen(self) -> pygame.Surface:
        return self.__screen
    def getState(self) -> str:
        return self.__state
    def getIsRunning(self) -> bool:
        return self.__is_running
    def getClock(self) -> pygame.time.Clock:
        return self.__clock
    def getTitleScreen(self) -> TitleScreen:
        return self.__title_screen
    def getGameWorld(self) -> Optional[GameWorld]:
        return self.__game_world
    def getGameMenu(self) -> GameMenu:
        return self.__game_menu
    def getWorldInit(self) -> WorldInit:
        return self.__world_init
    def getWorldLoad(self) -> WorldLoad:
        return self.__world_load
    def getGameOver(self) -> GameOver:
        return self.__game_over
    def getMusic1(self) -> pygame.mixer.Sound:
        return self.__music1
    def getMusic2(self) -> pygame.mixer.Sound:
        return self.__music2

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
    def setWorldInit(self, world_init):
        self.__world_init = world_init
    def setWorldLoad(self, world_load):
        self.__world_load = world_load
    def setGameOver(self, game_over):
        self.__game_over = game_over
    def setMusic1(self, music1):
        self.__music1 = music1
    def setMusic2(self, music2):
        self.__music2 = music2

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
                case 'world_init':
                    main_surf = self.runWorldInit(pygame_events, mouse_pos)
                case 'world_load':
                    main_surf = self.runWorldLoad()
                case 'game_world':
                    main_surf = self.runGameWorld(pygame_events, mouse_pos)
                case 'game_menu':
                    main_surf = self.runGameMenu(pygame_events, mouse_pos) 
                case 'game_over':
                    main_surf = self.runGameOver(pygame_events)
                case 'quit':
                    self.setIsRunning(False)
                case _:
                    raise ValueError(f"State ({state}) is unknown")
                
            # Sends main_surf to display.
            screen = self.getScreen()
            screen.fill((255, 255, 255))
            screen.blit(main_surf, (0, 0))
            pygame.display.flip()
            self.getClock().tick(60) # Keeps framerate constant at 60fps.
        pygame.quit() # On loop end.

    def runTitleScreen(self, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> pygame.Surface:
        """
        To run if state == 'title_screen'. Runs TitleScreen class.
        Returns surface to be blitted to screen.
        """
        title_screen = self.getTitleScreen()
        next_state = title_screen.run(pygame_events, mouse_pos)
        self.setState(next_state)
        return title_screen.getMainSurf()
    
    def runWorldInit(self, 
                     pygame_events: list[pygame.event.Event], 
                     mouse_pos: tuple[int, int]) -> pygame.Surface:
        """
        To run if state == 'world_init'. Runs WorldInit class.
        Returns surface to be blitted to screen.

        If GameWorld object is instantiated, sets the class attribute.
        """
        world_init = self.getWorldInit()
        next_state = world_init.run(pygame_events, mouse_pos)
        # Sets the instantiated GameWorld object if it exists.
        if next_state == 'game_world':
            self.setGameWorld(world_init.getInitialisedGameWorld())
            pygame.mixer.stop()
            self.getMusic2().play(-1)
        self.setState(next_state)
        return world_init.getMainSurf()

    def runWorldLoad(self):
        """Loads GameWorld object from file. Immediately enters game_world state.
        
        Sets game_world attribute to be the loaded GameWorld object.
        """
        world_load = self.getWorldLoad()
        next_state = world_load.run()
        # Sets the instantiated GameWorld object.
        self.setGameWorld(world_load.getInitialisedGameWorld())
        pygame.mixer.stop()
        self.getMusic2().play(-1)
        self.setState(next_state)
        return world_load.getMainSurf()

    def runGameWorld(self, 
                     pygame_events: list[pygame.event.Event], 
                     mouse_pos: tuple[int, int]) -> pygame.Surface:
        """
        To run if state == 'game_world'. Runs GameWorld class.
        Returns surface to be blitted to screen.
        """
        game_world = self.getGameWorld()
        next_state = game_world.run(pygame_events, mouse_pos)
        self.setState(next_state)
        return game_world.getMainSurf()

    def runGameMenu(self, 
                    pygame_events: list[pygame.event.Event], 
                    mouse_pos: tuple[int, int]) -> pygame.Surface:
        """Runs game menu."""
        game_menu = self.getGameMenu()
        next_state = game_menu.run(pygame_events, mouse_pos)
        self.setState(next_state)
        # Re-initialises TitleScreen if entered
        if next_state == 'title_screen':
            self.setTitleScreen(TitleScreen())
            pygame.mixer.stop()
            self.getMusic1().play(-1)
        return game_menu.getMainSurf()
    
    def runGameOver(self, 
                    pygame_events: list[pygame.event.Event]) -> pygame.Surface:
        """Run method for GameOver."""
        # Runs game over screen.
        game_over_state = self.getGameOver()
        next_state = game_over_state.run(pygame_events)
        self.setState(next_state)
        return game_over_state.getMainSurf()
