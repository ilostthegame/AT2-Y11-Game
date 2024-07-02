import pygame

class DataDisplay(pygame.sprite.Sprite):
    """
    Sidebar component which displays the following:
        - Character level
        - Exp / req exp
        - Health / max health, 
        - Level name
    To be updated each iteration with new information.

    Attributes:
        surf (pygame.Surface): Surface to which data is displayed
            Size: 432 x 200
    
    Methods:
        update(self,
               character_level: int,
               exp: int,
               req_exp: int,
               health: int,
               max_health: int,
               level_name: int) -> None:
            Updates surface with new data
    """

    # Attributes
    __surf = None

    # Constructor
    def __init__(self):
        self.setSurf(pygame.Surface((432, 200)))

    # Getters
    def getSurf(self):
        return self.__surf

    # Setters
    def setSurf(self, surf):
        self.__surf = surf


    def update(self,
               character_level: int,
               exp: int,
               req_exp: int,
               health: int,
               max_health: int,
               level_name: int) -> None:
        """
        Updates surface with new data
        """
        bigfont = pygame.font.Font(None, 48)
        font = pygame.font.Font(None, 24)
        surf = self.getSurf()

        # Rendering text surfaces
        lvlname_text_surf = bigfont.render(level_name, True, (0,0,0))
        chr_level_text_surf = font.render(f"LEVEL: {character_level}", True, (0,0,0))
        exp_text_surf = font.render(f"EXP: {exp} / {req_exp}", True, (0,0,0))
        health_text_surf = font.render(f"HP: {health} / {max_health}", True, (0,0,0))

        # Repositioning text surfaces' rects
        lvlname_text_rect = lvlname_text_surf.get_rect()
        lvlname_text_rect.center = (216, 32)
        chr_level_text_rect = chr_level_text_surf.get_rect()
        chr_level_text_rect.topleft = (20, 80)
        exp_text_rect = exp_text_surf.get_rect()
        exp_text_rect.topleft = (20, 100)
        health_text_rect = health_text_surf.get_rect()
        health_text_rect.topleft = (20, 120)

        # Blitting text objects to surface
        surf.fill((255, 255, 255))
        surf.blit(lvlname_text_surf, lvlname_text_rect)
        surf.blit(chr_level_text_surf, chr_level_text_rect)
        surf.blit(exp_text_surf, exp_text_rect)
        surf.blit(health_text_surf, health_text_rect)