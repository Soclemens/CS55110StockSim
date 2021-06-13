from random import randint
from math import log


class StockMarket:
    def __init__(self) -> None:
        """
        Handles the trading and prices of stocks
        """
        self.__stocks = []
    
    def getStockListings(self) -> list:  # (stock key, current price)
        pass

    def doTrade(self, action:list) -> int:
        # do a price lookUp, return the cost (negative if they bought, positive if sold)
        return 0

    def nextDay(self) -> None:
        """
        fluctuates all the stock prices by their equations for the next day for trading
        """
        pass

class Stock:
    def __init__(self, basePrice, volatility) -> None:
        self.__key = 0
        self.__baseprice = basePrice
        self.__volatility = volatility
        self.__upperBound = lambda x,b,s: -(.8)*log(x-1*(log(b+1,3)-log(s+1,3)),3) +.0026  # {0≤b,0≤s}
        self.__lowerBound = lambda x,b,s: -(.8)*log(-x+1*(log(b+1,3)-log(s+1,3)),3) +.0026  # {0≤b,0≤s}

    def flux(self) -> None:
        """
        I have no idea what to do with this, or even if this is the right idea.
        """


# def makeStock(key = None, basePrice = 20, volatility = 1.0):
#     if key == None:
#         key = ''.join([chr(ord('A')+randint(0,25)) for _ in range(3)])

        

#     return {'key':key, }