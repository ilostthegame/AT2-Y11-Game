from level_initialiser import LevelInitialiser
from pathfinder import Pathfinder

def testPathfinder():
    """Testing the pathfinder."""
    level_initialiser = LevelInitialiser()
    pathfinder = Pathfinder()

    # Initialising level
    contents = level_initialiser.getLevelContents('Music Centre 1')
    board = contents[0]
    coords_to_tile = board.getCoordsToTile()
    path = pathfinder.findPath(coords_to_tile, 
                        ['character', 'portal', 'npc'],
                        (0,0),
                        (5,5))
    
    print(path)
