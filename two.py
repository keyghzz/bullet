import random
def deckGo():
    deck = [(x%4,y%13) for x,y in enumerate(range(0,52))]
    deck.extend([(4,14),(4,15)])
    random.shuffle(deck)
    return deck

def drawfromDeck(num,deck):
    return deck[:num],deck[num:] #return what to draw and remaining deck as tuples

def getimgStr(card):
    suits = ["Clubs","Diamonds","Hearts","Spades","Joker"]
    ranks = [str(x) for x in range(2,11)]
    ranks.insert(0,"A")
    ranks.extend(["J","Q","K","",""])
    print(card)
    return "resources/" + str(suits[card[0]]) + str(ranks[card[1]]) + ".png"
