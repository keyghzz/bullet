"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import two as engine
import textbutton

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
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
        self.last_mouse_position = None
        self.cardsPlayer1 = None
        self.cardsPlayer2 = None
        self.discardPile = None
        self.deckShow = None
        self.spawn = None
        self.draw_sound = arcade.load_sound("resources/cardTakeOutPackage1.wav")
        self.swap_sound = arcade.load_sound("resources/cardShove3.wav")
        self.place_sound = arcade.load_sound("resources/cardPlace1.wav")
        self.wrong_sound = arcade.load_sound("resources/buzzer_x.wav")
        self.playScreen = True
        self.requestInstructions = False
        self.bulletList = None
        self.background = None

    def setup(self):
        # Create your sprites and sprite lists here
        self.button_list_loadingScreen = [] #buttons in loading screen

        play_button = textbutton.StartTextButton(60, 570, self.play_program)
        self.button_list_loadingScreen.append(play_button)

        continue_button = textbutton.ContinueTextButton(60, 515, self.continue_program)
        self.button_list_loadingScreen.append(continue_button)

        instructions_button = textbutton.InstructionsTextButton(60, 500, self.display_instructions)
        self.button_list_loadingScreen.append(instructions_button)

        leaderboard_button = textbutton.LeaderboardTextButton(60, 500, self.display_leaderboard)
        self.button_list_loadingScreen.append(leaderboard_button)

        self.background = arcade.load_texture("resources/BulletTitleScreen.png")

        self.cardsPlayer1 = arcade.SpriteList()
        self.cardsPlayer2 = arcade.SpriteList()

        self.discardPile = arcade.SpriteList()

        self.deckShow = arcade.SpriteList()
        deckguy = arcade.Sprite("resources/cardBack_red1.png", 0.9)
        deckguy.center_x = (SCREEN_WIDTH//2-(264))
        deckguy.center_y = (SCREEN_HEIGHT//2)
        self.deckShow.append(deckguy)

        self.spawn = arcade.SpriteList()

        self.playArea = arcade.Sprite("resources/playArea.png", 0.85)
        self.playArea.center_x = (SCREEN_WIDTH//2+(264))
        self.playArea.center_y = (SCREEN_HEIGHT//2)

        self.bulletList = arcade.SpriteList()

    def bootStart(self):
        first = arcade.Sprite(engine.getimgStr(engine.Game.discardCoord), 0.9)
        first.center_x = (SCREEN_WIDTH//2+(264))
        first.center_y = (SCREEN_HEIGHT//2)
        self.discardPile.append(first)

        bullet1 = arcade.Sprite("resources/bullet.png")
        bullet1.position = (SCREEN_WIDTH*3//4, 275)
        bullet1.bind = "p1"

        bullet2 = arcade.Sprite("resources/bullet2.png")
        bullet2.position = (SCREEN_WIDTH//4, 525)
        bullet2.bind = "p2"

        self.bulletList.append(bullet1)
        self.bulletList.append(bullet2)

        self.cardsPlayer1, self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val = engine.Game.refreshPlayers(self.cardsPlayer1,
        self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val, engine.Game.Player1.hand, engine.Game.Player2.hand, SCREEN_HEIGHT)

    def play_program(self):
        self.button_list_loadingScreen = []
        self.playScreen = False
        #code for making Game
        engine.Game = engine.Game([])
        self.bootStart()

    def continue_program(self):
        self.button_list_loadingScreen = []
        self.playScreen = False
        #code for making Game
        engine.Game = engine.Game(engine.loadProgress())
        self.bootStart()

    def display_instructions(self):
        print("Insert Instructions Here")

    def display_leaderboard(self):
        print("Leaderboard Displayed")

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        if not self.playScreen and not self.requestInstructions:
            # Call draw() on all your sprite lists below
            if engine.Game.Player1.turn:
                arcade.draw_text("YOUR TURN",
                            SCREEN_WIDTH//2, 275, arcade.color.WHITE, 50, width=500, align="center",
                            anchor_x="center", anchor_y="center", font_name = "resources/FSEX302.ttf")
            elif engine.Game.Player2.turn:
                arcade.draw_text("YOUR TURN",
                            SCREEN_WIDTH//2, 525, arcade.color.WHITE, 50, width=500, align="center",
                            anchor_x="center", anchor_y="center", font_name = "resources/FSEX302.ttf", rotation = 180.0)
            else:
                if engine.Game.hasWon == "Player 1":
                    arcade.draw_text("YOU WIN!",
                                SCREEN_WIDTH//2, 275, arcade.color.WHITE, 50, width=500, align="center",
                                anchor_x="center", anchor_y="center", font_name = "resources/FSEX302.ttf")
                    arcade.draw_text("YOU LOSE!",
                                SCREEN_WIDTH//2, 525, arcade.color.WHITE, 50, width=500, align="center",
                                anchor_x="center", anchor_y="center", font_name = "resources/FSEX302.ttf", rotation = 180.0)
                elif engine.Game.hasWon == "Player 2":
                    arcade.draw_text("YOU LOSE!",
                                SCREEN_WIDTH//2, 275, arcade.color.WHITE, 50, width=500, align="center",
                                anchor_x="center", anchor_y="center", font_name = "resources/FSEX302.ttf")
                    arcade.draw_text("YOU WIN!",
                                SCREEN_WIDTH//2, 525, arcade.color.WHITE, 50, width=500, align="center",
                                anchor_x="center", anchor_y="center", font_name = "resources/FSEX302.ttf", rotation = 180.0)
                else:
                    pass
            self.playArea.draw()
            self.bulletList.draw()
            if len(engine.Game.deck) != 0:
                self.deckShow.draw()
            self.discardPile.draw()
            self.cardsPlayer1.draw()
            self.cardsPlayer2.draw()
            self.spawn.draw()

        elif self.playScreen:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                  1600, 800, self.background)
            for button in self.button_list_loadingScreen:
                button.draw()
        elif self.requestInstructions:
            for button in self.button_list_instructions:
                button.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.sino_hatak is not None:
            self.sino_hatak.position = self.last_mouse_position
        if not self.playScreen and not self.requestInstructions:
            self.playArea.update()
            self.spawn.update()
            self.discardPile.update()
            self.cardsPlayer1.update()
            self.cardsPlayer2.update()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        if self.playScreen:
            textbutton.check_mouse_hovering_for_buttons(x, y, self.button_list_loadingScreen)
        elif self.requestInstructions:
            textbutton.check_mouse_hovering_for_buttons(x, y, self.button_list_instructions)

        if self.sino_hatak is not None:
            self.last_mouse_position = x, y
            self.sino_hatak.position = self.last_mouse_position

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if self.playScreen:
            textbutton.check_mouse_press_for_buttons(x, y, self.button_list_loadingScreen)
            textbutton.check_mouse_press_for_buttons(x, y, self.button_list_instructions)

        elif button == arcade.MOUSE_BUTTON_LEFT:
            toDrag = arcade.get_sprites_at_point((x,y), self.cardsPlayer1)
            toDrag += arcade.get_sprites_at_point((x,y), self.cardsPlayer2)
            toDrag += arcade.get_sprites_at_point((x,y), self.spawn)
            deckClick = arcade.get_sprites_at_point((x,y), self.deckShow)
            discardClick = arcade.get_sprites_at_point((x,y), self.discardPile)
            bulletClick = arcade.get_sprites_at_point((x,y), self.bulletList)

            if (len(toDrag) > 0):
                if engine.Game.specialTurn:
                    if len(self.spawn) != 0 and toDrag[0] == self.spawn[0] and engine.Game.specialMove != "Swap a card with the opponent.":
                        self.sino_hatak = None
                    else:
                        self.sino_hatak = toDrag[0]
                self.last_mouse_position = x, y
            elif len(deckClick) > 0 and len(self.spawn) == 0 and len(engine.Game.deck) != 0:
                print("Deck clicked.")
                cardTup, engine.Game.deck = engine.drawfromDeck(1, engine.Game.deck)
                card = arcade.Sprite(engine.getimgStr(cardTup[0]), 0.9)
                card.position = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
                self.spawn.append(card)
                engine.Game.spawnCoord = cardTup[0]
                engine.Game.hasDrawn(True)
                arcade.play_sound(self.draw_sound)
                if engine.isSpecial(engine.Game.spawnCoord):
                    engine.Game.getAction(engine.Game.spawnCoord)
                if len(engine.Game.deck) == 0:
                        engine.Game.lastTurn = True
            elif len(discardClick) != 0:
                self.sino_hatak = discardClick[len(discardClick)-1]
                self.last_mouse_position = x, y
            elif len(bulletClick) != 0 and engine.Game.lastTurn == False and not engine.Game.specialTurn:
                if bulletClick[0].bind == 'p1' and engine.Game.Player1.turn:
                    print("Player 1 has initiated bullet.")
                    engine.Game.hasBullet()
                elif bulletClick[0].bind == 'p2' and engine.Game.Player2.turn:
                    print("Player 2 has initiated bullet.")
                    engine.Game.hasBullet()

            if engine.Game.specialTurn:
                if engine.Game.specialMove == "View your own card.":
                    if engine.Game.Player1.turn:
                        own = arcade.get_sprites_at_point((x,y), self.cardsPlayer1)
                        if len(own) != 0:
                            show = arcade.Sprite((engine.getimgStr(engine.Game.Player1.sprite2val[own[0]])), 0.9)
                            show.position = own[0].position
                            self.cardsPlayer1.append(show)
                            engine.Game.specialTurn = False
                            engine.Game.specialMove = ""
                    elif engine.Game.Player2.turn:
                        own = arcade.get_sprites_at_point((x,y), self.cardsPlayer2)
                        if len(own) != 0:
                            show = arcade.Sprite((engine.getimgStr(engine.Game.Player2.sprite2val[own[0]])), 0.9)
                            show.position = own[0].position
                            self.cardsPlayer2.append(show)
                            engine.Game.specialTurn = False
                            engine.Game.specialMove = ""
                elif engine.Game.specialMove == "See the opponent's card.":
                    if engine.Game.Player1.turn:
                        own = arcade.get_sprites_at_point((x,y), self.cardsPlayer2)
                        if len(own) != 0:
                            show = arcade.Sprite((engine.getimgStr(engine.Game.Player2.sprite2val[own[0]])), 0.9)
                            show.position = own[0].position
                            self.cardsPlayer2.append(show)
                            engine.Game.specialTurn = False
                            engine.Game.specialMove = ""
                    elif engine.Game.Player2.turn:
                        own = arcade.get_sprites_at_point((x,y), self.cardsPlayer1)
                        if len(own) != 0:
                            show = arcade.Sprite((engine.getimgStr(engine.Game.Player1.sprite2val[own[0]])), 0.9)
                            show.position = own[0].position
                            self.cardsPlayer1.append(show)
                            engine.Game.specialTurn = False
                            engine.Game.specialMove = ""
                elif engine.Game.specialMove == "Your opponent's hand is shuffled.":
                    if engine.Game.Player1.turn:
                        engine.Game.Player2.shuffle()
                        engine.Game.specialTurn = False
                        engine.Game.specialMove = ""
                    elif engine.Game.Player2.turn:
                        engine.Game.Player1.shuffle()
                        engine.Game.specialTurn = False
                        engine.Game.specialMove = ""
                else:
                    pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        if self.playScreen:
            textbutton.check_mouse_release_for_buttons(x, y, self.button_list_loadingScreen)
            textbutton.check_mouse_release_for_buttons(x, y, self.button_list_instructions)
        #releases the card being dragged at mouse release
        hatak_last = self.sino_hatak
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.sino_hatak = None

        #checks if "sapaw" is initiated, i.e. if card is placed on discardPile
        p1Sapaw = arcade.check_for_collision_with_list(self.playArea, self.cardsPlayer1)
        if p1Sapaw != [] and engine.Game.Player1.hasDrawn == False:
            self.discardPile, engine.Game.Player1.hand, self.cardsPlayer1, isWrong = engine.Game.sapaw(p1Sapaw[0],
            self.discardPile, engine.Game.Player1.hand, engine.Game.Player1.sprite2val, self.cardsPlayer1,
            SCREEN_WIDTH, SCREEN_HEIGHT)
            self.cardsPlayer1, self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val = engine.Game.refreshPlayers(self.cardsPlayer1,
            self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val, engine.Game.Player1.hand, engine.Game.Player2.hand, SCREEN_HEIGHT)
            arcade.play_sound(self.place_sound)
            if isWrong:
                arcade.play_sound(self.wrong_sound)

        p2Sapaw = arcade.check_for_collision_with_list(self.playArea, self.cardsPlayer2)
        if p2Sapaw != [] and engine.Game.Player2.hasDrawn == False:
            self.discardPile, engine.Game.Player2.hand, self.cardsPlayer2, isWrong = engine.Game.sapaw(p2Sapaw[0],
            self.discardPile, engine.Game.Player2.hand, engine.Game.Player2.sprite2val, self.cardsPlayer2,
            SCREEN_WIDTH, SCREEN_HEIGHT)
            self.cardsPlayer1, self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val = engine.Game.refreshPlayers(self.cardsPlayer1,
            self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val, engine.Game.Player1.hand, engine.Game.Player2.hand, SCREEN_HEIGHT)
            arcade.play_sound(self.place_sound)
            if isWrong:
                arcade.play_sound(self.wrong_sound)

        dispose = arcade.check_for_collision_with_list(self.playArea, self.spawn)
        if dispose != []:
            print("Spawn was disposed.")
            self.discardPile, self.spawn = engine.Game.spawn2discard(dispose[0], self.discardPile, self.spawn, SCREEN_WIDTH, SCREEN_HEIGHT)
            engine.Game.endTurn()
            self.cardsPlayer1, self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val = engine.Game.refreshPlayers(self.cardsPlayer1,
            self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val, engine.Game.Player1.hand, engine.Game.Player2.hand, SCREEN_HEIGHT)
            arcade.play_sound(self.place_sound)

        if len(self.spawn) > 0:
            p1SpawnSwap = arcade.check_for_collision_with_list(self.spawn[0], self.cardsPlayer1)
            p2SpawnSwap = arcade.check_for_collision_with_list(self.spawn[0], self.cardsPlayer2)
            if engine.Game.specialTurn:
                p1SpawnSwap = []
                p2SpawnSwap = []
            if p1SpawnSwap != [] and engine.Game.Player1.turn == True:
                print("Player 1 spawn swapped.")
                self.discardPile, self.spawn, engine.Game.Player1.hand = engine.Game.spawnSwap(p1SpawnSwap[0], self.discardPile, self.spawn,
                engine.Game.Player1.hand, engine.Game.Player1.sprite2val, SCREEN_WIDTH, SCREEN_HEIGHT)
                engine.Game.endTurn()
                self.cardsPlayer1, self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val = engine.Game.refreshPlayers(self.cardsPlayer1,
                self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val, engine.Game.Player1.hand, engine.Game.Player2.hand, SCREEN_HEIGHT)
                arcade.play_sound(self.swap_sound)

            elif p2SpawnSwap != [] and engine.Game.Player2.turn == True:
                print("Player 2 spawn swapped.")
                self.discardPile, self.spawn, engine.Game.Player2.hand = engine.Game.spawnSwap(p2SpawnSwap[0], self.discardPile, self.spawn,
                engine.Game.Player2.hand, engine.Game.Player2.sprite2val, SCREEN_WIDTH, SCREEN_HEIGHT)
                engine.Game.endTurn()
                self.cardsPlayer1, self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val = engine.Game.refreshPlayers(self.cardsPlayer1,
                self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val, engine.Game.Player1.hand, engine.Game.Player2.hand, SCREEN_HEIGHT)
                arcade.play_sound(self.swap_sound)

            else:
                self.cardsPlayer1, self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val = engine.Game.refreshPlayers(self.cardsPlayer1,
                self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val, engine.Game.Player1.hand, engine.Game.Player2.hand, SCREEN_HEIGHT)
                self.spawn[0].position = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)

        if len(self.discardPile) > 0:
            p1DiscardSwap = arcade.check_for_collision_with_list(self.discardPile[len(self.discardPile)-1], self.cardsPlayer1)
            p2DiscardSwap = arcade.check_for_collision_with_list(self.discardPile[len(self.discardPile)-1], self.cardsPlayer2)

            if p1DiscardSwap != [] and engine.Game.Player1.turn == True and engine.Game.Player1.hasDrawn == False:
                print("Player 1 discard swapped.")
                self.discardPile, engine.Game.Player1.hand = engine.Game.discardSwap(p1DiscardSwap[0], self.discardPile,
                engine.Game.Player1.hand, engine.Game.Player1.sprite2val, SCREEN_WIDTH, SCREEN_HEIGHT)
                engine.Game.endTurn()
                self.cardsPlayer1, self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val = engine.Game.refreshPlayers(self.cardsPlayer1,
                self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val, engine.Game.Player1.hand, engine.Game.Player2.hand, SCREEN_HEIGHT)
                arcade.play_sound(self.swap_sound)

            elif p2DiscardSwap != [] and engine.Game.Player2.turn == True and engine.Game.Player2.hasDrawn == False:
                print("Player 2 discard swapped.")
                self.discardPile, engine.Game.Player2.hand = engine.Game.discardSwap(p2DiscardSwap[0], self.discardPile,
                engine.Game.Player2.hand, engine.Game.Player2.sprite2val, SCREEN_WIDTH, SCREEN_HEIGHT)
                engine.Game.endTurn()
                self.cardsPlayer1, self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val = engine.Game.refreshPlayers(self.cardsPlayer1,
                self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val, engine.Game.Player1.hand, engine.Game.Player2.hand, SCREEN_HEIGHT)
                arcade.play_sound(self.swap_sound)

            else:
                self.cardsPlayer1, self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val = engine.Game.refreshPlayers(self.cardsPlayer1,
                self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val, engine.Game.Player1.hand, engine.Game.Player2.hand, SCREEN_HEIGHT)
                self.discardPile[len(self.discardPile)-1].position = (SCREEN_WIDTH//2+264,SCREEN_HEIGHT//2)

        if engine.Game.specialTurn and engine.Game.specialMove == "Swap a card with the opponent.":
            if hatak_last != None:
                swap1 = arcade.check_for_collision_with_list(hatak_last, self.cardsPlayer1)
                swap2 = arcade.check_for_collision_with_list(hatak_last, self.cardsPlayer2)
            else:
                swap1 = []
                swap2 = []
            print(swap1, swap2)

            print(engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val)
            if len(swap2) != 0:
                swapval1 = engine.Game.Player1.sprite2val[hatak_last]
                swapval2 = engine.Game.Player2.sprite2val[swap2[0]]
                index1 = engine.Game.Player1.hand.index(swapval1)
                index2 = engine.Game.Player2.hand.index(swapval2)
                engine.Game.Player1.hand.remove(swap2val1)
                engine.Game.Player2.hand.remove(swap2val2)
                engine.Game.Player1.hand.insert(index1, swap2val2)
                engine.Game.Player2.hand.insert(index2, swap2val1)
                engine.Game.specialTurn = False
                engine.Game.specialMove = ""
                engine.Game.endTurn()
                arcade.play_sound(self.swap_sound)
            elif len(swap1) != 0:
                swapval1 = engine.Game.Player1.sprite2val[swap1[0]]
                swapval2 = engine.Game.Player2.sprite2val[hatak_last]
                index1 = engine.Game.Player1.hand.index(swapval1)
                index2 = engine.Game.Player2.hand.index(swapval2)
                engine.Game.Player1.hand.remove(swap2val1)
                engine.Game.Player2.hand.remove(swap2val2)
                engine.Game.Player1.hand.insert(index1, swap2val2)
                engine.Game.Player2.hand.insert(index2, swap2val1)
                engine.Game.specialTurn = False
                engine.Game.specialMove = ""
                engine.Game.endTurn()
                arcade.play_sound(self.swap_sound)

def refreshHand(hand, spriteList, tup):
    spriteList = arcade.SpriteList()
    sprite2val = {}
    if len(hand) != 0:
        for count, x in enumerate(hand):
            card = arcade.Sprite("resources/cardBack_red1.png",0.9)
            card.position = tup
            spriteList.move(-264,0)
            spriteList.append(card)
            sprite2val[card] = x
        spriteList.move((SCREEN_WIDTH//2)-spriteList.center[0],0)
    return spriteList, sprite2val

def val2sprite(val, spritepos):
    new = arcade.Sprite(engine.getimgStr(val), 0.9)
    new.position = spritepos
    return new

def main():
    """ Main method """
    laro = DigitalBullet(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    laro.setup()
    arcade.run()

if __name__ == "__main__":
    main()
