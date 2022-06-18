from classes.modelClass import model, crudOperation
from DataBase.dbIndex import DB

class categoryGlobalProdValue:
    def __set_name__(self, owner, value):
        self.__name = value
    def __set__(self, instance, value):
        instance.__dict__[self.__name] = value
    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]


class categoryGlobalProd(model):
    id = categoryGlobalProdValue()
    Name = categoryGlobalProdValue()

    def __init__(self):
        self.id = 0
        self.Name = ''
        self.tableDataBase = 'GlobalCategory'

    def setAll(self, id, Name):
        self.id = id
        self.Name = Name
        self.tableDataBase = 'CategoryProd'

    def SQLQuery(self,
                 crud,
                 fields,
                 where):
        db = DB()
        if(crud == crudOperation.Select):
            strq = 'SELECT ' + ' ' + fields + ' FROM ' + self.tableDataBase + ' ' + f' {"" if where == "" else " WHERE " +where} '
            categoryGlobal = db.SELECT(strq)
            categoryGlobal = self.ParseTupleToList(categoryGlobal)
            return categoryGlobal

    def ParseTupleToList(self, tuple):
        ctg = list()
        for item in tuple:
            listCategory = list(item)
            categ = categoryGlobalProd()
            print(listCategory[0])
            categ.setAll(listCategory[0], listCategory[1])
            ctg.append(categ)
        ctg.reverse()
        return ctg