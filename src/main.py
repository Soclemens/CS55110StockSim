from env import *
from agent import *

TRADING_DAYS = 252

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
    x = 10
    agents.extend([RiskNeutral(stockMarket.getStockListings(), 1) for _ in range(x)])  # makes x of neutral type of agent
    agents.extend([RiskTolerant(stockMarket.getStockListings(), 1) for _ in range(x)])  # makes x of tolerant type of agent
    agents.extend([RiskAvers(stockMarket.getStockListings(), 1) for _ in range(x)])  # makes x of avers type of agent
    for _ in range(TRADING_DAYS+1):  # Trade for x days
        todaysListing = stockMarket.getStockListings()  # get todays prices

        for agent in agents:  # for each agent
            for stock in todaysListing:  # for each stock
                action = agent.act()  # NOTE: Actor's decisions are pass by reference to market
                # print(action)
        stockMarket.updateMarket()  # update stock prices for tomorrow

        print("Finished day " + str(_) + " out of " + str(TRADING_DAYS + 1) + "... " + str((_/TRADING_DAYS) * 100) + "%")
    
    reportStats(agents)


if __name__ == '__main__':
    initialize()
