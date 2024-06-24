import pygame 
from pygame.locals import *
from file_id_interpreter import FileIdInterpreter
from assets import GAME_ASSETS
from attack import Attack

class Weapon(pygame.sprite.Sprite): 
    """
    A class representing a weapon.

    Attributes:
        image (pygame.Surface): The weapon's image. Size: 32 x 48, transparent
        name (str): Name of the weapon
        attack_list (list[Attack]): List of attacks on the weapon
        entity_xcoord (int): The xcoord of the entity holding weapon
        entity_ycoord (int): The ycoord of the entity holding weapon

    Methods:
    TODO
    """

    # Attributes
    __image = None
    __name = None
    __attack_list = None
    __entity_xcoord = None
    __entity_ycoord = None

    # Constructor
    def __init__(self, weapon_id: str, entity_xcoord: int, entity_ycoord: int):
        # Getting and unpacking file info
        attribute_list = FileIdInterpreter().interpretFileInfo('gameinfostorage/weapon_id.txt', weapon_id) # [image, name, *attacks]
        image_name, name = attribute_list[0], attribute_list[1]
        
        # Initialising weapon object.
        super().__init__()
        self.setImage(pygame.image.load(GAME_ASSETS[image_name]).convert_alpha())
        self.setName(name)
        self.setEntityXcoord(entity_xcoord)
        self.setEntityYcoord(entity_ycoord)

        # Adds all attacks to the attack list.
        attack_list = list()
        for attack_id in attribute_list[2:]:
            attack = Attack(attack_id)
            attack_list.append(attack)
        self.setAttackList(attack_list)

    # Getters
    def getImage(self):
        return self.__image
    def getName(self):
        return self.__name
    def getAttackList(self):
        return self.__attack_list
    def getEntityXcoord(self):
        return self.__entity_xcoord
    def getEntityYcoord(self):
        return self.__entity_ycoord

    # Setters
    def setImage(self, image):
        self.__image = image
    def setName(self, name):
        self.__name = name
    def setAttackList(self, attacks):
        self.__attack_list = attacks
    def setEntityXcoord(self, entity_xcoord):
        self.__entity_xcoord = entity_xcoord
    def setEntityYcoord(self, entity_ycoord):
        self.__entity_ycoord = entity_ycoord