from game import Game
import pygame
from assets import GAME_ASSETS, load_assets
from testing.test_pathfinder import testPathfinder

if __name__ == "__main__":
    load_assets()
    pygame.init()

    # testPathfinder()

    game = Game('game_world', True)
    game.runMainLoop()