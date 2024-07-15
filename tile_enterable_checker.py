from sprites.tile import Tile

class TileEnterableChecker:
    """
    Class containing methods for:
        - Determining all obstructed coordinates in a board.
        - Checking whether a singular tile is enterable.
    """

    def getObstructedCoords(self,
                           coords_to_tile: dict[tuple[int, int], Tile],
                           obstruction_entity_types: list[str]) -> list[tuple[int, int]]:
        """Determines all obstructed coordinates in a board.

        Given obstructed_entity_types, determines which coordinates within
        coords_to_tile can be entered by an entity.
        """
        obstructed_coords = list()
        for coords, tile in coords_to_tile.items():
            if tile.getAccessible() == False: # inaccessible tiles
                obstructed_coords.append(coords)
            elif tile.getOccupiedBy() in obstruction_entity_types: # tiles obstructed by entities
                obstructed_coords.append(coords)
        return obstructed_coords


    def checkTileEnterable(self, 
                           coords_to_tile: dict[tuple[int, int], Tile],
                           obstructed_coords: list[tuple[int, int]],
                           coords_to_check: tuple[int, int]) -> bool:
        """Checks whether a single tile is enterable.

        Checks the coords_to_check, to see if it fulfils the following conditions:
            - Is in the set of coordinates defined by the board.
            - Is not in obstructed_coords.

        Returns True if the coords fulfil these conditions, else returns False
        """

        if coords_to_check not in coords_to_tile.keys() or coords_to_check in obstructed_coords:
            return False
        return True
    

    