from flask import Flask
from flask import request
from flask import Response
import webview
from var import ValueAtRisk
import os
import threading
import sys


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    stocks = request.args.get('stocks')
    #weights = request.args.get('weights')
    #print( request.args.get('investment') )
    investment = request.args.get('investment')
    # timeframe = request.args.get('timeframe')
    
    stocks = stocks.replace(" ","")
    stocks = stocks.split(",")
    
    #weights = weights.replace(" ","")
    #weights = weights.split(",")
    
    #for i in range(0, len(weights)):
    #  weights[i] = float(weights[i])
    
    print("INV: "+str(investment))
    investment = int(investment)
      
    # timeframe = timeframe.replace(" ","")
    # timeframe = timeframe.split(",")
    
    print("Stocks: "+str(stocks))
    #print("weights: "+str(weights))
    print("investment: "+str(investment))
    # print("timeframe: "+str(timeframe))
    
    var = ValueAtRisk( stocks, investment )
    resp = Response("{\"errorcode\": 0, \"output\":["+var.getResult(True)+"]}")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
  
@app.route('/ui', methods=['POST', 'GET'])
def showUi():
  f = open("index.html","r")
  txt = f.read( )
  resp = Response(txt)
  resp.headers['Access-Control-Allow-Origin'] = '*'
  return txt

@app.route('/stocks.js', methods=['GET'])
def showStocks():
  f = open("./stocks.js","r")
  txt = f.read( )
  resp = Response(txt)
  resp.headers['content-type'] = 'application/javascript'
  return txt

def start_server():
    app.run(host='0.0.0.0', port=5000)
    

t = threading.Thread(target=start_server)
t.daemon = True
t.start()

try:
  webview.create_window('Value at Risk', 'index.html')
  webview.start(debug=True)
except:
  sys.exit()

