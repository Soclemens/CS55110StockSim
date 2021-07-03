import matplotlib.pyplot as plt
from numpy.lib.function_base import average
from env import *
from agent import *
import typer
from typing import Optional

app = typer.Typer()
TRADING_DAYS = 2


@app.command()
def gameLoop(actorCount: Optional[int] = 1, traidingDays: Optional[int] = 10, marketSize: Optional[int] = 30):
    stockMarket = StockMarket(marketSize=marketSize)  # initialize the stock market
    agents = []  # make a abstract container of agents
    agents.extend([RiskNeutral(ID=i+1) for i in range(actorCount)])  # makes x of neutral type of agent
    agents.extend([RiskTolerant(ID=i+1) for i in range(actorCount)])  # makes x of tolerant type of agent
    agents.extend([RiskAvers(ID=i+1) for i in range(actorCount)])  # makes x of avers type of agent
    for i in range(traidingDays+1):  # Trade for x days
        todaysListing = stockMarket.getStockListings()  # get todays prices
        for agent in agents:  # for each agent
            actions = agent.act(todaysListing)
            if len(actions)>0:
                print(agent.name+':')
                for act, order in actions:
                    print('\t', act, order)
        stockMarket.updateMarket()  # update stock prices for tomorrow

        print("Finished day " + str(i+1) + " out of " + str(TRADING_DAYS) + "... " + format((i+1)/TRADING_DAYS,'.2%'))
        print("--------------------------------------------------------------------------------------------------------")
    
    reportStats(agents, x)
    graph(stockMarket)


def reportStats(agents, numAgents):
    print("///////// STATS REPORT /////////")
    average = {'tolerant':0, 'neutral':0, 'avers':0 }
    for agent in agents:
        agent.printPerformance()
        if type(agent) == RiskAvers: average['avers']+= agent.returns()/numAgents
        elif type(agent) == RiskNeutral:  average['neutral']+= agent.returns()/numAgents
        elif type(agent) == RiskTolerant:  average['tolerant']+= agent.returns()/numAgents
    print('The average returns of each agent type was')
    print('\tRisk Averse:  ', '$'+format(average['avers'],'0.2f'))
    print('\tRisk Neutral: ', '$'+format(average['neutral'],'0.2f'))
    print('\tRisk Tolerant:', '$'+format(average['tolerant'],'0.2f'))


def graph(stockMarket):
    stocks = stockMarket.getStockListings()
    avgPrice = []

    for day in range(len(stocks[0].getPriceHistory())):
        price = 0
        for stock in stocks:
            price += stock.getPriceHistory()[day]
        avgPrice.append(price/len(stocks))

    plt.plot(avgPrice)
    plt.title("Average Stock Market Trend (SMP)")
    plt.xlabel("Day")
    plt.ylabel("Price($)")
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    app()
