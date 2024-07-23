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

    def getLevelContents(self, 
                         level_name: str,
                         character: Character
                         ) -> tuple[Board, pygame.sprite.Group, pygame.sprite.Group, pygame.sprite.Group]:
        """
        Main method for getting the level's board and entities.
        Parses the level code, gets Board and entity sprite groups, and draws board surface.
        Returns tuple containing level contents: 
            (board, enemy sprite group, npc sprite group, portal sprite group).
        """
        tile_info_list = self.parseLevelCode(level_name)
        level_contents = self.interpretTileInfo(tile_info_list, character)
        board = level_contents[0]
        board.drawBoardSurface()
        return level_contents

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
                          tile_info_list: list[tuple[str, int, int]],
                          character: Character
                          ) -> tuple[Board, pygame.sprite.Group, pygame.sprite.Group, pygame.sprite.Group]:
        """
        Interprets the list of tuples representing tile information.

        Iterates through the list of tuples, and using this:
            - Creates Board object, and fills its coords_to_tile dict.
            - Locates Character's coordinates, and sets them.
            - Creates and fills the sprite groups for the different entities.

        Returns a tuple containing the board, enemy sprite group, 
        npc sprite group and portal sprite group.
        """
        board = Board()
        enemy_group, npc_group, portal_group = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()

        for tile_info in tile_info_list:
            tile_type, entity_type, entity_id = tile_info[0].split('_')
            xcoord, ycoord = tile_info[1], tile_info[2]
            entity_on_tile = self.interpretEntityType(entity_type, entity_id, xcoord, ycoord, 
                                                      character, enemy_group, npc_group, portal_group)
            self.addTileToBoard(board, tile_type, entity_on_tile, xcoord, ycoord)
        return board, enemy_group, npc_group, portal_group

    def interpretEntityType(self, 
                            entity_type: str, 
                            entity_id: str, 
                            xcoord: int, 
                            ycoord: int, 
                            character: Character,
                            enemy_group: pygame.sprite.Group,
                            npc_group: pygame.sprite.Group, 
                            portal_group: pygame.sprite.Group) -> Optional[Entity]:
        """Creates/modifies an entity object based on entity_type on a tile.

        If entity is a character, modifies its coordinates.
        If entity is an enemy/portal/npc, creates an instance of it.
        Returns the entity object that was created/modified.
        """
        match entity_type:
            case 'C':
                character.setXcoord(xcoord)
                character.setYcoord(ycoord)
                entity = character
            case 'E':
                entity = Enemy(entity_id, xcoord, ycoord)
                enemy_group.add(entity)
            case 'N':
                entity = Npc(entity_id, xcoord, ycoord)
                npc_group.add(entity)
            case 'P':
                entity = Portal(entity_id, xcoord, ycoord)
                portal_group.add(entity)
            case '0':
                entity = None
            case _:
                raise ValueError(f"Entity type ({entity_type}) is unknown.")
        return entity

    def addTileToBoard(self, board: Board, tile_type: str, entity: Optional[Entity], 
                       xcoord: int, ycoord: int) -> None:
        """Adds a tile to Board's coord_to_tile dictionary."""
        coords_to_tile = board.getCoordsToTile()
        match tile_type:
            case 'G':
                tile = Tile('grass', (123, 245, 10), True, entity)
            case 'W':
                tile = Tile('wall', (77, 77, 77), False, entity)
            case 'L':
                tile = Tile('lava', (209, 23, 23), True, entity, 10)
            case _:
                raise ValueError(f"Tile type ({tile_type}) is unknown.")
        coords_to_tile[(xcoord, ycoord)] = tile
        board.setCoordsToTile(coords_to_tile)
        return