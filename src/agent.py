
class Trader:
    """Abstract class to allow for interfacing with env
       Contains act() and a default constructor"""

    #NOTE: Not used. Only 20 stocks are permitted, 1 of each stock
    #NOTE: Currently, there is not debt limit
    def __init__(self, stocks, stopLost=0.02, idealRisk = 0.02, money=10_000, name="ABSTRACT") -> None:
        self.name = name  # Dump little ID for pretty printing the type of agent for the report
        self.money = money  # limit for what the 
        self.portfolio = { 
            stock:[]  # {'num':0,'purchasePrice':0}  # allow for multiple instances of a stock
            for stock in stocks
        }  
        self.__log = []  # logs of actions taken
        self.stopLoss = stopLost  # persentage of return I want
        self.idealRisk = idealRisk


    def netWorth(self):
        """
        return the current net worth (money + sum of each stock's current price)
        """
        return self.money + sum([stock.goingPrice() * sum([i['num'] for i in self.portfolio[stock]]) for stock in self.__portfolio.keys()])
        
    def print(self, showPortfolio = False):
        """
        for printing the agent with its Type, Networth, then its portfolio of stocks with each price
        """
        msg = f"Agent:{self.name}\t"+ "NetWorth:" + format(self.netWorth(),".2f") +"\n\t"
        
        if showPortfolio:
            msg += "\n\t".join([
                "stock:"+stock.name+", "+format(stock.goingPrice(),".2f") 
                for stock in self.portfolio.keys() if sum([i['num'] for i in self.portfolio[stock]])>0
            ])
        
        print(msg)

    def narrateActions(self):
        """
        Will help with debugging and logging actions
        """
        ...


    def act(self, stock):
        """
        TODO: Figure out if this is the right way to do this
            Currently just tries to sell based on stoplose
            Buys based on portfolio management of risk
        """
        # determine what to sell
        mySale = self.__makeSale()
        # determine what to buy
        myOrder = self.__makePurchase()
        # compile results
        compiledOrder = mySale
        for stock in myOrder:
            compiledOrder[stock] += myOrder[stock]
                
        # TODO: Need to log actions...some how
        self.narrateActions()
        # Make the purchases for internal logs
        self.__updatePortfolio(compiledOrder)

        return compiledOrder

    def __updatePortfolio(self, order):
        for stock in order:
            amount = order.get(stock)
            if amount<0:  # remove stock from portfolio
                while amount<0:  # for each listing 
                    listing = self.portfolio[stock].pop(0)
                    if listing['amount']+amount>0:  # too much in this listting to sell it all
                        difference = listing['amount'] + amount
                        listing['amount'] = 'negative'
                    else:
                        amount += listing['amount']
                        self.money += stock.goingPrice() * listing['amount']

            elif amount>0:  # add stock to portfolio
                ...


    def __makeSale(self):
        receipt = {}
        for stock in self.portfolio:
            receipt[stock] = 0
            for listing in self.portfolio.get(stock):
                if abs(stock.goingPrice() - listing['purchasePrice'])/listing['purchasePrice'] >= self.stopLoss:
                    receipt[stock] = -listing['num']
        return receipt

    def __makePurchase(self):
        # TODO: Might need to establish hard limits for volatility
        # currently just preference
        """
        Figure out what I want to buy, and how much
        """
        optimalNum = [] # what I think I want
        for stock in self.portfolio:
            # DEPRECATED: 
                # risk assumed per $1 of this stock
                # fragmented_risk = stock.volatility/stock.goingPrice()
            # what would be the ideal amount of this stock to buy
            # TODO: Make sure this math makes sense!!!!
            ideal_amount = self.idealRisk / stock.volatility
            # what is the closest whole number approximation of that ideal_amount
            closest_amount = sorted(
                [int(ideal_amount),int(ideal_amount)+1],
                key=lambda x:abs(self.idealRisk - x*stock.volatility)
            )[0]
            # offset for how much I already own (across all listings I have for this stock)
            amount = closest_amount - sum([i.get('amount') for i in self.portfolio[stock]])
            optimalNum.append((stock, amount, stock.volatility*amount))
        # sort by best risk
        optimalNum = sorted(optimalNum, key=lambda x : abs(x[2]-self.idealRisk))
        # filter for what I can afford
        cost = 0
        order = {}
        for stock, amount, risk in optimalNum:
            # TODO: Here is where the tolerance check might go
            # make sure I can afford it
            if cost+(stock.goingPrice()*amount) <= self.money:
                cost += stock.goingPrice()*amount
                order[stock] = amount
            # else:
            #     break
        return order

"""
Currently, these classes are only modified the abstract classes
"""
class RiskAvers(Trader):
    def __init__(self, stocks) -> None:
        super().__init__(stocks, stopLost=0.05, idealRisk=0.01, name="riskAvers   ")


class RiskNeutral(Trader):
    def __init__(self, stocks) -> None:
        super().__init__(stocks, stopLost=0.02, idealRisk=0.02, name="riskNeutral ")


class RiskTolerant(Trader):
    def __init__(self, stocks) -> None:
        super().__init__(stocks, stopLost=0.01, idealRisk=0.04, name="riskTolerant")


# TODO, actually write these.

class WildCard(Trader):
    def __init__(self, stocks) -> None:
        super().__init__(stocks, stopLost=0.25)

    def act(self, listings) -> list:
        return [("NAN",0)]


class Oscillator(Trader):
    def __init__(self, stocks) -> None:
        super().__init__(stocks, stopLost=0.1)

    def act(self, listings) -> list:
        return [("NAN",0)]