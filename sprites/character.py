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

class Character(ActiveEntity):
    """Class representing a character entity.

    Attributes:
        (Inherited)
        surf (pygame.Surface): Pygame surface for the entity, onto which to blit the entity image, weapon and healthbar.
            Size: 64 x 64, transparent.
        image (pygame.Surface): Surface representing entity's sprite image.
            Size: 32 x 48, transparent.
        name (str): Name of character.
        strength (int): Strength stat.
        defence (int): Defence stat.
        max_health (int): Maximum health stat.
        health (int): Current health stat.
        health_regen (int): How much health regenerates each turn.
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
    """
    
    # Attributes
    __level = None
    __exp = None
    __selected_attack = None
    __enemies_in_range = None

    # Constructor
    def __init__(self,  # TODO all of this stuff should not be optional arguments. 
                        # Leave this for temporary testing before world_init is added.
                 image: pygame.Surface, 
                 name: str,
                 weapon_id: str, 
                 strength: int = 25, 
                 defence: int = 25, 
                 max_health: int = 100, 
                 health: int = 100, 
                 health_regen: int = 2,
                 is_alive: bool = True, 
                 xcoord: int = 0, 
                 ycoord: int = 0, 
                 level: int = 1, 
                 exp: int = 0):
        super().__init__(image, name, strength, defence, max_health, health, health_regen, 
                         Weapon(weapon_id, xcoord, ycoord),
                         is_alive, xcoord, ycoord, Healthbar(health, max_health)) 
        self.setLevel(level)
        self.setExp(exp)
        self.setSelectedAttack(None)
        self.setEnemiesInRange([])

    # Getters
    def getLevel(self) -> int:
        return self.__level
    def getExp(self) -> int:
        return self.__exp
    def getSelectedAttack(self) -> Attack:
        return self.__selected_attack
    def getEnemiesInRange(self):
        return self.__enemies_in_range
    
    # Setters
    def setLevel(self, level):
        self.__level = level
    def setExp(self, exp):
        self.__exp = exp
    def setSelectedAttack(self, selected_attack):
        self.__selected_attack = selected_attack
    def setEnemiesInRange(self, enemies_in_range):
        self.__enemies_in_range= enemies_in_range

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
        occupying_entity = coords_to_tile[destination_coords].getOccupiedBy()
        # If occupied by Npc, return its message.
        if isinstance(occupying_entity, Npc):
            message = f"{occupying_entity.getName()}: '{occupying_entity.getDialogue}'"
            return list(message)
        # If occupied by Portal, either move onto portal, or return error message.
        elif occupying_entity == Portal:
            if num_enemies == 0:
                occupying_entity.setIsActivated(True)
                return list("You entered the portal! You feel yourself being teleported.")
            else:
                return list("You try to enter the portal, but there are still enemies remaining.")
        # Tile is unobstructed and has no entities.
        else:
            self.setXcoord(destination_coords[0])
            self.setYcoord(destination_coords[1])
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
                           enemy_group: pygame.sprite.Group) -> list:
        """Returns a list of all enemies in range of selected attack."""
        enemies_in_range = []
        self_coords = (self.getXcoord(), self.getYcoord())
        selected_attack = self.getSelectedAttack()
        obstructed_coords = getObstructedCoords(coords_to_tile, Entity)
        for enemy in enemy_group:
            enemy_coords = (enemy.getXcoord(), enemy.getYcoord())
            if selected_attack.isInRange(self_coords, enemy_coords, obstructed_coords):
                enemies_in_range.append(enemy)
        return enemies_in_range

    def gainExp(self, exp): # TODO make this have game event
        """
        Increases character's exp, and increases levels accordingly. Subtracts used exp.
        Runs stat increase method based on levels gained.
        """
        original_level = self.getLevel()
        self.setExp(self.getExp() + exp)
        required_exp = self.calcRequiredExp() # Calculate exp required for next level

        # Level up character while character has enough exp to level up and is below the level cap (50).
        while self.getExp() >= required_exp and self.getLevel() < 50:
            self.setLevel(self.getLevel() + 1)
            self.setExp(self.getExp() - required_exp) # subtract used exps.
            required_exp = self.calcRequiredExp() # Re-calculate exp required for next level

        # Update attack/defence and if levelled up, prints levelup info.
        level_increase = self.updateStats(original_level)
        # TODO

    def updateStats(self, original_level):
        """Updates attack, defence based on change in level.

        Returns tuple (level_increase, attack_increase, defence_increase)
        """
        level_increase = self.getLevel() - original_level
        attack_increase = level_increase * 2
        defence_increase = level_increase * 2
        self.setAttack(self.getAttack() + attack_increase)
        self.setDefence(self.getDefence() + defence_increase)
        return (level_increase, attack_increase, defence_increase)

    def calcRequiredExp(self):
        """
        Calculates total required exp to get to next level
        """ 
        return int(100 * (1.5 ** (self.getLevel())))  # Current formula TODO change: 100 * 1.5^level.