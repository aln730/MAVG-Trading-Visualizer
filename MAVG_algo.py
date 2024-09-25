import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def download_stock_data(stock, date_start, date_end): #Download stock data from Yahoo Finance.

    stock_data = yf.download(stock, start=date_start, end=date_end)
    stock_data.sort_index(inplace=True)
    return stock_data

def calculate_moving_averages(stock_data, short_window, long_window): #Calculate short and long moving averages.

    stock_data['short_mavg'] = stock_data['Adj Close'].rolling(window=short_window, min_periods=1).mean()
    stock_data['long_mavg'] = stock_data['Adj Close'].rolling(window=long_window, min_periods=1).mean()
    return stock_data

def generate_signals(stock_data, short_window, long_window): #Generate buy and sell signals based on moving averages.

    stock_data['signal'] = 0.0
    stock_data['signal'][short_window:] = np.where(stock_data['short_mavg'][short_window:] > stock_data['long_mavg'][short_window:], 1.0, 0.0)
    stock_data['positions'] = stock_data['signal'].diff()
    return stock_data

def plot_trading_strategy(stock_data, short_window, long_window): #Plot the trading strategy with buy and sell signals.
    plt.figure(figsize=(12, 8))
    plt.plot(stock_data.index, stock_data['Adj Close'], label='Adjusted Close Price', color='black')
    plt.plot(stock_data.index, stock_data['short_mavg'], label=f'{short_window}-Day Moving Average', color='blue')
    plt.plot(stock_data.index, stock_data['long_mavg'], label=f'{long_window}-Day Moving Average', color='red')
    plt.plot(stock_data[stock_data['positions'] == 1].index, stock_data['short_mavg'][stock_data['positions'] == 1], '^', markersize=10, color='green', lw=0, label='Buy Signal')
    plt.plot(stock_data[stock_data['positions'] == -1].index, stock_data['short_mavg'][stock_data['positions'] == -1], 'v', markersize=10, color='red', lw=0, label='Sell Signal')

    plt.title('Trading Strategy (Moving Average Crossover)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.show()

# Main function to execute the trading strategy
def main():
    # Input from user
    stock = input("Enter the stock name: ")
    date_start = input("Enter the Start Date (YYYY-MM-DD): ")
    date_end = input("Enter the End Date (YYYY-MM-DD): ")

    # Define short and long windows
    short_window = 25
    long_window = 100

    # Execute functions
    stock_data = download_stock_data(stock, date_start, date_end)
    stock_data = calculate_moving_averages(stock_data, short_window, long_window)
    stock_data = generate_signals(stock_data, short_window, long_window)  # Pass the new parameters
    plot_trading_strategy(stock_data, short_window, long_window)

# Run the main function
main()

