import pygame
from sprites.tile import Tile

class Board(pygame.sprite.Sprite):
    """
    Class that represents the game board sprite. 

    Attributes:
        surf (pygame.Surface): Surface representing board. Size: 768 x 768
        coords_to_tile (dict[tuple[int, int], Tile]): Dictionary that relates coordinate tuples to Tiles 
            {(xcoord, ycoord): Tile})

    Methods:
    drawBoardSurface(self) -> None: 
        Using coords_to_tile, draws tiles onto board_surf
    """

    # Attributes
    __surf = None
    __coords_to_tile = None

    # Constructor
    def __init__(self):
        super().__init__()
        self.setSurf(pygame.Surface((768, 768)))
        self.setCoordsToTile(dict())

    # Getters
    def getSurf(self):
        return self.__surf
    def getCoordsToTile(self):
        return self.__coords_to_tile
    def getTileGroup(self):
        return self.__tile_group

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setCoordsToTile(self, coords_to_tile):
        self.__coords_to_tile = coords_to_tile

    # Methods
    def drawBoardSurface(self) -> None:
        """
        Using coords_to_tile dictionary, draws tiles onto surf
        """
        coords_to_tile = self.getCoordsToTile()
        board_surf = self.getSurf()
        # Iterating through all xcoord, ycoord and tile_type, and drawing onto board_surf
        for xcoord, ycoord in coords_to_tile.keys():
            tile = coords_to_tile[(xcoord, ycoord)]
            board_surf.blit(tile.getSurf(), (xcoord*64, ycoord*64, 64, 64))
            
        self.setSurf(board_surf)
        return
        