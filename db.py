"""
The database layer, extracted away.
"""
import json
import mysql.connector
from mysql.connector import errorcode
#import classes

class DatabaseError(Exception):
    pass

# Attempt 3
# TODO Make attempt three the official production code
from contextlib import closing
def runQuery(query):
    credentials = getCredentials()
    print(credentials)
    with closing(mysql.connector.connect(**credentials)) as conn:
        with closing(conn.cursor(buffered=True)) as cursor:
            cursor.execute(query)
            return cursor.fetchall().copy()

def runScalarQuery(query):
    try:
        return runQuery(query)[0][0]
    except IndexError as e:
        return None

def runUpdateQuery(query):
    credentials = getCredentials()
    with closing(mysql.connector.connect(**credentials)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(query)
            conn.commit()
# End of attempt 3 - 21 lines of code boy howdy


## Attempt #1 - so far, getCredentials is used in evey iteration until a better way is found
def getCredentials():
    # Returns username, password, connection string info - is this a bad idea?
    data = None
#   TODO fix the relative loading thing
#    with open('/home/github/StockWatcher/config.json', 'r') as f:
#        data = json.load(f)['db']
    data = {"db": {"user": "stock_watcher", "password": "StockWatcher!1234", "database":"stock_watcher","host":"localhost", }}
    return data['db']

def getConnection():
    config = getCredentials()
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong username/password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

def testConnection():
    results = runScalarQueryThree("SELECT 1")
    assert results == 1

if __name__ == '__main__':
    testConnection()
