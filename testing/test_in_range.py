from level_initialiser import LevelInitialiser
from movement_helper_funcs import getObstructedCoords
from attack import Attack
from sprites.character import Character
from sprites.npc import Npc
from sprites.portal import Portal
from sprites.enemy import Enemy
import pygame
from assets import GAME_ASSETS

def testInRange():
    """Testing Attack class's inRange() method, using LevelInitialiser and MovementHelperFuncs.
    
    To use:
    Set the level name for getLevelContents(), and desired attack ID in Attack object initialisation.
    Set parameters for attack isInRange().
    """
    level_initialiser = LevelInitialiser()
    attack = Attack('Co')
    character = Character(pygame.image.load(GAME_ASSETS['blue_orb']), 'Bob', "WC")

    # Initialising level and getting board information.
    contents = level_initialiser.getLevelContents('Music Centre 2', character)
    board = contents[0]
    coords_to_tile = board.getCoordsToTile()
    # Gets obstructed_coords
    obstructed_coords = getObstructedCoords(coords_to_tile, (Character,Npc,Portal,Enemy))
    # Testing attack inRange()
    result = attack.isInRange((0, 0), (11,3), obstructed_coords)
    print(result)
