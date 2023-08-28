"""Program: highscore.py

Author: Joel Henningsen

This module contains the HighScoreMenu class which is responsible for handling 
and displaying the high score screen. The run function is a loop that keeps the 
screen running, the render function places objects/background on the screen. There 
are also function that handling the reading of the high score text file, assessing 
the current high scores, and then writing any new ones to the text file.
"""


import pygame

# Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class HighScoreMenu:
    """A class to represent the high score menu screen."""
    def __init__(self, main_menu):
        # Initialize Pygame, setup window and caption
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Starship Strike")

        # Setup FPS and fonts
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Call read high scores to get the current list of high scores
        self.read_high_scores()
        
        # Initialize selected item, setup passed argument into this class
        self.selected_item = 0
        self.main_menu = main_menu

        # Load the background image
        self.background = pygame.image.load("graphics/high_score_bg.png").convert()


    def run(self):
        """Runs the high score menu loop, handles events."""
        # Setup running flag
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Moving between menu items on the screen
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_item = (self.selected_item - 1) % len(self.high_scores)
                    elif event.key == pygame.K_DOWN:
                        self.selected_item = (self.selected_item + 1) % len(self.high_scores)
                    # If user presses 'ESC', return to main menu
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        self.main_menu.run()

            self.render()
            self.clock.tick(60)

        pygame.quit()

    def render(self):
        """Draws the background background images, handles color of text objects."""
        # Attach background image to screen
        self.window.blit(self.background, (0, 0)) 

        # Draw high score text on screen
        title_surface = self.font.render("High Scores", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(400, 50))
        self.window.blit(title_surface, title_rect)

        # Iterate over menu items
        for index, (player, score) in enumerate(self.high_scores):
            # If highlighted, change color to white, otherwise black
            color = BLACK if index == self.selected_item else WHITE
            # Place the player and the score in the scren, centered
            text_surface = self.font.render(f"{player}: {score}", True, color)
            text_rect = text_surface.get_rect(center=(400, 150 + index * 50))
            self.window.blit(text_surface, text_rect)

        pygame.display.flip()

    def read_high_scores(self):
        """Read high score from high_scores.txt file ."""
        # Open file in reading mode
        with open("starship-strike/high_scores.txt", "r") as file:
            # Read each line
            lines = file.readlines()
            # Split lines by ',' and put into list
            self.high_scores = [line.strip().split(",") for line in lines]

    def write_high_scores(self):
        """Write high score list to high_score.txt file ."""
        # Open file in writing mode
        with open("starship-strike/high_scores.txt", "w") as file:
            lines = [f"{player},{score}\n" for player, score in self.high_scores]
            file.writelines(lines)

