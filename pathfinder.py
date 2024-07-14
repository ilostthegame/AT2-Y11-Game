from typing import Optional
from tile_enterable_checker import TileEnterableChecker
from sprites.tile import Tile

class Pathfinder:
    """
    Class containing methods that facilitate a pathfinding algorithm.

    Methods:
        findPath(self,
                 coords_to_tile: dict[tuple[int, int], Tile],
                 obstruction_entity_types: list[str],
                 starting_coords: tuple[int, int],
                 target_coords: tuple[int, int]) -> Optional[list[str]]:
            Returns the shortest path to get to the character, as a list containing movement directions in order.
            If no path exists, returns None.
        
        findAdjacentPaths(self,
                          coords_to_tile: dict[tuple[int, int], Tile],
                          coords_to_path: dict[tuple[int, int], Tile], 
                          root_coords: tuple[int, int], 
                          target_coords: tuple[int, int],
                          obstructed_coords: list[tuple[int, int]]) -> dict[tuple[int, int], Tile]:
            Intermediate step in the pathfinding algorithm: given root_coords, this checks each
            adjacent coords, and if they fulfil certain validity conditions, adds them to coords_to_path.
            Returns the updated coords_to_path dictionary.
    """

    def findPath(self,
                 coords_to_tile: dict[tuple[int, int], Tile],
                 obstruction_entity_types: list[str],
                 starting_coords: tuple[int, int],
                 target_coords: tuple[int, int]) -> Optional[list[str]]:
        """
        Returns the shortest path to get to the character, as a list containing movement directions in order.
        If no path exists, returns None.

        obstruction_entity_types is the list of entity types to be treated as obstructions:
        If for example, 'enemy' is not included, the algorithm will allow enemies to be part of the path.
        """

        # Gets obstructed coords.
        tile_enterable_checker = TileEnterableChecker()
        obstructed_coords = tile_enterable_checker.getObstructedCoords(coords_to_tile, obstruction_entity_types)
        # Initialises the pathfinding dictionary. Begins with the starting coords with an empty list.
        coords_to_path = {starting_coords: []} # Relates each tuple of coords to the shortest path to them.
        num_iterations = 0

        # Iterates pathfinding algorithm until either target coords
        # have been found or no new tiles are found in an iteration.
        while target_coords not in coords_to_path.keys():
            # Number of tiles that have been found by algorithm so far.
            num_found_tiles = len(coords_to_path.keys()) 
            # If a tile's coordinates was only found the previous iteration (its path length
            # is equal to the number of iterations), then check the tiles adjacent to it.
            for coords, path in coords_to_path.items():
                if len(path) == num_iterations: 
                    coords_to_path = self.findAdjacentPaths(coords_to_tile, coords_to_path, coords, target_coords, obstructed_coords)
            # If no new tiles have been found, break.
            new_num_tiles = len(coords_to_path.keys())
            if new_num_tiles == num_found_tiles:
                break
            num_iterations += 1
        
        # Checks whether target coords have been found. 
        # If so, returns the path leading to it. If not, returns None.
        if target_coords in coords_to_path.keys():
            return coords_to_path[target_coords]
        else:
            return None
        
    def findAdjacentPaths(self,
                          coords_to_tile: dict[tuple[int, int], Tile],
                          coords_to_path: dict[tuple[int, int], Tile], 
                          root_coords: tuple[int, int], 
                          target_coords: tuple[int, int],
                          obstructed_coords: list[tuple[int, int]]) -> dict[tuple[int, int], Tile]:
        """
        Intermediate step in the pathfinding algorithm: given root_coords, this checks each
        adjacent coords for the following condition:
            If must either be the target_coords or be enterable (by checkTileEnterable()), 
            and cannot already be in coords_to_path (hasn't previously been found by the algorithm).
        If these are fulfilled, the new coords and the path leading to it are added to coords_to_path.

        Returns the updated coords_to_path dictionary.
        """

        root_xcoord, root_ycoord = root_coords[0], root_coords[1]
        path_to_root = coords_to_path[root_coords]
        # Dictionary that relates each adjacent tile's coords to
        # their direction from the root tile.
        adj_coords_to_direction = {
            (root_xcoord + 1, root_ycoord): 'right',
            (root_xcoord - 1, root_ycoord): 'left',
            (root_xcoord, root_ycoord + 1): 'up',
            (root_xcoord, root_ycoord - 1): 'down'
        }

        for coords_to_check in adj_coords_to_direction.keys():
            # Checks whether the coords are either the target_coords or are enterable,
            # and whether the coords are not already in coords_to_path.
            if (    coords_to_check == target_coords or
                    TileEnterableChecker().checkTileEnterable(coords_to_tile, obstructed_coords, coords_to_check) and
                    coords_to_check not in coords_to_path.keys()):
                # Creates the new path leading to that tile, and adds it to coords_to_path
                new_path = path_to_root.copy()
                new_path.append(adj_coords_to_direction[coords_to_check])
                coords_to_path[coords_to_check] = new_path
        
        return coords_to_path
