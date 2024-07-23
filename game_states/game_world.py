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
        internal_state (str): Current internal state: in ['main', 'attack_target_selection', 'game_over']
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
        self.setSidebar(Sidebar(self.getCharacter().getWeapon().getAttackList()))
        self.setInternalState('main')

    # Getters
    def getSidebar(self) -> Sidebar:
        return self.__sidebar
    def getLevelName(self) -> str:
        return self.__level_name
    def getCharacter(self) -> Character:
        return self.__character
    def getBoard(self) -> Board:
        return self.__board
    def getNpcGroup(self) -> pygame.sprite.Sprite:
        return self.__npc_group
    def getEnemyGroup(self) -> pygame.sprite.Sprite:
        return self.__enemy_group
    def getPortalGroup(self) -> pygame.sprite.Sprite:
        return self.__portal_group
    def getInternalState(self) -> str:
        return self.__internal_state
    def getNumEnemies(self) -> int:
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
    def run(self, 
            pygame_events: list[pygame.event.Event], 
            mouse_pos: tuple[int, int]) -> str:
        """Main function for GameWorld game state.

        To be called each iteration of game loop, while state == "game_world".
        Interprets user input and runs turns. Updates surfaces.
        Returns the next state game is to enter.
        """
        # Interprets pygame events, and runs turns accordingly
        output = self.interpretUserInput(pygame_events, mouse_pos)
        if output == 'game_menu':
            return 'game_menu'
        self.updateDisplay()
        if self.getInternalState() == 'game_over':
            return 'game_over'
        else:
            return 'game_world'
    
    def interpretUserInput(self, 
                           pygame_events: list[pygame.event.Event],
                           mouse_pos: tuple[int, int]) -> Optional[str]:
        """Interprets pygame_events, and runs methods accordingly.

        Returns 'game_menu' if ESC key pressed, else returns None.
        """
        key_presses = [event.key for event in pygame_events if event.type == KEYDOWN]
        mouse_presses = [event.button for event in pygame_events if event.type == MOUSEBUTTONDOWN]
        if K_ESCAPE in key_presses:
            return 'game_menu'
        self.checkForActions(key_presses, mouse_presses, mouse_pos)
        self.checkSidebarInteraction(pygame_events, mouse_pos)
        return None
    
    def checkForActions(self, 
                        key_presses: list[int], 
                        mouse_presses: list[int], 
                        mouse_pos: tuple[int, int]) -> None:
        """Checks if user has done an action, and runs a turn for each action.

        If internal_state == 'main':
            Runs characterMoveAction() if the character has 
            pressed an arrow key.
        If internal_state == 'attack_target_selection':
            Runs characterAttackAction() if the character has
            clicked an enemy on the board.
        """
        if self.getInternalState() == 'main':
            key_to_direction = {K_UP: 'up',       K_DOWN: 'down', 
                                K_RIGHT: 'right', K_LEFT: 'left'}
            # For each user keypress, checks if it triggers a movement.
            for key in key_presses:
                if key in key_to_direction.keys():
                    self.characterMoveAction(key_to_direction[key])
        elif self.getInternalState() == 'attack_target_selection':
            if 1 in mouse_presses: # Left mouse button.
                # Tries to locate the clicked enemy.
                for enemy in self.getEnemyGroup():
                    if enemy.getSurf().get_rect().collidepoint(mouse_pos): 
                        self.characterAttackAction(enemy)
        return

    def checkSidebarInteraction(self,
                                pygame_events: list[pygame.event.Event],
                                mouse_pos: tuple[int, int]) -> None:
        """Checks if user has pressed any buttons in sidebar, 
        and runs subsequent functions.
        """
        # Checking the attack button handlers for attack selection/deselection.
        if self.getInternalState() == 'main':
            attack_buttons = self.getSidebar().getAttackButtons()
            # Getting the selected attack, if any.
            selected_attack_index = attack_buttons.getAttackSelected(pygame_events, mouse_pos)
            if selected_attack_index:
                self.handleAttackSelection(selected_attack_index)
        elif self.getInternalState() == 'attack_target_selection':
            attack_info_display = self.getSidebar().getAttackInfoDisplay()
            if attack_info_display.isBackPressed(pygame_events, mouse_pos):
                self.handleAttackDeselection()
        # Checking the game event display for page turns.
        game_event_display = self.getSidebar().getGameEventDisplay()
        game_event_display.updatePage(pygame_events, mouse_pos)
        return
    
    def characterMoveAction(self, direction: str) -> None:
        """Handles a turn starting with a character movement.

        Runs character moveOrInteract(). If the action was valid, then:
        - Run all enemy actions.
        - Run handleEndOfTurn().
        """
        character = self.getCharacter()
        coords_to_tile = self.getBoard().getCoordsToTile()
        num_enemies = self.getNumEnemies()
        character_caused_event = character.moveOrInteract(direction, coords_to_tile, num_enemies)
        # If movement/interaction was valid, carries out rest of turn.
        if character_caused_event != False:
            # all_events is all events caused by enemies.
            # The character event is added to this list.
            all_events = self.doEnemyActions()
            all_events.append(character_caused_event)
            self.handleEndOfTurn(all_events)
        return

    def characterAttackAction(self, target: Enemy) -> None:
        """Handles a turn starting with a character attack selection.

        Runs character attack(). If the target was valid, then:
        - Carries out attack and subsequent processes.
        - Run all enemy actions.
        - Run handleEndOfTurn().
        """
        character = self.getCharacter()
        character_caused_events = character.attack(target)
        # If attack was valid, carries out rest of turn.
        if character_caused_events != False:
            # Checks if character killed enemy.
            if not target.getIsAlive():
                self.removeEnemy(target)
                character.gainExp(target.getExpYield()) # TODO make this return events
            self.handleAttackDeselection()
            enemy_caused_events = self.doEnemyActions()
            all_events = character_caused_events + enemy_caused_events
            self.handleEndOfTurn(all_events)
        return

    def doEnemyActions(self) -> list[Optional[str]]:
        """Handles the actions of all enemies on the board.

        Runs action() method for each enemy in enemy_group.
        Returns a list of game events representing the actions by each enemy.
        """
        enemy_caused_events = list()
        # Does enemy action for each enemy, and adds events to enemy_caused_events
        for enemy in self.getEnemyGroup():
            events = enemy.action()
            enemy_caused_events.extend(events)
        return enemy_caused_events

    def handleEndOfTurn(self, events: list[str]) -> None:
        """Handles all calculations at the end of a turn.
        
        - Computes tile damage for all entities currently on tile.
            Adds game events representing tile damage taken.
        - Checks for all character/entity alive status.
            If character is dead, sets internal_state to 'game_over.
            If any enemy is dead, kill()s it.
        - Regenerates all entities.
        - Updates the number of remaining enemies.
        - If any portals have been activated, initialises the new level.
        - Sends all information to Sidebar's GameEventDisplay and DataDisplay.
        """
        coords_to_tile = self.getBoard().getCoordsToTile()
        character = self.getCharacter()
        enemy_group = self.getEnemyGroup()
        # Does tile damage to each entity.
        tile_damage_events = self.tileDamage(coords_to_tile)
        events.extend(tile_damage_events)
        # Checking for alive status of character/enemies.
        if not character.getIsAlive():
            self.setInternalState('game_over')
        for enemy in enemy_group:
            if not enemy.getIsAlive():
                self.removeEnemy(enemy)
        # Regenerating all entities.
        self.getCharacter().regenerate()
        for enemy in self.getEnemyGroup():
            enemy.regenerate()
        # Setting number of enemies.
        self.setNumEnemies(len(self.getEnemyGroup()))
        # Checking for portal activation.
        for portal in self.getPortalGroup():
            if portal.getIsActivated():
                self.setLevelName(portal.getDestination())
                self.initialiseLevel()
        # Updating Sidebar information.
        self.updateSidebarInfo(events)

    def removeEnemy(self, enemy: Enemy) -> None:
        """Removes enemy from enemy_group and from board."""
        coords = (enemy.getXcoord(), enemy.getYcoord())
        coords_to_tile = self.getBoard().getCoordsToTile()
        coords_to_tile[coords] = None
        enemy.kill()
    
    def tileDamage(self,
                   coords_to_tile: dict[tuple[int, int], Tile]) -> list[str]:
        """Computes tile damage.
        
        Returns a list of events caused.
        """
        events = []
        for tile in coords_to_tile.values():
            tile_damage = tile.getDamage()
            occupying_entity = tile.getOccupiedBy()
            # Checks that tile damage is nonzero, and a Character/Enemy is in the tile.
            if tile_damage != 0 and isinstance(occupying_entity, ActiveEntity) == True:
                damage_taken = occupying_entity.takeDamage(tile_damage)
                events.append(f"{occupying_entity.getName()} took"
                              f"{damage_taken} from a {tile.getName()} tile!")
                if not occupying_entity.getIsAlive():
                    events.append(f'{occupying_entity} fainted!')
        return events

    
    def handleAttackSelection(self, selected_attack_index: int) -> None:
        """Handles events if an attack is selected in AttackButtons.
        
        Changes internal state to 'attack_target_selection, and
        sets selected_attack and enemies_in_range in the Character instance.
        Sends the selected attack information to AttackInfoDisplay
        """
        self.setInternalState('attack_target_selection')
        # Selecting attack and getting enemies in range, in Character.
        character = self.getCharacter()
        character_attack_list = character.getWeapon().getAttackList()
        selected_attack = character_attack_list[selected_attack_index]
        character.setSelectedAttack(selected_attack)
        character.calcEnemiesInRange(self.getBoard().getCoordsToTile(),
                                     self.getEnemyGroup())
        attack_info_display = self.getSidebar().getAttackInfoDisplay()
        attack_info_display.updateSurf(selected_attack)
        return

    def handleAttackDeselection(self) -> None:
        """Handles events if an attack is deselected.
        
        Changes internal state to 'main', and removes info from Character.
        """
        self.setInternalState('main')
        self.getCharacter().setSelectedAttack(None)
        self.getCharacter().setEnemiesInRange([])
        return

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
        return
    
    def updateSidebarInfo(self, events: list[str]) -> None:
        """Updates DataDisplay and GameEventDisplay."""
        data_display = self.getSidebar().getDataDisplay()
        game_event_display = self.getSidebar().getGameEventDisplay()
        data_display.updateSurf(self.getCharacter(), self.getLevelName(),
                                self.getNumEnemies())
        game_event_display.updateEvents(events)

    def updateDisplay(self) -> None:
        """Updates all surfaces and blits onto main_surf.
        
        Updates the surfaces of sidebar and active entities.
        Highlights enemies in range of Character's attack.
        Blits board, sidebar and entities onto main_surf.
        """
        board = self.getBoard()
        character = self.getCharacter()
        sidebar = self.getSidebar()
        main_surf = self.getMainSurf()
        # Updating entity/sidebar surfaces.
        character.updateSurf()
        for enemy in self.getEnemyGroup():
            enemy.updateSurf()
        sidebar.updateSurf(self.getInternalState())
        # Highlight all enemies of character's selected attack
        highlighted_tiles = []
        for enemy in character.getEnemiesInRange():
            # Creates a transparent yellow square at the position of the enemy.
            tile_pos = (enemy.getXcoord()*64, enemy.getYcoord()*64)
            highlighted_square = pygame.Surface((64, 64), SRCALPHA)
            highlighted_square.fill((255, 255, 0, 0.7))
            highlighted_square.get_rect().topleft = tile_pos
            highlighted_tiles.append(highlighted_square)
        # Blitting all surfaces onto main_surf.
        main_surf.fill((0, 0, 0))
        main_surf.blit(board.getSurf(), (0, 0))
        main_surf.blit(sidebar.getSurf(), (768, 0))
        main_surf.blit(character.getSurf(), (character.getXcoord()*64, character.getYcoord()*64))
        for entity in (self.getNpcGroup().sprites() + self.getEnemyGroup().sprites() + 
                       self.getPortalGroup().sprites()):
            entity_screen_pos = (entity.getXcoord()*64, entity.getYcoord()*64)
            main_surf.blit(entity.getSurf(), entity_screen_pos)
        for tile_overlay in highlighted_tiles:
            main_surf.blit(tile_overlay, tile_overlay.get_rect)
        return