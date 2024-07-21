from game import Game
import pygame
from assets import GAME_ASSETS, load_assets
from testing.test_pathfinder import testPathfinder
from testing.test_in_range import testInRange

if __name__ == "__main__":
    load_assets()
    pygame.init()

    # game = Game('game_world', True)
    # game.runMainLoop()

    # # Pathfinder testing.
    # pygame.display.set_mode((100, 100))
    # testPathfinder()

    # Attack inRange() testing
    pygame.display.set_mode((100, 100))
    testInRange()