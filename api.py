from fastapi import FastAPI
import data
import webscraper

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Hello world"
    }

@app.get("/latest")
def latest_prices():
    latest_prices = data.getCurrentTickerValues()
    return {
        "data": latest_prices
    }

@app.post("/scrape")
def scrape_prices_now():
    webscraper.main()
    return {
        "message":"success",
        "errors":None
    }