Next On Docket:
    push to github
    start organizing modules into folders?
    use proper format for python project ie __init__.py stuff

config.json:
    when empty, be able to ask user for information aka username/password to write to config.json

cronjobs:
    figure out way to get webscraper to work on a minute basis without setting up crontab -e since a user won't be doing that


WebScraper:
    Get more detailed techincal analysis from different websites
    Perhaps integrate an api if its easy, otherwise, webscraping seems like a nice way to stay more anonmyous/set up (no API key required)
    Database of prices will need to change or have a joinable table that includes technical analysis numbers

Logger:
    Central all logger logic in here
    Make sure all modules actually use logger when appropriate
    See if I can add dates to the logger
    See if different modules can use a different "name" that is put after the date but before the info/error so we know what module is throwing what
    How to set line limit of log file/make a log1.log, log2.log, etc up to an arbitrarily set amount

IO:
    rename to Gui.py
    Start making a curses application - seems easier
    Maybe someone else can make a tkinter version
    Perhaps a way to serve it as HTML as well - might be best bet given I want to be able to see the information on my phone

Reports:
    schedule weekly on saturday at noon report of that weeks performance
    makes matplot lib into a reportonto a pdf

Notifications:
    make a method for emailing user
    make a method for texting user
    make a method for laptop notification
    make a method for phone notification somehow?

Database:
    convert to sqlite3 so that it can be part of an executable package (not possible with mysql)
    convert all current table definitions to sqlite3 syntax
    going to probably have to change queries slightly in data.py

db.py:
    add pruning logic - get rid of intermediary day prices (only keep open/close/max/low of day) after X days
    same goes for technical analysis whenit comes

Tests:
    write tests that confirm certain things like email/sms notifications and other things

CLI:
    way for user interact with the program to add tickers/shares to track and follow
    or to get current details/information
    Use click? 

API:
    create an py file that localizes all the commands a user is allowed to run

Users:
    do we want a managed userbase? or is this just for someone to download via commandline and 
    at very least, add single user name and password so that not anyone on network is able to access the data

Long Term:
    be able to make a website that displays all this stuff toa specificed user
