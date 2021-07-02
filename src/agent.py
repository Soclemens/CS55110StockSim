
class Trader:
    """Abstract class to allow for interfacing with env
       Contains act() and a default constructor"""

    #NOTE: Not used. Only 20 stocks are permitted, 1 of each stock
    #NOTE: Currently, there is not debt limit
    def __init__(self, stocks, stopLoss=2, idealRisk = 2, money=10_000, name="ABSTRACT") -> None:
        self.name = name  # Dump little ID for pretty printing the type of agent for the report
        # self.money = money  # limit for what the
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
        if (stock.volatility() - 1 < self.idealRisk > stock.volatility() + .75) and not self.portfolio.__contains__(stock):  # buy branch
            self.portfolio.append(stock)
            return "Buy Stock ", stock.name
        elif (stock.volatility() > self.idealRisk) and self.portfolio.__contains__(stock):  # sell branch
            print("my vol: ", self.idealRisk, ". The vol: ", stock.volatility())
            self.portfolio.remove(stock)
            return "Sell Stock ", stock.name
        else:
            # print("my vol: ", self.idealRisk, ". The vol: ", stock.volatility())
            return None


"""
Currently, these classes are only modified the abstract classes
"""
class RiskAvers(Trader):
    def __init__(self, stocks, id) -> None:
        super().__init__(stocks, stopLoss=1, idealRisk=1, name="(risk adverse:" + str(id) + ")")


class RiskNeutral(Trader):
    def __init__(self, stocks, id) -> None:
        super().__init__(stocks, stopLoss=1, idealRisk=2, name="(risk Neutral:" + str(id) + ")")


class RiskTolerant(Trader):
    def __init__(self, stocks, id) -> None:
        super().__init__(stocks, stopLoss=4, idealRisk=3, name="(risk Tolerant:" + str(id) + ")")


# TODO, actually write these.

class WildCard(Trader):
    def __init__(self, stocks) -> None:
        super().__init__(stocks, stopLoss=0.25)

    def act(self, listings) -> list:
        return [("NAN",0)]


class Oscillator(Trader):
    def __init__(self, stocks) -> None:
        super().__init__(stocks, stopLoss=0.1)

    def act(self, listings) -> list:
        return [("NAN",0)]