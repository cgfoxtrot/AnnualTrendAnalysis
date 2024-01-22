import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from collections import defaultdict

def fetch_stock_data(ticker_symbol, start_date, end_date):
    try:
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
        if stock_data.empty:
            raise ValueError("No data returned for given dates.")
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {str(e)}")
        return None

def analyze_stock_data(stock_data):
    if stock_data is None or stock_data.empty:
        print("No data available for analysis.")
        return None

    stock_data['Year'] = stock_data.index.year
    stock_data['Month'] = stock_data.index.month

    monthly_details = {}
    monthly_averages = defaultdict(list)
    monthly_change_usd = []
    for year in sorted(stock_data['Year'].unique()):
        monthly_details[year] = {}
        yearly_data = stock_data[stock_data['Year'] == year]
        for month in range(1, 13):
            month_data = yearly_data[yearly_data['Month'] == month]
            if not month_data.empty:
                price_change = month_data['Adj Close'].iloc[-1] - month_data['Adj Close'].iloc[0]
                price_change_percent = (price_change / month_data['Adj Close'].iloc[0]) * 100
                monthly_details[year][month] = (price_change, price_change_percent)
                monthly_averages[month].append(price_change_percent)
                monthly_change_usd.append(price_change)

    for month in monthly_averages:
        avg_change_percent = np.mean(monthly_averages[month])
        monthly_averages[month] = avg_change_percent

    avg_monthly_change_percent = np.mean(list(monthly_averages.values()))
    avg_monthly_change_usd = np.mean(monthly_change_usd)
    avg_yearly_change_percent = avg_monthly_change_percent * 12
    avg_yearly_change_usd = avg_monthly_change_usd * 12

    return monthly_details, monthly_averages, avg_monthly_change_usd, avg_yearly_change_usd, avg_monthly_change_percent, avg_yearly_change_percent

def print_analysis_results(ticker_symbol, start_date, end_date, monthly_details, monthly_averages, avg_monthly_change_usd, avg_yearly_change_usd, avg_monthly_change_percent, avg_yearly_change_percent):
    print(f"Analysis Results for {ticker_symbol} from {start_date} to {end_date}:")
    print("-" * 40)
    print(f"Average Monthly Trend (USD): ${avg_monthly_change_usd:.2f}")
    print(f"Average Monthly Trend (%): {avg_monthly_change_percent:.2f}%")
    print(f"Average Yearly Trend (USD): ${avg_yearly_change_usd:.2f}")
    print(f"Average Yearly Trend (%): {avg_yearly_change_percent:.2f}%")
    print("-" * 40)

def plot_cumulative_monthly_averages(ticker_symbol, monthly_averages):
    months = [datetime(2000, month, 1).strftime("%B") for month in range(1, 13)]
    average_changes = [monthly_averages[month] for month in range(1, 13)]
    cumulative_changes = np.cumsum(average_changes)
    
    plt.figure(figsize=(12, 6))
    plt.plot(months, cumulative_changes, marker='o', linestyle='-')
    title = f'Cumulative Monthly Average Changes in % for {ticker_symbol}'
    plt.title(title)
    plt.xlabel('Month')
    plt.ylabel('Cumulative Change in %')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

def main():
    print("\nWelcome to the Financial Securities Trend Analysis Tool\n")
    
    print("Examples of Ticker Symbols:")
    print("  - Stocks: AAPL (Apple), MSFT (Microsoft), TSLA (Tesla)")
    print("  - Indices: ^GSPC (S&P 500), ^DJI (Dow Jones Industrial Average), ^IXIC (NASDAQ Composite)")
    print("  - Cryptocurrencies: BTC-USD (Bitcoin), ETH-USD (Ethereum)")
    print("  - Commodities: CL=F (Crude Oil Futures), GC=F (Gold Futures)\n")

    ticker_symbol = input("Enter the ticker symbol (e.g., AAPL, ^GSPC): ").strip().upper()
    start_date = input("Enter the start date (YYYY-MM-DD format): ")
    end_date = input("Enter the end date (YYYY-MM-DD format): ")

    stock_data = fetch_stock_data(ticker_symbol, start_date, end_date)
    if stock_data is not None:
        monthly_details, monthly_averages, avg_monthly_change_usd, avg_yearly_change_usd, avg_monthly_change_percent, avg_yearly_change_percent = analyze_stock_data(stock_data)
        print_analysis_results(ticker_symbol, start_date, end_date, monthly_details, monthly_averages, avg_monthly_change_usd, avg_yearly_change_usd, avg_monthly_change_percent, avg_yearly_change_percent)
        plot_cumulative_monthly_averages(ticker_symbol, monthly_averages)

if __name__ == "__main__":
    main()

