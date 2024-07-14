import pygame

class Tile(pygame.sprite.Sprite):
    """
    Class representing a tile sprite
    TODO optional - convert this to a file system too.
    
    Attributes:
        surf (pygame.Surface): Size: 64 x 64
        accessible (bool): Whether tile can be entered by an entity
        occupied_by (Optional[str]): What entity is occupying the tile currently:
            Is None if no entity, else is in ['character', 'enemy', 'npc', 'portal']
        damage (int): How much damage an entity takes upon entering tile
    """
    # Attributes
    __surf = None
    __accessible = None
    __occupied_by = None
    __damage = None

    # Constructor
    def __init__(self, 
                 colour: tuple[int, int, int], 
                 accessible: bool,
                 occupied_by: str,
                 damage: int = 0):
        super().__init__()

        # Creates tile surface with grey border
        surf = pygame.Surface((64, 64))
        surf.fill((128, 128, 128)) # creates border
        pygame.draw.rect(surf, colour, (1, 1, 62, 62)) # Inner square of tile
        self.setSurf(surf)
        self.setAccessible(accessible)
        self.setOccupiedBy(occupied_by)
        self.setDamage(damage)

    # Getters
    def getSurf(self):
        return self.__surf
    def getAccessible(self):
        return self.__accessible
    def getOccupiedBy(self):
        return self.__occupied
    def getDamage(self):
        return self.__damage

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setAccessible(self, accessible):
        self.__accessible = accessible
    def setOccupiedBy(self, occupied):
        self.__occupied = occupied
    def setDamage(self, damage):
        self.__damage = damage