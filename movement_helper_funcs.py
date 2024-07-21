"""
Contains functions to facilitate ActiveEntity movement and pathfinding.
"""

# Imports
import pygame
from sprites.tile import Tile

# Functions
def getObstructedCoords(coords_to_tile: dict[tuple[int, int], Tile],
                        obstruction_entity_types: tuple[type]) -> list[tuple[int, int]]:
    """Determines all obstructed coordinates in a board.

    A tile is obstructed if it is not accessible, or
    contains an entity in obstruction_entity_types.
    """
    obstructed_coords = list()
    for coords, tile in coords_to_tile.items():
        if tile.getAccessible() == False:
            obstructed_coords.append(coords)
        elif isinstance(tile.getOccupiedBy(), obstruction_entity_types):
            obstructed_coords.append(coords)
    return obstructed_coords

def checkTileEnterable(coords_to_tile: dict[tuple[int, int], Tile],
                       obstructed_coords: list[tuple[int, int]],
                       coords_to_check: tuple[int, int]) -> bool:
    """Checks whether a single tile is enterable.

    If the coords_to_check fulfil the following conditions:
        - Is in the set of coordinates defined by the board.
        - Is not in obstructed_coords.
    Return True. Else, return False.
    """
    if coords_to_check not in coords_to_tile.keys() or coords_to_check in obstructed_coords:
        return False
    return True

def getDestinationCoords(current_coords: tuple[int, int],
                         direction: str) -> tuple[int, int]:
    """Determines the destination coords of a movement given its direction."""
    current_xcoord = current_coords[0]
    current_ycoord = current_coords[1]
    match direction:
        case 'right':
            new_coords = (current_xcoord+1, current_ycoord)
        case 'left':
            new_coords = (current_xcoord-1, current_ycoord)
        case 'up':
            new_coords = (current_xcoord, current_ycoord-1)
        case 'down':
            new_coords = (current_xcoord, current_ycoord+1)
        case _:
            raise ValueError(f"({direction}) is not a valid direction")
    return new_coords

