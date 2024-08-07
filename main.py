from game import Game
import pygame
from assets import GAME_ASSETS, load_assets
from testing.test_pathfinder import testPathfinder
from testing.test_in_range import testInRange

# NOTE to user: Refer to Github repository README for a guide/controls for game.

if __name__ == "__main__":
    load_assets()
    pygame.init()

    game = Game('title_screen', True)
    game.runMainLoop()

    # # Pathfinder testing.
    # pygame.display.set_mode((100, 100))
    # testPathfinder()

    # Attack inRange() testing
    # pygame.display.set_mode((100, 100))
    # testInRange()