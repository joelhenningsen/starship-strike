"""Program: menu.py

Author: Joel Henningsen

This module contains the MainMenu class which displays the initial options for 
the player. From this screen, the user can start the game, view high scores, or
quit the game. The run function is a loop that also handles the events of the 
user's actions.
"""


import pygame
from game import Game
from highscore import HighScoreMenu


# Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True

    def blit_screen(self):
        self.game.window.blit(self.game_display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu:
    """A class to represent the main menu screen."""
    def __init__(self):
        # Create a list of menu items
        self.menu_items = [
            "Start Game",
            "High Scores",
            "Quit"
        ]
        # Initialize to 0
        self.selected_item = 0

        # Load the background image
        self.background = pygame.image.load("graphics/menu_bg.png").convert()

    def run(self):
        """Runs the main menu screen loop, handles events."""
        # Setup running flag
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.game.display.fill(self.game.BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_display = False
                # Moving bewtween menu items on the screen
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                    elif event.key == pygame.K_DOWN:
                        self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                    # Handling enter/return button depending on which item is selected
                    elif event.key == pygame.K_RETURN:
                        if self.selected_item == 0:
                            self.run_display = False
                            self.run_display = self.start_game()
                        elif self.selected_item == 1:
                            self.run_display = False
                            self.show_high_scores()
                        elif self.selected_item == 2:
                            self.run_display = False

            self.render()
            self.clock.tick(60)

        pygame.quit()

    def render(self):
        """Draws the background background images, handles color of text objects."""
        # Attach background image to screen
        self.window.blit(self.background, (0, 0))

        # Iterate over menu items
        for index, item in enumerate(self.menu_items):
            # If highlighted, change color to white, otherwise black
            color = BLACK if index == self.selected_item else WHITE
            text_surface = self.font.render(item, True, color)
            text_rect = text_surface.get_rect(center=(400, 250 + index * 50))
            self.window.blit(text_surface, text_rect)

        pygame.display.flip()

    def start_game(self):
        """Starts the game."""
        # Create instance of class, run game, return result
        game = Game()
        return game.run()

    def show_high_scores(self):
        """Shows the high scores."""
        # Create instance of class, run high score screen
        high_score = HighScoreMenu(self)
        high_score.run()
