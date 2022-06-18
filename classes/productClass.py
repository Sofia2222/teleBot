from classes.modelClass import model, crudOperation
from DataBase.dbIndex import DB

class ProductValue:
    def __set_name__(self, owner, value):
        self.__name = value
    def __set__(self, instance, value):
        instance.__dict__[self.__name] = value
    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]


class Product(model):

    id = ProductValue()
    NamePhoto = ProductValue(),
    Name = ProductValue(),
    CategoryId = ProductValue(),
    Description = ProductValue(),
    Price = ProductValue(),
    isSale = ProductValue(),
    percentSale = ProductValue(),
    countProd = ProductValue(),

    def __init__(self):
        self.id = 0
        self.NamePhoto = ''
        self.Name = ''
        self.CategoryId = 0
        self.Description = ''
        self.Price = 0
        self.isSale = bool
        self.percentSale = 0.0
        self.countProd = 0
        self.tableDataBase = 'Products'


    def setAll(self, id, NamePhoto, Name, CategoryId, Description, Price, isSale, percentSale, countProd):
        self.id = id
        self.NamePhoto = NamePhoto
        self.Name = Name
        self.CategoryId = CategoryId
        self.Description = Description
        self.Price = Price
        self.isSale = isSale
        self.percentSale = percentSale
        self.countProd = countProd
        self.tableDataBase = 'Products'

    def SQLQuery(self,
                 crud,
                 fields,
                 where,
                 reverse = 'yes'):
        db = DB()
        if(crud == crudOperation.Select):
            strq = 'SELECT ' + ' ' + fields + ' FROM ' + self.tableDataBase + ' ' + f' {"" if where == "" else " WHERE " +where} '
            prods = db.SELECT(strq)
            prods = self.ParseTupleToList(prods)
            if reverse == 'yes':
                prods.reverse()
            return prods



    def ParseTupleToList(self, tuple):
        products = list()
        for item in tuple:
            listProduct = list(item)
            prod = Product()
            print(listProduct[0])
            prod.setAll(listProduct[0], listProduct[1], listProduct[2], listProduct[3], listProduct[4], listProduct[5],
                        listProduct[6], listProduct[7], listProduct[8])
            products.append(prod)
        return products



