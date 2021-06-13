from agent import Trader


from env import *
from agent import *

def initialize():
    # set up
    gameLoop()

def gameLoop():
    while True:
        # get perset for the day, give it to agents
        # get actions from agents, pass those actions to evn
        # return prices from evn to agents
        # fluctuate stocks for the day
        break



if __name__ == 'main':
    initialize()
    agent = RiskNeutral()
    agent.act()
    evn = StockMarket()