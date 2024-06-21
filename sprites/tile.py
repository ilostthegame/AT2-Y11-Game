import pygame

class Tile(pygame.sprite.Sprite):
    """
    Class representing a tile sprite
    TODO optional - convert this to a file system too.
    
    Attributes:
        surf (pygame.Surface)
        accessible (bool): Whether tile can be entered by an entity
        occupied (bool): Whether an ActiveEntity is on the tile
        damage (int): How much damage an entity takes upon entering tile
    """

    # Attributes
    __surf = None
    __accessible = None
    __occupied = None
    __damage = None

    # Constructor
    def __init__(self, 
                 colour: tuple[int, int, int], 
                 accessible: bool,  
                 damage: int = 0, 
                 occupied: bool = False,
                 surf: pygame.Surface = pygame.Surface((64, 64))):
        self.setAccessible(accessible)
        self.setDamage(damage)
        self.setOccupied(occupied)
        self.setSurf(surf)
        self.getSurf().fill(colour)

    # Getters
    def getSurf(self):
        return self.__surf
    def getAccessible(self):
        return self.__accessible
    def getOccupied(self):
        return self.__occupied
    def getDamage(self):
        return self.__damage

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setAccessible(self, accessible):
        self.__accessible = accessible
    def setOccupied(self, occupied):
        self.__occupied = occupied
    def setDamage(self, damage):
        self.__damage = damage
