"""Program: player.py

Author: Joel Henningsen

This module contains the SpaceShip and Bullet classes. The spaceship class handles 
the player's character and has functions to update the spaceship along with shooting 
bullets. The bullet class sets up what the bullet looks like and also updates it's
position relative to it's speed.
"""

import pygame


# Colors constants
WHITE = (255, 255, 255)


class Spaceship(pygame.sprite.Sprite):
    """A spaceship class that represents the player's character."""
    def __init__(self, all_sprites, bullets, window_width, window_height):
        """Initializes spaceship class."""
        # Inherits pygame.sprite.Sprite
        super().__init__()
        # Loads the image of the spaceship
        self.image = pygame.image.load("graphics/spaceship.png")
        self.rect = self.image.get_rect()
        
        # Spaces the spaceship on left side of screen, vertically centered
        self.rect.x = 10
        self.rect.centery = window_height // 2
        
        # Initialize speed to 10
        self.speed_y = 0

        self.all_sprites = all_sprites
        self.bullets = bullets

        # Setup window width and height
        self.window_width = window_width
        self.window_height = window_height

    def update(self):
        """Updates the location/position of player's spaceship."""
        # Update vertical position of spaceship
        self.rect.y += self.speed_y
        # Does not let the spaceship move off the screen
        if self.rect.top < 0:
            self.rect.top = 0
        # Does not let the spaceship move outside of window height
        elif self.rect.bottom > self.window_height:
            self.rect.bottom = self.window_height

    def shoot(self):
        """Shoots a bullet."""
        # Creates instance of bullet class, add's bullet to all_sprites
        bullet = Bullet(self.rect.right, self.rect.centery, self.window_width)
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    """A bullet class that represnts the bullet the spaceship shoots at the enemy."""
    def __init__(self, x, y, window_width):
        # Inherits
        super().__init__()
        # Adjust size of bullet, fill with white
        self.image = pygame.Surface((15, 3))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        # Bullet leaves right side of spaceship, centered vertically, speed of 5
        self.rect.left = x
        self.rect.centery = y
        self.speed_x = 5

        self.window_width = window_width

    def update(self):
        """Updates the bullet's position."""
        # Updates position of bullet according to it's speed
        self.rect.x += self.speed_x

        # If bullet leaves screen, get rid of it
        if self.rect.right > self.window_width:
            self.kill()
