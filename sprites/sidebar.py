import pygame
from sprites.button import Button
from sprites.game_event_display import GameEventDisplay
from button_output_getter import ButtonOutputGetter

class Sidebar(pygame.sprite.Sprite):
    """
    Class that represents the in-game sidebar. Contains:
    - Character data - 
    - Attack menu
    - Quest menu
    - Info outputter

    Attributes:
        surf (pygame.Surface): Entire surface of the sidebar.
        rect (pygame.Rect)
        game_event_display (GameEventDisplay): Sprite that displays game events. Blitted to bottom right.
        character_data_display (CharacterData TODO is a Sprite): Displays character healthbar, xp bar, and level.

        character_attacks (dict[Attack]): Represents all attacks player has
        character_quests (dict[Quest]) Represents all quests player has

        current_button_group (pygame.sprite.Group): Group representing all buttons on sidebar
        current_menu (str): Represents which menu the player is on.
            in [main, attack_menu, quest_menu]
        button_dict (dict[str, Button]): Relates button names to their objects, for conciseness.

    Methods:
        run(self) -> Optional[str]: Updates the sidebar surface. Returns any important outputs: attack usage or game menu. To be run each iteration
        interpretButtonOutput(self, button_output) -> Optional[str]: Interprets button output, changes current_menu, returns any important outputs.
        updateButtons(self) -> None: Updates which buttons are in current_button_group. To be run when a button is pressed.
        initialiseButtonDict(self) -> None: Inputs all button objects into button_dict. 
            To be run initially and whenever character_attacks or character_quests updated.
    """


    pass