import pygame
from game_states.game_state import GameState
from sprites.button import Button
from button_output_getter import ButtonOutputGetter

class GameMenu(GameState):
    """Class for game menu game state.
    
    Loaded from pressing ESC in GameWorld.

    Attributes:
        button_group (pygame.sprite.Group): Sprite group that contains buttons:
            Includes 'Resume Game' and 'Save and Exit'

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
    def run(self, 
            pygame_events: list[pygame.event.Event], 
            mouse_pos: tuple[int, int]) -> str: 
        """
        Checks for button presses. Returns the next state game is to enter.
        To be called each iteration of game loop.
        """
        button_outputs = ButtonOutputGetter().getOutputs(self.getButtonGroup(), pygame_events, mouse_pos)
        # If there exists button output(s), interprets the first one in button_outputs.
        if button_outputs:
            button_output = button_outputs[0]
            match button_output:
                case 'resume_game': 
                    return 'game_world'
                case 'exit':
                    return 'title_screen'
                case _:
                    raise Exception(f"Button output {button_output} is unknown")
        return 'game_menu'
            
    def initialiseButtons(self) -> None:
        """Creates buttons and adds them to button_group."""
        button_group = pygame.sprite.Group()
        resume_game_button = Button(pygame.Surface((256, 128)), 'Resume Game', 32,
                                    (200, 100, 0), 'resume_game', (600, 400), '1')
        save_and_exit_button = Button(pygame.Surface((256, 128)), 'Exit', 32,
                                      (200, 100, 0), 'exit', (600, 600), '0')
        button_group.add(resume_game_button, save_and_exit_button) 
        self.setButtonGroup(button_group)
        return
    
    def createSurf(self) -> None:
        """Blits surface (containing text/buttons) onto main_surf."""
        main_surf = self.getMainSurf()
        main_surf.fill((187, 211, 250))
        # Blitting title text.
        font = pygame.font.Font(None, 128)
        title_text = font.render("Menu", True, (0,0,0))
        title_text_rect = title_text.get_rect()
        title_text_rect.center = (600, 100)
        main_surf.blit(title_text, title_text_rect)
        # Blitting buttons.
        for button in self.getButtonGroup():
            main_surf.blit(button.getSurf(), button.getRect())
    
    
