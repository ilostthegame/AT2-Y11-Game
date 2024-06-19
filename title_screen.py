import pygame
from pygame.locals import *
from assets import GAME_ASSETS
from button import Button
# TODO Make an automatic positioning system for buttons, when new game/load game added.

class TitleScreen:
    """
    Class for title screen. Loaded automatically when game starts.

    Attributes:
        screen (pygame.display): Display on which all objects are blitted.
        button_group (pygame.sprite.Group): Group that contains start_button and quit_button
        is_running (bool): Whether TitleScreen loop is running
        output (str): Output to be returned to main once loop finished. Represents next state game will enter:
            ['start' -> run GameMenu, 'quit' -> end game loop]
            
    Methods:
        initialiseButtons(self): Creates start, quit buttons and adds them to button_group 
        handleDisplay(self): Blits all buttons onto the screen, and flips display.
        run(self): runs start menu loop. Returns output

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
    def initialiseButtons(self):
        """
        Creates Start button and Quit Button and adds them to button_group
        TODO Make it new game button, load game button (if save file exists), and quit button
        """
        start_button = Button(pygame.image.load(GAME_ASSETS['start_button']).convert(), 'start', (600, 300)),
        quit_button = Button(pygame.image.load(GAME_ASSETS['exit_button']).convert(), 'quit', (600, 600)),
        self.getButtonGroup().add(start_button) # adds start button to button group
        self.getButtonGroup().add(quit_button) # adds quit button to button group


    def handleDisplay(self):
        """
        Blits all buttons onto the screen, and flips display.
        """
        self.getScreen().fill((255, 255, 255)) # fills screen with white - overrides previous iteration's blits.
        for button in self.getButtonGroup():
            self.getScreen().blit(button.getSurf(), button.getRect()) # blits all buttons onto screen

        pygame.display.flip() # updates pygame display
                

    def run(self):
        """
        Runs game loop for menu class.
        """
        while self.getIsRunning() == True:
            # Pygame event handler
            for event in pygame.event.get(): 
                if event.type == QUIT: # handles quit
                    self.setOutput('quit')
                    self.setIsRunning(False)

                elif event.type == pygame.MOUSEBUTTONDOWN: # Checks if mouse button pressed
                    if event.button == 1: # Checks if it's left button
                        mouse_pos = pygame.mouse.get_pos()
                        buttons_pressed = [button for button in self.getButtonGroup() if button.getRect().collidepoint(mouse_pos)]
                        if len(buttons_pressed) == 1: # a button has been pressed
                            self.setOutput(buttons_pressed[0].getOutput()) # Sets output to the output of the button clicked.
                            self.setIsRunning(False) # Stops menu since button has been pressed
                        # TODO handling for if there are more than one buttons pressed:
                        # TODO make this code better - it's very conditional at the point.

            self.handleDisplay()
            
        return self.getOutput() # Returns 'quit' if pygame is to quit, and 'start' if start button pressed.