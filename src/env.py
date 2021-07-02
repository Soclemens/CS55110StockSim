from concurrent.futures.thread import ThreadPoolExecutor
from random import uniform
from statistics import stdev
import scipy.stats as stats
from sympy import log, solve, symbols
import numpy as np
import threading

class StockMarket:
    def __init__(self, marketSize=10) -> None:
        """
        Handles the trading and prices of stocks
        """
        self.__stocks = self.__makeStocks(marketSize=marketSize)

    def getStockListings(self) -> list:  # (stock key, current price)
        return self.__stocks



    def updateMarket(self) -> None:
        '''
        has each stock run updateStock on itself so it can update its values and clear the last days variables
        :return: None
        '''
        executor = ThreadPoolExecutor(max_workers=4)
        for stock in self.__stocks:
            executor.submit(stock.upDateStock())


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
            mu = uniform(0.01, maxGoing)  # this is the mean price of the stock
            sigma = uniform(0, volatility)  # this is the volatility percentage of a stock
            dist = stats.truncnorm((0.01 - mu) / sigma, (maxGoing - mu) / sigma, loc=mu, scale=sigma)
            values = dist.rvs(initAmount)

            stockMarket.append(Stock(values, stockNumber))  # grow the listings in the stock market

        return stockMarket


class Stock:
    def __init__(self, priceHistory, name) -> None:
        self.name = name if type(name) == str else str(name)  # Make sure it's a string
        self.__priceHistory = priceHistory  # a list of price histories to calculate volatility and going price
        self.goingPrice = lambda: self.__priceHistory[-1]  # the current going price of a stock
        self.volatility = lambda: stdev(priceHistory)  # how volatile a stock is. To calculate find the stdev of all past prices
        self.__todayBuys = 6  # simulate more actors
        self.__todaySells = 8 # simulate more actors

    def __repr__(self) -> str:
        return "key:" + self.name + " price:" + str(self.goingPrice())


    def upDateStock(self):
        '''
        Called at the end of each day to update the price history, going price, and the volatility.
        :return: returns a 0 for success, a -1 for a failure
        '''
        assert self.__todayBuys >= 0
        assert self.__todaySells >= 0
        x = symbols("x")
        xRange = []
        lowerBound = solve(-.8 * log(-1 * x + (log(self.__todayBuys + 1, 3) - log(self.__todaySells + 1, 3)), 10) * self.volatility(), x)[0]
        upperBound = solve(-.8 * log(x + -1 * (log(self.__todayBuys + 1, 3) - log(self.__todaySells + 1, 3)), 10) * self.volatility(), x)[0]
        xRange.append(lowerBound)
        xRange.append(upperBound)
        self.__priceHistory = np.append(self.__priceHistory, uniform(xRange[0], xRange[1]) + self.goingPrice())
        self.__todayBuys = 0  # simulate more actors
        self.__todaySells = 0  # simulate more actors

        return 0

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
