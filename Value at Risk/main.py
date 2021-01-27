from flask import Flask
from flask import request
from flask import Response, redirect
from var import ValueAtRisk
import os
import threading
import sys
import datetime

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    stocks = request.args.get('stocks')
    #weights = request.args.get('weights')
    #print( request.args.get('investment') )
    investment = request.args.get('investment')
    timeframe = request.args.get('timeInMonths')
    
    stocks = stocks.replace(" ","")
    stocks = stocks.split(",")
    
    #weights = weights.replace(" ","")
    #weights = weights.split(",")
    
    #for i in range(0, len(weights)):
    #  weights[i] = float(weights[i])
    
    print("INV: "+str(investment))
    investment = int(investment)
      
    timeframe = timeframe.replace(" ","")
    timeframe = timeframe.replace("[","")
    timeframe = timeframe.replace("]","")
    timeframe = timeframe.replace("'","")
    
    print("Stocks: "+str(stocks))
    #print("weights: "+str(weights))
    print("investment: "+str(investment))
    print("timeframe: "+str(timeframe))
    
    var = ValueAtRisk( stocks, investment, timeframe )
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
  
@app.route('/addStock', methods=['GET'])
def addStocks():
    with open('./stocks.js','r') as f:
        lines = f.readlines()

    with open('./stocks.js','w') as f:
       new_value = 'Something New'
       for line in lines:
           if line.startswith(']'):
               line = line.replace(']', '[' + request.args.get('stock') + '],')
           f.write(line)

    with open("./stocks.js","a") as f:
        f.write("\n]")
    
    return redirect("http://127.0.0.1:5000", code=200)

@app.route('/save', methods=['POST'])
def save():
    ts = datetime.datetime.now().timestamp()
    ts = datetime.datetime.fromtimestamp(ts).isoformat()
    
    ts = ts.replace(":", "-")
    
    filename = './Portfolios/' + ts + '-portfolio.json'
    
    print (request.get_data())
    
    data = str(request.get_data())
    data = data.replace("'", "")
    data = data[1:]
    
    print (data)
    
    with open(filename,'w') as f:
        f.write(data)
        
    return redirect("http://127.0.0.1:5000", code=200)

def start_server():
    app.run(host='127.0.0.1', port=5000)
    

#t = threading.Thread(target=start_server)
#t.daemon = True
#t.start()
  
def main():
    start_server()

if __name__ == "__main__":
    main()

