import interface
import arcade

# specifies window dimensions; cuurently only supports 1600 x 800 for title screen
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Digital Bullet"

def main():
    """
    This runs whenever the file is run in itself.
    The DigitalBullet is created for the main game.
    """
    laro = interface.DigitalBullet(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    laro.setup()
    arcade.run()

if __name__ == "__main__":
    main()
