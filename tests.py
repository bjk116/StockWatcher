"""
For testing out our code.
"""
import db
import webscraper
import datetime

def testDatasources():
    db.testConnection()

def testWebScraperStatus():
    tickers = db.runQuery("SELECT id, symbol FROM ticker")
    # Attempt 1 - just see if you can webscrape at the current moment
    # for (db_id, ticker) in tickers:
    #     try:
    #         price = webscraper.getPrice(ticker)
    #     except AttributeError as e:
    #         raise ScrapingError(f"Error scraping price for ticker {ticker}, cannot find price tag.")
    #     except ValueError as e:
    #         raise ScrapingError(f"HTML Tag does not contain parseable float to be the price of {ticker}") 

def testPriceSaving():
    # Attempt 2 - check and see if the latest price of all the most recent tickers are less than 60 seconds away from the current time
    tickers = db.runQuery("SELECT id, symbol FROM ticker")
    current_t_stamp = datetime.datetime.now()
    for (db_id, ticker) in tickers:
        last_t_stamp = db.runScalarQueryThree(f"SELECT started_t_stamp FROM prices WHERE fk_symbol_id={db_id} ORDER BY id DESC limit 1;")
        print(f"{last_t_stamp} and type is {type(last_t_stamp)}")
        diff = current_t_stamp - last_t_stamp
        assert diff.seconds < 60

if __name__ == "__main__":
    testPriceStatus()