import sys  # Tools used to exit game when player quits
from time import sleep  # Tools used to pause game
import pygame  # Contain functionality to create a game
from settings import Settings  # Use settings module
from ship import Ship  # Use ship module
from bullet import Bullet  # Use bullet module
from alien import Alien  # use alien module
from game_stats import GameStats  # use game_stats module
from button import Button  # use button module
from scoreboard import Scoreboard  # use scoreboard module


class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize game and create game resources"""
        # Initialize background setting needed for pygame to work
        pygame.init()
        self.settings = Settings()
        # self.screen creates a display window to draw all game graphic elements
        # argument is a tuple that define dimensions of game window
        # self.screen is a surface (surface - part of the screen where game elements are displayed)
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        # Displays caption "Alien Invasion"
        pygame.display.set_caption("Alien Invasion")
        # create instance to store game stats, Gamestats can now access AlienInvasion class
        self.stats = GameStats(self)
        # create scoreboard which refers to main game
        self.sb = Scoreboard(self)
        # Instance of ship is created after the screen is created
        # Ship() takes 1 parameter self, which refers to current instance of main game
        # The ship can now access properties from AlienInvasion class
        self.ship = Ship(self)
        # create a group (list) to store any live bullets that would get deleted
        self.bullets = pygame.sprite.Group()
        # create a group to store aliens
        self.aliens = pygame.sprite.Group()
        # create fleet of aliens
        self._create_fleet()
        # create play button
        self.play_button = Button(self, "Play")

    def Run_Game(self):
        """Start main loop of the game (game loop)"""
        # While loop used runs continuously and manage screen updates
        while True:
            # Helper method used only to help the class not to be called through an instance
            # Access respond to events method
            self._check_events()

            # if game is active mainloop should run
            if self.stats.game_active:
                # Position of ship is updated after event is checked before screen is updated
                self.ship.update()
                # update bullet position
                self._update_bullets()
                # update alien position
                self._update_aliens()

            # Access images method
            self._update_screen()

    # Respond to events
    def _check_events(self):
        """Respond to keypress and mouse events"""
        # Watch for keyboard and mouse events
        # event - action that user performs while playing the game (move mouse, press key)
        # event for loop listens for events and perform tasks depending on events

        # pygame.event.get() returns list of events (mouse, keyboard) taken place since function was called
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Detect and respond to different events
                sys.exit()  # When user exits game pygame.QUIT is detected and sys.exit() is called
            # If pygame detects an action of key pressed down
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # If key press is released
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            # If mouse is pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # return a tuple of mouse (x,y) coordinates
                mouse_pos = pygame.mouse.get_pos()
                # mouse has to press on play button in order to start game
                self._check_play_button(mouse_pos)

    def _fire_bullets(self):
        """Create a new bullet and add it to bullets group"""
        # If amount of bullets fired (spacebar pressed) is less then what is allowed
        if len(self.bullets) < self.settings.bullets_allowed:
            # Instance of new bullet is created
            new_bullet = Bullet(self)
            # Bullet is added to group
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """"Create fleet of aliens"""
        # create alien fleet and find number of aliens in a row
        # alien is created
        alien = Alien(self)
        # get alien width and height
        alien_width, alien_height = alien.rect.size
        # calculate horizontal space for aliens to distance each other
        # amount of aliens drawn must appear on screen width
        space_x = self.settings.screen_width - (2 * alien_width)
        # calculate how many aliens to fit in row
        num_alien_x = space_x // (2 * alien_width)

        # determine number of rows of aliens that fit on screen
        ship_height = self.ship.rect.height
        # determine number of rows to fit on screen
        space_y = (self.settings.screen_height -
                   (3 * alien_height) - ship_height)
        num_row = space_y // (2 * alien_height)
        # create full fleet of aliens
        # count from 0 to amount of rows needed
        # create fleet of aliens in specified amount of rows
        for row_num in range(num_row):
            # create first alien row
            # create for loop from 0 to amount of aliens needed to fill row
            for alien_num in range(num_alien_x):
                # create alien in 1 row
                self._create_alien(alien_num, row_num)

    # Update images to screen and flip to new screen
    def _update_screen(self):
        # Redraw the screen during each pass through the loop with background color
        # fill() method is found on in a surface and fills screen with color
        self.screen.fill(self.settings.bg_color)
        # Draw ship onto screen
        self.ship.blitme()
        # bullets.sprites() method returns a list of all sprites in the group bullet
        for bullet in self.bullets.sprites():
            # To draw each bullet the sprites are iterated and draw_bullet() is called on each bullet
            bullet.draw_bullet()
        # draw alien onto screen
        self.aliens.draw(self.screen)
        # draw score information
        self.sb.show_score()
        # draw play button is game is inactive
        if not self.stats.game_active:
            # draw button onto screen on top of all elements
            self.play_button.draw_button()

        # Make most recent drawn screen visible
        # Draws empty screen at each iteration of the while loop, old screen overwritten with new screen
        pygame.display.flip()

    def _update_bullets(self):
        """Update position of bullets and get rid of old ones"""
        # Update bullet position, calls bullet.update() for each bullet in the group
        self.bullets.update()
        # Get rid of bullets that disappeared
        # Get copy of bullets group in order not to affect group in other parts of code
        for bullet in self.bullets.copy():
            # If bullet position bottom is of the top screen
            if bullet.rect.bottom <= 0:
                # Bullet is removed
                self.bullets.remove(bullet)

        # check for bullet collision with alien
        self._check_bullet_alien_collisions()

    def _update_aliens(self):
        """Check if fleet is at edge then update position of all aliens in fleet"""
        self._check_fleet_edges()
        # check if aliens position is updated
        self.aliens.update()

        # if there is an alien-ship collision
        # spritecollideany() find if any member of group aliens collides with ship
        # loops through group aliens and return first alien collided with ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # ship responds to hit
            self._ship_hit()
        # find aliens hitting bottom of screen
        self._check_aliens_bottom()
        # new fleet appears every time ship is hit by alien or alien reaches bottom of screen

    def _check_keydown_events(self, event):
        """Respond to key press"""
        if event.key == pygame.K_RIGHT:
            # Move ship to the right
            self.ship.moving_right = True
        # If key press is left key move left
        elif event.key == pygame.K_LEFT:
            # Move ship to the left
            self.ship.moving_left = True
        # If key pressed is space fire bullets
        elif event.key == pygame.K_SPACE:
            self._fire_bullets()
        # If user press q key game quits
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            # Ship won't move rightwards
            self.ship.moving_right = False
        # If key released was left key
        elif event.key == pygame.K_LEFT:
            # Ship won't move left
            self.ship.moving_left = False

    def _ship_hit(self):
        """Respond to ship being hit by alien"""

        # if there is still ships left game continues
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1
            # update ships left
            self.sb.prep_ships()

            # Delete remaining enemies and bullets
            self.aliens.empty()
            self.bullets.empty()

            # create a new fleet and center ship
            self._create_fleet()
            # coordinate response when enemy hits ship
            self.ship.center_ship()
        # if there is no ships game stops
        else:
            self.stats.game_active = False
            # show cursor
            pygame.mouse.set_visible(True)

        # pause game briefly for regrouping
        sleep(0.5)

    def _create_alien(self, alien_num, row_num):
        # create alien
        alien = Alien(self)
        # get alien width and height
        alien_width, alien_height = alien.rect.size
        # place alien in row
        # for every alien created each alien is move 1 alien width right
        alien.x = alien_width + 2 * alien_width * alien_num
        # set alien rect position
        alien.rect.x = alien.x
        # create space for aliens below row
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_num
        # Add alien to group fleet
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond if any alien hits the edges"""
        # access aliens group list
        for alien in self.aliens.sprites():
            # check edges on whole fleet of aliens
            if alien.check_edges():
                # if alien is at edge, whole fleet needs to change directions
                self._check_fleet_direction()
                # loop stops when fleet need to change directions
                break

    def _check_fleet_direction(self):
        """Drop entire fleet and change directions"""
        for alien in self.aliens.sprites():
            # loop through each alien and drop each alien according to drop speed
            alien.rect.y += self.settings.fleet_drop_speed
        # change direction of fleet once by multiplying -1 every time fleet has to change directions
        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        # check for any bullets hitting aliens (collision)
        # get rid of bullet and alien after collision
        # groupcollide() compare positions of all bullets and all aliens for any overlap positions/collisions
        # A dictionary is returned containing the bullet and list of aliens hit by bullet as key/value pair
        # groupcollide(,,True, True) tells pygame to delete bullet and alien if collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)  # collisions of bullet-alien
        # if bullet hits an alien
        if collisions:
            # iterate through list of collided aliens
            for aliens in collisions.values():
                # increase score for every alien hit
                self.stats.score += self.settings.alien_points * len(aliens)
            # update score
            self.sb.prep_score()
            # update high score after aliens is hit by bullets
            self.sb.check_high_score()
        # if all aliens in current fleet are dead (if there is no aliens)
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            # Delete existing bullets, empty() deletes all elements
            self.bullets.empty()
            # create a new fleet
            self._create_fleet()
            # increase game for next fleet
            self.settings.increase_speed()

            # increase level count if fleet is destroyed
            self.stats.level += 1
            # update level count
            self.sb.prep_level()

    def _check_aliens_bottom(self):
        """Check if aliens reached the bottom"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            # if one alien hits the bottom of the screen then ship is hit
            # no need to check if all aliens hit the bottom
            if alien.rect.bottom >= screen_rect.bottom:
                # display same response as alien hitting ship
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """Start new game when player presses play button"""
        # collidepoint() check whether point of mouse click overlaps region defined by button rect
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        # if button is clicked and game active is false (not active)
        if button_clicked and not self.stats.game_active:
            # reset game settings
            self.settings.initialize_dynamic_settings()
            # reset game stats
            self.stats.reset_stats()
            # if play button press game is active
            self.stats.game_active = True
            # reset score to 0 with every new game
            self.sb.prep_score()
            # level image updates
            self.sb.prep_level()
            # how many ships player started with
            self.sb.prep_ships()

            # get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            # hide mouse cursor
            pygame.mouse.set_visible(False)


if __name__ == "__main__":  # If file is called directly
    # Make a game instance and run game
    ai = AlienInvasion()
    ai.Run_Game()
