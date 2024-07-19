import pygame
from sprites.tile import Tile
from sprites.enemy import Enemy
from sprites.npc import Npc
from sprites.portal import Portal
from sprites.board import Board
from sprites.character import Character
from typing import Optional
from sprites.entity import Entity

class LevelInitialiser:
    """Class containing methods to initialise a level's board and entities."""

    def getLevelContents(self, level_name: str
                         ) -> tuple[Board, tuple[int, int], pygame.sprite.Group, pygame.sprite.Group, pygame.sprite.Group]:
        """
        Main method for getting the level's board and entities.
        Parses the level code, gets Board, character coords and entity sprite groups, and draws board surface.
        Returns: board, character coords, enemy sprite group, npc sprite group, portal sprite group.
        """

        tile_info_list = self.parseLevelCode(level_name)
        board, character_coords, enemy_group, npc_group, portal_group = self.interpretTileInfo(tile_info_list)
        board.drawBoardSurface()
        return board, character_coords, enemy_group, npc_group, portal_group

    def parseLevelCode(self, level_name: str) -> list[tuple[str, int, int]]:
        """
        Find the level code in world_gen.txt, and gets its information.
        Returns list of tuples each representing a tile's info in form: 
            (tile_code, xcoord, ycoord), where tile_code is a string of form 'X_X_XX'
            representing {tile_type}_{entity_type}_{entity_id}.
        """

        str_to_find = '!!' + level_name # marker string for the level code
        with open('gameinfostorage/world_gen.txt', 'r') as world_gen_file:
            file_lines = world_gen_file.readlines()
            # Find place where level code begins
            for pos, line in enumerate(file_lines):
                if str_to_find in line:
                    starting_pos = pos + 1 # position of line at which level code starts
                    # Splits the 12x12 grid code into level_info.
                    level_code_lines = [file_lines[starting_pos + i] for i in range(12)] # The lines which contain the code.
                    tile_info_list = [(tile_code, int(xcoord), int(ycoord)) 
                                 for ycoord, code_line in enumerate(level_code_lines) 
                                 for xcoord, tile_code in enumerate(code_line.split())]
                    return tile_info_list
        # If no marker is found within the file, raises ValueError.
        raise ValueError(f"Level name ({level_name}) cannot be found in file 'world_gen.txt'.")

    def interpretTileInfo(self, 
                          tile_info_list: list[tuple[str, int, int]]
                          ) -> tuple[Board, tuple[int, int], pygame.sprite.Group, pygame.sprite.Group, pygame.sprite.Group]:
        """
        Interprets the list of tuples representing tile information.

        Iterates through the list of tuples, and using this:
        Creates Board object, and fills its coords_to_tile dict.
        Locates Character's coordinates.
        Creates the sprite groups for the different entities.

        Returns a tuple containing the board, character coords,
        enemy sprite group, npc sprite group and portal sprite group.
        """

        board = Board()
        enemy_group, npc_group, portal_group = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()

        for tile_info in tile_info_list:
            tile_type_id, entity_type_id, entity_id = tile_info[0].split('_')
            xcoord, ycoord = tile_info[1], tile_info[2] # Coordinates of tile
            tile_type = self.tileIdToType(tile_type_id)
            entity_type = self.entityIdToType(entity_type_id)

            self.addTileToBoard(board, tile_type, entity_type, xcoord, ycoord)
            # Saving character's coords/adding entity to group.
            if entity_type == None:
                continue
            elif entity_type == 'character':
                character_coords = (xcoord, ycoord)
            else:
                self.addEntityToGroup(entity_type, entity_id, xcoord, ycoord, enemy_group, npc_group, portal_group)
        # Returns the level info. Error handling for if Character was not located.
        try:
            return board, character_coords, enemy_group, npc_group, portal_group
        except NameError:
            raise Exception('Character was not located in tile info.')
    
    def addTileToBoard(self, board: Board, tile_type: str, entity_type: Optional[Entity], 
                       xcoord: int, ycoord: int) -> None:
        """Adds a tile to Board's coord_to_tile dictionary."""
        coords_to_tile = board.getCoordsToTile()
        # Creates Tile object depending on tile_type
        match tile_type:
            case 'grass':
                tile = Tile('grass', (123, 245, 10), True, entity_type)
            case 'wall':
                tile = Tile('wall', (77, 77, 77), False, entity_type)
            case 'lava':
                tile = Tile('lava', (209, 23, 23), True, entity_type, 10)
            case _:
                raise ValueError(f"Tile type ({tile_type}) is unknown.")
        coords_to_tile[(xcoord, ycoord)] = tile
        board.setCoordsToTile(coords_to_tile)
        return

    def addEntityToGroup(self, 
                         entity_type: Entity, 
                         entity_id: str, 
                         xcoord: int, 
                         ycoord: int, 
                         enemy_group: pygame.sprite.Group,
                         npc_group: pygame.sprite.Group, 
                         portal_group: pygame.sprite.Group) -> None:
        """Adds an enemy/portal/npc entity to its corresponding group."""
        if entity_type == Enemy:
            enemy = Enemy(entity_id, xcoord, ycoord)
            enemy_group.add(enemy)
        elif entity_type == Npc:
            npc = Npc(entity_id, xcoord, ycoord)
            npc_group.add(npc)
        elif entity_type == Portal:
            portal = Portal(entity_id, xcoord, ycoord)
            portal_group.add(portal)
        else:
            raise ValueError(f"Entity type ({entity_type}) is unknown.")
        return

    def tileIdToType(self, tile_type_id: str) -> str:
        """Returns a string representing the tile type, given its ID."""
        tile_type_expand_dict = {
            'G': 'grass',
            'W': 'wall',
            'L': 'lava'
        }
        try:
            tile_type = tile_type_expand_dict[tile_type_id]
        except KeyError:
            raise ValueError(f"Tile type id ({tile_type_id}) does not exist.")
        return tile_type

    def entityIdToType(self, entity_type_id: str) -> Optional[Entity]:
        """Returns the class representing an entity type, given its ID."""
        entity_type_expand_dict = {
            '0': None,
            'C': Character,
            'E': Enemy,
            'N': Npc,
            'P': Portal
        }
        try:
            entity_type = entity_type_expand_dict[entity_type_id]
        except KeyError:
            raise ValueError(f"Entity type id ({entity_type_id}) does not exist.")
        return entity_type