"""Program: game.py

Author: Joel Henningsen

This module contains the Game class which handles the setup of the game and runs it. 
Here, the game gets initialized along with all of it's objects. There is a run loop 
to constantly keep the game running. There's a function to check the game is running 
and keep updating the screen and it's objects. Another function draws the all visual 
elements. Finally, there's a funciton to handle when the player loses the game is over.
"""

import pygame
from highscore import HighScoreMenu
from player import Spaceship
from enemy import Enemy


class Game:
    """A game class to handle the setup and running of the game."""
    def __init__(self):
        # Initialize Pygame, setup window and caption
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.SPACE_KEY, self.START_KEY, self.BACK_KEY = (
            False, False, False, False, False)
        self.DISPLAY_W, self.DISPLAY_H = 800, 600
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        
        # Setup color constants
        self.BLACK, self.WHITE = (65, 65, 65), (255, 255, 255)
        pygame.display.set_caption("Starship Strike")

    def check_events(self):
        """Checks the inputs of the user."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_SPACE:
                    self.SPACE_KEY = True
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         self.running, self.playing = False, False
        #     # Moving the player up or down at a speed of +/- 7, shooting bullet
        #     elif event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_UP:
        #             self.player.speed_y = -7
        #         elif event.key == pygame.K_DOWN:
        #             self.player.speed_y = 7
        #         elif event.key == pygame.K_SPACE:
        #             self.player.shoot()
        #     # When key is released, speed is set back to 0
        #     elif event.type == pygame.KEYUP:
        #         if event.key == pygame.K_UP and self.player.speed_y < 0:
        #             self.player.speed_y = 0
        #         elif event.key == pygame.K_DOWN and self.player.speed_y > 0:
        #             self.player.speed_y = 0
    
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.SPACE_KEY, self.START_KEY, self.BACK_KEY = (
            False, False, False, False, False)


    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.BACK_KEY:
                self.playing = False
            self.display.fill(self.BLACK)

            # Initializing game objects
            self.all_sprites = pygame.sprite.Group()
            self.enemies = pygame.sprite.Group()
            self.bullets = pygame.sprite.Group()
            self.player = Spaceship(self.all_sprites, self.bullets, self.DISPLAY_W, self.DISPLAY_H)
            self.all_sprites.add(self.player)
            
            # Create 8 enemies
            for _ in range(8):
                enemy = Enemy(self.DISPLAY_W, self.DISPLAY_H)
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)

            # Initialize score and its font
            self.score = 0
            self.score_font = pygame.font.Font(None, 36)

            # Load background image, set x and it's speed to move
            self.background_img = pygame.image.load("graphics/space_bg.png")
            self.background_img = pygame.transform.scale(self.background_img, (self.DISPLAY_W, self.DISPLAY_H))
            self.bg_x = 0
            self.bg_speed = 25

            # Load moon image, set position to top right
            self.moon_img = pygame.image.load("graphics/moon.png")
            self.moon_rect = self.moon_img.get_rect()
            self.moon_rect.topright = (self.DISPLAY_W - 50, 30)

            # Font for "new highscore"
            self.font = pygame.font.Font(None, 36)
            self.window.blit(self.display, (0, 0))

            pygame.display.update()
            self.reset_keys

    def update(self):
        """Function to update the objects of the game."""
        # Update all of the sprites
        self.all_sprites.update()

        # Check for collision between enemy and bullet
        collision = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        
        # Iterates over collision dict. that holds collided enemies
        for enemy, _ in collision.items():
            new_enemy = Enemy(self.window_width, self.window_height)
            self.all_sprites.add(new_enemy)
            self.enemies.add(new_enemy)
            # For each collision, increment score by 1
            self.score += 1

        # Check if any enemy has reached the left-hand side of the screen
        for enemy in self.enemies:
            if enemy.rect.left < 0:
                self.game_over()

        # Check if player collides with enemies
        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.game_over()

        # Update the background position (illusion of scrolling)
        self.bg_x -= self.bg_speed
        if self.bg_x <= -self.window_width:
            self.bg_x = 0

    def render(self):
        """Function to draw the games window, background, sprites, and the score."""
        # Make the background black
        self.window.fill(BLACK)

        # Draw the background image loaded
        self.window.blit(self.background_img, (self.bg_x, 0))
        self.window.blit(self.background_img, (self.bg_x + self.window_width, 0))

        # Draw the moon image loaded
        self.window.blit(self.moon_img, self.moon_rect)

        self.all_sprites.draw(self.window)

        # Display the score at the top/middle of the screen
        score_text = self.score_font.render("Score: {}".format(self.score), True, WHITE)
        score_rect = score_text.get_rect(center=(self.window_width // 2, 20))
        self.window.blit(score_text, score_rect)

        # Update contents of entire display
        pygame.display.flip()

    def run(self):
        """Main game loop, calls event handles, updates game, and draws."""
        # Set running flag and clock for game's FPS
        running = True
        clock = pygame.time.Clock()

       # While the game is running, continuyally call these functions
        while running:
            if self.check_events():
                running = False
            self.update()
            self.render()
            clock.tick(60)  # Set the FPS limit to 60

    def game_over(self):
        """Handles when the game ends and some high score managment."""
        # Create instance of high score menu, call the read high score function
        high_score = HighScoreMenu(self)
        high_score.read_high_scores()

        # Check if the current score is a high score, compare new score with highest
        if self.score > int(high_score.high_scores[-1][1]):
           
           # Display new high score text, update screen
            new_highscore_surface = self.font.render("New highscore! Go to console to enter your name.", True, WHITE)
            new_highscore_rect = new_highscore_surface.get_rect(center=(400, 100))
            self.window.blit(new_highscore_surface, new_highscore_rect)
            pygame.display.flip()

            # Loop and input validation for user's name for new high score
            while True:
                try:
                    player_name = input("Congratulations! You achieved a high score! Enter your name (3 to 12 characters): ")
                    if len(player_name) >= 3 and len(player_name) <= 12 and player_name.isalpha():
                        break
                    else:
                        raise ValueError("Invalid entry. Name must be 3-12 characters long and only use alphabetical letters.")
                # Exception
                except ValueError as e:
                    print(e)
            # Add player name and new score to list, sort the list, and get rid of the lowest score
            high_score.high_scores.append((player_name, str(self.score)))
            high_score.high_scores.sort(key=lambda x: int(x[1]), reverse=True)
            high_score.high_scores.pop()  # Remove the lowest score, keep max of 5

            # Write new list of scores to high_score.txt
            high_score.write_high_scores()

        # Run the high score screen
        high_score.run()
        