import arcade

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Digital Bullet"

class TextButton:
    """ Text-based button """

    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=40,
                 font_name="resources/FSEX302.ttf",
                 face_color=arcade.color.AMAZON,
                 highlight_color=arcade.color.AMAZON,
                 shadow_color=arcade.color.AMAZON,
                 button_height=2):
        self.center_x = SCREEN_WIDTH//2
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_name = font_name
        self.pressed = False
        self.hover = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        """ Draw the button """
        if not self.pressed:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                        self.height, self.face_color)
        else:
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                        self.height, arcade.color.BLACK_LEATHER_JACKET)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        if not self.hover:
            arcade.draw_text(self.text, x, y,
                            arcade.color.WHITE, font_size=self.font_size, font_name="resources/FSEX302.ttf",
                            width=self.width, align="center",
                            anchor_x="center", anchor_y="center")
        else:
            arcade.draw_text(self.text, x, y,
                            arcade.color.DAFFODIL, font_size=self.font_size, font_name="resources/FSEX302.ttf",
                            width=self.width, align="center",
                            anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False

    def hovering(self):
        self.hover = True

    def not_hovering(self):
        self.hover = False

def check_mouse_press_for_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()


def check_mouse_release_for_buttons(_x, _y, button_list):
    """ If a mouse button has been released, see if we need to process
        any release events. """
    for button in button_list:
        if button.pressed:
            button.on_release()

def check_mouse_hovering_for_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            button.not_hovering()
            continue
        if x < button.center_x - button.width / 2:
            button.not_hovering()
            continue
        if y > button.center_y + button.height / 2:
            button.not_hovering()
            continue
        if y < button.center_y - button.height / 2:
            button.not_hovering()
            continue
        button.hovering()

class StartTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, (SCREEN_HEIGHT//2 + 120), 500, 100, "Start New Game", 35, "resources/FSEX302.ttf")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


class ContinueTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, (SCREEN_HEIGHT//2), 500, 100, "Continue", 35, "resources/FSEX302.ttf")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

class InstructionsTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, (SCREEN_HEIGHT//2 - 120), 500, 100, "Instructions", 35, "resources/FSEX302.ttf")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()
