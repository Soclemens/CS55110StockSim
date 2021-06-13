from env import *
from agent import *

def initialize():
    # set up
    gameLoop()

def gameLoop():
    theMarket = StockMarket()
    # TODO: create a list of actors
    while True:
        # TODO: Give each actor a chance to act based on that days perceptions. The list of actions ->
        #           Check my holdings and determine if I want to sell
        #               if yes update stock sell count and log this action under the actors log
        #           Check each stock and determine whether I want to buy any *can only own one of each **maybe
        #               if yes update stock buys count and log this action under the actors log
        #           Update my current returns and standings in the leader board
        # TODO: Give the market a chance to update itself for the next round
        break

    # TODO: Report final standings



if __name__ == 'main':
    initialize()