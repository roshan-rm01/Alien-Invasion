import pygame.font  # render text to the screen


class Button:

    # take ai instance and message as parameters
    def __init__(self, ai_game, msg):
        """Initialize button attributes"""
        self.screen = ai_game.screen
        # get screen rect from main game
        self.screen_rect = self.screen.get_rect()

        # set dimensions and properties
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        # prepare font attribute for rendering text
        # None tells pygame to use default font and 48 is the size of font
        self.font = pygame.font.SysFont(None, 48)

        # Build button rect object and center it
        # position button onto the screen
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # handle rendering of text font which acts as image
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on button"""
        # turn text into image , True - edge of text is smoother
        # Text background is set to same color as button
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        # text is centered on the button
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and draw message"""
        # fill - draw rectangle portion of button
        self.screen.fill(self.button_color, self.rect)
        # blit - draw text image to screen
        self.screen.blit(self.msg_image, self.msg_image_rect)
