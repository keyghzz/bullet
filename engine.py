import random
import interface
import os

def deckGo():

    '''
    Initializes the deck of cards
    '''

    deck = [(x%4,y%13) for x,y in enumerate(range(0,52))]
    deck.extend([(4,13),(4,13)])
    random.shuffle(deck)
    return deck

def drawfromDeck(num,deck):

    '''
    Returns what to draw and the remaining deck as lists
    '''

    return deck[:num],deck[num:]

def getimgStr(card):

    '''
    Returns the value of the card as a string
    '''

    suits = ["Clubs","Diamonds","Hearts","Spades","Joker"]
    ranks = [str(x) for x in range(2,11)]
    ranks.insert(0,"A")
    ranks.extend(["J","Q","K",""])
    return "resources/card" + str(suits[card[0]]) + str(ranks[card[1]]) + ".png"

class Player:

    '''
    Defines the Player and its attributes
    '''

    def __init__(self):
        self.hand = []
        self.turn = False
        self.hasDrawn = False
        self.sprite2val = {}
        self.hasSeen = False
    def shuffle(self):
        random.shuffle(self.hand)

class Game:

    '''
    Defines the entire game
    '''

    def __init__(self, toContinue):

        '''
        Initializes the start of the game
        '''

        self.Player1 = Player()
        self.Player2 = Player()
        self.lastTurn = False
        self.hasWon = ""
        self.score = (0,0)
        self.cardCountWinner = -1
        self.specialTurn = False
        if toContinue != []:

            '''
            Checks if a previous game was loaded
            '''

            self.Player1.hand = toContinue[0]
            self.Player2.hand = toContinue[2]
            self.Player1.turn = toContinue[1]
            self.Player2.turn = toContinue[3]
            self.discardCoord = toContinue[4]
            self.deck = toContinue[5]
            self.turnCount = toContinue[6]
            print("Loaded:", toContinue)
        else:

            '''
            Starts a new game
            '''

            self.turnCount = 0
            self.deck = deckGo()
            self.Player1.hand, self.deck = drawfromDeck(4,self.deck)
            self.Player2.hand, self.deck = drawfromDeck(4,self.deck)
            self.Player1.turn = True
            self.Player2.turn = False
            tempDiscardCoord, self.deck = drawfromDeck(1,self.deck)
            self.discardCoord = tempDiscardCoord[0]
            self.spawnCoord = None

    def sapaw(self, card, discardPile, hand, sprite2val, cardsPlayer, SCREEN_WIDTH, SCREEN_HEIGHT):

        '''
        Players discard a card that has the same vaue as the card on the discard pile
        '''

        if (sprite2val[card])[1] == self.discardCoord[1]:

            '''
            Thrown card matches the card on top of the discard pile
            '''

            isWrong = False
            cardpos = (SCREEN_WIDTH//2+(264), SCREEN_HEIGHT//2)
            discardPile.append(interface.val2sprite(sprite2val[card], cardpos))
            self.discardCoord = sprite2val[card]
            cardsPlayer.remove(card)
            hand.remove(sprite2val[card])
        else:

            '''
            Thrown card does not match the card on top of the discard pile, penalty is given
            '''

            isWrong = True
            penalty, self.deck = drawfromDeck(1, self.deck)
            if len(self.deck) == 0 or len(hand) == 5:

                '''
                Once a player has reached 6 cards in their hand or if there are no more cards to draw penalties from, the program will initiatre the last phases of the game
                '''

                print("uh oh.")
                self.lastTurn = True
            hand.append(penalty[0])
        self.saveProgress()
        return discardPile, hand, cardsPlayer, isWrong

    def spawn2discard(self, card, discardPile, spawn, SCREEN_WIDTH, SCREEN_HEIGHT):

        '''
        Player draws from the deck and discards
        '''

        card.position = (SCREEN_WIDTH//2+(264), SCREEN_HEIGHT//2)
        discardPile.append(card)
        self.discardCoord = self.spawnCoord
        spawn.remove(card)
        self.hasDrawn(False)
        return discardPile, spawn

    def hasDrawn(self, bool):

        '''
        Checks if the players have drawn from the deck
        '''

        if self.Player1.turn == True and bool:
            print("Player 1 has drawn from the deck.")
            self.Player1.hasDrawn = bool
        elif self.Player1.turn == True and not bool:
            self.Player1.hasDrawn = bool
        elif self.Player2.turn == True and bool:
            print("Player 2 has drawn from the deck.")
            self.Player2.hasDrawn = bool
        elif self.Player2.turn == True and not bool:
            self.Player2.hasDrawn = bool
        else:
            pass

    def hasBullet(self):

        '''
        Checks if the player has called "Bullet!" and initiates the last turns of the game
        '''

        self.endTurn()
        self.lastTurn = True

    def initiateWin(self):

        '''
        Checks who wins between the two players and ends the game
        '''

        card2score = [x for x in range(1, 11)]
        card2score.extend([11, 11, 11, 0])
        compare1 = (sum([card2score[x[1]] for x in self.Player1.hand]), len(self.Player1.hand))
        compare2 = (sum([card2score[x[1]] for x in self.Player2.hand]), len(self.Player2.hand))
        if compare1 < compare2:

            '''
            Player 1 has lower value
            '''

            self.hasWon = "Player 1"
            self.cardCountWinner = len(self.Player1.hand)
        elif compare1 > compare2:

            '''
            Player 2 has lower value
            '''

            self.hasWon = "Player 2"
            self.cardCountWinner = len(self.Player1.hand)
        elif compare1 == compare2:

            '''
            If both values are equal, the player with the less cards is the winner
            '''

            if self.turnCount %2 == 1:
                self.hasWon = "Player 1"
                self.cardCountWinner = len(self.Player1.hand)
            elif self.turnCount %2 == 0:
                self.hasWon = "Player 2"
                self.cardCountWinner = len(self.Player1.hand)
        self.endGame()

    def endGame(self):

        '''
        Records the game to the leaderboard
        '''

        file1 = 'saveState.txt'
        sav = open(file1, 'w+')
        sav.close()

        file2 = 'leaderboard.txt'
        if not os.path.exists(file2):
            leader = open(file2, 'w')
        leader = open(file2, 'r')
        l = leader.readlines()

        if len(l) != 0:
            prev = (int(l[len(l)-5][10:]), int(l[len(l)-4][10:]))
        else:
            prev = (0, 0)

        leader = open(file2, 'a')

        self.getScore()
        leader.write("------------\n")
        leader.write("Player 1: " + str(self.score[0] + prev[0]) + "\n")
        leader.write("Player 2: " + str(self.score[1] + prev[1]) + "\n\n")
        s = "" if self.cardCountWinner == 1 else "s"
        leader.write(self.hasWon + " has won with " + str(self.cardCountWinner) + " card" + s + " in hand.\n")
        s, verb = ("", "has") if self.turnCount // 2 == 1 else ("s", "have")
        leader.write(str(self.turnCount // 2) + " turn" + s + " " + verb  + " elapsed before the outcome.\n")

    def getScore(self):

        '''
        Updates the score of each player
        '''

        if self.hasWon == "Player 1":
            self.score = (1,0)

        elif self.hasWon == "Player 2":
            self.score = (0,1)

    def spawnSwap(self, card, discardPile, spawn, hand, sprite2val, SCREEN_WIDTH, SCREEN_HEIGHT):

        '''
        Draws a card from the deck and swaps it with a card in the player's hand
        '''

        cardpos = (SCREEN_WIDTH//2+(264), SCREEN_HEIGHT//2)
        discardPile.append(interface.val2sprite(sprite2val[card], cardpos))
        iOfC = hand.index(sprite2val[card])
        self.discardCoord = sprite2val[card]
        hand.remove(sprite2val[card])
        hand.insert(iOfC, self.spawnCoord)
        spawn.remove(spawn[0])
        self.hasDrawn(False)
        return discardPile, spawn, hand

    def discardSwap(self, card, discardPile, hand, sprite2val, SCREEN_WIDTH, SCREEN_HEIGHT):

        '''
        Draws a card from the discard pile and swaps it with a card in the player's hand
        '''

        cardpos = (SCREEN_WIDTH//2+(264), SCREEN_HEIGHT//2)
        discardPile.pop()
        discardPile.append(interface.val2sprite(sprite2val[card], cardpos))
        iOfC = hand.index(sprite2val[card])
        hand.remove(sprite2val[card])
        hand.insert(iOfC, self.discardCoord)
        self.discardCoord = sprite2val[card]
        return discardPile, hand

    def endTurn(self):

        '''
        Ends the player's turn after they have done an action
        '''

        if self.lastTurn:

            '''
            Checks if it's the players last turn and sets up the last phases of the game
            '''

            print("It's the last turn!")
            self.Player1.turn = False
            self.Player2.turn = False
            self.initiateWin()
        else:
            self.Player1.turn = not self.Player1.turn
            self.Player2.turn = not self.Player2.turn
            self.specialTurn = False
            self.specialMove = ""
            self.turnCount += 1
            if self.Player1.turn:
                print("It's Player 1's turn now.")
                self.saveProgress()
            elif self.Player2.turn:
                print("It's Player 2's turn now.")
                self.saveProgress()

    def getAction(self, cardTup):

        '''
        Defines the actions of the special cards:
        10 - Jack, 11 - Queen, 12 - King, 13 - Jokers
        '''

        self.specialTurn = True
        cardactions = {10: "See the opponent's card.",
                       11: "Swap a card with the opponent.",
                       12: "View your own card.",
                       13: "Your opponent's hand is shuffled."}

        self.specialMove = cardactions[cardTup[1]]
        print(self.specialMove)

    def refreshPlayers(self, cardsPlayer1, cardsPlayer2, sprite2val1, sprite2val2, hand1, hand2, SCREEN_HEIGHT):

        '''
        Refreshes the sprites and the positions of the player's cards
        '''

        cardsPlayer1, sprite2val1 = interface.refreshHand(hand1, cardsPlayer1, (70, 145))
        cardsPlayer2, sprite2val2 = interface.refreshHand(hand2, cardsPlayer2, (70, SCREEN_HEIGHT-(145)))
        return cardsPlayer1, cardsPlayer2, sprite2val1, sprite2val2

    def getAllRelevant(self):

        '''
        Takes the relevant data (player hands, cards in deck, turn count, etc.) to write later
        '''

        return "; ".join(str(x) for x in self.Player1.hand), str(self.Player1.turn), "; ".join(str(x) for x in self.Player2.hand), str(self.Player2.turn), str(self.discardCoord), "; ".join(str(x) for x in self.deck), str(self.turnCount)

    def saveProgress(self):

        '''
        Saves the progress of the game to a .txt file
        '''

        file = 'saveState.txt'
        sav = open(file, 'w+')
        for x in self.getAllRelevant():
            sav.write(x + "\n")
        sav.close()

def isSpecial(cardval):

    '''
    Defines which cards are special cards
    '''

    return cardval[1] > 9

def loadProgress():

    '''
    Reads the .txt save file and loads the game using the data
    '''

    file = 'saveState.txt'
    toContinue = []
    lines = []
    if os.path.exists(file):

        '''
        Checks if there is data to be loaded
        '''

        sav = open(file, 'r')
        for line in sav:
            lines.append(line)
        if len(lines) != 0:
            hand1, turn1, hand2, turn2, discardCoord, deck, turnCount = map(lambda x: x.split("; "), lines)
            hand1 = [tuple([int(x[0]), int(x[3:])]) for x in [hand.strip("\n").strip("(").strip(")") for hand in hand1]]
            turn1 = turn1[0][:len(turn1)-2]
            turn1 = turn1 == "True"
            hand2 = [tuple([int(x[0]), int(x[3:])]) for x in [hand.strip("\n").strip("(").strip(")") for hand in hand2]]
            turn2 = turn2[0][:len(turn2)-2]
            turn2 = turn2 == "True"
            discardCoord = discardCoord[0][:len(discardCoord[0])-2]
            discardCoord = tuple([int(discardCoord[1]), int(discardCoord[4:])])
            deck = [tuple([int(x[0]), int(x[3:])]) for x in [y.strip("\n").strip("(").strip(")") for y in deck]]
            turnCount = int(turnCount[0])
            toContinue = [hand1, turn1, hand2, turn2, discardCoord, deck, turnCount]
            sav.close()
    else:
        pass
    return toContinue
