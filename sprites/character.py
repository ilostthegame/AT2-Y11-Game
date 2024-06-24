import pygame
from sprites.active_entity import ActiveEntity
from pygame.locals import *
from assets import GAME_ASSETS
from sprites.healthbar import Healthbar
from sprites.weapon import Weapon

class Character(ActiveEntity):
    """
    Class representing a character sprite, with parent ActiveEntity

    Attributes:
        (Inherited)
        surf (pygame.Surface): Pygame surface for the entity, onto which to blit the entity image, weapon and healthbar -
            Size: 64 x 64, transparent.
        image (pygame.Surface): Surface representing entity's sprite image - Size: 32 x 48
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

        level (int): Current level of character
        experience_points (int): Experience point stat

    Methods:
        gainExperience(self, experience: int) -> None: 
            Increases experience, and if possible levels up.
        updateStats(self) -> None: 
            Updates attack, defence based on level.
        calcRequiredExperience(self) -> int: 
            Returns total required experience for the next level.
        takeDamage(self, damage: int) -> None: 
            Changes health according to defence and damage.
        getInfo(self) @abstractmethod: 
            Returns the info of entity for saving. TODO might not even be needed with pickling.
        
        (Inherited)
        updateSurf(self):  
            Blits the entity image, healthbar and weapon onto the entity's Surface.
        updatePos(self): 
            Changes position of Rect according to xcoord, ycoord
    """
    
    # Attributes
    __level = None
    __experience_points = None

    # Constructor
    def __init__(self,  
                 image: pygame.Surface, 
                 name: str,
                 weapon_id: str, 
                 attack: int = 25, 
                 defence: int = 25, 
                 max_health: int = 100, 
                 health: int = 100, 
                 health_regen: int = 2,
                 is_alive: bool = True, 
                 xcoord: int = 0, 
                 ycoord: int = 0, 
                 level: int = 1, 
                 experience_points: int = 0):
        super().__init__(image, name, attack, defence, max_health, health, health_regen, 
                         Weapon(weapon_id, xcoord, ycoord),
                         is_alive, xcoord, ycoord, Healthbar(health, max_health)) 
        self.setLevel(level)
        self.setExperiencePoints(experience_points)

    # Getters
    def getLevel(self):
        return self.__level
    def getExperiencePoints(self):
        return self.__experience_points
    
    # Setters
    def setLevel(self, level):
        self.__level = level
    def setExperiencePoints(self, experience_points):
        self.__experience_points = experience_points

    # Methods
    def gainExperience(self, experience):
        """
        Increases character's experience, and increases levels accordingly. Subtracts used experience.
        Runs stat increase method based on levels gained.
        """
        original_level = self.getLevel()
        self.setExperiencePoints(self.getExperiencePoints() + experience)
        required_experience = self.calcRequiredExperience() # Calculate experience required for next level

        # Level up character while character has enough experience to level up and is below the level cap (50).
        while self.getExperiencePoints() >= required_experience and self.getLevel() < 50:
            self.setLevel(self.getLevel() + 1)
            self.setExperiencePoints(self.getExperiencePoints() - required_experience) # subtract used experience points.
            required_experience = self.calcRequiredExperience() # Re-calculate experience required for next level

        # Update attack/defence and if levelled up, prints levelup info.
        level_increase = self.updateStats(original_level)
        # TODO


    def updateStats(self, original_level):
        """
        Updates attack, defence based on change in level. Adds 2 per level. Returns tuple (level_increase, attack_increase, defence_increase)
        """
        level_increase = self.getLeve() - original_level
        attack_increase = level_increase * 2
        defence_increase = level_increase * 2
        self.setAttack(self.getAttack() + attack_increase)
        self.setDefence(self.getDefence() + defence_increase)
        return (level_increase, attack_increase, defence_increase)

    def calcRequiredExperience(self):
        """
        Calculates total required experience to get to next level
        """ 
        return int(100 * (1.5 ** (self.getLevel())))  # Current formula TODO change: 100 * 1.5^level.

    def getInfo(self):
        """
        Returns character info
        """
        # TODO maybe this can just be generalised??? idk it's only useful for saving so do it later.
        pass