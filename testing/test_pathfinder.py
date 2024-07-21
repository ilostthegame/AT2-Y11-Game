from level_initialiser import LevelInitialiser
from pathfinder import Pathfinder
from sprites.character import Character
from sprites.npc import Npc
from sprites.portal import Portal
from sprites.enemy import Enemy
import pygame
from assets import GAME_ASSETS

def testPathfinder():
    """Testing the Pathfinder class, using LevelInitialiser and MovementHelperFuncs.
    
    To use:
    Set the level name for getLevelContents(), and set the arguments for findPath().
    """
    level_initialiser = LevelInitialiser()
    pathfinder = Pathfinder()
    character = Character(pygame.image.load(GAME_ASSETS['blue_orb']), 'Bob', "WC")

    # Initialising level and getting board information.
    contents = level_initialiser.getLevelContents('Music Centre 1', character)
    board = contents[0]
    coords_to_tile = board.getCoordsToTile()
    # Finding path.
    path = pathfinder.findPath(coords_to_tile, 
                        [Character, Portal, Npc],
                        (0,0),
                        (5,5))
    print(path)
