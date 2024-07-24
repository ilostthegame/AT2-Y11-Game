import pygame
from pygame.locals import *
from game_states.game_state import GameState

class GameOver(GameState):
    """Class that represents the game over game state.
    
    Attributes:
        (Inherited)
        main_surf (pygame.Surface): Surface onto which all sprites in the game state are blitted. 
            Size: 1200 x 768
    """
    
    # Constructor
    def __init__(self):
        super().__init__()
        self.createSurf()

    # Methods
    def run(self, 
            pygame_events: list[pygame.event.Event]) -> str:
        """Main run method for GameOver.

        Deletes all contents in save file.
        Returns 'title_screen' once a mouse button/key is pressed.
        Else, returns 'game_over'.
        """
        # Wait for mouse/key press.
        for event in pygame_events:
            if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                return 'title_screen'
        return 'game_over'

    def createSurf(self) -> None:
        """Creates the game_over screen surface."""
        main_surf = self.getMainSurf()
        font = pygame.font.Font(None, 64)
        main_surf.fill((255, 255, 255))
        main_surf.blit(font.render("GAME OVER", True, (0,0,0)), (500, 200))
        main_surf.blit(font.render("Press any key to exit", True, (0,0,0)), (300, 400))
        return
    

