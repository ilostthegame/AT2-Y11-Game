import pygame
from sprites.active_entity import ActiveEntity
from pygame.locals import *
from assets import GAME_ASSETS
from sprites.healthbar import Healthbar
from sprites.weapon import Weapon
from attack import Attack
from typing import Any, Optional
from sprites.tile import Tile
from sprites.npc import Npc
from sprites.portal import Portal
from sprites.entity import Entity
from movement_helper_funcs import getObstructedCoords, checkTileEnterable, getDestinationCoords
from sprites.quest_item import QuestItem

class Character(ActiveEntity):
    """Class representing a character entity.

    Attributes:
        (Inherited)
        surf (pygame.Surface): Pygame surface for the entity, onto which to 
                               blit the entity image, weapon and healthbar.
            Size: 64 x 64, transparent.
        rect (pygame.Rect): Rectangle representing entity's position
        image (pygame.Surface): Surface representing entity's sprite image.
            Size: 32 x 48, transparent.
        name (str): Name of character.
        strength (int): Strength stat.
        defence (int): Defence stat.
        max_health (int): Maximum health stat.
        health (int): Current health stat.
        weapon (Weapon): Currently held weapon.
        is_alive (bool): Whether entity is alive: health above 0 or not.
        xcoord (int): X coordinate of entity in world.
        ycoord (int): Y coordinate of entity in world.
        healthbar (Healthbar): Healthbar of entity.

        level (int): Current level of character.
        exp (int): Exp stat.
        selected_attack (Optional[Attack]): The currently selected attack
        enemies_in_range (list[Optional[Enemy]]): The list of enemies in range
            of the currently selected attack (empty when no attack selected).
        health_regen (int): How much health regenerates each turn.
        quest_item_names (set[str]): Set of owned quest items' names
    """
    
    # Attributes
    __level = None
    __exp = None
    __selected_attack = None
    __enemies_in_range = None
    __health_regen = None
    __quest_item_names = None

    # Constructor
    def __init__(self,  # TODO all of this stuff should not be optional arguments. 
                        # Leave this for temporary testing before world_init is added.
                 image: pygame.Surface, 
                 name: str,
                 weapon_id: str, 
                 strength: int = 25, 
                 defence: int = 25, 
                 max_health: int = 100000, 
                 health: int = 100000, 
                 is_alive: bool = True, 
                 xcoord: int = 0, 
                 ycoord: int = 0, 
                 level: int = 1, 
                 exp: int = 0,
                 health_regen: int = 10000):
        super().__init__(image, name, strength, defence, max_health, health,
                         Weapon(weapon_id, xcoord, ycoord),
                         is_alive, xcoord, ycoord, Healthbar(health, max_health)) 
        self.setLevel(level)
        self.setExp(exp)
        self.setSelectedAttack(None)
        self.setEnemiesInRange([])
        self.setHealthRegen(health_regen)
        self.setQuestItemNames(set())

    # Getters
    def getLevel(self) -> int:
        return self.__level
    def getExp(self) -> int:
        return self.__exp
    def getSelectedAttack(self) -> Attack:
        return self.__selected_attack
    def getEnemiesInRange(self) -> list:
        return self.__enemies_in_range
    def getHealthRegen(self) -> int:
        return self.__health_regen
    def getQuestItemNames(self) -> set[str]:
        return self.__quest_item_names
    
    # Setters
    def setLevel(self, level):
        self.__level = level
    def setExp(self, exp):
        self.__exp = exp
    def setSelectedAttack(self, selected_attack):
        self.__selected_attack = selected_attack
    def setEnemiesInRange(self, enemies_in_range):
        self.__enemies_in_range = enemies_in_range
    def setHealthRegen(self, health_regen):
        self.__health_regen = health_regen
    def setQuestItemNames(self, quest_item_names):
        self.__quest_item_names = quest_item_names

    def moveOrInteract(self,
                       direction: str, 
                       coords_to_tile: dict[tuple[int, int], Tile],
                       num_enemies: int) -> Optional[str] | False:
        """Attempts to move/interact in the specified direction.

        If the tile cannot be entered:
            Return False.
        If the tile contains an Npc:
            Returns the Npc's message.
        If the tile contains a Portal:
            If num_enemies == 0, set the portal's is_activated to True. 
                Return a success message.
            Else, return an error message.
        If the tile is completely unoccupied:
            Move to the tile. Returns None
        """
        current_coords = (self.getXcoord(), self.getYcoord())
        destination_coords = getDestinationCoords(current_coords, direction)
        # Checking whether the destination coordinates is either obstructed 
        # by a wall, by an enemy, or is not on the board.
        obstructed_coords = getObstructedCoords(coords_to_tile, (ActiveEntity))
        is_enterable = checkTileEnterable(coords_to_tile, obstructed_coords, destination_coords)
        if not is_enterable:
            return False
        # Handling the destination tile being occupied by different entities.
        occupying_entity = coords_to_tile[destination_coords].getOccupiedBy()
        # If occupied by Npc, return its message.
        if isinstance(occupying_entity, Npc):
            message = f"{occupying_entity.getName()} says: '{occupying_entity.getDialogue()}'"
            return message
        # If occupied by Portal, attempt to enter the portal
        elif isinstance(occupying_entity, Portal):
            event = occupying_entity.handleEnterAttempt(num_enemies, self.getQuestItemNames())
            return event
        # If occupied by a Quest Item, obtain the quest item.
        elif isinstance(occupying_entity, QuestItem):
            # If already owned, return error message.
            if occupying_entity.getName() in self.getQuestItemNames():
                event = (f"You already have a {occupying_entity.getName()}. "
                          "Leave some for other adventurers.")
            else:
                # Adds to owned quest items.
                event = f"You picked up the {occupying_entity.getName()}"
                self.getQuestItemNames().add(occupying_entity.getName()) 
                # Removes quest item from board.
                coords_to_tile[destination_coords].setOccupiedBy(None)
                occupying_entity.kill()
            return event
        # Tile is unobstructed and has no entities.
        else:
            # Sets own coordinates/screen position.
            self.setXcoord(destination_coords[0])
            self.setYcoord(destination_coords[1])
            self.updateRect()
            # Changes coords_to_tile to reflect movement.
            coords_to_tile[current_coords].setOccupiedBy(None)
            coords_to_tile[destination_coords].setOccupiedBy(self)
            return None

    def attack(self, enemy) -> Optional[list[str]] | False:
        """If enemy is in range, attacks them.
        
        Returns a list of events if the enemy was in range.
        Else if enemy not in range, returns False.
        """
        if enemy in self.getEnemiesInRange():
            events = self.useAttack(self.getSelectedAttack(), enemy)
            return events
        else:
            return False

    def calcEnemiesInRange(self, 
                           coords_to_tile: dict[tuple[int, int], Tile],
                           enemy_group: pygame.sprite.Group):
        """Sets enemies_in_range to a list of all enemies in range of selected attack."""
        enemies_in_range = []
        self_coords = (self.getXcoord(), self.getYcoord())
        selected_attack = self.getSelectedAttack()
        obstructed_coords = getObstructedCoords(coords_to_tile, Entity)
        for enemy in enemy_group:
            enemy_coords = (enemy.getXcoord(), enemy.getYcoord())
            if selected_attack.isInRange(self_coords, enemy_coords, obstructed_coords):
                enemies_in_range.append(enemy)
        self.setEnemiesInRange(enemies_in_range)

    def gainExp(self, exp) -> list[Optional[str]]:
        """Increases exp, and levels up if possible.

        Runs updateStats() for each level up.
        Returns a list of strings representing game events for level ups.
        """
        original_level = self.getLevel()
        self.setExp(self.getExp() + exp)
        required_exp = self.calcRequiredExp()
        events = []
        # Level up character while character has enough exp to level up.
        while self.getExp() >= required_exp:
            self.setLevel(self.getLevel() + 1)
            hp_incr, str_incr, def_incr = self.updateStats() # TODO TODO TODO make it so when enemy dies to lava 
            # character will also gain exp.
            events.append(f"Level up! +{hp_incr} Health! +{str_incr} Strength! "
                          f"+{def_incr} Defence!")
            self.setExp(self.getExp() - required_exp) # Subtract used exp.
            required_exp = self.calcRequiredExp() # Recalculate exp for next level.
        return events

    def updateStats(self) -> tuple[int, int, int]:
        """Updates max_health/health, attack, defence upon level up.

        Returns tuple (max_health_increase, strength_increase, defence_increase).
        """
        health_increase = 20
        strength_increase = 5
        defence_increase = 5
        self.setMaxHealth(self.getMaxHealth() + health_increase)
        self.setHealth(self.getHealth() + health_increase)
        self.setStrength(self.getStrength() + strength_increase)
        self.setDefence(self.getDefence() + defence_increase)
        return (health_increase, strength_increase, defence_increase)

    def calcRequiredExp(self):
        """Calculates total required exp to get to next level.""" 
        return int(10 * self.getLevel() ** 2) # TODO change formula - need one that is flatter at the start.
    
    def regenerate(self) -> None:
        """Regenerates health based on health_regen"""
        self.setHealth(self.getHealth() + self.getHealthRegen())