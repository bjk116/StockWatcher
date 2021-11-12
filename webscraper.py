import requests
from bs4 import BeautifulSoup
import logging
import datetime
import sys
import db

BASE_URL = "https://stocktwits.com/symbol/"

logging.basicConfig(filename='log.log', level=logging.DEBUG)

def getPrice(ticker='ETH.X'):
    """
    Returns price of ticker,or raises ValueError if price cannot be cast to float or an AttributeError if the tag is not properly found.
    Args:
        ticker: stock ticker as found in url stocktwits.com/SYMBOL/tickerHere
    Returns:
        price: float, price of ticker per stocktwits
            or
        raises ValueError if price is not decipherable, raises AttributeError if the proper HTML tag cannot be found
    """
    ticker_url = BASE_URL + ticker
    s = requests.Session()
    r = s.get(f"{ticker_url}")
    soup = BeautifulSoup(r.text, 'html.parser')
    ticker_text = soup.find('span', string=ticker)
    return float(ticker_text.nextSibling.text)

def savePrice(dt, price, db_id):
    formatted_dt = dt.strftime("%Y-%m-%d %H:%M:%S")
    query = f"INSERT INTO prices (price, fk_symbol_id, started_t_stamp) VALUES ({price}, {db_id}, '{formatted_dt}')"
    db.runUpdateQuery(query)

def getAndStorePrices():
    """
    Main application loop.
    """
    tickers = db.runQuery("SELECT id, symbol FROM ticker")
    for (db_id, ticker) in tickers:
        current_time = datetime.datetime.now()
        price = getPrice(ticker)
        savePrice(current_time, price, db_id)
        
if __name__ == '__main__':
#    command = sys.argv[1]
    noErrors = True
    logging.info("Running app.py")
    print("Running app.py")
#    if command == 'getAndSave':
    if True:
        try:
            getAndStorePrices()
        except Exception as e:
            print("unexpected error during get and store prices")
            logging.error("Unexpected error occured while running get and Store prices")
            logging.error(e)
            noErrors = False
        finally:
            if noErrors:
                print("Completed withuot errors")
            else:
                print("Completed with errors")

