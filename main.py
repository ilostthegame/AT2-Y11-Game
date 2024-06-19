from game import Game

# Constants
SCREEN_SIZE = (1200, 800)


if __name__ == "__main__":
    game = Game(SCREEN_SIZE, 'title_screen', True)
    game.run() # Run the game