import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from datetime import datetime,timedelta
import math

stocks=['RELIANCE.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'BHARTIARTL.NS', 'TCS.NS']

portfolio={}
for i in stocks:        #A dictionary 'portfolio' to store the stocks and their respective quantities
    portfolio[i]=0
    
#data=yf.download(stocks,end=end_date, start=start_date, group_by='ticker', interval='1d', progress=False)
#print(data)
current_portfolio_value=1000000
liquid_cash=1000000  # Initial capital of 10 Lakhs   
trades=[]
daily_portfolio_value=[]
entry_price_tracker={stock:0 for stock in stocks}  # To track the entry price of each stock
                #Started with an initial capital of 10 Lakhs and the portfolio 
                                        #value is updated with the current value of the stocks in the portfolio
#df=pd.DataFrame(data)
#print(df)
#df.to_csv("Top5_Nifty50_Stocks.csv")

class Stocks():
     
    
        def __init__(self,ticker):
            self.ticker=ticker

            
            
    
        def Upper_band(self,counter):
            share_name=yf.Ticker(self.ticker)
            self.highs=share_name.history(start=datetime.today().date()-timedelta(days=90-counter),end=datetime.today().date()-timedelta(days=60-counter) ,interval='1d')['High'].tolist()
            
            return np.max(self.highs)

        def Lower_band(self,counter):
            share_name=yf.Ticker(self.ticker)
            self.lows=share_name.history(start=datetime.today().date()-timedelta(days=90-counter),end=datetime.today().date()-timedelta(days=60-counter) ,interval='1d')['Low'].tolist()
            
            return np.min(self.lows)
        
        def Today_price(self,counter=0):
            share_name=yf.Ticker(self.ticker)
            close_price=share_name.history(start=datetime.today().date()-timedelta(days=60-counter),end=datetime.today().date(),interval='1d')['Close'].iloc[0]
            return close_price
        
        def buy(self,volume,counter):
            global liquid_cash, portfolio, trades
            if self.ticker in portfolio:
                portfolio[self.ticker]+=volume
                liquid_cash -= volume * self.Today_price(counter)
                trades.append({'ticker': self.ticker, 'action': 'buy', 'volume': volume, 'price': self.Today_price(counter=counter)})
                entry_price_tracker[self.ticker]= self.Today_price(counter=counter)  # Update entry price for existing stock

            else:
                portfolio[self.ticker]=volume
                liquid_cash -= volume * self.Today_price(counter=counter)
                trades.append({'ticker': self.ticker, 'action': 'buy', 'volume': volume, 'price': self.Today_price(counter=counter)})
                entry_price_tracker[self.ticker]=self.Today_price(counter=counter) # Track entry price
        def sell(self,volume,counter):
            global liquid_cash, portfolio, trades
            if self.ticker in portfolio:
                if portfolio[self.ticker] >= volume:
                    portfolio[self.ticker]-=volume
                    liquid_cash += volume * self.Today_price(counter)
                    trades.append({'ticker': self.ticker, 'action': 'sell', 'volume': volume, 'price': self.Today_price(counter=counter)})
                else:
                    print(f"Not enough shares to sell for {self.ticker}")

            else:
                print(f"{self.ticker} not in portfolio")


            
             
        
# while(True):
#      for i in stocks:
#           live_price=yf.
Reliance=Stocks('RELIANCE.NS')
HDFC_Bank=Stocks('HDFCBANK.NS')
ICICI_Bank=Stocks('ICICIBANK.NS')
TCS=Stocks('TCS.NS')
Bharti=Stocks('BHARTIARTL.NS')


stocks_list=[Reliance, HDFC_Bank, ICICI_Bank, TCS, Bharti]
counter=0
peak=1000000
drawdown_tracker=[]
cash_used_tracker=[] 
share_history=[] # Initial capital of 10 Lakhs
# Loop to simulate trading for the last 30 days

while(counter < 60):
     
     current_portfolio_value= liquid_cash 
     
     for stock in stocks_list:
          close_price=stock.Today_price(counter=counter)
          upper_band=stock.Upper_band(counter=counter)
          lower_band=stock.Lower_band(counter=counter)
          
          if stock.ticker in portfolio:
              current_portfolio_value += portfolio[stock.ticker] * close_price
              
          
          if close_price > upper_band and liquid_cash>=100*close_price:
              # Cap at 300, but scale up linearly with cash
            scaled=min(100,(0.4*liquid_cash)/close_price)       #buy and sell
            stock.buy(scaled,counter=counter)
            
            
          elif close_price < lower_band and portfolio[stock.ticker]>0:
            scaled=min(100, portfolio[stock.ticker])
            stock.sell(scaled, counter=counter)
          elif close_price <0.95*entry_price_tracker[stock.ticker] and portfolio[stock.ticker]>0:
            scaled=min(100, portfolio[stock.ticker])
            stock.sell(scaled, counter=counter)
          elif close_price >1.1*entry_price_tracker[stock.ticker] and portfolio[stock.ticker]>0:
            scaled=min(100, portfolio[stock.ticker])
            stock.sell(scaled, counter=counter)
          
     #print(current_portfolio_value)       
            
     counter+=1
     daily_portfolio_value.append({(datetime.today().date()-timedelta(days=60-counter)):current_portfolio_value})
     
     #peak=max(1000000, current_portfolio_value)
     peak=max(peak, current_portfolio_value)  # Ensure peak is at least 10 Lakhs
     drawdown_percentage = ((peak - current_portfolio_value) / peak) * 100
     drawdown_tracker.append({datetime.today().date()-timedelta(days=60-counter): drawdown_percentage})
     share_history.append({(datetime.today().date()-timedelta(days=60-counter)): portfolio.copy()})
     
     print(current_portfolio_value, drawdown_percentage)
     print(portfolio)
     
     
plt.figure('Daily Portfolio Value')
plt.plot([list(d.keys())[0] for d in daily_portfolio_value], [list(d.values())[0] for d in daily_portfolio_value],marker='o', linestyle='-', color='b')
plt.title('Portfolio Value Over Time')
plt.xlabel('Date',fontdict={'fontsize': 14})
plt.ylabel('Portfolio Value (INR)',fontdict={'fontsize': 14})
plt.ylim(950000, 1050000)
#plt.plot([list(d.keys())[0] for d in cash_used_tracker], [list(d.values())[0] for d in cash_used_tracker], marker='o', linestyle='-', color='g', label='Cash Used')
plt.autoscale()

plt.figure('Shares Held')
for stock in stocks_list:
    if stock.ticker not in portfolio:
        portfolio[stock.ticker] = 0  # Ensure all stocks are represented in the portfolio
plt.plot([list(d.keys())[0] for d in share_history],[list(d.values())[0].get('RELIANCE.NS', 0) for d in share_history],color='g',label='Reliance', marker='o', linestyle='-', linewidth=2, markersize=5)
plt.plot([list(d.keys())[0] for d in share_history], [list(d.values())[0].get('HDFCBANK.NS', 0) for d in share_history], color='b', label='HDFC Bank', marker='o', linestyle='-', linewidth=2, markersize=5)
plt.plot([list(d.keys())[0] for d in share_history], [list(d.values())[0].get('ICICIBANK.NS', 0) for d in share_history], color='r', label='ICICI Bank', marker='o', linestyle='-', linewidth=2, markersize=5)
plt.plot([list(d.keys())[0] for d in share_history], [list(d.values())[0].get('TCS.NS', 0) for d in share_history], color='c', label='TCS', marker='o', linestyle='-', linewidth=2, markersize=5)   
plt.plot([list(d.keys())[0] for d in share_history], [list(d.values())[0].get('BHARTIARTL.NS', 0) for d in share_history], color='m', label='Bharti Airtel', marker='o', linestyle='-', linewidth=2, markersize=5)
plt.legend()
plt.title('Number of shares currently holding')
plt.xlabel('Stocks', fontdict={'fontsize': 14})
plt.ylabel('Number of Shares', fontdict={'fontsize': 14})
plt.autoscale()

plt.figure('Drawdown Percentage')
plt.plot([list(d.keys())[0] for d in drawdown_tracker], [list(d.values())[0] for d in drawdown_tracker], marker='o', linestyle='-', color='r')
plt.title('Drawdown Percentage Over Time')
plt.xlabel('Date', fontdict={'fontsize': 14})
plt.ylabel('Drawdown Percentage (%)', fontdict={'fontsize': 14})
plt.ylim(0, 100)
plt.autoscale()


plt.show()






          
          
