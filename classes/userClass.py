from classes.modelClass import model, crudOperation
from DataBase.dbIndex import DB

class UserValue:
    def __set_name__(self, owner, value):
        self.__name = value
    def __set__(self, instance, value):
        instance.__dict__[self.__name] = value
    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]


class User(model):

    id = UserValue()
    Name = UserValue(),
    Surname = UserValue(),
    Mail = UserValue()

    def __init__(self):
        self.id = 0,
        self.Name = '',
        self.Surname = '',
        self.Mail = '',
        self.tableDataBase = 'Customers'

    def setAll(self, id, Name, Surname, Mail):
        self.id = id,
        self.Name = Name,
        self.Surname = Surname,
        self.Mail = Mail


    def SQLQuery(self,
                 crud,
                 fields,
                 where,
                 obj):
        db = DB()
        if (crud == crudOperation.Select):
            strq = 'SELECT ' + ' ' + fields + ' FROM ' + self.tableDataBase + ' ' + f' {"" if where == "" else " WHERE " + where} '
            customers = db.SELECT(strq)
            customers = self.ParseTupleToList(customers)
            return customers
        elif crud == crudOperation.Insert:
            strq = 'INSERT INTO ' + ' ' + self.tableDataBase + ' (id,Name,Surname,Mail) ' + \
                        f"VALUES ("  \
                        f"'{obj['userID']}', " \
                        f"'{obj['userName']}', " \
                        f"'{obj['userSurname'] if obj['userSurname'] != None else obj['userUsername']}', " \
                        f"'{obj['Mail']}'" \
                        f");"
            db.INSERT(strq)

    def ParseTupleToList(self, tuple):
        customers = list()
        for item in tuple:
            listCust = list(item)
            cust = User()
            print(listCust[0])
            cust.setAll(listCust[0], listCust[1], listCust[2], listCust[3])
            customers.append(cust)
        customers.reverse()
        return customers