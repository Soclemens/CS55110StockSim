class Trader:
    """Abstract class to allow for interfacing with env
       Contains act() and a default constructor"""

    def __init__(self, money=10_000, stopLoss=0.25) -> None:
        self.__money = money
        '''
        Do we want holdings to be a list of a class object or just a list of tuples?
        -Spencer
        '''
        self.__holdings = []  # list of stokes, amount, & their purchase price
        self.__stopLost = stopLoss  # persentage return. TODO, figure out of this should be flat, or percentile

    def act(self, listings: list) -> list:
        """
        Returns an "action" or a list of stock/number pairs corresponding to the by/sell amount
        """
        return [("NAN", 0)]


class RiskSeeking(Trader):
    def __init__(self, money=10_100) -> None:
        super().__init__(money=money, stopLoss=0.5)

    def act(self, listings) -> list:
        return [("NAN", 0)]


class RiskNeutral(Trader):
    def __init__(self, money=10_100) -> None:
        super().__init__(money=money, stopLoss=0.25)

    def act(self, listings) -> list:
        return [("NAN", 0)]


class WildCard(Trader):
    def __init__(self, money=10_100) -> None:
        super().__init__(money=money, stopLoss=0.25)

    def act(self, listings) -> list:
        return [("NAN", 0)]


class Oscillator(Trader):
    def __init__(self, money=10_100) -> None:
        super().__init__(money=money, stopLoss=0.1)

    def act(self, listings) -> list:
        return [("NAN", 0)]
