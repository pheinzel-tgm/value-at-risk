import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import numpy as np
import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import json
    
class ValueAtRisk:
  def __init__(self, tickers, initial_investment, time):
    
    # Create our portfolio of equities
    self.tickers = tickers
    
    # Set the investment weights (I arbitrarily picked for example)
    self.weights = np.array(1)
    
    # Set an initial investment level
    self.initial_investment = initial_investment
    
    # self.timeframe = timeframe
    self.time = int(time)

  def getVar95( self ):
    data = pdr.get_data_yahoo(self.tickers, start=dt.date.today( ) - relativedelta(months=+self.time) , end=dt.date.today())['Close']
    returns = data.pct_change()

    returns_sorted = returns.sort_values(by=returns.columns[0], ascending=True)

    count = returns_sorted.count()

    var95helper = count * 0.05

    var95 = returns_sorted.iat[int(var95helper), 0]

    return var95.to_json()

  def getVar99( self ):
    data = pdr.get_data_yahoo(self.tickers, start=dt.date.today( ) - relativedelta(months=+self.time), end=dt.date.today())['Close']
    returns = data.pct_change()

    returns_sorted = returns.sort_values(by=returns.columns[0], ascending=True)

    count = returns_sorted.count()

    var99helper = count * 0.01

    var99 = returns_sorted.iat[int(var99helper), 0]

    return var99.to_json()

  def getResult( self, json=None ):
    print("- * -")
    data = pdr.get_data_yahoo(self.tickers, start=dt.date.today( ) - relativedelta(months=+self.time), end=dt.date.today())['Close']
    returns = data.pct_change()

    returns_sorted = returns.sort_values(by=returns.columns[0], ascending=True)

    count = returns_sorted.count()

    var95helper = count * 0.05
    var99helper = count * 0.01

    var95 = abs(returns_sorted.iat[int(var95helper), 0])
    var99 = abs(returns_sorted.iat[int(var99helper), 0])

    var95pretty = round(abs(returns_sorted.iat[int(var95helper), 0]) * 100, 2)
    var99pretty = round(abs(returns_sorted.iat[int(var99helper), 0]) * 100, 2)

    var95per = round(var95 * self.initial_investment, 2)
    var99per = round(var99 * self.initial_investment, 2)

    returnjson = returns_sorted.to_json()

    #add to return array
    data = returnjson + ", { \"var\": [ "+str( var95pretty )+", "+str( var99pretty )+"]}" + ", { \"varactual\": [ "+str( var95per )+", "+str( var99per )+"] }"
    returnjson = data
        
    print("Value at Risk 95% Percent === ", var95)
    print("Value at Risk 95% Actual === ", var95per)
    print("Value at Risk 99% Percent === ", var99)
    print("Value at Risk 95% ACtual === ", var99per)
    if json == True:
      print("JSON: ")
      print(returnjson)
      return returnjson
    else:
      return returns_sorted
    
if __name__ == "__main__":
  v = ValueAtRisk( ['AAPL'], 1000000 )
  a = v.getResult( )
  print(a)
