"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import two as engine

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Digital Bullet"

class DigitalBullet(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)
        self.sino_hatak = None
        self.last_mouse_position = 0, 0
        self.cardsPlayer1 = None
        self.cardsPlayer2 = None
        self.discardPile = None
        self.deckShow = None
        self.spawn = None

    def setup(self):
        # Create your sprites and sprite lists here
        self.cardsPlayer1 = arcade.SpriteList()
        self.cardsPlayer2 = arcade.SpriteList()

        self.discardPile = arcade.SpriteList()

        first = arcade.Sprite(engine.getimgStr(engine.Game.discardCoord), 0.9)
        first.center_x = (SCREEN_WIDTH//2+264)
        first.center_y = (SCREEN_HEIGHT//2)

        self.discardPile.append(first)

        self.deckShow = arcade.SpriteList()
        deckguy = arcade.Sprite("resources/cardBack_red1.png", 0.9)
        deckguy.center_x = (SCREEN_WIDTH//2-264)
        deckguy.center_y = (SCREEN_HEIGHT//2)
        self.deckShow.append(deckguy)

        self.spawn = arcade.SpriteList()

        self.playArea = arcade.Sprite("resources/playArea.png", 0.85)
        self.playArea.center_x = (SCREEN_WIDTH//2+264)
        self.playArea.center_y = (SCREEN_HEIGHT//2)

        self.cardsPlayer1, engine.Game.sprite2val1 = self.refreshHand(engine.Game.Player1.hand, self.cardsPlayer1, (70, 145))

        self.cardsPlayer2, engine.Game.sprite2val2 = self.refreshHand(engine.Game.Player2.hand, self.cardsPlayer2, (70, SCREEN_HEIGHT-145))

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        if engine.Game.Player1.turn == True:
            arcade.draw_text("YOUR TURN",
                         SCREEN_WIDTH//2, 300, arcade.color.WHITE, 50, width=500, align="center",
                         anchor_x="center", anchor_y="center", font_name = "resources/FSEX302.ttf")
        else:
            arcade.draw_text("YOUR TURN",
                         SCREEN_WIDTH//2, 700, arcade.color.WHITE, 50, width=500, align="center",
                         anchor_x="center", anchor_y="center", font_name = "resources/FSEX302.ttf", rotation = 180.0)
        self.playArea.draw()
        self.cardsPlayer1.draw()
        self.cardsPlayer2.draw()
        if len(engine.Game.deck) != 0:
            self.deckShow.draw()
        self.discardPile.draw()
        self.spawn.draw()


    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.sino_hatak is not None:
            self.sino_hatak.position = self.last_mouse_position

        self.playArea.update()
        self.spawn.update()
        self.discardPile.update()
        self.cardsPlayer1.update()
        self.cardsPlayer2.update()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        if self.sino_hatak is not None:
            self.last_mouse_position = x, y
            self.sino_hatak.position = self.last_mouse_position

    def on_mouse_press(self, x, y, button, key_modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            toDrag = arcade.get_sprites_at_point((x,y), self.cardsPlayer1)
            toDrag += arcade.get_sprites_at_point((x,y), self.cardsPlayer2)
            toDrag += arcade.get_sprites_at_point((x,y), self.spawn)
            deckClick = arcade.get_sprites_at_point((x,y), self.deckShow)
            discardClick = arcade.get_sprites_at_point((x,y), self.discardPile)
            if len(toDrag) > 0:
                self.sino_hatak = toDrag[0]
                self.last_mouse_position = x, y
            elif len(deckClick) > 0 and len(self.spawn) == 0:
                cardTup, engine.Game.deck = engine.drawfromDeck(1, engine.Game.deck)
                if len(cardTup) != 0:
                    card = arcade.Sprite(engine.getimgStr(cardTup[0]), 0.9)
                    card.position = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                    self.spawn.append(card)
                    engine.Game.spawnCoord = cardTup[0]
                if engine.Game.Player1.turn == True:
                    engine.Game.Player1.hasDrawn = True
                elif engine.Game.Player2.turn == True:
                    engine.Game.Player2.hasDrawn = True
            elif len(discardClick) != 0:
                self.sino_hatak = discardClick[len(discardClick)-1]
                self.last_mouse_position = x, y
                #if len==0 INITIATE WIN SEQUENCE
        """
        Called when the user presses a mouse button.
        """

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        #releases the card being dragged at mouse release
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.sino_hatak = None

        #checks if "sapaw" is initiated, i.e. if card is placed on discardPile
        p1Sapaw = arcade.check_for_collision_with_list(self.playArea, self.cardsPlayer1)
        if p1Sapaw != [] and engine.Game.Player1.hasDrawn == False:
            self.discardPile, engine.Game.discardCoord, engine.Game.Player1, self.cardsPlayer1,
            engine.Game.sprite2val1 = engine.sapaw(engine.Game, p1Sapaw[0], self.discardPile, engine.Game.discardCoord,
            engine.Game.Player1, self.cardsPlayer1, engine.Game.sprite2val1, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.refreshPlayers()
        #dito tumigil!!!
        p2Sapaw = arcade.check_for_collision_with_list(self.playArea, self.cardsPlayer2)
        if p2Sapaw != [] and engine.Game.Player2.hasDrawn == False:
            self.discardPile, engine.Game.discardCoord, engine.Game.Player2, self.cardsPlayer2,
            engine.Game.sprite2val2 = engine.sapaw(engine.Game, p2Sapaw[0], self.discardPile, engine.Game.discardCoord,
            engine.Game.Player2, self.cardsPlayer2, engine.Game.sprite2val2, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.refreshPlayers()

        if arcade.check_for_collision_with_list(self.playArea, self.spawn) != []:
            for card in arcade.check_for_collision_with_list(self.playArea, self.spawn):
                card.position = (SCREEN_WIDTH//2+264, SCREEN_HEIGHT//2)
                self.discardPile.append(card)
                engine.Game.discardCoord = engine.Game.spawnCoord
                self.spawn.remove(card)
            if engine.Game.Player1.turn == True:
                engine.Game.Player1.hasDrawn = False
            elif engine.Game.Player2.turn == True:
                engine.Game.Player2.hasDrawn = False
            self.endTurn()

        if len(self.spawn) > 0:
            if arcade.check_for_collision_with_list(self.spawn[0], self.cardsPlayer1) != [] and engine.Game.Player1.turn == True:
                #make this a function
                for card in arcade.check_for_collision_with_list(self.spawn[0], self.cardsPlayer1):
                    card.position = (SCREEN_WIDTH//2+264, SCREEN_HEIGHT//2)
                    self.discardPile.append(card)
                    engine.Game.discardCoord = engine.Game.sprite2val1[card]
                    iOfC = engine.Game.Player1.hand.index(engine.Game.sprite2val1[card])
                    engine.Game.Player1.hand.remove(engine.Game.sprite2val1[card])
                    engine.Game.Player1.hand.insert(iOfC, engine.Game.spawnCoord)
                    self.spawn.remove(self.spawn[0])
                engine.Game.Player1.hasDrawn = False
                self.endTurn()

            elif arcade.check_for_collision_with_list(self.spawn[0], self.cardsPlayer2) != [] and engine.Game.Player2.turn == True:
                #same here
                for card in arcade.check_for_collision_with_list(self.spawn[0], self.cardsPlayer2):
                    card.position = (SCREEN_WIDTH//2+264, SCREEN_HEIGHT//2)
                    self.discardPile.append(card)
                    engine.Game.discardCoord = engine.Game.sprite2val2[card]
                    iOfC = engine.Game.Player2.hand.index(engine.Game.sprite2val2[card])
                    engine.Game.Player2.hand.remove(engine.Game.sprite2val2[card])
                    engine.Game.Player2.hand.insert(iOfC, engine.Game.spawnCoord)
                    self.spawn.remove(self.spawn[0])
                engine.Game.Player2.hasDrawn = False
                self.endTurn()
            else:
                self.refreshPlayers()
                self.spawn[0].position = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)

        if len(self.discardPile) > 0:
            if arcade.check_for_collision_with_list(self.discardPile[len(self.discardPile)-1], self.cardsPlayer1) != [] and engine.Game.Player1.turn == True and engine.Game.Player1.hasDrawn == False:
                #same here
                for card in arcade.check_for_collision_with_list(self.discardPile[len(self.discardPile)-1], self.cardsPlayer1):
                    card.position = (SCREEN_WIDTH//2+264, SCREEN_HEIGHT//2)
                    self.discardPile.remove(self.discardPile[len(self.discardPile)-1])
                    self.discardPile.append(card)
                    iOfC = engine.Game.Player1.hand.index(engine.Game.sprite2val1[card])
                    engine.Game.Player1.hand.insert(iOfC, engine.Game.discardCoord)
                    engine.Game.Player1.hand.remove(engine.Game.sprite2val1[card])
                    engine.Game.discardCoord = engine.Game.sprite2val1[card]
                self.endTurn()
            elif arcade.check_for_collision_with_list(self.discardPile[len(self.discardPile)-1], self.cardsPlayer2) != [] and engine.Game.Player2.turn == True and engine.Game.Player2.hasDrawn == False:
                #last na
                for card in arcade.check_for_collision_with_list(self.discardPile[len(self.discardPile)-1], self.cardsPlayer2):
                    card.position = (SCREEN_WIDTH//2+264, SCREEN_HEIGHT//2)
                    self.discardPile.remove(self.discardPile[len(self.discardPile)-1])
                    self.discardPile.append(card)
                    iOfC = engine.Game.Player2.hand.index(engine.Game.sprite2val2[card])
                    engine.Game.Player2.hand.insert(iOfC, engine.Game.discardCoord)
                    engine.Game.Player2.hand.remove(engine.Game.sprite2val2[card])
                    engine.Game.discardCoord = engine.Game.sprite2val2[card]
                self.endTurn()
            else:
                self.refreshPlayers()
                self.discardPile[len(self.discardPile)-1].position = (SCREEN_WIDTH//2+264,SCREEN_HEIGHT//2)

    def endTurn(self):
        engine.Game.Player1.turn = not engine.Game.Player1.turn
        engine.Game.Player2.turn = not engine.Game.Player2.turn
        self.refreshPlayers()

    def refreshHand(self, hand, spriteList, tup):
        spriteList = arcade.SpriteList()
        sprite2val = {}
        if len(hand) != 0:
            for x in hand:
                card = arcade.Sprite(engine.getimgStr(x),0.9)
                card.position = tup
                spriteList.move(-264,0)
                spriteList.append(card)
                sprite2val[card] = x
            spriteList.move((SCREEN_WIDTH//2)-spriteList.center[0],0)
        return spriteList, sprite2val

    def refreshPlayers(self):
        self.cardsPlayer1, engine.Game.sprite2val1 = self.refreshHand(engine.Game.Player1.hand, self.cardsPlayer1, (70, 145))
        self.cardsPlayer2, engine.Game.sprite2val2 = self.refreshHand(engine.Game.Player2.hand, self.cardsPlayer2, (70, SCREEN_HEIGHT-145))

def main():
    """ Main method """
    laro = DigitalBullet(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    laro.setup()
    arcade.run()


if __name__ == "__main__":
    main()
