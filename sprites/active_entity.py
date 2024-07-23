import pygame
from pygame.locals import *
from abc import ABC, abstractmethod
from sprites.healthbar import Healthbar
from sprites.weapon import Weapon
from attack import Attack
from random import randint
from math import sqrt, ceil, floor
from sprites.entity import Entity

class ActiveEntity(Entity, ABC):
    """Abstract class that represents 'active' (moving/battling) entities

    Attributes:
        (Inherited)
        surf (pygame.Surface): Pygame surface for the entity, onto which to blit the entity image, weapon and healthbar
            Size: 64 x 64, transparent
        xcoord (int): X coordinate of entity in world
        ycoord (int): Y coordinate of entity in world
            
        entity_image (pygame.Surface): Surface representing entity's sprite image. 
            Size: 32 x 48, transparent
        name (str): Name of entity
        strength (int): Strength stat
        defence (int): Defence stat
        max_health (int): Maximum health stat
        health (int): Current health stat
        health_regen (int): How much health regenerates each turn
        weapon (Weapon): Currently held weapon
        is_alive (bool): Whether entity's is alive: health above 0 or not
        healthbar (Healthbar): Healthbar of entity
    """

    # Attributes
    __entity_image = None 
    __name = None
    __strength = None
    __defence = None
    __max_health = None
    __health = None
    __health_regen = None
    __weapon = None
    __is_alive = None
    __healthbar = None

    # Constructor
    def __init__(self, 
                 entity_image: pygame.Surface, 
                 name: str, 
                 strength: int, 
                 defence: int, 
                 max_health: int, 
                 health: int,
                 health_regen: int, 
                 weapon: Weapon, 
                 is_alive: bool, 
                 xcoord: float, 
                 ycoord: float, 
                 healthbar: Healthbar):
        super().__init__(pygame.Surface((64, 64), SRCALPHA), xcoord, ycoord)
        self.setEntityImage(entity_image)
        self.setName(name)
        self.setStrength(strength)
        self.setDefence(defence)
        self.setMaxHealth(max_health)
        self.setHealth(health)
        self.setHealthRegen(health_regen)
        self.setWeapon(weapon)
        self.setIsAlive(is_alive)
        self.setHealthbar(healthbar)
        # Updates the display of entity surface.
        self.updateHealthbar()
        self.updateSurf()

    # Getters
    def getEntityImage(self) -> pygame.Surface:
        return self.__entity_image
    def getName(self) -> str:
        return self.__name
    def getStrength(self) -> int:
        return self.__strength
    def getDefence(self) -> int:
        return self.__defence
    def getMaxHealth(self) -> int:
        return self.__max_health
    def getHealth(self) -> int:
        return self.__health
    def getHealthRegen(self) -> int:
        return self.__health_regen
    def getWeapon(self) -> Weapon:
        return self.__weapon
    def getIsAlive(self) -> bool:
        return self.__is_alive
    def getHealthbar(self) -> Healthbar:
        return self.__healthbar

    # Setters
    def setHealth(self, health):
        """Sets health. Ensures 0 <= health <= max_health.
        
        If health == 0, sets is_alive to False.
        """
        if health < 0:
            self.__health = 0
            self.setIsAlive(False)
        elif health > self.getMaxHealth():
            self.__health = self.getMaxHealth()
        else:
            self.__health = health

    def setEntityImage(self, entity_image):
        self.__entity_image = entity_image
    def setName(self, name):
        self.__name = name
    def setStrength(self, strength):
        self.__strength = strength
    def setDefence(self, defence):
        self.__defence = defence
    def setMaxHealth(self, max_health):
        self.__max_health = max_health
    def setHealthRegen(self, health_regen):
        self.__health_regen = health_regen
    def setWeapon(self, weapon):
        self.__weapon = weapon
    def setIsAlive(self, is_alive):
        self.__is_alive = is_alive
    def setHealthbar(self, healthbar):
        self.__healthbar = healthbar
        
    # Methods
    def updateSurf(self) -> None:
        """Blits the entity_image, healthbar and weapon onto the entity's Surface."""
        surf = self.getSurf()
        surf.fill((0,0,0,0)) # Renders as transparent.
        surf.blit(self.getEntityImage(), (0, 0))
        surf.blit(self.getHealthbar().getSurf(), (0, 48))
        surf.blit(self.getWeapon().getSurf(), (32, 0))
        self.setSurf(surf)
        return

    def updateHealthbar(self):
        """Updates healthbar attributes, and its surface."""
        self.getHealthbar().setEntityMaxHealth(self.getMaxHealth())
        self.getHealthbar().setEntityHealth(self.getHealth())
        self.getHealthbar().updateSurf()

    def useAttack(self, attack: Attack, target) -> list[str]:
        """Runs an attack.

        Returns a list of two/three strings representing:
            - The user/name/target of the attack.
            - The result of the attack.
            - (Optional) that the target fainted.
        NOTE: This method does not check if the target is in range.
        Args:
            attack (Attack): The attack being used.
            target (ActiveEntity): The target of the attack.
        """
        power = attack.getPower()
        accuracy = attack.getAccuracy()
        acc_roll = randint(1, 100)
        events = []
        events.append(f'{self.getName()} used {attack.getName()} on {target.getName()}.')
        if acc_roll <= accuracy:
            raw_damage = self.calcRawDamage(power)
            damage_taken = target.takeDamage(raw_damage)
            events.append(f'{target.getName()} took {damage_taken} damage!')
            if not target.getIsAlive():
                events.append(f'{target.getName()} fainted!')
        else:
            events.append('The attack missed!')
        return events

    def calcRawDamage(self, power: int) -> int:
        """Returns raw damage of an attack based on power and strength."""
        strength = self.getStrength()
        return floor(sqrt(strength)/10 * power)

    def takeDamage(self, damage: int) -> int:
        """Takes damage based on damage of the attack, and defence.
        
        If dead, kill()'s self. 
        Returns the damage taken."""
        defence = self.getDefence()
        damage_taken = ceil((0.99)**defence * damage)
        self.setHealth(self.getHealth() - damage_taken)
        if not self.getIsAlive():
            self.kill()
        return damage_taken
    
    def regenerate(self) -> None:
        """Regenerates health based on health_regen"""
        self.setHealth(self.getHealth() + self.getHealthRegen())