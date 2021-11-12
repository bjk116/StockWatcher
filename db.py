"""
The database layer, extracted away.
"""
import json
import mysql.connector
from mysql.connector import errorcode

class DatabaseError(Exception):
    pass

def getCredentials():
    # Returns username, password, connection string info - is this a bad idea?
    data = None
    with open('config.json', 'r') as f:
        data = json.load(f)['db']
    return data

def getConnection():
    config = getCredentials()
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connctor.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong username/password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

def runQuery(query):
    # To do - parser for to check there is no update/insert/delete/create etc
    cnx = getConnection()
    if cnx is not None:
        try:
            cursor = cnx.cursor()
            cursor.execute(query)
#            for row in cursor:
#                print(row)
            return cursor.fetchall().copy()
        except Exception as e:
            print(f"Error when trying to run query: {query}")
            print(e)
        finally:
            cursor.close()
            cnx.close()
    else:
        raise DatabaseError("Database cannot be connected to at this time")

def runScalarQuery(query):
    try:
        return runQuery(query)[0][0]
    except IndexError as e:
        # Log
        return None

def runUpdateQuery(query):
    cnx = getConnection()
    if cnx is not None:
        try:
            cursor = cnx.cursor()
            cursor.execute(query)
            cnx.commit()
        except Exception as e:
            print(f"something went wrong when running update query: {query}")
            print(e)
        finally:
            cursor.close()
            cnx.close()

def testConnection():
    results = runQuery("SELECT 1")
    assert results[0][0] == 1

if __name__ == '__main__':
    testConnection()
