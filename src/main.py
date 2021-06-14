from env import *
from agent import *

TRADING_DAYS = 1

def initialize():
    # set up
    gameLoop()

def reportStats(agents):
    print("///////// STATS REPORT /////////")

def gameLoop():
    stockMarket = StockMarket()
    agents = []
    agents.extend([RiskNeutral() for _ in range(1)])  # makes x of this type of agent
    print("stockMarket")
    for _ in range(TRADING_DAYS+1):
        todaysListing = stockMarket.getStockListings()
        for agent in agents:
            for stock in todaysListing:
                
                agent.adjustBalance(stockMarket.doTrade(agent.act(todaysListing)))
        stockMarket.updateMarket()
    
    reportStats(agents)

    # TODO: Give each actor a chance to act based on that days perceptions. The list of actions ->
        #           Check my holdings and determine if I want to sell
        #               if yes update stock sell count and log this action under the actors log
        #           Check each stock and determine whether I want to buy any *can only own one of each **maybe
        #               if yes update stock buys count and log this action under the actors log
        #           Update my current returns and standings in the leader board
        # TODO: Give the market a chance to update itself for the next round
    # TODO: Report final standings

if __name__ == '__main__':
    initialize()
