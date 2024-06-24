import pygame
from sprites.button import Button
from sprites.game_event_display import GameEventDisplay
from sprites.character_data_display import CharacterDataDisplay
from button_output_getter import ButtonOutputGetter
from typing import Optional
from attack import Attack

class Sidebar(pygame.sprite.Sprite):
    """
    Class that represents the in-game sidebar. Contains:
    - CharacterDataDisplay - Their healthbar/xp bar/level and the level name. Size: 432 x 200
    - Attack buttons - 4 slots available. Size: 432 x 244 space. Each button is 200 x 100
    - GameEventDisplay - Displays game events. Size: 432 x 324

    Attributes:
        surf (pygame.Surface): Entire surface of the sidebar.
        rect (pygame.Rect)
        game_event_display (GameEventDisplay): Sprite that displays game events. Blitted to bottom right.
        character_data_display (CharacterDataDisplay): Displays character healthbar, xp bar, and level.
        character_attack_list (list[Attack]): Represents character's attacks. 
            To be set initially, and updated whenever character's weapon is set in GameWorld.
        attack_button_group (pygame.sprite.Group): Group representing attack buttons on sidebar

    Methods:
        run(self, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> Optional[str]: 
            Updates the sidebar surface and interprets button presses. To be run each iteration
            Returns string when button is pressed: 'attack X' - attack X button was pressed
            
        initialiseAttackButtons(self) -> None: 
            Creates all buttons in attack_button_group 
            To be run whenever character_attack_list is initialised or updated
    """
    # Attributes
    __surf = None
    __game_event_display = None
    __character_data_display = None
    __character_attack_list = None
    __attack_button_group = None

    # Constructor
    def __init__(self, character_attack_list: dict[Attack]):
        self.setSurf(pygame.Surface((432, 768)))
        self.setGameEventDisplay(GameEventDisplay())
        self.setCharacterDataDisplay(CharacterDataDisplay())
        
        # Initialise attack buttons
        self.setAttackButtonGroup(pygame.sprite.Group())
        self.setCharacterAttackList(character_attack_list)
        self.initialiseAttackButtons()

        # Add attack buttons TODO
        
        # TODO add the initial buttons
        

    # Getters
    def getSurf(self):
        return self.__surf
    def getGameEventDisplay(self):
        return self.__game_event_display
    def getCharacterDataDisplay(self):
        return self.__character_data_display
    def getCharacterAttackList(self):
        return self.__character_attack_list
    def getAttackButtonGroup(self):
        return self.__attack_button_group

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setGameEventDisplay(self, game_event_display):
        self.__game_event_display = game_event_display
    def setCharacterDataDisplay(self, character_data_display):
        self.__character_data_display = character_data_display
    def setCharacterAttackList(self, character_attack_list):
        self.__character_attack_list = character_attack_list
    def setAttackButtonGroup(self, attack_button_group):
        self.__attack_button_group = attack_button_group


    # Methods
    def run(self, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> Optional[str]: 
        """
        Updates the sidebar surface and interprets button presses. To be run each iteration
        Returns string when button is pressed: 'attackX' - attack X button was pressed
        """
        # Blits all objects to surface
        surf = self.getSurf()
        surf.fill((255, 255, 255))
        surf.blit(self.getCharacterDataDisplay().getSurf(), (0, 0))
        surf.blit(self.getGameEventDisplay().getSurf(), (0, 444))
        for button in self.getAttackButtonGroup():
             surf.blit(button.getSurf(), button.getRect())
        self.setSurf(surf)

        # Gets button outputs. If they exist, interprets the first one and returns output
        button_outputs = ButtonOutputGetter().getOutputs(self.getAttackButtonGroup(), pygame_events, mouse_pos)
        if button_outputs:
            button_output = button_outputs[0]
            match button_output:
                case 'attack 1':
                    return 'attack 1'
                case 'attack 2':
                    return 'attack 2'
                case 'attack 3':
                    return 'attack 3'
                case 'attack 4':
                    return 'attack 4'
                case _:
                    raise ValueError(f"Button output '{button_output}' is unknown")
                
        return


    def initialiseAttackButtons(self) -> None: 
        """
        Creates all buttons in attack_button_group 
        To be run whenever henever character_attack_list is updated
        """
        attack_button_group = self.getAttackButtonGroup()
        attack_button_group.empty()
        attack_list = self.getCharacterAttackList()
        # Add menu navigation buttons
        
        # Add attack buttons
        button_pos_dict = {1: (108, 261), 2: (324, 261), 3: (108, 383), 4: (324, 383)} # Relates attack number to position of button
        for pos, attack in enumerate(attack_list):
            pos += 1 # 1-based indexing of attacks
            if pos <= 4:
                button = Button(pygame.Surface((180, 100)), attack.getName(), 32, (100, 0, 100), f"attack {pos}", button_pos_dict[pos], str(pos))
                attack_button_group.add(button)
            else:
                raise ValueError("character_attack_list has too many elements (max is 4)")

        self.setAttackButtonGroup(attack_button_group)
