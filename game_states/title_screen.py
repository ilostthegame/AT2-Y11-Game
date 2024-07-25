import pygame
from game_states.game_state import GameState
from pygame.locals import *
from assets import GAME_ASSETS
from sprites.button import Button
from button_output_getter import ButtonOutputGetter

class TitleScreen(GameState):
    """Class for title screen game state.
    
    Loaded when game is initialised, and from selecting Save and Exit from GameMenu.

    Attributes:
        button_group (pygame.sprite.Group): Sprite group that contains buttons:
            Includes new_game, quit and load_game
        confirm_button_group (pygame.sprite.Group): Sprite group that contains
            confirmation button.

        (Inherited)
        main_surf (pygame.Surface): Surface onto which all sprites in the game state are blitted.
            Size: 1200 x 768
    """

    # Attributes
    __button_group = None 

    # Constructor
    def __init__(self):
        super().__init__()
        self.initialiseButtons()
        self.createSurf()

    # Getters
    def getButtonGroup(self) -> pygame.sprite.Group:
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
        # If there exists button output(s), interprets the first one in button_outputs.
        if button_outputs:
            button_output = button_outputs[0]
            match button_output:
                case 'new_game': 
                    # Checking for confirmation if a saved game exists.
                    if self.savedGameExist():
                        self.createConfirmationButton()
                    else:
                        return 'world_init'
                case 'confirm':
                    return 'world_init'
                case 'load_game':
                    return 'world_load'
                case 'quit':
                    return 'quit'
                case _:
                    raise Exception(f"Button output {button_output} is unknown")
                
        return 'title_screen'
            
    def initialiseButtons(self) -> None:
        """Creates title screen buttons and adds them to button groups."""
        button_group = pygame.sprite.Group()
        new_game_button = Button(pygame.Surface((256, 128)), 'New Game', 32,
                                 (200, 100, 0), 'new_game', (600, 250), '1')
        quit_button = Button(pygame.Surface((256, 128)), 'Quit', 32,
                            (200, 100, 0), 'quit', (600, 600), '0')
        button_group.add(new_game_button, quit_button) 
        if self.savedGameExist(): # Load Game only if saved game exists already.
            load_game_button = Button(pygame.Surface((256, 128)), 'Load Game', 32,
                                     (200, 200, 200), 'load_game', (600, 425), '2')
            button_group.add(load_game_button)
        self.setButtonGroup(button_group)
        return
    
    def createConfirmationButton(self) -> None:
        """Creates a confirmation button if user presses New Game
        but has an existing save file.

        Checks if such a button already exists, and if not, adds to button group.
        """
        button_group = self.getButtonGroup()
        button_outputs = [button.getOutput() for button in button_group]
        if 'confirm' not in button_outputs:
            button_group.add(Button(pygame.Surface((256, 128)), 'Are you sure?', 32,
                                    (255, 20, 20), 'confirm', (900, 250)))
        self.createSurf()
    
    def createSurf(self) -> None:
        """Blits surface (containing text/buttons) onto main_surf."""
        main_surf = self.getMainSurf()
        main_surf.fill((187, 211, 250))
        # Blitting title text.
        font = pygame.font.Font(None, 128)
        title_text = font.render("King's Quest", True, (0,0,0))
        title_text_rect = title_text.get_rect()
        title_text_rect.center = (600, 100)
        main_surf.blit(title_text, title_text_rect)
        # Blitting buttons.
        for button in self.getButtonGroup():
            main_surf.blit(button.getSurf(), button.getRect())
    
    def savedGameExist(self) -> bool:
        """Returns True/False for whether a saved gamefile exists."""
        with open('gameinfostorage/save_info.txt', 'r') as file:
            if file.readlines() == []:
                return False
            else:
                return True

