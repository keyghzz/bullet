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

def isEqual(val1, val2):
    return val1[1] == val2[1]

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
            self.tuloy = True
            self.discardCoord = 0,0
            #and assign other shit
        else:
            self.tuloy = False
            self.deck = deckGo()
            self.Player1.hand, self.deck = drawfromDeck(4,self.deck)
            self.Player2.hand, self.deck = drawfromDeck(4,self.deck)
            self.Player1.turn = True
            self.Player2.turn = False
            tempDiscardCoord, self.deck = drawfromDeck(1,self.deck)
            self.discardCoord = tempDiscardCoord[0]
            self.sprite2val1 = {}
            self.sprite2val2 = {}
            self.spawnCoord = None

def sapaw(Game, card, discardPile, discardCoord, Player, cardsPlayer, sprite2val, SCREEN_WIDTH, SCREEN_HEIGHT):
    if isEqual(sprite2val[card], discardCoord):
        card.position = (SCREEN_WIDTH//2+264, SCREEN_HEIGHT//2)
        discardPile.append(card)
        discardCoord = sprite2val[card]
        cardsPlayer.remove(card)
        discardCoord = sprite2val[card]
        Player.hand.remove(sprite2val[card])
    else:
        penalty, Game.deck = drawfromDeck(1, Game.deck)
        Player.hand.append(penalty[0])
    return discardPile, discardCoord, Player, cardsPlayer, sprite2val

Game = Game([])
print(Game.discardCoord)
