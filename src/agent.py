from random import uniform


from random import uniform

def map(value, a1, a2, b1, b2):
    """
    Maps a value from one range to another range
    """
    return b1 +(value-a1)*(b2-b1)/(a2-a1)

class Order():
    def __init__(self, stock, volume):
        self.stock = stock
        self.volume = volume
        self.boughtAt = stock.goingPrice()
    
    def worth(self):
        return self.stock.goingPrice() *self.volume

    def __repr__(self):
        msg = 'stock:'+ format(self.stock.name, '3s')
        msg += '  num:' + format(self.volume, '6.2f')
        msg += '  boughtAt:' + format(self.boughtAt, '6.2f')
        msg += '  now:' + format(self.stock.goingPrice(),'6.2f')
        return msg


class Trader:
    """Abstract class to allow for interfacing with env
       Contains act() and a default constructor"""

    def __init__(self, name="ABSTRACT", stopLoss=2, idealRisk = 2, budget=500) -> None:
        self.name = name  # Dump little ID for pretty printing the type of agent for the report
        self.portfolio = []
        self.stopLoss = stopLoss  # persentage of return I want
        self.idealRisk = idealRisk
        self.money = budget
        self.initialCapital = budget
        self.stats = {'timesBought':0, 'timesSold':0}


    def returns(self):
        """
        return how much money the agent as earned
        """
        return sum([order.worth() for order in self.portfolio]) + self.money -self.initialCapital
        
            
    def printPerformance(self):
        """
        Prints Name, Type, Returns(netGrowth)
        """
        print(f"Agent:{self.name} made:\t$"+format(self.returns(),".2f"))
    

    def sell(self):
        returnOrders = []
        for order in self.portfolio:
            # is the price outside of my stoploss range?
            if abs(order.stock.goingPrice()/order.boughtAt-1) >= self.stopLoss/100:
                self.money += order.worth()  # cash out the holding
                for _ in range(int(order.volume)): order.stock.stockSold()  # log transaction
                returnOrders.append(('Sold   ', order)) # log action
                self.portfolio.remove(order)  # remove from my portfolio
        return returnOrders


    def buy(self, todaysListing, soldOrders):
        actions = []
        shopingCard = []
        # This is the ideal risk I want per dollar
        ideal_unit_risk = self.idealRisk/self.initialCapital
        tolerance = self.idealRisk  # surrogate for a better metric, or using another parameter.
        
        for stock in todaysListing:
            # if I just sold this stock, don't buy it back!
            if stock in [order.stock for _,order in soldOrders]:continue
            # If I already own this stock, don't buy more! (for now)
            if stock in [order.stock for order in self.portfolio]: continue

            # risk per dollar of my investment
            unit_risk = stock.volatility()/stock.goingPrice()
            distaste = abs(unit_risk/ideal_unit_risk-1)  # (0% - 100%)
            # print(distaste)
            if distaste < tolerance: # here is the threshold for excitability (10% of my ideal risk)
                shopingCard.append((stock, distaste))  # add this order to the card (paired with the unit risk)
                
        # sort card by items closest to my ideal risk level
        if len(shopingCard)>0 and self.money>0:
            shopingCard = sorted(shopingCard, key=lambda pair: pair[1])  # sort by distance from idealUnitRisk
            budgetMax = self.money/len(shopingCard)*2  # find the budgest for each stock
            for stock, distaste in shopingCard:
                # uses a proportional 
                amount = (budgetMax * (1-map(distaste,0,tolerance,0,1)))/stock.goingPrice()  # the proportional amount of money I should spend
                newOrder = Order(stock, amount)
                for _ in range(int(amount)): stock.stockBought()  # log transaction
                self.portfolio.append(newOrder)  # save this stock in my own records
                actions.append(("Bought ", newOrder)) # record action
                self.money -= newOrder.worth()  # balance the books

        return actions


    def act(self, todaysListing):

        soldOrders = self.sell()  # doesn't required todays listing 
        buyOrders = self.buy(todaysListing, soldOrders)

        return soldOrders + buyOrders


"""
Currently, these classes are only modified the abstract classes
"""
class RiskAvers(Trader):
    def __init__(self, ID=1):
        super().__init__(stopLoss=5 + uniform(0, 3), idealRisk=1  + uniform(0, 1), name="Risk Adverse " + str(ID))


class RiskNeutral(Trader):
    def __init__(self, ID=1):
        super().__init__(stopLoss=10 + uniform(0, 4), idealRisk=2 + uniform(0, 1), name="Risk Neutral " + str(ID))


class RiskTolerant(Trader):
    def __init__(self, ID=1):
        super().__init__(stopLoss=20 + uniform(0, 5), idealRisk=3 + uniform(0, 1), name="Risk Tolerant " + str(ID))
