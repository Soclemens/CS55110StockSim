from random import random, randint, uniform, seed
from math import log
from statistics import stdev
import scipy.stats as stats

# Number of the groups that are going to be used
numGroups = 10

class StockMarket:
    def __init__(self) -> None:
        """
        Handles the trading and prices of stocks
        """
        self.__stocks = self.__makeStocks(marketSize=100)

    def getStockListings(self) -> list:  # (stock key, current price)
        return self.__stocks

    # NOTE: deprecated, might bring back if we do mass trading
    # def doTrade(self, action: list) -> int:
    #     # TODO: move this method into the actors realm of influence
    #     # I think this method should be in the actor classes because it will be up to them to do trades and not the market itself - Spencer
    #     # do a price lookUp, return the cost (negative if they bought, positive if sold)
    #     return 0

    def updateMarket(self) -> None:
        '''
        has each stock run updateStock on itself so it can update its values and clear the last days variables
        :return: None
        '''
        # TODO: Dial this in
        # Group updates (+-2.5%)
        groupOffset = [(random()-0.5)/20 for _ in range(numGroups)]
        for stock in self.__stocks:
            stock.upDateStock(groupOffset)

    def __makeStocks(self, maxGoing=100.00, volatility=4, marketSize=100, initAmount=10):
        """
        :param maxGoing: The starting price cap of any stock
        :param volatility: The starting volatility cap of any stock
        :param marketSize: How many stocks are in the market
        :param initAmount: How far back to seed the simulation
        :return: A list of stock objects
        """
        stockMarket = []  # the stock market array to return
        for stockNumber in range(marketSize):
            mu = uniform(0.01, 1000)  # this is the mean price of the stock
            sigma = uniform(0, volatility)  # this is the volatility percentage of a stock
            dist = stats.truncnorm((0.01 - mu) / sigma, (maxGoing - mu) / sigma, loc=mu, scale=sigma)
            values = dist.rvs(initAmount)

            # TODO: I have no idea what I'm doing!!!
            stockMarket.append(Stock(values, sigma, stockNumber))  # grow the listings in the stock market

        return stockMarket


class Stock:
    def __init__(self, priceHistory, myStdev, name) -> None:
        self.name = name if type(name) == str else str(name)  # Make sure it's a string
        self.__priceHistory = priceHistory  # a list of price histories to calculate volatility and going price
        self.goingPrice = lambda: self.__priceHistory[-1]  # the current going price of a stock
        
        #########
        seed(int(self.name))
        self.groupMembership = [round(random(), 2)]
        #########
        #########
        self.__findVolatility = lambda: stdev(priceHistory)  # how volatile a stock is. To calculate find the stdev of all past prices
        # NOTE: I've made a cached version that can be quired without running the function each time the agent make a judgment call
        self.volatility = self.__findVolatility()
        #########

        self.__todaySells = 0  # Stock object tracks how much of itself was sold
        self.__todayBuys = 0  # Stock object tracks how much of itself was bought

    def __repr__(self) -> str:
        return "key:" + self.name + " price:" + str(self.goingPrice())

    def __upperBound(x, b, s): 
        return -(.8) * log(x - 1 * (log(b + 1, 3) - log(s + 1, 3)), 3) + .0026  # {0≤b,0≤s}
    
    def __lowerBound(x, b, s):
        return -(.8) * log(-x + 1 * (log(b + 1, 3) - log(s + 1, 3)), 3) + .0026  # {0≤b,0≤s}


    def upDateStock(self, groupOffsets):
        '''
        Called at the end of each day to update the price history, going price, and the volatility.
        :return: returns a 0 for success, a -1 for a failure
        '''
        # TODO: Calculate new price based off of the equation and inputs
            # Needs to use the money witch magic here
        nextPrice = self.goingPrice()  # update each for the individual stock
        # TODO: Clear todaySells and todayBuys so they are fresh for tomorrow
        # TODO: Update going price so when actors buy or sell tomorrow they will be able to accurately calculate returns
        nextPrice += sum([self.groupMembership[i]*groupOffsets[i] for i in range(numGroups)])    # update for the group amount
        # TODO: Cache the Volatility for the agents decision making process.
            # (NEEDS validate)
        self.volatility = self.__findVolatility()         # TODO: Update stock volatility
        

    def stockBought(self):
        """
        Updates the class variable stocks bought to one plus itself to indicate an actor "bought" the stock.
        :return: None
        """
        self.__todayBuys += 1

    def stockSold(self):
        """
        Updates the class variable stocks sold to one plus itself to indicate an actor "sold" the stock.
        :return: None
        """
        self.__todaySells += 1


if __name__ == '__main__':  # this is here to test the code that I was writing and make sure Stock Market was working the way it should
    theMarket = StockMarket()
    print("rat")
