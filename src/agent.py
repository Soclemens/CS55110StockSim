
class Trader:
    """Abstract class to allow for interfacing with env
       Contains act() and a default constructor"""

    #NOTE: Not used. Only 20 stocks are permitted, 1 of each stock
    #NOTE: Currently, there is not debt limit
    def __init__(self, alltheStocks, money=10_000, stopLost=0.2, name="ABSTRACT") -> None:
        self.name = name  # Dump little ID for pretty printing the type of agent for the report
        self.__money = money
        # self.__deptLimit = money  # yoy can only go -10,000 in dept
        # list of stokes, amount, & their purchase price
        self.__holdings = { stock:{'amount':0,'purchasePrice':0} for stock in alltheStocks}  
        self.__log = []  # logs of actions taken
        self.__stopLoss = stopLost  # persentage of return I want
        # self.__stockLimit = 20

    def netWorth(self):
        """
        return the current net worth (money + sum of each stock's current price)
        """
        return self.__money + sum([stock.goingPrice() * self.__holdings[stock]['amount'] for stock in self.__holdings.keys()])
        
    def print(self, showPortfolio = False) -> str:
        """
        for printing the agent with its Type, Networth, then its portfolio of stocks with each price
        """
        msg = f"Agent:{self.name}\t"+ "NetWorth:" + format(self.netWorth(),".2f") +"\n\t"
        if showPortfolio:
            msg += "\n\t".join([
                "stock:"+stock.name+", "+format(stock.goingPrice(),".2f") 
                for stock in self.__holdings.keys() if self.__holdings[stock]['amount']>0
            ])
        print(msg)

    def act(self, stock):
        """
        Currently, just and interface to log the agents action based on it's stock analysis
        """
        result = self.__analyzeStock(stock)
        self.__log.append(result[1])
        return result

    # NOTE: This automatically assumes it's buying/selling its stock, make sure the market reflects that
    # NOTE: I have no idea what needs to be returned, the string or bool, or both.
    def __analyzeStock(self, stock) -> tuple:
        """
        This is the "act" function, returns true if they want to buy/keep a stock,
            or false if they want to sell/pass on that same stock
        """
        if self.__holdings[stock]['amount']>0:  # Check if I already own this stock
            # check if I'm within the stock tolerance
            if abs(1-stock.goingPrice()/self.__holdings[stock]['purchasePrice']) > self.__stopLoss:
                # Sell
                stock.stockSold()
                self.__holdings[stock]['amount'] -= 1  # remove from my own ledger
                # print(self.__holdings[stock]['amount'])  # add to my own ledger
                self.__money += stock.goingPrice()  # pocket the windfall
                self.__holdings[stock]['purchasePrice'] = 0
                return False, "Sell"
            else:
                return True, "Keep"
        else:  # nope, that's new
            if stock.volatility()<=self.__stopLoss: # check volatility
                # Buy
                stock.stockBought()
                self.__holdings[stock]['amount'] += 1  # add to my own ledger
                # print(self.__holdings[stock]['amount'])  # add to my own ledger
                self.__money -= stock.goingPrice()  # deduct the price
                self.__holdings[stock]['purchasePrice'] = stock.goingPrice()
                return True, "Buy"
            else:
                return False, "Pass" 

    def __str__(self):
        return "I am " + self.name

    # NOTE: currently deprecate, might bring back if we revert to mass ordering
    # def act(self, listings:list) -> list:
    #     """
    #     Returns an "action" or a list of stock/number pairs corresponding to the by/sell amount
    #     """
    #     stockOrder = {}
    #     for listing in listings:
    #         stockOrder[listing.key] = self.analyzeStock(listing)

    #     # Do I mamage the amount of stacks
    #     # How do I Balance the amount of
    #     # WHen do I remove stocks
    #     # when is it okay to remove.
    
    #    return [("NAN", 0)]


"""
Currently, these classes are only modified the abstract classes
"""
class RiskAvers(Trader):
    def __init__(self, allTheStocks) -> None:
        super().__init__(allTheStocks, stopLost=0.05, name="riskAvers   ")


class RiskNeutral(Trader):
    def __init__(self, allTheStocks) -> None:
        super().__init__(allTheStocks, stopLost=0.02, name="riskNeutral ")


class RiskTolerant(Trader):
    def __init__(self, allTheStocks) -> None:
        super().__init__(allTheStocks, stopLost=0.01, name="riskTolerant")


# TODO, actually write these.

class WildCard(Trader):
    def __init__(self, allTheStocks) -> None:
        super().__init__(allTheStocks, stopLost=0.25)

    def act(self, listings) -> list:
        return [("NAN",0)]


class Oscillator(Trader):
    def __init__(self, allTheStocks) -> None:
        super().__init__(allTheStocks, stopLost=0.1)

    def act(self, listings) -> list:
        return [("NAN",0)]