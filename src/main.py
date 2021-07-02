from env import *
from agent import *

TRADING_DAYS = 25

def initialize():
    # set up
    gameLoop()

def reportStats(agents, x):
    print("///////// STATS REPORT /////////")
    i = 0
    for agent in agents:
        print("group ", str(i // x), ": ", agent.returns)
        i += 1


def gameLoop():
    stockMarket = StockMarket(marketSize=30)  # initialize the stock market
    agents = []  # make a abstract container of agents
    x = 10
    agents.extend([RiskNeutral(stockMarket.getStockListings(), 1) for _ in range(x)])  # makes x of neutral type of agent
    agents.extend([RiskTolerant(stockMarket.getStockListings(), 1) for _ in range(x)])  # makes x of tolerant type of agent
    agents.extend([RiskAvers(stockMarket.getStockListings(), 1) for _ in range(x)])  # makes x of avers type of agent
    for _ in range(TRADING_DAYS+1):  # Trade for x days
        todaysListing = stockMarket.getStockListings()  # get todays prices

        for agent in agents:  # for each agent
            actions = []
            # print(agent.name)
            for stock in todaysListing:  # for each stock
                action = agent.act(stock)
                if action is not None:
                    actions.append(action)
            print(actions)
        stockMarket.updateMarket()  # update stock prices for tomorrow

        print("Finished day " + str(_) + " out of " + str(TRADING_DAYS + 1) + "... " + str((_/TRADING_DAYS) * 100) + "%")
        print("--------------------------------------------------------------------------------------------------------")
    
    reportStats(agents, x)


if __name__ == '__main__':
    initialize()
