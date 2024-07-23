import pygame
from ..character import Character

class DataDisplay(pygame.sprite.Sprite):
    """Sidebar component that displays character and level information.

    Displays the following:
        - Character level.
        - Exp / req exp.
        - Health / max health.
        - Level name.
        - Number of remaiining enemies.

    Attributes:
        surf (pygame.Surface): Surface to which data is displayed.
            Size: 432 x 200
    """

    # Attributes
    __surf = None

    # Constructor
    def __init__(self):
        self.setSurf(pygame.Surface((432, 200)))

    # Getters
    def getSurf(self) -> pygame.Surface:
        return self.__surf

    # Setters
    def setSurf(self, surf):
        self.__surf = surf

    # Methods
    def updateSurf(self,
                   character: Character,
                   level_name: int,
                   num_remaining_enemies: int) -> None:
        """Updates surface with new data.

        To be run at at the conclusion of a turn. TODO likely can split into separate methods.
        """
        # Getting character information
        level = character.getLevel()
        exp = character.getExp()
        req_exp = character.calcRequiredExp()
        health = character.getHealth()
        max_health = character.getMaxHealth()

        # Rendering text surfaces
        big_font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 24)
        lvlname_text_surf = big_font.render(level_name, True, (0,0,0))
        chr_level_text_surf = small_font.render(f"LEVEL: {level}", True, (0,0,0))
        exp_text_surf = small_font.render(f"EXP: {exp} / {req_exp}", True, (0,0,0))
        health_text_surf = small_font.render(f"HP: {health} / {max_health}", True, (0,0,0))
        numenemy_text_surf = small_font.render(f"Enemies left: {num_remaining_enemies}", True, (0,0,0))

        # Repositioning text surfaces' rects
        lvlname_text_rect = lvlname_text_surf.get_rect()
        lvlname_text_rect.center = (216, 32)
        chr_level_text_rect = chr_level_text_surf.get_rect()
        chr_level_text_rect.topleft = (20, 80)
        exp_text_rect = exp_text_surf.get_rect()
        exp_text_rect.topleft = (20, 100)
        health_text_rect = health_text_surf.get_rect()
        health_text_rect.topleft = (20, 120)
        numenemy_text_rect = numenemy_text_surf.get_rect()
        numenemy_text_rect.topleft = (20, 140)

        # Blitting text objects to surface
        surf = self.getSurf()
        surf.fill((255, 255, 255))
        surf.blit(lvlname_text_surf, lvlname_text_rect)
        surf.blit(chr_level_text_surf, chr_level_text_rect),
        surf.blit(exp_text_surf, exp_text_rect),
        surf.blit(health_text_surf, health_text_rect),
        surf.blit(numenemy_text_surf, numenemy_text_rect)
        return