import pygame
from sprites.button import Button
from sprites.game_event_display import GameEventDisplay
from button_output_getter import ButtonOutputGetter

class Sidebar(pygame.sprite.Sprite):
    """
    Class that represents the in-game sidebar. Contains:
    - Healthbar/experience bar
    - Attack menu
    - Quest menu
    - Info outputter

    Attributes:
        surf (pygame.Surface): Entire surface of the sidebar.
        rect (pygame.Rect)
        

        button_group (pygame.sprite.Group): Group representing all buttons on sidebar
        displayed_sprites (pygame.sprite.Group): Group representing all sprites to be sent to display.

    """


    pass