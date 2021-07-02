from random import uniform

class Trader:
    """Abstract class to allow for interfacing with env
       Contains act() and a default constructor"""

    #NOTE: Not used. Only 20 stocks are permitted, 1 of each stock
    #NOTE: Currently, there is not debt limit
    def __init__(self, stopLoss=2, idealRisk = 2, name="ABSTRACT") -> None:
        self.name = name  # Dump little ID for pretty printing the type of agent for the report
        self.returns = 0
        self.portfolio = []
        self.stopLoss = stopLoss  # persentage of return I want
        self.idealRisk = idealRisk


    # def netWorth(self):
    #     """
    #     return the current net worth (money + sum of each stock's current price)
    #     """
    #     return self.money + sum([stock.goingPrice() * sum([i['amount'] for i in self.portfolio[stock]]) for stock in self.portfolio])
    #
    # def print(self, showPortfolio = False):
    #     """
    #     for printing the agent with its Type, Networth, then its portfolio of stocks with each price
    #     """
    #     msg = f"Agent:{self.name}\t"+ "NetWorth:" + format(self.netWorth(),".2f") +"\n\t"
    #
    #     if showPortfolio:
    #
    #         msg += "\n\t".join([
    #             "stock("+stock.name+"): "+ str(sum([i['amount'] for i in self.portfolio[stock]]))
    #                 +", "+format(stock.goingPrice(),".2f")
    #             for stock in self.portfolio.keys() if sum([i['amount'] for i in self.portfolio[stock]])>0
    #         ])
    #
    #     print(msg)
    #
    # def narrateActions(self, order):
    #     """
    #     TODO: Will help with debugging and logging actions
    #     """
    #     if sum([order[stock] for stock in order])>0:
    #         print("Agent:"+self.name,"ordered")
    #         for stock in order:
    #             if order[stock]>0:
    #                 print('\t',order[stock], "of stock",stock.name)
    #     else:
    #         print("Agent:"+self.name,"Passed this turn")

    def act(self, stock):
        flag = True  # if stay true we can buy
        # figure out if I own the stock
        for orderItem in self.portfolio:
            if orderItem.stock == stock:
                flag = False  # Prevents me from buying IE we already have this stock no need to buy again
                if stock.goingPrice() - (orderItem.boughtAt * (self.stopLoss / 100)) > orderItem.boughtAt:  # sell branch
                    self.returns += stock.goingPrice() - orderItem.boughtAt
                    self.portfolio.remove(orderItem)
                    return "Sell Stock ", stock.name


        if stock.volatility() - 1 < self.idealRisk > stock.volatility() + .75 and flag:  # buy branch
            self.portfolio.append(Order(stock))
            stock.stockBought()
            return "Buy Stock ", stock.name

        return None

class Order():
    def __init__(self, stock):
        self.stock = stock
        self.boughtAt = stock.goingPrice()


"""
Currently, these classes are only modified the abstract classes
"""
class RiskAvers(Trader):
    def __init__(self, stocks, id) -> None:
        super().__init__(stopLoss=5 + uniform(0, 3), idealRisk=1  + uniform(0, 1), name="(risk adverse:" + str(id) + ")")


class RiskNeutral(Trader):
    def __init__(self, stocks, id) -> None:
        super().__init__(stopLoss=10 + uniform(0, 4), idealRisk=2 + uniform(0, 1), name="(risk Neutral:" + str(id) + ")")


class RiskTolerant(Trader):
    def __init__(self, stocks, id) -> None:
        super().__init__(stopLoss=20 + uniform(0, 5), idealRisk=3 + uniform(0, 1), name="(risk Tolerant:" + str(id) + ")")


# TODO, actually write these.
#
# class WildCard(Trader):
#     def __init__(self, stocks) -> None:
#         super().__init__(stocks, stopLoss=0.25)
#
#     def act(self, listings) -> list:
#         return [("NAN",0)]
#
#
# class Oscillator(Trader):
#     def __init__(self, stocks) -> None:
#         super().__init__(stocks, stopLoss=0.1)
#
#     def act(self, listings) -> list:
#         return [("NAN",0)]