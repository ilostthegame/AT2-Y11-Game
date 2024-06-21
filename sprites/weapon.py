import pygame 
from pygame.locals import *
from file_id_interpreter import FileIdInterpreter
from assets import GAME_ASSETS
from attack import Attack

class Weapon(pygame.sprite.Sprite): 
    """
    A class representing a weapon.

    Attributes:
        surf (pygame.Surface): The weapon surface.
        image (pygame.image): The weapon's image
        rect (pygame.Rect): The weapon surface's rectangle
        name (str): The name of the weapon
        attack_list (list): The list of attacks the weapon has
        entity_xcoord (int): The xcoord of the entity holding weapon
        entity_ycoord (int): The ycoord of the entity holding weapon
        TODO will need some cooldown tracker

    Methods:
    TODO
    """

    # Attributes
    __surf = None
    __image = None
    __rect = None
    __name = None
    __attack_list = None
    __entity_xcoord = None
    __entity_ycoord = None

    # Constructor
    def __init__(self, weapon_id: str, entity_xcoord: int, entity_ycoord: int):
        # Getting and unpacking file info
        attribute_list = FileIdInterpreter().interpretFileInfo('gameinfostorage/weapon_id.txt', weapon_id) # [image, name, *attacks]
        image, name = attribute_list[0], attribute_list[1]
        
        # Initialising weapon object.
        self.setImage(pygame.image.load(GAME_ASSETS[image]))
        self.setName(name)
        self.setAttackList(list())
        self.setEntityXcoord(entity_xcoord)
        self.setEntityYcoord(entity_ycoord)
        self.setSurf(pygame.Surface((64, 64), SRCALPHA))
        self.setRect(self.getSurf().get_rect())

        # Adds all attacks to the attack list.
        for attack_id in attribute_list[2:]:
            attack = Attack(attack_id)
            self.getAttackList().append(attack)

    # Getters
    def getSurf(self):
        return self.__surf
    def getImage(self):
        return self.__image
    def getRect(self):
        return self.__rect
    def getName(self):
        return self.__name
    def getAttackList(self):
        return self.__attack_list
    def getEntityXcoord(self):
        return self.__entity_xcoord
    def getEntityYcoord(self):
        return self.__entity_ycoord

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setImage(self, image):
        self.__image = image
    def setRect(self, rect):
        self.__rect = rect
    def setName(self, name):
        self.__name = name
    def setAttackList(self, attacks):
        self.__attack_list = attacks
    def setEntityXcoord(self, entity_xcoord):
        self.__entity_xcoord = entity_xcoord
    def setEntityYcoord(self, entity_ycoord):
        self.__entity_ycoord = entity_ycoord