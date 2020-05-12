import pygame
from pygame.sprite import Sprite


# ship is treated as a rectangle shape and inherits Sprite
class Ship(Sprite):
    """A class to manage the ship"""

    # Takes 2 parameters its reference and reference to current instance of AlienInvasion class
    # Ship is able to access game resources from defined in AlienInvasion
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        # access sprite attributes
        super().__init__()
        # Game screen assigned to ship attribute for easy access to main class
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # get screen rect attribute to place ship in correct location on the screen
        # get_rect() can help movement of the ship to a position
        self.screen_rect = ai_game.screen.get_rect()
        # Load the ship image and get its rect, image.load() returns a surface
        self.image = pygame.image.load("Images/ship.bmp")
        # Access ship surface rect attribute to place the ship
        self.rect = self.image.get_rect()
        # Start each ship at bottom center of the screen
        # get_rect() positions ship at middle bottom of the screen
        # Ship position set relative to the game screen (match position of ship on game screen)
        self.rect.midbottom = self.screen_rect.midbottom
        # Store decimal value for ship's horizontal x position
        self.x = float(self.rect.x)
        # Movement flag
        # if ship is moving rightwards
        self.moving_right = False
        # if ship is moving leftwards
        self.moving_left = False

    def update(self):
        """Update ship position based on movement flag"""
        # Update ship x value not rect
        # Ship speed can be adjusted
        # if moving right is true and right x coordinate of ship < screen right x coordinate
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        # if moving left is true and left x coordinate of ship > 0
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # Update rect object from self.x
        self.rect.x = self.x

    # Draw image to screen at specified position from self.rect
    def blitme(self):
        """Draw the ship in its current location"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center ship on screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        # ship centered back to original position
        self.x = float(self.rect.x)
