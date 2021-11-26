"""
For classes related to database and general concerns.
"""
import db

class Dataset():
    data = None
    columns = None
    statement = None
    def __init__(self, cursor):
        print(f"copying cursor data over")
        self.data = cursor.fetchall().copy()
        print(f"{self.data}")
        self.columns = cursor.column_names
        self.statement = cursor.statement
    
    def __iter__(self):
        """Since self.data is just a list, lets use that
        same iterator a list has"""
        return self.data.__iter__()
    
    def __getitem__(self):
        return self.data.__getitem__(self.data)

class Record():
    def __init__(self):
        self.checkDBTablExistence()
    
    def checkDBTablExistence(self):
        # TODO is this even necessary.  Calculating the db table name is, but checking existence is just for fun.
        className = self.__class__.__name__
        
        className = f"{className.lower()}s"

        query = f"SELECT COUNT(*) FROM information_schema.tables  WHERE table_schema = 'stock_watcher' AND table_name = '{className}';"
        print(query)
        result = db.runScalarQuery(query)
        print("Result: ", str(result))

class Notification(Record):
    pass

class Price(Record):
    pass