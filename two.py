import random
import main
import os

#TODO: specify sprite2val as function input

def deckGo():
    deck = [(x%4,y%13) for x,y in enumerate(range(0,52))]
    deck.extend([(4,13),(4,13)])
    random.shuffle(deck)
    return deck

def drawfromDeck(num,deck):
    return deck[:num],deck[num:] #return what to draw and remaining deck as lists

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
            self.Player1.hand = toContinue[0]
            self.Player2.hand = toContinue[2]
            self.Player1.turn = toContinue[1]
            self.Player2.turn = toContinue[3]
            self.discardCoord = toContinue[4]
            self.deck = toContinue[5]
            print("Loaded:", toContinue)
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
            isWrong = False
            card.position = (SCREEN_WIDTH//2+(264), SCREEN_HEIGHT//2)
            discardPile.append(card)
            self.discardCoord = sprite2val[card]
            cardsPlayer.remove(card)
            discardCoord = sprite2val[card]
            hand.remove(sprite2val[card])
        else:
            isWrong = True
            penalty, Game.deck = drawfromDeck(1, Game.deck)
            hand.append(penalty[0])
        self.saveProgress()
        return discardPile, hand, cardsPlayer, isWrong

    def spawn2discard(self, card, discardPile, spawn, SCREEN_WIDTH, SCREEN_HEIGHT):
        card.position = (SCREEN_WIDTH//2+(264), SCREEN_HEIGHT//2)
        discardPile.append(card)
        self.discardCoord = self.spawnCoord
        spawn.remove(card)
        self.hasDrawn(False)
        return discardPile, spawn

    def hasDrawn(self, bool):
        if self.Player1.turn == True:
            print("Player 1 has drawn from the deck.")
            self.Player1.hasDrawn = bool
        else:
            print("Player 2 has drawn from the deck.")
            self.Player2.hasDrawn = bool

    def spawnSwap(self, card, discardPile, spawn, hand, sprite2val, SCREEN_WIDTH, SCREEN_HEIGHT):
        card.position = (SCREEN_WIDTH//2+(264), SCREEN_HEIGHT//2)
        discardPile.append(card)
        iOfC = hand.index(sprite2val[card])
        self.discardCoord = sprite2val[card]
        hand.remove(sprite2val[card])
        hand.insert(iOfC, self.spawnCoord)
        spawn.remove(spawn[0])
        self.hasDrawn(False)
        return discardPile, spawn, hand

    def discardSwap(self, card, discardPile, hand, sprite2val, SCREEN_WIDTH, SCREEN_HEIGHT):
        card.position = (SCREEN_WIDTH//2+(264), SCREEN_HEIGHT//2)
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
        self.saveProgress()

    def refreshPlayers(self, cardsPlayer1, cardsPlayer2, sprite2val1, sprite2val2, hand1, hand2, SCREEN_HEIGHT):
        cardsPlayer1, sprite2val1 = main.refreshHand(hand1, cardsPlayer1, (70, 145))
        cardsPlayer2, sprite2val2 = main.refreshHand(hand2, cardsPlayer2, (70, SCREEN_HEIGHT-(145)))
        return cardsPlayer1, cardsPlayer2, sprite2val1, sprite2val2

    def getAllRelevant(self):
        return ", ".join(str(x) for x in self.Player1.hand), str(self.Player1.turn), ", ".join(str(x) for x in self.Player2.hand), str(self.Player2.turn), str(self.discardCoord), ", ".join(str(x) for x in self.deck)

    def saveProgress(self):
        file = 'saveState.txt'
        if os.path.exists(file):
            sav = open(file, 'w')
        else:
            sav = open(file, 'w+')

        for x in self.getAllRelevant():
            sav.write(x + "\n")
        sav.close()

def loadProgress():
    file = 'saveState.txt'
    toContinue = []
    lines = []
    if os.path.exists(file):
        sav = open(file, 'r')
        for line in sav:
            lines.append(line)
        hand1, turn1, hand2, turn2, discardCoord, deck = map(lambda x: x.split("), "), lines)
        hand1[len(hand1)-1] = hand1[len(hand1)-1][:len(hand1[len(hand1)-1])-2]
        hand1 = [tuple([int(x[1]), int(x[4:])]) for x in hand1]
        turn1 = turn1[0][:len(turn1)-2]
        turn1 = turn1 == "True"
        hand2[len(hand2)-1] = hand2[len(hand2)-1][:len(hand2[len(hand2)-1])-2]
        hand2 = [tuple([int(x[1]), int(x[4:])]) for x in hand2]
        turn2 = turn2[0][:len(turn2)-2]
        print(turn2)
        turn2 = turn2 == "True"
        discardCoord = discardCoord[0][:len(discardCoord[0])-2]
        discardCoord = tuple([int(discardCoord[1]), int(discardCoord[4:])])
        deck[len(deck)-1] = deck[len(deck)-1][:len(deck[len(deck)-1])-2]
        deck = [tuple([int(x[1]), int(x[4:])]) for x in deck[:len(deck)-2]]
        toContinue = [hand1, turn1, hand2, turn2, discardCoord, deck]
    else:
        pass
    sav.close()
    return toContinue
