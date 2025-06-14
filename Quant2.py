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

            else:
                portfolio[self.ticker]=volume
                liquid_cash -= volume * self.Today_price(counter=counter)
                trades.append({'ticker': self.ticker, 'action': 'buy', 'volume': volume, 'price': self.Today_price(counter=counter)})
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
drawdown_tracker=[]
cash_used_tracker=[]  # Initial capital of 10 Lakhs
# Loop to simulate trading for the last 30 days

fig1,(ax1,ax2,ax3) = plt.subplots(nrows=3,figsize=(10, 5)) 

def update(frame):
    ax1.clear()
    ax2.clear()
    ax3.clear()
    global current_portfolio_value, liquid_cash, portfolio, trades, daily_portfolio_value, drawdown_tracker, counter

    dates = [list(d.keys())[0] for d in daily_portfolio_value]
    portfolio_values = [list(d.values())[0] for d in daily_portfolio_value]
    drawdown_dates = [list(d.keys())[0] for d in drawdown_tracker]
    drawdown_values = [list(d.values())[0] for d in drawdown_tracker]
    
    ax1.plot(dates, portfolio_values, marker='o', linestyle='-', color='blue')
    ax2.plot(drawdown_dates, drawdown_values, marker='o', linestyle='-', color='red')
    ax3.bar(list(portfolio.keys()), list(portfolio.values()), color='g')

    if counter >= 60:
        return
    current_portfolio_value = liquid_cash  # Reset current portfolio value to liquid cash at the start of each day 
    for stock in stocks_list:
        close_price=stock.Today_price(counter=counter)
        upper_band=stock.Upper_band(counter=counter)
        lower_band=stock.Lower_band(counter=counter)
        if stock.ticker in portfolio:
            current_portfolio_value += portfolio[stock.ticker] * close_price
        if close_price > upper_band:
        # Cap at 300, but scale up linearly with cash
            scaled=math.ceil(min(300,3000*((close_price-upper_band)/upper_band)))
            stock.buy(scaled,counter=counter)
        elif close_price < lower_band:
            scaled=math.ceil(min(300,3000*((lower_band-close_price)/lower_band)))
            stock.sell(300-scaled, counter=counter)
    counter+=1
    daily_portfolio_value.append({(datetime.today().date()-timedelta(days=60-counter)):current_portfolio_value})
     
    peak=max(1000000, current_portfolio_value)
    drawdown_percentage = ((peak - current_portfolio_value) / peak) * 100
    drawdown_tracker.append({datetime.today().date()-timedelta(days=60-counter): drawdown_percentage})
    print(counter)
    
    return 




ax1.set_title('Portfolio Value Over Time')
ax1.set_xlabel('Day', fontsize=12)
ax1.set_ylabel('Portfolio Value (INR)')
ax1.set_ylim(950000,1050000)
ax1.autoscale(enable=True, axis='y', tight=True) 
 # Set y-axis to start from 0
  # Set y-axis to start from 0

ax2.set_title('Drawdown Over Time')
ax2.set_xlabel('Day',fontdict={'fontsize': 12})
ax2.set_ylim(0, 100)  # Set y-axis to start from 0
ax2.set_ylabel('Drawdown Percentage(INR)')
ax2.autoscale(enable=True, axis='y', tight=True)
  # Set y-axis to start from 0

ax3.set_title('Number of Shares Held Over Time')
ax3.set_xlabel('Stock')
ax3.set_ylabel('Number of Shares Held')
ax3.autoscale(enable=True, axis='y', tight=True) 
  # Set y-axis to start from 0
 
    

   


ani1=FuncAnimation(fig1,update,interval=1000,blit=False)

plt.show()









          
          
