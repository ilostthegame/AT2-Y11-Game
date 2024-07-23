import pygame
from sprites.button import Button
from sprites.sidebar.game_event_display import GameEventDisplay
from sprites.sidebar.data_display import DataDisplay
from typing import Optional
from attack import Attack
from sprites.sidebar.attack_buttons import AttackButtons
from sprites.sidebar.attack_info_display import AttackInfoDisplay


class Sidebar(pygame.sprite.Sprite):
    """Class that represents the in-game sidebar. 
    
    Contains three components:
    - DataDisplay - Displays character's healthbar/exp bar/level and the level name. Size: 432 x 200
    - AttackButtons/AttackInfo - Handles attack selection. Size: 432 x 244 space.
    - GameEventDisplay: Displays game events. Size: 432 x 324

    Attributes:
        surf (pygame.Surface): Entire surface of the sidebar. Size: 432 x 768
        data_display (DataDisplay): Sprite that displays level information.
        attack_buttons (AttackButtons): Sprite that displays and handles attack buttons.
        attack_info_display (AttackInfoDisplay): Sprite that displays a selected attack's info.
        game_event_display (GameEventDisplay): Sprite that displays game events.
    """

    # Attributes
    __surf = None
    __data_display = None
    __attack_buttons = None
    __attack_info_display = None
    __game_event_display = None
    
    def __init__(self, character_attack_list: list[Attack]) -> None:
        super().__init__()
        self.setSurf(pygame.Surface((432, 768)))
        self.setDataDisplay(DataDisplay())
        self.setAttackButtons(AttackButtons(character_attack_list))
        self.setAttackInfoDisplay(AttackInfoDisplay())
        self.setGameEventDisplay(GameEventDisplay())
        
    # Getters
    def getSurf(self) -> pygame.Surface:
        return self.__surf
    def getDataDisplay(self) -> DataDisplay:
        return self.__data_display
    def getAttackButtons(self) -> AttackButtons:
        return self.__attack_buttons
    def getGameEventDisplay(self) -> GameEventDisplay:
        return self.__game_event_display
    def getAttackInfoDisplay(self) -> AttackInfoDisplay:
        return self.__attack_info_display

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setDataDisplay(self, data_display):
        self.__data_display = data_display
    def setAttackButtons(self, attack_buttons):
        self.__attack_buttons = attack_buttons
    def setGameEventDisplay(self, game_event_display):
        self.__game_event_display = game_event_display
    def setAttackInfoDisplay(self, attack_info_display):
        self.__attack_info_display = attack_info_display

    # Methods
    def updateSurf(self,
                   game_world_state: str) -> None: 
        """Blits all components of sidebar onto surface.

        If game_world_state == 'main', blits AttackButtons.
        Else if game_world_state == 'attack_target_selection', blits AttackInfoDisplay.
        """
        surf = self.getSurf()
        surf.fill((255, 255, 255))
        surf.blit(self.getDataDisplay().getSurf(), (0, 0))
        if game_world_state == 'main':
            surf.blit(self.getAttackButtons().getSurf(), (0, 200))
        elif game_world_state == 'attack_target_selection':
            surf.blit(self.getAttackInfoDisplay().getSurf(), (0, 200))
        # Updates surface of GameEventDisplay.
        self.getGameEventDisplay().updateSurf()
        surf.blit(self.getGameEventDisplay().getSurf(), (0, 444))
        return
