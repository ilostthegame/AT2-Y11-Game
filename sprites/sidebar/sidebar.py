import pygame
from sprites.button import Button
from sprites.sidebar.game_event_display import GameEventDisplay
from sprites.sidebar.data_display import DataDisplay
from button_output_getter import ButtonOutputGetter
from typing import Optional, Any
from attack import Attack
from sprites.sidebar.attack_buttons import AttackButtons


class Sidebar(pygame.sprite.Sprite):
    """
    Class that represents the in-game sidebar. Contains three componenets:
    - DataDisplay - Displays character's healthbar/exp bar/level and the level name. Size: 432 x 200
    - AttackButtons - Handles attack buttons. Size: 432 x 244 space. Each button size is 200 x 100
    - GameEventDisplay: Displays game events. Size: 432 x 324

    Attributes:
        surf (pygame.Surface): Entire surface of the sidebar. Size: 432 x 768
        data_display (DataDisplay): Sprite that displays character healthbar, exp bar, and level.
        attack_buttons (AttackButtons): Sprite that displays and handles attack buttons.
        game_event_display (GameEventDisplay): Sprite that displays game events.

    Methods:
        update(self, 
               pygame_events: list[pygame.event.Event], 
               mouse_pos: tuple[int, int],
               health: int,
               max_health: int,
               exp: int,
               req_exp: int,
               level_name: str,
               attack_list: list[Optional[Attack]],
               valid_event_list: list[str],
               invalid_event: str) -> Optional[str]: 

            Updates all components of the sidebar, and blits them onto surf.
            To be run each iteration of GameWorld run().

            Returns 'attack X' if button is pressed: where X is the index of the attack.
    """

    # Attributes
    __surf = None
    __data_display = None
    __attack_buttons = None
    __game_event_display = None
    
    def __init__(self):
        super().__init__()
        self.setSurf(pygame.Surface((432, 768)))
        self.setDataDisplay(DataDisplay())
        self.setAttackButtons(AttackButtons())
        self.setGameEventDisplay(GameEventDisplay())
        
    # Getters
    def getSurf(self):
        return self.__surf
    def getDataDisplay(self):
        return self.__data_display
    def getAttackButtons(self):
        return self.__attack_buttons
    def getGameEventDisplay(self):
        return self.__game_event_display

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setDataDisplay(self, data_display):
        self.__data_display = data_display
    def setAttackButtons(self, attack_buttons):
        self.__attack_buttons = attack_buttons
    def setGameEventDisplay(self, game_event_display):
        self.__game_event_display = game_event_display


    # Methods
    def update(self, 
               pygame_events: list[pygame.event.Event], 
               mouse_pos: tuple[int, int],
               health: int,
               max_health: int,
               exp: int,
               req_exp: int,
               level_name: str,
               attack_list: list[Optional[Attack]],
               valid_event_list: list[str],
               invalid_event: str) -> Optional[str]: 
        """
        Updates all components of the sidebar, and blits them onto surf.
        To be run each iteration of GameWorld run().

        Returns 'attack X' if button is pressed: where X is the index of the attack.
        """

        data_display = self.getDataDisplay()
        attack_buttons = self.getAttackButtons()
        game_event_display = self.getGameEventDisplay()

        # Update components of sidebar
        data_display.update(health, max_health, exp, req_exp, level_name)
        used_attack = attack_buttons.update(pygame_events, mouse_pos, attack_list)
        game_event_display.update(valid_event_list, invalid_event)
        self.setDataDisplay(data_display)
        self.setAttackButtons(attack_buttons)
        self.setGameEventDisplay(game_event_display)

        # Blits all objects to surface
        surf = self.getSurf()
        surf.fill((255, 255, 255))
        surf.blit(self.getDataDisplay().getSurf(), (0, 0))
        surf.blit(self.getAttackButtons().getSurf(), (0, 200))
        surf.blit(self.getGameEventDisplay().getSurf(), (0, 444))
        self.setSurf(surf)
                
        return used_attack



