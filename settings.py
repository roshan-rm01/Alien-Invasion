class Settings:
    """Class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize game settings"""
        # Screen settings
        self.screen_width = 1000
        self.screen_height = 600
        # RGB Color
        self.bg_color = (230, 230, 230)
        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3
        # Bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet direction of 1 is right, -1 is left
        self.fleet_direction = 1
        # How quickly game speeds up
        self.speedup_scale = 1.1
        # How quickly alien point value increases, rate of increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    # initialize values that need to change throughout the game
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction of 1 represent right, -1 represent left
        self.fleet_direction = 1
        # scoring of each alien
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        # increase game speed using speed up scale
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        # point value increases as game difficulty speed increases
        self.alien_points = int(self.alien_points * self.score_scale)
