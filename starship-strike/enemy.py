"""Program: enemy.py

Author: Joel Henningsen

This module contains the Enemy class which handles the initializtion of the enemy 
spaceship. The image, position, and speed are loaded. The udpate function updates 
the location of the enemy, and at random chooses how fast it will be going.
"""

import pygame
import random


class Enemy(pygame.sprite.Sprite):
    """A class to represnt the enemy spaceship."""
    def __init__(self, window_width, window_height):
        """Initializes instance of Enemey class."""
        # Inherits
        super().__init__()
        
        # Loads the image of enemy spaceship
        self.image = pygame.image.load("graphics/enemy.png")
        self.rect = self.image.get_rect()

        # Set position to right side of window
        self.rect.right = window_width

        # Randomly select y position for enemy spaceship
        self.rect.y = random.randint(0, window_height - self.rect.height)

        # Randomly choose speed between 1 and 3
        self.speed_x = random.randint(1, 3)  # Added speed_x attribute for horizontal movement
        
        # Setup window and height
        self.window_width = window_width
        self.window_height = window_height

    def update(self):
        """Updates the position and speed of enemy spaceship."""
        # Update position of enemy, moves from right to left
        self.rect.x -= self.speed_x
        
        # Check if the enemy spaceship has reached left side of screen
        if self.rect.right < 0:
            self.rect.right = self.window_width
            self.rect.y = random.randint(0, self.window_height - self.rect.height)
            self.speed_x = random.randint(1, 3)
