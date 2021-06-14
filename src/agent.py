
class Trader:
    """Abstract class to allow for interfacing with env
       Contains act() and a default constructor"""
    def __init__(self, money=10_000, stopLost=0.25) -> None:
        self.__money = money
        self.__holdings = []  # list of stokes, amount, & their purchase price
        self.__log = []  # logs of actions taken
        self.__stopLoss = stopLost  # persentage return. TODO, figure out of this should be flat, or percentile

    def act(self, listings:list) -> list:
        """
        Returns an "action" or a list of stock/number pairs corresponding to the by/sell amount
        """
        for i in listings: print(i)
        return [("NAN", 0)]

    def adjustBalance(self, money):
        self.__money += money

    
class RiskSeeking(Trader):
    def __init__(self, money=10_100) -> None:
        super().__init__(money=money, stopLost=0.5)

    def act(self, listings) -> list:
        return [("NAN",0)]

class RiskNeutral(Trader):
    def __init__(self, money=10_100) -> None:
        super().__init__(money=money, stopLost=0.25)

    def act(self, listings: list) -> list:
        return super().act(listings)

class RiskNeutral(Trader):
    def __init__(self, money=10_100) -> None:
        super().__init__(money=money, stopLost=0.1)

    def act(self, listings) -> list:
        return [("NAN",0)]

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