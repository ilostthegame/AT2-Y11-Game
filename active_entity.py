import pygame
from pygame.locals import *
from abc import ABC, abstractmethod
from healthbar import Healthbar
from weapon import Weapon

class ActiveEntity(pygame.sprite.Sprite, ABC):
    """
    Abstract class with children Character and Entity sprites. Represents moving/battling sprites
    Attributes:
        surf (pygame.Surface): Pygame surface for the entity, onto which to blit the entity image, weapon and healthbar - 64x64 transparent square
        image (pygame.Surface): Surface representing entity's sprite image
        rect (pygame.Rect): Rectangle representing entity Surface position
        name (str): Name of character
        attack (int): Attack stat
        defence (int): Defence stat
        max_health (int): Maximum health stat
        health (int): Current health stat
        weapon (Weapon): Currently held weapon
        is_alive (bool): Whether entity's is alive: health above 0 or not
        xcoord (int): X coordinate of entity in world
        ycoord (int): Y coordinate of entity in world
        healthbar (Healthbar): Healthbar of entity

    Methods:
        updateSurf(self): Blits the character image, healthbar and weapon onto the entity's Surface.
        updatePos(self): Changes position of Rect according to xcoord, ycoord
        getInfo(self) @abstractmethod: Returns the info of entity for saving. TODO might not even be needed with pickling.

    """

    # Attributes
    __surf = None 
    __image = None 
    __rect = None 
    __name = None
    __attack = None
    __defence = None
    __max_health = None
    __health = None
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
                 weapon: str, 
                 is_alive: bool, 
                 xcoord: float, 
                 ycoord: float, 
                 healthbar: Healthbar,
                 surf: pygame.Surface = pygame.Surface((64, 64), SRCALPHA)):
        super().__init__()
        self.setImage(image)
        self.setName(name)
        self.setAttack(attack)
        self.setDefence(defence)
        self.setHealthbar(healthbar)
        self.setMaxHealth(max_health)
        self.setHealth(health)
        self.setWeapon(weapon)
        self.setIsAlive(is_alive)
        self.setXcoord(xcoord)
        self.setYcoord(ycoord)
        self.setSurf(surf)
        self.setRect(self.getSurf().get_rect())

    # Getters
    def getSurf(self):
        return self.__surf
    def getImage(self):
        return self.__image
    def getRect(self):
        return self.__rect
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
    def setRect(self, rect):
        self.__rect = rect
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
        # Update Healthbar's display
        self.getHealthbar().setEntityMaxHealth(self.getMaxHealth())
        self.getHealthbar().updateHealth()
        
    def setHealth(self, health):
        max_health = self.getMaxHealth() 
        if health > max_health: # ensures 0 <= health <= max_health
            self.__health = max_health
        elif health < 0:
            self.__health = 0
            self.setIsAlive(False)
        else:
            self.__health = health
        # Update Healthbar's display
        self.getHealthbar().setEntityHealth(self.getHealth())
        self.getHealthbar().updateHealth()
        
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
    def updateSurf(self):
        """
        Blits the character image, healthbar and weapon onto the entity's Surface.
        """
        surf = self.getSurf()
        surf.fill((0,0,0,0))
        surf.blit(self.getImage(), (0,0))
        surf.blit(self.getHealthbar().getSurf(), (0, 48))
        # surf.blit(self.getWeapon().getSurf(), (0,0))
        self.setSurf(surf)
    
    def updatePos(self):
        """
        Changes position of Rect according to xcoord, ycoord
        """
        rect = self.getRect()
        rect.topleft = (self.getXcoord() * 64, self.getYcoord() * 64)
        self.setRect(rect)

    @abstractmethod
    def getInfo(self):
        """
        Returns entity info.
        """
        pass
