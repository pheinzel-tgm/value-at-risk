import pandas as pd
import os
import quandl
import time
from datetime import * 
import dateutil

quandl.ApiConfig.api_key = "oq6oEJ2K3qbxskDG5iAv"

def getData(name, startDate, endDate):
    data = quandl.get(name, start_date = startDate)
    print(data)

while(True):
    print("Name: ")
    name = input()
    print("Time in Months: ")
    i_months = input()
    dateToday = datetime.strptime(str(date.today()), "%Y-%m-%d")
    d_months = dateutil.relativedelta.relativedelta(months=int(i_months))
    s_date = dateToday - d_months
    print("Getting Data for " + name + " from the last " + i_months + " months")
    getData(name, str(s_date), date.today)
