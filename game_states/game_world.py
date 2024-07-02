import pygame
from game_states.game_state import GameState
from assets import GAME_ASSETS
from pygame.locals import *
from sprites.enemy import Enemy
from sprites.portal import Portal
from sprites.npc import Npc
from sprites.sidebar.sidebar import Sidebar
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
        board (Board): Board sprite - 12x12 grid of tiles.
        npc_group (pygame.sprite.Group): Group containing all npc sprites 
        enemy_group (pygame.sprite.Group): Group containing all enemy sprites
        portal_group (pygame.sprite.Group): Group containing all portal sprites

        (Inherited)
        main_surf (pygame.Surface): Surface onto which all sprites in the game state are blitted. 
            Size: 1200 x 768


    Methods:
        run(self, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> str: 
            Runs all functions associated with GameWorld. 
            To be called each iteration of game loop, while state == "game_world"
            Returns the next state game is to enter.

        Handler methods TODO

        (Initialiser methods)
        initialiseLevel(self) -> None: 
            Initialises level tiles and entities
        parseLevelCode(self) -> list[tuple[str, int, int]]: 
            Returns list of tuples each representing a tile's info: 
            (tile_code, xcoord, ycoord) - tile_code is X_X_XX string representing {tile_type}, {entity_type}, {entity_id}
        interpretTileInfo(self, tile_info: tuple[str, int, int]): 
            Interprets a single tile_info tuple.
            - tile information gets sent to Board object.
            - enemy/npc/portal information sent to their respective groups

    ########
    TODO probably create a gameEvent handler based on the following system:
    Implement once turn based is in.

    Valid: Represents events that have occurred during the last valid user turn.
        4 lines of these displayed at a time.
        These events should be replaced when user next has a valid turn.
        The set of these events are:
            - User attacks enemy(s). 
            - Enemy attacks user.
            - Enemy faints.
            - Npc says something to user.

    Invalid: Represents an error message for an invalid user turn
        1 line displayed at a time.
        Event should be replaced when user next has a valid or invalid turn.
        These events represent erroneous user turns, these being:
            - User walks into wall/entity.
            - User selects invalid target(s) for attack.
            - User interacts with invalid/nonexistent entity.
            - User attempts to enter portal without clearing all enemies
    ###########

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
                 character: Character):
        super().__init__()
        self.setLevelName(level_name)
        self.setCharacter(character)
        self.setSidebar(Sidebar())
        self.setBoard(Board())
        self.setNpcGroup(pygame.sprite.Group())
        self.setEnemyGroup(pygame.sprite.Group())
        self.setPortalGroup(pygame.sprite.Group())

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
        for event in pygame_events:
            pass
            # Use pygame.event == KEYDOWN to do stuff with one movement at a time.

        board = self.getBoard()
        character = self.getCharacter()
        
        # Get attributes needed to update Sidebar
        character_level = character.getLevel()
        health = character.getHealth()
        max_health = character.getMaxHealth()
        exp = character.getExp()
        req_exp = character.calcRequiredExp()
        level_name = self.getLevelName()
        attack_list = character.getWeapon().getAttackList()

        #############
        ## TESTING ##
        #############
        valid_event_list = ['fdf', '123', 'i am an event', 'roco iani cool', 'idk', 'hihi', '2nd page now', 'how long can this message get honestly', '123123123', 'qwertyuiopasdfghjklzxcvbnm 1234567890 qwertyuiop ooooooooooof', 'Hayden Foxwell: "Make sure your uniforms are well adjusted"']
        invalid_event = 'bad'
        #############

        # Update Sidebar display
        sidebar = self.getSidebar()
        used_attack = sidebar.update(pygame_events, mouse_pos, character_level, health, max_health, exp, req_exp, level_name, attack_list, valid_event_list, invalid_event)
        self.setSidebar(sidebar)

        # Blit sprites onto main_surf
        main_surf = self.getMainSurf()
        main_surf.fill((0, 0, 0))
        main_surf.blit(board.getSurf(), (0, 0))
        main_surf.blit(sidebar.getSurf(), (768, 0))
        self.setMainSurf(main_surf)

        #############
        ## TESTING ##
        #############
        print(used_attack)
        #############
        
        return 'game_world'


    # Level initialisation methods.
    def initialiseLevel(self) -> None:
        """
        Initialises the level's board and entities.
        """
        # Interpret tile code, send info to sprite groups and Board object.
        tile_info = self.parseLevelCode()
        for tile in tile_info: # Iterates through all tuples
            self.interpretTileInfo(tile)
        
        # Initialise board surface
        board = self.getBoard()
        board.drawBoardSurface()
        self.setBoard(board)
        

    def parseLevelCode(self) -> list[tuple[str, int, int]]:
        """
        Returns list of tuples each representing a tile's info in form: 
            (tile_code, xcoord, ycoord), where tile_code is X_X_XX string representing {tile_type}, {entity_type}, {entity_id}
        """
        str_to_find = '!!' + self.getLevelName() # marker string for the level code
        with open('gameinfostorage/world_gen.txt', 'r') as world_gen_file:
            file_lines = world_gen_file.readlines()

            # Find place where level code begins
            for pos, line in enumerate(file_lines):
                if str_to_find in line:
                    starting_pos = pos + 1 # position of line at which level code starts

                    # Splits the 12x12 grid code into components.
                    level_code_lines = [file_lines[starting_pos + i] for i in range(12)]
                    tile_info = [(tile_code, int(xcoord), int(ycoord)) for ycoord, code_line in enumerate(level_code_lines) for xcoord, tile_code in enumerate(code_line.split())]
                    return tile_info
            
        raise ValueError(f"Level name ({self.getLevelName()}) cannot be found in file 'world_gen.txt'.")


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
                raise ValueError(f"Tile type ({tile_type}) cannot be found")
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
                raise ValueError(f"Entity type ({entity_type}) cannot be found.")
        return