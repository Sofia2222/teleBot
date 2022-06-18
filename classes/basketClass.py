from classes.modelClass import model, crudOperation
from DataBase.dbIndex import DB

class BasketItem:
    def __set_name__(self, owner, value):
        self.__name = value

    def __set__(self, instance, value):
        instance.__dict__[self.__name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]

class Basket:
    id = BasketItem()
    idCust = BasketItem()
    idsProd = BasketItem()
    SumOrder = BasketItem()
    countsProd = BasketItem()

    def __init__(self):
        self.id = 0
        self.idCust = ''
        self.idsProd = ''
        self.SumOrder = 0.0
        self.countsProd = 0
        self.tableDataBase = 'Basket'


    def setAll(self, id, idCust, idsProd, SumOrder, countsProd):
        self.id = id
        self.idCust = idCust
        self.idsProd = idsProd
        self.SumOrder = SumOrder
        self.countsProd = countsProd

    def SQLQuery(self,
                 crud,
                 fields,
                 where,
                 obj):
        db = DB()
        if (crud == crudOperation.Select):
            strq = 'SELECT ' + ' ' + fields + ' FROM ' + self.tableDataBase + ' ' + f' {"" if where == "" else " WHERE " + where} '
            baskets = db.SELECT(strq)
            baskets = self.ParseTupleToList(baskets)
            return baskets
        elif crud == crudOperation.Insert:
            strq = 'INSERT INTO ' + self.tableDataBase + ' (idCust, idsProd, SumOrder, CountsProd) ' + \
                   f"VALUES (" \
                   f" '{obj['idCust']}', " \
                   f" '{str(obj['idsProd'])}', " \
                   f" '{obj['SumOrder']}', " \
                   f" '{obj['countsProd']}'" \
                   f");"
            db.INSERT(strq)
        elif crud == crudOperation.Update:
            strq = "UPDATE " + self.tableDataBase + " SET" + f" idsProd = '{obj['idsProd']}' ,SumOrder = {obj['SumOrder']}, CountsProd = '{obj['countsProd']}' " \
                    f"WHERE idCust = {obj['idCust']} "
            db.UPDATE(strq)
        elif crud == crudOperation.Delete:
            strq = 'DELETE FROM' + ' ' + self.tableDataBase + ' ' + 'WHERE ' + where
            db.DELETE(strq)

    def ParseTupleToList(self, tuple):
        baskets = list()
        for item in tuple:
            listBasket = list(item)
            bask = Basket()
            print(listBasket[0])
            bask.setAll(listBasket[0], listBasket[1], listBasket[2], listBasket[3], listBasket[4])
            baskets.append(bask)
        baskets.reverse()
        return baskets



