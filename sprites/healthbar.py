import pygame

class Healthbar(pygame.sprite.Sprite):
    """
    Class representing a healthbar sprite

    Attributes:

        surf (pygame.Surface): Represents the surface of the healthbar. size: 64x16
        rect (pygame.Rect): Position of surface

        Entity info:
        entity_health (int)
        entity_max_health (int)

    Methods: 
        updateHealth(self): Updates the health indicator of healthbar - to be called whenever entity health or max_health updates
    """

    # Attributes
    __surf = None
    __rect = None
    __entity_health = None
    __entity_max_health = None

    # Constructor
    def __init__(self, entity_health: int, entity_max_health: int):
        super().__init__()
        self.setSurf(pygame.Surface((64, 16)))
        self.setRect(self.getSurf().get_rect())
        self.setEntityHealth(entity_health)
        self.setEntityMaxHealth(entity_max_health)

    # Getters
    def getSurf(self):
        return self.__surf
    def getRect(self):
        return self.__rect
    def getEntityHealth(self):
        return self.__entity_health
    def getEntityMaxHealth(self):
        return self.__entity_max_health

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setRect(self, rect):
        self.__rect = rect
    def setEntityHealth(self, entity_health):
        self.__entity_health = entity_health
    def setEntityMaxHealth(self, entity_max_health):
        self.__entity_max_health = entity_max_health

    def updateHealth(self):
        """
        Updates the health indicator of healthbar - to be called whenever entity health or max_health updates
        """
        surf = self.getSurf()
        length = int(self.getEntityHealth()/self.getEntityMaxHealth() * 62) # calculates length of healthbar to be filled based on percent.
        pygame.draw.rect(surf, (50, 50, 50), (0, 0, 64, 16)) # draw background of healthbar
        pygame.draw.rect(surf, (0, 50, 200), (1, 1, length, 14)) # draw health indicator
        self.setSurf(surf)