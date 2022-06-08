class BasketItem:
    def __set_name__(self, owner, value):
        self.__name = value

    def __set__(self, instance, value):
        instance.__dict__[self.__name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.__name]

class Basket:
    idsProd = []
    SumOrder = BasketItem()
    idCust = BasketItem()

    def __init__(self, idCust):
        self.idsProd = list()
        self.idCust = idCust
        self.SumOrder = 0

    def __add__(self, other):
        self.idsProd.append(other['id'])
        self.SumOrder = self.SumOrder + other['price']



