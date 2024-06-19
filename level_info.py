import pygame
from pygame.locals import *
from enemy import Enemy
from npc import Npc
from portal import Portal
from assets import load_assets
from character import Character
load_assets()
import time

class LevelInfo():
    """
    Class representing the level information: 
        - Stores level name and meta-info
        - Initialises all tiles and entities in world.
        - Stores tiles and their coordinates in a dictionary (position_tile_dict)
        - Stores entities (enemies/npcs) in groups (npc_group, enemy_group, portal_group)

    Attributes:
        level_name (str): Name of the current level
        all_clear (bool): True if all enemies are cleared, False otherwise.
        board_surf (pygame.Surface): Surface onto which all tiles are drawn

        character (Character): Character sprite in level
        position_tile_dict (dict): Dictionary with coordinate tuple (xcoord, ycoord) keys with values being the tile type at the coordinate:
            {(xcoord, ycoord): tile_type}
        npc_group (pygame.sprite.Group): Group containing all npc sprites 
        enemy_group (pygame.sprite.Group): Group containing all enemy sprites
        portal_group (pygame.sprite.Group): Group containing all portal sprites
        all_sprites (pygame.sprite.Group): Pygame group containing all sprites [tiles, character, enemies, npcs]
    
    Methods:
        initialiseLevel(self): Initialises level tiles and entities 
        parseLevelCode(self): Parses the code of the level with name level_name, and returns tuples (tile_code, xcoord, ycoord) - tile_code is X_X_XX strings
        doStuffWithTileInfo(self, tile_info): Adds a tile_info tuple's information to entity groups and tile dict. TODO make this have a real name
        drawBoardSurface(self): Draws board_surface using position_tile_dict

    """
    
    # Attributes
    __level_name = None
    __all_clear = None
    __board_surf = None
    __character = None
    __position_tile_dict = None
    __npc_group = None
    __enemy_group = None
    __portal_group = None
    __all_sprites = None

    # Constructor
    def __init__(self, level_name: str, board_surf: pygame.Surface, character: Character):
        self.setLevelName(level_name)
        self.setBoardSurf(board_surf)
        self.setCharacter(character)
        self.setPositionTileDict(dict())
        self.setNpcGroup(pygame.sprite.Group())
        self.setEnemyGroup(pygame.sprite.Group())
        self.setPortalGroup(pygame.sprite.Group())
        self.setAllSprites(pygame.sprite.Group())
        self.getAllSprites().add(character) # adds character to all_sprites group
        self.initialiseLevel()

    # Getters
    def getLevelName(self):
        return self.__level_name
    def getAllClear(self):
        return self.__all_clear
    def getBoardSurf(self):
        return self.__board_surf
    def getCharacter(self):
        return self.__character
    def getPositionTileDict(self):
        return self.__position_tile_dict
    def getNpcGroup(self):
        return self.__npc_group
    def getEnemyGroup(self):
        return self.__enemy_group
    def getPortalGroup(self):
        return self.__portal_group
    def getAllSprites(self):
        return self.__all_sprites

    # Setters
    def setLevelName(self, level_name):
        self.__level_name = level_name
    def setAllClear(self, all_clear):
        self.__all_clear = all_clear
    def setBoardSurf(self, board_surf):
        self.__board_surf = board_surf
    def setCharacter(self, character):
        self.__character = character
    def setPositionTileDict(self, position_tile_dict):
        self.__position_tile_dict = position_tile_dict
    def setNpcGroup(self, npc_group):
        self.__npc_group = npc_group
    def setEnemyGroup(self, enemy_group):
        self.__enemy_group = enemy_group
    def setPortalGroup(self, portal_group):
        self.__portal_group = portal_group
    def setAllSprites(self, all_sprites):
        self.__all_sprites = all_sprites



    # Methods
    def initialiseLevel(self):
        """
        Initialises the level's tiles and entities.
        """
        tile_info = self.parseLevelCode()
        for t in tile_info: # iterates through all tuples (tile_code, xcoord, ycoord).
            self.doStuffWithTileInfo(t)
        self.drawBoardSurface()
        


    def parseLevelCode(self):
        """
        Finds 11x11 level code in file and returns a list of tuples of form: (tile_code, xcoord, ycoord)
        """
        str_to_find = '!!' + self.getLevelName() # !!{level_name} - marker line for world gen code
        with open('gameinfostorage/world_gen.txt', 'r') as world_gen_file:
            file_lines = world_gen_file.readlines()
            for pos, line in enumerate(file_lines):
                if str_to_find in line:
                    starting_pos = pos + 1 # position of line at which level code starts

                    # level_code_lines is a list of 11 lines representing each row of tile code
                    level_code_lines = [file_lines[starting_pos + i] for i in range(11)]
                    # tile_info is a list containing 121 tuples representing tile information
                    tile_info = [(tile_code, xcoord, ycoord) for ycoord, code_line in enumerate(level_code_lines) for xcoord, tile_code in enumerate(code_line.split())]
                    return tile_info
    

    def doStuffWithTileInfo(self, tile_info):
        """
        Input tile_info: singular tuple representing a tile: (tile_code, xcoord, ycoord)
        Interprets tile_info, then adds tile entity to tile_list.
        Adds enemy/npc/portal entities on tile (if exists) to their respective groups.
        """
        tile_type, entity_type, entity_id = tile_info[0].split('_')
        xcoord, ycoord = int(tile_info[1]), int(tile_info[2]) # coordinates of tile

        # Adding tile to position_tile_dict
        if tile_type == 'G':
            self.getPositionTileDict()[(xcoord, ycoord)] = 'grass'
        elif tile_type == 'W':
            self.getPositionTileDict()[(xcoord, ycoord)] = 'wall'
        elif tile_type == 'L':
            self.getPositionTileDict()[(xcoord, ycoord)] = 'lava'

        # Adding entity (if exists) to respective group, and to all_sprites
        if entity_type == '0': # if no entity exists on tile
            return
        elif entity_type == 'E': # enemy
            enemy = Enemy(entity_id, xcoord, ycoord)
            self.getEnemyGroup().add(enemy)
            self.getAllSprites().add(enemy)
        elif entity_type == 'N': #n npc
            npc = Npc(entity_id, xcoord, ycoord)
            self.getNpcGroup().add(npc)
            self.getAllSprites().add(npc)
        elif entity_type == 'P': # portal
            portal = Portal(entity_id, xcoord, ycoord)
            self.getPortalGroup().add(portal)
            self.getAllSprites().add(portal)
        else: # error handling
            raise Exception("entity_type does not exist.")
        return

    def drawBoardSurface(self):
        """
        Using position_tile_dict, draws tiles onto board_surf
        """ 
        position_tile_dict = self.getPositionTileDict()
        board_surf = self.getBoardSurf()
        # Iterating through all xcoord, ycoord and tile_type
        for xcoord, ycoord in position_tile_dict.keys():
            tile_type = position_tile_dict[(xcoord, ycoord)]
            if tile_type == 'grass':
                pygame.draw.rect(board_surf, (0, 255, 0), (xcoord*64, ycoord*64, 64, 64))
            elif tile_type == 'wall':
                pygame.draw.rect(board_surf, (0, 0, 0), (xcoord*64, ycoord*64, 64, 64))
            elif tile_type == 'lava':
                pygame.draw.rect(board_surf, (255, 0, 0), (xcoord*64, ycoord*64, 64, 64))
        
## TESTING
# x=time.time()
# test = LevelInfo('Dining Hall 1', pygame.Surface((728, 728)), Enemy('RI', 2, 2))
# run = True
# screen = pygame.display.set_mode((1200, 800))


# pygame.init()
# y=time.time()
# print(y-x)
# while run:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             run = False
#     screen.blit(test.getBoardSurf(), (0, 0)) # Blits the board to the top left of screen.
#     pygame.display.flip()
# pygame.quit()
