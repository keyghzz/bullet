import random
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

def endTurn(self):
    self.Player1.turn = not self.Player1.turn
    self.Player2.turn = not self.Player2.turn
    self.cardsPlayer1, self.sprite2val1 = self.refreshHand(self.Player1.hand, self.cardsPlayer1, (70, 145))
    self.cardsPlayer2, self.sprite2val2 = self.refreshHand(self.Player2.hand, self.cardsPlayer2, (70, SCREEN_HEIGHT-145))
