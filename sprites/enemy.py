import pygame
from random import shuffle
from file_id_interpreter import FileIdInterpreter
from sprites.active_entity import ActiveEntity
from assets import GAME_ASSETS
from sprites.healthbar import Healthbar
from sprites.weapon import Weapon
from sprites.tile import Tile
from sprites.portal import Portal
from sprites.npc import Npc
from typing import Optional, Union
from pathfinder import Pathfinder
from attack import Attack
from movement_helper_funcs import getObstructedCoords, checkTileEnterable, getDestinationCoords

class Enemy(ActiveEntity):
    """Class representing an enemy entity.

    Attributes:
        (Inherited)
        surf (pygame.Surface): Pygame surface for the enemy, onto which 
                               to blit the enemy image, weapon and healthbar.
            Size: 64 x 64, transparent.
        image (pygame.Surface): Surface representing enemy's sprite image. 
            Size: 32 x 48, transparent
        name (str): Name of enemy
        strength (int): Strength stat
        defence (int): Defence stat
        max_health (int): Maximum health stat
        health (int): Current health stat
        health_regen (int): How much health regenerates each turn
        weapon (Weapon): Currently held weapon
        is_alive (bool): Whether entity is alive: health above 0 or not
        xcoord (int): X coordinate of entity in world
        ycoord (int): Y coordinate of entity in world
        healthbar (Healthbar): Healthbar of entity

        movement_pattern (str): Represents the algorithm used for movement.
            In ['stationary', 'direct', TODO 'random']
        exp_yield (int): Represents how much exp is earned through defeating enemy
    """

    # Attributes
    __movement_pattern = None
    __exp_yield = None

    # Constructor
    def __init__(self, enemy_id: str, xcoord: int, ycoord: int):
        attribute_list = FileIdInterpreter().interpretFileInfo('gameinfostorage/enemy_id.txt', enemy_id) 
        
        # Unpacking attribute_list, and creating additional enemy attributes
        image_name, name, strength, defence, health, health_regen, weapon_id, movement_pattern, exp_yield = attribute_list 
        strength, defence, health, health_regen, exp_yield = [int(i) for i in (strength, defence, health, health_regen, exp_yield)]
        weapon = Weapon(weapon_id, xcoord, ycoord)
        healthbar = Healthbar(health, health)
    
        # Initialising enemy object. Note that health variable is used for both max_health and health.
        super().__init__(pygame.image.load(GAME_ASSETS[image_name]).convert_alpha(), # enemy image
                         name, strength, defence, health, health, health_regen, weapon, True, xcoord, ycoord, healthbar)
        self.setMovementPattern(movement_pattern)
        self.setExpYield(exp_yield)

    # Getters
    def getMovementPattern(self):
        return self.__movement_pattern
    def getExpYield(self):
        return self.__exp_yield

    # Setters
    def setMovementPattern(self, movement_pattern):
        self.__movement_pattern = movement_pattern
    def setExpYield(self, exp_yield):
        self.__exp_yield = exp_yield

    # Methods
    def action(self,
               character,
               coords_to_tile: dict[tuple[int, int], Tile]) -> Optional[list[str]]:
        """Runs a single turn's action for the enemy.

        Attempts to attack character. If all its attacks are out of range,
        then moves towards character.
        Returns a list of game events done by the enemy.
        """
        self_coords = (self.getXcoord(), self.getYcoord())
        character_coords = (character.getXcoord(), character.getYcoord())
        attacks = self.getShuffledAttacks() # randomised order attacks
        # Checks whether any attack is in range.
        # If so, perform the attack, and return its results.
        obstructed_coords = getObstructedCoords(coords_to_tile, (ActiveEntity,Npc,Portal))
        for attack in attacks:
            if attack.isInRange(self_coords, character_coords, obstructed_coords):
                events = self.useAttack(attack, character)
                return events
        # If no attack was in range, enemy does movement.
        if self.getMovementPattern() == 'direct':
            self.moveToCharacter(coords_to_tile, character_coords)
        return None

    def getShuffledAttacks(self) -> list[Attack]:
        """Returns a list containing enemy's attacks in random order"""
        attack_list = self.getWeapon().getAttackList()
        randomised_list = attack_list.copy()
        shuffle(randomised_list)
        return randomised_list

    def moveToCharacter(self, 
                        coords_to_tile: dict[tuple[int, int], Tile],
                        character_coords: tuple[int, int]) -> None:
        """Main movement method to be called: moves enemy towards character.

        First attempts to find a path between enemy and character that doesn't pass through other enemies.
        If impossible, then attempts to find a path between enemy and character that can pass through other enemies.
        NOTE: The reasoning for this implementation is so that even if an enemy's path to the character is blocked by 
        other enemies, it will still keep moving to the character, based on an optimal situation without other enemies.

        Moves according to the first path found (using moveInDirection()).
        Else if no path was found in either of these attempts, raises an Exception.
        """
        from sprites.character import Character

        pathfinder = Pathfinder()
        self_coords = (self.getXcoord(), self.getYcoord())
        # Finds path which doesn't pass through other enemies
        path = pathfinder.findPath(coords_to_tile, [Character,Enemy,Npc,Portal], self_coords, character_coords)
        # If no such path, finds a path which can pass through other enemies
        if path == None:
            path = pathfinder.findPath(coords_to_tile, [Character,Npc,Portal], self_coords, character_coords)
        # If no path found still, raises an Exception.
        if path == None:
            raise Exception('Path cannot be found between enemy and player')
        else: 
            self.move(path[0], coords_to_tile)
    
    def move(self, 
             direction: str, 
             coords_to_tile: dict[tuple[int, int], Tile]) -> None:
        """Moves enemy in the specified direction if the tile is enterable."""
        current_coords = (self.getXcoord(), self.getYcoord())
        destination_coords = getDestinationCoords(current_coords, direction)
        # Checking whether the destination coordinates can be entered.
        obstructed_coords = getObstructedCoords(coords_to_tile, (ActiveEntity,Npc,Portal))
        is_enterable = checkTileEnterable(coords_to_tile, obstructed_coords, destination_coords)
        if is_enterable:
            self.setXcoord(destination_coords[0])
            self.setYcoord(destination_coords[1])
            # Changes coords_to_tile to reflect movement.
            coords_to_tile[current_coords].setOccupiedBy(None)
            coords_to_tile[destination_coords].setOccupiedBy(self)
        return