import pygame
from game_state import GameState
from pygame.locals import *
from assets import GAME_ASSETS
from sprites.button import Button
# TODO Make an automatic positioning system for buttons, when new game/load game added.

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
        initialiseButtons(self): Creates start, quit buttons and adds them to button_group 
        savedGameExist(self): Evaluates whether a saved gamefile exists. Returns True/False
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
            Returns the next state game is to enter.
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

        # Interpret button outputs
        for button_output in button_outputs:
            self.setIsRunning(False) # stops TitleScreen loop if button is pressed 
            self.setOutput(button_output) # Note that with multiple buttons pressed, this sets output to be the last output in button_output

        
        return self.getOutput() # Returns 'quit' if pygame is to quit, and 'start' if start button pressed.
            
                
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
                                 'new game',
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
                                      'load game',
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
