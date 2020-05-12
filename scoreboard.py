import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """A class to report score information"""

    # ai game access setting, screen and stats objects
    def __init__(self, ai_game):
        """Initialize score keeping attributes"""
        # access main game
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # font settings for scoring information
        self.text_color = (30, 30, 30)
        # None - sets default font at size 48
        self.font = pygame.font.SysFont(None, 48)

        # prepare initial score image
        self.prep_score()
        # display high score
        self.prep_high_score()
        # display level count
        self.prep_level()
        # display ships left
        self.prep_ships()

    # turn scoreboard into image
    def prep_score(self):
        """Turn the score into a rendered image"""
        # round the score value to nearest 10, -1 rounds to nearest 10
        rounded_score = round(self.stats.score, -1)
        # turn score into string value, string formatting insert commas to score
        score_str = "{:,}".format(rounded_score)
        # create image of score and display on main screen
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)
        # Display score at top right of screen
        self.score_rect = self.score_image.get_rect()
        # move score position at up right of screen
        # scoreboard is 20 pixels from the right and 20 pixels down
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    # display score image
    def show_score(self):
        """Draw score, ships and levels to screen"""
        # draw message onto screen at location score_rect
        # draw current score top right
        self.screen.blit(self.score_image, self.score_rect)
        # draw high score top center
        self.screen.blit(self.high_score_image, self.high_score_rect)
        # draw level count onto screen
        self.screen.blit(self.level_image, self.level_rect)
        # draw ships left on screen
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """Turn high score into rendered image"""
        # round high score to nearest 10
        high_score = round(self.stats.high_score, -1)
        # format high score with commas
        high_score_str = "{:,}".format(high_score)
        # generate high score image
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)

        # center high score at top of screen
        self.high_score_rect = self.high_score_image.get_rect()
        # set top attribute of screen to match top of score image
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check to see if there is a new high score"""
        # if current score beats high score
        if self.stats.score > self.stats.high_score:
            # set current score to high score
            self.stats.high_score = self.stats.score
            # update high score image
            self.prep_score()

    def prep_level(self):
        """Turn level count into rendered image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                          self.text_color, self.settings.bg_color)

        # position level count below score
        self.level_rect = self.level_image.get_rect()
        # set image right attribute to match score right attribute
        self.level_rect.right = self.score_rect.right
        # set top attribute 10 pixels below bottom of score image
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left"""
        # create an empty group of ships to hold ships
        self.ships = Group()
        # for every ship that is left/available
        for ship_number in range(self.stats.ships_left):
            # create a new ship
            ship = Ship(self.ai_game)
            # set x coordinate so ship is 10 pixels left of the each ship
            ship.rect.x = 10 + ship_number * ship.rect.width
            # set y coordinate 10 pixels down from the top
            ship.rect.y = 10
            # add each new ship to group
            self.ships.add(ship)
