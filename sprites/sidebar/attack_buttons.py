import pygame
from sprites.button import Button
from attack import Attack
from typing import Optional
from button_output_getter import ButtonOutputGetter

class AttackButtons(pygame.sprite.Sprite):
    """
    Sidebar component that displays and handles the attack buttons

    Attributes:
        surf (pygame.Surface): Surface on which the attack buttons are blitted.
            Size: 432 x 244
        attack_button_group (pygame.sprite.Group): Group of attack buttons:
            Each button returns 'attack X', where X is the corresponding index of the attack in attack_list.
            Each button has size: 180 x 100.
        attack_list (list[Optional[Attack]]): List of character's attacks.
        
    Methods:
        update(self, 
               pygame_events: list[pygame.event.Event],
               mouse_pos: tuple[int, int],
               attack_list: list[Optional[Attack]]) -> Optional[str]:
            Updates attack buttons, and checks if any are activated.
            Blits attack buttons onto surf.
            Returns a button output if it exists: 'attack X' where X is the index of the attack

            To be run each iteration of GameWorld run().
            
        updateAttackButtons(self, attack_list: list[Optional[Attack]]) -> None:
            Updates all buttons in attack_button_group based on attack_list
    """

    # Attributes
    __surf = None
    __attack_button_group = None
    __attack_list = None

    # Constructor
    def __init__(self):
        super().__init__()
        self.setSurf(pygame.Surface((432, 244)))
        self.setAttackButtonGroup(pygame.sprite.Group())
        self.setAttackList(list())

    # Getters
    def getSurf(self):
        return self.__surf
    def getAttackButtonGroup(self):
        return self.__attack_button_group
    def getAttackList(self):
        return self.__attack_list

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setAttackButtonGroup(self, attack_button_group):
        self.__attack_button_group = attack_button_group
    def setAttackList(self, attack_list):
        self.__attack_list = attack_list

    # Methods
    def update(self, 
               pygame_events: list[pygame.event.Event],
               mouse_pos: tuple[int, int],
               attack_list: list[Optional[Attack]]) -> Optional[str]:
        """
        Updates attack buttons, and checks if any are activated.
        Blits attack buttons onto surf.
        Returns a button output if it exists: 'attack X' where X is the index of the attack

        To be run each iteration of GameWorld run().
        """

        self.updateAttackButtons(attack_list)

        # If button_outputs exist, interprets first one and sets method output
        used_attack = None
        relative_mouse_pos = (mouse_pos[0] - 768, mouse_pos[1] - 200)
        button_outputs = ButtonOutputGetter().getOutputs(self.getAttackButtonGroup(), pygame_events, relative_mouse_pos)
        if button_outputs:
            button_output = button_outputs[0]
            match button_output:
                case 'attack 0':
                    used_attack = 'attack 0'
                case 'attack 1':
                    used_attack = 'attack 1'
                case 'attack 2':
                    used_attack = 'attack 2'
                case 'attack 3':
                    used_attack = 'attack 3'
                case _:
                    raise ValueError(f"Button output '{button_output}' is unknown")
                
        # Blits all buttons to surface
        surf = self.getSurf()
        surf.fill((255, 255, 255))
        for button in self.getAttackButtonGroup():
            surf.blit(button.getSurf(), button.getRect())
        self.setSurf(surf)

        return used_attack

    def updateAttackButtons(self, attack_list: list[Optional[Attack]]) -> None:
        """
        Updates all buttons in attack_button_group based on attack_list
        """

        # Add attack buttons to attack_button_group
        if attack_list != self.getAttackList(): # Checks that attack_list is new
            self.setAttackList(attack_list)
            attack_button_group = pygame.sprite.Group()
            button_pos_dict = {0: (108, 61), 1: (324, 61), 2: (108, 183), 3: (324, 183)} # Relates attack index to position of button

            for pos, attack in enumerate(attack_list):
                if pos <= 3:
                    button = Button(pygame.Surface((180, 100)), attack.getName(), 32, (200, 50, 50), f"attack {pos}", button_pos_dict[pos], str(pos+1))
                    attack_button_group.add(button)
                else:
                    raise ValueError(f"attack_list has too many elements (maximum is 4).\nCurrent attack list: {attack_list}")

            self.setAttackButtonGroup(attack_button_group)
        
        return
