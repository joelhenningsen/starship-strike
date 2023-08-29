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


class MainMenu:
    """A class to represent the main menu screen."""
    def __init__(self):
        # Initialize Pygame, setup window and caption
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Starship Strike")

        # Setup FPS and fonts
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

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
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Moving bewtween menu items on the screen
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                    elif event.key == pygame.K_DOWN:
                        self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                    # Handling enter/return button depending on which item is selected
                    elif event.key == pygame.K_RETURN:
                        if self.selected_item == 0:
                            # running = False
                            running = self.start_game()
                        if self.selected_item == 1:
                            # running = False
                            self.show_high_scores()
                        if self.selected_item == 2:
                            running = False

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
