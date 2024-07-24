import pygame
from game_states.game_state import GameState
from pygame.locals import *
from assets import GAME_ASSETS
from game_states.game_world import GameWorld
from typing import Optional
from sprites.character import Character

class WorldLoad(GameState):
    """Class that represents the game state for loading world.
    
    Instantiates GameWorld object from save file.
    Loaded when Load Game is selected in TitleScreen.

    Attributes:
        initialised_game_world (Optional[GameWorld]): The GameWorld object (containing Character) 
            that is initialised as a result of running this gamestate.

        (Inherited) - Unnecessary.
        main_surf (pygame.Surface): Surface onto which all sprites in the game state are blitted.
            Size: 1200 x 768
    """
    # Attributes
    __initialised_game_world = None

    # Constructor
    def __init__(self):
        super().__init__()
        self.setInitialisedGameWorld(None)

    # Getters
    def getInitialisedGameWorld(self) -> Optional[GameWorld]:
        return self.__initialised_game_world

    # Setters
    def setInitialisedGameWorld(self, initialised_game_world):
        self.__initialised_game_world = initialised_game_world

    def run(self) -> str:
        """Instantiates the GameWorld object from file, and sets as
        initialised_game_world attribute.
        
        Immediately returns 'game_world' to enter game world.
        """
        with open('gameinfostorage/save_info.txt', 'r') as file:
            file_lines = file.readlines()
            self.interpretSaveInfo(file_lines)
        return 'game_world'
    
    def interpretSaveInfo(self, file_lines: list[str]) -> GameWorld:
        """Interprets save info and sets initialised_game_world object."""
        level_name = file_lines[0].strip()
        raw_character_stats = file_lines[1:8]
        character_stats = [int(i.strip()) for i in raw_character_stats]
        sth, dfn, hp, maxhp, hr, exp, lvl = character_stats
        weapon_id = file_lines[8].strip()
        # Creating set of quest items
        character_quest_items = set()
        items = file_lines[9:]
        for i in items:
            if i != None:
                character_quest_items.add(i.strip())
        # Creating Character object
        character_image = pygame.image.load(GAME_ASSETS['character'])
        character = Character(character_image, 'Player', weapon_id,
                              sth, dfn, maxhp, hp, lvl, exp, hr)
        character.setQuestItemNames(character_quest_items)
        # Creating GameWorld and initialising level.
        game_world = GameWorld(level_name, character)
        game_world.initialiseLevel()
        self.setInitialisedGameWorld(game_world)