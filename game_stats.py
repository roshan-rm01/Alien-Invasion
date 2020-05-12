class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize stats"""
        self.settings = ai_game.settings
        # get stats when player restart the game
        self.reset_stats()
        # If alien invasion game is live or not
        self.game_active = False
        # High score is never reset
        self.high_score = 0

    def reset_stats(self):
        """"Initialize stats that change during game"""
        # number of ships player has during game
        self.ships_left = self.settings.ship_limit
        # reset score every time game starts (no __init__())
        self.score = 0
        # display current level
        self.level = 1


