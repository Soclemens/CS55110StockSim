
class Trader:
    """Abstract class to allow for interfacing with env
       Contains act() and a default constructor"""
    def __init__(self, stockNumber, money=10_000, stopLost=0.25) -> None:
        self.__stockLimit
        self.__money = money
        self.__deptLimit = money  # yoy can only go -10,000 in dept
        # list of stokes, amount, & their purchase price
        self.__holdings = { i:{'stock':None, 'amount':0, 'purchasePrice':0} for i in range(stockNumber)}  
        self.__log = []  # logs of actions taken
        self.__stopLoss = stopLost  # persentage return. TODO, figure out of this should be flat, or percentile

    def act(self, listings:list) -> list:
        """
        Returns an "action" or a list of stock/number pairs corresponding to the by/sell amount
        """
        stockOrder = {}
        for listing in listings:
            stockOrder[listing.key] = self.analyzeStock(listing)

        # TODO: Do I mamage the amount of stacks
        # How do I Balance the amount of
        # WHen do I remove stocks
        # when is it okay to remove.

        return [("NAN", 0)]

    def analyzeStock(self, stock):  # no history used... yet
        ratio = stock.__goingPrice()/self.__holdings.get(stock.key,default={})

    def adjustBalance(self, money):
        self.__money += money

    
class RiskAvers(Trader):
    def __init__(self, money=10_100) -> None:
        super().__init__(money=money, stopLost=0.5)


class RiskNeutral(Trader):
    def __init__(self, money=10_100) -> None:
        super().__init__(money=money, stopLost=0.25)


class RiskTolerant(Trader):
    def __init__(self, money=10_100) -> None:
        super().__init__(money=money, stopLost=0.1)


class WildCard(Trader):
    def __init__(self, money=10_100) -> None:
        super().__init__(money=money, stopLost=0.25)

    def act(self, listings) -> list:
        return [("NAN",0)]


class Oscillator(Trader):
    def __init__(self, money=10_100) -> None:
        super().__init__(money=money, stopLost=0.1)

    def act(self, listings) -> list:
        return [("NAN",0)]