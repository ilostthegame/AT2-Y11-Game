from typing import Optional
from movement_helper_funcs import getObstructedCoords, checkTileEnterable, getDestinationCoords
from sprites.tile import Tile

class Pathfinder:
    """Class containing methods that facilitate a pathfinding algorithm."""

    def findPath(self,
                 coords_to_tile: dict[tuple[int, int], Tile],
                 obstruction_entity_types: list[str],
                 starting_coords: tuple[int, int],
                 target_coords: tuple[int, int]) -> list[str]:
        """Main pathfinding method - finds path between starting_coords and target_coords.

        Returns the shortest path to get to the character, as a list containing movement directions in order.
        If no path exists, returns string 'path not found'.

        obstruction_entity_types is the list of entity types to be treated as obstructions:
        If for example, 'enemy' is not included, the algorithm will allow enemies to be part of the path.
        """

        obstructed_coords = getObstructedCoords(coords_to_tile, obstruction_entity_types)
        coords_to_path = {starting_coords: []} # Dictionary to track found paths.
        num_iterations = 0

        # Iterates pathfinding algorithm until either the target coords have been found 
        # or no new tiles are found.
        while target_coords not in coords_to_path.keys():
            num_found_tiles = len(coords_to_path.keys())
            new_coords_to_path = coords_to_path.copy()
            # Iterates through all existing coords.
            # If a tile was found the previous iteration (its path length equals the number of iterations), 
            # then check the tiles adjacent to it, to add to new_coords_to_path.
            for coords, path in coords_to_path.items():
                if len(path) == num_iterations: 
                    self.findAdjacentPaths(coords_to_tile, new_coords_to_path, coords, target_coords, obstructed_coords)
            coords_to_path = new_coords_to_path
            # If no new tiles have been found, break.
            new_num_found_tiles = len(coords_to_path.keys())
            if new_num_found_tiles == num_found_tiles:
                break
            num_iterations += 1
        
        # Checks whether target coords have been found. 
        if target_coords in coords_to_path.keys():
            return coords_to_path[target_coords]
        else:
            return 'path not found'
        
    def findAdjacentPaths(self,
                          coords_to_tile: dict[tuple[int, int], Tile],
                          coords_to_path: dict[tuple[int, int], Tile], 
                          root_coords: tuple[int, int], 
                          target_coords: tuple[int, int],
                          obstructed_coords: list[tuple[int, int]]) -> None:
        """Intermediate step in the pathfinding algorithm which checks adjacent coords to root_coords.
        
        Checks for the following condition:
            The coords must either be the target_coords, or be enterable,
            and cannot already be in coords_to_path (hasn't previously been found by the algorithm).
        If these are fulfilled, the new coords and the path leading to it are added to coords_to_path.
        """
        path_to_root = coords_to_path[root_coords]
        direction_list = ['right', 'left', 'up', 'down']

        for direction in direction_list:
            dest_coords = getDestinationCoords(root_coords, direction)
            # Checks destination coords for the condition specified in docstring.
            if (    dest_coords == target_coords or
                    checkTileEnterable(coords_to_tile, obstructed_coords, dest_coords) and
                    dest_coords not in coords_to_path.keys()):
                # Creates the new path leading to that tile, and adds it to coords_to_path
                new_path = path_to_root.copy()
                new_path.append(direction)
                coords_to_path[dest_coords] = new_path