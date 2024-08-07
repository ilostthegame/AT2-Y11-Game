import pygame
from typing import Optional
from sprites.entity import Entity

class Tile(pygame.sprite.Sprite):
    """
    Class representing a tile sprite.
    
    Attributes:
        name (str): Name of tile.
        surf (pygame.Surface): Size: 64 x 64.
        accessible (bool): Whether tile can be entered by an entity.
        occupied_by (Optional[Entity]]): The entity currently occupying the tile.
        damage (int): How much damage an entity takes upon entering tile.
    """
    # Attributes
    __name = None
    __surf = None
    __accessible = None
    __occupied_by = None
    __damage = None

    # Constructor
    def __init__(self,
                 name: str,
                 colour: tuple[int, int, int], 
                 accessible: bool,
                 occupied_by: Optional[Entity],
                 damage: int = 0):
        super().__init__()
        surf = pygame.Surface((64, 64))
        pygame.draw.rect(surf, (128, 128, 128), (0,0, 64, 64))
        pygame.draw.rect(surf, colour, (1, 1, 62, 62)) 
        self.setName(name)
        self.setSurf(surf)
        self.setAccessible(accessible)
        self.setOccupiedBy(occupied_by)
        self.setDamage(damage)

    # Getters
    def getName(self):
        return self.__name
    def getSurf(self):
        return self.__surf
    def getAccessible(self):
        return self.__accessible
    def getOccupiedBy(self):
        return self.__occupied_by
    def getDamage(self):
        return self.__damage

    # Setters
    def setName(self, name):
        self.__name = name
    def setSurf(self, surf):
        self.__surf = surf
    def setAccessible(self, accessible):
        self.__accessible = accessible
    def setOccupiedBy(self, occupied_by):
        self.__occupied_by = occupied_by
    def setDamage(self, damage):
        self.__damage = damage