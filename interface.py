import arcade
import engine
import textbutton
import os

# specifies window dimensions; cuurently only supports 1600 x 800 for title screen
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Digital Bullet"

class DigitalBullet(arcade.Window):
    '''
    This is a class for the Arcade Window which contains
    everything to do with the game's graphics.
    '''
    def __init__(self, width, height, title):
        '''
        This initializes the objects to be used
        '''
        # makes screen dimensions and title callable throughout the class
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON) # background color
        self.sino_hatak = None # variable for dragging mechanism (to be explained at length)
        self.last_mouse_position = None # same as above

        # SpriteList objects to be used later on
        self.cardsPlayer1 = None
        self.cardsPlayer2 = None
        self.discardPile = None
        self.deckShow = None
        self.spawn = None
        self.bulletList = None

        # sounds to be played
        self.draw_sound = arcade.load_sound("resources/cardTakeOutPackage1.wav")
        self.swap_sound = arcade.load_sound("resources/cardShove3.wav")
        self.place_sound = arcade.load_sound("resources/cardPlace1.wav")
        self.wrong_sound = arcade.load_sound("resources/buzzer_x.wav")

        # booleans for screen display
        self.playScreen = True
        self.requestInstructions = False
        self.requestLeaderboard = False

        # texture for background
        self.background = None

        # sprite for leaderboard and instructions
        self.leaderboard = None
        self.toDrawI = None

    def setup(self):
        '''
        This function is called when the window is first created.
        It initializes the SpriteList objects that will be used for storing the sprites.
        '''
        # list for buttons in loading screen
        self.button_list_loadingScreen = []

        play_button = textbutton.StartTextButton(60, 570, self.play_program)
        self.button_list_loadingScreen.append(play_button)

        continue_button = textbutton.ContinueTextButton(60, 515, self.continue_program)
        self.button_list_loadingScreen.append(continue_button)

        instructions_button = textbutton.InstructionsTextButton(60, 500, self.display_instructions)
        self.button_list_loadingScreen.append(instructions_button)

        leaderboard_button = textbutton.LeaderboardTextButton(60, 500, self.display_leaderboard)
        self.button_list_loadingScreen.append(leaderboard_button)

        # background image of loading screen
        self.background = arcade.load_texture("resources/BulletTitleScreen.png")

        # creates the leaderboard sprite
        self.leaderboard = arcade.Sprite("resources/leaderboard.png", 0.3)
        self.leaderboard.center_x = (SCREEN_WIDTH//2)
        self.leaderboard.center_y = (SCREEN_HEIGHT//2)

        # SpriteList objects for players' cards
        self.cardsPlayer1 = arcade.SpriteList()
        self.cardsPlayer2 = arcade.SpriteList()

        # SpriteList object for discard pile cards
        self.discardPile = arcade.SpriteList()

        # SpriteList and Sprite objects for the deck
        self.deckShow = arcade.SpriteList()
        deckguy = arcade.Sprite("resources/cardBack_red1.png", 0.9)
        deckguy.center_x = (SCREEN_WIDTH//2-(264))
        deckguy.center_y = (SCREEN_HEIGHT//2)
        self.deckShow.append(deckguy)

        # SpriteList object for spawn - buffer where drawn cards go
        self.spawn = arcade.SpriteList()

        # transparent Sprite object for discard pile - cards that collide with this object are played
        self.playArea = arcade.Sprite("resources/playArea.png", 0.85)
        self.playArea.center_x = (SCREEN_WIDTH//2+(264))
        self.playArea.center_y = (SCREEN_HEIGHT//2)

        # SpriteList object for the bullets needed - "bullet" mechanic of the game
        self.bulletList = arcade.SpriteList()
        bullet1 = arcade.Sprite("resources/bullet.png")
        bullet1.position = (SCREEN_WIDTH*3//4, 275)
        bullet1.bind = "p1" # the bullet's bind indicates the player's side it is located in

        bullet2 = arcade.Sprite("resources/bullet2.png")
        bullet2.position = (SCREEN_WIDTH//4, 525)
        bullet2.bind = "p2"

        self.bulletList.append(bullet1)
        self.bulletList.append(bullet2)

        self.instructionsList = []

    def bootStart(self):
        '''
        This function sets up the game-specific variables such as the players' hands
        and the top card of the discard pile.

        It allows for the loading of these information through the save state.
        '''
        # SpriteList object for the card on top of the discard pile
        first = arcade.Sprite(engine.getimgStr(engine.Game.discardCoord), 0.9)
        first.center_x = (SCREEN_WIDTH//2+(264))
        first.center_y = (SCREEN_HEIGHT//2)
        self.discardPile.append(first)

        # calls the function to refresh the players' hand
        self.cardsPlayer1, self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val = engine.Game.refreshPlayers(self.cardsPlayer1,
        self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val, engine.Game.Player1.hand, engine.Game.Player2.hand, SCREEN_HEIGHT)

    def play_program(self):
        '''
        This function is called when the play button is pressed.
        It renders a new screen and starts a new game.
        '''
        self.button_list_loadingScreen = [] # empties the list for laoding screen buttons to remove button display
        self.playScreen = False # boolean for displaying the loading screen is set to false

        # creates the engine.Game variable of the class Game to initate play
        engine.Game = engine.Game([]) # the "[]" indicates that there is no variable to load
        # initializes the game display on start up
        self.bootStart()

    def continue_program(self):
        '''
        This function is called when the continue button is pressed.
        It renders a new screen and loads the previous game state.
        '''
        self.button_list_loadingScreen = []
        self.playScreen = False

        # creates the engine.Game variable of the class Game to initate play
        engine.Game = engine.Game(engine.loadProgress()) # calls the function to check for and gather variables from the previous game state
        self.bootStart()

    def display_instructions(self):
        '''
        This function is called when the instructions button is pressed.
        It displays the instructions by creating a list of sprites upon each click.
        Every succeeding click iterates over the list until it is empty.
        '''
        self.requestInstructions = True
        for x in range(1,8):
            tempI = arcade.Sprite("resources/INSTRUCTIONS" + str(x) + ".png")
            tempI.position = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            self.instructionsList.append(tempI)
        self.instructionsList.reverse()
        self.toDrawI = self.instructionsList.pop()
        print("The instructions have been displayed.")

    def display_leaderboard(self):
        '''
        This function is called when the leaderboard button is pressed.
        It displays the leaderboard.
        '''
        self.requestLeaderboard = True
        print("The leaderboard has been displayed.")

    def on_draw(self):
        '''
        This function is called every time the update function is called.
        It draws the specified objects on the screen.
        '''
        # This command clears the screen to the background color and erases the objects from the last frame.
        arcade.start_render()

        # This draws game-specific elements on the screen only if the game has started.
        if not self.playScreen:
            # This draws turn and action labels for the players.
            if not engine.Game.specialTurn:
                label = "YOUR TURN"
            else:
                label = engine.Game.specialMove.upper()
            if engine.Game.Player1.turn:
                arcade.draw_text(label,
                            SCREEN_WIDTH//2, 275, arcade.color.WHITE, 40, width=1000, align="center",
                            anchor_x="center", anchor_y="center", font_name = "resources/FSEX302.ttf")
            elif engine.Game.Player2.turn:
                arcade.draw_text(label,
                            SCREEN_WIDTH//2, 525, arcade.color.WHITE, 40, width=1000, align="center",
                            anchor_x="center", anchor_y="center", font_name = "resources/FSEX302.ttf", rotation = 180.0)

            # Since both players' turns are set to False upon win, this function indicates win only if a player has won.
            else:
                # This displays the win result after the game.
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

                # Error catching - nothing should pass through here unless win was called prematurely.
                else:
                    print("Win declaration error.")
            # draws the objects created from bottom to top, i.e. playArea is at the bottom while spawn is at the top
            self.playArea.draw()
            self.bulletList.draw()

            # draws the deck image only while there are cards in the deck.
            if len(engine.Game.deck) != 0:
                self.deckShow.draw()
            self.discardPile.draw()
            self.cardsPlayer1.draw()
            self.cardsPlayer2.draw()
            self.spawn.draw()

        # This draws play screen elements only if the game hasn't started.
        elif self.playScreen:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                  1600, 800, self.background)
            for button in self.button_list_loadingScreen:
                button.draw()

            if self.requestLeaderboard:
                self.leaderboard.draw()
                # This loads the leaderboard from the text file.
                file = 'leaderboard.txt'
                if os.path.exists(file):
                    f = open(file, "r")
                    wincount = f.readlines()
                    p1wins = wincount[1]
                    p2wins = wincount[2]

                    arcade.draw_text(p1wins,
                    SCREEN_WIDTH//2, SCREEN_HEIGHT//2-(30), arcade.color.WHITE, 50,
                    anchor_x="center", anchor_y="center", font_name="resources/FSEX302.ttf")
                    arcade.draw_text(p2wins,
                    SCREEN_WIDTH//2, SCREEN_HEIGHT//2-(120), arcade.color.WHITE, 50,
                    anchor_x="center", anchor_y="center", font_name="resources/FSEX302.ttf")
                else:
                    arcade.draw_text("Player 1: 0",
                    SCREEN_WIDTH//2, SCREEN_HEIGHT//2-(30), arcade.color.WHITE, 50,
                    anchor_x="center", anchor_y="center", font_name="resources/FSEX302.ttf")
                    arcade.draw_text("Player 2: 0",
                    SCREEN_WIDTH//2, SCREEN_HEIGHT//2-(120), arcade.color.WHITE, 50,
                    anchor_x="center", anchor_y="center", font_name="resources/FSEX302.ttf")

            elif self.requestInstructions:
                self.toDrawI.draw()

        else:
            pass

    def on_update(self, delta_time):
        '''
        This function is called for every frame, i.e. ~once every second.
        It allows for object movement and calls on_draw for every run.
        '''
        # If an object is being dragged, update its position based on where the mouse was.
        if self.sino_hatak is not None:
            self.sino_hatak.position = self.last_mouse_position

        # If the game is playing, update the game objects.
        if not self.playScreen and not self.requestInstructions:
            self.playArea.update()
            self.spawn.update()
            self.discardPile.update()
            self.cardsPlayer1.update()
            self.cardsPlayer2.update()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        '''
        This function is called whenever the mouse moves.
        It allows for object movement and button hover.
        '''

        # These allow for button highlighting when the mouse hovers it.
        if self.playScreen:
            textbutton.check_mouse_hovering_for_buttons(x, y, self.button_list_loadingScreen)
        elif self.requestInstructions:
            textbutton.check_mouse_hovering_for_buttons(x, y, self.button_list_instructions)

        # This changes the location of the object being dragged to the mouse's.
        if self.sino_hatak is not None:
            self.last_mouse_position = x, y
            self.sino_hatak.position = self.last_mouse_position

    # This function is called whenever the mouse buttons are pressed.
    def on_mouse_press(self, x, y, button, key_modifiers):

        # This checks if the following buttons are pressed.
        if self.playScreen:
            textbutton.check_mouse_press_for_buttons(x, y, self.button_list_loadingScreen)
            textbutton.check_mouse_press_for_buttons(x, y, self.button_list_instructions)

        # If the game has started, this checks whether the left mouse button is pressed.
        elif button == arcade.MOUSE_BUTTON_LEFT:
            # These creates a list toDrag which specifies objects to drag.
            # Only objects from the specified SpriteList objects may be dragged.
            toDrag = arcade.get_sprites_at_point((x,y), self.cardsPlayer1) # The get_sprites_at_point function returns a list of objects at the x, y coordinate.
            toDrag += arcade.get_sprites_at_point((x,y), self.cardsPlayer2) # The lists are added since these objects are not stacked and located far from each other.
            toDrag += arcade.get_sprites_at_point((x,y), self.spawn) # Thus, only one object is clicked at once.

            # These create lists for respective game-specific elements distinct of the cards.
            deckClick = arcade.get_sprites_at_point((x,y), self.deckShow) # This creates a list for the deck image when clicked. It contains the deck image when clicked; else, it is empty.
            discardClick = arcade.get_sprites_at_point((x,y), self.discardPile) # This creates a list of clicked cards from the discard pile. Either it contains all cards or it is empty.
            bulletClick = arcade.get_sprites_at_point((x,y), self.bulletList) # This creates a list of clicked bullets. At most, one bullet sprite is found here; else, it is empty.

            # This specifies the objects to drag. If the list of objects to be dragged is not empty, the first element is recorded.
            # Since the lists are mutually exclusive, and only one action can be done at a time,
            if (len(toDrag) > 0) and engine.Game.turnCount > 1:
                # If the player has drawn a special turn that does not involve card swapping, card dragging is not allowed unless it is the spawn card.
                # Else, cards may be dragged.
                if engine.Game.specialTurn and engine.Game.specialMove != "Swap a card with the opponent.":
                    if len(self.spawn) != 0 and toDrag[0] == self.spawn[0]:
                        self.sino_hatak = toDrag[0]
                    else:
                        self.sino_hatak = None
                else:
                    self.sino_hatak = toDrag[0]
                # The mouse position is saved for updating the position of the object to be dragged at on_update.
                self.last_mouse_position = x, y

            # This specifies when a card is should be drawn.
            # The deck must be clicked, no card should be on spawn and the deck should not be empty.
            elif len(deckClick) > 0 and len(self.spawn) == 0 and len(engine.Game.deck) != 0 and engine.Game.turnCount > 1:
                print("Deck clicked.")
                cardTup, engine.Game.deck = engine.drawfromDeck(1, engine.Game.deck) # A card is drawn from the deck.
                card = arcade.Sprite(engine.getimgStr(cardTup[0]), 0.9) # It is initialized as a sprite,
                card.position = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2) # set at the location of the spawn,
                self.spawn.append(card) # appended to the spawn pile,
                engine.Game.spawnCoord = cardTup[0] # and stored as the last spawn coordinate.
                engine.Game.hasDrawn(True) # This variable restricts drawing more than one card and other actions while the card is drawn.
                arcade.play_sound(self.draw_sound) # This plays the draw sound.

                # This checks if the drawn card has a special ability.
                if engine.isSpecial(engine.Game.spawnCoord):
                    engine.Game.getAction(engine.Game.spawnCoord) # This function gets the specific action of the card.

                # If the deck is empty after the card was drawn, the current turn becomes the last.
                if len(engine.Game.deck) == 0:
                        engine.Game.lastTurn = True

            # If the discard pile is clicked, allow dragging for the card on top of the discard pile.
            elif len(discardClick) != 0 and not engine.Game.specialTurn and not engine.Game.Player1.hasDrawn and not engine.Game.Player2.hasDrawn and engine.Game.turnCount > 1:
                self.sino_hatak = discardClick[len(discardClick)-1]
                self.last_mouse_position = x, y

            # If a bullet was clicked, the last turn was not yet initiated and it is currently not a special turn, the "bullet" mechanic is triggered.
            elif len(bulletClick) != 0 and engine.Game.lastTurn == False and not engine.Game.specialTurn and engine.Game.turnCount > 1:
                # The bind of the respective sprites indicates the player who has initiated bullet.
                if bulletClick[0].bind == 'p1' and engine.Game.Player1.turn:
                    print("Player 1 has initiated bullet.")
                    engine.Game.hasBullet()
                elif bulletClick[0].bind == 'p2' and engine.Game.Player2.turn:
                    print("Player 2 has initiated bullet.")
                    engine.Game.hasBullet()

            # This allows for viewing two cards for the first turn.
            if engine.Game.turnCount <= 1:
                engine.Game.specialTurn = True
                engine.Game.specialMove = "View your own card."

            # If it is currently a special turn, initialize the respective special actions.
            if engine.Game.specialTurn:
                if engine.Game.specialMove == "View your own card.":
                    # If it is the player's turn, check if the player has clicked of his/her own cards.
                    if engine.Game.Player1.turn:
                        own = arcade.get_sprites_at_point((x,y), self.cardsPlayer1)
                        # If the player has clicked a card on his/her hand, create a sprite which shows its value.
                        # The special move is reset to "".
                        if len(own) != 0:
                            show = arcade.Sprite((engine.getimgStr(engine.Game.Player1.sprite2val[own[0]])), 0.9)
                            show.position = own[0].position
                            self.cardsPlayer1.append(show)
                            engine.Game.specialMove = ""
                            # These allow for viewing two cards from the hand at the start of the game.
                            if engine.Game.turnCount == 0 and not engine.Game.Player1.hasSeen:
                                engine.Game.specialMove = "View your own card."
                                engine.Game.Player1.hasSeen = True
                            elif engine.Game.turnCount == 0 and engine.Game.Player1.hasSeen:
                                engine.Game.endTurn()

                    elif engine.Game.Player2.turn:
                        own = arcade.get_sprites_at_point((x,y), self.cardsPlayer2)
                        if len(own) != 0:
                            show = arcade.Sprite((engine.getimgStr(engine.Game.Player2.sprite2val[own[0]])), 0.9)
                            show.position = own[0].position
                            self.cardsPlayer2.append(show)
                            engine.Game.specialMove = ""
                            if engine.Game.turnCount == 1 and not engine.Game.Player2.hasSeen:
                                engine.Game.specialMove = "View your own card."
                                engine.Game.Player2.hasSeen = True
                            elif engine.Game.turnCount == 1 and engine.Game.Player2.hasSeen:
                                engine.Game.endTurn()

                elif engine.Game.specialMove == "See the opponent's card.":
                    # If it is the player's turn, check if the player has clicked his/her opponent's cards.
                    if engine.Game.Player1.turn:
                        own = arcade.get_sprites_at_point((x,y), self.cardsPlayer2)
                        # If the player has clicked a card on his/her opponent's hand, create a sprite which shows its value.
                        # The special move is reset to "".
                        if len(own) != 0:
                            show = arcade.Sprite((engine.getimgStr(engine.Game.Player2.sprite2val[own[0]])), 0.9)
                            show.position = own[0].position
                            self.cardsPlayer2.append(show)
                            engine.Game.specialMove = ""
                    elif engine.Game.Player2.turn:
                        own = arcade.get_sprites_at_point((x,y), self.cardsPlayer1)
                        if len(own) != 0:
                            show = arcade.Sprite((engine.getimgStr(engine.Game.Player1.sprite2val[own[0]])), 0.9)
                            show.position = own[0].position
                            self.cardsPlayer1.append(show)
                            engine.Game.specialMove = ""

                elif engine.Game.specialMove == "Your opponent's hand is shuffled.":
                    # If it is the player's turn, his/her opponent's cards are shuffled.
                    if engine.Game.Player1.turn:
                        engine.Game.Player2.shuffle()
                    elif engine.Game.Player2.turn:
                        engine.Game.Player1.shuffle()
                else:
                    # This condition is satisfied only when the special move is card swap among players.
                    # In which case, the special move is handled by mouse release.
                    pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        This function is called when a user releases a mouse button.
        It comprises of majority of the game's mechanics such as:
           - card matching,
           - special card abilities,
           - and turns.
        """
        hatak_last = self.sino_hatak
        # This function allows the leaderboard to vanish after click.
        if self.requestLeaderboard:
            clicked = arcade.MOUSE_BUTTON_LEFT
            if clicked > 0:
                self.requestLeaderboard = False
        # This function alters the instructions displayed upon every click until all instructions have been displayed.
        elif self.requestInstructions:
            clicked = arcade.MOUSE_BUTTON_LEFT
            if clicked > 0 and len(self.instructionsList) != 0:
                self.toDrawI = self.instructionsList.pop()
            else:
                self.requestInstructions = False
        # This checks for loading screen button clicks while the loading screen is open.
        elif self.playScreen:
            textbutton.check_mouse_release_for_buttons(x, y, self.button_list_loadingScreen)
            textbutton.check_mouse_release_for_buttons(x, y, self.button_list_instructions)

        # This releases the card being dragged at mouse release.
        elif button == arcade.MOUSE_BUTTON_LEFT:
            self.sino_hatak = None

        '''
        This checks if "sapaw" is initiated, i.e. if card is placed on discardPile.
        The playArea serves as the object to detect collision.
        The sapaw function alters the hand appropriately. If the wrong card is pressed, a card is added onto the hand.
        Else, the card is released from the hand.
        '''
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
        '''
        This checks whether a special turn is initiated.
        If the special ability is swap, check for hand collisions with the last card dragged.
        '''
        if engine.Game.specialTurn and engine.Game.specialMove == "Swap a card with the opponent.":
            if hatak_last != None:
                swap1 = arcade.check_for_collision_with_list(hatak_last, self.cardsPlayer1)
                swap2 = arcade.check_for_collision_with_list(hatak_last, self.cardsPlayer2)
            else:
                swap1 = []
                swap2 = []

            if len(swap2) != 0 and engine.Game.Player1.turn:
                swapval1 = engine.Game.Player1.sprite2val[hatak_last]
                swapval2 = engine.Game.Player2.sprite2val[swap2[0]]
                index1 = engine.Game.Player1.hand.index(swapval1)
                index2 = engine.Game.Player2.hand.index(swapval2)
                engine.Game.Player1.hand.remove(swapval1)
                engine.Game.Player2.hand.remove(swapval2)
                engine.Game.Player1.hand.insert(index1, swapval2)
                engine.Game.Player2.hand.insert(index2, swapval1)
                engine.Game.specialMove = ""
                arcade.play_sound(self.swap_sound)
            elif len(swap1) != 0 and engine.Game.Player1.turn:
                swapval1 = engine.Game.Player1.sprite2val[swap1[0]]
                swapval2 = engine.Game.Player2.sprite2val[hatak_last]
                index1 = engine.Game.Player1.hand.index(swapval1)
                index2 = engine.Game.Player2.hand.index(swapval2)
                engine.Game.Player1.hand.remove(swapval1)
                engine.Game.Player2.hand.remove(swapval2)
                engine.Game.Player1.hand.insert(index1, swapval2)
                engine.Game.Player2.hand.insert(index2, swapval1)
                engine.Game.specialMove = ""
                arcade.play_sound(self.swap_sound)
        '''
        If the discard pile is dragged, check for collisions with the players' hand.
        Swap the cards upon contact with the discard pile.
        '''
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

            # This allows for the snapping of the cards when there is a discard card but no action is done.
            # This is performed regularly since there is always a card at discard.
            else:
                self.cardsPlayer1, self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val = engine.Game.refreshPlayers(self.cardsPlayer1,
                self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val, engine.Game.Player1.hand, engine.Game.Player2.hand, SCREEN_HEIGHT)
                self.discardPile[len(self.discardPile)-1].position = (SCREEN_WIDTH//2+264,SCREEN_HEIGHT//2)

        #If the spawn card is dragged to the play area, the card is disposed.
        dispose = arcade.check_for_collision_with_list(self.playArea, self.spawn)
        if dispose != []:
            print("Spawn was disposed.")
            self.discardPile, self.spawn = engine.Game.spawn2discard(dispose[0], self.discardPile, self.spawn, SCREEN_WIDTH, SCREEN_HEIGHT)
            engine.Game.endTurn()
            self.cardsPlayer1, self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val = engine.Game.refreshPlayers(self.cardsPlayer1,
            self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val, engine.Game.Player1.hand, engine.Game.Player2.hand, SCREEN_HEIGHT)
            arcade.play_sound(self.place_sound)

        # If the spawn card is dragged to the players' hands, swap the spawn card with the card of the hand it was swapped to.
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

            # Similarly, this allows for the snapping of the cards when there is a spawn card but no action is done.
            else:
                self.cardsPlayer1, self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val = engine.Game.refreshPlayers(self.cardsPlayer1,
                self.cardsPlayer2, engine.Game.Player1.sprite2val, engine.Game.Player2.sprite2val, engine.Game.Player1.hand, engine.Game.Player2.hand, SCREEN_HEIGHT)
                self.spawn[0].position = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)

def refreshHand(hand, spriteList, tup):
    """
    This allows for the redrawing of the card when:
      - no action is done or
      - an action that changes the hand is done.
    """
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
    """
    This creates a sprite for the image of the card when it is viewed
    by the special ability.
    """
    new = arcade.Sprite(engine.getimgStr(val), 0.9)
    new.position = spritepos
    return new

def main():
    """
    This runs whenever the file is run in itself.
    The DigitalBullet is created for the main game.
    """
    laro = DigitalBullet(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    laro.setup()
    arcade.run()

if __name__ == "__main__":
    main()
