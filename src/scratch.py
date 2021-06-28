import scipy.stats as stats
from random import randint, uniform
from statistics import stdev

lowerPrice, upperPrice = 0.01, 500
# mu is mean, sigma is stdev
for i in range(10):
    mu = uniform(0.01, 1000)  # this is the mean price of the stock
    sigma = uniform(0, 4)  # this is the volatility percentage of a stock
    dist = stats.truncnorm((lowerPrice - mu) / sigma, (upperPrice - mu) / sigma, loc=mu, scale=sigma)

    values = dist.rvs(5)
    print("calculated stdev", stdev(values))
    print(mu, ":", sigma)