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
from level_initialiser import LevelInitialiser
from typing import Optional, Any
from sprites.entity import Entity
from sprites.active_entity import ActiveEntity

class GameWorld(GameState):
    """Class representing the game world.
    
    Loaded after completion of WorldInit and WorldLoad.

    Attributes:
        sidebar (Sidebar): In-game sidebar
        level_name (str): Name of the current level
        internal_state (str): Current internal state: in ['main', 'attack_target_selection']
        character (Character): Character sprite controlled by player
        board (Board): Board sprite - 12x12 grid of tiles.
        npc_group (pygame.sprite.Group): Group containing all npc sprites 
        enemy_group (pygame.sprite.Group): Group containing all enemy sprites
        portal_group (pygame.sprite.Group): Group containing all portal sprites
        num_enemies (int): The number of remaining enemies in enemy_group.

        (Inherited)
        main_surf (pygame.Surface): Surface onto which all sprites in the game state are blitted. 
            Size: 1200 x 768
    """

    # Attributes
    __sidebar = None
    __level_name = None
    __character = None
    __board = None
    __npc_group = None
    __enemy_group = None
    __portal_group = None
    __internal_state = None
    __num_enemies = None

    # Constructor
    def __init__(self, 
                 level_name: str, 
                 character: Character):
        super().__init__()
        self.setLevelName(level_name)
        self.setCharacter(character)
        self.initialiseLevel()
        self.setSidebar(Sidebar())
        self.setInternalState('main')

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
    def getInternalState(self):
        return self.__internal_state
    def getNumEnemies(self):
        return self.__num_enemies

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
    def setInternalState(self, internal_state):
        self.__internal_state = internal_state
    def setNumEnemies(self, num_enemies):
        self.__num_enemies = num_enemies

    # Methods
    def run(self, pygame_events: list[pygame.event.Event], mouse_pos: tuple[int, int]) -> str:
        """
        Runs all functions associated with GameWorld. 
        To be called each iteration of game loop, while state == "game_world"
        Returns the next state game is to enter.
        """
        board = self.getBoard()
        character = self.getCharacter()
        sidebar = self.getSidebar()

        # Interprets pygame events, and runs turns.
        # If output is 'game_menu', switches game state to GameMenu.
        output = self.interpretUserInput(pygame_events, mouse_pos)
        if output == 'game_menu':
            return 'game_menu'

        # This thing does all the attack button handling. Should be runSidebar.
        # Since I'll have an updateSidebarInfo function for what happens at the end of a turn
        # And this runSidebar is for stuff like attack button handling etc.
        self.updateSidebar(pygame_events, mouse_pos) # TODO fix

        # Blit sprites onto main_surf
        main_surf = self.getMainSurf()
        main_surf.fill((0, 0, 0))
        main_surf.blit(board.getSurf(), (0, 0))
        main_surf.blit(sidebar.getSurf(), (768, 0))
        for entity in self.getNpcGroup():
            entity_screen_pos = (entity.getXcoord()*64, entity.getYcoord()*64)
            main_surf.blit(entity.getSurf(), entity_screen_pos)
        self.setMainSurf(main_surf)

        return 'game_world'
    
    
    def interpretUserInput(self, 
                     pygame_events: list[pygame.event.Event],
                     mouse_pos: tuple[int, int]) -> Optional[str]:
        """Interprets pygame_events, for whether the user has made an action.

        Checks whether ESC has been pressed: this returns to the gamestate GameMenu.
        If internal_state is main, checks whether the user has tried to move or interact.
        If internal_state is attack_target_selection, check whether user has tried to click an enemy.
        Runs handleTurn() for any actions.
        Returns 'game_menu' if ESC key pressed, else returns None.
        """
        key_presses = [event.key for event in pygame_events if event.type == KEYDOWN]
        mouse_presses = [event.button for event in pygame_events if event.type == MOUSEBUTTONDOWN]
        if K_ESCAPE in key_presses:
            return 'game_menu'
        if self.getInternalState() == 'main':
            key_to_action = {K_UP: ('move', 'up'),       K_DOWN: ('move', 'down'), 
                             K_RIGHT: ('move', 'right'), K_LEFT: ('move', 'left')}
            # For each user keypress, checks if it represents an action.
            # If it does, sends the action to character.
            for key in key_presses:
                if key in key_to_action.keys():
                    self.handleTurn(key_to_action[key])
        elif self.getInternalState() == 'attack_target_selection':
            if 1 in mouse_presses: # Left mouse button has been clicked.
                for enemy in self.getEnemyGroup():
                    if enemy.getRect().collidepoint(mouse_pos): # Gets the clicked enemy
                        self.handleTurn(('attack', enemy))
        return None
    
    def handleTurn(self, action: tuple[str, Any]) -> None:
        """Handles a single turn given a user action.

        Given a player action: 
            Runs corresponding Character method. If the action was valid:
                Runs all enemy actions, and sends all events that 
                occurred during that turn to the GameEventDisplay.
        """
        character = self.getCharacter()
        character_caused_events = character.handleAction(action)

        # Depending on validity of action, handles enemy turns and sends events to GameEventDisplay.
        if character_caused_events != False:
            enemy_caused_events = self.handleEnemyActions()
            all_events = character_caused_events + enemy_caused_events
            self.handleEndOfTurn(all_events)

        self.setCharacter(character)
        return

    def handleEnemyActions(self) -> list[Optional[str]]:
        """Handles the actions of all enemies on the board.

        Runs action() method for each enemy in enemy_group.
        Returns a list of game events representing the actions by each enemy.
        """
        enemy_caused_events = list()
        # Does enemy action for each enemy, and adds events to enemy_caused_events
        for enemy in self.getEnemyGroup(): 
            enemy_caused_events.extend(enemy.action())
            # TODO check that character is alive at each of each iteration.
            # if dead, run a game over screen.
        return enemy_caused_events

    def handleEndOfTurn(self, events: list[str]) -> None:
        """Handles all calculations at the end of a turn.
        
        - Updates how many enemies are still remaining.
        - Regenerates all entities.
        - Computes tile damage for all entities currently on tile.
            Adds game events representing tile damage taken.
        - If any portals have been activated, initialises the new level.
        - Sends all information to Sidebar's GameEventDisplay and DataDisplay.
        """
        coords_to_tile = self.getBoard().getCoordsToTile()
        self.setNumEnemies(len(self.getEnemyGroup()))
        # Regenerating all entities
        self.getCharacter.regenerate()
        for enemy in self.getEnemyGroup():
            enemy.regenerate()
        # Checking for tile damage TODO move to a new method for readability.
        for tile in coords_to_tile.keys():
            tile_damage = tile.getDamage()
            occupying_entity = tile.getOccupied()
            # Checks that tile damage is nonzero, and a Character/Enemy is in the tile.
            if tile_damage != 0 and isinstance(occupying_entity, ActiveEntity) == True:
                damage_taken = occupying_entity.takeDamage(tile_damage)
                events.append(f"{occupying_entity.getName()} took"
                              f"{damage_taken} from a {tile.getName()} tile!")
                if not occupying_entity.getIsAlive():
                    events.append(f'{occupying_entity} fainted!')
        # Checking for portal activation
        for portal in self.getPortalGroup():
            if portal.getIsActivated():
                self.setLevelName(portal.getDestination())
                self.initialiseLevel()
        # Updating GameEventDisplay
        game_event_display = self.getSidebar().getGameEventDisplay()
        # TODO update the display
        return
    
    def updateSidebar(self, pygame_events, mouse_pos) -> None:
        """
        Updates the Sidebar display, and checks if the attack buttons have been pressed.
        If an attack button is pressed, updates Character's selected attack,
        and GameWorld's internal state.
        """
        pass 
        # # Get attributes needed to update Sidebar
        # character = self.getCharacter()
        # character_level = character.getLevel()
        # health = character.getHealth()
        # max_health = character.getMaxHealth()
        # exp = character.getExp()
        # req_exp = character.calcRequiredExp()
        # level_name = self.getLevelName()
        # attack_list = character.getWeapon().getAttackList()

        # # Update Sidebar display
        # sidebar = self.getSidebar()
        # used_attack = sidebar.update(pygame_events, mouse_pos, character_level, health, max_health, exp, 
        #                              req_exp, level_name, attack_list)
        # self.setSidebar(sidebar)

    def initialiseLevel(self) -> None:
        """Initialises level contents based on level_name
        
        Sets the enemy/npc/portal sprite groups, Board, and num_enemies_remaining.
        """
        level_contents = LevelInitialiser().getLevelContents(self.getLevelName(), self.getCharacter())
        board, enemy_group, npc_group, portal_group = level_contents
        self.setBoard(board)
        self.setEnemyGroup(enemy_group)
        self.setNpcGroup(npc_group)
        self.setPortalGroup(portal_group)
        self.setNumEnemies(len(enemy_group))
