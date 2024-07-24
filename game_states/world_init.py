import pygame
from game_states.game_state import GameState
from pygame.locals import *
from assets import GAME_ASSETS
from sprites.character import Character
from game_states.game_world import GameWorld
from button_output_getter import ButtonOutputGetter
from sprites.button import Button

class WorldInit(GameState):
    """Class for world initialisation game state.
    
    Initialises GameWorld objects, and included Character.
    Loaded when New Game is selected in TitleScreen.

    Attributes:
        weapon_select_buttons (pygame.sprite.Group): Group containing buttons for weapon selection.
        initialised_game_world (Optional[GameWorld]): The GameWorld object (containing Character) 
            that is initialised as a result of running this gamestate.

        (Inherited)
        main_surf (pygame.Surface): Surface onto which all sprites in the game state are blitted.
            Size: 1200 x 768
    """
    # Attributes
    __weapon_select_buttons = None
    __initialised_game_world = None

    # Constructor
    def __init__(self):
        super().__init__()
        self.createButtons()
        self.createSurf()
        self.setInitialisedGameWorld(None)

    # Getters
    def getWeaponSelectButtons(self):
        return self.__weapon_select_buttons
    def getInitialisedGameWorld(self):
        return self.__initialised_game_world

    # Setters
    def setWeaponSelectButtons(self, weapon_select_buttons):
        self.__weapon_select_buttons = weapon_select_buttons
    def setInitialisedGameWorld(self, initialised_game_world):
        self.__initialised_game_world = initialised_game_world

    # Methods
    def run(self, 
            pygame_events: list[pygame.event.Event], 
            mouse_pos: tuple[int, int]) -> str:
        """
        Runs all functions to initialise the game world.
        To be called each iteration of game loop while state == 'world_init'.
        Returns the next state game is to enter.
        """
        # Getting button outputs
        button_outputs = ButtonOutputGetter().getOutputs(self.getWeaponSelectButtons(), pygame_events, mouse_pos) 
        if button_outputs:
            # Instantiating character and gameworld
            chosen_weapon = button_outputs[0]
            character = self.instantiateCharacter(chosen_weapon)
            game_world = self.instantiateGameWorld(character)
            self.setInitialisedGameWorld(game_world)
            return 'game_world'
        return 'world_init'

    def instantiateGameWorld(self, character: Character) -> GameWorld:
        """Instantiates and returns initial GameWorld object."""
        game_world = GameWorld('Dining Hall', character)
        return game_world

    def instantiateCharacter(self, weapon_id: str) -> Character:
        """Instantiates and returns initial character object."""
        character_image = pygame.image.load(GAME_ASSETS['character'])
        character = Character(character_image, 'Player', weapon_id, 50, 50, 100, 100, 1, 0, 5)
        return character

    def createSurf(self) -> None:
        """Creates surface containing buttons, blits to main_surf"""
        main_surf = self.getMainSurf()
        main_surf.fill((187, 211, 250))
        # Creates text surfaces
        font = pygame.font.Font(None, 64)
        welcome_text = font.render("Hello, player.", True, (0,0,0))
        instruct_text = font.render("Please choose a weapon.", True, (0,0,0))
        # Setting position of text surface
        welcome_text_rect = welcome_text.get_rect()
        welcome_text_rect.center = (600, 80)
        instruct_text_rect = instruct_text.get_rect()
        instruct_text_rect.center = (600, 150)
        # Blitting text surfaces.
        main_surf.blit(welcome_text, welcome_text_rect)
        main_surf.blit(instruct_text, instruct_text_rect)
        # Blitting button surfaces.
        for button in self.getWeaponSelectButtons():
            main_surf.blit(button.getSurf(), button.getRect())

    def createButtons(self) -> None:
        """Creates the weapon selection buttons, and adds to weapon_select_buttons."""
        buttons = pygame.sprite.Group()
        buttons.add(Button(pygame.Surface((200, 100)), 'Sword', 40, 
                                    (255, 255, 255), 'Sw', (150, 300))) 
        buttons.add(Button(pygame.Surface((200, 100)), 'Bow', 40, 
                                    (255, 255, 255), 'Bo', (450, 300)))
        buttons.add(Button(pygame.Surface((200, 100)), 'Daggers', 40, 
                                    (255, 255, 255), 'Dg', (750, 300)))
        buttons.add(Button(pygame.Surface((200, 100)), 'Spellbook', 40, 
                                    (255, 255, 255), 'Sb', (1050, 300)))
        self.setWeaponSelectButtons(buttons)