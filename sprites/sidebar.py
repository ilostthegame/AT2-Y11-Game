import pygame
from sprites.button import Button
from sprites.game_event_display import GameEventDisplay
from sprites.character_data_display import CharacterDataDisplay
from button_output_getter import ButtonOutputGetter
from typing import Optional
from attack import Attack
from quest import Quest

class Sidebar(pygame.sprite.Sprite):
    """
    Class that represents the in-game sidebar. Contains:
    - Character data - Their healthbar/xp bar/level
    - Attack and Quest menus - note there exist 4 slots for each. 
    - GameEventDisplay

    Attributes:
        surf (pygame.Surface): Entire surface of the sidebar.
        rect (pygame.Rect)
        game_event_display (GameEventDisplay): Sprite that displays game events. Blitted to bottom right.
        character_data_display (CharacterData TODO is a Sprite): Displays character healthbar, xp bar, and level.
        character_attacks (dict[Attack]): Represents all attacks player has.
        character_quests (dict[Quest]) Represents all quests player has.
        current_button_group (pygame.sprite.Group): Group representing all buttons on sidebar
        current_menu (str): Represents which menu the player is on. In [main, attack_menu, quest_menu]
        button_dict (dict[str, Button]): Relates button names to their objects, for conciseness.

    Methods:
        run(self, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> Optional[str]: 
            Updates the sidebar surface. To be run each iteration
            Returns any outputs received from interpretButtonOutput().
        interpretButtonOutput(self, button_output: str) -> Optional[str]: 
            Interprets button output, changes current_menu accordingly. 
            Returns any important outputs: if an attack is used, or if game menu is accessed. 
        updateButtons(self) -> None: 
            Updates which buttons are in current_button_group. To be run when a button is pressed.
        initialiseButtonDict(self) -> None: 
            Inputs all button objects into button_dict. 
            To be run in constructor, and whenever character_attacks or character_quests are updated.
    """
    # Attributes
    __surf = None
    __rect = None
    __game_event_display = None
    __character_data_display = None
    __character_attacks = None
    __character_quests = None
    __current_button_group = None
    __current_menu = None
    __button_dict = None

    # Constructor
    def __init__(self, 
                 character_attacks: dict[Attack], 
                 character_quests: dict[Quest]): #
        self.setSurf(pygame.Surface((496, 800)))
        self.setRect((704, 0, 496, 800)) # position is top-right of screen.
        self.setGameEventDisplay(GameEventDisplay())
        self.setCharacterDataDisplay(CharacterDataDisplay())
        self.setCharacterAttacks(character_attacks)
        self.setCharacterQuests(character_quests)

        # Initialise button dictionary
        self.setButtonDict(dict())
        self.initialiseButtonDict()

        # Add initial buttons: Attack menu, Quest menu, Game menu
        self.setCurrentMenu('main')
        self.setCurrentButtonGroup(pygame.sprite.Group())
        # TODO add the initial buttons
        
        

    # Getters
    def getSurf(self):
        return self.__surf
    def getRect(self):
        return self.__rect
    def getGameEventDisplay(self):
        return self.__game_event_display
    def getCharacterDataDisplay(self):
        return self.__character_data_display
    def getCharacterAttacks(self):
        return self.__character_attacks
    def getCharacterQuests(self):
        return self.__character_quests
    def getCurrentButtonGroup(self):
        return self.__current_button_group
    def getCurrentMenu(self):
        return self.__current_menu
    def getButtonDict(self):
        return self.__button_dict

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setRect(self, rect):
        self.__rect = rect
    def setGameEventDisplay(self, game_event_display):
        self.__game_event_display = game_event_display
    def setCharacterDataDisplay(self, character_data_display):
        self.__character_data_display = character_data_display
    def setCharacterAttacks(self, character_attacks):
        self.__character_attacks = character_attacks
    def setCharacterQuests(self, character_quests):
        self.__character_quests = character_quests
    def setCurrentButtonGroup(self, current_button_group):
        self.__current_button_group = current_button_group
    def setCurrentMenu(self, current_menu):
        self.__current_menu = current_menu
    def setButtonDict(self, button_dict):
        self.__button_dict = button_dict

    # Methods
    def run(self, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> Optional[str]: 
        """
        Updates the sidebar surface. To be run each iteration
        Returns any outputs received from interpretButtonOutput().
        """
        # Blits all objects to surface
        surf = self.getSurf()
        surf.fill((255, 255, 255))
        surf.blit(self.getCharacterDataDisplay().getSurf(), (0, 0))
        surf.blit(self.getGameEventDisplay().getSurf(), (500, 0))
        for button in self.getCurrentButtonGroup():
            surf.blit(button.getSurf(), button.getRect())
        self.setSurf(surf)

        button_outputs = ButtonOutputGetter().getOutputs(self.getButtonGroup(), pygame_events, mouse_pos)
        
        # If there exists button output(s), interprets the first one in button_outputs.
        if button_outputs:
            button_output = button_outputs[0]
            output = self.interpretButtonOutput(button_output) # may be None, or a string representing action caused by button.

        return output


    def interpretButtonOutput(self, button_output: str) -> Optional[str]: 
        """
        Interprets button output, changes current_menu accordingly.
        Returns any important outputs: if an attack is used, or if game menu is accessed. 
        """
        match button_output:
            case 'new_game': # TODO change
                return 'world_init'
            case 'load_game':
                return 'world_load'
            case 'quit_game':
                return 'quit'
            case _:
                raise Exception("Unknown button output")

    def updateButtons(self) -> None: 
        """
        Updates which buttons are in current_button_group. To be run when a button is pressed.
        """
        pass


    def initialiseButtonDict(self) -> None: 
        """
        Inputs all button objects into button_dict. 
        To be run in constructor, and whenever character_attacks or character_quests are updated.
        """
        pass