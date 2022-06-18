from classes.modelClass import model, crudOperation
from DataBase.dbIndex import DB

class OrderValue:
    def __set_name__(self, owner, value):
        self.__name = value
    def __set__(self, instance, value):
        instance.__dict__[self.__name] = value
    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]

class Orders(model):
    id = OrderValue()
    idCust = OrderValue()
    idsProd = OrderValue()
    countProd = OrderValue()
    City = OrderValue()
    AdressNP = OrderValue()
    SumOrder = OrderValue()
    Phone = OrderValue()

    def __init__(self):
        self.id = 0
        self.idCust = 0
        self.idsProd = 0
        self.countProd = 0
        self.City = ''
        self.AdressNP = ''
        self.SumOrder = 0
        self.Phone = ''
        self.tableDataBase = 'Orders'

    def setAll(self, id, idCust, idsProd, countProd, City, AdressNP, SumOrder, Phone):
        self.id = id
        self.idCust = idCust
        self.idsProd = idsProd
        self.countProd = countProd
        self.City = City
        self.AdressNP = AdressNP
        self.SumOrder = SumOrder
        self.Phone = Phone


    def SQLQuery(self,
                 crud,
                 fields,
                 where,
                 obj):
        db = DB()
        if(crud == crudOperation.Select):
            strq = 'SELECT ' + ' ' + fields + ' FROM ' + self.tableDataBase + ' ' + f' {"" if where == "" else " WHERE " +where} '
            orders = db.SELECT(strq)
            orders = self.ParseTupleToList(orders)
            return orders
        elif crud == crudOperation.Insert:
            strq = 'INSERT INTO ' + ' ' + self.tableDataBase + ' (idCust, idsProd, countProd, City, AdressNP, SumOrder, Phone) ' + \
                   f"VALUES (" \
                   f"'{obj['idCust']}', " \
                   f"'{obj['idsProd']}', " \
                   f"'{obj['countProd']}', " \
                   f"'{obj['City']}'," \
                   f"'{obj['AdressNP']}',"\
                   f"'{obj['SumOrder']}'," \
                   f"'{obj['Phone']}'" \
                   f");"
            print(strq)
            db.INSERT(strq)
        elif crud == crudOperation.Update:
            strq = "UPDATE " + self.tableDataBase + f" SET Phone = '{obj['Phone']}'" \
                    f"WHERE idCust = {obj['idCust']} "
            db.UPDATE(strq)


    def ParseTupleToList(self, tuple):
        orders = list()
        for item in tuple:
            listOrders = list(item)
            ord = Orders()
            ord.setAll(listOrders[0], listOrders[1], listOrders[2], listOrders[3], listOrders[4], listOrders[5],
                        listOrders[6], listOrders[7])
            orders.append(ord)
        orders.reverse()
        return orders
