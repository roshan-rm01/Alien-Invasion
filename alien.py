import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Class representing single alien in fleet"""

    def __init__(self, ai_game):
        """Initialize alien and set position"""
        super().__init__()
        # access screen from main game
        self.screen = ai_game.screen
        # get setting from main game to access attributes
        self.settings = ai_game.settings

        # Load alien image and set rect attribute
        self.image = pygame.image.load("Images/alien.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien near top left of screen
        # set position of alien
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store alien exact position
        self.x = float(self.rect.x)

    # check for alien collision with wall
    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        # if alien is at either edge of sceen
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    # update alien position to move
    def update(self):
        """Move alien to the right or left"""
        # alien position change either left or right
        self.x += (self.settings.alien_speed
                   * self.settings.fleet_direction)
        # set x position to rect x position to update alien position
        self.rect.x = self.x
