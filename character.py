import pygame
from active_entity import ActiveEntity
from pygame.locals import *
from assets import GAME_ASSETS
from healthbar import Healthbar
from weapon import Weapon

class Character(ActiveEntity):
    """
    Class representing a character sprite, with parent ActiveEntity

    Attributes:
        MAX_LEVEL (int): Maximum level of character
        level (int): Current level of character
        experience_points (int): Experience point stat
        skills (list[*Skill]): List of skills the character has 
        items (list[*Item]): List of items the character has 
        gold (int): Amount of gold character has 
        
    Methods:
        gainExperience(self, experience): Increases experience, and if possible levels up.
        updateStats(self): Updates attack, defence based on level.
        calcRequiredExperience(self): Calculates total required experience for the next level.
        takeDamage(self, damage): Changes health according to defence and damage.
        TODO updatePosition(self, pressed_keys):
        TODO getInfo
    """
    
    # Attributes
    MAX_LEVEL = 50
    __level = None
    __experience_points = None
    __skills = None
    __items = None
    __gold = None

    # Constructor
    def __init__(self,  
                 image: pygame.Surface, 
                 name: str, 
                 attack: int, 
                 defence: int, 
                 max_health: int, 
                 health: int, 
                 weapon: Weapon, 
                 is_alive: bool, 
                 xcoord: int, 
                 ycoord: int, 
                 level: int, 
                 experience_points: int, 
                 skills: list, 
                 items: list, 
                 gold: int, 
                 healthbar: Healthbar):
        super().__init__(image, name, attack, defence, max_health, health, weapon, is_alive, xcoord, ycoord, healthbar) 
        self.setLevel(level)
        self.setExperiencePoints(experience_points)
        self.setSkills(skills)
        self.setItems(items)
        self.setGold(gold)

    # Getters
    def getLevel(self):
        return self.__level
    def getExperiencePoints(self):
        return self.__experience_points
    def getSkills(self):
        return self.__skills
    def getItems(self):
        return self.__items
    def getGold(self):
        return self.__gold

    # Setters
    def setLevel(self, level):
        self.__level = level
    def setExperiencePoints(self, experience_points):
        self.__experience_points = experience_points
    def setSkills(self, skills):
        self.__skills = skills
    def setItems(self, items):
        self.__items = items
    def setGold(self, gold):
        self.__gold = gold


    # Methods
    def gainExperience(self, experience):
        """
        Increases character's experience, and increases levels accordingly. Subtracts used experience.
        Runs stat increase method based on levels gained.
        """
        original_level = self.getLevel()
        self.setExperiencePoints(self.getExperiencePoints() + experience)  # Increase character's experience points
        required_experience = self.calcRequiredExperience() # Calculate experience required for next level

        # Level up character while character has enough experience to level up and is below the level cap.
        while self.getExperiencePoints() >= required_experience and self.getLevel() < self.MAX_LEVEL:
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
        return int(100 * (1.5 ** (self.getLevel()))) # Current formula TODO change: 100 * 1.5^level.

    def getInfo(self):
        """
        Returns character info
        """
        # TODO maybe this can just be generalised??? idk it's only useful for saving so do it later.
        pass