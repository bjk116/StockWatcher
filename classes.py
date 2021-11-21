"""
For classes related to database and general concerns.
"""
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