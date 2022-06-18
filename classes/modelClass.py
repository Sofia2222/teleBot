from enum import Enum

class crudOperation(Enum):
    Update = 'UPDATE'
    Insert = 'INSERT INTO'
    Select = 'SELECT'
    Delete = 'DELETE FROM'

class model:
    id:int
    tableDataBase:str

    def __init__(self):
        pass


