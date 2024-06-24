from game import Game
import pygame
from assets import GAME_ASSETS, load_assets


if __name__ == "__main__":
    load_assets()
    pygame.init()
    game = Game('game_world', True)
    game.run()