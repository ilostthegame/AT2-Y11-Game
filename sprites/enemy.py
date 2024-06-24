import pygame
import random
from file_id_interpreter import FileIdInterpreter
from sprites.active_entity import ActiveEntity
from assets import GAME_ASSETS, load_assets
from sprites.healthbar import Healthbar
from sprites.weapon import Weapon

class Enemy(ActiveEntity):
    """
    Class representing an enemy sprite, with parent ActiveEntity

    Attributes:
        (Inherited)
        surf (pygame.Surface): Pygame surface for the entity, onto which to blit the entity image, weapon and healthbar
            Size: 64 x 64 transparent.
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

        movement_pattern (str): Represents the algorithm to be used for 
        xp_yield (int): Represents how much xp is earned through defeating enemy
    
    Methods:
        calcMovement(self, user_position: tuple[int, int]): 
            Returns a tuple (xcoord, ycoord) representing the square enemy will move to.
        TODO
        getInfo(self): 
            Returns info of enemy
        
        (Inherited)
        updateSurf(self): 
            Blits the entity image, healthbar and weapon onto the entity's Surface.
        updatePos(self): 
            Changes position of Rect according to xcoord, ycoord
    """

    # Attributes
    __movement_pattern = None
    __xp_yield = None

    # Constructor
    def __init__(self, enemy_id: str, xcoord: int, ycoord: int):
        # Getting file info
        # Attributes in attribute_list = [image, name, attack, defence, health, health_regen, weapon_id, movement_pattern, xp_yield]
        attribute_list = FileIdInterpreter().interpretFileInfo('gameinfostorage/enemy_id.txt', enemy_id) 
        
        # Unpacking file info, and creating additional enemy attributes
        image, name, attack, defence, health, health_regen, weapon_id, movement_pattern, xp_yield = attribute_list # unpacks attribute_list
        attack, defence, health, health_regen, xp_yield = [int(i) for i in (attack, defence, health, health_regen, xp_yield)] # converts some attributes to integers
        weapon = Weapon(weapon_id, xcoord, ycoord) # creates weapon object enemy is wielding
        healthbar = Healthbar(health, health) # creates healthbar object attached to enemy
    
        # Initialising enemy object. Note that health variable is used to set both max_health and health.
        super().__init__(pygame.image.load(GAME_ASSETS[image]), # enemy image
                         name, attack, defence, health, health, health_regen, weapon, True, xcoord, ycoord, healthbar)
        self.setMovementPattern(movement_pattern)
        self.setXpYield(xp_yield)

    # Getters
    def getMovementPattern(self):
        return self.__movement_pattern
    def getXpYield(self):
        return self.__xp_yield

    # Setters
    def setMovementPattern(self, movement_pattern):
        self.__movement_pattern = movement_pattern
    def setXpYield(self, xp_yield):
        self.__xp_yield = xp_yield

    # Methods
    def getInfo(self):
        pass