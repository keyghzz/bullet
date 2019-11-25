import random
import main

#TODO: specify sprite2val as function input

def deckGo():
    deck = [(x%4,y%13) for x,y in enumerate(range(0,52))]
    deck.extend([(4,13),(4,13)])
    random.shuffle(deck)
    return deck

def drawfromDeck(num,deck):
    return deck[:num],deck[num:] #return what to draw and remaining deck as tuples

def getimgStr(card):
    suits = ["Clubs","Diamonds","Hearts","Spades","Joker"]
    ranks = [str(x) for x in range(2,11)]
    ranks.insert(0,"A")
    ranks.extend(["J","Q","K",""])
    return "resources/card" + str(suits[card[0]]) + str(ranks[card[1]]) + ".png"

class Player:
    def __init__(self):
        self.hand = []
        self.turn = False
        self.hasDrawn = False
        self.sprite2val = {}
    def get_sprite2val(self, card):
        return self.sprite2val[card]

'''
note:

Game.deck
Game.Player1
Game.Player2

'''
class Game:
    def __init__(self, toContinue):
        self.Player1 = Player()
        self.Player2 = Player()
        if toContinue != []:
            self.discardCoord = 0,0
            #and assign other shit
        else:
            self.deck = deckGo()
            self.Player1.hand, self.deck = drawfromDeck(4,self.deck)
            self.Player2.hand, self.deck = drawfromDeck(4,self.deck)
            self.Player1.turn = True
            self.Player2.turn = False
            tempDiscardCoord, self.deck = drawfromDeck(1,self.deck)
            self.discardCoord = tempDiscardCoord[0]
            self.spawnCoord = None

    def sapaw(self, card, discardPile, hand, sprite2val, cardsPlayer, SCREEN_WIDTH, SCREEN_HEIGHT):
        if (sprite2val[card])[1] == self.discardCoord[1]:
            card.position = (SCREEN_WIDTH//2+264, SCREEN_HEIGHT//2)
            discardPile.append(card)
            self.discardCoord = sprite2val[card]
            cardsPlayer.remove(card)
            discardCoord = sprite2val[card]
            hand.remove(sprite2val[card])
        else:
            penalty, Game.deck = drawfromDeck(1, Game.deck)
            hand.append(penalty[0])
        return discardPile, hand, cardsPlayer

    def spawn2discard(self, card, discardPile, spawn, SCREEN_WIDTH, SCREEN_HEIGHT):
        card.position = (SCREEN_WIDTH//2+264, SCREEN_HEIGHT//2)
        discardPile.append(card)
        self.discardCoord = self.spawnCoord
        spawn.remove(card)
        self.hasDrawn(False)
        return discardPile, spawn

    def hasDrawn(self, bool):
        if self.Player1.turn == True:
            self.Player1.hasDrawn = bool
        else:
            self.Player2.hasDrawn = bool

    def spawnSwap(self, card, discardPile, spawn, hand, sprite2val, SCREEN_WIDTH, SCREEN_HEIGHT):
        card.position = (SCREEN_WIDTH//2+264, SCREEN_HEIGHT//2)
        discardPile.append(card)
        iOfC = hand.index(sprite2val[card])
        self.discardCoord = sprite2val[card]
        hand.remove(sprite2val[card])
        hand.insert(iOfC, self.spawnCoord)
        spawn.remove(spawn[0])
        self.hasDrawn(False)
        return discardPile, spawn, hand

    def discardSwap(self, card, discardPile, hand, sprite2val, SCREEN_WIDTH, SCREEN_HEIGHT):
        card.position = (SCREEN_WIDTH//2+264, SCREEN_HEIGHT//2)
        discardPile.pop()
        discardPile.append(card)
        iOfC = hand.index(sprite2val[card])
        hand.remove(sprite2val[card])
        hand.insert(iOfC, self.discardCoord)
        self.discardCoord = sprite2val[card]
        return discardPile, hand

    def endTurn(self):
        self.Player1.turn = not self.Player1.turn
        self.Player2.turn = not self.Player2.turn
        if self.Player1.turn:
            print("It's Player 1's turn now.")
        else:
            print("It's Player 2's turn now.")

    def refreshPlayers(self, cardsPlayer1, cardsPlayer2, sprite2val1, sprite2val2, hand1, hand2, SCREEN_HEIGHT):
        cardsPlayer1, sprite2val1 = main.refreshHand(hand1, cardsPlayer1, (70, 145))
        cardsPlayer2, sprite2val2 = main.refreshHand(hand2, cardsPlayer2, (70, SCREEN_HEIGHT-145))
        return cardsPlayer1, cardsPlayer2, sprite2val1, sprite2val2
Game = Game([])
print("Player 1 was dealt the following cards: " + ", ".join(map(str, Game.Player1.hand)))
print("Player 2 was dealt the following cards: " + ", ".join(map(str, Game.Player2.hand)))
