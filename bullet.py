import pygame
from pygame.sprite import Sprite


# Bullet class inherits sprite
class Bullet(Sprite):
    """A class to manage bullets fired from ship"""

    def __init__(self, ai_game):
        """Create bullet object at ship current position"""
        # Inherit __init__() from sprite
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) with width and height and then set correct position
        # Create a rectangle shape no image used
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        # Bullet position is set to the top of ship position
        self.rect.midtop = ai_game.ship.rect.midtop
        # Store the bullet position as decimal value to make adjustments
        self.y = float(self.rect.y)

    # Manage bullets position
    def update(self):
        """Move bullet up the screen"""
        # x position of bullet never changes when fired
        # Update decimal position of bullet
        self.y -= self.settings.bullet_speed
        # Update rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet to screen"""
        # draw bullet shape and fills bullet rect with color stored in self.color
        pygame.draw.rect(self.screen, self.color, self.rect)


