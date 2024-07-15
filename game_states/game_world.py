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
from typing import Optional, Any, Callable

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
        TODO need all_sprites

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

        self.updateSidebar()

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
        """
        Interprets pygame_events into actions, and runs handleTurn() for each.
        Returns 'game_menu' if ESC key pressed, else returns None
        """

        key_presses = [event.key for event in pygame_events if event.type == KEYDOWN]
        mouse_presses = [event.button for event in pygame_events if event.type == MOUSEBUTTONDOWN]

        if self.getInternalState() == 'main':
            # Checking for keypress-triggered actions: move and interact
            keybinds = {K_UP: ('move', 'up'), K_DOWN: ('move', 'down'), K_RIGHT: ('move', 'right'), K_LEFT: ('move', 'left'),
                        K_i: ('interact', 'up'), K_k: ('interact', 'down'), K_l: ('interact', 'right'), K_j: ('interact', 'left')}
            for key in key_presses:
                if key in keybinds.keys(): # Checks whether the key would cause an action
                    self.handleTurn(keybinds[key]) # Does turn associated with that key
                elif key == K_ESCAPE:
                    return 'game_menu'
            
        if self.getInternalState() == 'attack_target_selection':
            if 1 in mouse_presses: # left mouse button
                for enemy in self.getEnemyGroup():
                    if enemy.getRect().collidepoint(mouse_pos): # Gets the clicked enemy
                        self.handleTurn(('attack', enemy))

        return
    
    def handleTurn(self, action: tuple[str, Any]) -> None:
        """
        Handles a single turn with the given user action.

        Given a player action: 
            Runs corresponding Character method.
            Only if the action was valid, runs all enemy actions.
            Sends all events that occurred during that turn to the GameEventDisplay.
        """

        action_type = action[0]
        action_arg = action[1]
        character = self.getCharacter()
        game_event_display = self.getSidebar().getGameEventDisplay()
        
        # With action_type, determines and runs the corresponding character method.
        #
        # character_triggered_events is event(s) caused by the character action.
        # It is a list if the event is valid, and is a string if event is invalid.
        #
        # E.g. if character attacks an enemy successfully, then character_triggered_events
        # is a list with the attack used, and damage done to enemy.
        match action_type: # TODO fix the methods such that they have correct arguments.
            case 'move':
                is_valid, character_triggered_events = character.move(action_arg)
            case 'interact':
                is_valid, character_triggered_events = character.interact(action_arg)
            case 'attack':
                is_valid, character_triggered_events = character.attack(action_arg)
            case _:
                raise ValueError(f'Action ({action_type}) does not exist.')
        # Depending on validity of action, handles enemy turns and sends events to GameEventDisplay.
        if is_valid:   
            enemy_triggered_events = self.handleEnemyActions()
            all_events = character_triggered_events + enemy_triggered_events
            game_event_display.updateEvents(True, all_events)
        else:
            game_event_display.updateEvents(False, character_triggered_events)

        self.setCharacter(character)
        self.setSidebar(self.getSidebar().setGameEventDisplay(game_event_display))
        return

    def handleEnemyActions(self) -> list[Optional[str]]:
        """
        Runs action() method for each enemy in enemy_group.
        Returns a list of game events representing the actions by each enemy.
        """

        enemy_triggered_events = list()
        # Does enemy action for each enemy, and adds events to enemy_triggered_events
        for enemy in self.getEnemyGroup(): 
            enemy_triggered_events.extend([i for i in enemy.action()])
        return enemy_triggered_events
    
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
        """Sets Board, Character's coordinates, and entity groups based on level_name"""
        level_contents = LevelInitialiser().getLevelContents(self.getLevelName())
        board, character_coords, enemy_group, npc_group, portal_group = level_contents
        self.setBoard(board)
        self.setEnemyGroup(enemy_group)
        self.setNpcGroup(npc_group)
        self.setPortalGroup(portal_group)
        character = self.getCharacter()
        character.setXcoord(character_coords[0])
        character.setXcoord(character_coords[1])
        self.setCharacter(character)