import pygame
from sprites.button import Button
from attack import Attack
from typing import Optional
from button_output_getter import ButtonOutputGetter

class AttackButtons(pygame.sprite.Sprite):
    """Sidebar component that displays and handles the attack buttons.

    Supplementary to the AttackInfoDisplay component.
    While GameWorld's internal_state == 'main', the getAttackSelected() method 
    should be run each frame.
    Once an attack button is pressed, GameWorld's internal_state should become
    'attack_target_selection', and the corresponding attack should be
    selected within the character.

    Attributes:
        surf (pygame.Surface): Surface on which the attack buttons are blitted.
            Size: 432 x 244
        attack_button_group (pygame.sprite.Group): Group of attack buttons:
            Each button returns 'attack X', where X is the corresponding index 
            of the attack in attack_list.
            Each button has size: 180 x 100.
    """

    # Attributes
    __surf = None
    __attack_button_group = None

    # Constructor
    def __init__(self, attack_list: list[Attack]):
        super().__init__()
        self.setSurf(pygame.Surface((432, 244)))
        self.createAttackButtonGroup(attack_list)
        self.createSurf()

    # Getters
    def getSurf(self):
        return self.__surf
    def getAttackButtonGroup(self):
        return self.__attack_button_group

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setAttackButtonGroup(self, attack_button_group):
        self.__attack_button_group = attack_button_group

    # Methods
    def getAttackSelected(self, 
                          pygame_events: list[pygame.event.Event],
                          mouse_pos: tuple[int, int]) -> Optional[int]:
        """Checks for whether an attack button has been pressed.
        
        Returns the pressed button output, or None if no buttons were pressed.
        Button output is a integer representing the attack's index (zero indexed).
        """
        # Mouse pos relative to top left of this sprite.
        relative_mouse_pos = (mouse_pos[0] - 768, mouse_pos[1] - 200)
        # Getting and interpreting button output.
        button_outputs = ButtonOutputGetter().getOutputs(self.getAttackButtonGroup(), 
                                                         pygame_events, relative_mouse_pos)
        # If a button was pressed, return its output.
        if button_outputs:
            button_output = button_outputs[0]
            return button_output
        else:
            return None

    def createAttackButtonGroup(self, attack_list: list[Attack]) -> None:
        """Creates all buttons in attack_button_group."""
        attack_button_group = pygame.sprite.Group()
        # Dictionary that relates attack index to position of button.
        attack_id_to_button_pos = {0: (216, 60), 1: (216, 110), 2: (216, 160), 3: (216, 210)} 
        # Creating buttons for each attack.
        for id, attack in enumerate(attack_list):
            if id <= 3:
                button = Button(pygame.Surface((380, 38)), attack.getName(), 32, (245, 185, 66), 
                                id, attack_id_to_button_pos[id], str(id+1))
                attack_button_group.add(button)
            else:
                raise ValueError(f"Character's attack_list has too many attacks (maximum is 4).")
        self.setAttackButtonGroup(attack_button_group)
    
    def createSurf(self) -> None:
        """Creates and sets the surf attribute.
        
        Uses attack_button_group to draw the buttons onto its surface.
        """
        surf = pygame.Surface((432, 244))
        surf.fill((255, 255, 255))
        # Creating title text surface
        font = pygame.font.Font(None, 32)
        title_text = font.render('Attacks:', True, (0,0,0))
        title_text_rect = title_text.get_rect()
        title_text_rect.center = (216, 20)
        # Blits all objects to surface.
        surf.blit(title_text, title_text_rect)
        for button in self.getAttackButtonGroup():
            surf.blit(button.getSurf(), button.getRect())
        self.setSurf(surf)