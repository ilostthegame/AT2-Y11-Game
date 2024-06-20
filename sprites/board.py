import pygame
from tile import Tile

class Board(pygame.sprite.Sprite):
    """
    Class that represents the game board sprite. 

    Attributes:
        surf (pygame.Surface)
        rect (pygame.Rect)
        tile_dict (dict[tuple[int, int], Tile])
    
    
    """
