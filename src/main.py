from env import *
from agent import *

TRADING_DAYS = 100

def initialize():
    # set up
    gameLoop()

def reportStats(agents):
    print("///////// STATS REPORT /////////")
    # TODO: for each agent, IDK, whatever stats you want. Crunch the logs I guess?
    for agent in agents:
        agent.print(showPortfolio=True)


def gameLoop():
    stockMarket = StockMarket()  # initialize the stock market
    agents = []  # make a abstract container of agents
    agents.extend([RiskNeutral(stockMarket.getStockListings()) for _ in range(1)])  # makes x of neutral type of agent
    agents.extend([RiskTolerant(stockMarket.getStockListings()) for _ in range(1)])  # makes x of tolerant type of agent
    agents.extend([RiskAvers(stockMarket.getStockListings()) for _ in range(1)])  # makes x of avers type of agent
    for _ in range(TRADING_DAYS+1): # Trade for x days
        todaysListing = stockMarket.getStockListings()  # get todays prices

        for agent in agents:  # for each agent
            for stock in todaysListing:  # for each stock
                action = agent.act(stock)  # NOTE: Actor's decisions are pass by reference to market
                # print(action)
        stockMarket.updateMarket()  # update stock prices for tomorrow
    
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
