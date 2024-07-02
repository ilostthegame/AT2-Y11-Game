import pygame
from game_states.game_state import GameState
from pygame.locals import *
from assets import GAME_ASSETS
from sprites.button import Button
from button_output_getter import ButtonOutputGetter

class TitleScreen(GameState):
    """
    Class for title screen game state. Has parent GameState.
    Loaded when game is initialised, and from 'save_and_exit' from GameMenu

    Attributes:
        button_group (pygame.sprite.Group): Sprite group that contains buttons:
            Includes new_game, quit and load_game

        (Inherited)
        main_surf (pygame.Surface): Surface onto which all sprites in the game state are blitted.
            Size: 1200 x 768

    Methods:
        run(self, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> str:
            Runs all functions associated with TitleScreen. To be called each iteration of game loop.
            Returns the next state game is to enter.
        initialiseButtons(self) -> None:
            Creates new_game, quit and load_game buttons and adds them to button_group
        savedGameExist(self) -> bool:
            Evaluates whether a saved gamefile exists. Returns True/False
    """

    # Attributes
    __button_group = None 

    # Constructor
    def __init__(self):
        super().__init__()
        self.setButtonGroup(pygame.sprite.Group())
        self.initialiseButtons()

    # Getters
    def getButtonGroup(self):
        return self.__button_group

    # Setters
    def setButtonGroup(self, button_group):
        self.__button_group = button_group

    # Methods
    def run(self, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> str: 
        """
        Runs all functions associated with TitleScreen. To be called each iteration of game loop.
        Returns the next state game is to enter: in [title_screen, game_world, exit]
        """
        
        button_outputs = ButtonOutputGetter().getOutputs(self.getButtonGroup(), pygame_events, mouse_pos) # Gets all button outputs
        next_state = 'title_screen'
        
        # If there exists button output(s), interprets the first one in button_outputs.
        if button_outputs:
            button_output = button_outputs[0]
            match button_output:
                case 'new_game': 
                    next_state = 'world_init'
                case 'load_game':
                    next_state = 'world_load'
                case 'quit':
                    next_state = 'quit'
                case _:
                    raise Exception(f"Button output {button_output} is unknown")
                
        # Blits all buttons to surface
        main_surf = self.getMainSurf()
        main_surf.fill((187, 211, 250))
        for button in self.getButtonGroup():
            main_surf.blit(button.getSurf(), button.getRect())
        self.setMainSurf(main_surf)

        return next_state
            
                
    def initialiseButtons(self) -> None:
        """
        Creates title screen buttons and adds them to button_group.
        """
        button_group = self.getButtonGroup()
        new_game_button = Button(pygame.Surface((256, 128)), 
                                 'New Game',
                                 32,
                                 (200, 100, 0),
                                 'new_game',
                                 (600, 200),
                                 '1')
        quit_button = Button(pygame.Surface((256, 128)), 
                                 'Quit',
                                 32,
                                 (200, 100, 0),
                                 'quit',
                                 (600, 600),
                                 '0')
        button_group.add(new_game_button, quit_button) 
        if self.savedGameExist(): # Load Game only if saved game exists already.
            load_game_button = Button(pygame.Surface((256, 128)), 
                                      'Load Game',
                                      32,
                                      (200, 200, 200),
                                      'load_game',
                                      (600, 400),
                                      '2')
            button_group.add(load_game_button)
        self.setButtonGroup(button_group)
        return
        
    
    def savedGameExist(self) -> bool:
        """
        Evaluates whether a saved gamefile exists. Returns True/False
        """
        return True # TODO make functional once savedgame exists
