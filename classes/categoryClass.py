from classes.modelClass import model, crudOperation
from DataBase.dbIndex import DB

class categoryProdValue:
    def __set_name__(self, owner, value):
        self.__name = value
    def __set__(self, instance, value):
        instance.__dict__[self.__name] = value
    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]


class categoryProd(model):
    id = categoryProdValue()
    Name = categoryProdValue()
    idGlobalCategory = categoryProdValue()

    def __init__(self):
        self.id = 0
        self.Name = ''
        self.idGlobalCategory = 0
        self.tableDataBase = 'CategoryProd'

    def setAll(self, id, Name, idGlobalCategory):
        self.id = id
        self.Name = Name
        self.idGlobalCategory = idGlobalCategory
        self.tableDataBase = 'CategoryProd'

    def SQLQuery(self,
                 crud,
                 fields,
                 where):
        db = DB()
        if(crud == crudOperation.Select):
            strq = 'SELECT ' + ' ' + fields + ' FROM ' + self.tableDataBase + ' ' + f' {"" if where == "" else " WHERE " +where} '
            category = db.SELECT(strq)
            category = self.ParseTupleToList(category)
            return category

    def ParseTupleToList(self, tuple):
        categoryProdd = list()
        for item in tuple:
            listCategory = list(item)
            categg = categoryProd()
            print(listCategory[0])
            categg.setAll(listCategory[0], listCategory[1], listCategory[2])
            categoryProdd.append(categg)
        categoryProdd.reverse()
        return categoryProdd



