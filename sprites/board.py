import pygame
from sprites.tile import Tile

class Board(pygame.sprite.Sprite):
    """
    Class that represents the game board sprite. 

    Attributes:
        surf (pygame.Surface)
        position_tile_dict (dict[tuple[int, int], Tile]): Dictionary that relates coordinate tuples to Tiles 
            {(xcoord, ycoord): Tile})
    
    Can copy() to get a new game board to blit all sprites upon.
    Can probably do that in GameWorld.

    Methods:
    drawBoardSurface(self): 
        Using position_tile_dict, draws tiles onto board_surf
    
    """

    # Attributes
    __surf = None
    __position_tile_dict = None

    # Constructor
    def __init__(self):
        super().__init__()
        self.setSurf(pygame.Surface((768, 768)))
        self.setPositionTileDict(dict())

    # Getters
    def getSurf(self):
        return self.__surf
    def getPositionTileDict(self):
        return self.__position_tile_dict

    # Setters
    def setSurf(self, surf):
        self.__surf = surf
    def setPositionTileDict(self, position_tile_dict):
        self.__position_tile_dict = position_tile_dict

    # Methods
    def drawBoardSurface(self):
        """
        Using position_tile_dict, draws tiles onto surf
        """
        position_tile_dict = self.getPositionTileDict()
        board_surf = self.getSurf()
        # Iterating through all xcoord, ycoord and tile_type, and drawing onto board_surf
        for xcoord, ycoord in position_tile_dict.keys():
            tile = position_tile_dict[(xcoord, ycoord)]
            #pygame.draw.rect(board_surf, tile.getColour(), (xcoord*64, ycoord*64, 64, 64))
            board_surf.blit(tile.getSurf(), (xcoord*64, ycoord*64, 64, 64))

        self.setSurf(board_surf)
        


