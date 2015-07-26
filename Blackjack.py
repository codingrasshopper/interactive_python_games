# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        #print pos
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        hand_str = " "
        for i in self.hand:
            hand_str = hand_str + " " + str(i)
        return "hand contains" +str(hand_str)

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = 0
        is_A = False
        
        for card in self.hand:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                is_A = True
        
        if is_A and (hand_value + 10 <= 21):
                hand_value += 10
        return hand_value	# compute the value of the hand
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for num_card, card in enumerate(self.hand):
            pos0 = pos[0] + num_card *80
            if  pos[1] == 100 and num_card == 0 and  in_play == True:
                # draw card back
                canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                                  [pos0 + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]],
                                  CARD_BACK_SIZE)
            else:
                # draw face card
                card.draw(canvas, [pos0, pos[1]])
            #print pos
                
        
        
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for suit in SUITS: 
            for rank in RANKS:
                self.cards.append(Card(suit,rank))
                                                   
                

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)    

    def deal_card(self):
        y = random.choice(self.cards)# deal a card object from the deck
        self.cards.remove(y)
        return y
    
    def __str__(self):
        deck_str = "Deck contains "
        for i in self.cards:
            deck_str +=  " " + str(i)
        return deck_str



#define event handlers for buttons
def deal():
    global  outcome,in_play, hand_player, hand_dealer, deck, score
    
    outcome = "Hit or stand?"
    if in_play == True:
        outcome = "You Lose"
        score -= 1
    hand_player = Hand()
    hand_dealer = Hand()
    deck = Deck()
    deck.shuffle()
    
    hand_player.add_card(deck.deal_card())
    hand_player.add_card(deck.deal_card())
    hand_dealer.add_card(deck.deal_card())
    hand_dealer.add_card(deck.deal_card())
  #  print str(hand_player), str(hand_dealer)
    in_play = True

def hit():
    global in_play, outcome, score, hand_player, deck
    if in_play:
        hand_player.add_card(deck.deal_card())
        if hand_player.get_value() <= 21:
            outcome = "Hit or stand? "
        else:
            outcome = "You have busted! "
            score -= 1
            in_play = False	
 
    
       
def stand():
    global in_play, outcome, score, hand_player, hand_dealer
    if in_play:
        in_play = False
        if hand_player.get_value() > 21:
            outcome = "You have busted! New deal?"
            score -= 1
        else:
            while hand_dealer.get_value() < 17:
                hand_dealer.add_card(deck.deal_card())
                outcome = ""
            if hand_dealer.get_value() > 21:
                score += 1
                outcome = "You won! New deal?"
            elif hand_dealer.get_value() >= hand_player.get_value():
                score -= 1
                outcome = "You lose! New deal?"
            else:
                score += 1
                outcome = "You won! New deal?"	
   
    

# draw handler    
def draw(canvas):
    
    canvas.draw_text("Blackjack", [200, 25], 30, "White")

    # draw text
    canvas.draw_text("Dealer", [10, 45], 24, "Black")
    canvas.draw_text("Player", [10, 300], 24, "Black")
   

    hand_dealer.draw(canvas, [10, 100]) 
    hand_player.draw(canvas, [10, 350])
    
    canvas.draw_text(outcome, [100, 500], 24, "White")
    canvas.draw_text("Score: " + str(score), [500, 25], 24, "white")
    

frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
# initialization frame
frame.start()
deal()
