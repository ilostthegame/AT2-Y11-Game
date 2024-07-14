import pygame
import random
from file_id_interpreter import FileIdInterpreter
from sprites.active_entity import ActiveEntity
from assets import GAME_ASSETS, load_assets
from sprites.healthbar import Healthbar
from sprites.weapon import Weapon
from sprites.character import Character
from sprites.tile import Tile
from sprites.portal import Portal
from sprites.npc import Npc
from typing import Optional, Union
from pathfinder import Pathfinder
from tile_enterable_checker import TileEnterableChecker

class Enemy(ActiveEntity):
    """
    Class representing an enemy sprite, with parent ActiveEntity

    Attributes:
        (Inherited)
        surf (pygame.Surface): Pygame surface for the entity, onto which to blit the entity image, weapon and healthbar.
            Size: 64 x 64, transparent.
        image (pygame.Surface): Surface representing entity's sprite image. 
            Size: 32 x 48, transparent
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
        exp_yield (int): Represents how much exp is earned through defeating enemy
    
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

        (Movement/pathfinding methods)
        moveToCharacter(self, coords_to_tile: dict[tuple[int, int], Tile]) -> None:
            Main movement method to be called: moves enemy towards character.
        getCharacterCoords(self, coords_to_tile: dict[tuple[int, int], Tile]) -> Optional[tuple[int, int]]:
            Returns the coordinates of character if they are found in coords_to_tile, else returns None.
        moveInDirection(self, direction: str, coords_to_tile: dict[tuple[int, int], Tile]) -> None:
            Given a direction, if the tile in that direction is unoccupied, moves there.
    """

    # Attributes
    __movement_pattern = None
    __exp_yield = None

    # Constructor
    def __init__(self, enemy_id: str, xcoord: int, ycoord: int):
        # Getting file info
        # Attributes in attribute_list = [image, name, attack, defence, health, health_regen, weapon_id, movement_pattern, exp_yield]
        attribute_list = FileIdInterpreter().interpretFileInfo('gameinfostorage/enemy_id.txt', enemy_id) 
        
        # Unpacking file info, and creating additional enemy attributes
        image_name, name, attack, defence, health, health_regen, weapon_id, movement_pattern, exp_yield = attribute_list # unpacks attribute_list
        attack, defence, health, health_regen, exp_yield = [int(i) for i in (attack, defence, health, health_regen, exp_yield)] # converts some attributes to integers
        weapon = Weapon(weapon_id, xcoord, ycoord) # creates weapon object enemy is wielding
        healthbar = Healthbar(health, health) # creates healthbar object attached to enemy
    
        # Initialising enemy object. Note that health variable is used to set both max_health and health.
        super().__init__(pygame.image.load(GAME_ASSETS[image_name]).convert_alpha(), # enemy image
                         name, attack, defence, health, health, health_regen, weapon, True, xcoord, ycoord, healthbar)
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
               character: Character, 
               enemy_group: pygame.sprite.Group, 
               npc_group: pygame.sprite.Group, 
               portal_group: pygame.sprite.Group, 
               coords_to_tile: dict[tuple[int, int], Tile]) -> list[str]:
        """
        Runs a single turn's action for the enemy.
        Returns a list of game events done by the enemy.
        """
        pass
        # Get character's position

        # Get a list of inaccessible tiles (these can't be fired over either)

        # Calculate whether character is in range of any attack in randomised order. If so, then do attack.
        # Else, calculate potential movements based on movement pattern.


    def moveToCharacter(self, coords_to_tile: dict[tuple[int, int], Tile]) -> None:
        """
        Main movement method to be called: moves enemy towards character.

        First attempts to find a path between enemy and character that doesn't pass through other enemies.
        If impossible, then attempts to find a path between enemy and character that can pass through other enemies.
        NOTE: The reasoning for this implementation is so that even if an enemy's path to the character is blocked by 
        other enemies, it will still keep moving to the character, based on an optimal situation without other enemies.

        Moves according to the first path found (using moveInDirection()).
        Else if no path was found in either of these attempts, raises an Exception.
        """
    
        pathfinder = Pathfinder()
        self_coords = (self.getXcoord(), self.getYcoord())
        character_coords = self.getCharacterCoords()
        # Finds path which doesn't pass through other enemies
        path = pathfinder.findPath(coords_to_tile, ['character', 'enemy', 'npc', 'portal'], self_coords, character_coords)
        # If no such path, finds a path which can pass through other enemies
        if path == None:
            path = pathfinder.findPath(coords_to_tile, ['character', 'enemy', 'npc', 'portal'], self_coords, character_coords)
        # If no path found still, raises an Exception.
        if path == None:
            raise Exception('Path cannot be found between enemy and player')
        else: 
            self.moveInDirection(path[0], coords_to_tile)
        return
    
    def getCharacterCoords(self, coords_to_tile) -> Optional[tuple[int, int]]:
        """
        Returns the coordinates of character if they are found in coords_to_tile, else returns None.
        """
        for coords, tile in coords_to_tile.items():
            if tile.getOccupiedBy() == 'character':
                return coords
        return

    def moveInDirection(self, direction: str, coords_to_tile: dict[tuple[int, int], Tile]) -> None:
        """
        Given a direction, if the tile in that direction is unoccupied, moves there.
        Returns True if the movement was successful, else returns False.
        """
        
        # Gets the new coordinates of the movement.
        current_xcoord = self.getXcoord()
        current_ycoord = self.getYcoord()
        match direction:
            case 'right':
                new_coords = (current_xcoord + 1, current_ycoord)
            case 'left':
                new_coords = (current_xcoord + 1, current_ycoord)
            case 'up':
                new_coords = (current_xcoord + 1, current_ycoord)
            case 'down':
                new_coords = (current_xcoord + 1, current_ycoord)
            case _:
                raise ValueError(f"({direction}) is not a valid direction")
        
        # Checking whether the new coordinates can be entered
        tile_enterable_checker = TileEnterableChecker()
        obstructed_coords = tile_enterable_checker.getObstructedCoords(coords_to_tile, ['enemy', 'character', 'npc', 'portal'])
        is_enterable = tile_enterable_checker.checkTileEnterable(coords_to_tile, obstructed_coords, new_coords)
        if is_enterable: # If enterable, change enemy's coordinates.
            self.setXcoord(new_coords[0])
            self.setYcoord(new_coords[1])
        return

    def getInfo(self):
        pass