import pygame
from sprites.button import Button
from attack import Attack
from button_output_getter import ButtonOutputGetter

class AttackInfoDisplay(pygame.sprite.Sprite):
    """Sidebar component that displays a selected attack's info.

    Supplementary to the AttackButtons sidebar component.
    The instance of this class should be updated with new attack info, 
    and its updateSurf() method run, once an attack button is pressed.
    While GameWorld's internal_state == 'attack_target_selection',
    the isBackPressed() method should be run each frame. If the back button is pressed,
    the selected attack should be deselected, and internal_state reverted to 'main'.

    Attributes:
        surf (pygame.Surface): Surface containing attack info/back button.
            Size: 432 x 244
        back_button_group (pygame.sprite.Group): Group containing the back button.
    """

    # Attributes
    __surf = None
    __back_button_group = None

    # Constructor
    def __init__(self):
        super().__init__()
        self.setSurf(pygame.Surface((432, 244)))
        self.createBackButtonGroup()

    # Getters
    def getSurf(self) -> pygame.Surface:
        return self.__surf
    def getBackButtonGroup(self) -> pygame.sprite.Group:
        return self.__back_button_group

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setBackButtonGroup(self, back_button_group):
        self.__back_button_group = back_button_group

    # Methods
    def updateSurf(self, attack: Attack) -> None:
        """Updates surface with attack information and back button."""
        # Parsing attack info.
        name, power = attack.getName(), attack.getPower()
        accuracy, range = attack.getAccuracy(), attack.getRange()

        # Creating text objects.
        font = pygame.font.Font(None, 32)
        name_text = font.render(f"Using attack: {name}", True, 'black')
        power_text = font.render(f"Power: {power}", True, 'black')
        accuracy_text = font.render(f"Accuracy: {accuracy}", True, 'black')
        range_text = font.render(f"Range: {range}", True, 'black')
        instruction_text = font.render("Click on a highlighted enemy to attack them.", True, 'black')

        # Getting back_button surface and rect.
        back_button = self.getBackButtonGroup().sprites()[0]
        back_button_surf = back_button.getSurf()
        back_button_rect = back_button.getRect()

        # Blitting text objects and back button onto surface.
        # TODO fix the exact positionings. This can actually be in a separate section ig. (like data_display)
        surf = self.getSurf()
        surf.fill((255, 255, 255))
        surf.blit(name_text, (100,20))
        surf.blit(power_text, (30,50))
        surf.blit(accuracy_text, (30,80))
        surf.blit(range_text, (30,110))
        surf.blit(instruction_text, (80,150))
        surf.blit(back_button_surf, back_button_rect)

    def isBackPressed(self, 
                      pygame_events: list[pygame.event.Event],
                      mouse_pos: tuple[int, int]) -> bool:
        """Returns True/False representing if the back button is pressed"""
        # Mouse pos relative to top left of this sprite.
        relative_mouse_pos = (mouse_pos[0] - 768, mouse_pos[1] - 200) 
        button_outputs = ButtonOutputGetter().getOutputs(self.getBackButtonGroup(), 
                                                         pygame_events, relative_mouse_pos)
        if 'Back' in button_outputs:
            return True
        else:
            return False

    def createBackButtonGroup(self) -> None:
        """Creates back button and adds to the back_button_group attribute."""
        back_button_group = pygame.sprite.Group()
        back_button = Button(pygame.Surface((100, 50)), 'Back', 
                             32, 'grey', 'Back', (370, 210), 'B')
        back_button_group.add(back_button)
        self.setBackButtonGroup(back_button_group)