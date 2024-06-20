import pygame
from game_state import GameState
from pygame.locals import *
from assets import GAME_ASSETS
from sprites.button import Button

class TitleScreen(GameState):
    """
    Class for title screen. Loaded automatically when game starts.

    Attributes:
        button_group (pygame.sprite.Group): Sprite group that contains buttons

        (Inherited)
        all_sprites: Sprite group that represents all pygame sprites. To be blitted each iteration
            
    Methods:
        run(self) -> str: Runs all functions associated with TitleScreen. To be called each iteration of game loop.
            Returns the next state game is to enter.
        initialiseButtons(self) -> None: Creates start, quit buttons and adds them to button_group 
        savedGameExist(self) -> bool: Evaluates whether a saved gamefile exists. Returns True/False
    """

    # Attributes
    __button_group = None 

    # Constructor
    def __init__(self, button_group: pygame.sprite.Group):
        super().__init__()
        self.setButtonGroup(button_group)
        self.initialiseButtons()

    # Getters
    def getButtonGroup(self):
        return self.__button_group

    # Setters
    def setButtonGroup(self, button_group):
        self.__button_group = button_group

    # Methods
    def run(self, pygame_events, mouse_pos) -> str: 
        """
        Runs all functions associated with TitleScreen. To be called each iteration of game loop.
        Returns the next state game is to enter: in [title_screen, game_world, exit]
        """
        button_outputs = list() # List of all outputs from activated buttons

        # Event handler
        for event in pygame_events:
            # Handle mouse left-button click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                buttons_pressed = [button for button in self.getButtonGroup() if button.getRect().collidepoint(mouse_pos)]
                for button in buttons_pressed:
                    button_outputs.append(button.getOutput())

            # Handle keypress
            elif event.type == pygame.KEYDOWN:
                for button in self.getButtonGroup():
                    if event.unicode.lower() == button.getConnectedKey().lower():
                        button_outputs.append(button.getOutput())

            else:
                continue
            
        # If there exists button output(s), interprets the first one in button_outputs.
        if button_outputs:
            foo = button_outputs[0] # TODO fix name, and make the new_game, load_game cases activate some initialisation function. Perhaps within game_world
            match foo:
                case 'new_game': 
                    return 'game_world'
                case 'load_game':
                    return 'game_world'
                case 'exit':
                    return 'exit'
                case _:
                    raise Exception("Unknown button output")

        return 'title_screen' # Re-enter title screen
            
                
    def initialiseButtons(self) -> None:
        """
        Creates title screen buttons and adds them to button_group, and all_sprites
        """
        button_group = pygame.sprite.Group()
        all_sprites_group = pygame.sprite.Group()
        new_game_button = Button(pygame.Surface((256, 128)), 
                                 'New Game',
                                 32,
                                 (200, 100, 0),
                                 'new_game',
                                 (600, 200))
        exit_button = Button(pygame.Surface((256, 128)), 
                                 'Exit',
                                 32,
                                 (200, 100, 0),
                                 'exit',
                                 (600, 600),
                                 'P')
        button_group.add(new_game_button, exit_button) # adds new game and exit buttons

        if self.savedGameExist(): # adds load game button if it exists
            load_game_button = Button(pygame.Surface((256, 128)), 
                                      'Load Game',
                                      32,
                                      (200, 200, 200),
                                      'load_game',
                                      (400, 200))
            button_group.add(load_game_button)
        
        all_sprites_group.add(button_group)
        self.setButtonGroup(button_group)
        self.setAllSprites(all_sprites_group)
        
    
    def savedGameExist(self) -> bool:
        """
        Evaluates whether a saved gamefile exists. Returns True/False
        """
        return True # TODO make functional once savedgame exists
