import pygame
from pygame.locals import *
from assets import GAME_ASSETS
from sprites.button import Button
# TODO Make an automatic positioning system for buttons, when new game/load game added.

class TitleScreen:
    """
    Class for title screen. Loaded automatically when game starts.

    Attributes:
        screen (pygame.Surface): pygame display Surface.
        button_group (pygame.sprite.Group): Sprite group that contains buttons
        all_sprites (pygame.sprite.Group): Sprite group with all sprites
        is_running (bool): Whether TitleScreen loop is running
        output (str): Output to be returned to main once loop finished. Represents next state game will enter:
            {'start': run GameMenu, 'quit': end game loop}
            
    Methods:
        run(self): runs start menu loop. Returns output
        handleDisplay(self): Blits all buttons onto the screen, and flips display.
        initialiseButtons(self): Creates start, quit buttons and adds them to button_group 
        savedGameExist(self): Evaluates whether a saved gamefile exists. Returns True/False
    """

    # Attributes
    __screen = None 
    __button_group = None 
    __is_running = None
    __output = None

    # Constructor
    def __init__(self, screen: pygame.Surface, button_group: pygame.sprite.Group, is_running: bool):
        self.setScreen(screen)
        self.setButtonGroup(button_group)
        self.setIsRunning(is_running)
        self.initialiseButtons()

    # Getters
    def getScreen(self):
        return self.__screen
    def getButtonGroup(self):
        return self.__button_group
    def getIsRunning(self):
        return self.__is_running
    def getOutput(self):
        return self.__output

    # Setters
    def setScreen(self, screen):
        self.__screen = screen
    def setButtonGroup(self, button_group):
        self.__button_group = button_group
    def setIsRunning(self, is_running):
        self.__is_running = is_running
    def setOutput(self, output):
        self.__output = output


    # Methods
    def run(self) -> str:
        """
        Runs game loop for menu class.
        """
        while self.getIsRunning() == True:
            button_outputs = list() # List of all outputs from activated buttons

            # Pygame event handler
            for event in pygame.event.get(): 
                # Handle game quit
                if event.type == QUIT:
                    self.setOutput('quit')
                    self.setIsRunning(False)

                # Handle mouse left-button click
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    buttons_pressed = [button for button in self.getButtonGroup() if button.getRect().collidepoint(mouse_pos)]
                    for button in buttons_pressed:
                        button_outputs.append(button.getOutput())

                # Handle keypress
                elif event.type == pygame.KEYDOWN:
                    for button in self.getButtonGroup():
                        if event.unicode.lower() == button.getConnectedKey().lower():
                            button_outputs.append(button.getOutput())

            # Interpret button outputs
            for button_output in button_outputs:
                self.setIsRunning(False) # stops TitleScreen loop if button is pressed 
                self.setOutput(button_output) # Note that with multiple buttons pressed, this sets output to be the last output in button_output

            self.handleDisplay()
            
        return self.getOutput() # Returns 'quit' if pygame is to quit, and 'start' if start button pressed.

    def handleDisplay(self) -> None:
        """
        Blits all sprites onto the screen, and flips display.
        """
        self.getScreen().fill((255, 255, 255))
        for button in self.getButtonGroup(): # blits all buttons onto screen
            self.getScreen().blit(button.getSurf(), button.getRect())
        pygame.display.flip()
                
                
    def initialiseButtons(self) -> None:
        """
        Creates title screen buttons and adds them to button_group
        """
        start_button = Button()
        quit_button = Button(pygame.image.load(GAME_ASSETS['exit_button']).convert(), 'quit', (600, 600)),
        self.getButtonGroup().add(start_button) # adds start button to button group
        self.getButtonGroup().add(quit_button) # adds quit button to button group
    
    def savedGameExist(self) -> bool:
        """
        Evaluates whether a saved gamefile exists. Returns True/False
        """
        return True # TODO make functional
