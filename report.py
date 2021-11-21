"""
Prints data to a pdf on  command, or scheduled.
Can be scheduled to be emailed.
"""
import matplotlib.pyplot as plt
import data
import datetime
import db

def runStatusReport():       
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=3)
    results = data.statusReport(1, start_date=start_date, end_date=end_date)
    return results


def singleStockPrice(ticker_id, start_date=None, end_date=None, minute_differential=None):
    """
    Args:
        ticker: int, id of the ticker inthe db
    """
    if end_date is None:
        end_date = datetime.datetime.now()
    if start_date is None and minute_differential is not None:
        start_date = end_date - datetime.timedelta(minutes=minute_differential)
    elif start_date is None:
        start_date = end_date - datetime.timedelta(minutes=10)
    price_data = data.getHistoricalPrices(ticker_id, start_date, end_date)
    symbol = price_data[0][0]
    prices = [float(price) for (symbol, dt, price) in price_data]
    startPrice = prices[0]
    endPrice = prices[-1]
    print(f"end price is {endPrice} start price is {startPrice}")
    dt =  [dt for (symbol, dt, price) in price_data]
    plt.plot(dt,prices, label=symbol)
    plt.ylabel(f"{symbol} Price")
    plt.xlabel("Time")
    plt.legend()
    plt.show()

def singleStockPortfolio(ticker_id, start_date=None, end_date=None):
    """
    Args:
        ticker: int, id of the ticker inthe db
    """
    if end_date is None:
        end_date = datetime.datetime.now()
    if start_date is None:
        start_date = end_date - datetime.timedelta(minutes=10)
    portfolio = data.getHistoricalPortfolioValues(ticker_id, start_date=start_date, end_date=end_date)
    symbol = portfolio[0][0]
    total_value = [round(current_value,2) for (symbol, dt, single_price, shares, current_value, total_cost_basis) in portfolio]
    dt = [dt for (symbol, dt, single_price, shares, current_value, cost_value) in portfolio]
    cost_basis = [round(total_cost_basis,2) for (symbol, dt, single_price, shares, current_value, total_cost_basis) in portfolio]
    plt.plot(dt, total_value, label=f'{symbol} Total Value')
    plt.plot(dt, cost_basis, label=f'{symbol} Cost Basis')
    plt.ylabel(f'Portfolio Value for {symbol}')
    plt.xlabel('Time')
    plt.legend()
    plt.show()

#'ETH.X', datetime.datetime(2021, 11, 19, 20, 11, 1), Decimal('4313.3400'), 12.9119, 55693.30592525483, 33932.406898498535)

def run():
    ticker_id = 1
    singleStockPortfolio(ticker_id)

if __name__ == "__main__":
    run()