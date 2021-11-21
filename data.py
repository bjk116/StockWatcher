"""
Localize database queries.
"""
import db
import datetime

def statusReport(ticker_id,start_date=None, end_date=None):
    """
    Report on how well often prices were recieved over the course
    of an hour.
    """
    if end_date is None:
        end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=3)
    query = f"""select YEAR(finished_t_stamp) as 'Year',
    MONTH(finished_t_stamp) as 'Month',
    DAY(finished_t_stamp) as 'Day',
    HOUR(finished_t_stamp) as 'Hour',
    if(count(*)>60,60,count(*)) as 'Count' 
    FROM prices 
    WHERE fk_symbol_id={ticker_id} AND 
    started_t_stamp < '{end_date}' and started_t_stamp >'{start_date}'
    GROUP BY YEAR(finished_t_stamp),MONTH(finished_t_stamp),DAY(finished_t_stamp),HOUR(finished_t_stamp);
    ORDER BY Year ASC, Month ASC, Day ASC, Hour ASC"""
    results = db.runQuery(query)
    return results

def getTickers():
    return db.runQuery("SELECT id, symbol FROM ticker")

def getCurrentTickerValues():
    query = """
    SELECT t.symbol, p.price, p.finished_t_stamp
    FROM prices p 
    LEFT JOIN ticker t ON t.id = p.fk_symbol_id 
    WHERE (p.started_t_stamp,p.fk_symbol_id) IN (SELECT MAX(started_t_stamp), fk_symbol_id FROM prices GROUP BY fk_symbol_id);
    """
    return db.runQuery(query)

def getHistoricalPrices(ticker_id, start_date, end_date):
    """
    Gets historical prices for the different stocks in ticker table.
    Args:
        ticker_id: inselect t, id of the ticker whos price you want
        start_date: datetime
        end_date: datetime
    Returns:
        List of tuples (str: Symbol, dt timeofprice, float price) 
        [("ETH.X", "2021-11-19 17:21:01", 4010.9500),...]
    """
    query = f"select t.symbol, p.started_t_stamp, p.price from prices p JOIN ticker t ON p.fk_symbol_id = t.id where fk_symbol_id = {ticker_id} AND started_t_stamp > '{start_date}' AND started_t_stamp < '{end_date}' order by p.id desc;"
    results = db.runQuery(query)
    # Should this get parsed somehow? Datetime objec and decimal objects. 
    return results

def getHistoricalPortfolioValues(ticker_id, start_date=None, end_date=None):
    """
    Returns a dataset of values consisting of the shares at the time
    multiplied by the shares at the time to create the portfolio value at the moment.
    Args:
        start_date: datetime, if none dfaults to now
        end_date: datetime, if none, defaultes to 10 minutes ago
    Returns:
        [('ETH.X'), ("2021-11-19 19:59:00", 4200.24, 12.91), ()] 
    """
    query = f"""select t.symbol, p.started_t_stamp, p.price, ps.shares, p.price*ps.shares, ps.shares*ps.cost_basis from prices p JOIN ticker t ON p.fk_symbol_id = t.id JOIN positions ps ON p.fk_symbol_id = ps.fk_symbol_id WHERE p.fk_symbol_id = {ticker_id} ORDER BY p.id DESC LIMIT 10;"""
    results = db.runQuery(query)
    return results

def getPortfolio(as_of_date=None, with_subtotals=False):
    """
    Gets latest price of tickers joined with positions so that we only return profits/losses
    on shares that the user actually owns.
    Args:
        as_of_date: datetime, if None then current time
        with_subtotals: bool flag - if false, don't return row with subtotals, if true, do
    Returns:
        list[(tuples)]
    TO DO: Move subtotals to a generic function on datasets
    """
    if as_of_date is None:
        as_of_date = datetime.datetime.now()
    query = f"SELECT t.symbol as 'Ticker', ps.cost_basis as 'Cost Basis',p.price as 'Current Price',ROUND(p.price - ps.cost_basis, 4) as 'Per Share P\L', ps.shares as 'Shares', ROUND(ps.shares*p.price,4) as 'Current Value', ROUND(ps.shares*(p.price-ps.cost_basis),4) as 'Total P\L' FROM prices p JOIN positions ps ON p.fk_symbol_id = ps.fk_symbol_id JOIN ticker t ON p.fk_symbol_id = t.id WHERE (p.started_t_stamp,p.fk_symbol_id) IN (SELECT MAX(started_t_stamp), fk_symbol_id FROM prices WHERE finished_t_stamp<='{as_of_date}'  GROUP BY fk_symbol_id)"
    data = db.runQuery(query)
    if not with_subtotals:
        return data
    total_portfolio_value = 0
    total_portfolio_profit = 0.0
    try:
        for (symbol, cost_basis, cur_price, per_share_proft, shares, total_value, total_profit) in data:
            total_portfolio_value += total_value
            total_portfolio_profit += total_profit
        data.append(('-','-','-','-','-',round(total_portfolio_value,2), round(total_portfolio_profit,2)))
    except ValueError as e:
        # To Do - log error
        print(str(e))
    return data

def calculatePortfolioPerformance(start_date, end_date):
    """
    Calculates performance of the portfolio over the last x days;
    Args:
        days: datetime, how many days backwards do you want to go?
        startDate: datetime, the last day of permance measured, if None defaults to today
    Retruns:
        Maybe a dictionary?
        {
            "starting_values" : {},
            "ending_value" : {},
            "difference" : {} TODO make statistics that are put here
        }
    """
    start_portfolio = getPortfolio(as_of_date=start_date, with_subtotals=True)
    end_portfolio = getPortfolio(as_of_date=end_date, with_subtotals=True)
    start_subtotals = start_portfolio[-1]
    end_subtotals = end_portfolio[-1]
    start_value = start_subtotals[-2]
    end_value = end_subtotals[-2]
    difference = end_value - start_value
    print(f"""
    {start_date}: {start_value}
    {end_date}: {end_value}
    difference: {difference}
    """)
    return start_subtotals, end_subtotals

def calculatePerformanceFor(end_date=None):
    """
    Handles the date logic for perofmrances.
    """
    if end_date is None:
        end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=4)
    calculatePortfolioPerformance(start_date, end_date)

def getCurrentPrice(ticker_id):
    """
    Gets latest price for the ticker_id
    """
    return db.runScalarQuery(f"SELECT price FROM prices WHERE fk_symbol_id = {ticker_id} ORDER BY id desc limit 1")