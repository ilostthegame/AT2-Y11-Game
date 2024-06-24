import pygame
from pygame.locals import *
from abc import ABC, abstractmethod
from sprites.healthbar import Healthbar
from sprites.weapon import Weapon

class ActiveEntity(pygame.sprite.Sprite, ABC):
    """
    Abstract class with children Character and Entity sprites. Represents moving/battling sprites
    Attributes:
        surf (pygame.Surface): Pygame surface for the entity, onto which to blit the entity image, weapon and healthbar
            Size: 64 x 64, transparent
        image (pygame.Surface): Surface representing entity's sprite image. Size: 32 x 48
        name (str): Name of character
        attack (int): Attack stat
        defence (int): Defence stat
        max_health (int): Maximum health stat
        health (int): Current health stat
        health_regen (int): How much health regenerates each turn
        weapon (Weapon): Currently held weapon
        is_alive (bool): Whether entity's is alive: health above 0 or not
        xcoord (int): X coordinate of entity in world
        ycoord (int): Y coordinate of entity in world
        healthbar (Healthbar): Healthbar of entity

    Methods:
        updateSurf(self): 
            Blits the character image, healthbar and weapon onto the entity's Surface.
        updatePos(self): 
            Changes xcoord, ycoord based on pygame events.
        getInfo(self) @abstractmethod: 
            Returns the info of entity for saving. TODO might not even be needed with pickling.

    """

    # Attributes
    __surf = None 
    __image = None 
    __name = None
    __attack = None
    __defence = None
    __max_health = None
    __health = None
    __health_regen = None
    __weapon = None
    __is_alive = None
    __xcoord = None
    __ycoord  = None
    __healthbar = None

    # Constructor
    def __init__(self, 
                 image: pygame.Surface, 
                 name: str, 
                 attack: int, 
                 defence: int, 
                 max_health: int, 
                 health: int,
                 health_regen: int, 
                 weapon: Weapon, 
                 is_alive: bool, 
                 xcoord: float, 
                 ycoord: float, 
                 healthbar: Healthbar):
        super().__init__()
        self.setSurf(pygame.Surface((64, 64), SRCALPHA))
        self.setImage(image)
        self.setName(name)
        self.setAttack(attack)
        self.setDefence(defence)
        self.setMaxHealth(max_health)
        self.setHealth(health)
        self.setHealthRegen(health_regen)
        self.setWeapon(weapon)
        self.setIsAlive(is_alive)
        self.setXcoord(xcoord)
        self.setYcoord(ycoord)
        self.setHealthbar(healthbar)

        self.updateHealthbar()
        self.updateSurf()

    # Getters
    def getSurf(self):
        return self.__surf
    def getImage(self):
        return self.__image
    def getName(self):
        return self.__name
    def getAttack(self):
        return self.__attack
    def getDefence(self):
        return self.__defence
    def getMaxHealth(self):
        return self.__max_health
    def getHealth(self):
        return self.__health
    def getHealthRegen(self):
        return self.__health_regen
    def getWeapon(self):
        return self.__weapon
    def getIsAlive(self):
        return self.__is_alive
    def getXcoord(self):
        return self.__xcoord
    def getYcoord(self):
        return self.__ycoord
    def getHealthbar(self):
        return self.__healthbar

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setImage(self, image):
        self.__image = image
    def setName(self, name):
        self.__name = name

    def setAttack(self, attack):
        if attack < 0:
            self.__attack = 0
        else:
            self.__attack = attack

    def setDefence(self, defence):
        if defence < 0:
            self.__defence = 0
        else:
            self.__defence = defence

    def setMaxHealth(self, max_health):
        if max_health <= 0: # makes sure max_health > 0
            self.setMaxHealth(1)
        else:
            self.__max_health = max_health

    def setHealth(self, health):
        max_health = self.getMaxHealth() 
        if health > max_health: # ensures 0 <= health <= max_health
            self.__health = max_health
        elif health < 0:
            self.__health = 0
            self.setIsAlive(False)
        else:
            self.__health = health

    def setHealthRegen(self, health_regen):
        self.__health_regen = health_regen
    def setWeapon(self, weapon):
        self.__weapon = weapon
    def setIsAlive(self, is_alive):
        self.__is_alive = is_alive
    def setXcoord(self, xcoord):
        self.__xcoord = xcoord
    def setYcoord(self, ycoord):
        self.__ycoord = ycoord
    def setHealthbar(self, healthbar):
        self.__healthbar = healthbar
        

    # Methods
    def updateSurf(self) -> None:
        """
        Blits the character image, healthbar and weapon onto the entity's Surface.
        """
        surf = self.getSurf()
        surf.fill((0,0,0,0))
        surf.blit(self.getImage(), (0, 0))
        surf.blit(self.getHealthbar().getSurf(), (0, 48))
        surf.blit(self.getWeapon().getSurf(), (32, 0))
        self.setSurf(surf)
        return
    
    def updatePos(self, pygame_events: list[pygame.event.Event]) -> None:
        """
        Changes xcoord, ycoord based on pygame events.
        """
        pass
    
    def updateHealthbar(self):
        """
        Updates healthbar attributes, and its surface.
        """
        self.getHealthbar().setEntityMaxHealth(self.getMaxHealth())
        self.getHealthbar().setEntityHealth(self.getHealth())
        self.getHealthbar().updateSurf()

    @abstractmethod
    def getInfo(self):
        """
        Returns entity info.
        """
        pass
