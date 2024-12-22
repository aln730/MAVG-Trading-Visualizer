"""
MAVGalgo.py
Author: zxcv / Arnav Gawas
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def get_stock_data(stock_symbol, start_date, end_date):
    """
    Downloads stock data for a given stock symbol from Yahoo Finance.
    """
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    stock_data.sort_index(inplace=True) 
    return stock_data

def add_moving_averages(stock_data, short_window, long_window):
    """
    Adds two moving averages to the stock data: a short one and a long one.
    """
    stock_data['short_mavg'] = stock_data['Adj Close'].rolling(window=short_window, min_periods=1).mean()
    stock_data['long_mavg'] = stock_data['Adj Close'].rolling(window=long_window, min_periods=1).mean()
    return stock_data

def generate_buy_sell_signals(stock_data, short_window, long_window):
    """
    Generates buy and sell signals based on the moving averages.
    """
    stock_data['signal'] = 0.0
    stock_data['signal'][short_window:] = np.where(stock_data['short_mavg'][short_window:] > stock_data['long_mavg'][short_window:], 1.0, 0.0)
    stock_data['positions'] = stock_data['signal'].diff()
    return stock_data

def plot_data(stock_data, short_window, long_window):
    """
    Plots the stock data along with buy and sell signals.
    """
    plt.figure(figsize=(12, 8))
    plt.plot(stock_data.index, stock_data['Adj Close'], label='Stock Price', color='black')
    plt.plot(stock_data.index, stock_data['short_mavg'], label=f'{short_window}-Day Moving Average', color='#E11C52')
    plt.plot(stock_data.index, stock_data['long_mavg'], label=f'{long_window}-Day Moving Average', color='#B0197E')
    
    plt.plot(stock_data[stock_data['positions'] == 1].index, stock_data['short_mavg'][stock_data['positions'] == 1], '^', markersize=10, color='green', lw=0, label='Buy Signal')
 
    plt.plot(stock_data[stock_data['positions'] == -1].index, stock_data['short_mavg'][stock_data['positions'] == -1], 'v', markersize=10, color='red', lw=0, label='Sell Signal')

    plt.title('Stock Trading Strategy (Moving Average Crossover)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.show()

def main():
    """
    Main function to run the trading strategy.
    It asks for user input, downloads stock data, calculates moving averages, and generates signals.
    """
    print("Welcome to the Stock Trading Strategy!")
    
    stock_symbol = input("Enter the stock ticker: ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    short_window = 5
    long_window = 20

    stock_data = get_stock_data(stock_symbol, start_date, end_date)
    
    if stock_data is not None:
        stock_data = add_moving_averages(stock_data, short_window, long_window)
        
        stock_data = generate_buy_sell_signals(stock_data, short_window, long_window)

        plot_data(stock_data, short_window, long_window)
    else:
        print("Sorry, couldn't get the stock data. Please check the stock symbol and dates.")


if __name__ == "__main__":
    main()

