
class Order():
    def __init__(self, stock, volume):
        self.stock = stock
        self.volume = volume
        self.boughtAt = stock.goingPrice()
    
    def worth(self):
        return self.stock.goingPrice() *self.volume

    def __repr__(self):
        msg = 'stock:'+self.stock.name
        msg += ', num:' + str(self.volume)
        msg += ', boughtAt:' + format(self.boughtAt, '.2f')
        msg += ', now:' + format(self.stock.goingPrice(),'.2f')
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
                for _ in range(order.volume): order.stock.stockSold()  # log transaction
                returnOrders.append(('Sold', order)) # log action
                self.portfolio.remove(order)  # remove from my portfolio
        return returnOrders


    def buy(self, todaysListing, soldOrders):
        actions = []
        shopingCard = []
        for stock in todaysListing:
            # if I just sold this stock, don't buy it back!
            if stock in [order.stock for _,order in soldOrders]:continue
            # If I already own this stock, don't buy more! (for now)
            if stock in [order.stock for order in self.portfolio]: continue

            # find the optimal amount of this stock to purchase
            ideal_amount = self.idealRisk / stock.volatility()
            closest_amount = sorted([int(ideal_amount),int(ideal_amount)+1],
                key=lambda amount:abs(self.idealRisk - amount*stock.volatility())
            )[0]
            
            #TODO: Get this checked and see if this is what was meant
            # if stock.volatility() - 1 < self.idealRisk < stock.volatility() + .75:  # buy branch
            
            # is this adjusted volatility outside of my confort zone? 
            if self.idealRisk+1 > closest_amount*stock.volatility() > self.idealRisk-0.75:  # buy branch
                shopingCard.append(Order(stock, closest_amount))  # add this order to the card
            
        # sort card by items closest to my ideal risk level
        for order in sorted(shopingCard, key=lambda order:abs(self.idealRisk - order.stock.volatility()*order.volume)):
            if self.money >= order.worth():
                for _ in range(order.volume): order.stock.stockBought()  # log transaction
                self.portfolio.append(order)  # save this stock in my own records
                actions.append(("Bought ", order)) # record action
                self.money -= order.worth()  # balance the books

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
        super().__init__(stopLoss=5, idealRisk=1, name="Risk Adverse " + str(ID))


class RiskNeutral(Trader):
    def __init__(self, ID=1):
        super().__init__(stopLoss=10, idealRisk=2, name="Risk Neutral " + str(ID))


class RiskTolerant(Trader):
    def __init__(self, ID=1):
        super().__init__(stopLoss=20, idealRisk=3, name="Risk Tolerant " + str(ID))
