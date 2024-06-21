import pygame
from game_states.game_state import GameState
from assets import GAME_ASSETS
from pygame.locals import *
from sprites.enemy import Enemy
from sprites.portal import Portal
from sprites.npc import Npc
from sidebar import Sidebar
from sprites.tile import Tile
from sprites.board import Board
from sprites.character import Character

class GameWorld(GameState):
    """
    Class representing the game world. Has parent GameState.
    Loaded from GameMenu? TODO (all state calcualations should occur in Game).

    Attributes:
        sidebar (Sidebar): In-game sidebar
        level_name (str): Name of the current level
    
        character (Character): Character sprite controlled by player
        board (Board): Board sprite - 11x11 grid of tiles.
        npc_group (pygame.sprite.Group): Group containing all npc sprites 
        enemy_group (pygame.sprite.Group): Group containing all enemy sprites
        portal_group (pygame.sprite.Group): Group containing all portal sprites

        (Inherited)
        displayed_sprites: Sprite group that represents all pygame sprites that are to be sent to display


    Methods:
        run(self, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> str: 
            Runs all functions associated with GameWorld. 
            To be called each iteration of game loop, while state == "game_world"
            Returns the next state game is to enter.

        Handler methods TODO

        (Initialiser methods)
        initialiseLevel(self) -> None: Initialises level tiles and entities
        parseLevelCode(self) -> list[tuple[str, int, int]]: Returns list of tuples each representing a tile's info: 
            (tile_code, xcoord, ycoord) - tile_code is X_X_XX string representing {tile_type}, {entity_type}, {entity_id}
        interpretTileInfo(self, tile_info): Interprets a single tile_info tuple.
            - tile information gets sent to Board object.
            - enemy/npc/portal information sent to their respective groups

    """

    # Attributes
    __sidebar = None
    __level_name = None
    __character = None
    __board = None
    __npc_group = None
    __enemy_group = None
    __portal_group = None

    # Constructor
    def __init__(self, 
                 level_name: str, 
                 character: Character, 
                 board: Board = Board(),
                 sidebar: Sidebar = 'placeholder',
                 npc_group: pygame.sprite.Group = pygame.sprite.Group(), 
                 enemy_group: pygame.sprite.Group = pygame.sprite.Group(), 
                 portal_group: pygame.sprite.Group = pygame.sprite.Group()):
        super().__init__()
        self.setLevelName(level_name)
        self.setCharacter(character)
        self.setBoard(board)
        self.setSidebar(sidebar)
        self.setNpcGroup(npc_group)
        self.setEnemyGroup(enemy_group)
        self.setPortalGroup(portal_group)
        self.initialiseLevel() # Initialise starting level

    # Getters
    def getSidebar(self):
        return self.__sidebar
    def getLevelName(self):
        return self.__level_name
    def getCharacter(self):
        return self.__character
    def getBoard(self):
        return self.__board
    def getNpcGroup(self):
        return self.__npc_group
    def getEnemyGroup(self):
        return self.__enemy_group
    def getPortalGroup(self):
        return self.__portal_group

    # Setters
    def setSidebar(self, sidebar):
        self.__sidebar = sidebar
    def setLevelName(self, level_name):
        self.__level_name = level_name
    def setCharacter(self, character):
        self.__character = character
    def setBoard(self, board):
        self.__board = board
    def setNpcGroup(self, npc_group):
        self.__npc_group = npc_group
    def setEnemyGroup(self, enemy_group):
        self.__enemy_group = enemy_group
    def setPortalGroup(self, portal_group):
        self.__portal_group = portal_group


    # Methods
    def run(self, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> str:
        """
        Runs all functions associated with GameWorld. 
            To be called each iteration of game loop, while state == "game_world"
            Returns the next state game is to enter.
        """

        # Pygame event handler



        # Use pygame.event == KEYDOWN to do stuff with one movement at a time.



    # Level initialisation methods.
    def initialiseLevel(self) -> None:
        """
        Initialises the level's tiles and entities.
        """
        tile_info = self.parseLevelCode()
        for tile in tile_info: # Iterates through all tuples
            self.interpretTileInfo(tile)
        
    def parseLevelCode(self) -> list[tuple[str, int, int]]:
        """
        Returns list of tuples each representing a tile's info: 
            (tile_code, xcoord, ycoord), where tile_code is X_X_XX string representing {tile_type}, {entity_type}, {entity_id}
        """
        str_to_find = '!!' + self.getLevelName() # marker string for the level code
        with open('gameinfostorage/world_gen.txt', 'r') as world_gen_file:
            file_lines = world_gen_file.readlines()

            # Find place where level code begins
            for pos, line in enumerate(file_lines):
                if str_to_find in line:
                    starting_pos = pos + 1 # position of line at which level code starts

                    # Splits the 11x11 grid code into components.
                    level_code_lines = [file_lines[starting_pos + i] for i in range(11)]
                    tile_info = [(tile_code, int(xcoord), int(ycoord)) for ycoord, code_line in enumerate(level_code_lines) for xcoord, tile_code in enumerate(code_line.split())]
                    return tile_info
            
            raise Exception(f"Level {self.getLevelName()} is not found")

    def interpretTileInfo(self, tile_info) -> None:
        """
        Interprets a single tile_info tuple.
            - tile information gets sent to Board object.
            - enemy/npc/portal information sent to their respective groups
        """
        tile_type, entity_type, entity_id = tile_info[0].split('_')
        xcoord, ycoord = tile_info[1], tile_info[2] # coordinates of tile

        # Adding tile to Board's position_tile_dict
        board = self.getBoard()
        position_tile_dict = board.getPositionTileDict()
        match tile_type:
            case 'G': # grass
                tile = Tile((123, 245, 10), True)
            case 'W': # wall
                tile = Tile((77, 77, 77), False)
            case 'L': # lava
                tile = Tile((209, 23, 23), True, 10)
            case _:
                raise Exception(f"Tile type {tile_type} does not exist")
        position_tile_dict[(xcoord, ycoord)] = tile
        board.setPositionTileDict(position_tile_dict)
        self.setBoard(board)

        # Adding entity (if exists) to respective group, and to all_sprites
        match entity_type:
            case '0': # no entity exists
                return
            case 'E': # enemy
                enemy_group = self.getEnemyGroup()
                enemy = Enemy(entity_id, xcoord, ycoord)
                enemy_group.add(enemy)
                self.setEnemyGroup(enemy_group)
            case 'N': # npc
                npc_group = self.getNpcGroup()
                npc = Npc(entity_id, xcoord, ycoord)
                npc_group.add(npc)
                self.setNpcGroup(npc_group)
            case 'P': # portal
                portal_group = self.getPortalGroup()
                portal = Portal(entity_id, xcoord, ycoord)
                portal_group.add(portal)
                self.setPortalGroup(portal_group)
            case _:
                raise Exception(f"Entity type {entity_type} does not exist.")
        return